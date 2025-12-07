"""
Test Dang-specific RAG queries
"""
import asyncio
from vector_search import get_vector_search

def test_dang_queries():
    """Test Dang-specific queries."""
    print("=" * 60)
    print("Testing Dang Places & Food RAG")
    print("=" * 60)
    
    vector_search = get_vector_search()
    
    # Dang-specific test queries
    test_queries = [
        "tharu culture",
        "dang places to visit",
        "traditional tharu food",
        "dhikri ghonghi",
        "bat cave adventure",
        "tharu homestay",
        "dang waterfall",
        "tharu museum"
    ]
    
    print("\n🔍 Testing Dang-specific queries:\n")
    for query in test_queries:
        print(f"Query: '{query}'")
        results = vector_search.search(query, top_k=3, min_score=0.2)
        
        if results:
            for i, place in enumerate(results, 1):
                name = place.get('name', 'Unknown')
                score = place.get('similarity_score', 0.0)
                category = place.get('metadata', {}).get('category', 'Unknown')
                area = place.get('metadata', {}).get('area', 'Unknown')
                print(f"  {i}. {name} ({category}) - {area} - Score: {score:.4f}")
        else:
            print("  No results found")
        print()
    
    print("✅ Dang RAG test completed!")

if __name__ == "__main__":
    test_dang_queries()
