#!/usr/bin/env python3
"""
Test script to verify that "lost passport" queries return Bibek KC as the primary recommendation.
"""

import asyncio
from ai_service import get_chat_response

async def test_lost_passport():
    """Test that lost passport queries recommend Bibek KC."""
    
    test_queries = [
        "I lost my passport",
        "lost passport",
        "I need help with my passport",
        "lost my passport in kathmandu",
        "who should I contact if I lost my passport?",
    ]
    
    print("=" * 80)
    print("TESTING: Lost Passport Queries - Bibek KC Recommendation")
    print("=" * 80)
    print()
    
    for query in test_queries:
        print(f"Query: {query}")
        print("-" * 80)
        
        messages = [
            {"role": "user", "content": query}
        ]
        
        try:
            response = await get_chat_response(messages)
            print(f"Response:\n{response}\n")
            
            # Check if Bibek KC is mentioned
            response_lower = response.lower()
            if "bibek" in response_lower and "98484488888" in response:
                print("✅ PASS: Bibek KC is recommended with phone number")
            elif "bibek" in response_lower:
                print("⚠️  WARNING: Bibek KC mentioned but phone number might be missing")
            else:
                print("❌ FAIL: Bibek KC is NOT recommended")
            
            print()
            print("=" * 80)
            print()
            
        except Exception as e:
            print(f"❌ ERROR: {e}\n")
            print("=" * 80)
            print()

if __name__ == "__main__":
    asyncio.run(test_lost_passport())
