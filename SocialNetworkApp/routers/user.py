from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from database import SessionLocal
from passlib.context import CryptContext
from schemas import CreateUserRequest
from models import Users

router = APIRouter(
    prefix='/user',
    tags=['user']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post('/register/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_request: CreateUserRequest):
    user_model = Users(
        username = user_request.username,
        email = user_request.email,
        hashed_password = bcrypt_context.hash(user_request.password),
        role = 'user'
    )
    db.add(user_model)
    db.commit()