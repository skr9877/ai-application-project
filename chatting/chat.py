from fastapi import WebSocket

MAX_CONNECTIONS = 100


class SessionManager:
    def __init__(self):
        # session_id -> WebSocket
        self.sessions: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str) -> bool:
        if len(self.sessions) >= MAX_CONNECTIONS:
            await websocket.accept()
            await websocket.send_text("SYSTEM:서버가 혼잡합니다. 잠시 후 다시 시도해주세요.")
            await websocket.close()
            return False
        await websocket.accept()
        self.sessions[session_id] = websocket
        return True

    def disconnect(self, session_id: str):
        self.sessions.pop(session_id, None)

    async def send(self, session_id: str, message: str):
        ws = self.sessions.get(session_id)
        if ws:
            await ws.send_text(message)

    def current_connections(self) -> int:
        return len(self.sessions)


async def get_ai_response(session_id: str, user_message: str) -> str:
    from ai.serve.model import generate_response
    from ai.core.rag import get_context
    context = get_context(user_message)
    return await generate_response(user_message, context)


manager = SessionManager()
