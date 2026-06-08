from sqlalchemy.orm import Session
from app.models.note import Note
from app.models.user_book import UserBook
from app.models.user import User
from app.schemas.note import NoteCreate, NoteUpdate
from app.services.activity_service import log_activity
from app.models.enums import ActivityActionEnum


def create_note(payload: NoteCreate, current_user: User, db: Session):
    user_book = (
        db.query(UserBook)
        .filter(
            UserBook.id == payload.user_book_id, UserBook.user_id == current_user.id
        )
        .first()
    )

    if not user_book:
        raise ValueError("Bok not found in your library. Please at it to your library")

    note = Note(
        user_book_id=payload.user_book_id, page=payload.page, content=payload.content
    )

    db.add(note)
    db.flush()
    
    log_activity(
        db=db, 
        user_id=current_user.id, 
        action=ActivityActionEnum.NOTE_CREATED, 
        entity_type="Note", 
        entity_id=note.id
    )
    db.commit()
    db.refresh(note)

    return note


def get_notes(current_user: User, db: Session):
    return (
        db.query(Note).join(UserBook).filter(UserBook.user_id == current_user.id).all()
    )


def update_note(
    note_id,
    payload: NoteUpdate,
    current_user: User,
    db: Session,
):
    note = (
        db.query(Note)
        .join(UserBook)
        .filter(
            Note.id == note_id,
            UserBook.user_id == current_user.id,
        )
        .first()
    )

    if not note:
        raise ValueError("Note not found")

    if payload.page is not None:
        note.page = payload.page

    if payload.content is not None:
        note.content = payload.content

    if payload.is_public is not None:
        note.is_public = payload.is_public

    db.commit()

    db.refresh(note)

    return note


def delete_note(
    note_id,
    current_user: User,
    db: Session,
):
    note = (
        db.query(Note)
        .join(UserBook)
        .filter(
            Note.id == note_id,
            UserBook.user_id == current_user.id,
        )
        .first()
    )

    if not note:
        raise ValueError("Note not found")

    db.delete(note)

    db.commit()

    return True
