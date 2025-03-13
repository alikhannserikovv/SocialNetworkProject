from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Path
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from database import SessionLocal
from schemas import PostRequest
from models import Profiles, Posts, Users
from .user import get_current_user

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post('', status_code=status.HTTP_201_CREATED)
async def create_post(user: user_dependency, db: db_dependency, post_request: PostRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    if db.query(Profiles).filter(Profiles.user_id == user.get('id')).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    post_model = Posts(**post_request.model_dump(), user_id = user.get('id'))
    db.add(post_model)
    db.commit()

@router.get('', status_code=status.HTTP_200_OK)
async def read_posts(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    if db.query(Profiles).filter(Profiles.user_id == user.get('id')).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return (
        db.query(Posts)
        .filter(Posts.user_id == user.get("id"))
        .all()
    )

@router.put('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_post(user: user_dependency, db: db_dependency, post_request: PostRequest,
                      post_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    if db.query(Profiles).filter(Profiles.user_id == user.get('id')).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    post_model = db.query(Posts).filter(Posts.id == post_id).first()
    if post_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    post_model.title = post_request.title
    post_model.text = post_request.text
    post_model.updated_at = datetime.now(timezone.utc)
    db.add(post_model)
    db.commit()

@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(user: user_dependency, db: db_dependency, post_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    if db.query(Profiles).filter(Profiles.user_id == user.get('id')).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    post_model = db.query(Posts).filter(Posts.id == post_id).first()
    if post_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    db.delete(post_model)
    db.commit()

@router.get('/{user_id}', status_code=status.HTTP_200_OK)
async def read_user_posts(db: db_dependency, user_id: int = Path(gt=0)):
    if db.query(Users).filter(Users.id == user_id).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return (
        db.query(Posts)
        .filter(Posts.user_id == user_id)
        .all()
    )