from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not found in environment variables")

router = APIRouter(prefix="/chat", tags=["Chat"])
templates = Jinja2Templates(directory="app/templates")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@router.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request, "title": "Chat with Gemini AI"})

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    chat = model.start_chat(history=[])
    try:
        while True:
            data = await websocket.receive_text()

            if not data:
                continue

            if data.lower() == "exit":
                await websocket.send_text("Ending chat session.\n")
                break

            try:
                response = chat.send_message(data, stream=True)
                for chunk in response:
                    await websocket.send_text(chunk.text)
                
                await websocket.send_text("\n")

            except Exception as e:
                await websocket.send_text(f"Error: {str(e)}\n")

    except WebSocketDisconnect:
        print("Client disconnected")
    finally:
        await websocket.close()
