import os

from dotenv import load_dotenv
from sqlmodel import Field, Session, SQLModel, create_engine

load_dotenv(override=True)
engine = create_engine(os.environ.get("DATABASE_URL", "sqlite:///./dev.db"))


def get_db_session():
    with Session(engine) as session:
        yield session


class Note(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field()
    content: str | None = Field(default="")
