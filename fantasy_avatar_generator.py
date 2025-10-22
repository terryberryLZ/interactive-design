#!/usr/bin/env python3
"""
Fantasy Pixel Avatar Generator - Standalone pygame version
Click anywhere or press R to generate a new random avatar
Supports --seed parameter for reproducible generation
Can be packaged as a Windows .exe with PyInstaller
"""

import pygame
import random
import sys
import argparse

# Global variables for avatar components
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

# Pixel size for drawing (4 pixels = 1 logical pixel, for 512x512 output from 128x128 logical)
PIXEL = 4

# Screen dimensions
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512


def random_choice(lst):
    """Helper function to pick random item from list"""
    return random.choice(lst)


def lerp(a, b, t):
    """Linear interpolation between a and b"""
    return a + (b - a) * t


def draw_rect(surface, color, x, y, w=PIXEL, h=PIXEL):
    """Draw a rectangle on the surface"""
    pygame.draw.rect(surface, color, (x, y, w, h))


def draw_background(surface, bg_type):
    """Draw background"""
    if bg_type == "solid_purple":
        surface.fill((180, 160, 200))
    elif bg_type == "solid_blue":
        surface.fill((160, 180, 210))
    elif bg_type == "solid_pink":
        surface.fill((240, 200, 220))
    elif bg_type == "gradient_sunset":
        # Orange to purple gradient
        for i in range(128):
            t = float(i) / 128
            r = int(lerp(255, 150, t))
            g = int(lerp(180, 100, t))
            b = int(lerp(100, 180, t))
            for j in range(128):
                draw_rect(surface, (r, g, b), j * PIXEL, i * PIXEL)
    elif bg_type == "gradient_ocean":
        # Light blue to dark blue gradient
        for i in range(128):
            t = float(i) / 128
            r = int(lerp(200, 60, t))
            g = int(lerp(220, 100, t))
            b = int(lerp(255, 180, t))
            for j in range(128):
                draw_rect(surface, (r, g, b), j * PIXEL, i * PIXEL)
    elif bg_type == "pattern_stars":
        # Dark background with stars
        surface.fill((40, 40, 70))
        for i in range(20):
            x = random.randint(0, 127) * PIXEL
            y = random.randint(0, 127) * PIXEL
            draw_rect(surface, (255, 255, 200), x, y)
    elif bg_type == "pattern_dots":
        # Light background with dots
        surface.fill((230, 230, 250))
        for i in range(0, 128, 8):
            for j in range(0, 128, 8):
                if (i + j) % 16 == 0:
                    draw_rect(surface, (200, 200, 230), i * PIXEL, j * PIXEL)


def draw_head(surface, race, skin_col):
    """Draw the head/face based on race"""
    x_center = 256
    y_center = 224
    
    if race == "human":
        # Balanced, round head
        for i in range(7, 13):
            for j in range(4, 12):
                draw_rect(surface, skin_col, x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL)
        # Normal ears
        draw_rect(surface, skin_col, x_center - 64, y_center + 4, PIXEL * 2, PIXEL * 3)
        draw_rect(surface, skin_col, x_center + 56, y_center + 4, PIXEL * 2, PIXEL * 3)
    
    elif race == "orc":
        # Broad, square head
        for i in range(6, 14):
            for j in range(3, 13):
                draw_rect(surface, skin_col, x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL)
        # Tusks
        draw_rect(surface, (255, 255, 220), x_center - 40, y_center + 20, PIXEL * 2, PIXEL * 3)
        draw_rect(surface, (255, 255, 220), x_center + 32, y_center + 20, PIXEL * 2, PIXEL * 3)
        
    elif race == "elf":
        # Elegant, oval head
        for i in range(7, 13):
            for j in range(4, 12):
                draw_rect(surface, skin_col, x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL)
        # Pointed ears
        draw_rect(surface, skin_col, x_center - 72, y_center, PIXEL * 2, PIXEL * 2)
        draw_rect(surface, skin_col, x_center - 88, y_center - 8, PIXEL * 2, PIXEL * 2)
        draw_rect(surface, skin_col, x_center + 64, y_center, PIXEL * 2, PIXEL * 2)
        draw_rect(surface, skin_col, x_center + 80, y_center - 8, PIXEL * 2, PIXEL * 2)
        
    elif race == "dwarf":
        # Stocky, round head with beard
        for i in range(7, 13):
            for j in range(5, 11):
                draw_rect(surface, skin_col, x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL)
        # Beard
        for i in range(7, 13):
            for j in range(10, 14):
                draw_rect(surface, (100, 60, 30), x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL)
                
    elif race == "goblin":
        # Small, pointy head
        for i in range(7, 13):
            for j in range(5, 12):
                draw_rect(surface, skin_col, x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL)
        # Large ears
        draw_rect(surface, skin_col, x_center - 72, y_center + 8, PIXEL * 2, PIXEL * 3)
        draw_rect(surface, skin_col, x_center + 64, y_center + 8, PIXEL * 2, PIXEL * 3)
    
    # Draw eyes (all races)
    draw_rect(surface, (255, 255, 255), x_center - 32, y_center + 8, PIXEL * 3, PIXEL * 2)
    draw_rect(surface, (255, 255, 255), x_center + 16, y_center + 8, PIXEL * 3, PIXEL * 2)
    draw_rect(surface, (0, 0, 0), x_center - 24, y_center + 8, PIXEL, PIXEL)
    draw_rect(surface, (0, 0, 0), x_center + 24, y_center + 8, PIXEL, PIXEL)


