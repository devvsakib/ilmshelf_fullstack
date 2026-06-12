from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.core.admin import require_admin

from app.services import publisher_service

from app.schemas.publisher_schema import (
    PublisherCreate,
    PublisherUpdate,
    PublisherResponse,
)

router = APIRouter()


@router.post(
    "/",
    response_model=PublisherResponse,
)
def create_publisher(
    payload: PublisherCreate,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return publisher_service.create_publisher(
        payload,
        db,
    )


@router.get(
    "/",
    response_model=list[PublisherResponse],
)
def get_publishers(
    db: Session = Depends(get_db),
):
    return publisher_service.get_publishers(db)


@router.get(
    "/{publisher_id}",
    response_model=PublisherResponse,
)
def get_publisher(
    publisher_id: UUID,
    db: Session = Depends(get_db),
):
    publisher = publisher_service.get_publisher(
        publisher_id,
        db,
    )

    if not publisher:
        raise HTTPException(
            404,
            "Publisher not found",
        )

    return publisher


@router.patch(
    "/{publisher_id}",
    response_model=PublisherResponse,
)
def update_publisher(
    publisher_id: UUID,
    payload: PublisherUpdate,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    publisher = publisher_service.update_publisher(
        publisher_id,
        payload,
        db,
    )

    if not publisher:
        raise HTTPException(
            404,
            "Publisher not found",
        )

    return publisher


@router.delete("/{publisher_id}")
def delete_publisher(
    publisher_id: UUID,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    result = publisher_service.delete_publisher(
        publisher_id,
        db,
    )

    if not result:
        raise HTTPException(
            404,
            "Publisher not found",
        )

    return result
