from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.models.database import User
from app.schema.user import UserCreate


def create_user(db_session: Session, user: UserCreate):
    new_user = User(**user.model_dump())

    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    return new_user


def get_user(db_session: Session, id: str):
    # lazy query
    # statement = select(User).where(User.id == id)
    # user = db_session.exec(statement).first()
    # _ = user.posts -> this one lazy query, will be queried when accessed
    # return user

    statement = select(User).options(selectinload(User.posts)).where(User.id == id)  # type: ignore
    return db_session.exec(statement).first()


def get_users(db_session: Session):
    return db_session.exec(select(User)).all()
