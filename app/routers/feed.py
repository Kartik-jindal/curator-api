# app/routers/feed.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas, database, security

# Create a new router for the feed endpoint
router = APIRouter(
    tags=["Feed"]  # Group this endpoint under "Feed" in the API docs
)

@router.get("/feed", response_model=List[schemas.Content])
def get_user_feed_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    """
    Retrieves the personalized content feed for the currently authenticated user.

    The feed consists of content items tagged with tags that the user follows.
    - **Authentication**: Requires a valid JWT access token.
    """
    # The endpoint logic is extremely simple because all the complexity
    # is handled by the CRUD function.
    feed = crud.get_user_feed(db=db, user=current_user, skip=skip, limit=limit)
    return feed