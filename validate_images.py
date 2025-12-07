#!/usr/bin/env python3
"""
Image Validation Script
======================
Validates that your image files match the expected names from image_mapping.json
"""

import json
import os
from pathlib import Path

def validate_images(image_folder_path):
    """Validate images in a folder against image_mapping.json"""
    
    # Load expected images
    with open('image_mapping.json', 'r', encoding='utf-8') as f:
        mapping = json.load(f)
    
    # Collect all expected image names
    expected_images = set()
    
    # Places
    for place_id, images in mapping['places'].items():
        for img in images:
            expected_images.add(img)
    
    # Foods
    for img in mapping['foods']:
        expected_images.add(img)
    
    # Guides
    for img in mapping['guides']:
        expected_images.add(img)
    
    print("=" * 80)
    print("IMAGE VALIDATION REPORT")
    print("=" * 80)
    print(f"\nTotal expected images: {len(expected_images)}")
    
    # Check if folder exists
    if not os.path.exists(image_folder_path):
        print(f"\n❌ Folder not found: {image_folder_path}")
        print(f"\nPlease provide the path to your images folder.")
        print(f"Example: python3 validate_images.py /path/to/your/images")
        return
    
    # Get all image files in folder
    image_extensions = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}
    found_images = set()
    
    for file in os.listdir(image_folder_path):
        file_path = os.path.join(image_folder_path, file)
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file)
            if ext in image_extensions:
                found_images.add(file)
    
    print(f"Images found in folder: {len(found_images)}")
    print(f"\n{'='*80}")
    print("VALIDATION RESULTS")
    print(f"{'='*80}\n")
    
    # Check matches
    matches = []
    missing = []
    extra = []
    
    for expected in sorted(expected_images):
        # Check exact match
        if expected in found_images:
            matches.append(expected)
        else:
            # Check case-insensitive match
            found_match = None
            for found in found_images:
                if found.lower() == expected.lower():
                    found_match = found
                    break
            
            if found_match:
                print(f"⚠️  Case mismatch: Expected '{expected}', found '{found_match}'")
                matches.append(expected)
            else:
                missing.append(expected)
    
    # Find extra images (not in expected list)
    for found in found_images:
        if found not in expected_images:
            # Case-insensitive check
            is_expected = any(found.lower() == exp.lower() for exp in expected_images)
            if not is_expected:
                extra.append(found)
    
    # Print results
    print(f"✅ Matched images: {len(matches)}")
    if matches:
        print(f"   First 10: {', '.join(sorted(matches)[:10])}")
    
    print(f"\n❌ Missing images: {len(missing)}")
    if missing:
        print(f"   First 20 missing:")
        for img in sorted(missing)[:20]:
            print(f"     - {img}")
        if len(missing) > 20:
            print(f"     ... and {len(missing) - 20} more")
    
    if extra:
        print(f"\n📦 Extra images (not in mapping): {len(extra)}")
        print(f"   These might be additional images you want to use:")
        for img in sorted(extra)[:10]:
            print(f"     - {img}")
        if len(extra) > 10:
            print(f"     ... and {len(extra) - 10} more")
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"✅ Ready to add: {len(matches)} images")
    print(f"❌ Still needed: {len(missing)} images")
    print(f"📦 Extra found: {len(extra)} images")
    
    if matches:
        print(f"\n💡 Next step: Add the {len(matches)} matched images to Xcode Assets!")
        print(f"   See ADD_IMAGES_TO_XCODE.md for instructions")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        image_folder = sys.argv[1]
    else:
        # Default: check current directory
        image_folder = "."
        print("No folder specified. Checking current directory...")
        print("Usage: python3 validate_images.py /path/to/your/images\n")
    
    validate_images(image_folder)
