"""
Test Emergency Contacts in AI Service
=====================================
Test that AI service correctly retrieves and includes Bibek KC when asked about emergency contacts.
"""
import asyncio
from ai_service import get_chat_response

async def test_emergency_queries():
    """Test emergency-related queries in AI chat."""
    print("=" * 60)
    print("Testing Emergency Contacts in AI Chat")
    print("=" * 60)
    
    test_queries = [
        "What are the emergency contacts in Kathmandu?",
        "I need emergency help in Kathmandu",
        "Who can I call for emergency assistance?",
        "Give me emergency numbers for Kathmandu",
        "I need Bibek KC's number",
        "What's the Neptou emergency agent contact?"
    ]
    
    print("\n🤖 Testing AI responses with emergency contacts:\n")
    
    for query in test_queries:
        print(f"Query: '{query}'")
        print("-" * 60)
        
        try:
            messages = [{"role": "user", "content": query}]
            response = await get_chat_response(messages)
            
            # Check if Bibek KC is mentioned
            if "bibek" in response.lower() or "98484488888" in response:
                print("✅ Bibek KC found in response!")
            else:
                print("⚠️  Bibek KC not found in response")
            
            # Check if phone number is included
            if "98484488888" in response or "984-844-88888" in response.replace(" ", ""):
                print("✅ Phone number included!")
            
            print(f"Response preview: {response[:200]}...")
            print()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print()
    
    print("=" * 60)
    print("Test completed!")

if __name__ == "__main__":
    asyncio.run(test_emergency_queries())
