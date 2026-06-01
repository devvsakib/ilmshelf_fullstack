from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.shelf import Shelf
from app.models.user import User
from app.schemas.shelf import ShelfCreate

from app.utils.slug import generate_slug


def create_shelf(payload: ShelfCreate, current_user: User, db: Session):
    shelf_slug = generate_slug(payload.name)
    existing_shelf = (
        db.query(Shelf)
        .filter(
            Shelf.created_by == current_user.id,
            Shelf.slug == shelf_slug,
        )
        .first()
    )

    if existing_shelf:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a shelf with this name.",
        )

    shelf = Shelf(
        name=payload.name,
        slug=shelf_slug,
        type=payload.type,
        is_public=payload.is_public,
        created_by=current_user.id,
    )

    db.add(shelf)
    db.commit()
    db.refresh(shelf)

    return shelf


def get_my_shelves(current_user: User, db: Session):
    return db.query(Shelf).filter(Shelf.created_by == current_user.id).all()
