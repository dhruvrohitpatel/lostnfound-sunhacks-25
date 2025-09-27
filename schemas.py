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

class SubmissionBase(BaseModel):
    text: str
    name: Optional[str] = "Anonymous"
    image_path: Optional[str] = None
    image_filename: Optional[str] = None
    image_size: Optional[int] = None

class SubmissionCreate(SubmissionBase):
    pass

class SubmissionOut(SubmissionBase):
    id: int
    timestamp: datetime
    class Config:
        orm_mode = True
