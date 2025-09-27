#!/usr/bin/env python3
"""
Example usage of the AI-powered Lost & Found system
"""

import requests
import json
from typing import Dict, Any

# Base URL for the API
BASE_URL = "http://localhost:8000"

def create_sample_data():
    """Create some sample lost and found items for testing"""
    
    # Sample lost items
    lost_items = [
        {
            "title": "Black Backpack",
            "description": "Nike black backpack with laptop compartment, lost near the library",
            "location": "ASU Library",
            "image_path": None
        },
        {
            "title": "iPhone 13",
            "description": "Silver iPhone 13 with cracked screen, lost in the engineering building",
            "location": "Engineering Building",
            "image_path": None
        },
        {
            "title": "Red Water Bottle",
            "description": "Stainless steel red water bottle with ASU logo",
            "location": "Student Union",
            "image_path": None
        }
    ]
    
    # Sample found items
    found_items = [
        {
            "title": "Blue Backpack",
            "description": "Blue Jansport backpack found in the cafeteria",
            "location": "Cafeteria",
            "image_path": None
        },
        {
            "title": "White AirPods",
            "description": "White AirPods case found in the gym",
            "location": "Gym",
            "image_path": None
        },
        {
            "title": "Green Jacket",
            "description": "Green hoodie jacket found on campus bus",
            "location": "Campus Bus",
            "image_path": None
        }
    ]
    
    print("Creating sample lost items...")
    for item in lost_items:
        response = requests.post(f"{BASE_URL}/lost/", json=item)
        if response.status_code == 200:
            print(f"✓ Created lost item: {item['title']}")
        else:
            print(f"✗ Failed to create lost item: {item['title']}")
    
    print("\nCreating sample found items...")
    for item in found_items:
        response = requests.post(f"{BASE_URL}/found/", json=item)
        if response.status_code == 200:
            print(f"✓ Created found item: {item['title']}")
        else:
            print(f"✗ Failed to create found item: {item['title']}")

def test_natural_language_search():
    """Test natural language search functionality"""
    print("\n" + "="*50)
    print("TESTING NATURAL LANGUAGE SEARCH")
    print("="*50)
    
    search_queries = [
        "black backpack",
        "phone with cracked screen",
        "red water bottle",
        "blue bag",
        "white earbuds",
        "green clothing"
    ]
    
    for query in search_queries:
        print(f"\nSearching for: '{query}'")
        
        # Search lost items
        lost_search = {
            "query": query,
            "search_type": "text",
            "limit": 5
        }
        
        response = requests.post(f"{BASE_URL}/search/lost", json=lost_search)
        if response.status_code == 200:
            results = response.json()
            print(f"Lost items found: {results['total_matches']}")
            for result in results['results'][:3]:  # Show top 3
                item = result['item']
                print(f"  - {item['title']} (similarity: {result['similarity_score']:.3f}, confidence: {result['confidence']:.3f})")
                print(f"    Location: {item['location']}")
                if result['matched_features']:
                    print(f"    Matched features: {', '.join(result['matched_features'])}")
        
        # Search found items
        found_search = {
            "query": query,
            "search_type": "text",
            "limit": 5
        }
        
        response = requests.post(f"{BASE_URL}/search/found", json=found_search)
        if response.status_code == 200:
            results = response.json()
            print(f"Found items: {results['total_matches']}")
            for result in results['results'][:3]:  # Show top 3
                item = result['item']
                print(f"  - {item['title']} (similarity: {result['similarity_score']:.3f}, confidence: {result['confidence']:.3f})")
                print(f"    Location: {item['location']}")
                if result['matched_features']:
                    print(f"    Matched features: {', '.join(result['matched_features'])}")
        
        if response.status_code == 200 and results['suggestions']:
            print(f"Suggestions: {', '.join(results['suggestions'])}")

def test_advanced_search():
    """Test advanced search with filters"""
    print("\n" + "="*50)
    print("TESTING ADVANCED SEARCH WITH FILTERS")
    print("="*50)
    
    # Search with location filter
    location_search = {
        "query": "backpack",
        "search_type": "text",
        "location_filter": "library",
        "limit": 10
    }
    
    print(f"\nSearching for 'backpack' in library:")
    response = requests.post(f"{BASE_URL}/search/lost", json=location_search)
    if response.status_code == 200:
        results = response.json()
        print(f"Results found: {results['total_matches']}")
        for result in results['results']:
            item = result['item']
            print(f"  - {item['title']} at {item['location']} (similarity: {result['similarity_score']:.3f})")

def test_health_check():
    """Test the health check endpoint"""
    print("\n" + "="*50)
    print("HEALTH CHECK")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        health = response.json()
        print(f"Status: {health['status']}")
        print("AI Models:")
        for model, status in health['ai_models'].items():
            status_icon = "✓" if status else "✗"
            print(f"  {status_icon} {model}: {'Loaded' if status else 'Not loaded'}")
    else:
        print("✗ Health check failed")

def main():
    """Main function to run all tests"""
    print("AI-Powered Lost & Found System - Example Usage")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✓ Server is running")
        else:
            print("✗ Server is not responding properly")
            return
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server. Make sure it's running on http://localhost:8000")
        print("Run: uvicorn main:app --reload")
        return
    
    # Run tests
    test_health_check()
    create_sample_data()
    test_natural_language_search()
    test_advanced_search()
    
    print("\n" + "="*60)
    print("Example completed! Try these additional features:")
    print("- Upload images with /upload/lost and /upload/found endpoints")
    print("- Search by image with /search/image endpoint")
    print("- Use the interactive API docs at http://localhost:8000/docs")

if __name__ == "__main__":
    main()


