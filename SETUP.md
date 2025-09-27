# Quick Setup Guide

## Prerequisites
- Python 3.8 or higher
- pip package manager
- At least 4GB RAM (for AI models)
- Internet connection (for downloading models)

## Installation Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Test the Installation
```bash
python test_system.py
```

### 3. Start the Server
```bash
python start_server.py
```

### 4. Access the System
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## First Run Notes

### Model Download
On first startup, the system will download AI models:
- Sentence Transformers model (~80MB)
- CLIP model (~500MB)
- ResNet model (~100MB)

This may take a few minutes depending on your internet connection.

### Database Creation
The SQLite database (`lostfound.db`) will be created automatically on first run.

## Quick Test

Run the example script to test the system:
```bash
python example_usage.py
```

## Troubleshooting

### Common Issues

1. **Out of Memory**
   - Close other applications
   - The system needs ~4GB RAM for AI models
   - Consider using CPU-only mode (models will be slower)

2. **Model Download Fails**
   - Check internet connection
   - Try running again (downloads are cached)
   - Manual download: Models are stored in `~/.cache/`

3. **Port Already in Use**
   - Change port in `start_server.py`
   - Or kill existing process: `lsof -ti:8000 | xargs kill`

### Performance Tips

- **GPU Support**: Install PyTorch with CUDA for faster processing
- **Memory**: Close other applications during model loading
- **Storage**: Ensure at least 2GB free space for models

## Development Mode

For development with auto-reload:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Production Deployment

For production deployment:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Next Steps

1. **Add Sample Data**: Use `example_usage.py` to create test items
2. **Test Search**: Try natural language searches like "black backpack"
3. **Upload Images**: Test image recognition with photos
4. **Explore API**: Check out the interactive docs at `/docs`

## Support

If you encounter issues:
1. Run `python test_system.py` to diagnose problems
2. Check the logs in the terminal
3. Verify all dependencies are installed
4. Ensure sufficient system resources


