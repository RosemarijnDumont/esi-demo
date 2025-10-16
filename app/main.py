
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.services.csv_parser import parse_csv_data
from app.services.user_service import create_user
import csv
from io import StringIO

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/users/bulk-import")
async def bulk_import_users(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")

    content = await file.read()
    csv_content = content.decode("utf-8")

    if not csv_content.strip():
        raise HTTPException(status_code=400, detail="Uploaded CSV file is empty.")

    imported_count = 0
    errors = []

    try:
        users_data = parse_csv_data(csv_content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"CSV parsing error: {e}")

    for user_data in users_data:
        try:
            create_user(db, user_data)
            imported_count += 1
        except Exception as e:
            errors.append(f"Error importing user {user_data.get('email', '')}: {e}")

    if errors:
        return {"message": "Bulk import completed with errors", "imported_count": imported_count, "errors": errors}
    return {"message": "Bulk import completed", "imported_count": imported_count, "errors": []}

@app.get("/upload") # Placeholder for a simple frontend upload page
async def upload_page():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bulk User Import</title>
    </head>
    <body>
        <h1>Upload CSV for Bulk User Import</h1>
        <form action="/api/users/bulk-import" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept=".csv">
            <button type="submit">Upload</button>
        </form>
        <div id="status" data-testid="import-status"></div>
        <div id="imported-count" data-testid="imported-count"></div>
        <ul id="errors" data-testid="error-list"></ul>
        <div id="error-message" data-testid="error-message" style="color: red;"></div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

from fastapi.responses import HTMLResponse
