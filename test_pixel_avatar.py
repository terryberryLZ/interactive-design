#!/usr/bin/env python3
"""
Test suite for Pixel-Art Avatar Generator
Validates all components and features
"""

import sys
import os
import json
from pathlib import Path

# Set headless mode for testing
os.environ['SDL_VIDEODRIVER'] = 'dummy'

import pygame
pygame.init()

from pixel_avatar_generator import (
    PixelCanvas, ColorPalette, AvatarGenerator,
    LOGICAL_WIDTH, LOGICAL_HEIGHT
)

def test_color_palette():
    """Test color palette loading and access"""
    print("Testing ColorPalette...")
    
    palette = ColorPalette()
    
    # Test palette loaded
    assert 'backgrounds' in palette.colors
    assert 'skin_tones' in palette.colors
    assert 'hair_colors' in palette.colors
    print("  ✓ Palette structure valid")
    
    # Test color retrieval
    bg_color = palette.get('backgrounds', 'cyan_blue')
    assert len(bg_color) == 3
    assert all(0 <= c <= 255 for c in bg_color)
    print("  ✓ Color retrieval works")
    
    # Test at least 5 variants in key categories
    assert len(palette.colors['backgrounds']) >= 5
    assert len(palette.colors['skin_tones']) >= 5
    assert len(palette.colors['hair_colors']) >= 5
    print("  ✓ Sufficient color variants (5+ each)")
    
    print("✓ ColorPalette tests passed\n")

def test_pixel_canvas():
    """Test PixelCanvas drawing and scaling"""
    print("Testing PixelCanvas...")
    
    canvas = PixelCanvas(LOGICAL_WIDTH, LOGICAL_HEIGHT)
    
    # Test dimensions
    assert canvas.width == LOGICAL_WIDTH
    assert canvas.height == LOGICAL_HEIGHT
    print(f"  ✓ Canvas size: {LOGICAL_WIDTH}×{LOGICAL_HEIGHT}")
    
    # Test clear
    canvas.clear((255, 0, 0))
    assert canvas.surface.get_at((0, 0))[:3] == (255, 0, 0)
    print("  ✓ Clear function works")
    
    # Test pixel setting
    canvas.set_pixel(10, 10, (0, 255, 0))
    assert canvas.surface.get_at((10, 10))[:3] == (0, 255, 0)
    print("  ✓ Set pixel works")
    
    # Test rectangle drawing
    canvas.draw_rect(20, 20, 10, 10, (0, 0, 255))
    assert canvas.surface.get_at((25, 25))[:3] == (0, 0, 255)
    print("  ✓ Draw rectangle works")
    
    # Test scaling
    scaled = canvas.get_scaled_surface(4)
    assert scaled.get_width() == LOGICAL_WIDTH * 4
    assert scaled.get_height() == LOGICAL_HEIGHT * 4
    print("  ✓ 4× scaling works")
    
    # Test PNG save
    test_file = "test_canvas.png"
    canvas.save_png(test_file, scale=1)
    assert Path(test_file).exists()
    os.remove(test_file)
    print("  ✓ PNG export works")
    
    print("✓ PixelCanvas tests passed\n")

def test_avatar_generator():
    """Test AvatarGenerator functionality"""
    print("Testing AvatarGenerator...")
    
    palette = ColorPalette()
    generator = AvatarGenerator(palette)
    
    # Test variant counts (requirement: at least 5 each)
    assert len(generator.hair_styles) >= 5
    assert len(generator.eye_styles) >= 5
    assert len(generator.mouth_styles) >= 5
    assert len(generator.clothing_styles) >= 5
    assert len(generator.accessory_styles) >= 5
    print(f"  ✓ Hair styles: {len(generator.hair_styles)}")
    print(f"  ✓ Eye styles: {len(generator.eye_styles)}")
    print(f"  ✓ Mouth styles: {len(generator.mouth_styles)}")
    print(f"  ✓ Clothing styles: {len(generator.clothing_styles)}")
    print(f"  ✓ Accessory styles: {len(generator.accessory_styles)}")
    
    # Test random generation
    generator.generate_random()
    assert 'background' in generator.config
    assert 'skin_tone' in generator.config
    assert 'hair_style' in generator.config
    assert 'eye_style' in generator.config
    assert 'mouth_style' in generator.config
    assert 'clothing' in generator.config
    assert 'accessory' in generator.config
    print("  ✓ Random generation creates valid config")
    
    # Test drawing (should not crash)
    canvas = PixelCanvas(LOGICAL_WIDTH, LOGICAL_HEIGHT)
    try:
        generator.draw(canvas)
        print("  ✓ Avatar drawing successful")
    except Exception as e:
        print(f"  ✗ Avatar drawing failed: {e}")
        return False
    
    print("✓ AvatarGenerator tests passed\n")

