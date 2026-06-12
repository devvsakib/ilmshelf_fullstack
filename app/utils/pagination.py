from math import ceil


def paginate(
    query,
    page: int = 1,
    limit: int = 20,
):
    total = query.count()

    items = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "items": items,
        "page": page,
        "limit": limit,
        "total": total,
        "pages": ceil(total / limit) if total else 0,
    }
