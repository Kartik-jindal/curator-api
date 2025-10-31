# app/routers/tags.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas, database

# Create a new router for tag-related endpoints
router = APIRouter(
    prefix="/tags",  # All routes in this file will start with /tags
    tags=["Tags"]      # Group them under "Tags" in the API docs
)

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