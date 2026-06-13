from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.core.admin import require_admin

from app.services import admin_restore_service

router = APIRouter()


@router.post("/books/{book_id}/restore")
def restore_book(
    book_id: UUID,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    result = admin_restore_service.restore_book(
        book_id,
        db,
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    return {"message": "Book restored successfully"}


@router.post("/authors/{author_id}/restore")
def restore_author(
    author_id: UUID,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    result = admin_restore_service.restore_author(
        author_id,
        db,
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return {"message": "Author restored successfully"}


@router.post("/publishers/{publisher_id}/restore")
def restore_publisher(
    publisher_id: UUID,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    result = admin_restore_service.restore_publisher(
        publisher_id,
        db,
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Publisher not found",
        )

    return {"message": "Publisher restored successfully"}


@router.post("/tags/{tag_id}/restore")
def restore_tag(
    tag_id: UUID,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    result = admin_restore_service.restore_tag(
        tag_id,
        db,
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Tag not found",
        )

    return {"message": "Tag restored successfully"}
