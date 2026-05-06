from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.crud import get_db
from app.database.models import BlockedIP
from app.utils.dependencies import get_current_admin
from pydantic import BaseModel

router = APIRouter(prefix="/blocks", tags=["Blocked IPs"])

class BlockIPRequest(BaseModel):
    ip_address: str
    reason: str = "Manual Admin Block"

@router.get("/")
def get_blocked_ips(db: Session = Depends(get_db)):
    """Retrieve all blocked IPs."""
    return db.query(BlockedIP).order_by(BlockedIP.created_at.desc()).all()


@router.post("/")
def block_ip_manually(
    req: BlockIPRequest, 
    db: Session = Depends(get_db), 
    admin=Depends(get_current_admin)
):
    """Manually add an IP to the blocklist."""
    existing = db.query(BlockedIP).filter(BlockedIP.ip_address == req.ip_address).first()
    if existing:
        raise HTTPException(status_code=400, detail="IP is already blocked")

    blocked = BlockedIP(
        ip_address=req.ip_address,
        reason=req.reason
    )
    db.add(blocked)
    db.commit()
    db.refresh(blocked)
    return blocked


@router.delete("/{ip_address}")
def unblock_ip(
    ip_address: str, 
    db: Session = Depends(get_db), 
    admin=Depends(get_current_admin)
):
    """Remove an IP from the blocklist."""
    blocked = db.query(BlockedIP).filter(BlockedIP.ip_address == ip_address).first()
    if not blocked:
        raise HTTPException(status_code=404, detail="IP not found in blocklist")

    db.delete(blocked)
    db.commit()
    return {"message": f"Successfully unblocked {ip_address}"}
