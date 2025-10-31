from sqlalchemy.orm import Session
from . import models, schemas
from . import security
# app/crud.py
from typing import List, Optional
from . import models, schemas, security
# ... rest of the file
# We import models and schemas to have access to our Pydantic and SQLAlchemy models.
# The '.' means import from the same directory (the 'app' folder).


def get_user_by_email(db: Session, email:str):
    return db.query(models.User).filter(models.User.email == email).first()
    # This function queries the database for a user with a specific email.
    # db.query(models.User): Start a query on the 'users' table.
    # .filter(models.User.email == email): Add a WHERE clause to the query.
    # .first(): Execute the query and return only the first result found, or None if no user is found.

def create_user(db: Session, user: schemas.UserCreate):
    """
    Creates a new user in the database.
    1. Hashes the plain-text password.
    2. Creates a new SQLAlchemy User model instance.
    3. Adds it to the session, commits it to the DB, and refreshes the instance.
    """
    # Step 1: Hash the password from the incoming user data.
    hashed_password = security.get_password_hash(user.password)

    # Step 2: Create a SQLAlchemy User model instance from the data.
    # We DON'T store the plain 'user.password'. We store the 'hashed_password'.
    db_user = models.User(
        email=user.email, 
        full_name=user.full_name,
        hashed_password=hashed_password
    )

    # Step 3: Add the new user object to the database session.
    db.add(db_user)

    # Step 4: Commit the changes to the database. This is what actually saves it. 
    db.commit()

    # Step 5: Refresh the 'db_user' instance. This makes the database return
    # the new data that was created, like the auto-generated 'id' and 'created_at'.
    db.refresh(db_user)
    
    # Step 6: Return the new user instance.
    return db_user

def create_user_content(db: Session, content: schemas.ContentCreate, user_id: int) -> models.Content:
    """Creates a new content item in the DB associated with a user."""
    db_content = models.Content(**content.dict(), owner_id=user_id)
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

def get_content(db: Session, skip: int = 0, limit: int = 100) -> List[models.Content]:
    """Returns a list of all content items, with pagination."""
    return db.query(models.Content).offset(skip).limit(limit).all()

def get_content_by_id(db: Session, content_id: int) -> Optional[models.Content]:
    """Returns a single content item by its ID, or None if not found."""
    return db.query(models.Content).filter(models.Content.id == content_id).first()


def delete_content_by_id(db: Session, content_id: int) -> Optional[models.Content]:
    """Deletes a content item from the DB by its ID."""
    db_content = db.query(models.Content).filter(models.Content.id == content_id).first()
    if db_content:
        db.delete(db_content)
        db.commit()
    return db_content