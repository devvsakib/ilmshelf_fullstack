from fastapi import HTTPException


class NotFoundException(HTTPException):
    def __init__(self, message="Resource not found"):
        super().__init__(
            status_code=404,
            detail=message,
        )
