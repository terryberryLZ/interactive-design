#!/usr/bin/env python3
"""
Demo: Batch Avatar Generation
Generate multiple avatars with specific seeds and save them

This demonstrates how to use the avatar generator programmatically
to create a gallery of avatars.
"""

import pygame
import random
from fantasy_avatar_generator import generate_avatar, SCREEN_WIDTH, SCREEN_HEIGHT


def batch_generate(num_avatars=10, output_dir="avatar_gallery"):
    """
    Generate a batch of avatars and save them
    
    Args:
        num_avatars: Number of avatars to generate
        output_dir: Directory to save avatars (will be created if it doesn't exist)
    """
    import os
    
    # Create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Batch Avatar Generator')
    
    print(f"Generating {num_avatars} avatars...")
    print(f"Output directory: {output_dir}/")
    print()
    
    for i in range(num_avatars):
        # Use a predictable seed for reproducibility
        seed = i * 100
        random.seed(seed)
        
        # Generate avatar
        generate_avatar(screen)
        
        # Save to file
        filename = f"{output_dir}/avatar_{i:03d}_seed_{seed}.png"
        pygame.image.save(screen, filename)
        
        print(f"  [{i+1}/{num_avatars}] Generated {filename}")
    
    pygame.quit()
    
    print()
    print(f"✓ Successfully generated {num_avatars} avatars!")
    print(f"  Saved to: {output_dir}/")


def generate_themed_gallery():
    """
    Generate a themed gallery with specific race/style combinations
    """
    import os
    
    output_dir = "themed_gallery"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Define themes with specific seeds that produce interesting results
    themes = [
        ("warrior_orc", 42),
        ("wise_elf", 100),
        ("grumpy_dwarf", 500),
        ("sneaky_goblin", 1000),
        ("noble_human", 123),
        ("wizard_elf", 456),
        ("tough_dwarf", 789),
        ("wild_orc", 321),
    ]
    
    print("Generating themed avatar gallery...")
    print(f"Output directory: {output_dir}/")
    print()
    
    for name, seed in themes:
        random.seed(seed)
        generate_avatar(screen)
        
        filename = f"{output_dir}/{name}.png"
        pygame.image.save(screen, filename)
        print(f"  ✓ {name} (seed {seed})")
    
    pygame.quit()
    
    print()
    print(f"✓ Themed gallery complete!")
    print(f"  Saved to: {output_dir}/")


def main():
    """Main demo function"""
    import sys
    
    print("=" * 60)
    print("Fantasy Avatar Generator - Batch Demo")
    print("=" * 60)
    print()
    
    if len(sys.argv) > 1:
        try:
            num = int(sys.argv[1])
            batch_generate(num)
        except ValueError:
            print("Error: Please provide a valid number")
            print("Usage: python demo_batch_generate.py [number]")
            sys.exit(1)
    else:
        # Default: generate themed gallery
        generate_themed_gallery()
        
        print()
        print("To generate a custom batch:")
        print("  python demo_batch_generate.py 20")


if __name__ == '__main__':
    main()
