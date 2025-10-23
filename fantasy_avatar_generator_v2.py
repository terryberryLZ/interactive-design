#!/usr/bin/env python3
"""
Fantasy Pixel Avatar Generator V2 - Asset-based version
Uses AI-generated modular assets for composition
Click anywhere or press R to generate a new random avatar
Press S to save the current avatar
"""

import pygame
import random
import sys
import os
from pathlib import Path
from datetime import datetime

# Screen dimensions
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512

# Asset directories
ASSETS_DIR = Path("assets")
HATS_DIR = ASSETS_DIR / "hats"
HAIR_DIR = ASSETS_DIR / "hair"
CLOTHES_DIR = ASSETS_DIR / "clothes"
ACCESSORIES_DIR = ASSETS_DIR / "accessories"
BACKGROUNDS_DIR = ASSETS_DIR / "backgrounds"

# Asset cache
assets_cache = {
    "hats": [],
    "hair": [],
    "clothes": [],
    "accessories": [],
    "backgrounds": []
}

# Fallback colors for when assets aren't loaded yet
FALLBACK_COLORS = {
    "background": (180, 160, 200),
    "body": (255, 220, 177),
    "clothes": (100, 150, 200),
    "hair": (80, 60, 40),
    "hat": (150, 50, 50),
    "accessory": (200, 180, 50)
}


def load_assets():
    """Load all available assets from directories"""
    print("Loading assets...")
    
    # Load hats
    if HATS_DIR.exists():
        for file in HATS_DIR.glob("*.png"):
            try:
                img = pygame.image.load(str(file)).convert_alpha()
                # Resize to screen size if needed
                if img.get_size() != (SCREEN_WIDTH, SCREEN_HEIGHT):
                    img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                assets_cache["hats"].append(img)
                print(f"  Loaded hat: {file.name}")
            except Exception as e:
                print(f"  Error loading {file.name}: {e}")
    
    # Load hair
    if HAIR_DIR.exists():
        for file in HAIR_DIR.glob("*.png"):
            try:
                img = pygame.image.load(str(file)).convert_alpha()
                if img.get_size() != (SCREEN_WIDTH, SCREEN_HEIGHT):
                    img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                assets_cache["hair"].append(img)
                print(f"  Loaded hair: {file.name}")
            except Exception as e:
                print(f"  Error loading {file.name}: {e}")
    
    # Load clothes
    if CLOTHES_DIR.exists():
        for file in CLOTHES_DIR.glob("*.png"):
            try:
                img = pygame.image.load(str(file)).convert_alpha()
                if img.get_size() != (SCREEN_WIDTH, SCREEN_HEIGHT):
                    img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                assets_cache["clothes"].append(img)
                print(f"  Loaded clothes: {file.name}")
            except Exception as e:
                print(f"  Error loading {file.name}: {e}")
    
    # Load accessories
    if ACCESSORIES_DIR.exists():
        for file in ACCESSORIES_DIR.glob("*.png"):
            try:
                img = pygame.image.load(str(file)).convert_alpha()
                if img.get_size() != (SCREEN_WIDTH, SCREEN_HEIGHT):
                    img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                assets_cache["accessories"].append(img)
                print(f"  Loaded accessory: {file.name}")
            except Exception as e:
                print(f"  Error loading {file.name}: {e}")
    
    # Load backgrounds
    if BACKGROUNDS_DIR.exists():
        for file in BACKGROUNDS_DIR.glob("*.png"):
            try:
                img = pygame.image.load(str(file)).convert_alpha()
                if img.get_size() != (SCREEN_WIDTH, SCREEN_HEIGHT):
                    img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                assets_cache["backgrounds"].append(img)
                print(f"  Loaded background: {file.name}")
            except Exception as e:
                print(f"  Error loading {file.name}: {e}")
    
    # Summary
    print("\nAssets loaded:")
    print(f"  Hats: {len(assets_cache['hats'])}")
    print(f"  Hair: {len(assets_cache['hair'])}")
    print(f"  Clothes: {len(assets_cache['clothes'])}")
    print(f"  Accessories: {len(assets_cache['accessories'])}")
    print(f"  Backgrounds: {len(assets_cache['backgrounds'])}")
    
    if sum(len(v) for v in assets_cache.values()) == 0:
        print("\n⚠️ No assets found! Using fallback mode.")
        print("Please add PNG files to the assets folders.")
        print("See ASSET_GENERATION_GUIDE.md for instructions.")


