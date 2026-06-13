from fastapi import (
    APIRouter,
    Depends,
    Query,
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.services import search_service

from app.schemas.search_schema import (
    GlobalSearchResponse,
)

router = APIRouter()


@router.get(
    "",
    response_model=GlobalSearchResponse,
)
def global_search(
    q: str = Query(
        ...,
        min_length=1,
    ),
    db: Session = Depends(get_db),
):
    return search_service.global_search(
        q,
        db,
    )
