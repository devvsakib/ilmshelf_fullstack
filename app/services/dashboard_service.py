from sqlalchemy import func
from app.models.user_book import UserBook
from app.models.wishlist import Wishlist
from app.models.note import Note
from app.models.highlight import Highlight
from app.models.book import Book
from app.models.enums import ReadStatusEnum


def get_dashboard(current_user, db):
    total_books = db.query(UserBook).filter(UserBook.user_id == current_user.id).count()

    completed_books = (
        db.query(UserBook)
        .filter(
            UserBook.user_id == current_user.id,
            UserBook.read_status == ReadStatusEnum.COMPLETED,
        )
        .count()
    )

    currently_reading = (
        db.query(UserBook)
        .filter(
            UserBook.user_id == current_user.id,
            UserBook.read_status == ReadStatusEnum.IN_PROGRESS,
        )
        .count()
    )

    wishlist_count = (
        db.query(Wishlist).filter(Wishlist.user_id == current_user.id).count()
    )

    notes_count = (
        db.query(Note)
        .join(UserBook)
        .filter(UserBook.user_id == current_user.id)
        .count()
    )

    highlights_count = (
        db.query(Highlight)
        .join(UserBook)
        .filter(UserBook.user_id == current_user.id)
        .count()
    )

    total_spent = (
        db.query(func.sum(Book.price))
        .join(UserBook, UserBook.book_id == Book.id)
        .filter(UserBook.user_id == current_user.id)
        .scalar()
        or 0
    )

    return {
        "total_books": total_books,
        "completed_books": completed_books,
        "currently_reading": currently_reading,
        "wishlist_count": wishlist_count,
        "notes_count": notes_count,
        "highlights_count": highlights_count,
        "total_spent": total_spent,
    }
