#!/usr/bin/env python3
"""
Fantasy Avatar Generator - High Quality Version
Uses SVG-based rendering for beautiful fantasy-style avatars
Click anywhere or press R to generate a new random avatar
Press S to save the current avatar
"""

import pygame
import random
import sys
import argparse
from fantasy_render import (
    render_svg_to_surface,
    generate_background_svg,
    generate_head_svg,
    generate_expression_svg,
    generate_headwear_svg,
    generate_necklace_svg,
    generate_earrings_svg,
    generate_clothes_svg,
    CAIRO_AVAILABLE
)

# Global variables
current_avatar = {}
random_seed = None

# Avatar component options
GENDERS = ["male", "female"]
RACES = ["human", "orc", "elf", "dwarf", "goblin"]
SKIN_COLORS = [
    (120, 180, 120),  # Green (orc/goblin)
    (255, 220, 177),  # Light (elf/human)
    (210, 140, 100),  # Tan (dwarf/human)
    (180, 255, 180),  # Light green
    (200, 200, 240),  # Pale blue
    (255, 200, 150),  # Peach (human)
    (245, 210, 180),  # Light tan (human)
    (160, 120, 90),   # Dark tan (human)
]
EXPRESSIONS = ["handsome", "serious", "cute", "goofy"]
HEADWEAR = ["horn_helmet", "flower_crown", "wizard_hat", "tentacle_hat", "headband", "none"]
NECKLACES = ["skull_pendant", "gem_collar", "leaf_necklace", "rune_pendant", "none"]
EARRINGS = ["hoop", "feather", "bone", "stud", "none"]
CLOTHES = ["robe", "armor", "tunic", "cloak", "hoodie"]
BACKGROUNDS = ["solid_purple", "solid_blue", "solid_pink", "gradient_sunset", "gradient_ocean", "pattern_stars", "pattern_dots"]

# Screen dimensions
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512


def random_choice(lst):
    """Helper function to pick random item from list"""
    return random.choice(lst)


def generate_avatar(screen):
    """Generate and render a complete fantasy avatar"""
    global current_avatar
    
    # Randomly select components
    current_avatar = {
        "gender": random_choice(GENDERS),
        "race": random_choice(RACES),
        "skin_color": random_choice(SKIN_COLORS),
        "expression": random_choice(EXPRESSIONS),
        "headwear": random_choice(HEADWEAR),
        "necklace": random_choice(NECKLACES),
        "earring": random_choice(EARRINGS),
        "clothes": random_choice(CLOTHES),
        "background": random_choice(BACKGROUNDS)
    }
    
    # Generate a unique key for this avatar combination
    avatar_key = f"{current_avatar['race']}_{current_avatar['expression']}_{current_avatar['headwear']}_{random.randint(0, 9999)}"
    
    # Render each component as SVG and composite
    # Background
    bg_svg = generate_background_svg(current_avatar["background"])
    bg_surface = render_svg_to_surface(f"bg_{current_avatar['background']}", bg_svg)
    screen.blit(bg_surface, (0, 0))
    
    # Clothes (behind head)
    clothes_svg = generate_clothes_svg(current_avatar["clothes"], current_avatar["skin_color"])
    clothes_surface = render_svg_to_surface(f"clothes_{current_avatar['clothes']}_{avatar_key}", clothes_svg)
    screen.blit(clothes_surface, (0, 0))
    
    # Head
    head_svg = generate_head_svg(current_avatar["race"], current_avatar["skin_color"])
    head_surface = render_svg_to_surface(f"head_{current_avatar['race']}_{avatar_key}", head_svg)
    screen.blit(head_surface, (0, 0))
    
    # Expression
    expr_svg = generate_expression_svg(current_avatar["expression"])
    expr_surface = render_svg_to_surface(f"expr_{current_avatar['expression']}_{avatar_key}", expr_svg)
    screen.blit(expr_surface, (0, 0))
    
    # Earrings
    earring_svg = generate_earrings_svg(current_avatar["earring"])
    earring_surface = render_svg_to_surface(f"earring_{current_avatar['earring']}_{avatar_key}", earring_svg)
    screen.blit(earring_surface, (0, 0))
    
    # Necklace
    necklace_svg = generate_necklace_svg(current_avatar["necklace"])
    necklace_surface = render_svg_to_surface(f"necklace_{current_avatar['necklace']}_{avatar_key}", necklace_svg)
    screen.blit(necklace_surface, (0, 0))
    
    # Headwear (on top)
    headwear_svg = generate_headwear_svg(current_avatar["headwear"], current_avatar["race"])
    headwear_surface = render_svg_to_surface(f"headwear_{current_avatar['headwear']}_{avatar_key}", headwear_svg)
    screen.blit(headwear_surface, (0, 0))
    
    # Print avatar info
    print(f"\n=== Generated Avatar ===")
    print(f"Race: {current_avatar['race']}")
    print(f"Expression: {current_avatar['expression']}")
    print(f"Headwear: {current_avatar['headwear']}")
    print(f"Clothes: {current_avatar['clothes']}")
    print(f"Accessories: {current_avatar['earring']}, {current_avatar['necklace']}")
    print(f"======================\n")


def main():
    """Main application loop"""
    global random_seed
    
    # Check if cairosvg is available
    if not CAIRO_AVAILABLE:
        print("\n" + "="*60)
        print("WARNING: cairosvg is not installed!")
        print("To get high-quality SVG rendering, please install it:")
        print("    pip install cairosvg")
        print("\nThe generator will run in fallback mode with basic rendering.")
        print("="*60 + "\n")
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Fantasy Avatar Generator - High Quality')
    parser.add_argument('--seed', type=int, help='Random seed for reproducible generation')
    args = parser.parse_args()
    
    # Set random seed if provided
    if args.seed is not None:
        random_seed = args.seed
        random.seed(random_seed)
        print(f"Using random seed: {random_seed}")
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Fantasy Avatar Generator HQ - Press R to generate, S to save')
    clock = pygame.time.Clock()
    
    # Generate initial avatar
    generate_avatar(screen)
    
    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                generate_avatar(screen)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    generate_avatar(screen)
                elif event.key == pygame.K_s:
                    # Save screenshot
                    import os
                    os.makedirs("output", exist_ok=True)
                    timestamp = pygame.time.get_ticks()
                    filename = f"output/avatar_hq_{timestamp}.png"
                    pygame.image.save(screen, filename)
                    print(f"✓ Saved avatar to {filename}")
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit(0)


if __name__ == '__main__':
    main()
