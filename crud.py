from sqlalchemy.orm import Session
import models, schemas

def create_lost_item(db: Session, item: schemas.LostItemCreate):
    db_item = models.LostItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_lost_items(db: Session):
    return db.query(models.LostItem).all()

def create_found_item(db: Session, item: schemas.FoundItemCreate):
    db_item = models.FoundItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_found_items(db: Session):
    return db.query(models.FoundItem).all()
