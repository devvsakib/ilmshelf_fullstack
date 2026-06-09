from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.author_schema import (
    AuthorCreate,
    AuthorUpdate,
    AuthorResponse,
)

from app.services import author_service

from app.core.admin import require_admin

router = APIRouter()


@router.post(
    "/",
    response_model=AuthorResponse,
)
def create_author(
    payload: AuthorCreate,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return author_service.create_author(
        payload,
        db,
    )


@router.get(
    "/",
    response_model=list[AuthorResponse],
)
def get_authors(
    db: Session = Depends(get_db),
):
    return author_service.get_authors(db)


@router.get(
    "/{author_id}",
    response_model=AuthorResponse,
)
def get_author(
    author_id: UUID,
    db: Session = Depends(get_db),
):
    author = author_service.get_author(
        author_id,
        db,
    )

    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return author


@router.patch(
    "/{author_id}",
    response_model=AuthorResponse,
)
def update_author(
    author_id: UUID,
    payload: AuthorUpdate,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    author = author_service.update_author(
        author_id,
        payload,
        db,
    )

    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return author


@router.delete("/{author_id}")
def delete_author(
    author_id: UUID,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    result = author_service.delete_author(
        author_id,
        db,
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return result
