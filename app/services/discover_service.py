from sqlalchemy import func  # <-- Add this import
from app.models.book import Book
from app.models.user_book import UserBook


def recent_books(
    db,
    limit=20,
):
    return (
        db.query(Book)
        .filter(Book.deleted_at.is_(None))
        .order_by(Book.created_at.desc())
        .limit(limit)
        .all()
    )


def popular_books(
    db,
    limit=20,
):
    return (
        db.query(Book)
        .outerjoin(
            UserBook,
            UserBook.book_id == Book.id,
        )
        .group_by(Book.id)
        .order_by(func.count(UserBook.id).desc())
        .limit(limit)
        .all()
    )
