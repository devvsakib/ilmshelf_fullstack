from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.reading_session import (
    ReadingSession,
)

from app.schemas.reading_session_schema import ReadingSessionCreate


def create_session(
    payload: ReadingSessionCreate,
    user_id,
    db: Session,
):
    book = (
        db.query(Book)
        .filter(
            Book.id == payload.book_id,
            Book.deleted_at.is_(None),
        )
        .first()
    )

    if not book:
        return None

    session = ReadingSession(
        user_id=user_id,
        book_id=payload.book_id,
        pages_read=payload.pages_read,
        started_at=payload.started_at,
        ended_at=payload.ended_at,
    )

    db.add(session)

    db.commit()
    db.refresh(session)

    return session


def get_my_sessions(
    user_id,
    db: Session,
):
    return (
        db.query(ReadingSession)
        .filter(
            ReadingSession.user_id == user_id,
            ReadingSession.deleted_at.is_(None),
        )
        .order_by(ReadingSession.created_at.desc())
        .all()
    )
