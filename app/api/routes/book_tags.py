from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.core.admin import require_admin

from app.schemas.book_tag_schema import BookTagCreate, BookTagResponse

from app.services import book_tag_service

router = APIRouter()


@router.post(
    "/books/{book_id}/tags",
    response_model=BookTagResponse,
)
def assign_tag(
    book_id: UUID,
    payload: BookTagCreate,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    result = book_tag_service.assign_tag_to_book(
        book_id,
        payload,
        db,
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Book or Tag not found",
        )

    return result


@router.get(
    "/books/{book_id}/tags",
    response_model=list[BookTagResponse],
)
def get_book_tags(
    book_id: UUID,
    db: Session = Depends(get_db),
):
    return book_tag_service.get_book_tags(
        book_id,
        db,
    )


@router.delete("/book-tags/{book_tag_id}")
def remove_book_tag(
    book_tag_id: UUID,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    result = book_tag_service.remove_book_tag(
        book_tag_id,
        db,
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="BookTag not found",
        )

    return result
