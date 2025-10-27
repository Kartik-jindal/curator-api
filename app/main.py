from fastapi import FastAPI

# creating an instance of FastAPI that will be our main application named Curator API
app = FastAPI(title="Curator API")

# simple 'root' endpoint to verify that the API is running
# the tags parameter is used for grouping endpoints in the documentation

@app.get("/", tags = ["Root"])
def read_root():
    return {"message": "Welcome to Curator API!"}