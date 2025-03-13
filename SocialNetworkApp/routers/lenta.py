from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Path
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT
from database import SessionLocal
from schemas import CommentRequest
from models import Profiles, Posts, Comments
from .user import get_current_user

router = APIRouter(
    prefix='/lenta',
    tags=['Lenta']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get('', status_code=HTTP_200_OK)
async def get_all_posts(db: db_dependency):
    return (
        db.query(Posts).all()
    )