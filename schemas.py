from pydantic import BaseModel
from typing import Optional, List, Dict, Any
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
    categories: Optional[List[str]] = None
    color_tags: Optional[List[str]] = None
    class Config:
        from_attributes = True

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
    categories: Optional[List[str]] = None
    color_tags: Optional[List[str]] = None
    class Config:
        from_attributes = True

# New schemas for AI-powered search
class SearchQuery(BaseModel):
    query: str
    search_type: str = "both"  # "text", "image", or "both"
    location_filter: Optional[str] = None
    category_filter: Optional[List[str]] = None
    color_filter: Optional[List[str]] = None
    limit: int = 10

class RankedResult(BaseModel):
    item: LostItemOut | FoundItemOut
    similarity_score: float
    match_type: str  # "text", "image", or "combined"
    confidence: float
    matched_features: List[str]  # What features matched (categories, colors, etc.)

class SearchResponse(BaseModel):
    results: List[RankedResult]
    total_matches: int
    search_time_ms: float
    suggestions: List[str]  # Alternative search suggestions

class ImageUpload(BaseModel):
    description: Optional[str] = None
    location: Optional[str] = None
