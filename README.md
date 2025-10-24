# Project: Curator API

The "Curator" API is the backend service for a content curation platform. Its mission is to provide a robust, fast, and reliable system for authenticated users to save, organize, and discover interesting online content (articles, videos, etc.) through a flexible tagging system.

## Core Features (MVP)

1.  **User Authentication:**
    - Users can register with an email and password.
    - Users can log in to receive a JWT access token.
    - All other endpoints will be protected.

2.  **Content Submission:**
    - An authenticated user can submit content via a URL.
    - The service will attempt to fetch the content's title from the URL.
    - Users can perform CRUD (Create, Read, Update, Delete) operations on their own content.

3.  **Tagging System:**
    - Users can associate one or more "tags" with content.
    - This is a many-to-many relationship (`content` <-> `tags`).

4.  **Content Discovery:**
    - Users can follow/unfollow specific tags.
    - A personalized "feed" endpoint will provide content based on followed tags.

## Technology Stack

- **Language:** Python 3.10+
- **Web Framework:** FastAPI
- **Database:** PostgreSQL
- **Data Validation:** Pydantic
- **Database Migrations:** Alembic
- **Containerization:** Docker & Docker Compose
- **Authentication:** JWT with Passlib for password hashing

## Initial Database Schema

- **`users` Table:** `id`, `email`, `hashed_password`, `full_name`, `created_at`
- **`content` Table:** `id`, `url`, `title`, `submitter_id` (FK to users), `submitted_at`
- **`tags` Table:** `id`, `name` (unique)
- **`content_tags` Association Table:** `content_id`, `tag_id`
- **`user_followed_tags` Association Table:** `user_id`, `tag_id`

---

## Week 1 (Oct 27 - Nov 2) Development Plan

- [ ] Create SQLAlchemy models for `User`, `Content`, and `Tag` in `app/models.py`.
- [ ] Define the many-to-many association tables in the models.
- [ ] Set up the main database connection logic in `app/database.py`.
- [ ] Initialize Alembic for this project and generate the first migration script.
- [ ] Apply the first migration to create all tables in the database.