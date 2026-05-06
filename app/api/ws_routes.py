from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.database.models import IntrusionLog, Client, PolicyDecision
from app.database.crud import get_db
from app.intrusion.ml_engine import predict_action
from app.policy.decision_engine import process_agentic_action
from app.core.blocking_engine import block_ip

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
            
            # Predict the autonomous action using the Agentic ML Model
            predicted_action = predict_action(
                packet_rate=data.get("packet_rate", 0), 
                failed_logins=data.get("failed_logins", 0)
            )

            client_id = data.get("agent_id") or data.get("client_id") # Support both for backwards compatibility

            # DB session
            db: Session = next(get_db())

            # find client
            client = db.query(Client).filter(Client.id == client_id).first()

            if not client:
                print("Unknown client")
                continue

            intrusion = IntrusionLog(
                src_ip=data.get("ip", data.get("src_ip", "0.0.0.0")),
                packet_rate=data.get("packet_rate", 0),
                failed_logins=data.get("failed_logins", 0),
                attack_type=data.get("event", data.get("attack_type", "Unknown")),
                risk_score=0.0, # Deprecated
                risk_level="Unknown", # Deprecated
                action=predicted_action, # Set the action from the ML model
                details=data.get("details", ""),
                client_id=client.id
            )

            db.add(intrusion)
            db.commit()
            
            # Record decision audit
            decision = PolicyDecision(
                intrusion_id=intrusion.id,
                action_taken=predicted_action
            )
            db.add(decision)
            db.commit()

            print(f"Intrusion logged. ML Model Predicted Action: {predicted_action}")
            
            # Execute Autonomous Actions
            process_agentic_action(db, predicted_action, data.get("ip", "0.0.0.0"))

    except WebSocketDisconnect:

        print("Agent disconnected")