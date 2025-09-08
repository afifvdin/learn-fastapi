from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from scalar_fastapi import get_scalar_api_reference
from sqlmodel import Session, select

from app.database import Note, get_db_session
from app.schema import NoteCreate, NoteRead

app = FastAPI(
    title="Title",
    version="1.0.0",
)


@app.get("/notes", response_model=list[NoteRead])
def get_notes(db: Session = Depends(get_db_session)):
    return db.exec(select(Note)).all()


@app.post("/notes", response_model=Note)
def create_note(dto: NoteCreate, db: Session = Depends(get_db_session)):
    note = Note(title=dto.title, content=dto.content)
    db.add(note)
    db.commit()
    db.refresh(note)

    return note.model_dump()


@app.get("/scalar", include_in_schema=False)
async def scalar_html() -> HTMLResponse:
    if not app.openapi_url:
        raise ValueError("openapi_url is None")

    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)
