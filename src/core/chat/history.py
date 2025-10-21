# src/core/chat/history.py
import os
import json
import uuid
import psycopg
from psycopg import sql
from contextlib import asynccontextmanager
from typing import List, AsyncGenerator, Sequence, Optional
from dotenv import load_dotenv
from langchain_postgres import PostgresChatMessageHistory
from langchain_core.messages import (
    BaseMessage,
    messages_from_dict,
    message_to_dict,
)
from src.core.utils.constants import CHAT_HISTORY_TABLE
# --- Environment Setup ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
load_dotenv(os.path.join(BASE_DIR, ".env"))

DATABASE_URL = os.getenv("DATABASE_URL")


# --- Custom Async Chat History ---
class LimitedAsyncPostgresChatMessageHistory(PostgresChatMessageHistory):
    """
    Async Postgres chat history with message limit.
    Uses psycopg.AsyncConnection explicitly for async operations.
    """

    def __init__(self, session_id: str, conn_str: str, limit: int = 10):
        # Base class still needs a sync connection
        sync_conn = psycopg.connect(conn_str)
        super().__init__(CHAT_HISTORY_TABLE, session_id, sync_connection=sync_conn)
        self.conn_str = conn_str
        self.limit = limit

    # --- Async Connection Manager ---
    @asynccontextmanager
    async def async_client(self) -> AsyncGenerator[psycopg.AsyncConnection, None]:
        conn = await psycopg.AsyncConnection.connect(conninfo=self.conn_str)
        try:
            yield conn
        finally:
            await conn.close()

    # --- SQL Helpers ---
    @staticmethod
    def _insert_message_query(table_name: str) -> sql.Composed:
        return sql.SQL(
            "INSERT INTO {table_name} (session_id, message) VALUES (%s, %s)"
        ).format(table_name=sql.Identifier(table_name))

    # --- Async Overrides ---
    async def aget_messages(self) -> List[BaseMessage]:
        """Fetch last N messages (chronological order)."""
        query = sql.SQL(
            """
            SELECT message
            FROM {table}
            WHERE session_id = %(session_id)s
            ORDER BY id DESC
            LIMIT %(limit)s;
            """
        ).format(table=sql.Identifier(self._table_name))

        async with self.async_client() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, {"session_id": self._session_id, "limit": self.limit})
                rows = await cur.fetchall()

    # rows -> list of tuples, each with (message_json,)
        message_dicts = [row[0] for row in rows]
        #print(message_dicts)
        return messages_from_dict(message_dicts[::-1])  # reverse back to chronological

    async def aadd_messages(self, messages: Sequence[BaseMessage]) -> None:
        """Add messages asynchronously."""
        values = [
            (self._session_id, json.dumps(message_to_dict(m))) for m in messages
        ]

        async with self.async_client() as conn:
            query = self._insert_message_query(self._table_name)
            async with conn.cursor() as cur:
                await cur.executemany(query, values)
            await conn.commit()


# --- Factory Function ---
def get_by_session_id(session_id: Optional[str] = None, limit: int = 10):
    """
    Create a LimitedAsyncPostgresChatMessageHistory for a given session.
    """
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL missing in environment variables")

    sid = session_id or str(uuid.uuid4())
    return LimitedAsyncPostgresChatMessageHistory(sid, conn_str=DATABASE_URL, limit=limit)
