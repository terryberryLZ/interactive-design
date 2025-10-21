#!/usr/bin/env python3
"""
Test script to generate sample avatars automatically
"""

import pygame
from pixel_avatar_generator import PixelCanvas, ColorPalette, AvatarGenerator, LOGICAL_WIDTH, LOGICAL_HEIGHT

# Initialize pygame (headless mode)
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.init()

def generate_sample_avatars(count=5):
    """Generate sample avatars with different seeds"""
    palette = ColorPalette()
    canvas = PixelCanvas(LOGICAL_WIDTH, LOGICAL_HEIGHT)
    
    print(f"Generating {count} sample avatars...")
    
    for i in range(count):
        # Use seed for reproducibility
        generator = AvatarGenerator(palette, seed=i * 100)
        generator.generate_random()
        generator.draw(canvas)
        
        # Save at 1x
        filename_1x = f"sample_avatar_{i+1}.png"
        canvas.save_png(filename_1x, scale=1)
        
        # Save at 4x
        filename_4x = f"sample_avatar_{i+1}_4x.png"
        canvas.save_png(filename_4x, scale=4)
        
        print(f"  Generated: {filename_1x} and {filename_4x}")
        print(f"    Config: {generator.config}")
    
    print(f"\n✓ Successfully generated {count} sample avatars")

if __name__ == "__main__":
    generate_sample_avatars(5)
    pygame.quit()
