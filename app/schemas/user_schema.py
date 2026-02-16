from pydantic import BaseModel, EmailStr


# 🔹 Register schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# 🔹 Login schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# 🔹 Response schema (optional but useful later)
class UserOut(BaseModel):
    id: int
    email: str
    role: str
    is_blocked: bool

    class Config:
        from_attributes = True   # pydantic v2 replacement for orm_mode
