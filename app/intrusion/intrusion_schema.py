from pydantic import BaseModel
from datetime import datetime


class IntrusionCreate(BaseModel):
    client_id: int
    attack_type: str
    risk_score: float



class IntrusionResponse(BaseModel):
    id: int
    attack_type: str
    risk_score: float
    risk_level: str
    timestamp: datetime
    client_id: int

    class Config:
        from_attributes = True
