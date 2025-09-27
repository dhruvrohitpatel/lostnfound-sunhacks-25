# AI-Powered Lost & Found System

A comprehensive lost and found system with advanced AI capabilities including natural language search, image recognition, and smart ranking for matching lost and found items.

## Features

### 🤖 AI-Powered Search
- **Natural Language Search**: Search using conversational queries like "black backpack lost near library"
- **Image Recognition**: Upload photos to find visually similar items using computer vision
- **Smart Ranking**: Combines text and image similarity with confidence scoring
- **AI Suggestions**: Intelligent search suggestions when no results are found

### 🔍 Advanced Search Capabilities
- **Semantic Search**: Uses sentence transformers for understanding meaning, not just keywords
- **Multi-modal Matching**: Combines text descriptions and image features
- **Filtering**: Search by location, category, color, and other attributes
- **Real-time Processing**: Fast search with sub-second response times

### 📱 Modern API
- **RESTful API**: Clean, well-documented endpoints
- **File Upload Support**: Upload images directly through the API
- **Interactive Documentation**: Auto-generated API docs with Swagger UI
- **Health Monitoring**: Built-in health checks for AI model status

## Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **AI/ML Models**:
  - Sentence Transformers for text embeddings
  - CLIP for image-text understanding
  - ResNet for image feature extraction
  - Scikit-learn for similarity calculations
- **Image Processing**: PIL, Torchvision
- **Async Support**: aiofiles for file operations

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd lostnfound-sunhacks-25
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

4. **Access the API**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

## API Endpoints

### Basic CRUD Operations
- `POST /lost/` - Create a lost item
- `GET /lost/` - List all lost items
- `POST /found/` - Create a found item
- `GET /found/` - List all found items

### AI-Powered Search
- `POST /search/lost` - Search lost items with natural language
- `POST /search/found` - Search found items with natural language
- `POST /search/image` - Search items using image recognition

### File Upload
- `POST /upload/lost` - Upload lost item with image
- `POST /upload/found` - Upload found item with image

### Utilities
- `PUT /items/{item_id}/ai-update` - Update AI features for existing item
- `GET /health` - Check system and AI model status

## Usage Examples

### 1. Create Items
```python
import requests

# Create a lost item
lost_item = {
    "title": "Black Backpack",
    "description": "Nike backpack with laptop compartment",
    "location": "ASU Library",
    "image_path": None
}
response = requests.post("http://localhost:8000/lost/", json=lost_item)
```

### 2. Natural Language Search
```python
# Search for lost items
search_query = {
    "query": "black backpack lost near library",
    "search_type": "text",
    "limit": 10
}
response = requests.post("http://localhost:8000/search/lost", json=search_query)
results = response.json()

for result in results['results']:
    print(f"Item: {result['item']['title']}")
    print(f"Similarity: {result['similarity_score']:.3f}")
    print(f"Confidence: {result['confidence']:.3f}")
```

### 3. Image Search
```python
# Search using image
with open("lost_item_photo.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post("http://localhost:8000/search/image", files=files)
    results = response.json()
```

### 4. Advanced Search with Filters
```python
# Search with filters
advanced_search = {
    "query": "backpack",
    "search_type": "text",
    "location_filter": "library",
    "category_filter": ["backpack", "bag"],
    "color_filter": ["black", "blue"],
    "limit": 5
}
response = requests.post("http://localhost:8000/search/lost", json=advanced_search)
```

## AI Model Details

### Text Processing
- **Model**: `all-MiniLM-L6-v2` (Sentence Transformers)
- **Purpose**: Generate semantic embeddings for natural language search
- **Features**: 384-dimensional vectors capturing semantic meaning

### Image Processing
- **CLIP Model**: `openai/clip-vit-base-patch32`
- **Purpose**: Image-text understanding and category classification
- **ResNet**: `resnet50` for visual feature extraction
- **Features**: 2048-dimensional feature vectors for image similarity

### Similarity Calculation
- **Method**: Cosine similarity for both text and image features
- **Ranking**: Weighted combination of text (60%) and image (40%) similarity
- **Confidence**: Adjusted based on match type and feature overlap

## Database Schema

### LostItem Table
- `id`: Primary key
- `title`: Item title/name
- `description`: Detailed description
- `location`: Where the item was lost
- `image_path`: Path to uploaded image
- `text_embedding`: AI-generated text embedding (PickleType)
- `image_features`: AI-generated image features (PickleType)
- `categories`: AI-extracted categories (JSON)
- `color_tags`: AI-extracted colors (JSON)
- `timestamp`: Creation timestamp

### FoundItem Table
- Same schema as LostItem

## Performance Considerations

### Model Loading
- Models are loaded once at startup
- GPU acceleration if available (CUDA)
- Fallback to CPU if GPU not available

### Search Optimization
- Embeddings are pre-computed and stored
- Similarity calculations are vectorized
- Results are limited and ranked efficiently

### Memory Management
- Images are processed in batches
- Temporary files are cleaned up
- Embeddings are stored efficiently

## Development

### Running Tests
```bash
python example_usage.py
```

### Adding New Features
1. Update models in `models.py`
2. Add schemas in `schemas.py`
3. Implement CRUD operations in `crud.py`
4. Add API endpoints in `main.py`
5. Update AI processing in `ai.py`

### Customizing AI Models
- Modify model loading in `ai.py`
- Adjust similarity weights in ranking functions
- Add new feature extraction methods
- Update confidence calculation logic

## Troubleshooting

### Common Issues

1. **Model Loading Errors**
   - Check internet connection for downloading models
   - Verify PyTorch installation
   - Check available memory/disk space

2. **Search Not Working**
   - Verify database has items with embeddings
   - Check AI model status at `/health`
   - Ensure proper text preprocessing

3. **Image Processing Issues**
   - Verify PIL installation
   - Check image file formats
   - Ensure sufficient memory for image processing

### Performance Issues
- Monitor GPU memory usage
- Consider reducing image resolution
- Implement caching for frequent queries
- Use database indexing for large datasets

## Future Enhancements

- [ ] Real-time notifications for matches
- [ ] Machine learning for improving match accuracy
- [ ] Integration with campus systems
- [ ] Mobile app development
- [ ] Advanced image preprocessing
- [ ] Multi-language support
- [ ] Geospatial search capabilities
- [ ] User authentication and profiles

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FastAPI for the excellent web framework
- Hugging Face for pre-trained models
- PyTorch for deep learning capabilities
- SQLAlchemy for database management
- The open-source AI community for amazing tools and models