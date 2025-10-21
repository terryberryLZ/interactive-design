#!/usr/bin/env python3
"""
Fantasy Pixel Avatar Generator - Pygame Version
Click anywhere to generate a new random avatar
Refactored from Processing Python Mode to native Python with Pygame
"""

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Global variables for avatar components
current_avatar = {}

# Avatar component options
GENDERS = ["male", "female"]
RACES = ["orc", "elf", "dwarf", "goblin"]
SKIN_COLORS = [
    (120, 180, 120),  # Green (orc/goblin)
    (255, 220, 177),  # Light (elf)
    (210, 140, 100),  # Tan (dwarf)
    (180, 255, 180),  # Light green
    (200, 200, 240),  # Pale blue
    (255, 200, 150),  # Peach
]
EXPRESSIONS = ["smile", "angry", "silly", "cute"]
HEADWEAR = ["horn_helmet", "flower_crown", "wizard_hat", "tentacle_hat", "none"]
NECKLACES = ["skull_pendant", "gem_collar", "leaf_necklace", "none"]
EARRINGS = ["hoop", "feather", "bone", "none"]
CLOTHES = ["robe", "armor", "tunic", "cloak"]

# Pixel size for drawing
PIXEL = 8

# Window settings
WINDOW_WIDTH = 320
WINDOW_HEIGHT = 320
BACKGROUND_COLOR = (240, 240, 250)

def setup():
    """Initialize the Pygame window and generate first avatar"""
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Fantasy Pixel Avatar Generator")
    return screen

def generate_avatar():
    """Generate random avatar components"""
    global current_avatar
    
    # Randomly select components
    current_avatar = {
        "gender": random.choice(GENDERS),
        "race": random.choice(RACES),
        "skin_color": random.choice(SKIN_COLORS),
        "expression": random.choice(EXPRESSIONS),
        "headwear": random.choice(HEADWEAR),
        "necklace": random.choice(NECKLACES),
        "earring": random.choice(EARRINGS),
        "clothes": random.choice(CLOTHES)
    }

def draw_avatar(screen):
    """Draw the complete avatar on the screen"""
    # Clear background
    screen.fill(BACKGROUND_COLOR)
    
    # Draw avatar components in order (back to front)
    draw_clothes(screen, current_avatar["clothes"], current_avatar["skin_color"])
    draw_head(screen, current_avatar["race"], current_avatar["skin_color"])
    draw_expression(screen, current_avatar["expression"])
    draw_earrings(screen, current_avatar["earring"])
    draw_necklace(screen, current_avatar["necklace"])
    draw_headwear(screen, current_avatar["headwear"], current_avatar["race"])
    
    # Update display
    pygame.display.flip()

# ============ Head Drawing Functions ============

def draw_head(screen, race, skin_col):
    """Draw the head/face based on race"""
    # Head is centered around x=160, y=140
    x_center = 160
    y_center = 140
    
    if race == "orc":
        # Broad, square head
        for i in range(6, 14):
            for j in range(3, 13):
                pygame.draw.rect(screen, skin_col, 
                               (x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL))
        # Tusks
        tusk_color = (255, 255, 220)
        pygame.draw.rect(screen, tusk_color, (x_center - 40, y_center + 20, PIXEL * 2, PIXEL * 3))
        pygame.draw.rect(screen, tusk_color, (x_center + 32, y_center + 20, PIXEL * 2, PIXEL * 3))
        
    elif race == "elf":
        # Elegant, oval head
        for i in range(7, 13):
            for j in range(4, 12):
                pygame.draw.rect(screen, skin_col,
                               (x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL))
        # Pointed ears
        pygame.draw.rect(screen, skin_col, (x_center - 72, y_center, PIXEL * 2, PIXEL * 2))
        pygame.draw.rect(screen, skin_col, (x_center - 88, y_center - 8, PIXEL * 2, PIXEL * 2))
        pygame.draw.rect(screen, skin_col, (x_center + 64, y_center, PIXEL * 2, PIXEL * 2))
        pygame.draw.rect(screen, skin_col, (x_center + 80, y_center - 8, PIXEL * 2, PIXEL * 2))
        
    elif race == "dwarf":
        # Stocky, round head with beard
        for i in range(7, 13):
            for j in range(5, 11):
                pygame.draw.rect(screen, skin_col,
                               (x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL))
        # Beard
        beard_color = (100, 60, 30)  # Brown beard
        for i in range(7, 13):
            for j in range(10, 14):
                pygame.draw.rect(screen, beard_color,
                               (x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL))
                
    elif race == "goblin":
        # Small, pointy head
        for i in range(7, 13):
            for j in range(5, 12):
                pygame.draw.rect(screen, skin_col,
                               (x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL))
        # Large ears
        pygame.draw.rect(screen, skin_col, (x_center - 72, y_center + 8, PIXEL * 2, PIXEL * 3))
        pygame.draw.rect(screen, skin_col, (x_center + 64, y_center + 8, PIXEL * 2, PIXEL * 3))
    
    # Draw eyes (all races)
    white = (255, 255, 255)
    black = (0, 0, 0)
    pygame.draw.rect(screen, white, (x_center - 32, y_center + 8, PIXEL * 3, PIXEL * 2))
    pygame.draw.rect(screen, white, (x_center + 16, y_center + 8, PIXEL * 3, PIXEL * 2))
    pygame.draw.rect(screen, black, (x_center - 24, y_center + 8, PIXEL, PIXEL))
    pygame.draw.rect(screen, black, (x_center + 24, y_center + 8, PIXEL, PIXEL))

