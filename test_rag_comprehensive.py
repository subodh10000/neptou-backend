"""
Comprehensive RAG Test Suite
Tests all aspects of the RAG system including Dang places and food
"""
import json
from vector_search import get_vector_search

def test_all_places():
    """Test that all places are loaded correctly."""
    print("=" * 60)
    print("Test 1: Loading All Places")
    print("=" * 60)
    
    vector_search = get_vector_search()
    places_count = len(vector_search.places_data)
    
    print(f"\n✅ Total places loaded: {places_count}")
    
    # Count by category
    categories = {}
    dang_places = []
    
    for place in vector_search.places_data:
        category = place.get('metadata', {}).get('category', 'unknown')
        categories[category] = categories.get(category, 0) + 1
        
        name = place.get('name', '')
        if 'dang' in name.lower() or 'tharu' in name.lower():
            dang_places.append(name)
    
    print("\n📊 Places by category:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")
    
    print(f"\n🏛️  Dang/Tharu places found: {len(dang_places)}")
    for place in dang_places:
        print(f"  - {place}")
    
    return places_count == 23

def test_dang_food_queries():
    """Test queries related to Dang food."""
    print("\n" + "=" * 60)
    print("Test 2: Dang Food Queries")
    print("=" * 60)
    
    vector_search = get_vector_search()
    
    food_queries = [
        "dhikri",
        "ghonghi snail curry",
        "tharu food",
        "anadi rice",
        "traditional terai cuisine",
        "tharu thali"
    ]
    
    print("\n🔍 Testing food-related queries:\n")
    all_found = True
    
    for query in food_queries:
        print(f"Query: '{query}'")
        results = vector_search.search(query, top_k=3, min_score=0.2)
        
        if results:
            for i, place in enumerate(results, 1):
                name = place.get('name', 'Unknown')
                score = place.get('similarity_score', 0.0)
                print(f"  {i}. {name} - Score: {score:.4f}")
            
            # Check if any Dang/Tharu place is in results
            has_dang = any('dang' in r.get('name', '').lower() or 'tharu' in r.get('name', '').lower() 
                          for r in results)
            if has_dang:
                print("  ✅ Found Dang/Tharu related place")
            else:
                print("  ⚠️  No Dang/Tharu place in top results")
        else:
            print("  ❌ No results found")
            all_found = False
        print()
    
    return all_found

def test_dang_places_queries():
    """Test queries for Dang places."""
    print("=" * 60)
    print("Test 3: Dang Places Queries")
    print("=" * 60)
    
    vector_search = get_vector_search()
    
    place_queries = [
        "dang district",
        "tharu culture experience",
        "bat cave",
        "waterfall in dang",
        "tharu museum",
        "world tallest trishul",
        "tharu homestay"
    ]
    
    print("\n🔍 Testing place-related queries:\n")
    all_found = True
    
    for query in place_queries:
        print(f"Query: '{query}'")
        results = vector_search.search(query, top_k=3, min_score=0.2)
        
        if results:
            for i, place in enumerate(results, 1):
                name = place.get('name', 'Unknown')
                score = place.get('similarity_score', 0.0)
                area = place.get('metadata', {}).get('area', 'Unknown')
                print(f"  {i}. {name} ({area}) - Score: {score:.4f}")
            
            # Check if top result is Dang-related
            top_result = results[0].get('name', '').lower()
            if 'dang' in top_result or 'tharu' in top_result or 'chamera' in top_result or 'purandhara' in top_result:
                print("  ✅ Top result is Dang-related")
            else:
                print(f"  ⚠️  Top result '{results[0].get('name')}' may not be Dang-specific")
        else:
            print("  ❌ No results found")
            all_found = False
        print()
    
    return all_found

def test_context_formatting():
    """Test RAG context formatting."""
    print("=" * 60)
    print("Test 4: Context Formatting")
    print("=" * 60)
    
    vector_search = get_vector_search()
    
    # Test with Dang-specific query
    results = vector_search.search("tharu culture and food", top_k=5, min_score=0.2)
    
    if results:
        context = vector_search.format_context_for_llm(results, max_places=5)
        print("\n📝 Formatted context for LLM:")
        print(context[:500] + "..." if len(context) > 500 else context)
        print("\n✅ Context formatting works correctly")
        return True
    else:
        print("❌ No results to format")
        return False

def test_knowledge_base():
    """Test knowledge_base.py Dang information."""
    print("\n" + "=" * 60)
    print("Test 5: Knowledge Base (knowledge_base.py)")
    print("=" * 60)
    
    try:
        import knowledge_base
        
        # Test Dang context
        dang_context = knowledge_base.get_city_context(["dang"])
        
        print("\n📚 Dang context from knowledge_base.py:")
        print(dang_context)
        
        # Check if food items are mentioned
        food_items = ["dhikri", "ghonghi", "anadi rice", "sidhara", "tharu thali"]
        found_foods = []
        
        for food in food_items:
            if food.lower() in dang_context.lower():
                found_foods.append(food)
        
        print(f"\n🍽️  Food items found in context: {len(found_foods)}/{len(food_items)}")
        for food in found_foods:
            print(f"  ✅ {food}")
        
        return len(found_foods) >= 3  # At least 3 food items should be found
    except Exception as e:
        print(f"❌ Error testing knowledge base: {e}")
        return False

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("🧪 COMPREHENSIVE RAG TEST SUITE")
    print("=" * 60)
    print("\nTesting RAG system with Dang places and food...\n")
    
    results = []
    
    # Run all tests
    results.append(("Loading All Places", test_all_places()))
    results.append(("Dang Food Queries", test_dang_food_queries()))
    results.append(("Dang Places Queries", test_dang_places_queries()))
    results.append(("Context Formatting", test_context_formatting()))
    results.append(("Knowledge Base", test_knowledge_base()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n📊 Results: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! RAG system is working correctly.")
    else:
        print(f"\n⚠️  {len(results) - passed} test(s) failed. Check output above.")
    
    return passed == len(results)

if __name__ == "__main__":
    main()
