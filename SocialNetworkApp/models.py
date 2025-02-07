from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from database import Base

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String)
    profile_id = Column(Integer, ForeignKey("profiles.id"))

class Profiles(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    surname = Column(String)
    date_of_birth = Column(Date, nullable=False)
    created_at = Column(Date, nullable=False)
    updated_at = Column(Date)
    is_verified = Column(Boolean)
    last_login = Column(Date)
    is_active = Column(Boolean)