def draw_expression(screen, expression):
    """Draw facial expression"""
    x_center = 160
    y_center = 140
    
    black = (0, 0, 0)
    
    if expression == "smile":
        # Happy mouth
        pygame.draw.rect(screen, black, (x_center - 16, y_center + 32, PIXEL * 4, PIXEL))
        pygame.draw.rect(screen, black, (x_center - 24, y_center + 24, PIXEL, PIXEL))
        pygame.draw.rect(screen, black, (x_center + 16, y_center + 24, PIXEL, PIXEL))
        
    elif expression == "angry":
        # Angry eyebrows
        pygame.draw.rect(screen, black, (x_center - 40, y_center, PIXEL * 3, PIXEL))
        pygame.draw.rect(screen, black, (x_center + 24, y_center, PIXEL * 3, PIXEL))
        # Frown
        pygame.draw.rect(screen, black, (x_center - 16, y_center + 32, PIXEL * 4, PIXEL))
        
    elif expression == "silly":
        # Tongue out
        tongue_color = (255, 100, 120)
        pygame.draw.rect(screen, tongue_color, (x_center - 8, y_center + 32, PIXEL * 2, PIXEL * 2))
        # One eye wink
        pygame.draw.rect(screen, black, (x_center - 32, y_center + 8, PIXEL * 3, PIXEL))
        
    elif expression == "cute":
        # Round mouth
        mouth_color = (255, 150, 150)
        pygame.draw.rect(screen, mouth_color, (x_center - 8, y_center + 28, PIXEL * 2, PIXEL * 2))
        # Blush
        blush_color = (255, 180, 180)
        pygame.draw.rect(screen, blush_color, (x_center - 48, y_center + 24, PIXEL * 2, PIXEL))
        pygame.draw.rect(screen, blush_color, (x_center + 40, y_center + 24, PIXEL * 2, PIXEL))

# ============ Accessory Drawing Functions ============

