from fastapi import HTTPException


def get_or_404(
    query,
    message="Resource not found",
):
    item = query.first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail=message,
        )

    return item
