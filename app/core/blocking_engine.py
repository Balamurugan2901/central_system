from sqlalchemy.orm import Session
from app.database.models import BlockedIP

def block_ip(db: Session, ip: str, reason: str = "Threat detected"):

    # already blocked check
    existing = db.query(BlockedIP).filter(BlockedIP.ip_address == ip).first()
    if existing:
        return existing

    blocked = BlockedIP(
        ip_address=ip,
        reason=reason
    )

    db.add(blocked)
    db.commit()
    db.refresh(blocked)

    return blocked