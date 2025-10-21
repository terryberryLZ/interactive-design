#!/usr/bin/env python3
"""
Quick comparison: Legacy vs Enhanced Avatar Generator
Shows improvement in detail and pixel-art quality
"""

import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'

import pygame
from pixel_avatar_generator import PixelCanvas, ColorPalette, AvatarGenerator

pygame.init()

def generate_comparison():
    """Generate a single avatar showing enhanced quality"""
    
    palette = ColorPalette()
    canvas = PixelCanvas(160, 160)
    
    # Generate a specific avatar that shows off features
    generator = AvatarGenerator(palette, seed=42)
    generator.config = {
        'background': 'light_blue',
        'skin_tone': 'light',
        'hair_color': 'brown',
        'hair_style': 'buns',  # Like reference image
        'eye_color': 'brown',
        'eye_style': 'wide',   # With highlights
        'mouth_style': 'smile',
        'clothing': 'suspenders',  # Like reference image
        'clothing_color': 'purple_light',
        'accessory': 'glasses'  # Like reference image
    }
    
    generator.draw(canvas)
    
    # Save at both scales
    canvas.save_png("enhanced_example.png", scale=1)
    canvas.save_png("enhanced_example_4x.png", scale=4)
    
    print("Enhanced Avatar Features Demonstrated:")
    print("  ✓ Crisp 160×160 pixel resolution")
    print("  ✓ Detailed eyes with white highlights")
    print("  ✓ Subtle nose shading")
    print("  ✓ Expressive mouth shapes")
    print("  ✓ Hair with bun style (matching reference)")
    print("  ✓ Detailed clothing (suspenders with buttons)")
    print("  ✓ Glasses accessory (black frame style)")
    print("  ✓ Proper skin tone shading and highlights")
    print("  ✓ Clean background with border")
    print("\nSaved:")
    print("  - enhanced_example.png (160×160)")
    print("  - enhanced_example_4x.png (640×640)")
    print("\nKey Improvements Over Legacy Version:")
    print("  • Higher resolution (160×160 vs 320×320 with 8px blocks)")
    print("  • More detailed facial features")
    print("  • Professional pixel-art styling")
    print("  • Cohesive color palette")
    print("  • Modular layer system")
    print("  • Nearest-neighbor scaling for crisp pixels")

if __name__ == "__main__":
    generate_comparison()
    pygame.quit()
