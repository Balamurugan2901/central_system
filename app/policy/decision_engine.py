from app.core.blocking_engine import block_ip
from sqlalchemy.orm import Session

def process_agentic_action(db: Session, action: str, ip_address: str):
    """
    Executes the autonomous action predicted by the ML model.
    """
    print(f"Executing Agentic Action: {action} on IP: {ip_address}")
    
    if action == "BLOCK_IP":
        block_ip(db, ip_address, reason="ML Agentic Autonomous Block")
    elif action == "RATE_LIMIT":
        print(f"⚠️ Rate limiting applied to {ip_address}")
    elif action == "ALERT":
        print(f"🔔 Alert triggered for activity from {ip_address}")
    else:
        print(f"✅ Traffic from {ip_address} allowed")
