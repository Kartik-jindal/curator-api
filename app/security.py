from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt , JWTError
from .config import settings
from fastapi import Depends , HTTPException , status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import crud , database , schemas , models

# Create a CryptContext instance for password hashing
# "bcrypt" is a secure and common choice
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hash a plain-text password safely.
    - Ensures password is a string.
    - Truncates to 72 bytes (bcrypt limit).
    """
    if not isinstance(password, str):
        password = str(password)
    # Truncate to bcrypt’s 72-byte limit
    return pwd_context.hash(password[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hashed version.
    Returns True if they match.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a new JWT access token.

    Args:
        data (dict): The data to encode into the token's payload. This should
                     contain the user's identifier (e.g., email or ID).
        expires_delta (Optional[timedelta]): A specific lifespan for this token.
                                             If None, a default is used.

    Returns:
        str: The encoded JWT as a string.
    """
    # Make a copy of the payload data to avoid modifying the original dict.
    to_encode = data.copy()

    # Determine the token's expiration time.
    if expires_delta:
        # If a custom lifespan is provided, use it.
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Otherwise, use the default lifespan from our settings file.
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    # Add the expiration time ('exp') claim to the payload.
    # This is a standard JWT claim.
    to_encode.update({"exp": expire})

    # Use the jose library to encode the payload into a JWT string.
    # It takes the payload, our secret key, and the signing algorithm.
    encoded_jwt = jwt.encode(
        claims=to_encode, 
        key=settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(database.get_db)
) -> models.User:
    """
    Decodes a JWT token, validates it, and fetches the user from the database.

    This is a dependency function that will be injected into protected endpoints.

    Args:
        token (str): The JWT from the 'Authorization: Bearer <token>' header.
                     This is injected automatically by `Depends(oauth2_scheme)`.
        db (Session): The database session, injected by `Depends(database.get_db)`.

    Returns:
        models.User: The authenticated SQLAlchemy user model.
    
    Raises:
        HTTPException 401: If credentials cannot be validated for any reason.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    
    return user

def get_current_active_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    """
    A dependency wrapper that gets the current user and can be extended
    to check if the user is active.
    """
    return current_user