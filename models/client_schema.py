from pydantic import BaseModel

class ClientCreate(BaseModel):
    name: str
    ip_address: str


class ClientResponse(BaseModel):
    id: int
    name: str
    ip_address: str

    class Config:
        orm_mode = True
