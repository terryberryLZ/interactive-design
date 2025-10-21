#!/usr/bin/env python3
"""
Create a showcase image with multiple sample avatars
"""

import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'

import pygame
from pixel_avatar_generator import PixelCanvas, ColorPalette, AvatarGenerator, LOGICAL_WIDTH, LOGICAL_HEIGHT

pygame.init()

def create_showcase(rows=2, cols=4):
    """Create a showcase with multiple avatars in a grid"""
    
    palette = ColorPalette()
    canvas = PixelCanvas(LOGICAL_WIDTH, LOGICAL_HEIGHT)
    
    # Create a larger canvas for the grid
    grid_width = cols * LOGICAL_WIDTH
    grid_height = rows * LOGICAL_HEIGHT
    grid_surface = pygame.Surface((grid_width, grid_height))
    grid_surface.fill((240, 240, 250))  # Light background
    
    print(f"Creating {rows}×{cols} showcase ({grid_width}×{grid_height})...")
    
    avatar_count = 0
    for row in range(rows):
        for col in range(cols):
            # Generate avatar with different seed for variety
            seed = avatar_count * 123 + 42
            generator = AvatarGenerator(palette, seed=seed)
            generator.generate_random()
            generator.draw(canvas)
            
            # Blit to grid
            x = col * LOGICAL_WIDTH
            y = row * LOGICAL_HEIGHT
            grid_surface.blit(canvas.surface, (x, y))
            
            avatar_count += 1
            print(f"  Avatar {avatar_count}: {generator.config['hair_style']}, {generator.config['clothing']}, {generator.config['accessory']}")
    
    # Save at 1x and 4x
    pygame.image.save(grid_surface, "enhanced_avatar_showcase.png")
    
    # Scale up 4x
    scaled = pygame.transform.scale(
        grid_surface,
        (grid_width * 4, grid_height * 4)
    )
    pygame.image.save(scaled, "enhanced_avatar_showcase_4x.png")
    
    print(f"\n✓ Saved showcase images")
    print(f"  - enhanced_avatar_showcase.png ({grid_width}×{grid_height})")
    print(f"  - enhanced_avatar_showcase_4x.png ({grid_width*4}×{grid_height*4})")

if __name__ == "__main__":
    create_showcase(rows=2, cols=4)
    pygame.quit()
