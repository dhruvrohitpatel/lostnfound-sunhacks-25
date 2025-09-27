from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
import time
import os
import aiofiles
import models, schemas, crud
from database import SessionLocal, engine
from ai import ai_service

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ASU Lost & Found AI", description="AI-powered lost and found system with natural language search and image recognition")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "Welcome to ASU Lost & Found AI API!", "features": ["natural language search", "image recognition", "smart ranking", "AI suggestions"]}

# Basic CRUD endpoints
@app.post("/lost/", response_model=schemas.LostItemOut)
def create_lost(item: schemas.LostItemCreate, db: Session = Depends(get_db)):
    return crud.create_lost_item(db, item)

@app.get("/lost/", response_model=List[schemas.LostItemOut])
def list_lost(db: Session = Depends(get_db)):
    return crud.get_lost_items(db)

@app.post("/found/", response_model=schemas.FoundItemOut)
def create_found(item: schemas.FoundItemCreate, db: Session = Depends(get_db)):
    return crud.create_found_item(db, item)

@app.get("/found/", response_model=List[schemas.FoundItemOut])
def list_found(db: Session = Depends(get_db)):
    return crud.get_found_items(db)

# AI-powered search endpoints
@app.post("/search/lost", response_model=schemas.SearchResponse)
def search_lost_items(query: schemas.SearchQuery, db: Session = Depends(get_db)):
    """Search lost items using natural language with AI"""
    start_time = time.time()
    
    try:
        results = crud.search_lost_items(db, query)
        
        # Convert to RankedResult objects
        ranked_results = []
        for result in results:
            ranked_results.append(schemas.RankedResult(
                item=result['item'],
                similarity_score=result['similarity_score'],
                match_type=result['match_type'],
                confidence=result['confidence'],
                matched_features=result['matched_features']
            ))
        
        # Generate suggestions
        suggestions = ai_service.generate_search_suggestions(query.query, len(ranked_results))
        
        search_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        return schemas.SearchResponse(
            results=ranked_results,
            total_matches=len(ranked_results),
            search_time_ms=search_time,
            suggestions=suggestions
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/search/found", response_model=schemas.SearchResponse)
def search_found_items(query: schemas.SearchQuery, db: Session = Depends(get_db)):
    """Search found items using natural language with AI"""
    start_time = time.time()
    
    try:
        results = crud.search_found_items(db, query)
        
        # Convert to RankedResult objects
        ranked_results = []
        for result in results:
            ranked_results.append(schemas.RankedResult(
                item=result['item'],
                similarity_score=result['similarity_score'],
                match_type=result['match_type'],
                confidence=result['confidence'],
                matched_features=result['matched_features']
            ))
        
        # Generate suggestions
        suggestions = ai_service.generate_search_suggestions(query.query, len(ranked_results))
        
        search_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        return schemas.SearchResponse(
            results=ranked_results,
            total_matches=len(ranked_results),
            search_time_ms=search_time,
            suggestions=suggestions
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/search/image", response_model=schemas.SearchResponse)
async def search_by_image(
    file: UploadFile = File(...),
    search_type: str = "both",
    db: Session = Depends(get_db)
):
    """Search items using image recognition"""
    start_time = time.time()
    
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Search using image
        results = crud.search_by_image(db, file_path, search_type)
        
        # Convert to RankedResult objects
        ranked_results = []
        for result in results:
            ranked_results.append(schemas.RankedResult(
                item=result['item'],
                similarity_score=result['similarity_score'],
                match_type=result['match_type'],
                confidence=result['confidence'],
                matched_features=result['matched_features']
            ))
        
        # Generate suggestions
        suggestions = ai_service.generate_search_suggestions("image search", len(ranked_results))
        
        search_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Clean up uploaded file
        try:
            os.remove(file_path)
        except:
            pass
        
        return schemas.SearchResponse(
            results=ranked_results,
            total_matches=len(ranked_results),
            search_time_ms=search_time,
            suggestions=suggestions
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image search failed: {str(e)}")

@app.post("/upload/lost", response_model=schemas.LostItemOut)
async def upload_lost_item_with_image(
    title: str,
    description: str,
    location: str,
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    """Upload a lost item with optional image"""
    try:
        image_path = None
        
        if file and file.content_type.startswith('image/'):
            # Save image
            image_path = os.path.join(UPLOAD_DIR, f"lost_{int(time.time())}_{file.filename}")
            async with aiofiles.open(image_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
        
        # Create item
        item_data = schemas.LostItemCreate(
            title=title,
            description=description,
            location=location,
            image_path=image_path
        )
        
        return crud.create_lost_item(db, item_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/upload/found", response_model=schemas.FoundItemOut)
async def upload_found_item_with_image(
    title: str,
    description: str,
    location: str,
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    """Upload a found item with optional image"""
    try:
        image_path = None
        
        if file and file.content_type.startswith('image/'):
            # Save image
            image_path = os.path.join(UPLOAD_DIR, f"found_{int(time.time())}_{file.filename}")
            async with aiofiles.open(image_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
        
        # Create item
        item_data = schemas.FoundItemCreate(
            title=title,
            description=description,
            location=location,
            image_path=image_path
        )
        
        return crud.create_found_item(db, item_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.put("/items/{item_id}/ai-update")
def update_item_ai_features(
    item_id: int,
    item_type: str,
    db: Session = Depends(get_db)
):
    """Update AI features for an existing item"""
    try:
        updated_item = crud.update_item_ai_features(db, item_id, item_type)
        if not updated_item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        return {"message": "AI features updated successfully", "item": updated_item}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ai_models": {
            "text_model": ai_service.text_model is not None,
            "clip_model": ai_service.clip_model is not None,
            "resnet_model": ai_service.resnet is not None
        }
    }
