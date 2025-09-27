from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LostItemBase(BaseModel):
    title: str
    description: str
    location: str
    image_path: Optional[str] = None

class LostItemCreate(LostItemBase):
    pass

class LostItemOut(LostItemBase):
    id: int
    timestamp: datetime
    class Config:
        orm_mode = True

class FoundItemBase(BaseModel):
    title: str
    description: str
    location: str
    image_path: Optional[str] = None

class FoundItemCreate(FoundItemBase):
    pass

class FoundItemOut(FoundItemBase):
    id: int
    timestamp: datetime
    class Config:
        orm_mode = True
