#!/usr/bin/env python3
"""
Startup script for the AI-Powered Lost & Found System
"""

import uvicorn
import os
import sys
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import torch
        import sentence_transformers
        import transformers
        import sklearn
        import fastapi
        import sqlalchemy
        print("✓ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["uploads", "models"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Directory '{directory}' ready")

def main():
    """Main startup function"""
    print("AI-Powered Lost & Found System")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Check if database exists, if not it will be created
    if not os.path.exists("lostfound.db"):
        print("✓ Database will be created on first run")
    
    print("\nStarting server...")
    print("API will be available at: http://localhost:8000")
    print("Interactive docs at: http://localhost:8000/docs")
    print("Health check at: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 40)
    
    try:
        # Start the server
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


