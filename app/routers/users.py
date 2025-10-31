from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Import from the parent directory ('..') to get access to our other files
from .. import crud, models, schemas, database, security  # <--- MODIFIED

# Create an instance of APIRouter.
# This is like a mini-FastAPI app.
router = APIRouter(
    prefix="/users",  # All routes in this file will start with /users
    tags=["Users"]    # This will group them under "Users" in the docs
)

@router.post("/", response_model=schemas.User)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """
    Creates a new user. Checks if the email is already registered.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return crud.create_user(db=db, user=user)

# --- ADDED THIS ENTIRE ENDPOINT ---
@router.get("/me", response_model=schemas.User)
def read_current_user(current_user: models.User = Depends(security.get_current_active_user)):
    """
    Retrieves the complete profile for the currently authenticated user.

    - **Authentication**: Requires a valid JWT access token.
    - The user object is fetched by the dependency and simply returned.
    """
    return current_user

@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(user_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieves the public profile for a specific user by their ID.

    - This is a public endpoint.
    """
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user