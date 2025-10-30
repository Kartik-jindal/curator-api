from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# The 'engine' is the main entry point to the database.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Each instance of SessionLocal will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# We will inherit from this Base class to create each of the database models.
Base = declarative_base()

def get_db():
    # A dependency function that creates and yields a new database session for each request, and ensures it's closed afterward.

    db = SessionLocal()  # Create a new session from our session factory
    try:
        yield db  # Provide the session to the endpoint
    finally:
        # This 'finally' block will run whether the request was successful
        # or an error occurred. It guarantees the session is closed.
        db.close()
