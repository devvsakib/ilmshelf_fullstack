def paginate(
    query,
    page: int = 1,
    limit: int = 20,
):
    total = query.count()

    items = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit,
    }
