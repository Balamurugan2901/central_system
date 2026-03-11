from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.core.blocking_engine import block_ip

router = APIRouter(prefix="/block", tags=["Blocking"])


@router.post("/ip/{ip}")
def block_ip_api(ip: str, db: Session = Depends(get_db)):

    blocked = block_ip(db, ip)

    return {
        "status": "blocked",
        "ip": blocked.ip_address,
        "reason": blocked.reason
    }