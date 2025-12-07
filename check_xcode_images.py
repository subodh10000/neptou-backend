#!/usr/bin/env python3
"""
Check Xcode Assets Images
==========================
Validates images added to Xcode Assets.xcassets against expected images
"""

import json
import os
from pathlib import Path

def check_xcode_images(assets_path):
    """Check images in Xcode Assets.xcassets"""
    
    # Load expected images
    with open('image_mapping.json', 'r', encoding='utf-8') as f:
        mapping = json.load(f)
    
    # Collect all expected image names (without extension)
    expected_images = set()
    
    # Places
    for place_id, images in mapping['places'].items():
        for img in images:
            name_without_ext = os.path.splitext(img)[0]
            expected_images.add(name_without_ext)
    
    # Foods
    for img in mapping['foods']:
        name_without_ext = os.path.splitext(img)[0]
        expected_images.add(name_without_ext)
    
    # Guides
    for img in mapping['guides']:
        name_without_ext = os.path.splitext(img)[0]
        expected_images.add(name_without_ext)
    
    print("=" * 80)
    print("XCODE ASSETS VALIDATION")
    print("=" * 80)
    print(f"\nExpected images: {len(expected_images)}")
    
    # Find all image sets in Assets.xcassets
    if not os.path.exists(assets_path):
        print(f"\n❌ Assets path not found: {assets_path}")
        return
    
    image_sets = []
    for root, dirs, files in os.walk(assets_path):
        for dir_name in dirs:
            if dir_name.endswith('.imageset'):
                image_set_name = dir_name.replace('.imageset', '')
                image_sets.append(image_set_name)
    
    print(f"Found image sets in Xcode: {len(image_sets)}")
    
    # Match images
    matched = []
    missing = []
    extra = []
    
    for expected in sorted(expected_images):
        if expected in image_sets:
            matched.append(expected)
        else:
            # Check case-insensitive
            found_match = None
            for found in image_sets:
                if found.lower() == expected.lower():
                    found_match = found
                    break
            
            if found_match:
                print(f"⚠️  Case mismatch: Expected '{expected}', found '{found_match}'")
                matched.append(expected)
            else:
                missing.append(expected)
    
    # Find extra images
    for found in image_sets:
        if found not in expected_images:
            # Check case-insensitive
            is_expected = any(found.lower() == exp.lower() for exp in expected_images)
            if not is_expected and found not in ['AppIcon', 'AccentColor']:
                extra.append(found)
    
    # Print results
    print("\n" + "=" * 80)
    print("VALIDATION RESULTS")
    print("=" * 80)
    
    print(f"\n✅ Matched images: {len(matched)}")
    if matched:
        print(f"   Examples: {', '.join(sorted(matched)[:10])}")
        if len(matched) > 10:
            print(f"   ... and {len(matched) - 10} more")
    
    print(f"\n❌ Missing images: {len(missing)}")
    if missing:
        print(f"   First 20 missing:")
        for img in sorted(missing)[:20]:
            print(f"     - {img}")
        if len(missing) > 20:
            print(f"     ... and {len(missing) - 20} more")
    
    if extra:
        print(f"\n📦 Extra images (not in mapping): {len(extra)}")
        print(f"   These are in Xcode but not expected:")
        for img in sorted(extra)[:10]:
            print(f"     - {img}")
        if len(extra) > 10:
            print(f"     ... and {len(extra) - 10} more")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ Correctly added: {len(matched)}/{len(expected_images)} images ({len(matched)*100//len(expected_images) if expected_images else 0}%)")
    print(f"❌ Still missing: {len(missing)} images")
    
    if len(matched) > 0:
        print(f"\n🎉 Great! You've added {len(matched)} images successfully!")
        if len(missing) > 0:
            print(f"   You can add the remaining {len(missing)} images later.")
    
    # Check for common issues
    print("\n" + "=" * 80)
    print("COMMON ISSUES CHECK")
    print("=" * 80)
    
    # Check for main images
    main_images = [img for img in expected_images if img.endswith('_main')]
    main_found = [img for img in matched if img.endswith('_main')]
    print(f"\nMain images (ending with '_main'):")
    print(f"  Expected: {len(main_images)}, Found: {len(main_found)}")
    
    # Check essential images
    essential = ['pashupatinath_main', 'boudhanath_main', 'swayambhunath_main', 
                'momo', 'dal_bhat', 'guide1']
    essential_found = [img for img in essential if img in matched]
    print(f"\nEssential images:")
    for img in essential:
        status = "✅" if img in matched else "❌"
        print(f"  {status} {img}")

if __name__ == "__main__":
    import sys
    
    # Default path to Assets.xcassets
    assets_path = "/Users/subodhkathayat/Desktop/hackathon/Neptou/Neptou/Assets.xcassets"
    
    if len(sys.argv) > 1:
        assets_path = sys.argv[1]
    
    check_xcode_images(assets_path)
