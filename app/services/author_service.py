from sqlalchemy.orm import Session

from app.models.author import Author
from app.schemas.author import AuthorCreate


def create_author(payload: AuthorCreate, db: Session):
    author = Author(
        name_bn=payload.name_bn,
        name_en=payload.name_en,
        name_ar=payload.name_ar,
        bio=payload.bio,
    )

    db.add(author)

    db.commit()

    db.refresh(author)

    return author


def get_authors(db: Session):
    return db.query(Author).all()


def get_author(author_id, db: Session):
    return db.query(Author).filter(Author.id == author_id).first()
