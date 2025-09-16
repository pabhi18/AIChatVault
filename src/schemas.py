from pydantic import BaseModel, EmailStr

class RegisterIn(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str | None = "user"

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    remaining_free_chats: int | None = None