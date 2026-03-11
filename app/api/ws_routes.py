from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.database.models import IntrusionLog, Client
from app.database.crud import get_db
import json

router = APIRouter()

class ConnectionManager:

    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, client_ip: str):
        await websocket.accept()
        self.active_connections[client_ip] = websocket
        print(f"Agent connected: {client_ip}")

    def disconnect(self, client_ip: str):
        if client_ip in self.active_connections:
            del self.active_connections[client_ip]
            print(f"Agent disconnected: {client_ip}")

    async def send_command(self, client_ip: str, command: dict):
        if client_ip in self.active_connections:
            await self.active_connections[client_ip].send_json(command)


manager = ConnectionManager()


@router.websocket("/ws/agent")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    try:

        while True:

            data = await websocket.receive_text()
            data = json.loads(data)

            print("Received intrusion event:", data)

            client_ip = data.get("client_ip")

            # DB session
            db: Session = next(get_db())

            # find client
            client = db.query(Client).filter(Client.ip_address == client_ip).first()

            if not client:
                print("Unknown client")
                continue

            intrusion = IntrusionLog(
                src_ip=data.get("src_ip"),
                packet_rate=data.get("packet_rate"),
                failed_logins=data.get("failed_logins"),
                attack_type=data.get("event"),
                risk_score=data.get("risk_score"),
                risk_level=data.get("risk_level"),
                action=data.get("action"),
                client_id=client.id
            )

            db.add(intrusion)
            db.commit()

            print("Intrusion stored in database")

    except WebSocketDisconnect:

        print("Agent disconnected")