def draw_expression(surface, expression):
    """Draw facial expression"""
    x_center = 256
    y_center = 224
    
    if expression == "handsome":
        # Confident smile with raised eyebrows
        draw_rect(surface, (0, 0, 0), x_center - 16, y_center + 32, PIXEL * 4, PIXEL)
        draw_rect(surface, (0, 0, 0), x_center - 24, y_center + 24, PIXEL, PIXEL)
        draw_rect(surface, (0, 0, 0), x_center + 16, y_center + 24, PIXEL, PIXEL)
        # Raised eyebrows
        draw_rect(surface, (0, 0, 0), x_center - 40, y_center - 4, PIXEL * 3, PIXEL)
        draw_rect(surface, (0, 0, 0), x_center + 24, y_center - 4, PIXEL * 3, PIXEL)
        
    elif expression == "serious":
        # Straight mouth with stern eyebrows
        draw_rect(surface, (0, 0, 0), x_center - 16, y_center + 32, PIXEL * 4, PIXEL)
        # Furrowed eyebrows
        draw_rect(surface, (0, 0, 0), x_center - 40, y_center, PIXEL * 3, PIXEL)
        draw_rect(surface, (0, 0, 0), x_center + 24, y_center, PIXEL * 3, PIXEL)
        
    elif expression == "cute":
        # Round mouth
        draw_rect(surface, (255, 150, 150), x_center - 8, y_center + 28, PIXEL * 2, PIXEL * 2)
        # Blush
        draw_rect(surface, (255, 180, 180), x_center - 48, y_center + 24, PIXEL * 2, PIXEL)
        draw_rect(surface, (255, 180, 180), x_center + 40, y_center + 24, PIXEL * 2, PIXEL)
        
    elif expression == "goofy":
        # Tongue out with one eye closed
        draw_rect(surface, (255, 100, 120), x_center - 8, y_center + 32, PIXEL * 2, PIXEL * 2)
        # One eye wink
        draw_rect(surface, (0, 0, 0), x_center - 32, y_center + 8, PIXEL * 3, PIXEL)
        # Silly raised eyebrow on other side
        draw_rect(surface, (0, 0, 0), x_center + 24, y_center - 4, PIXEL * 3, PIXEL)


