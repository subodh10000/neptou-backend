#!/usr/bin/env python3
"""
Update Guides in RAG System
============================
Updates guide information in the RAG embeddings to match SwiftUI SampleData.
"""

import json
import os
import sys

# Try to import sentence_transformers
try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
except ImportError:
    print("❌ Error: sentence_transformers not installed")
    print("   Please activate your virtual environment:")
    print("   source venv/bin/activate")
    print("   Then run this script again")
    sys.exit(1)

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def main():
    print("🔄 Updating RAG with new guide information...")
    print("=" * 50)
    
    # Load model
    print(f"📦 Loading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)
    
    # Load tourism data
    tourism_file = os.path.join(os.path.dirname(__file__), "tourism_data.json")
    with open(tourism_file, 'r', encoding='utf-8') as f:
        tourism_data = json.load(f)
    
    # Filter guides
    guides = [item for item in tourism_data if item.get('category') == 'guide']
    print(f"📚 Found {len(guides)} guides to process")
    
    if not guides:
        print("⚠️  No guides found in tourism_data.json")
        print("   Make sure guides are added with category: 'guide'")
        return
    
    # Load existing embeddings
    embeddings_file = os.path.join(os.path.dirname(__file__), "tourism_embeddings.json")
    existing_embeddings = []
    if os.path.exists(embeddings_file):
        with open(embeddings_file, 'r', encoding='utf-8') as f:
            existing_embeddings = json.load(f)
        print(f"📖 Loaded {len(existing_embeddings)} existing embeddings")
    else:
        print("⚠️  No existing embeddings file found - creating new one")
    
    # Remove old guide embeddings
    old_count = len(existing_embeddings)
    existing_embeddings = [e for e in existing_embeddings if e.get('metadata', {}).get('category') != 'guide']
    removed_count = old_count - len(existing_embeddings)
    if removed_count > 0:
        print(f"🧹 Removed {removed_count} old guide embeddings")
    print(f"   {len(existing_embeddings)} embeddings remaining")
    
    # Create embeddings for new guides
    print("\n🔢 Creating embeddings for guides...")
    guide_embeddings = []
    
    for guide in guides:
        name = guide.get('name', 'Unknown')
        print(f"   Processing: {name}")
        
        # Create comprehensive searchable text
        searchable_parts = [name]
        
        if guide.get('description'):
            searchable_parts.append(guide['description'])
        
        if guide.get('specialties'):
            specialties = ', '.join(guide['specialties'])
            searchable_parts.append(f"Specialties: {specialties}")
        
        if guide.get('languages'):
            languages = ', '.join(guide['languages'])
            searchable_parts.append(f"Languages: {languages}")
        
        location = guide.get('location', {})
        area = location.get('area', 'Nepal')
        searchable_parts.append(f"Location: {area}")
        
        if guide.get('bio'):
            searchable_parts.append(guide['bio'])
        
        searchable_text = ". ".join(searchable_parts)
        
        # Generate embedding
        embedding = model.encode(searchable_text, convert_to_numpy=True).tolist()
        
        # Create embedding entry
        guide_embedding = {
            'name': name,
            'embedding': embedding,
            'metadata': {
                'category': 'guide',
                'area': area,
                'tags': guide.get('specialties', []) + ['guide', 'local_expert', 'tour_guide'],
                'description': guide.get('description', ''),
                'bio': guide.get('bio', guide.get('description', '')),
                'languages': guide.get('languages', []),
                'specialties': guide.get('specialties', []),
                'price_per_day': guide.get('price_per_day', 0),
                'rating': guide.get('rating', 0),
                'review_count': guide.get('review_count', 0),
                'verified': guide.get('verified', False),
                'type': 'guide',
                'id': guide.get('id', '')
            }
        }
        guide_embeddings.append(guide_embedding)
    
    # Merge with existing
    all_embeddings = existing_embeddings + guide_embeddings
    
    # Save
    print(f"\n💾 Saving embeddings to {embeddings_file}...")
    with open(embeddings_file, 'w', encoding='utf-8') as f:
        json.dump(all_embeddings, f, ensure_ascii=False, indent=2)
    
    print("\n✅ Successfully updated RAG system!")
    print(f"   - Added {len(guide_embeddings)} guide embeddings")
    print(f"   - Total embeddings: {len(all_embeddings)}")
    print("\n📝 Next steps:")
    print("   1. Restart your backend server")
    print("   2. Test with queries like: 'find a guide for culture tours'")
    print("   3. The AI will now recommend these guides when relevant")

if __name__ == "__main__":
    main()
