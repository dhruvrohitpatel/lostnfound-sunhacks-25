from sqlalchemy import Column, Integer, String, Text, DateTime, PickleType, JSON
from sqlalchemy.sql import func
from database import Base

class LostItem(Base):
    __tablename__ = "lost_items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)        # short description e.g. "Black Backpack"
    description = Column(Text)                # details
    location = Column(String)
    image_path = Column(String, nullable=True)
    text_embedding = Column(PickleType, nullable=True)  # Store text embeddings for semantic search
    image_features = Column(PickleType, nullable=True)  # Store image feature vectors
    categories = Column(JSON, nullable=True)  # AI-extracted categories/tags
    color_tags = Column(JSON, nullable=True)  # AI-extracted color information
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class FoundItem(Base):
    __tablename__ = "found_items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    location = Column(String)
    image_path = Column(String, nullable=True)
    text_embedding = Column(PickleType, nullable=True)  # Store text embeddings for semantic search
    image_features = Column(PickleType, nullable=True)  # Store image feature vectors
    categories = Column(JSON, nullable=True)  # AI-extracted categories/tags
    color_tags = Column(JSON, nullable=True)  # AI-extracted color information
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
