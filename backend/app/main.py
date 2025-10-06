from fastapi import FastAPI
from api.endpoints import users # Import the new users endpoint

app = FastAPI()

app.include_router(users.router, prefix="/api/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Hello World"}
