#!/usr/bin/env python3
"""
Test script to verify the HQ avatar generator dependencies
"""

import sys

def test_dependencies():
    """Test if all required dependencies are installed"""
    print("\n" + "="*60)
    print("Testing Fantasy Avatar Generator HQ Dependencies")
    print("="*60 + "\n")
    
    all_ok = True
    
    # Test pygame
    print("1. Testing pygame...")
    try:
        import pygame
        print(f"   ✓ pygame {pygame.version.ver} installed")
    except ImportError:
        print("   ✗ pygame NOT installed")
        print("     Install with: pip install pygame")
        all_ok = False
    
    # Test Pillow
    print("\n2. Testing Pillow...")
    try:
        from PIL import Image
        import PIL
        print(f"   ✓ Pillow {PIL.__version__} installed")
    except ImportError:
        print("   ✗ Pillow NOT installed")
        print("     Install with: pip install Pillow")
        all_ok = False
    
    # Test cairosvg
    print("\n3. Testing cairosvg (for SVG rendering)...")
    try:
        import cairosvg
        print(f"   ✓ cairosvg installed")
        
        # Try a simple render test
        test_svg = '<svg width="100" height="100"><rect width="100" height="100" fill="red"/></svg>'
        try:
            png_data = cairosvg.svg2png(bytestring=test_svg.encode('utf-8'))
            print("   ✓ SVG rendering test passed")
        except Exception as e:
            print(f"   ⚠ cairosvg installed but rendering failed: {e}")
            print("     You may need to install Cairo libraries")
            all_ok = False
            
    except ImportError:
        print("   ✗ cairosvg NOT installed")
        print("     Install with: pip install cairosvg")
        print("     OR on Windows: pip install pipwin && pipwin install cairocffi")
        all_ok = False
    
    print("\n" + "="*60)
    if all_ok:
        print("✓ All dependencies are installed and working!")
        print("\nYou can now run:")
        print("  python fantasy_avatar_hq.py")
        print("  python demo_batch_generate_hq.py 10")
    else:
        print("✗ Some dependencies are missing or not working.")
        print("\nTo install all dependencies:")
        print("  pip install -r requirements.txt")
        print("\nNote: The generator can still run without cairosvg,")
        print("but will use basic rendering instead of high-quality SVG.")
    print("="*60 + "\n")
    
    return all_ok


if __name__ == '__main__':
    success = test_dependencies()
    sys.exit(0 if success else 1)
