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
from app.services import admin_service

router = APIRouter()


@router.get("/dashboard")
def dashboard(
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return admin_service.get_dashboard(db)


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
    return admin_service.promote_user(user_id, db)


@router.patch("/users/{user_id}/demote")
def demote_user(
    user_id: UUID,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return admin_service.demote_user(user_id, db)


@router.delete("/users/{user_id}")
def delete_user(
    user_id: UUID,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return admin_service.delete_user(user_id, db)


@router.delete("/books/{book_id}")
def delete_book(
    book_id: UUID,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return admin_service.delete_book(book_id, db)


@router.delete("/shelves/{shelf_id}")
def delete_shelf(
    shelf_id: UUID,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return admin_service.delete_shelf(shelf_id, db)


@router.patch("/users/{user_id}/restore")
def restore_user(
    user_id: UUID,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return admin_service.restore_user(
        user_id,
        db,
    )


@router.patch("/books/{book_id}/restore")
def restore_book(
    book_id: UUID,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return admin_service.restore_book(
        book_id,
        db,
    )


@router.patch("/shelves/{shelf_id}/restore")
def restore_shelf(
    shelf_id: UUID,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return admin_service.restore_shelf(
        shelf_id,
        db,
    )
