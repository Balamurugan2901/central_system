from pydantic import BaseModel
from datetime import datetime

class IntrusionOut(BaseModel):
    id: int
    src_ip: str
    dst_ip: str
    protocol: str
    risk_level: str
    timestamp: datetime

    class Config:
        from_attributes = True
