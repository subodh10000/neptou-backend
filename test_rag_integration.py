"""
Test RAG Integration
===================
Quick test to verify RAG is working correctly.
"""
import asyncio
from vector_search import get_vector_search

async def test_vector_search():
    """Test basic vector search functionality."""
    print("=" * 60)
    print("Testing Vector Search (RAG)")
    print("=" * 60)
    
    try:
        vector_search = get_vector_search()
        
        # Test queries
        test_queries = [
            "quiet place to meditate",
            "spicy local food",
            "historical architecture",
            "kathmandu temples",
            "peaceful garden"
        ]
        
        print("\n🔍 Testing semantic search queries:\n")
        for query in test_queries:
            print(f"Query: '{query}'")
            results = vector_search.search(query, top_k=3, min_score=0.2)
            
            if results:
                for i, place in enumerate(results, 1):
                    name = place.get('name', 'Unknown')
                    score = place.get('similarity_score', 0.0)
                    category = place.get('metadata', {}).get('category', 'Unknown')
                    print(f"  {i}. {name} ({category}) - Score: {score:.4f}")
            else:
                print("  No results found")
            print()
        
        print("✅ Vector search test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_rag_context_formatting():
    """Test RAG context formatting for LLM."""
    print("\n" + "=" * 60)
    print("Testing RAG Context Formatting")
    print("=" * 60)
    
    try:
        vector_search = get_vector_search()
        
        # Get some results
        results = vector_search.search("temple", top_k=5, min_score=0.2)
        
        if results:
            context = vector_search.format_context_for_llm(results, max_places=5)
            print("\n📝 Formatted context for LLM:")
            print(context)
            print("\n✅ Context formatting test completed!")
            return True
        else:
            print("⚠️  No results to format")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🧪 RAG Integration Test Suite\n")
    
    # Run tests
    results = []
    results.append(asyncio.run(test_vector_search()))
    results.append(asyncio.run(test_rag_context_formatting()))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Vector Search: {'✅ PASS' if results[0] else '❌ FAIL'}")
    print(f"Context Formatting: {'✅ PASS' if results[1] else '❌ FAIL'}")
    
    if all(results):
        print("\n🎉 All tests passed! RAG integration is working.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
