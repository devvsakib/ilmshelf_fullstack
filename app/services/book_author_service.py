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
    book = (
        db.query(Book)
        .filter(
            Book.id == book_id,
            Book.deleted_at.is_(None),
        )
        .first()
    )

    if not book:
        return None

    author = (
        db.query(Author)
        .filter(
            Author.id == payload.author_id,
            Author.deleted_at.is_(None),
        )
        .first()
    )

    if not author:
        return None

    existing = (
        db.query(BookAuthor)
        .filter(
            BookAuthor.book_id == book_id,
            BookAuthor.author_id == payload.author_id,
            BookAuthor.role == payload.role,
            BookAuthor.deleted_at.is_(None),
        )
        .first()
    )

    if existing:
        return existing

    assignment = BookAuthor(
        book_id=book_id,
        author_id=payload.author_id,
        role=payload.role,
    )

    db.add(assignment)

    db.commit()
    db.refresh(assignment)

    return assignment


def get_book_authors(
    book_id,
    db: Session,
):
    records = (
        db.query(BookAuthor)
        .join(
            Author,
            Author.id == BookAuthor.author_id,
        )
        .filter(
            BookAuthor.book_id == book_id,
            BookAuthor.deleted_at.is_(None),
        )
        .all()
    )

    result = []

    for item in records:
        result.append(
            {
                "id": item.id,
                "author_id": item.author.id,
                "name_bn": item.author.name_bn,
                "name_en": item.author.name_en,
                "name_ar": item.author.name_ar,
                "role": item.role,
            }
        )

    return result


def delete_book_author(
    book_author_id,
    db: Session,
):
    item = (
        db.query(BookAuthor)
        .filter(
            BookAuthor.id == book_author_id,
            BookAuthor.deleted_at.is_(None),
        )
        .first()
    )

    if not item:
        return None

    db.delete(item)

    db.commit()

    return {"message": "Book author removed successfully"}
