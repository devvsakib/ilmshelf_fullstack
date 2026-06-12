from fastapi import HTTPException


def raise_not_found(
    message="Resource not found",
):
    raise HTTPException(
        status_code=404,
        detail=message,
    )
