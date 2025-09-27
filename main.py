from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ASU Lost & Found")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Welcome to ASU Lost & Found API!"}

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
