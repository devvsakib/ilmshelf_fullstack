from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.models.shelf import Shelf
from app.core.auth import get_current_user
from app.models.enums import ShelfTypeEnum
from app.schemas.shelf import ShelfCreate, ShelfResponse
from app.services.shelf_service import create_shelf, get_my_shelves, get_public_shelves

router = APIRouter()


@router.post("", response_model=ShelfResponse)
def create_new_shelf(
    payload: ShelfCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_shelf(
        payload,
        current_user,
        db,
    )


@router.get("/")
def public_shelves(
    db: Session = Depends(
        get_db,
    ),
):
    return get_public_shelves(db)


@router.get("/my", response_model=list[ShelfResponse])
def my_shelves(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(
        get_db,
    ),
):
    return get_my_shelves(current_user, db)
