from pydantic import BaseModel

# Import BaseModel for validation.


class CreateBookSchema(BaseModel):
    # Schema used when creating a book.

    title: str
    # Book title.

    author: str
    # Author name.

    pages: int
    # Total pages.

    description: str
