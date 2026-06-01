from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_userBooks():
    return {
        "message": "List of books",
        "books": ["Book 1", "Book 2", "Book 3"],
    }

@router.post("/")
def create_userBook():
    return {
        "message": "Book added to library",
        "books": ["Book 1", "Book 2", "Book 3"],
    }
