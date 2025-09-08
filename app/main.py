from fastapi import Depends, FastAPI, HTTPException
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


@app.get("/notes/{id}", response_model=NoteRead)
def get_note(id: int, db: Session = Depends(get_db_session)):
    note = db.get(Note, id)
    if not note:
        raise HTTPException(404, "Note not found")
    return note


@app.post("/notes", response_model=Note)
def create_note(dto: NoteCreate, db: Session = Depends(get_db_session)):
    note = Note(title=dto.title, content=dto.content)
    db.add(note)
    db.commit()
    db.refresh(note)

    return note.model_dump()


@app.patch("/notes/{id}", response_model=NoteRead)
def update_note(id: int, dto: NoteCreate, db: Session = Depends(get_db_session)):
    note = db.get(Note, id)
    if not note:
        raise HTTPException(404, "Note not found")
    note.title = dto.title
    note.content = dto.content
    db.commit()
    db.refresh(note)
    return note


@app.delete("/notes/{id}", response_model=NoteRead)
def delete_note(id: int, db: Session = Depends(get_db_session)):
    note = db.get(Note, id)
    if not note:
        raise HTTPException(404, "Note not found")
    db.delete(note)
    db.commit()

    return note


@app.get("/scalar", include_in_schema=False)
async def scalar_html() -> HTMLResponse:
    if not app.openapi_url:
        raise ValueError("openapi_url is None")

    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)
