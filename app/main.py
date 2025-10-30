from fastapi import FastAPI

# Import the engine and Base from your database.py file
from .database import engine
# Import the models 
from . import models
# Import the router for user-related endpoints
from .routers import users

# When our application starts, it tells SQLAlchemy
# to look at all the classes that inherit from Base (our models) and create
# the corresponding tables in the database.
# If the tables already exist, this command does nothing.
models.Base.metadata.create_all(bind=engine)

# Create the main FastAPI application instance.
app = FastAPI(title="Curator API")

# This line connects the router from app/routers/users.py to our main app.
# Now, any endpoint defined in that router will be part of the main application.
app.include_router(users.router)

# The root endpoint, for a simple health check.
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Curator API!"}