def draw_headwear(screen, headwear_type, race):
    """Draw headwear"""
    x_center = 160
    y_center = 140
    
    if headwear_type == "horn_helmet":
        # Metal helmet
        helmet_color = (150, 150, 150)
        for i in range(7, 13):
            for j in range(3, 6):
                pygame.draw.rect(screen, helmet_color,
                               (x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL))
        # Horns
        horn_color = (240, 240, 220)
        pygame.draw.rect(screen, horn_color, (x_center - 64, y_center - 40, PIXEL * 2, PIXEL * 4))
        pygame.draw.rect(screen, horn_color, (x_center + 56, y_center - 40, PIXEL * 2, PIXEL * 4))
        pygame.draw.rect(screen, horn_color, (x_center - 72, y_center - 56, PIXEL * 2, PIXEL * 2))
        pygame.draw.rect(screen, horn_color, (x_center + 64, y_center - 56, PIXEL * 2, PIXEL * 2))
        
    elif headwear_type == "flower_crown":
        # Flowers
        pygame.draw.rect(screen, (255, 100, 150), (x_center - 48, y_center - 32, PIXEL * 2, PIXEL * 2))
        pygame.draw.rect(screen, (255, 200, 100), (x_center - 16, y_center - 40, PIXEL * 2, PIXEL * 2))
        pygame.draw.rect(screen, (150, 100, 255), (x_center + 24, y_center - 32, PIXEL * 2, PIXEL * 2))
        # Leaves
        leaf_color = (100, 200, 100)
        for i in range(7, 13):
            pygame.draw.rect(screen, leaf_color, (x_center - 80 + i * PIXEL, y_center - 24, PIXEL, PIXEL))
            
    elif headwear_type == "wizard_hat":
        # Tall pointed hat
        hat_color = (50, 50, 120)
        # Brim
        for i in range(6, 14):
            pygame.draw.rect(screen, hat_color, (x_center - 80 + i * PIXEL, y_center - 24, PIXEL, PIXEL))
        # Cone
        for i in range(8, 12):
            for j in range(5, 12):
                if j < 9 - abs(i - 10):
                    pygame.draw.rect(screen, hat_color,
                                   (x_center - 80 + i * PIXEL, y_center - 40 - j * PIXEL, PIXEL, PIXEL))
        # Star decoration
        star_color = (255, 255, 100)
        pygame.draw.rect(screen, star_color, (x_center - 8, y_center - 64, PIXEL, PIXEL))
        
    elif headwear_type == "tentacle_hat":
        # Octopus-like hat
        tentacle_color = (200, 100, 200)
        # Main body
        for i in range(7, 13):
            for j in range(3, 6):
                pygame.draw.rect(screen, tentacle_color,
                               (x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL))
        # Tentacles
        pygame.draw.rect(screen, tentacle_color, (x_center - 56, y_center - 16, PIXEL, PIXEL * 3))
        pygame.draw.rect(screen, tentacle_color, (x_center - 32, y_center - 24, PIXEL, PIXEL * 3))
        pygame.draw.rect(screen, tentacle_color, (x_center + 24, y_center - 24, PIXEL, PIXEL * 3))
        pygame.draw.rect(screen, tentacle_color, (x_center + 48, y_center - 16, PIXEL, PIXEL * 3))

def draw_necklace(screen, necklace_type):
    """Draw necklace"""
    x_center = 160
    y_center = 140
    
    if necklace_type == "skull_pendant":
        # Chain
        chain_color = (200, 200, 200)
        for i in range(8, 12):
            pygame.draw.rect(screen, chain_color, (x_center - 80 + i * PIXEL, y_center + 64, PIXEL, PIXEL))
        # Skull
        skull_color = (240, 240, 230)
        pygame.draw.rect(screen, skull_color, (x_center - 16, y_center + 72, PIXEL * 4, PIXEL * 3))
        pygame.draw.rect(screen, (0, 0, 0), (x_center - 8, y_center + 72, PIXEL, PIXEL))
        pygame.draw.rect(screen, (0, 0, 0), (x_center + 8, y_center + 72, PIXEL, PIXEL))
        
    elif necklace_type == "gem_collar":
        # Gold collar
        gold_color = (255, 215, 0)
        for i in range(7, 13):
            pygame.draw.rect(screen, gold_color, (x_center - 80 + i * PIXEL, y_center + 64, PIXEL, PIXEL))
        # Gems
        pygame.draw.rect(screen, (255, 50, 50), (x_center - 32, y_center + 64, PIXEL, PIXEL))
        pygame.draw.rect(screen, (50, 50, 255), (x_center, y_center + 64, PIXEL, PIXEL))
        pygame.draw.rect(screen, (50, 255, 50), (x_center + 24, y_center + 64, PIXEL, PIXEL))
        
    elif necklace_type == "leaf_necklace":
        # Vine
        vine_color = (100, 150, 80)
        for i in range(8, 12):
            pygame.draw.rect(screen, vine_color, (x_center - 80 + i * PIXEL, y_center + 64, PIXEL, PIXEL))
        # Leaves
        leaf_color = (120, 200, 100)
        pygame.draw.rect(screen, leaf_color, (x_center - 24, y_center + 72, PIXEL * 2, PIXEL * 2))
        pygame.draw.rect(screen, leaf_color, (x_center + 8, y_center + 72, PIXEL * 2, PIXEL * 2))