def draw_headwear(surface, headwear_type, race):
    """Draw headwear"""
    x_center = 256
    y_center = 224
    
    if headwear_type == "headband":
        # Simple headband
        for i in range(7, 13):
            draw_rect(surface, (200, 150, 100), x_center - 80 + i * PIXEL, y_center - 16)
        # Small decoration
        draw_rect(surface, (255, 200, 100), x_center - 4, y_center - 16)
    
    elif headwear_type == "horn_helmet":
        # Metal helmet
        for i in range(7, 13):
            for j in range(3, 6):
                draw_rect(surface, (150, 150, 150), x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL)
        # Horns
        draw_rect(surface, (240, 240, 220), x_center - 64, y_center - 40, PIXEL * 2, PIXEL * 4)
        draw_rect(surface, (240, 240, 220), x_center + 56, y_center - 40, PIXEL * 2, PIXEL * 4)
        draw_rect(surface, (240, 240, 220), x_center - 72, y_center - 56, PIXEL * 2, PIXEL * 2)
        draw_rect(surface, (240, 240, 220), x_center + 64, y_center - 56, PIXEL * 2, PIXEL * 2)
        
    elif headwear_type == "flower_crown":
        # Flowers
        draw_rect(surface, (255, 100, 150), x_center - 48, y_center - 32, PIXEL * 2, PIXEL * 2)
        draw_rect(surface, (255, 200, 100), x_center - 16, y_center - 40, PIXEL * 2, PIXEL * 2)
        draw_rect(surface, (150, 100, 255), x_center + 24, y_center - 32, PIXEL * 2, PIXEL * 2)
        # Leaves
        for i in range(7, 13):
            draw_rect(surface, (100, 200, 100), x_center - 80 + i * PIXEL, y_center - 24)
            
    elif headwear_type == "wizard_hat":
        # Tall pointed hat
        # Brim
        for i in range(6, 14):
            draw_rect(surface, (50, 50, 120), x_center - 80 + i * PIXEL, y_center - 24)
        # Cone
        for i in range(8, 12):
            for j in range(5, 12):
                if j < 9 - abs(i - 10):
                    draw_rect(surface, (50, 50, 120), x_center - 80 + i * PIXEL, y_center - 40 - j * PIXEL)
        # Star decoration
        draw_rect(surface, (255, 255, 100), x_center - 8, y_center - 64)
        
    elif headwear_type == "tentacle_hat":
        # Octopus-like hat
        # Main body
        for i in range(7, 13):
            for j in range(3, 6):
                draw_rect(surface, (200, 100, 200), x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL)
        # Tentacles
        draw_rect(surface, (200, 100, 200), x_center - 56, y_center - 16, PIXEL, PIXEL * 3)
        draw_rect(surface, (200, 100, 200), x_center - 32, y_center - 24, PIXEL, PIXEL * 3)
        draw_rect(surface, (200, 100, 200), x_center + 24, y_center - 24, PIXEL, PIXEL * 3)
        draw_rect(surface, (200, 100, 200), x_center + 48, y_center - 16, PIXEL, PIXEL * 3)


def draw_necklace(surface, necklace_type):
    """Draw necklace"""
    x_center = 256
    y_center = 224
    
    if necklace_type == "rune_pendant":
        # Chain
        for i in range(8, 12):
            draw_rect(surface, (150, 150, 170), x_center - 80 + i * PIXEL, y_center + 64)
        # Glowing rune
        draw_rect(surface, (100, 200, 255), x_center - 16, y_center + 72, PIXEL * 4, PIXEL * 3)
        draw_rect(surface, (200, 230, 255), x_center - 8, y_center + 76)
    
    elif necklace_type == "skull_pendant":
        # Chain
        for i in range(8, 12):
            draw_rect(surface, (200, 200, 200), x_center - 80 + i * PIXEL, y_center + 64)
        # Skull
        draw_rect(surface, (240, 240, 230), x_center - 16, y_center + 72, PIXEL * 4, PIXEL * 3)
        draw_rect(surface, (0, 0, 0), x_center - 8, y_center + 72)
        draw_rect(surface, (0, 0, 0), x_center + 8, y_center + 72)
        
    elif necklace_type == "gem_collar":
        # Gold collar
        for i in range(7, 13):
            draw_rect(surface, (255, 215, 0), x_center - 80 + i * PIXEL, y_center + 64)
        # Gems
        draw_rect(surface, (255, 50, 50), x_center - 32, y_center + 64)
        draw_rect(surface, (50, 50, 255), x_center, y_center + 64)
        draw_rect(surface, (50, 255, 50), x_center + 24, y_center + 64)
        
    elif necklace_type == "leaf_necklace":
        # Vine
        for i in range(8, 12):
            draw_rect(surface, (100, 150, 80), x_center - 80 + i * PIXEL, y_center + 64)
        # Leaves
        draw_rect(surface, (120, 200, 100), x_center - 24, y_center + 72, PIXEL * 2, PIXEL * 2)
        draw_rect(surface, (120, 200, 100), x_center + 8, y_center + 72, PIXEL * 2, PIXEL * 2)


