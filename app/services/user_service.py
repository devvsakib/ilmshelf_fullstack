from fastapi import HTTPException
from app.models.user import User
from app.models.user_book import UserBook
from app.models.shelf import Shelf

# Assuming your hashing utilities reside here. Adjust path if necessary!
from app.core.security import verify_password, hash_password


def get_public_profile(user_id, db):
    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.deleted_at.is_(None),
        )
        .first()
    )

    if not user:
        return None

    books_count = db.query(UserBook).filter(UserBook.user_id == user_id).count()

    completed_books = (
        db.query(UserBook)
        .filter(
            UserBook.user_id == user_id,
            UserBook.read_status == "COMPLETED",
        )
        .count()
    )

    shelves_count = (
        db.query(Shelf)
        .filter(
            Shelf.created_by == user_id,
            Shelf.deleted_at.is_(None),
        )
        .count()
    )

    return {
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name,
        "books_count": books_count,
        "completed_books": completed_books,
        "shelves_count": shelves_count,
    }


def get_me(current_user):
    return current_user


def update_me(current_user, payload, db):
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(current_user, key, value)

    db.commit()
    db.refresh(current_user)
    return current_user


def change_password(current_user, payload, db):
    if not verify_password(payload.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=400,
            detail="Current password incorrect",
        )

    current_user.password_hash = hash_password(payload.new_password)
    db.commit()

    return {"message": "Password changed successfully"}
