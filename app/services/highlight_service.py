from sqlalchemy.orm import Session
from app.models.highlight import Highlight
from app.models.user_book import UserBook
from app.models.user import User

from app.schemas.highlight import HighlightCreate, HighlightUpdate


def create_highlight(payload: HighlightCreate, current_user: User, db: Session):
    user_book = (
        db.query(UserBook)
        .filter(
            UserBook.user_id == current_user.id, UserBook.id == payload.user_book_id
        )
        .first()
    )

    if not user_book:
        return ValueError("Book not found in your library")

    highlight = Highlight(
        user_book_id=payload.user_book_id,
        page=payload.page,
        selected_text=payload.selected_text,
        note=payload.note,
    )

    db.add(highlight)

    db.commit()

    db.refresh(highlight)

    return highlight


def get_highlights(current_user: User, db: Session):
    return (
        db.query(Highlight)
        .join(UserBook)
        .filter(UserBook.user_id == current_user.id)
        .all()
    )


def update_highlight(
    highlight_id,
    payload: HighlightUpdate,
    current_user: User,
    db: Session,
):
    highlight = (
        db.query(Highlight)
        .join(UserBook)
        .filter(
            Highlight.id == highlight_id,
            UserBook.user_id == current_user.id,
        )
        .first()
    )

    if not highlight:
        raise ValueError("Highlight not found")

    if payload.page is not None:
        highlight.page = payload.page

    if payload.selected_text is not None:
        highlight.selected_text = payload.selected_text

    if payload.note is not None:
        highlight.note = payload.note

    db.commit()

    db.refresh(highlight)

    return highlight


def delete_highlight(
    highlight_id,
    current_user: User,
    db: Session,
):
    highlight = (
        db.query(Highlight)
        .join(UserBook)
        .filter(
            Highlight.id == highlight_id,
            UserBook.user_id == current_user.id,
        )
        .first()
    )

    if not highlight:
        raise ValueError("Highlight not found")

    db.delete(highlight)

    db.commit()

    return True
