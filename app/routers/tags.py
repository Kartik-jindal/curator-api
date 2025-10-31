# app/routers/tags.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas, database, security


router = APIRouter(
    prefix="/tags",  # All routes in this file will start with /tags
    tags=["Tags"]      # Group them under "Tags" in the API docs
)


@router.post("/{tag_id}/follow", response_model=schemas.User)
def follow_a_tag(
    tag_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    """
    Allows the currently authenticated user to follow a tag.

    - **Authentication**: Requires a valid JWT access token.
    """
    # 1. Fetch the tag from the database to ensure it exists.
    tag = crud.get_tag_by_id(db, tag_id=tag_id)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
        
    # 2. Call the CRUD function to create the association.
    # The `current_user` is already a full SQLAlchemy object thanks to our dependency.
    updated_user = crud.follow_tag(db=db, user=current_user, tag=tag)

    return updated_user


@router.post("/", response_model=schemas.Tag, status_code=status.HTTP_201_CREATED)
def create_new_tag(tag: schemas.TagCreate, db: Session = Depends(database.get_db)):
    """
    Creates a new tag in the database.

    - Checks if a tag with the same name already exists to prevent duplicates.
    - This is a public endpoint.
    """
    # First, check if a tag with this name already exists.
    # We are converting the incoming tag name to lowercase to standardize tags.
    tag_name_lower = tag.name.lower()
    db_tag = crud.get_tag_by_name(db, name=tag_name_lower)
    
    # If the tag already exists, we should not create a new one.
    # Instead of an error, we could also just return the existing tag.
    # For now, raising an error is clearer.
    if db_tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Tag with this name already exists"
        )
    
    # If the tag doesn't exist, create it.
    # Note: We are creating it with the standardized lowercase name.
    tag_to_create = schemas.TagCreate(name=tag_name_lower)
    return crud.create_tag(db=db, tag=tag_to_create)

@router.delete("/{tag_id}/follow", response_model=schemas.User)
def unfollow_a_tag(
    tag_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    """
    Allows the currently authenticated user to unfollow a tag.

    - **Authentication**: Requires a valid JWT access token.
    """
    # 1. Fetch the tag from the database to ensure it exists.
    tag = crud.get_tag_by_id(db, tag_id=tag_id)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
        
    # 2. Call the CRUD function to delete the association.
    updated_user = crud.unfollow_tag(db=db, user=current_user, tag=tag)

    return updated_user