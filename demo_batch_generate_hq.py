#!/usr/bin/env python3
"""
High Quality Avatar Batch Generator
Generates a gallery of fantasy avatars using the new HQ rendering system
"""

import pygame
import random
import os
import sys
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

# Avatar component options (same as main generator)
RACES = ["human", "orc", "elf", "dwarf", "goblin"]
SKIN_COLORS = [
    (120, 180, 120),  # Green
    (255, 220, 177),  # Light
    (210, 140, 100),  # Tan
    (180, 255, 180),  # Light green
    (200, 200, 240),  # Pale blue
    (255, 200, 150),  # Peach
    (245, 210, 180),  # Light tan
    (160, 120, 90),   # Dark tan
]
EXPRESSIONS = ["handsome", "serious", "cute", "goofy"]
HEADWEAR = ["horn_helmet", "flower_crown", "wizard_hat", "tentacle_hat", "headband", "none"]
NECKLACES = ["skull_pendant", "gem_collar", "leaf_necklace", "rune_pendant", "none"]
EARRINGS = ["hoop", "feather", "bone", "stud", "none"]
CLOTHES = ["robe", "armor", "tunic", "cloak", "hoodie"]
BACKGROUNDS = ["solid_purple", "solid_blue", "solid_pink", "gradient_sunset", "gradient_ocean", "pattern_stars", "pattern_dots"]

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512


def generate_single_avatar(screen, seed=None):
    """Generate a single avatar and return its data"""
    if seed is not None:
        random.seed(seed)
    
    avatar = {
        "race": random.choice(RACES),
        "skin_color": random.choice(SKIN_COLORS),
        "expression": random.choice(EXPRESSIONS),
        "headwear": random.choice(HEADWEAR),
        "necklace": random.choice(NECKLACES),
        "earring": random.choice(EARRINGS),
        "clothes": random.choice(CLOTHES),
        "background": random.choice(BACKGROUNDS)
    }
    
    avatar_key = f"{avatar['race']}_{seed if seed else random.randint(0, 99999)}"
    
    # Render layers
    bg_svg = generate_background_svg(avatar["background"])
    bg_surface = render_svg_to_surface(f"bg_{avatar['background']}", bg_svg)
    screen.blit(bg_surface, (0, 0))
    
    clothes_svg = generate_clothes_svg(avatar["clothes"], avatar["skin_color"])
    clothes_surface = render_svg_to_surface(f"clothes_{avatar['clothes']}_{avatar_key}", clothes_svg)
    screen.blit(clothes_surface, (0, 0))
    
    head_svg = generate_head_svg(avatar["race"], avatar["skin_color"])
    head_surface = render_svg_to_surface(f"head_{avatar['race']}_{avatar_key}", head_svg)
    screen.blit(head_surface, (0, 0))
    
    expr_svg = generate_expression_svg(avatar["expression"])
    expr_surface = render_svg_to_surface(f"expr_{avatar['expression']}_{avatar_key}", expr_svg)
    screen.blit(expr_surface, (0, 0))
    
    earring_svg = generate_earrings_svg(avatar["earring"])
    earring_surface = render_svg_to_surface(f"earring_{avatar['earring']}_{avatar_key}", earring_svg)
    screen.blit(earring_surface, (0, 0))
    
    necklace_svg = generate_necklace_svg(avatar["necklace"])
    necklace_surface = render_svg_to_surface(f"necklace_{avatar['necklace']}_{avatar_key}", necklace_svg)
    screen.blit(necklace_surface, (0, 0))
    
    headwear_svg = generate_headwear_svg(avatar["headwear"], avatar["race"])
    headwear_surface = render_svg_to_surface(f"headwear_{avatar['headwear']}_{avatar_key}", headwear_svg)
    screen.blit(headwear_surface, (0, 0))
    
    return avatar


def generate_gallery(num_avatars=20, output_dir="output_hq_gallery", seed_start=1000):
    """Generate a gallery of high-quality avatars"""
    
    if not CAIRO_AVAILABLE:
        print("\nERROR: cairosvg is required for batch generation!")
        print("Install with: pip install cairosvg")
        return
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize pygame (hidden window)
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Generating HQ Avatars...')
    
    print(f"\n{'='*60}")
    print(f"Generating {num_avatars} high-quality fantasy avatars...")
    print(f"Output directory: {output_dir}")
    print(f"{'='*60}\n")
    
    avatars_data = []
    
    for i in range(num_avatars):
        seed = seed_start + i
        avatar = generate_single_avatar(screen, seed)
        
        # Save the avatar
        filename = f"{output_dir}/avatar_hq_{i+1:03d}_seed{seed}.png"
        pygame.image.save(screen, filename)
        
        avatars_data.append({
            "filename": filename,
            "seed": seed,
            **avatar
        })
        
        # Progress indicator
        progress = (i + 1) / num_avatars * 100
        bar_length = 40
        filled = int(bar_length * (i + 1) / num_avatars)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        print(f"[{bar}] {progress:5.1f}% | Avatar {i+1}/{num_avatars} | {avatar['race']} {avatar['expression']}")
    
    pygame.quit()
    
    # Save metadata
    metadata_file = f"{output_dir}/avatars_metadata.txt"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        f.write("High Quality Fantasy Avatar Gallery\n")
        f.write("="*60 + "\n\n")
        for i, avatar in enumerate(avatars_data, 1):
            f.write(f"Avatar #{i}\n")
            f.write(f"  File: {avatar['filename']}\n")
            f.write(f"  Seed: {avatar['seed']}\n")
            f.write(f"  Race: {avatar['race']}\n")
            f.write(f"  Expression: {avatar['expression']}\n")
            f.write(f"  Headwear: {avatar['headwear']}\n")
            f.write(f"  Clothes: {avatar['clothes']}\n")
            f.write(f"  Accessories: {avatar['earring']}, {avatar['necklace']}\n")
            f.write(f"  Background: {avatar['background']}\n")
            f.write("\n")
    
    print(f"\n{'='*60}")
    print(f"✓ Successfully generated {num_avatars} avatars!")
    print(f"✓ Saved to: {output_dir}/")
    print(f"✓ Metadata: {metadata_file}")
    print(f"{'='*60}\n")


