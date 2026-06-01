from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_books():
    return {
        "message": "List of books",
        "books": ["Book 1", "Book 2", "Book 3"],
    }


@router.post("/")
def create_book():
    return {
        "message": "Book created",
        "books": ["Book 1", "Book 2", "Book 3"],
    }
