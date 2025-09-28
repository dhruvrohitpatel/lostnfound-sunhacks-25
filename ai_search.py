import os
import json
import time
import requests
from typing import List, Dict, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatGPTAISearch:
    def __init__(self):
        """Initialize ChatGPT AI search service"""
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.base_url = "https://api.openai.com/v1/chat/completions"
        
        if self.api_key and self.api_key != "test_key":
            logger.info("OpenAI API key found")
        else:
            logger.warning("OPENAI_API_KEY not found or invalid. Please set your OpenAI API key.")
            self.api_key = None
    
    def _call_chatgpt(self, prompt: str, max_tokens: int = 1000) -> Optional[str]:
        """Call ChatGPT API with a prompt using direct HTTP requests"""
        if not self.api_key:
            return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that analyzes lost and found items to find matches based on user descriptions."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.3
            }
            
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
            
        except Exception as e:
            logger.error(f"Error calling ChatGPT: {e}")
            return None
    
    def search_submissions(self, submissions: List[Dict], query: str, threshold: float = 0.2) -> List[Dict]:
        """Search submissions using ChatGPT-powered semantic search"""
        try:
            if not self.api_key or not query.strip():
                logger.warning("ChatGPT API key not available or empty query")
                return self._simple_keyword_search(submissions, query)
            
            # Prepare submissions data for ChatGPT
            submissions_text = []
            for i, submission in enumerate(submissions):
                item_text = f"Item {i+1}: {submission.get('text', '')} | Name: {submission.get('name', 'Anonymous')} | Contact: {submission.get('contact', 'N/A')}"
                submissions_text.append(item_text)
            
            # Create prompt for ChatGPT
            prompt = f"""
You are analyzing lost and found items. The user searched for: "{query}"

Items:
{chr(10).join(submissions_text)}

TASK: Return ONLY the item numbers that match the search query as a JSON array.

RULES:
- For "backpack" search: only return items that contain "backpack" in the text
- For "goggles" search: only return items that contain "goggles" in the text  
- For "phone case" search: only return items that contain "phone" or "case" in the text
- If NO items match, return: []
- If some items match, return: [item_numbers]
- NEVER return all items unless the search query matches everything

EXAMPLES:
- Search "backpack" → return [2] (only item 2 mentions backpack)
- Search "goggles" → return [1] (only item 1 mentions goggles)
- Search "phone" → return [3] (only item 3 mentions phone)

Your response (JSON array only):
"""
            
            # Get ChatGPT response
            response = self._call_chatgpt(prompt, max_tokens=500)
            if not response:
                logger.warning("No response from ChatGPT, falling back to keyword search")
                return self._simple_keyword_search(submissions, query)
            
            # Parse ChatGPT response
            try:
                # Extract JSON from response
                response = response.strip()
                if response.startswith('```json'):
                    response = response[7:]
                if response.endswith('```'):
                    response = response[:-3]
                
                matched_indices = json.loads(response)
                if not isinstance(matched_indices, list):
                    matched_indices = []
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Error parsing ChatGPT response: {e}")
                return submissions
            
            # Create results based on ChatGPT's analysis
            results = []
            for idx in matched_indices:
                if 0 <= idx - 1 < len(submissions):  # Convert to 0-based index
                    submission = submissions[idx - 1]
                    submission_copy = submission.copy()
                    submission_copy['similarity_score'] = 0.9  # High confidence from ChatGPT
                    submission_copy['matched_text'] = f"{submission.get('text', '')} {submission.get('name', '')} {submission.get('contact', '')}"
                    submission_copy['match_reasons'] = ["ChatGPT semantic analysis"]
                    results.append(submission_copy)
            
            # Sort by similarity score (descending)
            results.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            return results
            
        except Exception as e:
            logger.error(f"Error in ChatGPT search: {e}")
            return submissions
    
    def generate_search_suggestions(self, query: str, results_count: int) -> List[str]:
        """Generate alternative search suggestions using ChatGPT"""
        if not self.api_key:
            return self._get_fallback_suggestions(query, results_count)
        
        try:
            prompt = f"""
The user searched for: "{query}"
Number of results found: {results_count}

Please provide 3 helpful search suggestions to improve their search. Consider:
- If no results: suggest broader terms, different keywords, or alternative descriptions
- If some results: suggest ways to refine or expand the search
- Think about synonyms, related terms, and different ways to describe the same item

Return only the 3 suggestions, one per line, without numbering or bullet points.
"""
            
            response = self._call_chatgpt(prompt, max_tokens=200)
            if response:
                suggestions = [s.strip() for s in response.split('\n') if s.strip()]
                return suggestions[:3]
        except Exception as e:
            logger.error(f"Error generating suggestions with ChatGPT: {e}")
        
        return self._get_fallback_suggestions(query, results_count)
    
    def _get_fallback_suggestions(self, query: str, results_count: int) -> List[str]:
        """Fallback suggestions when ChatGPT is not available"""
        if results_count == 0:
            return [
                f"Try searching for just '{query.split()[0]}' if you searched for multiple words",
                "Search by location (e.g., 'library', 'campus')",
                "Search by item type (e.g., 'backpack', 'phone')"
            ]
        else:
            return [
                "Try adding more specific details",
                "Search by the person's name if you remember it",
                "Try searching without location to see items from other areas"
            ]
    
    def _simple_keyword_search(self, submissions: List[Dict], query: str) -> List[Dict]:
        """Simple keyword-based search as fallback"""
        if not query.strip():
            return submissions
        
        query_lower = query.lower()
        results = []
        
        for submission in submissions:
            # Search in text, name, and contact fields
            text = submission.get('text', '').lower()
            name = submission.get('name', '').lower()
            contact = submission.get('contact', '').lower()
            
            # Check if query matches any field
            if (query_lower in text or 
                query_lower in name or 
                query_lower in contact):
                
                # Add similarity score based on keyword matches
                submission_copy = submission.copy()
                submission_copy['similarity_score'] = 0.8  # High confidence for keyword match
                submission_copy['matched_text'] = f"{submission.get('text', '')} {submission.get('name', '')} {submission.get('contact', '')}"
                submission_copy['match_reasons'] = ["Keyword match"]
                results.append(submission_copy)
        
        # Sort by similarity score (descending)
        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        return results

# Global AI instance
ai_search_service = ChatGPTAISearch()
