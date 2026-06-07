from datetime import datetime
from sqlalchemy.orm import Session
from app.models.book import Book
from app.models.user import User
from app.models.shelf import Shelf
from app.models.user_book import UserBook
from app.models.reading_goal import ReadingGoal

from app.models.enums import ReadStatusEnum

from app.schemas.user_book import UserBookCreate, UserBookUpdate, UserBookResponse


# add to own lib
def create_user_book(payload: UserBookCreate, current_user: User, db: Session):
    book = db.query(Book).filter(Book.id == payload.book_id).first()

    if not book:
        raise ValueError("Book not found.")

    existing = (
        db.query(UserBook)
        .filter(
            UserBook.user_id == current_user.id, UserBook.book_id == payload.book_id
        )
        .first()
    )

    if existing:
        raise ValueError("Book already in your library.")

    if payload.shelf_id:
        shelf = db.query(Shelf).filter(Shelf.id == payload.shelf_id).first()

        if not shelf:
            raise ValueError("Shelf not found.")

    user_book = UserBook(
        user_id=current_user.id, book_id=payload.book_id, shelf_id=payload.shelf_id
    )

    db.add(user_book)
    db.commit()
    db.refresh(user_book)
    return user_book


def get_my_library(current_user: User, db: Session):
    return db.query(UserBook).filter(UserBook.user_id == current_user.id).all()


def update_user_book(
    user_book_id, payload: UserBookUpdate, current_user: User, db: Session
):
    user_book = (
        db.query(UserBook)
        .filter(UserBook.id == user_book_id, UserBook.user_id == current_user.id)
        .first()
    )
    current_year = datetime.utcnow().year

    if not user_book:
        raise ValueError("Book not found.")

    if payload.shelf_id is not None:
        user_book.shelf_id = payload.shelf_id
    if payload.current_page is not None:
        user_book.current_page = payload.current_page
    if payload.rating is not None:
        user_book.rating = payload.rating
    if payload.is_private is not None:
        user_book.is_private = payload.is_private
    if payload.purchase_date is not None:
        user_book.purchase_date = payload.purchase_date

    if payload.read_status is not None:
        # track prev status to prev dup counting
        old_status = user_book.read_status
        user_book.read_status = payload.read_status

        if payload.read_status == ReadStatusEnum.IN_PROGRESS:
            user_book.reading_started_at = datetime.utcnow()

        if payload.read_status == ReadStatusEnum.COMPLETED:
            user_book.reading_completed_at = datetime.utcnow()

            if old_status != ReadStatusEnum.COMPLETED:
                goal = (
                    db.query(ReadingGoal)
                    .filter(
                        ReadingGoal.user_id == current_user.id,
                        ReadingGoal.year == current_year,
                    )
                    .first()
                )

                if goal:
                    goal.completed_books += 1

            if (
                old_status == ReadStatusEnum.COMPLETED
                and payload.read_status != ReadStatusEnum.COMPLETED
            ):
                goal = (
                    db.query(ReadingGoal)
                    .filter(
                        ReadingGoal.user_id == current_user.id,
                        ReadingGoal.year == current_year,
                    )
                    .first()
                )
                if goal and goal.completed_books > 0:
                    goal.completed_books -= 1

    db.commit()
    db.refresh(user_book)
    return user_book
