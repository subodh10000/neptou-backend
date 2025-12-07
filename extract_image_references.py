#!/usr/bin/env python3
"""
Extract all image references from tourism_data.json
This script helps identify all images needed for places, foods, and guides.
"""

import json
import os
from collections import defaultdict

def extract_image_references():
    """Extract all image references from tourism_data.json"""
    
    # Load tourism data
    with open('tourism_data.json', 'r', encoding='utf-8') as f:
        places = json.load(f)
    
    # Collect all image references
    place_images = defaultdict(list)
    food_images = []
    guide_images = []
    
    for place in places:
        place_id = place.get('id', 'unknown')
        place_name = place.get('name', 'Unknown')
        images = place.get('images', [])
        
        if images:
            place_images[place_id].extend(images)
        else:
            # Generate placeholder image name based on place ID
            image_name = place_id.replace('ktm_', '').replace('_', '_') + '_main.jpg'
            place_images[place_id].append(image_name)
    
    # Extract food images (places with category "food" or "restaurant")
    for place in places:
        category = place.get('category', '').lower()
        if category in ['food', 'restaurant', 'cuisine']:
            place_id = place.get('id', 'unknown')
            place_name = place.get('name', 'Unknown')
            images = place.get('images', [])
            if images:
                food_images.extend(images)
            else:
                food_images.append(f"{place_id}_main.jpg")
    
    # Guide images (from SampleData - we'll add these manually)
    guide_images = [
        'guide1.jpg',  # Bibek KC
        'guide2.jpg',  # Keshab Thapa
        'guide3.jpg',  # Sushant Jaix
        'guide4.jpg',  # Subodh Kathayat
        'guide5.jpg',  # Sushant Yadav
    ]
    
    # Traditional food images
    traditional_food_images = [
        'dal_bhat.jpg',
        'momo.jpg',
        'samay_baji.jpg',
        'juju_dhau.jpg',
        'chatamari.jpg',
        'sekuwa.jpg',
        'sel_roti.jpg',
        'thukpa.jpg',
        'dhikri.jpg',
        'ghonghi.jpg',
        'tharu_thali.jpg',
        'sidhara.jpg',
        'bhakka.jpg',
    ]
    
    # Print summary
    print("=" * 80)
    print("IMAGE REFERENCE EXTRACTION REPORT")
    print("=" * 80)
    print(f"\nTotal Places: {len(places)}")
    print(f"Places with images: {sum(1 for p in places if p.get('images'))}")
    print(f"Places without images: {sum(1 for p in places if not p.get('images'))}")
    
    print("\n" + "=" * 80)
    print("PLACE IMAGES NEEDED")
    print("=" * 80)
    all_place_images = set()
    for place_id, images in place_images.items():
        all_place_images.update(images)
    
    print(f"\nTotal unique place images: {len(all_place_images)}")
    print("\nImage list:")
    for img in sorted(all_place_images):
        print(f"  - {img}")
    
    print("\n" + "=" * 80)
    print("FOOD IMAGES NEEDED")
    print("=" * 80)
    all_food_images = set(food_images + traditional_food_images)
    print(f"\nTotal unique food images: {len(all_food_images)}")
    print("\nImage list:")
    for img in sorted(all_food_images):
        print(f"  - {img}")
    
    print("\n" + "=" * 80)
    print("GUIDE IMAGES NEEDED")
    print("=" * 80)
    print(f"\nTotal guide images: {len(guide_images)}")
    print("\nImage list:")
    for img in guide_images:
        print(f"  - {img}")
    
    # Generate image mapping file for iOS
    print("\n" + "=" * 80)
    print("GENERATING IMAGE MAPPING FILE")
    print("=" * 80)
    
    mapping = {
        'places': {pid: imgs for pid, imgs in place_images.items()},
        'foods': list(all_food_images),
        'guides': guide_images
    }
    
    with open('image_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)
    
    print("\n✅ Generated image_mapping.json")
    print("\nNext steps:")
    print("1. Add all listed images to Assets.xcassets in Xcode")
    print("2. Use the image names exactly as listed")
    print("3. Images should be in .jpg or .png format")
    print("4. Recommended size: 1200x800px for places, 800x800px for foods/guides")

if __name__ == '__main__':
    extract_image_references()
