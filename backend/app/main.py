
from fastapi import FastAPI
from app.api.v1 import mfa
from app.db.base_class import Base
from app.db.session import engine

# This call should create all tables defined by your SQLAlchemy models
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MFA Integration Backend")

app.include_router(mfa.router, prefix="/api/v1")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the MFA Integration Backend!"}
