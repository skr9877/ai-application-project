from fastapi import WebSocket


class SessionManager:
    def __init__(self):
        # session_id -> WebSocket
        self.sessions: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.sessions[session_id] = websocket

    def disconnect(self, session_id: str):
        self.sessions.pop(session_id, None)

    async def send(self, session_id: str, message: str):
        ws = self.sessions.get(session_id)
        if ws:
            await ws.send_text(message)


async def get_ai_response(session_id: str, user_message: str) -> str:
    # TODO: 여기에 회사 AI 모델 연결
    return f"(AI 미연결) 입력하신 내용: {user_message}"


manager = SessionManager()