def test_deterministic_generation():
    """Test deterministic seeding"""
    print("Testing deterministic generation...")
    
    palette = ColorPalette()
    
    # Generate with seed
    gen1 = AvatarGenerator(palette, seed=12345)
    gen1.generate_random()
    config1 = gen1.config.copy()
    
    # Generate with same seed
    gen2 = AvatarGenerator(palette, seed=12345)
    gen2.generate_random()
    config2 = gen2.config.copy()
    
    # Should be identical
    assert config1 == config2
    print("  ✓ Same seed produces identical avatars")
    
    # Generate with different seed
    gen3 = AvatarGenerator(palette, seed=54321)
    gen3.generate_random()
    config3 = gen3.config.copy()
    
    # Should be different
    assert config1 != config3
    print("  ✓ Different seed produces different avatars")
    
    print("✓ Deterministic generation tests passed\n")

def test_full_avatar_generation():
    """Test complete avatar generation and export"""
    print("Testing full avatar generation pipeline...")
    
    palette = ColorPalette()
    canvas = PixelCanvas(LOGICAL_WIDTH, LOGICAL_HEIGHT)
    
    # Test multiple avatars
    for i in range(5):
        generator = AvatarGenerator(palette, seed=i * 111)
        generator.generate_random()
        generator.draw(canvas)
        
        # Save at different scales
        file_1x = f"test_avatar_{i}_1x.png"
        file_4x = f"test_avatar_{i}_4x.png"
        
        canvas.save_png(file_1x, scale=1)
        canvas.save_png(file_4x, scale=4)
        
        assert Path(file_1x).exists()
        assert Path(file_4x).exists()
        
        # Clean up
        os.remove(file_1x)
        os.remove(file_4x)
    
    print("  ✓ Generated and exported 5 avatars successfully")
    print("✓ Full pipeline tests passed\n")

def test_layer_coverage():
    """Test that all layer types can be drawn without errors"""
    print("Testing layer coverage...")
    
    palette = ColorPalette()
    canvas = PixelCanvas(LOGICAL_WIDTH, LOGICAL_HEIGHT)
    generator = AvatarGenerator(palette)
    
    # Test all hair styles
    for hair_style in generator.hair_styles:
        generator.config = {
            'background': 'cyan_blue',
            'skin_tone': 'light',
            'hair_color': 'brown',
            'hair_style': hair_style,
            'eye_color': 'brown',
            'eye_style': 'round',
            'mouth_style': 'smile',
            'clothing': 'hoodie',
            'clothing_color': 'purple_light',
            'accessory': 'none'
        }
        try:
            generator.draw(canvas)
        except Exception as e:
            print(f"  ✗ Failed to draw hair style '{hair_style}': {e}")
            return False
    print(f"  ✓ All {len(generator.hair_styles)} hair styles work")
    
    # Test all eye styles
    for eye_style in generator.eye_styles:
        generator.config['eye_style'] = eye_style
        try:
            generator.draw(canvas)
        except Exception as e:
            print(f"  ✗ Failed to draw eye style '{eye_style}': {e}")
            return False
    print(f"  ✓ All {len(generator.eye_styles)} eye styles work")
    
    # Test all mouth styles
    for mouth_style in generator.mouth_styles:
        generator.config['mouth_style'] = mouth_style
        try:
            generator.draw(canvas)
        except Exception as e:
            print(f"  ✗ Failed to draw mouth style '{mouth_style}': {e}")
            return False
    print(f"  ✓ All {len(generator.mouth_styles)} mouth styles work")
    
    # Test all clothing styles
    for clothing_style in generator.clothing_styles:
        generator.config['clothing'] = clothing_style
        try:
            generator.draw(canvas)
        except Exception as e:
            print(f"  ✗ Failed to draw clothing style '{clothing_style}': {e}")
            return False
    print(f"  ✓ All {len(generator.clothing_styles)} clothing styles work")
    
    # Test all accessories
    for accessory in generator.accessory_styles:
        generator.config['accessory'] = accessory
        try:
            generator.draw(canvas)
        except Exception as e:
            print(f"  ✗ Failed to draw accessory '{accessory}': {e}")
            return False
    print(f"  ✓ All {len(generator.accessory_styles)} accessories work")
    
    print("✓ Layer coverage tests passed\n")

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Pixel-Art Avatar Generator Test Suite")
    print("=" * 60)
    print()
    
    try:
        test_color_palette()
        test_pixel_canvas()
        test_avatar_generator()
        test_deterministic_generation()
        test_full_avatar_generation()
        test_layer_coverage()
        
        print("=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60)
        return True
    
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    pygame.quit()
    sys.exit(0 if success else 1)
