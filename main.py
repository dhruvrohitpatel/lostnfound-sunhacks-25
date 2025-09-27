from fastapi import FastAPI, Depends, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
import os
import uuid
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ASU Lost & Found")

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def root():
    """Serve the main web interface"""
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.post("/lost/", response_model=schemas.LostItemOut)
def create_lost(item: schemas.LostItemCreate, db: Session = Depends(get_db)):
    return crud.create_lost_item(db, item)

@app.get("/lost/", response_model=list[schemas.LostItemOut])
def list_lost(db: Session = Depends(get_db)):
    return crud.get_lost_items(db)

@app.post("/found/", response_model=schemas.FoundItemOut)
def create_found(item: schemas.FoundItemCreate, db: Session = Depends(get_db)):
    return crud.create_found_item(db, item)

@app.get("/found/", response_model=list[schemas.FoundItemOut])
def list_found(db: Session = Depends(get_db)):
    return crud.get_found_items(db)

# New API endpoints for image and text collection
@app.post("/api/submit")
async def submit_content(
    text: str = Form(""),
    name: str = Form(""),
    image: UploadFile = File(None),
    timestamp: str = Form("")
):
    """Submit user content with image and text"""
    try:
        # Validate input
        if not text.strip() and not image:
            raise HTTPException(status_code=400, detail="Either text or image must be provided")
        
        # Prepare response data
        response_data = {
            "id": str(uuid.uuid4()),
            "text": text.strip(),
            "name": name.strip() if name else "Anonymous",
            "timestamp": timestamp or datetime.now().isoformat(),
            "image_url": None
        }
        
        # Handle image upload
        if image and image.filename:
            # Validate file type
            if not image.content_type.startswith('image/'):
                raise HTTPException(status_code=400, detail="File must be an image")
            
            # Generate unique filename
            file_extension = os.path.splitext(image.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join("uploads", unique_filename)
            
            # Save file
            with open(file_path, "wb") as buffer:
                content = await image.read()
                buffer.write(content)
            
            response_data["image_url"] = f"/uploads/{unique_filename}"
            response_data["image_filename"] = image.filename
            response_data["image_size"] = len(content)
        
        # Here you could save to database if needed
        # For now, we'll just return the data
        
        return {
            "success": True,
            "message": "Content submitted successfully",
            "data": response_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing submission: {str(e)}")

@app.get("/api/submissions")
def get_submissions():
    """Get all submissions (for admin purposes)"""
    # This would typically fetch from database
    # For now, return empty list
    return {"submissions": []}

# Serve uploaded images
@app.get("/uploads/{filename}")
async def get_uploaded_file(filename: str):
    """Serve uploaded images"""
    file_path = os.path.join("uploads", filename)
    if os.path.exists(file_path):
        from fastapi.responses import FileResponse
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")
