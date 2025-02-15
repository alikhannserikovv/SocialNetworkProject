from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Path
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT
from database import SessionLocal
from schemas import PostRequest
from models import Users, Profiles, Posts
from .user import get_current_user

router = APIRouter(
    prefix='/post',
    tags=['post']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post('/post', status_code=HTTP_201_CREATED)
async def create_post(user: user_dependency, db: db_dependency, post_request: PostRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    post_model = Posts(**post_request.model_dump(), user_id = user.get('id'))
    db.add(post_model)
    db.commit()

@router.put('/{post_id}', status_code=HTTP_204_NO_CONTENT)
async def update_post(user: user_dependency, db: db_dependency, post_request: PostRequest, post_id: int):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    post_model = db.query(Posts).filter(Posts.id == post_id).first()
    if post_model is None:
        raise HTTPException(status_code=404, detail="Post not found")
    post_model.title = post_request.title
    post_model.text = post_request.text
    post_model.updated_at = datetime.now(timezone.utc)
    db.add(post_model)
    db.commit()

@router.get('/', status_code=HTTP_200_OK)
async def read_post(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Posts).filter(Posts.user_id == user.get('id')).all()

@router.delete('/{post_id}', status_code=HTTP_204_NO_CONTENT)
async def delete_post(user: user_dependency, db: db_dependency, post_id: int):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    post_model = db.query(Posts).filter(Posts.id == post_id).first()
    if post_model is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post_model)
    db.commit()
