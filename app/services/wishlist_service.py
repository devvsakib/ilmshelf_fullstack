from sqlalchemy.orm import Session
from app.models.wishlist import Wishlist
from app.models.user import User
from app.schemas.wishlist import WishlistCreate


def create_wishlist(payload: WishlistCreate, current_user: User, db: Session):
    existing = (
        db.query(Wishlist)
        .filter(
            Wishlist.user_id == current_user.id, Wishlist.book_id == payload.book_id
        )
        .first()
    )

    if existing:
        raise ValueError("Already in wishlist")

    wishlist = Wishlist(user_id=current_user.id, book_id=payload.book_id)
    db.add(wishlist)
    db.commit()
    db.refresh(wishlist)

    return wishlist


def get_wishlist(current_user: User, db: Session):
    return db.query(Wishlist).filter(Wishlist.user_id == current_user.id).all()


def delete_wishlist(wishlist_book_id, current_user: User, db: Session):
    wishlist = (
        db.query(Wishlist)
        .filter(Wishlist.id == wishlist_book_id, Wishlist.user_id == current_user.id)
        .first()
    )
    if not wishlist:
        raise ValueError("Wishlist not found")
    db.delete(wishlist)
    db.commit()

    return True