def draw_earrings(surface, earring_type):
    """Draw earrings"""
    x_center = 256
    y_center = 224
    
    if earring_type == "stud":
        # Small stud earrings
        draw_rect(surface, (255, 215, 0), x_center - 64, y_center + 16)
        draw_rect(surface, (255, 215, 0), x_center + 56, y_center + 16)
        # Shine effect
        draw_rect(surface, (255, 255, 200), x_center - 64, y_center + 16, PIXEL // 2, PIXEL // 2)
        draw_rect(surface, (255, 255, 200), x_center + 56, y_center + 16, PIXEL // 2, PIXEL // 2)
    
    elif earring_type == "hoop":
        # Gold hoops
        draw_rect(surface, (255, 215, 0), x_center - 64, y_center + 16, PIXEL, PIXEL * 3)
        draw_rect(surface, (255, 215, 0), x_center + 56, y_center + 16, PIXEL, PIXEL * 3)
        draw_rect(surface, (255, 215, 0), x_center - 72, y_center + 24)
        draw_rect(surface, (255, 215, 0), x_center + 64, y_center + 24)
        
    elif earring_type == "feather":
        # Feather earrings
        draw_rect(surface, (100, 200, 200), x_center - 64, y_center + 16, PIXEL, PIXEL * 4)
        draw_rect(surface, (100, 200, 200), x_center + 56, y_center + 16, PIXEL, PIXEL * 4)
        draw_rect(surface, (100, 200, 200), x_center - 72, y_center + 24, PIXEL, PIXEL * 2)
        draw_rect(surface, (100, 200, 200), x_center + 64, y_center + 24, PIXEL, PIXEL * 2)
        
    elif earring_type == "bone":
        # Bone earrings
        draw_rect(surface, (240, 240, 220), x_center - 64, y_center + 16, PIXEL * 2, PIXEL * 3)
        draw_rect(surface, (240, 240, 220), x_center + 56, y_center + 16, PIXEL * 2, PIXEL * 3)


def draw_clothes(surface, clothes_type, skin_col):
    """Draw clothing/armor"""
    x_center = 256
    y_center = 224
    
    if clothes_type == "hoodie":
        # Modern hoodie
        for i in range(6, 14):
            for j in range(13, 20):
                draw_rect(surface, (80, 80, 100), x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL)
        # Hood
        for i in range(7, 13):
            for j in range(3, 5):
                draw_rect(surface, (80, 80, 100), x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL)
        # Drawstrings
        draw_rect(surface, (200, 200, 200), x_center - 16, y_center + 28, PIXEL, PIXEL * 2)
        draw_rect(surface, (200, 200, 200), x_center + 8, y_center + 28, PIXEL, PIXEL * 2)
    
    elif clothes_type == "robe":
        # Flowing robe
        for i in range(6, 14):
            for j in range(13, 20):
                draw_rect(surface, (80, 60, 140), x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL)
        # Belt
        for i in range(7, 13):
            draw_rect(surface, (150, 100, 50), x_center - 80 + i * PIXEL, y_center + 48)
            
    elif clothes_type == "armor":
        # Plate armor
        for i in range(7, 13):
            for j in range(13, 19):
                draw_rect(surface, (180, 180, 200), x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL)
        # Armor details
        for i in range(8, 12):
            draw_rect(surface, (120, 120, 140), x_center - 80 + i * PIXEL, y_center + 40)
            
    elif clothes_type == "tunic":
        # Simple tunic
        for i in range(7, 13):
            for j in range(13, 19):
                draw_rect(surface, (150, 100, 60), x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL)
        # Collar
        for i in range(8, 12):
            draw_rect(surface, skin_col, x_center - 80 + i * PIXEL, y_center + 24)
            
    elif clothes_type == "cloak":
        # Mysterious cloak
        # Shoulders
        for i in range(6, 14):
            for j in range(12, 20):
                if i < 8 or i > 11:
                    draw_rect(surface, (40, 40, 60), x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL)
        # Center
        for i in range(8, 12):
            for j in range(13, 19):
                draw_rect(surface, (40, 40, 60), x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL)
        # Clasp
        draw_rect(surface, (255, 215, 0), x_center - 8, y_center + 24, PIXEL * 2, PIXEL)


def generate_avatar(surface):
    """Generate random avatar components and draw"""
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
    
    # Draw background first
    draw_background(surface, current_avatar["background"])
    
    # Draw avatar components in order (back to front)
    draw_clothes(surface, current_avatar["clothes"], current_avatar["skin_color"])
    draw_head(surface, current_avatar["race"], current_avatar["skin_color"])
    draw_expression(surface, current_avatar["expression"])
    draw_earrings(surface, current_avatar["earring"])
    draw_necklace(surface, current_avatar["necklace"])
    draw_headwear(surface, current_avatar["headwear"], current_avatar["race"])


def main():
    """Main game loop"""
    global random_seed
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Fantasy Pixel Avatar Generator')
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
    pygame.display.set_caption('Fantasy Pixel Avatar Generator - Press R or Click to generate')
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
                    timestamp = pygame.time.get_ticks()
                    filename = f"avatar_{timestamp}.png"
                    pygame.image.save(screen, filename)
                    print(f"Saved avatar to {filename}")
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit(0)


if __name__ == '__main__':
    main()
