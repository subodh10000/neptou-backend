"""
Vector Search Module for RAG
============================
Loads tourism place embeddings and performs semantic search.
Now includes local insights and authentic Nepal information.
"""
import os
import json
import numpy as np
from typing import List, Dict, Tuple, Optional
from sentence_transformers import SentenceTransformer

# Initialize the embedding model (must match the one used in vectorizer)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

class VectorSearch:
    """Manages vector embeddings and performs semantic search."""
    
    def __init__(self, embeddings_path: str = "tourism_embeddings.json"):
        """
        Initialize the vector search system.
        
        Args:
            embeddings_path: Path to the JSON file containing place embeddings
        """
        self.embeddings_path = embeddings_path
        self.model = None
        self.places_data = []
        self.embeddings = []
        self._load_embeddings()
        self._load_model()
    
    def _load_model(self):
        """Load the sentence transformer model."""
        try:
            self.model = SentenceTransformer(EMBEDDING_MODEL)
            print(f"✅ Loaded embedding model: {EMBEDDING_MODEL}")
        except Exception as e:
            print(f"❌ Error loading embedding model: {e}")
            raise
    
    def _load_embeddings(self):
        """Load place embeddings from JSON file."""
        try:
            embeddings_file = os.path.join(
                os.path.dirname(__file__), 
                self.embeddings_path
            )
            
            if not os.path.exists(embeddings_file):
                print(f"⚠️  Warning: Embeddings file not found at {embeddings_file}")
                print("   Run 'kathmandu_tourism_vectorizer.py' first to generate embeddings.")
                return
            
            with open(embeddings_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.places_data = data
            self.embeddings = [np.array(item['embedding']) for item in data]
            
            # Also load emergency contacts embeddings if available
            self._load_emergency_contacts()
            
            # Count different types of entries
            places_count = sum(1 for item in data if item.get('metadata', {}).get('type') != 'local_insight')
            insights_count = sum(1 for item in data if item.get('metadata', {}).get('type') == 'local_insight')
            
            print(f"✅ Loaded {len(self.places_data)} total entries:")
            print(f"   - {places_count} places")
            print(f"   - {insights_count} local insights")
        except Exception as e:
            print(f"❌ Error loading embeddings: {e}")
            self.places_data = []
            self.embeddings = []
    
    def _load_emergency_contacts(self):
        """Load emergency contacts embeddings if available."""
        try:
            emergency_file = os.path.join(os.path.dirname(__file__), "emergency_contacts_embeddings.json")
            if os.path.exists(emergency_file):
                with open(emergency_file, 'r', encoding='utf-8') as f:
                    emergency_data = json.load(f)
                
                # Add emergency contacts to places data (they'll be searchable)
                for contact in emergency_data:
                    # Format as place-like structure for compatibility
                    self.places_data.append({
                        "name": contact["name"],
                        "embedding": contact["embedding"],
                        "metadata": {
                            "category": "emergency",
                            "area": contact["location"],
                            "tags": [contact["category"], "emergency", "contact"]
                        }
                    })
                    self.embeddings.append(np.array(contact["embedding"]))
                
                print(f"✅ Loaded {len(emergency_data)} emergency contacts with embeddings")
        except Exception as e:
            print(f"⚠️  Could not load emergency contacts: {e}")
    
    def search(self, query: str, top_k: int = 5, min_score: float = 0.0) -> List[Dict]:
        """
        Perform semantic search to find relevant places and local insights.
        
        Args:
            query: User's search query
            top_k: Number of top results to return
            min_score: Minimum similarity score threshold
        
        Returns:
            List of dictionaries containing place/insight information and similarity scores
        """
        if not self.model or not self.places_data:
            # Silently return empty list - RAG will gracefully degrade
            return []
        
        # Convert query to vector
        query_vec = self.model.encode(query, convert_to_numpy=True)
        
        # Calculate cosine similarity with all places
        results = []
        for i, place_vec in enumerate(self.embeddings):
            # Cosine similarity: dot product / (norm_a * norm_b)
            similarity = np.dot(query_vec, place_vec) / (
                np.linalg.norm(query_vec) * np.linalg.norm(place_vec)
            )
            
            if similarity >= min_score:
                place_info = {
                    **self.places_data[i],
                    'similarity_score': float(similarity)
                }
                results.append(place_info)
        
        # Sort by similarity (highest first)
        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        # Return top K results
        return results[:top_k]
    
    def get_places_by_names(self, place_names: List[str]) -> List[Dict]:
        """
        Retrieve full place information by names.
        
        Args:
            place_names: List of place names to retrieve
        
        Returns:
            List of place dictionaries
        """
        results = []
        place_names_lower = [name.lower() for name in place_names]
        
        for place in self.places_data:
            if place['name'].lower() in place_names_lower:
                results.append(place)
        
        return results
    
    def get_places_by_category(self, category: str) -> List[Dict]:
        """
        Get all places in a specific category.
        
        Args:
            category: Category to filter by
        
        Returns:
            List of places in that category
        """
        return [
            place for place in self.places_data
            if place.get('metadata', {}).get('category', '').lower() == category.lower()
        ]
    
    def format_context_for_llm(self, places: List[Dict], max_places: int = 10) -> str:
        """
        Format retrieved places, guides, and local insights into a context string for the LLM.
        
        Args:
            places: List of place/guide/insight dictionaries
            max_places: Maximum number of places to include
        
        Returns:
            Formatted context string
        """
        if not places:
            return ""
        
        context_parts = ["\n[RELEVANT INFORMATION FROM KNOWLEDGE BASE]"]
        
        # Separate places, guides, and local insights
        regular_places = []
        guides = []
        local_insights = []
        
        for place in places[:max_places]:
            metadata = place.get('metadata', {})
            item_type = metadata.get('type', '')
            category = metadata.get('category', '')
            
            if item_type == 'local_insight':
                local_insights.append(place)
            elif category == 'guide' or item_type == 'guide':
                guides.append(place)
            else:
                regular_places.append(place)
        
        # Format guides (special formatting)
        if guides:
            context_parts.append("\n[LOCAL GUIDES]")
            for guide in guides:
                name = guide.get('name', 'Unknown')
                metadata = guide.get('metadata', {})
                bio = metadata.get('bio', metadata.get('description', ''))
                specialties = metadata.get('specialties', [])
                languages = metadata.get('languages', [])
                area = metadata.get('area', 'Nepal')
                price = metadata.get('price_per_day', 0)
                rating = metadata.get('rating', 0)
                
                context_parts.append(f"\n- {name}")
                context_parts.append(f"  Location: {area}")
                if bio:
                    context_parts.append(f"  {bio}")
                if specialties:
                    context_parts.append(f"  Specialties: {', '.join(specialties)}")
                if languages:
                    context_parts.append(f"  Languages: {', '.join(languages)}")
                if price > 0:
                    context_parts.append(f"  Price: NPR {price}/day")
                if rating > 0:
                    context_parts.append(f"  Rating: {rating}/5.0")
        
        # Format regular places
        if regular_places:
            context_parts.append("\n[PLACES TO VISIT]")
            for place in regular_places:
                name = place.get('name', 'Unknown')
                category = place.get('metadata', {}).get('category', 'Unknown')
                area = place.get('metadata', {}).get('area', 'Unknown')
                tags = place.get('metadata', {}).get('tags', [])
                
                context_parts.append(f"\n- {name} ({category})")
                context_parts.append(f"  Location: {area}")
                if tags:
                    context_parts.append(f"  Tags: {', '.join(tags)}")
        
        # Format local insights
        if local_insights:
            for insight in local_insights:
                title = insight.get('name', 'Unknown')
                content = insight.get('metadata', {}).get('content', '')
                district = insight.get('metadata', {}).get('area', 'Nepal')
                tags = insight.get('metadata', {}).get('tags', [])
                
                context_parts.append(f"\n- {title} ({district})")
                context_parts.append(f"  {content}")
                if tags:
                    context_parts.append(f"  Tags: {', '.join(tags)}")
        
        context_parts.append("\n")
        return "\n".join(context_parts)


# Global instance (singleton pattern)
_vector_search_instance: Optional[VectorSearch] = None

def get_vector_search() -> VectorSearch:
    """Get or create the global vector search instance."""
    global _vector_search_instance
    if _vector_search_instance is None:
        _vector_search_instance = VectorSearch()
    return _vector_search_instance
