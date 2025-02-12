from datetime import date
from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    name: str
    surname: str
    username: str
    password: str
    email: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ProfileRequest(BaseModel):
    name: str
    surname: str
    date_of_birth: date