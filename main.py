import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "chatting"))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from chat import manager, get_ai_response

app = FastAPI()
templates = Jinja2Templates(directory="chatting/templates")


@app.get("/chat", response_class=HTMLResponse)
async def create_chat(request: Request):
    session_id = str(uuid.uuid4())
    return templates.TemplateResponse(request, "chat.html", {
        "session_id": session_id
    })



@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    try:
        while True:
            user_message = await websocket.receive_text()
            await manager.send(session_id, f"고객: {user_message}")

            ai_reply = await get_ai_response(session_id, user_message)
            await manager.send(session_id, f"AI: {ai_reply}")
    except WebSocketDisconnect:
        manager.disconnect(session_id)
