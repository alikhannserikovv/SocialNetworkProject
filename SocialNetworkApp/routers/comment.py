from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Path
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from database import SessionLocal
from schemas import CommentRequest
from models import Profiles, Posts, Comments
from .user import get_current_user

router = APIRouter(
    prefix='/comments',
    tags=['Comments']
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
async def create_comment(user: user_dependency, db: db_dependency, comment_request: CommentRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    if db.query(Profiles).filter(Profiles.user_id == user.get('id')).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    if db.query(Posts).filter(Posts.id == comment_request.post_id).first() is None:
        raise HTTPException(status_code=404, detail="Post not found")
    comment_model = Comments(
        post_id = comment_request.post_id,
        text = comment_request.text,
        user_id = user.get('id')
    )
    db.add(comment_model)
    db.commit()

@router.get('', status_code=status.HTTP_200_OK)
async def read_comments(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    if db.query(Profiles).filter(Profiles.user_id == user.get('id')).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return (
        db.query(Comments)
        .filter(Comments.user_id == user.get('id'))
        .all()
    )

@router.put('/{comment_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_comment(user: user_dependency, db: db_dependency, comment_request: CommentRequest,
                         comment_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    if db.query(Profiles).filter(Profiles.user_id == user.get('id')).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    comment_model = db.query(Comments).filter(Comments.id == comment_id).first()
    if comment_model is  None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    if comment_model.post_id != comment_request.post_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    comment_model.text = comment_request.text
    comment_model.updated_at = datetime.now(timezone.utc)
    db.add(comment_model)
    db.commit()

@router.delete(('/{comment_id}'), status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(user: user_dependency, db: db_dependency, comment_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    if db.query(Profiles).filter(Profiles.user_id == user.get('id')).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    comment_model = db.query(Comments).filter(Comments.id == comment_id).first()
    if comment_model is  None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    db.delete(comment_model)
    db.commit()