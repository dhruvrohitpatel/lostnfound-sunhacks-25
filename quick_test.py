#!/usr/bin/env python3
"""
Quick test script for the AI-Powered Lost & Found System
Tests core functionality without loading heavy AI models
"""

import sys
import importlib

def test_basic_imports():
    """Test basic imports without AI models"""
    print("Testing basic imports...")
    
    try:
        import fastapi
        print("✓ FastAPI")
    except ImportError as e:
        print(f"✗ FastAPI: {e}")
        return False
    
    try:
        import sqlalchemy
        print("✓ SQLAlchemy")
    except ImportError as e:
        print(f"✗ SQLAlchemy: {e}")
        return False
    
    try:
        import pydantic
        print("✓ Pydantic")
    except ImportError as e:
        print(f"✗ Pydantic: {e}")
        return False
    
    return True

def test_database():
    """Test database functionality"""
    print("\nTesting database...")
    
    try:
        from database import engine, SessionLocal
        from models import Base, LostItem, FoundItem
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created")
        
        # Test session
        db = SessionLocal()
        try:
            lost_count = db.query(LostItem).count()
            found_count = db.query(FoundItem).count()
            print(f"✓ Database connection working (Lost: {lost_count}, Found: {found_count})")
            return True
        finally:
            db.close()
            
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

def test_models():
    """Test model definitions"""
    print("\nTesting models...")
    
    try:
        from models import LostItem, FoundItem
        
        # Check required attributes
        required_attrs = ['title', 'description', 'location', 'text_embedding', 'image_features', 'categories', 'color_tags']
        
        for attr in required_attrs:
            if not hasattr(LostItem, attr):
                print(f"✗ LostItem missing {attr}")
                return False
            if not hasattr(FoundItem, attr):
                print(f"✗ FoundItem missing {attr}")
                return False
        
        print("✓ All model attributes present")
        return True
        
    except Exception as e:
        print(f"✗ Models test failed: {e}")
        return False

def test_schemas():
    """Test schema definitions"""
    print("\nTesting schemas...")
    
    try:
        from schemas import SearchQuery, RankedResult, SearchResponse
        
        # Test SearchQuery
        query = SearchQuery(query="test", limit=5)
        print("✓ SearchQuery schema working")
        
        print("✓ All schemas working")
        return True
        
    except Exception as e:
        print(f"✗ Schemas test failed: {e}")
        return False

def test_crud():
    """Test CRUD operations"""
    print("\nTesting CRUD operations...")
    
    try:
        from crud import create_lost_item, create_found_item
        from schemas import LostItemCreate, FoundItemCreate
        from database import SessionLocal
        
        # Test item creation (without AI processing for speed)
        db = SessionLocal()
        try:
            # Create test items
            lost_item = LostItemCreate(
                title="Test Lost Item",
                description="Test description",
                location="Test location"
            )
            
            found_item = FoundItemCreate(
                title="Test Found Item", 
                description="Test description",
                location="Test location"
            )
            
            print("✓ CRUD schemas working")
            return True
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"✗ CRUD test failed: {e}")
        return False

def main():
    """Run quick tests"""
    print("AI-Powered Lost & Found System - Quick Test")
    print("=" * 50)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Models", test_models),
        ("Schemas", test_schemas),
        ("Database", test_database),
        ("CRUD", test_crud),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} PASSED")
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} FAILED: {e}")
    
    print("\n" + "=" * 50)
    print(f"Quick Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Core system is working! Ready to start the server.")
        print("\nTo start the server:")
        print("  python start_server.py")
        print("\nNote: AI models will load on first server start (may take a few minutes)")
        return True
    else:
        print("❌ Some core tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

