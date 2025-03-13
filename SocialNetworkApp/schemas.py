from datetime import date
from pydantic import BaseModel, EmailStr
from typing import Optional
from models import UserRole


class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: EmailStr
    role: Optional[UserRole] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class ProfileRequest(BaseModel):
    name: str
    surname: str
    date_of_birth: date

class PostRequest(BaseModel):
    title: str
    text: str

class CommentRequest(BaseModel):
    post_id: int
    text: str