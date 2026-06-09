from uuid import UUID
from datetime import datetime
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.user import User
from app.models.book import Book
from app.models.shelf import Shelf
from app.models.note import Note
from app.models.highlight import Highlight

from app.models.enums import RoleEnum

from app.core.admin import require_admin

router = APIRouter()


@router.get("/dashboard")
def dashboard(
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return {
        "total_users": db.query(User).filter(User.deleted_at.is_(None)).count(),
        "total_books": db.query(Book).filter(Book.deleted_at.is_(None)).count(),
        "total_shelves": db.query(Shelf).filter(Shelf.deleted_at.is_(None)).count(),
        "total_notes": db.query(Note).filter(Note.deleted_at.is_(None)).count(),
        "total_highlights": db.query(Highlight)
        .filter(Highlight.deleted_at.is_(None))
        .count(),
    }


@router.get("/users")
def get_users(
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return db.query(User).filter(User.deleted_at.is_(None)).all()


@router.get("/books")
def get_books(
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return db.query(Book).filter(Book.deleted_at.is_(None)).all()


@router.get("/shelves")
def get_shelves(
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return db.query(Shelf).filter(Shelf.deleted_at.is_(None)).all()


@router.patch("/users/{user_id}/promote")
def promote_user(
    user_id: UUID,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
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
        return {"message": "User not found"}

    user.role = RoleEnum.ADMIN

    db.commit()
    db.refresh(user)

    return {
        "message": "User promoted successfully",
        "role": user.role,
    }


@router.patch("/users/{user_id}/demote")
def demote_user(
    user_id: UUID,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
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
        return {"message": "User not found"}

    user.role = RoleEnum.USER

    db.commit()
    db.refresh(user)

    return {
        "message": "User demoted successfully",
        "role": user.role,
    }


@router.delete("/users/{user_id}")
def delete_user(
    user_id: UUID,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
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
        return {"message": "User not found"}

    user.deleted_at = datetime.utcnow()

    db.commit()

    return {
        "message": "User deleted successfully",
    }


@router.delete("/books/{book_id}")
def delete_book(
    book_id: UUID,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
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
        return {"message": "Book not found"}

    book.deleted_at = datetime.utcnow()

    db.commit()

    return {
        "message": "Book deleted successfully",
    }


@router.delete("/shelves/{shelf_id}")
def delete_shelf(
    shelf_id: UUID,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    shelf = (
        db.query(Shelf)
        .filter(
            Shelf.id == shelf_id,
            Shelf.deleted_at.is_(None),
        )
        .first()
    )

    if not shelf:
        return {"message": "Shelf not found"}

    shelf.deleted_at = datetime.utcnow()

    db.commit()

    return {
        "message": "Shelf deleted successfully",
    }
