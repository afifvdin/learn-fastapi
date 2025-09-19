from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.core.settings import settings
from app.models.database import User
from app.models.engine import db_session
from app.schema.auth import AuthLogin, AuthRegister, RegisterResponse
from app.services import auth_service

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(user: AuthRegister, db: Session = Depends(db_session)):
    try:
        user.password = auth_service.hash_password(user.password)
        new_user = User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@auth_router.post("/login")
def login(user: AuthLogin, db: Session = Depends(db_session)):
    statement = select(User).where(User.email == user.email)
    result = db.exec(statement).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password")

    is_password_match = auth_service.verify_password(user.password, result.password)

    if not is_password_match:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password")

    access_token = auth_service.create_access_token({"sub": result.email})

    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/login/google", name="login_google")
async def login_google(request: Request):
    return await auth_service.oauth.google.authorize_redirect(request, settings.GOOGLE_REDIRECT_URL)


@auth_router.get("/callback/google")
async def callback_google(request: Request):
    return await auth_service.oauth.google.authorize_access_token(request)
