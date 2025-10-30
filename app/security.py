from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from .config import settings

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