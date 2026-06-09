from sqlalchemy.orm import Session
from datetime import datetime

from app.models.author import Author
from app.schemas.author_schema import (
    AuthorCreate,
    AuthorUpdate,
)


def create_author(
    payload: AuthorCreate,
    db: Session,
):
    author = Author(**payload.model_dump())

    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def get_authors(db: Session):
    return (
        db.query(Author)
        .filter(Author.deleted_at.is_(None))
        .order_by(Author.name_bn)
        .all()
    )


def get_author(
    author_id,
    db: Session,
):
    return (
        db.query(Author)
        .filter(
            Author.id == author_id,
            Author.deleted_at.is_(None),
        )
        .first()
    )


def update_author(
    author_id,
    payload: AuthorUpdate,
    db: Session,
):
    author = (
        db.query(Author)
        .filter(
            Author.id == author_id,
            Author.deleted_at.is_(None),
        )
        .first()
    )

    if not author:
        return None

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(author, key, value)

    db.commit()
    db.refresh(author)

    return author


def delete_author(
    author_id,
    db: Session,
):
    author = (
        db.query(Author)
        .filter(
            Author.id == author_id,
            Author.deleted_at.is_(None),
        )
        .first()
    )

    if not author:
        return None

    author.deleted_at = datetime.utcnow()

    db.commit()

    return {"message": "Author deleted successfully"}
