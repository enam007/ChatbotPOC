from fastapi import FastAPI
from src.core.routes import chat_routes


from dotenv import load_dotenv
import os

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "prod")  # default to prod

def setup_langsmith_tracing():
    if APP_ENV == "dev":
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "ChatbotPOC")
        os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")
        print("✅ LangSmith tracing ENABLED (dev mode)")
    else:
        # remove tracing in prod
        os.environ.pop("LANGCHAIN_TRACING_V2", None)
        os.environ.pop("LANGCHAIN_PROJECT", None)
        os.environ.pop("LANGCHAIN_API_KEY", None)
        print("🚫 LangSmith tracing DISABLED (prod mode)")
setup_langsmith_tracing()

if os.getenv("LANGCHAIN_TRACING_V2") == "true":
    from langsmith import Client
    client = Client()
else:
    client = None
app = FastAPI(title="RoomsAI Agent API")

# Include routes
#app.include_router(run.router)

# Include chat routes
app.include_router(chat_routes.router)
