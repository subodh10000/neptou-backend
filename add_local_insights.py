#!/usr/bin/env python3
"""
Add Local Insights to RAG System
=================================
This script adds local, authentic Nepal insights to the RAG knowledge base.
These are insider tips and information not available on the internet.

Usage:
    python3 add_local_insights.py
    
Or with virtual environment:
    source venv/bin/activate
    python3 add_local_insights.py
"""

import json
import os
import sys

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
except ImportError:
    print("❌ Error: sentence_transformers not installed")
    print("   Install with: pip install sentence-transformers numpy")
    print("   Or activate your virtual environment first")
    sys.exit(1)

# Initialize embedding model (same as used in vectorizer)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def load_local_insights():
    """Load local insights from JSON file."""
    insights_file = os.path.join(os.path.dirname(__file__), "local_insights.json")
    
    if not os.path.exists(insights_file):
        print(f"❌ Local insights file not found: {insights_file}")
        return []
    
    with open(insights_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data.get("local_insights", [])

def create_embeddings_for_insights(insights):
    """Create embeddings for local insights."""
    print(f"📚 Loading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)
    
    insights_with_embeddings = []
    
    for insight in insights:
        # Create searchable text from insight
        searchable_text = f"{insight['title']}. {insight['content']}"
        if insight.get('tags'):
            searchable_text += f" Tags: {', '.join(insight['tags'])}"
        
        # Generate embedding
        embedding = model.encode(searchable_text, convert_to_numpy=True).tolist()
        
        # Create structure compatible with tourism_embeddings.json
        insight_data = {
            "name": insight['title'],
            "embedding": embedding,
            "metadata": {
                "category": insight.get('category', 'local_insight'),
                "area": insight.get('district', 'Nepal'),
                "tags": insight.get('tags', []),
                "content": insight['content'],
                "authenticity_level": insight.get('authenticity_level', 'local_expert'),
                "type": "local_insight",
                "id": insight.get('id', '')
            }
        }
        
        insights_with_embeddings.append(insight_data)
    
    return insights_with_embeddings

def merge_with_tourism_embeddings(insights_embeddings):
    """Merge local insights with existing tourism embeddings."""
    embeddings_file = os.path.join(os.path.dirname(__file__), "tourism_embeddings.json")
    
    existing_data = []
    if os.path.exists(embeddings_file):
        with open(embeddings_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        print(f"✅ Loaded {len(existing_data)} existing places")
    else:
        print("⚠️  No existing tourism_embeddings.json found - creating new file")
    
    # Add local insights to existing data
    merged_data = existing_data + insights_embeddings
    
    # Save merged data
    with open(embeddings_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Added {len(insights_embeddings)} local insights")
    print(f"✅ Total entries in knowledge base: {len(merged_data)}")
    
    return merged_data

def main():
    """Main function to add local insights to RAG."""
    print("🚀 Adding Local Insights to RAG System...")
    print("=" * 50)
    
    # Load local insights
    insights = load_local_insights()
    if not insights:
        print("❌ No local insights found. Please add insights to local_insights.json")
        return
    
    print(f"📖 Loaded {len(insights)} local insights")
    
    # Create embeddings
    print("\n🔢 Creating embeddings...")
    insights_with_embeddings = create_embeddings_for_insights(insights)
    
    # Merge with existing embeddings
    print("\n🔀 Merging with existing knowledge base...")
    merged_data = merge_with_tourism_embeddings(insights_with_embeddings)
    
    print("\n✅ Local insights successfully added to RAG system!")
    print("\n📝 Next steps:")
    print("   1. Restart your backend server")
    print("   2. Test with queries like: 'best time to visit Pashupatinath'")
    print("   3. The AI will now include local insights in responses")

if __name__ == "__main__":
    main()