def draw_fallback_avatar(surface):
    """Draw a simple fallback avatar when no assets are loaded"""
    # Background
    surface.fill(FALLBACK_COLORS["background"])
    
    # Body/torso
    pygame.draw.ellipse(surface, FALLBACK_COLORS["clothes"], 
                       (150, 250, 212, 220))
    
    # Head
    pygame.draw.circle(surface, FALLBACK_COLORS["body"], 
                      (256, 180), 80)
    
    # Hair
    pygame.draw.circle(surface, FALLBACK_COLORS["hair"], 
                      (256, 140), 60)
    
    # Hat
    pygame.draw.polygon(surface, FALLBACK_COLORS["hat"],
                       [(256, 80), (200, 160), (312, 160)])
    
    # Accessory (simple necklace)
    pygame.draw.circle(surface, FALLBACK_COLORS["accessory"], 
                      (256, 240), 15)
    
    # Eyes
    pygame.draw.circle(surface, (50, 50, 50), (230, 170), 10)
    pygame.draw.circle(surface, (50, 50, 50), (282, 170), 10)
    pygame.draw.circle(surface, (255, 255, 255), (235, 165), 4)
    pygame.draw.circle(surface, (255, 255, 255), (287, 165), 4)
    
    # Mouth
    pygame.draw.arc(surface, (50, 50, 50), (226, 190, 60, 30), 
                   3.14, 6.28, 3)


def generate_avatar(surface):
    """Generate a new random avatar by compositing assets"""
    # Clear surface
    surface.fill((255, 255, 255))
    
    # If no assets loaded, use fallback
    if sum(len(v) for v in assets_cache.values()) == 0:
        draw_fallback_avatar(surface)
        return
    
    # Layer 1: Background
    if assets_cache["backgrounds"]:
        bg = random.choice(assets_cache["backgrounds"])
        surface.blit(bg, (0, 0))
    else:
        surface.fill(FALLBACK_COLORS["background"])
    
    # Layer 2: Body/Clothes
    if assets_cache["clothes"]:
        clothes = random.choice(assets_cache["clothes"])
        surface.blit(clothes, (0, 0))
    else:
        # Fallback body
        pygame.draw.circle(surface, FALLBACK_COLORS["body"], (256, 180), 80)
        pygame.draw.ellipse(surface, FALLBACK_COLORS["clothes"], (150, 250, 212, 220))
    
    # Layer 3: Hair
    if assets_cache["hair"]:
        hair = random.choice(assets_cache["hair"])
        surface.blit(hair, (0, 0))
    else:
        # Fallback hair
        pygame.draw.circle(surface, FALLBACK_COLORS["hair"], (256, 140), 60)
    
    # Layer 4: Hat (50% chance to skip)
    if assets_cache["hats"] and random.random() > 0.3:
        hat = random.choice(assets_cache["hats"])
        surface.blit(hat, (0, 0))
    
    # Layer 5: Accessory (50% chance to skip)
    if assets_cache["accessories"] and random.random() > 0.5:
        accessory = random.choice(assets_cache["accessories"])
        surface.blit(accessory, (0, 0))


def save_avatar(surface):
    """Save the current avatar to file"""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = output_dir / f"avatar_{timestamp}.png"
    
    pygame.image.save(surface, str(filename))
    print(f"✅ Avatar saved: {filename}")
    return filename


def main():
    """Main game loop"""
    pygame.init()
    
    # Create window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fantasy Avatar Generator V2 (Asset-based)")
    
    # Load assets
    load_assets()
    
    # Generate initial avatar
    avatar_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    generate_avatar(avatar_surface)
    
    # Font for instructions
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    
    # Main loop
    running = True
    show_instructions = True
    instruction_timer = pygame.time.get_ticks()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Generate new avatar on click
                generate_avatar(avatar_surface)
                print("🎲 New avatar generated!")
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Generate new avatar on R key
                    generate_avatar(avatar_surface)
                    print("🎲 New avatar generated!")
                
                elif event.key == pygame.K_s:
                    # Save avatar on S key
                    save_avatar(avatar_surface)
                
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        # Draw avatar
        screen.blit(avatar_surface, (0, 0))
        
        # Show instructions for first 5 seconds
        if show_instructions:
            elapsed = pygame.time.get_ticks() - instruction_timer
            if elapsed < 5000:
                # Semi-transparent overlay
                overlay = pygame.Surface((SCREEN_WIDTH, 80))
                overlay.set_alpha(200)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, SCREEN_HEIGHT - 80))
                
                # Instructions text
                text1 = font.render("Click or press R to generate new avatar", True, (255, 255, 255))
                text2 = font.render("Press S to save | ESC to quit", True, (255, 255, 255))
                screen.blit(text1, (20, SCREEN_HEIGHT - 70))
                screen.blit(text2, (20, SCREEN_HEIGHT - 45))
            else:
                show_instructions = False
        
        pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    main()
