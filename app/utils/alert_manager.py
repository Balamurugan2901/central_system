from typing import List
from fastapi import WebSocket

class AlertManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self.connections.remove(ws)

    async def broadcast(self, message: dict):
        for conn in self.connections:
            await conn.send_json(message)


alert_manager = AlertManager()

def build_action_message(ip: str, action: str):
    return {
        "action": action,
        "ip": ip,
        "timestamp": datetime.utcnow().isoformat()
    }

