from datetime import datetime

from app.models.book import Book
from app.models.author import Author
from app.models.publisher import Publisher
from app.models.tag import Tag


def restore_book(
    book_id,
    db,
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        return None

    book.deleted_at = None

    db.commit()
    db.refresh(book)

    return book


def restore_author(
    author_id,
    db,
):
    author = db.query(Author).filter(Author.id == author_id).first()

    if not author:
        return None

    author.deleted_at = None

    db.commit()
    db.refresh(author)

    return author


def restore_publisher(
    publisher_id,
    db,
):
    publisher = db.query(Publisher).filter(Publisher.id == publisher_id).first()

    if not publisher:
        return None

    publisher.deleted_at = None

    db.commit()
    db.refresh(publisher)

    return publisher


def restore_tag(
    tag_id,
    db,
):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()

    if not tag:
        return None

    tag.deleted_at = None

    db.commit()
    db.refresh(tag)

    return tag
