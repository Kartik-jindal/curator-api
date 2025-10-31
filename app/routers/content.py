# app/routers/content.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Import all the necessary components from our application
from .. import crud, models, schemas, database, security

# Create the router for content-related endpoints
router = APIRouter(
    prefix="/content",  # All routes in this file will start with /content
    tags=["Content"]      # Group them under "Content" in the API docs
)

@router.post("/", response_model=schemas.Content, status_code=status.HTTP_201_CREATED)
def create_new_content(
    content: schemas.ContentCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    """
    Creates a new content item for the currently authenticated user.

    - **Authentication**: Requires a valid JWT access token.
    - The new content will be owned by the user whose token is provided.
    """
    # We now have access to `current_user` thanks to our dependency.
    # We pass the user's ID to the CRUD function.
    return crud.create_user_content(db=db, content=content, user_id=current_user.id)


@router.get("/", response_model=List[schemas.Content])
def read_all_content(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(database.get_db)
):
    """
    Retrieves a list of all content items.
    
    - This is a public endpoint and does not require authentication.
    - Supports pagination via `skip` and `limit` query parameters.
    """
    all_content = crud.get_content(db, skip=skip, limit=limit)
    return all_content


@router.get("/{content_id}", response_model=schemas.Content)
def read_single_content(content_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieves a single content item by its ID.

    - This is a public endpoint.
    """
    db_content = crud.get_content_by_id(db, content_id=content_id)
    if db_content is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
    return db_content


@router.delete("/{content_id}", response_model=schemas.Content)
def delete_user_content(
    content_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    """
    Deletes a content item.

    - **Authentication**: Requires a valid JWT access token.
    - **Authorization**: Requires the authenticated user to be the owner of the content.
    """
    # First, get the content item from the DB
    db_content = crud.get_content_by_id(db, content_id=content_id)

    # Check if the content even exists
    if not db_content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")

    # ---- THIS IS THE AUTHORIZATION CHECK ----
    # Is the `owner_id` of the content the same as the `id` of the user making the request?
    if db_content.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )
    # ---- END OF AUTHORIZATION CHECK ----

    # If authorization passes, proceed with deletion.
    # We need a CRUD function for this. Let's assume it exists and add it next.
    crud.delete_content_by_id(db, content_id=content_id)
    
    # Return the data of the deleted item as confirmation.
    return db_content