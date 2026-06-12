from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.tag import Tag
from app.models.book_tag import BookTag
from app.schemas.book_tag_schema import BookTagCreate


def assign_tag_to_book(
    book_id,
    payload: BookTagCreate,
    db: Session,
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        return None

    tag = db.query(Tag).filter(Tag.id == payload.tag_id).first()

    if not tag:
        return None

    existing = (
        db.query(BookTag)
        .filter(
            BookTag.book_id == book_id,
            BookTag.tag_id == payload.tag_id,
        )
        .first()
    )

    if existing:
        return existing

    item = BookTag(
        book_id=book_id,
        tag_id=payload.tag_id,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def get_book_tags(
    book_id,
    db: Session,
):
    return db.query(BookTag).filter(BookTag.book_id == book_id).all()


def remove_book_tag(
    book_tag_id,
    db: Session,
):
    item = db.query(BookTag).filter(BookTag.id == book_tag_id).first()

    if not item:
        return None

    db.delete(item)
    db.commit()

    return {"message": "Tag removed successfully"}
