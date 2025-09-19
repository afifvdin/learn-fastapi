from datetime import datetime, timedelta

import jwt
from authlib.integrations.starlette_client import OAuth
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlmodel import Session, select

from app.core.settings import settings
from app.models.database import User
from app.models.engine import db_session
from app.schema.auth import RegisterResponse

password_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid email profile",
    },
)


def hash_password(password: str):
    return password_ctx.hash(password)


def verify_password(password: str, hashed_password: str):
    return password_ctx.verify(password, hashed_password)


def create_access_token(
    payload: dict[str, str | datetime], expires_delta: timedelta = timedelta(minutes=settings.JWT_TOKEN_EXPIRES)
) -> str:
    to_encode = payload.copy()
    expired_at = datetime.now() + expires_delta
    to_encode.update({"exp": expired_at})
    return jwt.encode(to_encode, settings.JWT_SECRET, settings.JWT_ALGORITHM)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(db_session)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        statement = select(User).where(User.email == email)
        result = db.exec(statement).first()
        if result is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        return RegisterResponse(**result.model_dump())
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
