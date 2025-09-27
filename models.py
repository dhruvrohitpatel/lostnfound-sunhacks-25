from sqlalchemy import Column, Integer, String, Text, DateTime, LargeBinary
from sqlalchemy.sql import func
from database import Base

class LostItem(Base):
    __tablename__ = "lost_items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)        # short description e.g. "Black Backpack"
    description = Column(Text)                # details
    location = Column(String)
    image_path = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class FoundItem(Base):
    __tablename__ = "found_items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    location = Column(String)
    image_path = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    name = Column(String, default="Anonymous")
    image_path = Column(String, nullable=True)
    image_filename = Column(String, nullable=True)
    image_size = Column(Integer, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
