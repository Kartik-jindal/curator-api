# app/main.py

from fastapi import FastAPI

# We can also clean up these unused imports now
# from .database import engine  <-- No longer needed here
# from . import models          <-- No longer needed here

# Import all the routers for your different application sections
from .routers import users, auth, content , tags

# Create the main FastAPI application instance.
app = FastAPI(title="Curator API")

# Include the routers from other files. This connects all the endpoints
# from the users, auth, and content files to our main application.
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(content.router)
app.include_router(tags.router)

# The root endpoint, for a simple health check to see if the API is running.
@app.get("/", tags=["Root"])
def read_root():
    """
    A simple root endpoint to confirm the API is running.
    """
    return {"message": "Welcome to the Curator API!"}