def generate_themed_set(theme, output_dir, num=5):
    """Generate a themed set of avatars"""
    
    themes = {
        "warriors": {
            "clothes": ["armor"],
            "headwear": ["horn_helmet", "headband"],
            "expression": ["serious", "handsome"],
            "necklace": ["skull_pendant", "none"]
        },
        "wizards": {
            "clothes": ["robe"],
            "headwear": ["wizard_hat"],
            "expression": ["serious", "handsome"],
            "necklace": ["rune_pendant", "gem_collar"]
        },
        "elves": {
            "race": ["elf"],
            "headwear": ["flower_crown", "headband", "none"],
            "clothes": ["tunic", "robe"],
            "expression": ["cute", "handsome"]
        },
        "dwarves": {
            "race": ["dwarf"],
            "clothes": ["armor", "tunic"],
            "headwear": ["horn_helmet", "none"],
            "expression": ["serious", "goofy"]
        }
    }
    
    if theme not in themes:
        print(f"Unknown theme: {theme}")
        print(f"Available themes: {', '.join(themes.keys())}")
        return
    
    if not CAIRO_AVAILABLE:
        print("\nERROR: cairosvg is required!")
        print("Install with: pip install cairosvg")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    print(f"\nGenerating {num} {theme} avatars...\n")
    
    theme_config = themes[theme]
    
    for i in range(num):
        seed = random.randint(1000, 9999)
        random.seed(seed)
        
        # Use theme constraints
        avatar = {
            "race": random.choice(theme_config.get("race", RACES)),
            "skin_color": random.choice(SKIN_COLORS),
            "expression": random.choice(theme_config.get("expression", EXPRESSIONS)),
            "headwear": random.choice(theme_config.get("headwear", HEADWEAR)),
            "necklace": random.choice(theme_config.get("necklace", NECKLACES)),
            "earring": random.choice(EARRINGS),
            "clothes": random.choice(theme_config.get("clothes", CLOTHES)),
            "background": random.choice(BACKGROUNDS)
        }
        
        avatar_key = f"{theme}_{i}_{seed}"
        
        # Render
        bg_svg = generate_background_svg(avatar["background"])
        screen.blit(render_svg_to_surface(f"bg_{avatar['background']}", bg_svg), (0, 0))
        
        clothes_svg = generate_clothes_svg(avatar["clothes"], avatar["skin_color"])
        screen.blit(render_svg_to_surface(f"clothes_{avatar_key}", clothes_svg), (0, 0))
        
        head_svg = generate_head_svg(avatar["race"], avatar["skin_color"])
        screen.blit(render_svg_to_surface(f"head_{avatar_key}", head_svg), (0, 0))
        
        expr_svg = generate_expression_svg(avatar["expression"])
        screen.blit(render_svg_to_surface(f"expr_{avatar_key}", expr_svg), (0, 0))
        
        earring_svg = generate_earrings_svg(avatar["earring"])
        screen.blit(render_svg_to_surface(f"earring_{avatar_key}", earring_svg), (0, 0))
        
        necklace_svg = generate_necklace_svg(avatar["necklace"])
        screen.blit(render_svg_to_surface(f"necklace_{avatar_key}", necklace_svg), (0, 0))
        
        headwear_svg = generate_headwear_svg(avatar["headwear"], avatar["race"])
        screen.blit(render_svg_to_surface(f"headwear_{avatar_key}", headwear_svg), (0, 0))
        
        filename = f"{output_dir}/{theme}_{i+1:02d}_seed{seed}.png"
        pygame.image.save(screen, filename)
        
        print(f"  ✓ Generated {theme} #{i+1}: {avatar['race']} - {filename}")
    
    pygame.quit()
    print(f"\n✓ Theme '{theme}' complete! Saved to {output_dir}/\n")


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Batch generate high-quality fantasy avatars')
    parser.add_argument('num_avatars', type=int, nargs='?', default=20, help='Number of avatars to generate (default: 20)')
    parser.add_argument('--theme', type=str, help='Generate themed avatars (warriors, wizards, elves, dwarves)')
    parser.add_argument('--output', type=str, default='output_hq_gallery', help='Output directory')
    parser.add_argument('--seed', type=int, default=1000, help='Starting seed value')
    
    args = parser.parse_args()
    
    if args.theme:
        generate_themed_set(args.theme, args.output, args.num_avatars)
    else:
        generate_gallery(args.num_avatars, args.output, args.seed)


if __name__ == '__main__':
    main()
