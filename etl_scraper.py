# neptou-backend/etl_scraper.py

import os
import json
import time
from firecrawl import Firecrawl
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional

# Load environment variables
load_dotenv()

# Initialize Firecrawl (New Class Name)
api_key = os.getenv("FIRECRAWL_API_KEY")
if not api_key:
    print("❌ Error: FIRECRAWL_API_KEY not found in .env file.")
    exit()

app = Firecrawl(api_key=api_key)

# Credit limit - adjust based on your plan
MAX_CREDITS = 500
CREDIT_BUFFER = 50  # Stop when we have less than this many credits left

# The cities we want to "learn" about
# Reduced to lower request limit and API costs
TARGET_CITIES = [
    "Kathmandu", 
    "Pokhara"
]

# --- SENIOR ENGINEER MOVE: Typed Schema ---
# We use Pydantic to strictly define the data shape. 
# This ensures the AI doesn't give us broken JSON.

class PlaceItem(BaseModel):
    name: str = Field(description="Name of the tourist place")
    category: str = Field(description="One of: temple, nature, culture, food, adventure, hotel, market")
    description: str = Field(description="Brief 1 sentence description")
    location_area: str = Field(description="Specific area name")

class CityExtraction(BaseModel):
    places: List[PlaceItem]

def check_credits():
    """Check remaining credits and return True if we can proceed."""
    try:
        usage = app.get_credit_usage()
        
        # Handle ExtractResponse object or dict
        if hasattr(usage, 'remaining_credits'):
            remaining = usage.remaining_credits
        elif isinstance(usage, dict):
            remaining = usage.get('remaining_credits', usage.get('remaining', usage.get('credits_remaining', 0)))
        else:
            # Try to convert to dict
            remaining = getattr(usage, 'remaining_credits', 0)
        
        if remaining:
            print(f"   💳 Credits remaining: {remaining}/{MAX_CREDITS}")
            
            if remaining < CREDIT_BUFFER:
                print(f"   ⚠️  WARNING: Only {remaining} credits left! Stopping to avoid limit.")
                return False
            return True
        else:
            print(f"   💳 Credit check: {usage}")
            return True  # If we can't parse, proceed cautiously
    except Exception as e:
        print(f"   ⚠️  Could not check credits: {e}. Proceeding with caution...")
        return True  # If check fails, proceed but be careful

def scrape_city_data(city):
    print(f"\n🕷️  Scraping top places in {city}...")
    
    # We use a robust travel guide URL or fallback to Wikipedia
    # Wikipedia is reliable for 'extract' calls
    clean_city = city.split()[0]
    url = f"https://en.wikipedia.org/wiki/Tourism_in_{clean_city}"
    
    # Fallback for cities without a 'Tourism in...' page
    if "Dang" in city or "Kailali" in city:
        url = f"https://en.wikipedia.org/wiki/{clean_city}_District"

    prompt = f"Extract only the top 3 most popular tourist destinations in {city}. Keep descriptions very brief."

    try:
        # NEW API METHOD: .extract()
        # This uses AI to read the page and fill our Pydantic model
        data = app.extract(
            urls=[url],
            prompt=prompt,
            schema=CityExtraction.model_json_schema()
        )
        
        # The 'data' object is an ExtractResponse object
        if data:
            # ExtractResponse has a 'data' attribute that contains the extracted content
            if hasattr(data, 'data'):
                extracted_data = data.data
                # The extracted_data should be a dict with our schema structure
                if isinstance(extracted_data, dict):
                    places = extracted_data.get('places', [])
                    if places:
                        print(f"   ✅ Successfully extracted {len(places)} places")
                        return places
                # Sometimes it might be nested
                if isinstance(extracted_data, dict) and 'data' in extracted_data:
                    places = extracted_data['data'].get('places', [])
                    if places:
                        print(f"   ✅ Successfully extracted {len(places)} places")
                        return places
            
            # Try accessing as dict if it has dict-like methods
            if isinstance(data, dict):
                if 'data' in data:
                    places = data['data'].get('places', [])
                    if places:
                        return places
                if 'places' in data:
                    return data['places']
                if 'extract' in data and isinstance(data['extract'], dict):
                    places = data['extract'].get('places', [])
                    if places:
                        return places
            
            # If it's a list, return directly
            if isinstance(data, list):
                return data
            
            # Debug: print what we got
            print(f"   ⚠️  Unexpected response structure. Type: {type(data)}")
            if hasattr(data, '__dict__'):
                print(f"   🔍 Attributes: {list(data.__dict__.keys())}")
        
        return []
    
    except Exception as e:
        print(f"❌ Error scraping {city}: {e}")
        return []

def main():
    print("🚀 Starting ETL Scraper (v2.0)...")
    print(f"💰 Credit limit: {MAX_CREDITS} (will stop at {CREDIT_BUFFER} remaining)")
    print("="*50)
    
    # Check initial credits
    if not check_credits():
        print("❌ Not enough credits to start. Exiting.")
        return
    
    all_places = []
    
    for i, city in enumerate(TARGET_CITIES, 1):
        print(f"\n[{i}/{len(TARGET_CITIES)}] Processing {city}...")
        
        # Check credits before each request
        if not check_credits():
            print(f"⚠️  Stopping early due to low credits. Processed {len(all_places)} places so far.")
            break
        
        places = scrape_city_data(city)
        
        if places:
            print(f"   ✅ Found {len(places)} places in {city}")
            
            # Post-process and clean
            for p in places:
                # Convert Pydantic dict or raw dict to our clean format
                if not isinstance(p, dict):
                    p = p.model_dump() # Convert if it's a Pydantic object
                
                p['city_context'] = city.split()[0]
                
                # Create ID
                clean_name = p['name'].lower().replace(' ', '_').replace("'", "")
                p['id'] = f"{p['city_context'].lower()}_{clean_name}"
                
                all_places.append(p)
        else:
            print(f"   ⚠️  No data found for {city}")
        
        # Check credits after request
        check_credits()
        
        # Longer delay to be safe with rate limits
        if i < len(TARGET_CITIES):
            print(f"   ⏳ Waiting 3 seconds before next request...")
            time.sleep(3)

    # Save to JSON
    output_file = "raw_scraped_data.json"
    with open(output_file, "w") as f:
        json.dump(all_places, f, indent=2)
    
    # Final credit check
    print("\n" + "="*50)
    check_credits()
    print("="*50)
    print(f"🎉 DONE! Saved {len(all_places)} total places to {output_file}")
    print("👉 Now run 'kathmandu_tourism_vectorizer.py' to process this data.")
    print("="*50)

if __name__ == "__main__":
    main()