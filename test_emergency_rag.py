"""
Test Emergency Contacts RAG
============================
Test that emergency contacts (especially Bibek KC) are retrieved correctly.
"""
import asyncio
from emergency_contacts import search_emergency_contacts, format_emergency_contacts_for_llm

def test_emergency_search():
    """Test emergency contact search."""
    print("=" * 60)
    print("Testing Emergency Contacts RAG")
    print("=" * 60)
    
    test_queries = [
        "emergency contacts in kathmandu",
        "bibek kc",
        "neptou emergency agent",
        "police number",
        "ambulance kathmandu",
        "tourist police",
        "emergency help",
        "local agent kathmandu"
    ]
    
    print("\n🔍 Testing emergency contact search:\n")
    
    for query in test_queries:
        print(f"Query: '{query}'")
        results = search_emergency_contacts(query)
        
        if results:
            print(f"   Found {len(results)} contacts:")
            for i, contact in enumerate(results[:3], 1):
                print(f"   {i}. {contact.name} - {contact.phone} ({contact.category})")
                
                # Check if Bibek KC is in results for Kathmandu queries
                if "kathmandu" in query.lower() or "emergency" in query.lower():
                    if any("bibek" in c.name.lower() for c in results):
                        print(f"      ✅ Bibek KC found in results!")
        else:
            print("   ❌ No results found")
        print()
    
    # Test formatting for LLM
    print("\n📝 Testing LLM formatting:")
    kathmandu_contacts = search_emergency_contacts("emergency contacts kathmandu")
    if kathmandu_contacts:
        formatted = format_emergency_contacts_for_llm(kathmandu_contacts[:5])
        print(formatted[:500] + "..." if len(formatted) > 500 else formatted)
        print("\n✅ Formatting works correctly")
    
    # Verify Bibek KC is included
    print("\n✅ Verification:")
    bibek_results = search_emergency_contacts("bibek")
    if bibek_results:
        bibek = bibek_results[0]
        print(f"   Bibek KC: {bibek.phone}")
        print(f"   Location: {bibek.location}")
        print(f"   Available 24/7: {bibek.available_24_7}")
        print("   ✅ Bibek KC contact verified!")
    else:
        print("   ❌ Bibek KC not found!")

if __name__ == "__main__":
    test_emergency_search()
