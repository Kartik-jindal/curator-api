
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import crud, schemas, security, database

# Create a new router for authentication-related endpoints.
router = APIRouter(
    tags=["Authentication"]  # Group these endpoints under "Authentication" in the docs.
)

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(database.get_db)
):
    """
    Provides a login endpoint to issue JWT access tokens.

    This endpoint follows the OAuth2 standard for token issuance using a
    "password" grant type. The client sends username and password in a
    form-data body.

    Args:
        form_data (OAuth2PasswordRequestForm): FastAPI's dependency to handle
                                               form data with "username" and "password" fields.
        db (Session): The SQLAlchemy database session dependency.

    Raises:
        HTTPException: 401 Unauthorized if authentication fails.

    Returns:
        schemas.Token: A Pydantic model containing the access token and token type.
    """
    # Step 1: Authenticate the user.
    # We use our crud function to find the user by their email (which is the "username" here).
    user = crud.get_user_by_email(db, email=form_data.username)

    # Check if a user was found and if the provided password is correct.
    # 'verify_password' compares the plain-text password from the form with the
    # hashed password stored in our database.
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        # If authentication fails, raise an HTTP 401 Unauthorized error.
        # It's important to include the "WWW-Authenticate" header for the OAuth2 spec.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Step 2: Create the access token.
    # The token's payload ('sub' for subject) should identify the user.
    # We use the user's email as the subject.
    access_token = security.create_access_token(
        data={"sub": user.email}
    )

    # Step 3: Return the token.
    # The response is structured according to our `schemas.Token` Pydantic model.
    return {"access_token": access_token, "token_type": "bearer"}