from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.services import discover_service

from app.schemas.discover_schema import (
    DiscoverBookResponse,
)

router = APIRouter()


@router.get(
    "/recent",
    response_model=list[DiscoverBookResponse],
)
def recent_books(
    db: Session = Depends(get_db),
):
    return discover_service.recent_books(db)


@router.get(
    "/popular",
    response_model=list[DiscoverBookResponse],
)
def popular_books(
    db: Session = Depends(get_db),
):
    return discover_service.popular_books(db)
