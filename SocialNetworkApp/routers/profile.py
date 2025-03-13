from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Path
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from database import SessionLocal
from schemas import ProfileRequest
from models import Profiles
from .user import get_current_user

router = APIRouter(
    prefix='/profiles',
    tags=['Profiles']
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
async def create_profile(user: user_dependency, db: db_dependency,
                         profile_request: ProfileRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    if db.query(Profiles).filter(Profiles.user_id == user.get('id')).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already has a profile")
    profile_model = Profiles(
        user_id = user.get('id'),
        name = profile_request.name,
        surname = profile_request.surname,
        date_of_birth = profile_request.date_of_birth,
        is_verified = False,
        last_login = datetime.now(timezone.utc),
        is_active = True
    )
    db.add(profile_model)
    db.commit()

@router.get('/{profile_id}', status_code=status.HTTP_200_OK)
async def read_profile(user: user_dependency, db: db_dependency, profile_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    profile_model = db.query(Profiles).filter(Profiles.id == profile_id).first()
    if profile_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile is not found")
    return profile_model

@router.put('/{profile_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_profile(user: user_dependency, db: db_dependency, profile_request: ProfileRequest,
                         profile_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    profile_model = db.query(Profiles).filter(Profiles.id == profile_id).first()
    if profile_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile is not found")
    profile_model.name = profile_request.name
    profile_model.surname = profile_request.surname
    profile_model.date_of_birth = profile_request.date_of_birth
    profile_model.updated_at = datetime.now(timezone.utc)
    db.add(profile_model)
    db.commit()

@router.delete('/{profile_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(user: user_dependency, db: db_dependency, profile_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    profile_model = db.query(Profiles).filter(Profiles.id == profile_id).first()
    if profile_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile is not found")
    db.delete(profile_model)
    db.commit()