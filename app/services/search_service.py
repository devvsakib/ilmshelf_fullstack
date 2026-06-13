from app.models.book import Book
from app.models.author import Author
from app.models.publisher import Publisher
from app.models.tag import Tag


def global_search(
    query: str,
    db,
):
    books = (
        db.query(Book)
        .filter(
            Book.deleted_at.is_(None),
            (
                Book.title_bn.ilike(f"%{query}%")
                | Book.title_en.ilike(f"%{query}%")
                | Book.title_ar.ilike(f"%{query}%")
            ),
        )
        .limit(10)
        .all()
    )

    authors = (
        db.query(Author)
        .filter(
            Author.deleted_at.is_(None),
            (
                Author.name_bn.ilike(f"%{query}%")
                | Author.name_en.ilike(f"%{query}%")
                | Author.name_ar.ilike(f"%{query}%")
            ),
        )
        .limit(10)
        .all()
    )

    publishers = (
        db.query(Publisher)
        .filter(
            Publisher.deleted_at.is_(None),
            (
                Publisher.name.ilike(f"%{query}%")
            ),
        )
        .limit(10)
        .all()
    )

    tags = (
        db.query(Tag)
        .filter(
            Tag.deleted_at.is_(None),
            Tag.name.ilike(f"%{query}%"),
        )
        .limit(10)
        .all()
    )

    return {
        "books": books,
        "authors": authors,
        "publishers": publishers,
        "tags": tags,
    }
