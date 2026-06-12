from app.models.user import User
from app.models.user_book import UserBook
from app.models.shelf import Shelf


def get_public_profile(
    user_id,
    db,
):
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
