from math import ceil
from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.book import Book
from app.models.user import User
from app.models.publisher import Publisher
from app.schemas.book import BookCreate, BookUpdate
from app.utils.slug import generate_slug
from app.services.activity_service import log_activity
from app.models.enums import ActivityActionEnum
from app.utils.responses import success_response
from app.exceptions.not_found import NotFoundException
from datetime import datetime
from app.models.book_author import BookAuthor
from app.models.book_tag import BookTag
from app.models.author import Author
from app.models.tag import Tag
from app.models.wishlist import Wishlist
from app.models.user_book import UserBook


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


def get_books(
    db: Session,
    page,
    limit,
    author_id=None,
    tag_id=None,
    language=None,
    published_year=None,
):
    offset = (page - 1) * limit
    books = (
        db.query(Book)
        .filter(Book.deleted_at.is_(None))
        .offset(offset)
        .limit(limit)
        .all()
    )

    total = db.query(Book).count()

    data = {
        "items": books,
        "page": page,
        "limit": limit,
        "total": total,
        "has_next": total > page * limit,
    }
    return success_response(data)


def get_single_book_details(book_id, db: Session):
    book = db.query(Book).filter(Book.id == book_id, Book.deleted_at.is_(None)).first()

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


def get_book_details(
    book_id,
    db,
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

    authors = []
    translators = []
    editors = []

    assignments = (
        db.query(BookAuthor)
        .join(
            Author,
            Author.id == BookAuthor.author_id,
        )
        .filter(
            BookAuthor.book_id == book_id,
        )
        .all()
    )

    for item in assignments:
        person = {
            "id": item.author.id,
            "name_bn": item.author.name_bn,
            "name_en": item.author.name_en,
            "name_ar": item.author.name_ar,
        }

        if item.role == "AUTHOR":
            authors.append(person)

        elif item.role == "TRANSLATOR":
            translators.append(person)

        elif item.role == "EDITOR":
            editors.append(person)

    tags = []

    tag_assignments = (
        db.query(BookTag)
        .join(
            Tag,
            Tag.id == BookTag.tag_id,
        )
        .filter(
            BookTag.book_id == book_id,
        )
        .all()
    )

    for item in tag_assignments:
        tags.append(
            {
                "id": item.tag.id,
                "name": item.tag.name,
                "slug": item.tag.slug,
            }
        )

    wishlist_count = db.query(Wishlist).filter(Wishlist.book_id == book_id).count()

    reader_count = db.query(UserBook).filter(UserBook.book_id == book_id).count()

    publisher = None

    if book.publisher:
        publisher = {
            "id": book.publisher.id,
            "name": book.publisher.name,
        }

    return {
        "id": book.id,
        "title_bn": book.title_bn,
        "title_en": book.title_en,
        "title_ar": book.title_ar,
        "cover_url": book.cover_url,
        "authors": authors,
        "translators": translators,
        "editors": editors,
        "publisher": publisher,
        "tags": tags,
        "wishlist_count": wishlist_count,
        "reader_count": reader_count,
    }


def search_books(
    db,
    search=None,
    publisher_id=None,
    page=1,
    limit=20,
):
    query = db.query(Book).filter(Book.deleted_at.is_(None))

    if search:
        query = query.filter(
            Book.title_bn.ilike(f"%{search}%")
            | Book.title_en.ilike(f"%{search}%")
            | Book.title_ar.ilike(f"%{search}%")
        )

    if publisher_id:
        query = query.filter(Book.publisher_id == publisher_id)

    total = query.count()

    items = (
        query.order_by(Book.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "items": items,
        "page": page,
        "limit": limit,
        "total": total,
        "pages": ceil(total / limit) if total else 0,
    }


def update_book(
    book_id,
    payload: BookUpdate,
    db: Session,
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise NotFoundException("Book not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)

    return book


def delete_book(
    book_id,
    db: Session,
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise NotFoundException("Book not found")

    book.deleted_at = datetime.utcnow()

    db.commit()

    return {"message": "Book deleted"}
