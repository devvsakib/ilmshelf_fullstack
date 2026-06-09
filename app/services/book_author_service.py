from app.models.book_author import BookAuthor
from app.models.author import Author
from app.schemas.book_author import BookAuthorCreate
from sqlalchemy.orm import Session


def assign_author(book_id, payload: BookAuthorCreate, db: Session):
    author = db.query(Author).filter(Author.id == payload.author_id).first()

    if not author:
        raise ValueError("Author not found")

    relation = BookAuthor(
        book_id=book_id,
        author_id=payload.author_id,
        role=payload.role,
    )

    db.add(relation)

    db.commit()

    db.refresh(relation)

    return relation
