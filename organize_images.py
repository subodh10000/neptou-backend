#!/usr/bin/env python3
"""
Organize Images for Xcode
=========================
Lists all matched images ready to add to Xcode Assets
"""

import json
import os
from pathlib import Path

def organize_images(image_folder_path):
    """List all images ready to add to Xcode"""
    
    # Load expected images
    with open('image_mapping.json', 'r', encoding='utf-8') as f:
        mapping = json.load(f)
    
    # Collect all expected image names
    expected_images = {}
    
    # Places
    for place_id, images in mapping['places'].items():
        for img in images:
            expected_images[img] = "place"
    
    # Foods
    for img in mapping['foods']:
        expected_images[img] = "food"
    
    # Guides
    for img in mapping['guides']:
        expected_images[img] = "guide"
    
    # Get all image files in folder
    image_extensions = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}
    found_images = {}
    
    for file in os.listdir(image_folder_path):
        file_path = os.path.join(image_folder_path, file)
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file)
            if ext in image_extensions:
                found_images[file] = file_path
    
    # Match images
    matched = []
    name_variations = {}
    
    for expected_name, category in expected_images.items():
        # Check exact match
        if expected_name in found_images:
            matched.append((expected_name, category, found_images[expected_name]))
        else:
            # Check case-insensitive and extension variations
            expected_base = os.path.splitext(expected_name)[0].lower()
            for found_name, found_path in found_images.items():
                found_base = os.path.splitext(found_name)[0].lower()
                if found_base == expected_base:
                    name_variations[expected_name] = (found_name, found_path, category)
                    matched.append((expected_name, category, found_path))
                    break
    
    # Print organized list
    print("=" * 80)
    print("IMAGES READY TO ADD TO XCODE")
    print("=" * 80)
    print(f"\nTotal matched: {len(matched)} images\n")
    
    # Group by category
    places = [m for m in matched if m[1] == "place"]
    foods = [m for m in matched if m[1] == "food"]
    guides = [m for m in matched if m[1] == "guide"]
    
    print(f"📍 Places: {len(places)} images")
    print(f"🍜 Foods: {len(foods)} images")
    print(f"👤 Guides: {len(guides)} images")
    
    print("\n" + "=" * 80)
    print("PLACE IMAGES (Add to Xcode as Image Sets)")
    print("=" * 80)
    for img_name, _, _ in sorted(places):
        xcode_name = os.path.splitext(img_name)[0]
        print(f"  • {xcode_name}")
    
    print("\n" + "=" * 80)
    print("FOOD IMAGES (Add to Xcode as Image Sets)")
    print("=" * 80)
    for img_name, _, _ in sorted(foods):
        xcode_name = os.path.splitext(img_name)[0]
        print(f"  • {xcode_name}")
    
    print("\n" + "=" * 80)
    print("GUIDE IMAGES (Add to Xcode as Image Sets)")
    print("=" * 80)
    for img_name, _, _ in sorted(guides):
        xcode_name = os.path.splitext(img_name)[0]
        print(f"  • {xcode_name}")
    
    # Name variations
    if name_variations:
        print("\n" + "=" * 80)
        print("NAME VARIATIONS (Use these exact names in Xcode)")
        print("=" * 80)
        for expected, (found, _, category) in name_variations.items():
            xcode_name = os.path.splitext(expected)[0]
            print(f"  • File: {found} → Xcode Name: {xcode_name} ({category})")
    
    print("\n" + "=" * 80)
    print("QUICK ADD INSTRUCTIONS")
    print("=" * 80)
    print("\n1. Open Xcode")
    print("2. Open: Neptou/Neptou/Assets.xcassets")
    print("3. Drag all images from: ~/Downloads/Neptou pictures/")
    print("4. Xcode will create image sets automatically")
    print("5. For name variations, rename the image set to match the expected name")
    print(f"\n✅ You're ready to add {len(matched)} images!")

if __name__ == "__main__":
    import sys
    
    image_folder = "~/Downloads/Neptou pictures/"
    if len(sys.argv) > 1:
        image_folder = sys.argv[1]
    
    # Expand user home directory
    image_folder = os.path.expanduser(image_folder)
    
    organize_images(image_folder)
