from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.database.base import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ip_address = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    intrusions = relationship("IntrusionLog", back_populates="client")


class IntrusionLog(Base):
    __tablename__ = "intrusions"

    id = Column(Integer, primary_key=True, index=True)
    src_ip = Column(String)
    packet_rate = Column(Float)
    failed_logins = Column(Integer)
    attack_type = Column(String)
    risk_score = Column(Float)
    risk_level = Column(String)   # 🔥 NEW COLUMN
    action = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    client_id = Column(Integer, ForeignKey("clients.id"))
    client = relationship("Client", back_populates="intrusions")
    decisions = relationship("PolicyDecision", back_populates="intrusion")


class BehaviorLog(Base):
    __tablename__ = "behavior_logs"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    activity = Column(String)
    anomaly_score = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)


class PolicyDecision(Base):
    __tablename__ = "policy_decisions"

    id = Column(Integer, primary_key=True, index=True)
    intrusion_id = Column(Integer, ForeignKey("intrusions.id"))
    action_taken = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    intrusion = relationship("IntrusionLog", back_populates="decisions")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    role = Column(String, default="user")   # user / admin
    is_blocked = Column(Boolean, default=False)

