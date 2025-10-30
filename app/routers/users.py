from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Import from the parent directory ('..') to get access to our other files
from .. import crud, models, schemas, database

# Create an instance of APIRouter.
# This is like a mini-FastAPI app.
router = APIRouter(
    prefix="/users",  # All routes in this file will start with /users
    tags=["Users"]    # This will group them under "Users" in the docs
)

@router.post("/" , response_model = schemas.User)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):

    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code = 400, detail= "Email already registered")
    
    return crud.create_user(db= db , user = user)