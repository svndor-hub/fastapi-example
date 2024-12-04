from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from src.auth.config import settings
from src.auth.dependencies import SessionDep
from src.auth.models import User
from src.database import fetch_one

from sqlalchemy import select

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(session: SessionDep, username: str, password: str):
    query = select(User).where(User.username == username)
    user = await fetch_one(query, session)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
