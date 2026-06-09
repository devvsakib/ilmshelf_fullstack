from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.author import Author
from app.models.book_author import BookAuthor

from app.schemas.book_author_schema import (
    BookAuthorCreate,
)


def assign_author_to_book(
    book_id,
    payload: BookAuthorCreate,
    db: Session,
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        return None

    author = db.query(Author).filter(Author.id == payload.author_id).first()

    if not author:
        return None

    existing = (
        db.query(BookAuthor)
        .filter(
            BookAuthor.book_id == book_id,
            BookAuthor.author_id == payload.author_id,
            BookAuthor.role == payload.role,
        )
        .first()
    )

    if existing:
        return existing

    item = BookAuthor(
        book_id=book_id,
        author_id=payload.author_id,
        role=payload.role,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def get_book_authors(
    book_id,
    db: Session,
):
    return db.query(BookAuthor).filter(BookAuthor.book_id == book_id).all()


def remove_book_author(
    book_author_id,
    db: Session,
):
    item = db.query(BookAuthor).filter(BookAuthor.id == book_author_id).first()

    if not item:
        return None

    db.delete(item)

    db.commit()

    return {"message": "Removed successfully"}
