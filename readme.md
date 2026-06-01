# IlmShelf Backend Architecture

## Overview

IlmShelf is a scalable Islamic personal library and research platform.

Core Concepts:

* Global public book catalog
* Personal user libraries
* System and custom shelves
* Reading progress tracking
* Notes/highlights
* Wishlist and goals
* Public/private books
* Future AI and community support

---

# Recommended Stack

## Backend

* Python FastAPI
* SQLAlchemy
* Alembic
* Pydantic

## Database

* PostgreSQL

## Cache (Later)

* Redis

## Auth

* JWT

## File Storage (Later)

* Cloudflare R2 / S3 compatible storage

---

# Why PostgreSQL Instead of MongoDB

PostgreSQL fits this application better because:

* Many-to-many relationships
* User ↔ Book ↔ Shelf relations
* Search and indexing support
* Analytics possibilities
* Better consistency
* Easier recommendation systems later
* Better long-term scalability

MongoDB would become difficult once:

* books belong to multiple shelves
* users have independent states
* recommendation systems are added
* community/social features grow

Use PostgreSQL.

---

# Core Database Entities

## Main Tables

```txt
users
books
authors
publishers
shelves
book_shelves
book_authors
book_tags
tags
user_books
notes
highlights
wishlists
reading_goals
lending_records
```

---

# ENUMS

## VisibilityEnum

```python
PUBLIC
PRIVATE
```

## ShelfTypeEnum

```python
SYSTEM
CUSTOM
```

## ReadStatusEnum

```python
NOT_STARTED
IN_PROGRESS
COMPLETED
ON_HOLD
DROPPED
```

## AuthorRoleEnum

```python
WRITER
TRANSLATOR
EDITOR
REVIEWER
```

---

# USERS TABLE

```sql
users
```

| Field         | Type           |
| ------------- | -------------- |
| id            | UUID           |
| name          | VARCHAR        |
| username      | VARCHAR UNIQUE |
| email         | VARCHAR UNIQUE |
| password_hash | TEXT           |
| avatar        | TEXT           |
| bio           | TEXT           |
| is_active     | BOOLEAN        |
| created_at    | TIMESTAMP      |
| updated_at    | TIMESTAMP      |
| deleted_at    | TIMESTAMP NULL |

Indexes:

* email
* username

---

# BOOKS TABLE

Global public catalog.

```sql
books
```

| Field          | Type           |
| -------------- | -------------- |
| id             | UUID           |
| slug           | VARCHAR UNIQUE |
| title_bn       | TEXT           |
| title_en       | TEXT           |
| title_ar       | TEXT           |
| description_bn | TEXT           |
| description_en | TEXT           |
| description_ar | TEXT           |
| cover_url      | TEXT           |
| isbn           | VARCHAR        |
| pages          | INTEGER        |
| published_year | INTEGER        |
| publisher_id   | UUID           |
| source         | VARCHAR        |
| visibility     | VisibilityEnum |
| owner_id       | UUID NULL      |
| language       | VARCHAR        |
| metadata       | JSONB          |
| created_at     | TIMESTAMP      |
| updated_at     | TIMESTAMP      |
| deleted_at     | TIMESTAMP NULL |

Indexes:

* slug
* isbn
* visibility
* GIN index on metadata
* Full text index on titles

Notes:

* owner_id NULL = public catalog book
* owner_id filled = private user-created book

---

# AUTHORS TABLE

```sql
authors
```

| Field      | Type      |
| ---------- | --------- |
| id         | UUID      |
| name_bn    | TEXT      |
| name_en    | TEXT      |
| name_ar    | TEXT      |
| bio        | TEXT      |
| avatar     | TEXT      |
| created_at | TIMESTAMP |

---

# BOOK_AUTHORS TABLE

Many-to-many relationship.

```sql
book_authors
```

| Field     | Type           |
| --------- | -------------- |
| id        | UUID           |
| book_id   | UUID           |
| author_id | UUID           |
| role      | AuthorRoleEnum |

Example:

* Writer
* Translator
* Reviewer

