from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import User
from app.utils.dependencies import get_current_admin
from app.utils.alert_manager import alert_manager

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users")
def list_users(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return db.query(User).all()


@router.put("/block/{user_id}")
def block_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_blocked = True
    db.commit()
    return {"msg": "User blocked"}


@router.put("/unblock/{user_id}")
def unblock_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_blocked = False
    db.commit()
    return {"msg": "User unblocked"}

@router.websocket("/alerts")
async def alerts(ws: WebSocket):
    await alert_manager.connect(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        alert_manager.disconnect(ws)

@router.get("/stats/total")
def total_attacks(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    count = db.query(IntrusionLog).count()
    return {"total_attacks": count}

from sqlalchemy import func

@router.get("/stats/risk")
def risk_stats(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    data = (
        db.query(IntrusionLog.risk_level, func.count())
        .group_by(IntrusionLog.risk_level)
        .all()
    )

    return {level: count for level, count in data}

@router.get("/recent")
def recent_attacks(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return (
        db.query(IntrusionLog)
        .order_by(IntrusionLog.timestamp.desc())
        .limit(10)
        .all()
    )

@router.get("/search")
def search_ip(
    ip: str,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return (
        db.query(IntrusionLog)
        .filter(IntrusionLog.src_ip == ip)
        .all()
    )

from sqlalchemy import func
from datetime import date

@router.get("/analytics/daily")
def daily_attacks(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    data = (
        db.query(
            func.date(IntrusionLog.timestamp).label("day"),
            func.count().label("count")
        )
        .group_by(func.date(IntrusionLog.timestamp))
        .order_by(func.date(IntrusionLog.timestamp))
        .all()
    )

    return [{"date": str(d.day), "attacks": d.count} for d in data]

@router.get("/analytics/risk-distribution")
def risk_distribution(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    data = (
        db.query(
            IntrusionLog.risk_level,
            func.count()
        )
        .group_by(IntrusionLog.risk_level)
        .all()
    )

    return {level: count for level, count in data}

@router.get("/analytics/top-ips")
def top_attackers(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    data = (
        db.query(
            IntrusionLog.src_ip,
            func.count().label("count")
        )
        .group_by(IntrusionLog.src_ip)
        .order_by(func.count().desc())
        .limit(5)
        .all()
    )

    return [{"ip": ip, "attacks": count} for ip, count in data]

@router.get("/monitor/live")
def live_attacks(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    data = (
        db.query(IntrusionLog)
        .order_by(IntrusionLog.timestamp.desc())
        .limit(20)
        .all()
    )

    return data

@router.get("/monitor/summary")
def summary(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    total = db.query(IntrusionLog).count()
    high = db.query(IntrusionLog).filter(IntrusionLog.risk_level=="HIGH").count()
    medium = db.query(IntrusionLog).filter(IntrusionLog.risk_level=="MEDIUM").count()
    low = db.query(IntrusionLog).filter(IntrusionLog.risk_level=="LOW").count()

    return {
        "total": total,
        "high": high,
        "medium": medium,
        "low": low
    }
