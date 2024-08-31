from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

router = APIRouter(prefix="/chat", tags=["Chat"])
templates = Jinja2Templates(directory="app/templates")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@router.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request, "title": "Chat with AI"})

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    chat = model.start_chat(history=[])
    try:
        while True:
            data = await websocket.receive_text()

            if data:
                if data.lower() == "exit":
                    await websocket.send_text("Ending chat session.")
                    break
                response = chat.send_message(data, stream=True)
                full_response = ""
                for chunk in response:
                    full_response += chunk.text
                await websocket.send_text(full_response)
    except WebSocketDisconnect:
        print("Client disconnected")
    finally:
        await websocket.close()
