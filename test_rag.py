"""
test_rag.py
Run this to verify your AI 'Brain' is working correctly.
"""
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# 1. Load your generated data
try:
    with open("tourism_embeddings.json", "r") as f:
        data = json.load(f)
    print(f"✅ Loaded {len(data)} places from your Knowledge Base.")
except FileNotFoundError:
    print("❌ Error: Run 'kathmandu_tourism_vectorizer.py' first!")
    exit()

# 2. Initialize the model (Must match the one used in vectorizer)
model = SentenceTransformer("all-MiniLM-L6-v2")

def search(query):
    print(f"\n🔎 Query: '{query}'")
    
    # Convert query to vector
    query_vec = model.encode(query)
    
    # Calculate similarity with every place
    results = []
    for item in data:
        place_vec = np.array(item['embedding'])
        # Cosine Similarity Formula
        similarity = np.dot(query_vec, place_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(place_vec))
        results.append((similarity, item['name'], item['metadata']['category']))
    
    # Sort by best match
    results.sort(key=lambda x: x[0], reverse=True)
    
    # Print top 3
    for score, name, cat in results[:3]:
        print(f"   {score:.4f} | {name} ({cat})")

# --- TEST CASES ---
# These queries test "Vibe" rather than keywords
search("I want a quiet place to meditate") 
search("Spicy local food")
search("Historical architecture")