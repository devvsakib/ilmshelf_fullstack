from app.models.user_book import UserBook
from app.models.enums import ReadStatusEnum

def get_statistics(
    user_id,
    db,
):
    total_books = db.query(UserBook).filter(UserBook.user_id == user_id).count()

    completed_books = (
        db.query(UserBook)
        .filter(
            UserBook.user_id == user_id,
            UserBook.read_status == ReadStatusEnum.COMPLETED,
        )
        .count()
    )

    reading_books = (
        db.query(UserBook)
        .filter(
            UserBook.user_id == user_id,
            UserBook.read_status == ReadStatusEnum.IN_PROGRESS,
        )
        .count()
    )

    completion_rate = (
        round(
            completed_books / total_books * 100,
            2,
        )
        if total_books
        else 0
    )

    return {
        "total_books": total_books,
        "completed_books": completed_books,
        "reading_books": reading_books,
        "completion_rate": completion_rate,
    }
