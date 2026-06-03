from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.book import Book
from app.models.user import User
from app.models.publisher import Publisher
from app.schemas.book import BookCreate
from app.utils.slug import generate_slug


def create_book(payload: BookCreate, current_user: User, db: Session):
    slug = generate_slug(payload.title_bn or payload.title_en)

    existing_slug = db.query(Book).filter(Book.slug == slug).first()
    if existing_slug:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This book already in DataBase",
        )

    if payload.isbn:
        existing_isbn = db.query(Book).filter(Book.isbn == payload.isbn).first()
        if existing_isbn:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ISBN already exists",
            )

    # if payload.publisher_id:
    #     publisher = (
    #         db.query(Publisher)
    #         .filter(
    #             Publisher.id == payload.publisher_id
    #         )
    #         .first()
    #     )
    #     if not publisher:
    #         raise ValueError("Publisher not found")

    existing_book = db.query(Book).filter(Book.title_bn == payload.title_bn).first()
    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This book already in DataBase",
        )

    book = Book(
        slug=slug,
        title_bn=payload.title_bn,
        title_en=payload.title_en,
        title_ar=payload.title_ar,
        description_bn=payload.description_bn,
        description_en=payload.description_en,
        description_ar=payload.description_ar,
        cover_url=payload.cover_url,
        isbn=payload.isbn,
        pages=payload.pages,
        published_year=payload.published_year,
        language=payload.language,
        visibility=payload.visibility,
        publisher_id=payload.publisher_id,
        owner_id=current_user.id,
        book_metadata=payload.book_metadata,
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return book


def get_books(db: Session):
    return db.query(Book).all()


def get_book(book_id, db: Session):
    return db.query(Book).filter(Book.id == book_id).first()
