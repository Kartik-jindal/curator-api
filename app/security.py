from passlib.context import CryptContext

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
