import re
import uuid


def generate_slug(text: str):
    slug = text.lower()

    slug = re.sub(r"[^a-z0-9\s-]", "", slug)

    slug = re.sub(r"\s+", "-", slug)

    slug = slug.strip("-")

    if not slug:
        slug = str(uuid.uuid4())

    return slug
