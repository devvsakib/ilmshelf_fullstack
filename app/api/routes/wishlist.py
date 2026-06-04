from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.wishlist_service import create_wishlist, delete_wishlist, get_wishlist
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.wishlist import Wishlist
from app.schemas.wishlist import WishlistResponse, WishlistCreate

router = APIRouter()


@router.post("", response_model=WishlistResponse)
def create_new_wishlist(
    payload: WishlistCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return create_wishlist(payload, current_user, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[WishlistResponse])
def get_all_wishlist(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_wishlist(current_user, db)


@router.delete("/{wishlist_book_id}")
def remove_wishlist(
    wishlist_book_id,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return delete_wishlist(wishlist_book_id, current_user, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
