from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.book import BookCreate, BookResponse, BookUpdate
from app.db.database import get_db
from app.core.auth import get_current_user
from app.core.admin import require_admin
from app.services import book_service
from app.schemas.book_details_schema import BookDetailsResponse
from app.schemas.book_list_schema import BookListResponse
from uuid import UUID
from typing import Optional

router = APIRouter()


@router.post(
    "",
    response_model=BookResponse,
)
def create_new_book(
    payload: BookCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return book_service.create_book(
            payload,
            current_user,
            db,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "",
    response_model=BookListResponse,
)
def get_books(
    search: Optional[str] = None,
    publisher_id: Optional[UUID] = None,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    return book_service.search_books(
        db=db,
        search=search,
        publisher_id=publisher_id,
        page=page,
        limit=limit,
    )


@router.get("/{book_id}")
def get_single_book(
    book_id: UUID,
    db: Session = Depends(get_db),
):
    book = book_service.get_single_book_details(
        book_id,
        db,
    )

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    return book


@router.get(
    "/{book_id}/details",
    response_model=BookDetailsResponse,
)
def get_book_details(
    book_id: UUID,
    db: Session = Depends(get_db),
):
    book = book_service.get_book_details(
        book_id,
        db,
    )

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    return book


@router.patch("/{book_id}")
def update_book(
    book_id: UUID,
    payload: BookUpdate,
    db: Session = Depends(get_db),
):
    return book_service.update_book(
        book_id,
        payload,
        db,
    )


@router.delete("/{book_id}")
def delete_book(
    book_id: UUID,
    db: Session = Depends(get_db),
):
    return book_service.delete_book(
        book_id,
        db,
    )
