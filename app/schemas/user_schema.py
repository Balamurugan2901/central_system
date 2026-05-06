from pydantic import BaseModel


# Register schema
class UserCreate(BaseModel):
    email: str
    password: str


# Login schema — use plain str so any email format is accepted
class UserLogin(BaseModel):
    email: str
    password: str


# Response schema
class UserOut(BaseModel):
    id: int
    email: str
    role: str
    is_blocked: bool

    class Config:
        from_attributes = True   # pydantic v2 replacement for orm_mode
