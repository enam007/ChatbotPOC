from fastapi import FastAPI
from src.core.routes import chat_routes

app = FastAPI(title="RoomsAI Agent API")

# Include routes
#app.include_router(run.router)

# Include chat routes
app.include_router(chat_routes.router)
