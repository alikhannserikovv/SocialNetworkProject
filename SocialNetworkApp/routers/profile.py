from datetime import date
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Path
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT
from database import SessionLocal
from passlib.context import CryptContext
from schemas import ProfileRequest
from models import Users, Profiles
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from .user import get_current_user

router = APIRouter(
    prefix='/profile',
    tags=['profile']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post('/create', status_code=HTTP_201_CREATED)
async def create_profile(user: user_dependency, db: db_dependency,
                         profile_request: ProfileRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    profile_model = Profiles(
        user_id = user.get('id'),
        name = profile_request.name,
        surname = profile_request.surname,
        date_of_birth = profile_request.date_of_birth,
        created_at = date.today(),
        is_verified = False,
        last_login = date.today(),
        is_active = True
    )
    db.add(profile_model)
    db.commit()
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User is not found")
    if user_model.profile_id is not None:
        raise HTTPException(status_code=404, detail="User already has a profile")
    profile_model = db.query(Profiles).filter(Profiles.user_id == user_model.id).first()
    user_model.profile_id = profile_model.id
    db.add(user_model)
    db.commit()

@router.get('/{profile_id}', status_code=HTTP_200_OK)
async def read_profile(user: user_dependency, db: db_dependency, profile_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    profile_model = db.query(Profiles).filter(Profiles.id == profile_id).first()
    if profile_model is None:
        raise HTTPException(status_code=404, detail="Profile is not found")
    return profile_model

@router.put('/{profile_id}', status_code=HTTP_204_NO_CONTENT)
async def update_profile(user: user_dependency, db: db_dependency, profile_request: ProfileRequest,
                         profile_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    profile_model = db.query(Profiles).filter(Profiles.id == profile_id).first()
    if profile_model is None:
        raise HTTPException(status_code=404, detail="Profile is not found")
    profile_model.name = profile_request.name
    profile_model.surname = profile_request.surname
    profile_model.date_of_birth = profile_request.date_of_birth
    db.add(profile_model)
    db.commit()

@router.delete('/{profile_id}', status_code=HTTP_204_NO_CONTENT)
async def delete_profile(user: user_dependency, db: db_dependency, profile_id: int):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    profile_model = db.query(Profiles).filter(Profiles.id == profile_id).first()
    if profile_model is None:
        raise HTTPException(status_code=404, detail="Profile is not found")
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.profile_id = None
    db.delete(profile_model)
    db.commit()