from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


# For now the URL for database is local SQLite file.
# It will be replaced with proper PostgreSQL URL from environment variables later.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False}
)

# SessionLocal class will be used to create database sessions
SessionLocal = sessionmaker(autocommit = False , autoflush = False, bind = engine)

# Base class for our models
Base = declarative_base()