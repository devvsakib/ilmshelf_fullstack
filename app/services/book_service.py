from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.book import Book
from app.models.user import User
from app.models.user_book import UserBook
from app.models.publisher import Publisher
from app.schemas.book import BookCreate
from app.utils.slug import generate_slug
from app.services.activity_service import log_activity
from app.models.enums import ActivityActionEnum


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
    db.flush()

    log_activity(
        db=db,
        user_id=current_user.id,
        action=ActivityActionEnum.BOOK_ADDED,
        entity_type="Book",
        entity_id=book.id,
    )
    db.commit()
    db.refresh(book)

    return book


def get_books(db: Session, page, limit):
    offset = (page - 1) * limit
    books = db.query(Book).offset(offset).limit(limit).all()

    total = db.query(Book).count()

    return {
        "items": books,
        "page": page,
        "limit": limit,
        "total": total,
        "has_next": total > page * limit,
    }


def get_book_details(book_id, db: Session):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        return None

    total_readers = db.query(UserBook).filter(UserBook.book_id == book_id).count()

    average_rating = (
        db.query(func.avg(UserBook.rating)).filter(UserBook.book_id == book_id).scalar()
    )

    return {
        "book": book,
        "authors": [x.author for x in book.book_authors],
        "tags": [x.tag for x in book.book_tags],
        "publisher": book.publisher,
        "total_readers": total_readers,
        "average_rating": average_rating,
    }
