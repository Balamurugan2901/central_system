from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.crud import get_db
from app.database.models import User
from app.schemas.user_schema import UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token
from app.database.models import IntrusionLog
from app.utils.dependencies import get_current_admin


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        password=hash_password(user.password),
        role="user"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "User created successfully"}
    

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email, "role": db_user.role})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/intrusions")
def get_intrusions(db: Session = Depends(get_db)):
    return db.query(IntrusionLog)\
        .order_by(IntrusionLog.timestamp.desc())\
        .all()

@router.get("/intrusions/high")
def get_high_risk(db: Session = Depends(get_db)):
    return db.query(IntrusionLog)\
        .filter(IntrusionLog.risk_level == "HIGH")\
        .all()

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):

    total = db.query(IntrusionLog).count()
    high = db.query(IntrusionLog)\
        .filter(IntrusionLog.risk_level=="HIGH")\
        .count()
    medium = db.query(IntrusionLog)\
        .filter(IntrusionLog.risk_level=="MEDIUM")\
        .count()

    return {
        "total_intrusions": total,
        "high_risk": high,
        "medium_risk": medium
    }

# @router.get("/history")
# def get_intrusions(
#     db: Session = Depends(get_db),
#     admin=Depends(get_current_admin)
# ):
#     return db.query(IntrusionLog).all()

# @router.get("/stats/total")
# def total_attacks(
#     db: Session = Depends(get_db),
#     admin=Depends(get_current_admin)
# ):
#     count = db.query(IntrusionLog).count()
#     return {"total_attacks": count}

# from sqlalchemy import func

# @router.get("/stats/risk")
# def risk_stats(
#     db: Session = Depends(get_db),
#     admin=Depends(get_current_admin)
# ):
#     data = (
#         db.query(IntrusionLog.risk_level, func.count())
#         .group_by(IntrusionLog.risk_level)
#         .all()
#     )

#     return {level: count for level, count in data}

# @router.get("/recent")
# def recent_attacks(
#     db: Session = Depends(get_db),
#     admin=Depends(get_current_admin)
# ):
#     return (
#         db.query(IntrusionLog)
#         .order_by(IntrusionLog.timestamp.desc())
#         .limit(10)
#         .all()
#     )

# @router.get("/search")
# def search_ip(
#     ip: str,
#     db: Session = Depends(get_db),
#     admin=Depends(get_current_admin)
# ):
#     return (
#         db.query(IntrusionLog)
#         .filter(IntrusionLog.src_ip == ip)
#         .all()
#     )
