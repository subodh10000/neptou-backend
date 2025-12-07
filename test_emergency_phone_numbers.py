#!/usr/bin/env python3
"""
Test Emergency Contacts Phone Numbers
=====================================
Test that AI responses include phone numbers for all emergency contacts.
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from ai_service import get_chat_response
from emergency_contacts import EMERGENCY_CONTACTS, format_emergency_contacts_for_llm, search_emergency_contacts

async def test_emergency_phone_numbers():
    """Test that emergency contact responses include phone numbers."""
    
    print("=" * 80)
    print("TESTING: Emergency Contacts Phone Numbers in AI Responses")
    print("=" * 80)
    
    test_queries = [
        "What are the emergency contacts in Kathmandu?",
        "I need emergency contacts",
        "Give me emergency numbers for Kathmandu",
        "Who can I call for emergency help?",
    ]
    
    print("\n🔍 Testing AI responses with emergency contacts:\n")
    
    for query in test_queries:
        print(f"\n{'='*80}")
        print(f"Query: {query}")
        print(f"{'='*80}")
        
        messages = [
            {"role": "user", "content": query}
        ]
        
        try:
            result = await get_chat_response(messages)
            
            # Handle both dict and string responses
            if isinstance(result, dict):
                response_text = result.get("response", "")
            else:
                response_text = result
            
            response_lower = response_text.lower()
            
            # Check for Bibek KC and his number
            has_bibek = "bibek" in response_lower
            has_bibek_number = "98484488888" in response_text or "984-844-88888" in response_text.replace(" ", "")
            
            # Check for other emergency numbers
            has_police = "100" in response_text or "police" in response_lower
            has_ambulance = "102" in response_text or "ambulance" in response_lower
            has_fire = "101" in response_text or "fire" in response_lower
            
            # Count phone numbers in response
            phone_number_patterns = [
                "98484488888", "100", "102", "101", 
                "+977-1-4247041", "+977-1-4424111", "+977-1-5970123"
            ]
            phone_count = sum(1 for pattern in phone_number_patterns if pattern in response_text)
            
            print(f"\nResponse:\n{response_text}\n")
            print(f"Analysis:")
            print(f"  ✅ Bibek KC mentioned: {has_bibek}")
            print(f"  ✅ Bibek KC phone number included: {has_bibek_number}")
            print(f"  ✅ Police mentioned: {has_police}")
            print(f"  ✅ Ambulance mentioned: {has_ambulance}")
            print(f"  ✅ Fire mentioned: {has_fire}")
            print(f"  ✅ Total phone numbers found: {phone_count}")
            
            # Validation
            if has_bibek and has_bibek_number:
                print(f"  ✅ PASS: Bibek KC with phone number")
            elif has_bibek:
                print(f"  ❌ FAIL: Bibek KC mentioned but phone number missing!")
            
            if phone_count >= 3:
                print(f"  ✅ PASS: Multiple phone numbers included")
            elif phone_count > 0:
                print(f"  ⚠️  WARNING: Only {phone_count} phone number(s) found")
            else:
                print(f"  ❌ FAIL: No phone numbers found in response!")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("TESTING: Emergency Contacts Formatting")
    print("=" * 80)
    
    # Test the formatting function
    contacts = search_emergency_contacts("emergency contacts kathmandu")
    formatted = format_emergency_contacts_for_llm(contacts[:5])
    
    print("\nFormatted emergency contacts context:")
    print(formatted)
    
    # Verify phone numbers are in formatted output
    bibek_contact = next((c for c in EMERGENCY_CONTACTS if "bibek" in c.name.lower()), None)
    if bibek_contact:
        if bibek_contact.phone in formatted:
            print(f"\n✅ PASS: Bibek KC phone number ({bibek_contact.phone}) found in formatted context")
        else:
            print(f"\n❌ FAIL: Bibek KC phone number ({bibek_contact.phone}) NOT found in formatted context")
    
    # Check for other phone numbers
    other_contacts = [c for c in contacts[:5] if "bibek" not in c.name.lower()]
    for contact in other_contacts:
        if contact.phone in formatted:
            print(f"✅ {contact.name} phone number ({contact.phone}) found in formatted context")
        else:
            print(f"❌ {contact.name} phone number ({contact.phone}) NOT found in formatted context")

if __name__ == "__main__":
    asyncio.run(test_emergency_phone_numbers())
