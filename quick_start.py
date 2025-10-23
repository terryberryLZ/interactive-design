"""
Quick Start Demo - Fantasy Avatar Generator V2

This script demonstrates:
1. Asset loading status
2. Fallback mode vs Asset mode
3. Basic usage examples
"""

import os
from pathlib import Path

def check_assets():
    """Check what assets are available"""
    assets_dir = Path("assets")
    
    print("=" * 60)
    print("Fantasy Avatar Generator V2 - Asset Check")
    print("=" * 60)
    
    categories = ["hats", "hair", "clothes", "accessories", "backgrounds"]
    
    total_assets = 0
    for category in categories:
        cat_dir = assets_dir / category
        if cat_dir.exists():
            png_files = list(cat_dir.glob("*.png"))
            count = len(png_files)
            total_assets += count
            
            status = "✅" if count > 0 else "⚠️"
            print(f"{status} {category.capitalize():15} : {count} assets")
            
            if count > 0 and count <= 3:
                for f in png_files:
                    print(f"   - {f.name}")
        else:
            print(f"⚠️ {category.capitalize():15} : Folder not found")
    
    print("=" * 60)
    print(f"Total assets: {total_assets}")
    print("=" * 60)
    
    if total_assets == 0:
        print("\n⚠️  No assets found - Generator will use FALLBACK mode")
        print("\nTo add AI-generated assets:")
        print("1. Read: ASSET_GENERATION_GUIDE.md")
        print("2. Generate fantasy art with Leonardo.ai or similar")
        print("3. Add PNG files (512x512, transparent) to assets/ folders")
        print("4. Restart the generator\n")
    else:
        print(f"\n✅ Found {total_assets} assets - Generator will use ASSET mode")
        print("The more assets you add, the more variety in generated avatars!\n")
    
    return total_assets


def show_usage():
    """Show usage instructions"""
    print("\n" + "=" * 60)
    print("How to Run:")
    print("=" * 60)
    print("\nClassic Generator (pixel art):")
    print("  python fantasy_avatar_generator.py")
    print("\nV2 Asset-Based Generator (with AI modules):")
    print("  python fantasy_avatar_generator_v2.py")
    print("\nControls:")
    print("  - Click or press R: Generate new avatar")
    print("  - Press S: Save avatar to output/ folder")
    print("  - Press ESC: Quit")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asset_count = check_assets()
    show_usage()
    
    # Offer to run the generator
    print("Ready to run? Choose an option:")
    print("1. Run Classic Generator (no assets needed)")
    print("2. Run V2 Asset Generator (uses assets if available)")
    print("3. Exit")
    
    try:
        choice = input("\nYour choice (1/2/3): ").strip()
        
        if choice == "1":
            print("\nStarting Classic Generator...")
            os.system("python fantasy_avatar_generator.py")
        elif choice == "2":
            print("\nStarting V2 Asset Generator...")
            os.system("python fantasy_avatar_generator_v2.py")
        else:
            print("\nExiting. Happy generating! 🎨")
    except KeyboardInterrupt:
        print("\n\nExiting. Happy generating! 🎨")
