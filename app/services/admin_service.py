from sqlalchemy.orm import Session

from app.models.user import User
from app.models.book import Book
from app.models.shelf import Shelf
from app.models.note import Note
from app.models.highlight import Highlight
from app.models.author import Author
from app.models.tag import Tag
from app.models.publisher import Publisher
from app.models.wishlist import Wishlist
from app.models.reading_goal import ReadingGoal
from app.models.enums import RoleEnum

from app.exceptions.not_found import NotFoundException

from app.utils.soft_delete import soft_delete


def get_dashboard(db: Session):
    return {
        "total_users": db.query(User).filter(User.deleted_at.is_(None)).count(),
        "total_books": db.query(Book).filter(Book.deleted_at.is_(None)).count(),
        "total_shelves": db.query(Shelf).filter(Shelf.deleted_at.is_(None)).count(),
        "total_notes": db.query(Note).filter(Note.deleted_at.is_(None)).count(),
        "total_highlights": db.query(Highlight)
        .filter(Highlight.deleted_at.is_(None))
        .count(),
    }


def get_dashboard_stats(
    db: Session,
):
    return {
        "total_users": (db.query(User).filter(User.deleted_at.is_(None)).count()),
        "total_books": (db.query(Book).filter(Book.deleted_at.is_(None)).count()),
        "total_authors": (db.query(Author).filter(Author.deleted_at.is_(None)).count()),
        "total_publishers": (
            db.query(Publisher).filter(Publisher.deleted_at.is_(None)).count()
        ),
        "total_tags": (db.query(Tag).filter(Tag.deleted_at.is_(None)).count()),
        "total_shelves": (db.query(Shelf).filter(Shelf.deleted_at.is_(None)).count()),
        "total_notes": db.query(Note).count(),
        "total_highlights": db.query(Highlight).count(),
        "total_wishlists": db.query(Wishlist).count(),
        "total_reading_goals": db.query(ReadingGoal).count(),
    }


def get_users(
    db: Session,
):
    return (
        db.query(User)
        .filter(User.deleted_at.is_(None))
        .order_by(User.created_at.desc())
        .all()
    )


def update_user_role(
    user_id,
    role,
    db: Session,
):
    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.deleted_at.is_(None),
        )
        .first()
    )

    if not user:
        return None

    user.role = role

    db.commit()
    db.refresh(user)

    return user


def promote_user(
    user_id,
    db: Session,
):
    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.deleted_at.is_(None),
        )
        .first()
    )

    if not user:
        raise NotFoundException("User not found")

    user.role = RoleEnum.ADMIN

    db.commit()

    db.refresh(user)

    return user


def demote_user(
    user_id,
    db: Session,
):
    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.deleted_at.is_(None),
        )
        .first()
    )

    if not user:
        raise NotFoundException("User not found")

    user.role = RoleEnum.USER

    db.commit()

    db.refresh(user)

    return user


def delete_user(
    user_id,
    db: Session,
):
    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.deleted_at.is_(None),
        )
        .first()
    )

    if not user:
        raise NotFoundException("User not found")

    return soft_delete(
        user,
        db,
    )


def delete_book(
    book_id,
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
        raise NotFoundException("Book not found")

    return soft_delete(
        book,
        db,
    )


def delete_shelf(shelf_id, db: Session):
    shelf = (
        db.query(Shelf)
        .filter(
            Shelf.id == shelf_id,
            Shelf.deleted_at.is_(None),
        )
        .first()
    )

    if not shelf:
        raise NotFoundException("Book not found")

    return soft_delete(
        shelf,
        db,
    )


def restore_user(
    user_id,
    db: Session,
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise NotFoundException("User not found")

    user.deleted_at = None

    db.commit()

    db.refresh(user)

    return user


def restore_book(
    book_id,
    db: Session,
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise NotFoundException("Book not found")

    book.deleted_at = None

    db.commit()

    db.refresh(book)

    return book


def restore_shelf(
    shelf_id,
    db: Session,
):
    shelf = db.query(Shelf).filter(Shelf.id == shelf_id).first()

    if not shelf:
        raise NotFoundException("Shelf not found")

    shelf.deleted_at = None

    db.commit()

    db.refresh(shelf)

    return shelf
