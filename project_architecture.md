# PROJECT 1: "CURATOR" API ARCHITECTURE

## Why Separate Files? The "Separation of Concerns" Principle

- **Maintainability:** As an application grows, having thousands of lines of code in one `main.py` file becomes impossible to navigate and manage.
- **Readability:** When you look at a file, you know exactly what its purpose is. `models.py` only contains database table definitions. `schemas.py` only contains data shapes for the API.
- **Testability:** It's much easier to write tests for small, focused pieces of code than for one giant, tangled file.
- **Collaboration:** Multiple developers can work on different files (`users.py`, `content.py`) at the same time without creating conflicts.

## Our Core Application Files (inside the `app/` directory)

- **`main.py` (The Entry Point / The Conductor):**
  - Its main job is to create the single FastAPI application instance.
  - It will be responsible for bringing together ("including") all the different routers from other files.
  - It should contain almost NO business logic itself. It's the orchestra conductor, not an instrument.

- **`database.py` (The Database Plumber):**
  - Its only job is to handle the database connection.
  - It will create the SQLAlchemy `engine` (the connection pool) and the `SessionLocal` class (the session factory).
  - It will also define the `Base` class that all our models will inherit from.

- **`models.py` (The Database Blueprint):**
  - This file defines what our database tables look like, using Python classes.
  - Each class in this file maps directly to a table in our PostgreSQL database.
  - This is the "shape" of our data *in the database*.

- **`schemas.py` (The API Contract):**
  - This file defines the "shape" of the data for our API, using Pydantic models.
  - It controls what data we expect to receive in API requests (e.g., a new user must have an `email` and `password`).
  - It also controls what data we send back in API responses (e.g., never send back a user's `hashed_password`).
  - It acts as the data validation and serialization layer, separate from the database models.

- **`crud.py` (The Database Worker):**
  - "CRUD" stands for **C**reate, **R**ead, **U**pdate, **D**elete.
  - This file will contain simple, reusable functions that perform these basic operations on the database.
  - For example: `get_user_by_email(db, email)`, `create_user(db, user_data)`.
  - This keeps all our direct database interactions in one place.

- **`routers/` directory (The API Departments):**
  - (We will create this directory later)
  - As our API grows, we will group related endpoints into different files. For example, all user-related endpoints (`/users/`, `/users/{id}`) will live in `routers/users.py`. All content-related endpoints will live in `routers/content.py`.