def draw_earrings(screen, earring_type):
    """Draw earrings"""
    x_center = 160
    y_center = 140
    
    if earring_type == "hoop":
        # Gold hoops
        gold_color = (255, 215, 0)
        pygame.draw.rect(screen, gold_color, (x_center - 64, y_center + 16, PIXEL, PIXEL * 3))
        pygame.draw.rect(screen, gold_color, (x_center + 56, y_center + 16, PIXEL, PIXEL * 3))
        pygame.draw.rect(screen, gold_color, (x_center - 72, y_center + 24, PIXEL, PIXEL))
        pygame.draw.rect(screen, gold_color, (x_center + 64, y_center + 24, PIXEL, PIXEL))
        
    elif earring_type == "feather":
        # Feather earrings
        feather_color = (100, 200, 200)
        pygame.draw.rect(screen, feather_color, (x_center - 64, y_center + 16, PIXEL, PIXEL * 4))
        pygame.draw.rect(screen, feather_color, (x_center + 56, y_center + 16, PIXEL, PIXEL * 4))
        pygame.draw.rect(screen, feather_color, (x_center - 72, y_center + 24, PIXEL, PIXEL * 2))
        pygame.draw.rect(screen, feather_color, (x_center + 64, y_center + 24, PIXEL, PIXEL * 2))
        
    elif earring_type == "bone":
        # Bone earrings
        bone_color = (240, 240, 220)
        pygame.draw.rect(screen, bone_color, (x_center - 64, y_center + 16, PIXEL * 2, PIXEL * 3))
        pygame.draw.rect(screen, bone_color, (x_center + 56, y_center + 16, PIXEL * 2, PIXEL * 3))

def draw_clothes(screen, clothes_type, skin_col):
    """Draw clothing/armor"""
    x_center = 160
    y_center = 140
    
    if clothes_type == "robe":
        # Flowing robe
        robe_color = (80, 60, 140)
        for i in range(6, 14):
            for j in range(13, 20):
                pygame.draw.rect(screen, robe_color,
                               (x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL))
        # Belt
        belt_color = (150, 100, 50)
        for i in range(7, 13):
            pygame.draw.rect(screen, belt_color, (x_center - 80 + i * PIXEL, y_center + 48, PIXEL, PIXEL))
            
    elif clothes_type == "armor":
        # Plate armor
        armor_color = (180, 180, 200)
        for i in range(7, 13):
            for j in range(13, 19):
                pygame.draw.rect(screen, armor_color,
                               (x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL))
        # Armor details
        detail_color = (120, 120, 140)
        for i in range(8, 12):
            pygame.draw.rect(screen, detail_color, (x_center - 80 + i * PIXEL, y_center + 40, PIXEL, PIXEL))
            
    elif clothes_type == "tunic":
        # Simple tunic
        tunic_color = (150, 100, 60)
        for i in range(7, 13):
            for j in range(13, 19):
                pygame.draw.rect(screen, tunic_color,
                               (x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL))
        # Collar
        for i in range(8, 12):
            pygame.draw.rect(screen, skin_col, (x_center - 80 + i * PIXEL, y_center + 24, PIXEL, PIXEL))
            
    elif clothes_type == "cloak":
        # Mysterious cloak
        cloak_color = (40, 40, 60)
        # Shoulders
        for i in range(6, 14):
            for j in range(12, 20):
                if i < 8 or i > 11:
                    pygame.draw.rect(screen, cloak_color,
                                   (x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL))
        # Center
        for i in range(8, 12):
            for j in range(13, 19):
                pygame.draw.rect(screen, cloak_color,
                               (x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL))
        # Clasp
        gold_color = (255, 215, 0)
        pygame.draw.rect(screen, gold_color, (x_center - 8, y_center + 24, PIXEL * 2, PIXEL))

def main():
    """Main game loop"""
    screen = setup()
    clock = pygame.time.Clock()
    
    # Generate initial avatar
    generate_avatar()
    draw_avatar(screen)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Generate new avatar on mouse click
                generate_avatar()
                draw_avatar(screen)
        
        clock.tick(60)  # 60 FPS
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