---

# PUBLISHERS TABLE

```sql
publishers
```

| Field      | Type      |
| ---------- | --------- |
| id         | UUID      |
| name       | VARCHAR   |
| website    | TEXT      |
| created_at | TIMESTAMP |

---

# TAGS TABLE

```sql
tags
```

| Field | Type           |
| ----- | -------------- |
| id    | UUID           |
| slug  | VARCHAR UNIQUE |
| name  | VARCHAR        |

---

# BOOK_TAGS TABLE

```sql
book_tags
```

| Field   | Type |
| ------- | ---- |
| id      | UUID |
| book_id | UUID |
| tag_id  | UUID |

---

# SHELVES TABLE

Supports both:

* system shelves
* custom user shelves

```sql
shelves
```

| Field      | Type          |
| ---------- | ------------- |
| id         | UUID          |
| name       | VARCHAR       |
| slug       | VARCHAR       |
| type       | ShelfTypeEnum |
| created_by | UUID NULL     |
| is_public  | BOOLEAN       |
| created_at | TIMESTAMP     |

Examples:

* Aqeedah
* Hadith
* Tafsir
* Ramadan Reading

---

# BOOK_SHELVES TABLE

Books can belong to multiple shelves.

```sql
book_shelves
```

| Field    | Type |
| -------- | ---- |
| id       | UUID |
| book_id  | UUID |
| shelf_id | UUID |

---

# USER_BOOKS TABLE

MOST IMPORTANT TABLE.

Stores user-specific reading state.

```sql
user_books
```

| Field                | Type           |
| -------------------- | -------------- |
| id                   | UUID           |
| user_id              | UUID           |
| book_id              | UUID           |
| shelf_id             | UUID           |
| read_status          | ReadStatusEnum |
| current_page         | INTEGER        |
| rating               | INTEGER        |
| is_private           | BOOLEAN        |
| reading_started_at   | TIMESTAMP NULL |
| reading_completed_at | TIMESTAMP NULL |
| purchase_date        | DATE NULL      |
| notes_count          | INTEGER        |
| metadata             | JSONB          |
| created_at           | TIMESTAMP      |
| updated_at           | TIMESTAMP      |

Indexes:

* user_id
* book_id
* read_status
* composite(user_id, book_id)

This table allows:

* multiple users saving same book
* independent progress tracking
* personal organization

---

# NOTES TABLE

```sql
notes
```

| Field        | Type      |
| ------------ | --------- |
| id           | UUID      |
| user_book_id | UUID      |
| content      | TEXT      |
| page         | INTEGER   |
| is_public    | BOOLEAN   |
| created_at   | TIMESTAMP |

---

# HIGHLIGHTS TABLE

```sql
highlights
```

| Field         | Type      |
| ------------- | --------- |
| id            | UUID      |
| user_book_id  | UUID      |
| page          | INTEGER   |
| selected_text | TEXT      |
| note          | TEXT      |
| created_at    | TIMESTAMP |

---

# WISHLISTS TABLE

```sql
wishlists
```

| Field      | Type      |
| ---------- | --------- |
| id         | UUID      |
| user_id    | UUID      |
| book_id    | UUID      |
| created_at | TIMESTAMP |

---

# READING_GOALS TABLE

```sql
reading_goals
```

| Field           | Type      |
| --------------- | --------- |
| id              | UUID      |
| user_id         | UUID      |
| year            | INTEGER   |
| target_books    | INTEGER   |
| completed_books | INTEGER   |
| created_at      | TIMESTAMP |

---

# LENDING_RECORDS TABLE

```sql
lending_records
```

| Field       | Type           |
| ----------- | -------------- |
| id          | UUID           |
| user_id     | UUID           |
| book_id     | UUID           |
| borrowed_to | VARCHAR        |
| borrowed_at | TIMESTAMP      |
| returned_at | TIMESTAMP NULL |

---

# Relationship Architecture

