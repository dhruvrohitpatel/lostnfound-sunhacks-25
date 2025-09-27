from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Dict, Any, Optional
import models, schemas
from ai import ai_service
import logging

logger = logging.getLogger(__name__)

def create_lost_item(db: Session, item: schemas.LostItemCreate):
    """Create a lost item with AI processing"""
    db_item = models.LostItem(**item.dict())
    
    # Generate AI features
    try:
        # Generate text embedding
        combined_text = f"{item.title} {item.description} {item.location}"
        text_embedding = ai_service.get_text_embedding(combined_text)
        db_item.text_embedding = text_embedding
        
        # Process image if provided
        if item.image_path:
            image_features = ai_service.extract_image_features(item.image_path)
            db_item.image_features = image_features
            
            # Analyze image content
            image_analysis = ai_service.analyze_image_content(item.image_path)
            db_item.categories = image_analysis.get("categories", [])
            db_item.color_tags = image_analysis.get("colors", [])
        
    except Exception as e:
        logger.error(f"Error processing AI features for lost item: {e}")
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_lost_items(db: Session):
    return db.query(models.LostItem).all()

def create_found_item(db: Session, item: schemas.FoundItemCreate):
    """Create a found item with AI processing"""
    db_item = models.FoundItem(**item.dict())
    
    # Generate AI features
    try:
        # Generate text embedding
        combined_text = f"{item.title} {item.description} {item.location}"
        text_embedding = ai_service.get_text_embedding(combined_text)
        db_item.text_embedding = text_embedding
        
        # Process image if provided
        if item.image_path:
            image_features = ai_service.extract_image_features(item.image_path)
            db_item.image_features = image_features
            
            # Analyze image content
            image_analysis = ai_service.analyze_image_content(item.image_path)
            db_item.categories = image_analysis.get("categories", [])
            db_item.color_tags = image_analysis.get("colors", [])
        
    except Exception as e:
        logger.error(f"Error processing AI features for found item: {e}")
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_found_items(db: Session):
    return db.query(models.FoundItem).all()

def search_lost_items(db: Session, query: schemas.SearchQuery) -> List[Dict[str, Any]]:
    """Search lost items using AI-powered semantic search"""
    try:
        # Get query embedding
        query_embedding = ai_service.get_text_embedding(query.query)
        if query_embedding is None:
            return []
        
        # Get all lost items
        lost_items = db.query(models.LostItem).all()
        results = []
        
        for item in lost_items:
            # Calculate text similarity
            text_similarity = 0.0
            if item.text_embedding:
                text_similarity = ai_service.calculate_text_similarity(query_embedding, item.text_embedding)
            
            # Apply filters
            if query.location_filter and query.location_filter.lower() not in item.location.lower():
                continue
            
            if query.category_filter and item.categories is not None:
                if not any(cat.lower() in [c.lower() for c in item.categories] for cat in query.category_filter):
                    continue
            
            if query.color_filter and item.color_tags is not None:
                if not any(color.lower() in [c.lower() for c in item.color_tags] for color in query.color_filter):
                    continue
            
            results.append({
                'item': item,
                'text_similarity': text_similarity,
                'image_similarity': 0.0  # Will be calculated if image search is performed
            })
        
        # Rank results
        ranked_results = ai_service.rank_results(results, query.query)
        
        # Apply limit
        return ranked_results[:query.limit]
        
    except Exception as e:
        logger.error(f"Error searching lost items: {e}")
        return []

def search_found_items(db: Session, query: schemas.SearchQuery) -> List[Dict[str, Any]]:
    """Search found items using AI-powered semantic search"""
    try:
        # Get query embedding
        query_embedding = ai_service.get_text_embedding(query.query)
        if query_embedding is None:
            return []
        
        # Get all found items
        found_items = db.query(models.FoundItem).all()
        results = []
        
        for item in found_items:
            # Calculate text similarity
            text_similarity = 0.0
            if item.text_embedding:
                text_similarity = ai_service.calculate_text_similarity(query_embedding, item.text_embedding)
            
            # Apply filters
            if query.location_filter and query.location_filter.lower() not in item.location.lower():
                continue
            
            if query.category_filter and item.categories is not None:
                if not any(cat.lower() in [c.lower() for c in item.categories] for cat in query.category_filter):
                    continue
            
            if query.color_filter and item.color_tags is not None:
                if not any(color.lower() in [c.lower() for c in item.color_tags] for color in query.color_filter):
                    continue
            
            results.append({
                'item': item,
                'text_similarity': text_similarity,
                'image_similarity': 0.0  # Will be calculated if image search is performed
            })
        
        # Rank results
        ranked_results = ai_service.rank_results(results, query.query)
        
        # Apply limit
        return ranked_results[:query.limit]
        
    except Exception as e:
        logger.error(f"Error searching found items: {e}")
        return []

def search_by_image(db: Session, query_image_path: str, search_type: str = "both") -> List[Dict[str, Any]]:
    """Search items using image similarity"""
    try:
        # Extract features from query image
        query_features = ai_service.extract_image_features(query_image_path)
        if query_features is None:
            return []
        
        results = []
        
        # Search in lost items
        if search_type in ["both", "lost"]:
            lost_items = db.query(models.LostItem).all()
            for item in lost_items:
                if item.image_features:
                    image_similarity = ai_service.calculate_image_similarity(query_features, item.image_features)
                    results.append({
                        'item': item,
                        'text_similarity': 0.0,
                        'image_similarity': image_similarity
                    })
        
        # Search in found items
        if search_type in ["both", "found"]:
            found_items = db.query(models.FoundItem).all()
            for item in found_items:
                if item.image_features:
                    image_similarity = ai_service.calculate_image_similarity(query_features, item.image_features)
                    results.append({
                        'item': item,
                        'text_similarity': 0.0,
                        'image_similarity': image_similarity
                    })
        
        # Rank results
        ranked_results = ai_service.rank_results(results, query_image_path=query_image_path)
        
        return ranked_results
        
    except Exception as e:
        logger.error(f"Error searching by image: {e}")
        return []

def get_item_by_id(db: Session, item_id: int, item_type: str = "lost"):
    """Get item by ID"""
    if item_type == "lost":
        return db.query(models.LostItem).filter(models.LostItem.id == item_id).first()
    else:
        return db.query(models.FoundItem).filter(models.FoundItem.id == item_id).first()

def update_item_ai_features(db: Session, item_id: int, item_type: str = "lost"):
    """Update AI features for an existing item"""
    try:
        item = get_item_by_id(db, item_id, item_type)
        if not item:
            return None
        
        # Regenerate text embedding
        combined_text = f"{item.title} {item.description} {item.location}"
        text_embedding = ai_service.get_text_embedding(combined_text)
        item.text_embedding = text_embedding
        
        # Regenerate image features if image exists
        if item.image_path:
            image_features = ai_service.extract_image_features(item.image_path)
            item.image_features = image_features
            
            # Re-analyze image content
            image_analysis = ai_service.analyze_image_content(item.image_path)
            item.categories = image_analysis.get("categories", [])
            item.color_tags = image_analysis.get("colors", [])
        
        db.commit()
        db.refresh(item)
        return item
        
    except Exception as e:
        logger.error(f"Error updating AI features: {e}")
        return None
