def paginate(query, page=1, limit=20):
    total = query.count()

    items = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "has_next": total > page * limit,
    }
