import openai
import numpy as np

openai.api_key = "YOUR_API_KEY"

def get_embedding(text: str):
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1)*np.linalg.norm(vec2))
