import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routes import chat
from fastapi.staticfiles import StaticFiles

load_dotenv()

API_KEY = os.getenv("API_KEY")

app = FastAPI(
    title="AI Chat API",
    docs_url='/',
    description="This API allows you to chat with an AI model using WebSocket connections.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

