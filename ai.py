import os
import time
import pickle
import numpy as np
from typing import List, Dict, Tuple, Optional, Any
from PIL import Image
import torch
import torchvision.transforms as transforms
from sentence_transformers import SentenceTransformer
from transformers import CLIPProcessor, CLIPModel
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LostFoundAI:
    def __init__(self):
        """Initialize AI models for text and image processing"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
        
        # Initialize text embedding model
        try:
            self.text_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Text embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load text model: {e}")
            self.text_model = None
        
        # Initialize CLIP model for image-text understanding
        try:
            self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
            self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
            self.clip_model.to(self.device)
            logger.info("CLIP model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load CLIP model: {e}")
            self.clip_model = None
            self.clip_processor = None
        
        # Initialize image feature extractor (ResNet for visual features)
        try:
            self.resnet = torch.hub.load('pytorch/vision:v0.10.0', 'resnet50', pretrained=True)
            self.resnet.eval()
            self.resnet.to(self.device)
            self.image_transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            logger.info("ResNet model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load ResNet model: {e}")
            self.resnet = None
            self.image_transform = None
    
    def get_text_embedding(self, text: str) -> Optional[np.ndarray]:
        """Generate text embedding for semantic search"""
        if not self.text_model or not text.strip():
            return None
        
        try:
            embedding = self.text_model.encode(text)
            return embedding
        except Exception as e:
            logger.error(f"Error generating text embedding: {e}")
            return None
    
    def extract_image_features(self, image_path: str) -> Optional[np.ndarray]:
        """Extract visual features from image using ResNet"""
        if not self.resnet or not os.path.exists(image_path):
            return None
        
        try:
            image = Image.open(image_path).convert('RGB')
            image_tensor = self.image_transform(image).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                features = self.resnet(image_tensor)
                # Remove the final classification layer, keep features
                features = torch.nn.functional.adaptive_avg_pool2d(
                    features.view(features.size(0), -1, 1, 1), (1, 1)
                ).view(features.size(0), -1)
                return features.cpu().numpy().flatten()
        except Exception as e:
            logger.error(f"Error extracting image features: {e}")
            return None
    
    def analyze_image_content(self, image_path: str) -> Dict[str, Any]:
        """Analyze image content using CLIP for categories and descriptions"""
        if not self.clip_model or not os.path.exists(image_path):
            return {"categories": [], "colors": [], "description": ""}
        
        try:
            image = Image.open(image_path).convert('RGB')
            
            # Predefined categories for lost and found items
            categories = [
                "backpack", "laptop", "phone", "keys", "wallet", "book", "clothing", 
                "shoes", "glasses", "jewelry", "bag", "umbrella", "bottle", "electronics",
                "notebook", "pen", "watch", "headphones", "charger", "jacket", "hat"
            ]
            
            # Predefined color descriptions
            colors = [
                "black", "white", "red", "blue", "green", "yellow", "orange", "purple", 
                "pink", "brown", "gray", "silver", "gold"
            ]
            
            # Process image and categories
            inputs = self.clip_processor(text=categories, images=image, return_tensors="pt", padding=True)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.clip_model(**inputs)
                logits_per_image = outputs.logits_per_image
                probs = logits_per_image.softmax(dim=-1)
            
            # Get top categories
            top_categories = []
            category_probs = probs[0].cpu().numpy()
            top_indices = np.argsort(category_probs)[-5:][::-1]  # Top 5 categories
            
            for idx in top_indices:
                if category_probs[idx] > 0.1:  # Threshold for relevance
                    top_categories.append(categories[idx])
            
            # Analyze colors
            detected_colors = self._detect_colors(image)
            
            return {
                "categories": top_categories,
                "colors": detected_colors,
                "description": self._generate_image_description(image)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing image content: {e}")
            return {"categories": [], "colors": [], "description": ""}
    
    def _detect_colors(self, image: Image.Image) -> List[str]:
        """Simple color detection based on dominant colors"""
        try:
            # Convert to numpy array
            img_array = np.array(image)
            img_array = img_array.reshape(-1, 3)
            
            # Define color ranges (RGB)
            color_ranges = {
                "red": ([100, 0, 0], [255, 100, 100]),
                "blue": ([0, 0, 100], [100, 100, 255]),
                "green": ([0, 100, 0], [100, 255, 100]),
                "yellow": ([100, 100, 0], [255, 255, 100]),
                "black": ([0, 0, 0], [50, 50, 50]),
                "white": ([200, 200, 200], [255, 255, 255]),
                "gray": ([50, 50, 50], [200, 200, 200]),
                "brown": ([100, 50, 0], [200, 150, 100]),
            }
            
            detected_colors = []
            for color_name, (lower, upper) in color_ranges.items():
                mask = np.all((img_array >= lower) & (img_array <= upper), axis=1)
                if np.sum(mask) > len(img_array) * 0.1:  # 10% threshold
                    detected_colors.append(color_name)
            
            return detected_colors[:3]  # Return top 3 colors
            
        except Exception as e:
            logger.error(f"Error detecting colors: {e}")
            return []
    
    def _generate_image_description(self, image: Image.Image) -> str:
        """Generate a simple description of the image"""
        try:
            if not self.clip_model:
                return "Image description not available"
            
            # Simple description prompts
            prompts = [
                "A photo of a lost item",
                "A personal belonging",
                "An everyday object",
                "Something valuable"
            ]
            
            inputs = self.clip_processor(text=prompts, images=image, return_tensors="pt", padding=True)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.clip_model(**inputs)
                logits_per_image = outputs.logits_per_image
                probs = logits_per_image.softmax(dim=-1)
            
            best_prompt_idx = torch.argmax(probs).item()
            return prompts[best_prompt_idx]
            
        except Exception as e:
            logger.error(f"Error generating image description: {e}")
            return "Image description not available"
    
    def calculate_text_similarity(self, query_embedding: np.ndarray, item_embedding: np.ndarray) -> float:
        """Calculate cosine similarity between text embeddings"""
        try:
            if item_embedding is None or query_embedding is None:
                return 0.0
            
            # Ensure embeddings are numpy arrays
            if not isinstance(query_embedding, np.ndarray):
                query_embedding = np.array(query_embedding)
            if not isinstance(item_embedding, np.ndarray):
                item_embedding = np.array(item_embedding)
            
            similarity = sklearn_cosine_similarity([query_embedding], [item_embedding])[0][0]
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating text similarity: {e}")
            return 0.0
    
    def calculate_image_similarity(self, query_features: np.ndarray, item_features: np.ndarray) -> float:
        """Calculate cosine similarity between image features"""
        try:
            if item_features is None or query_features is None:
                return 0.0
            
            # Ensure features are numpy arrays
            if not isinstance(query_features, np.ndarray):
                query_features = np.array(query_features)
            if not isinstance(item_features, np.ndarray):
                item_features = np.array(item_features)
            
            similarity = sklearn_cosine_similarity([query_features], [item_features])[0][0]
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating image similarity: {e}")
            return 0.0
    
    def rank_results(self, results: List[Dict], query_text: str = None, query_image_path: str = None) -> List[Dict]:
        """Rank search results based on combined text and image similarity"""
        try:
            ranked_results = []
            
            for result in results:
                item = result['item']
                text_score = result.get('text_similarity', 0.0)
                image_score = result.get('image_similarity', 0.0)
                
                # Combined scoring with weights
                text_weight = 0.6
                image_weight = 0.4
                
                # Adjust weights based on available data
                if query_text and query_image_path:
                    combined_score = (text_score * text_weight) + (image_score * image_weight)
                    match_type = "combined"
                elif query_text:
                    combined_score = text_score
                    match_type = "text"
                else:
                    combined_score = image_score
                    match_type = "image"
                
                # Boost score for category/color matches
                category_bonus = 0.0
                if query_text:
                    query_lower = query_text.lower()
                    if item.categories is not None:
                        for category in item.categories:
                            if category.lower() in query_lower:
                                category_bonus += 0.1
                    
                    if item.color_tags is not None:
                        for color in item.color_tags:
                            if color.lower() in query_lower:
                                category_bonus += 0.05
                
                final_score = min(1.0, combined_score + category_bonus)
                
                # Determine confidence based on score and match type
                confidence = self._calculate_confidence(final_score, match_type)
                
                ranked_results.append({
                    'item': item,
                    'similarity_score': final_score,
                    'match_type': match_type,
                    'confidence': confidence,
                    'matched_features': self._get_matched_features(item, query_text)
                })
            
            # Sort by similarity score (descending)
            ranked_results.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            return ranked_results
            
        except Exception as e:
            logger.error(f"Error ranking results: {e}")
            return results
    
    def _calculate_confidence(self, score: float, match_type: str) -> float:
        """Calculate confidence score based on similarity and match type"""
        base_confidence = score
        
        # Adjust confidence based on match type
        if match_type == "combined":
            confidence_multiplier = 1.2
        elif match_type == "text":
            confidence_multiplier = 1.0
        else:  # image
            confidence_multiplier = 0.8
        
        return min(1.0, base_confidence * confidence_multiplier)
    
    def _get_matched_features(self, item, query_text: str = None) -> List[str]:
        """Determine which features of the item matched the query"""
        matched_features = []
        
        if not query_text:
            return matched_features
        
        query_lower = query_text.lower()
        
        # Check category matches
        if item.categories is not None:
            for category in item.categories:
                if category.lower() in query_lower:
                    matched_features.append(f"category: {category}")
        
        # Check color matches
        if item.color_tags is not None:
            for color in item.color_tags:
                if color.lower() in query_lower:
                    matched_features.append(f"color: {color}")
        
        # Check location matches
        if item.location and item.location.lower() in query_lower:
            matched_features.append(f"location: {item.location}")
        
        # Check title/description matches
        if item.title and item.title.lower() in query_lower:
            matched_features.append(f"title: {item.title}")
        
        return matched_features
    
    def generate_search_suggestions(self, query: str, results_count: int) -> List[str]:
        """Generate alternative search suggestions based on the query"""
        suggestions = []
        
        # If no results, suggest broader terms
        if results_count == 0:
            suggestions.extend([
                f"Try searching for just '{query.split()[0]}' if you searched for multiple words",
                "Search by location (e.g., 'library', 'campus')",
                "Search by color (e.g., 'black', 'red')",
                "Search by item type (e.g., 'backpack', 'phone')"
            ])
        else:
            suggestions.extend([
                "Try adding more specific details like color or location",
                "Search by the brand name if you remember it",
                "Try searching without the location to see items from other areas"
            ])
        
        return suggestions[:3]  # Return top 3 suggestions

# Global AI instance
ai_service = LostFoundAI()

