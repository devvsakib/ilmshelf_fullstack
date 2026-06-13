from app.models.user_book import UserBook
from app.models.enums import ReadStatusEnum
from sqlalchemy import extract
from app.models.reading_session import ReadingSession


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


def get_monthly_statistics(
    user_id,
    db,
):
    rows = (
        db.query(ReadingSession)
        .filter(
            ReadingSession.user_id == user_id,
            ReadingSession.deleted_at.is_(None),
        )
        .all()
    )

    result = {}

    for row in rows:
        month = row.started_at.strftime("%Y-%m")

        if month not in result:
            result[month] = {
                "month": month,
                "sessions": 0,
                "pages_read": 0,
                "reading_hours": 0,
            }

        result[month]["sessions"] += 1
        result[month]["pages_read"] += row.pages_read

        if row.ended_at:
            hours = (row.ended_at - row.started_at).total_seconds() / 3600

            result[month]["reading_hours"] += round(
                hours,
                2,
            )

    return list(
        sorted(
            result.values(),
            key=lambda x: x["month"],
            reverse=True,
        )
    )


def get_yearly_statistics(
    user_id,
    db,
):
    rows = (
        db.query(ReadingSession)
        .filter(
            ReadingSession.user_id == user_id,
            ReadingSession.deleted_at.is_(None),
        )
        .all()
    )

    result = {}

    for row in rows:
        year = row.started_at.year

        if year not in result:
            result[year] = {
                "year": year,
                "sessions": 0,
                "pages_read": 0,
                "reading_hours": 0,
            }

        result[year]["sessions"] += 1
        result[year]["pages_read"] += row.pages_read

        if row.ended_at:
            hours = (row.ended_at - row.started_at).total_seconds() / 3600

            result[year]["reading_hours"] += round(
                hours,
                2,
            )

    return list(
        sorted(
            result.values(),
            key=lambda x: x["year"],
            reverse=True,
        )
    )
