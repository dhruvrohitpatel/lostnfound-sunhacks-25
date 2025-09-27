#!/usr/bin/env python3
"""
Test script for the AI-Powered Lost & Found System
"""

import sys
import importlib
import traceback

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    modules_to_test = [
        ("fastapi", "FastAPI"),
        ("sqlalchemy", "SQLAlchemy"),
        ("sentence_transformers", "SentenceTransformers"),
        ("transformers", "CLIP"),
        ("torch", "PyTorch"),
        ("sklearn", "Scikit-learn"),
        ("PIL", "Pillow"),
        ("numpy", "NumPy")
    ]
    
    failed_imports = []
    
    for module_name, display_name in modules_to_test:
        try:
            importlib.import_module(module_name)
            print(f"✓ {display_name}")
        except ImportError as e:
            print(f"✗ {display_name}: {e}")
            failed_imports.append(module_name)
    
    return len(failed_imports) == 0

def test_ai_service():
    """Test AI service initialization"""
    print("\nTesting AI service...")
    
    try:
        from ai import ai_service
        print("✓ AI service imported successfully")
        
        # Test text embedding
        test_text = "This is a test"
        embedding = ai_service.get_text_embedding(test_text)
        if embedding is not None:
            print(f"✓ Text embedding generated (shape: {embedding.shape})")
        else:
            print("✗ Text embedding failed")
            return False
        
        # Test similarity calculation
        similarity = ai_service.calculate_text_similarity(embedding, embedding)
        if similarity > 0.99:  # Should be very similar to itself
            print(f"✓ Similarity calculation working (similarity: {similarity:.3f})")
        else:
            print(f"✗ Similarity calculation failed (similarity: {similarity:.3f})")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ AI service test failed: {e}")
        traceback.print_exc()
        return False

def test_database():
    """Test database initialization"""
    print("\nTesting database...")
    
    try:
        from database import engine, SessionLocal
        from models import Base, LostItem, FoundItem
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created")
        
        # Test database session
        db = SessionLocal()
        try:
            # Test basic query
            lost_count = db.query(LostItem).count()
            found_count = db.query(FoundItem).count()
            print(f"✓ Database connection working (Lost: {lost_count}, Found: {found_count})")
            return True
        finally:
            db.close()
        
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        traceback.print_exc()
        return False

def test_models():
    """Test model definitions"""
    print("\nTesting models...")
    
    try:
        from models import LostItem, FoundItem
        
        # Check if models have required attributes
        lost_attrs = ['title', 'description', 'location', 'text_embedding', 'image_features', 'categories', 'color_tags']
        found_attrs = ['title', 'description', 'location', 'text_embedding', 'image_features', 'categories', 'color_tags']
        
        lost_model = LostItem
        found_model = FoundItem
        
        for attr in lost_attrs:
            if hasattr(lost_model, attr):
                print(f"✓ LostItem has {attr}")
            else:
                print(f"✗ LostItem missing {attr}")
                return False
        
        for attr in found_attrs:
            if hasattr(found_model, attr):
                print(f"✓ FoundItem has {attr}")
            else:
                print(f"✗ FoundItem missing {attr}")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Models test failed: {e}")
        traceback.print_exc()
        return False

def test_schemas():
    """Test schema definitions"""
    print("\nTesting schemas...")
    
    try:
        from schemas import SearchQuery, RankedResult, SearchResponse
        
        # Test SearchQuery
        query = SearchQuery(query="test", limit=5)
        print(f"✓ SearchQuery created: {query.query}")
        
        # Test RankedResult (without actual item)
        print("✓ RankedResult schema available")
        
        # Test SearchResponse
        print("✓ SearchResponse schema available")
        
        return True
        
    except Exception as e:
        print(f"✗ Schemas test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("AI-Powered Lost & Found System - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Model Test", test_models),
        ("Schema Test", test_schemas),
        ("Database Test", test_database),
        ("AI Service Test", test_ai_service),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 20)
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} PASSED")
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\nTo start the server, run:")
        print("python start_server.py")
        print("\nOr directly with uvicorn:")
        print("uvicorn main:app --reload")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


