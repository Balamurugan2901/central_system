from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.crud import get_db, create_intrusion_log
from app.database.models import IntrusionLog
from app.intrusion.intrusion_schema import IntrusionCreate, IntrusionResponse
from app.intrusion.risk_analyzer import classify_risk
from app.intrusion.ml_engine import predict_risk
from app.intrusion.packet_sniffer import capture_packet
from app.intrusion.feature_engineering import extract_features
from app.intrusion.rule_engine import check_rules
from app.policy.decision_engine import decide_action
from app.utils.alert_manager import alert_manager
from app.utils.dependencies import get_current_admin


router = APIRouter()


from app.policy.decision_engine import decide_action

@router.post("/intrusions", response_model=IntrusionResponse)
def log_intrusion(data: IntrusionCreate, db: Session = Depends(get_db)):

    # 🔹 ML prediction
    score = predict_risk(
        packet_rate=data.packet_rate,
        failed_logins=data.failed_logins
    )

    # 🔹 classification
    risk_level = classify_risk(score)

    # 🔹 decision
    action = decide_action(risk_level)

    # 🔹 store intrusion log
    intrusion = IntrusionLog(
        src_ip=data.src_ip,
        packet_rate=data.packet_rate,
        failed_logins=data.failed_logins,
        attack_type=data.attack_type,
        risk_score=score,
        risk_level=risk_level,
        action=action,
        client_id=data.client_id
    )

    db.add(intrusion)
    db.commit()
    db.refresh(intrusion)

    # 🔹 store policy decision (audit log)
    decision = PolicyDecision(
        intrusion_id=intrusion.id,
        action_taken=action
    )
    db.add(decision)
    db.commit()

    # 🔹 realtime alert
    if risk_level in ["MEDIUM", "HIGH"]:
        import asyncio
        asyncio.create_task(alert_manager.broadcast({
            "type": "intrusion_alert",
            "risk": risk_level,
            "score": score,
            "ip": data.src_ip
        }))

    return {
        "id": intrusion.id,
        "attack_type": intrusion.attack_type,
        "risk_score": score,
        "risk_level": risk_level,
        "timestamp": intrusion.timestamp,
        "client_id": intrusion.client_id,
        "action": action
    }




@router.get("/intrusions", response_model=list[IntrusionResponse])
def get_intrusions(db: Session = Depends(get_db)):
    return db.query(IntrusionLog).all()



router = APIRouter(prefix="/intrusion", tags=["Intrusion"])

@router.post("/run")
async def run_scan(db: Session = Depends(get_db)):

    # 1️⃣ Capture packet
    packet = capture_packet()

    # 2️⃣ Feature extraction
    features = extract_features(packet)

    # 3️⃣ ML + Rule detection
    ml_flag = predict(features)
    rule_flag = check_rules(packet)

    # 4️⃣ Risk calculation
    risk = calculate_risk(ml_flag, rule_flag)

    # 5️⃣ Save log in DB
    log = IntrusionLog(
        src_ip=packet.get("src_ip"),
        dst_ip=packet.get("dst_ip"),
        protocol=packet.get("protocol"),
        risk_level=risk
    )
    db.add(log)
    db.commit()

    # 6️⃣ Websocket alert if high risk
    if risk == "HIGH":
        await alert_manager.broadcast(
            f"HIGH RISK intrusion from {packet.get('src_ip','unknown')}"
        )

    return {
        "packet": packet,
        "risk_level": risk
    }


@router.post("/scan")
def scan(packet_rate: float, failed_logins: int, db: Session = Depends(get_db)):

    score = predict_risk(packet_rate, failed_logins)

    # level classification
    if score >= 8:
        level = "HIGH"
    elif score >= 4:
        level = "MEDIUM"
    else:
        level = "LOW"

    action = decide_action(level)

    log = create_intrusion_log(db, {
        "src_ip": "unknown",
        "packet_rate": packet_rate,
        "failed_logins": failed_logins,
        "risk_score": score,
        "risk_level": level,
        "action": action
    })

    return {
        "risk_score": score,
        "risk_level": level,
        "action": action,
        "log_id": log.id
    }

@router.get("/history")
def get_intrusions(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return db.query(IntrusionLog).all()