# Windows Setup Guide

## Prerequisites
- Windows 10 or 11
- Internet connection
- At least 4GB RAM
- 5GB free disk space

## Step 1: Install Python

### Method 1: Microsoft Store (Easiest)
1. Press `Windows + R`, type `ms-windows-store:` and press Enter
2. Search for "Python 3.11" or "Python 3.12"
3. Click "Install"

### Method 2: Official Website
1. Go to https://www.python.org/downloads/
2. Click "Download Python 3.x.x"
3. **IMPORTANT**: During installation, check "Add Python to PATH"
4. Click "Install Now"

### Method 3: Anaconda
1. Go to https://www.anaconda.com/download
2. Download Anaconda for Windows
3. Install with default settings
4. Use "Anaconda Prompt" instead of regular PowerShell

## Step 2: Verify Installation

Open PowerShell or Command Prompt and run:
```cmd
python --version
```

You should see something like: `Python 3.11.x`

## Step 3: Install the Lost & Found System

### Option A: Automatic Setup (Recommended)
```cmd
setup_windows.bat
```

### Option B: Manual Setup
```cmd
# Navigate to the project folder
cd "C:\Users\josep\OneDrive\Desktop\Joseph\School\hackathon2025\lostnfound-sunhacks-25"

# Install packages
python -m pip install -r requirements.txt

# Test the system
python test_system.py

# Start the server
python start_server.py
```

## Step 4: Access the System

Once the server starts:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Troubleshooting

### "python is not recognized"
- Python is not installed or not in PATH
- Reinstall Python and check "Add Python to PATH"
- Or use full path: `C:\Users\[username]\AppData\Local\Programs\Python\Python311\python.exe`

### "pip is not recognized"
- Use `python -m pip` instead of just `pip`
- Example: `python -m pip install -r requirements.txt`

### Out of Memory Errors
- Close other applications
- The AI models need ~4GB RAM
- Consider using fewer workers: `uvicorn main:app --workers 1`

### Port Already in Use
- Change port: `uvicorn main:app --port 8001`
- Or kill existing process:
  ```cmd
  netstat -ano | findstr :8000
  taskkill /PID [PID_NUMBER] /F
  ```

### Model Download Issues
- Check internet connection
- Models are cached, so retry if download fails
- Manual cache location: `%USERPROFILE%\.cache\`

## Performance Tips

### For Better Performance:
1. **Install CUDA** (if you have NVIDIA GPU):
   ```cmd
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

2. **Use SSD**: Install on SSD for faster model loading

3. **Close Background Apps**: Free up RAM for AI models

### For Development:
```cmd
# Auto-reload on changes
uvicorn main:app --reload

# Different port
uvicorn main:app --port 8001

# More workers (production)
uvicorn main:app --workers 4
```

## Quick Start Commands

```cmd
# 1. Install Python (if not done)
# Download from python.org

# 2. Run setup
setup_windows.bat

# 3. Start server
python start_server.py

# 4. Test system
python example_usage.py
```

## Next Steps

1. **Add Sample Data**: The example script will create test items
2. **Try Natural Language Search**: "black backpack lost near library"
3. **Upload Images**: Test image recognition functionality
4. **Explore API**: Check interactive docs at http://localhost:8000/docs

## Support

If you encounter issues:
1. Run `python test_system.py` to diagnose problems
2. Check Python installation: `python --version`
3. Verify packages: `python -m pip list`
4. Check system resources (RAM, disk space)

## File Structure

```
lostnfound-sunhacks-25/
├── main.py              # Main API server
├── ai.py                # AI models and processing
├── models.py            # Database models
├── schemas.py           # API schemas
├── crud.py              # Database operations
├── requirements.txt     # Python dependencies
├── setup_windows.bat    # Windows setup script
├── test_system.py       # System tests
├── example_usage.py     # Usage examples
└── README.md            # Full documentation
```


