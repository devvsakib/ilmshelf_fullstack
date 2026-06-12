from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.core.admin import require_admin

from app.schemas.tag_schema import TagCreate, TagUpdate, TagResponse

from app.services import tag_service

router = APIRouter()


@router.post(
    "/",
    response_model=TagResponse,
)
def create_tag(
    payload: TagCreate,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    return tag_service.create_tag(
        payload,
        db,
    )


@router.get(
    "/",
    response_model=list[TagResponse],
)
def get_tags(
    db: Session = Depends(get_db),
):
    return tag_service.get_tags(db)


@router.get(
    "/{tag_id}",
    response_model=TagResponse,
)
def get_tag(
    tag_id: UUID,
    db: Session = Depends(get_db),
):
    tag = tag_service.get_tag(
        tag_id,
        db,
    )

    if not tag:
        raise HTTPException(
            404,
            "Tag not found",
        )

    return tag


@router.patch(
    "/{tag_id}",
    response_model=TagResponse,
)
def update_tag(
    tag_id: UUID,
    payload: TagUpdate,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    tag = tag_service.update_tag(
        tag_id,
        payload,
        db,
    )

    if not tag:
        raise HTTPException(
            404,
            "Tag not found",
        )

    return tag


@router.delete("/{tag_id}")
def delete_tag(
    tag_id: UUID,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    result = tag_service.delete_tag(
        tag_id,
        db,
    )

    if not result:
        raise HTTPException(
            404,
            "Tag not found",
        )

    return result