```txt
User
 ├── UserBooks
 │      ├── Notes
 │      └── Highlights
 │
 ├── Shelves
 ├── Wishlist
 ├── ReadingGoals
 └── LendingRecords

Book
 ├── Authors
 ├── Tags
 ├── Shelves
 └── UserBooks
```

---

# JSONB Usage

Use JSONB only where flexibility is beneficial.

Recommended:

## books.metadata

```json
{
  "edition": "2nd",
  "source_link": "...",
  "extra_info": {}
}
```

## user_books.metadata

```json
{
  "lastOpenedAt": "...",
  "device": "web"
}
```

Do NOT store core relational data inside JSONB.

---

# Soft Delete Strategy

Every major table should include:

```sql
deleted_at TIMESTAMP NULL
```

Instead of hard deleting.

Benefits:

* restore support
* audit support
* accidental deletion recovery

---

# Timestamp Strategy

Every major table:

```sql
created_at
updated_at
```

Auto-update updated_at using SQLAlchemy.

---

# Search Strategy

Use PostgreSQL Full Text Search later.

Searchable fields:

* title_bn
* title_en
* title_ar
* author names
* publisher
* tags

Potential future:

* Meilisearch
* Elasticsearch

---

# Recommended FastAPI Folder Structure

```txt
app/
 ├── api/
 │    ├── routes/
 │    │    ├── auth.py
 │    │    ├── books.py
 │    │    ├── shelves.py
 │    │    ├── user_books.py
 │    │    ├── notes.py
 │    │    └── wishlist.py
 │
 ├── core/
 │    ├── config.py
 │    ├── security.py
 │    └── database.py
 │
 ├── models/
 │    ├── user.py
 │    ├── book.py
 │    ├── author.py
 │    ├── shelf.py
 │    └── user_book.py
 │
 ├── schemas/
 │    ├── book.py
 │    ├── user.py
 │    └── shelf.py
 │
 ├── services/
 ├── repositories/
 ├── utils/
 └── main.py
```

---

# SQLAlchemy Example

## Book Model

```python
class Book(Base):
    __tablename__ = "books"

    id = Column(UUID(as_uuid=True), primary_key=True)
    slug = Column(String, unique=True, nullable=False)

    title_bn = Column(Text)
    title_en = Column(Text)
    title_ar = Column(Text)

    cover_url = Column(Text)

    visibility = Column(
        Enum(VisibilityEnum),
        default=VisibilityEnum.PUBLIC
    )

    created_at = Column(DateTime, default=datetime.utcnow)
```

---

# Pydantic Example

```python
class BookCreate(BaseModel):
    title_bn: str
    title_en: str | None = None
    description_bn: str | None = None
    pages: int | None = None
```

---

# API Structure

```txt
/api/v1/auth
/api/v1/books
/api/v1/shelves
/api/v1/user-books
/api/v1/notes
/api/v1/wishlist
/api/v1/goals
/api/v1/lending
```

---

# Authentication Flow

Use JWT:

```txt
POST /auth/register
POST /auth/login
POST /auth/refresh
```

Store:

* access token
* refresh token

---

# Migration Strategy from LocalStorage

Old structure:

```json
{
  "meta": {},
  "user": {}
}
```

Migration:

## meta

Move into:

* books table

## user

Move into:

* user_books table

---

# Future AI Features Compatibility

Architecture already supports:

* AI summaries
* semantic search
* recommendation engine
* OCR processing
* Arabic explanation
* scholar linking
* quote extraction

Because:

* books are normalized
* relationships are clean
* metadata is structured

---

# Future Community Features

Possible later:

* public profiles
* public shelves
* shared collections
* reviews
* comments
* following users
* reading clubs

Current architecture already supports expansion.

---

# MVP Recommendation

DO NOT build everything immediately.

Start with:

1. Authentication
2. Public books
3. User shelves
4. UserBooks
5. Notes
6. Search

Then expand.

---

# Final Recommendation

This project has strong potential because:

* clear niche
* real use case
* scalable structure
* reusable content
* community possibilities
* Islamic research potential

Focus on:

* excellent UX
* fast search
* clean organization
* mobile responsiveness
* simple onboarding

Ship early.
