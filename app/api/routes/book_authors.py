from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.core.admin import require_admin

from app.schemas.book_author_schema import (
    BookAuthorCreate,
    BookAuthorResponse,
    BookAuthorDetailsResponse,
)

from app.services import book_author_service

router = APIRouter()


@router.post(
    "/books/{book_id}/authors",
    response_model=BookAuthorResponse,
)
def assign_author_to_book(
    book_id: UUID,
    payload: BookAuthorCreate,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    result = book_author_service.assign_author_to_book(
        book_id,
        payload,
        db,
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Book or Author not found",
        )

    return result


@router.get(
    "/books/{book_id}/authors",
    response_model=list[BookAuthorDetailsResponse],
)
def get_book_authors(
    book_id: UUID,
    db: Session = Depends(get_db),
):
    return book_author_service.get_book_authors(
        book_id,
        db,
    )


@router.delete(
    "/book-authors/{book_author_id}",
)
def delete_book_author(
    book_author_id: UUID,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    result = book_author_service.delete_book_author(
        book_author_id,
        db,
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Assignment not found",
        )

    return result
