#!/usr/bin/env python3
"""
Fantasy Pixel Avatar Generator - Rewritten with proper alignment
Click anywhere or press R to generate a new random avatar
Press S to save the current avatar
"""

import pygame
import random
import sys
from datetime import datetime
from pathlib import Path

# Screen dimensions
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512
PIXEL_SIZE = 4  # Scale factor for pixel art

# Canvas grid (logical pixels)
GRID_WIDTH = SCREEN_WIDTH // PIXEL_SIZE  # 128
GRID_HEIGHT = SCREEN_HEIGHT // PIXEL_SIZE  # 128

# Avatar anchor points (in grid coordinates)
CENTER_X = GRID_WIDTH // 2  # 64
CENTER_Y = GRID_HEIGHT // 2  # 64

HEAD_Y = CENTER_Y - 8  # Head starts above center
BODY_Y = CENTER_Y + 16  # Body starts below head
NECK_Y = CENTER_Y + 8  # Neck position


class AvatarGenerator:
    """Main avatar generator class"""
    
    def __init__(self):
        # Component options
        self.skin_colors = [
            (255, 220, 177),  # Peach
            (245, 210, 180),  # Light tan
            (210, 140, 100),  # Tan
            (160, 120, 90),   # Dark tan
            (120, 180, 120),  # Green (orc)
            (200, 200, 240),  # Pale blue (elf)
        ]
        
        self.hair_colors = [
            (80, 60, 40),     # Brown
            (240, 220, 100),  # Blonde
            (40, 40, 40),     # Black
            (200, 100, 50),   # Ginger
            (180, 180, 200),  # Silver
            (100, 50, 150),   # Purple
        ]
        
        self.cloth_colors = [
            (100, 150, 200),  # Blue
            (200, 50, 50),    # Red
            (100, 200, 100),  # Green
            (150, 100, 180),  # Purple
            (200, 200, 100),  # Yellow
            (100, 100, 100),  # Gray
        ]
        
        self.backgrounds = [
            ("solid", (180, 160, 200)),
            ("solid", (160, 180, 210)),
            ("solid", (240, 200, 220)),
            ("solid", (200, 220, 200)),
            ("gradient", ((255, 180, 100), (150, 100, 180))),
            ("gradient", ((200, 220, 255), (60, 100, 180))),
        ]
    
    def draw_pixel(self, surface, color, gx, gy, w=1, h=1):
        """Draw a pixel at grid coordinates"""
        pygame.draw.rect(surface, color, 
                        (gx * PIXEL_SIZE, gy * PIXEL_SIZE, 
                         w * PIXEL_SIZE, h * PIXEL_SIZE))
    
    def draw_background(self, surface, bg_type):
        """Draw background"""
        bg_style, bg_data = bg_type
        
        if bg_style == "solid":
            surface.fill(bg_data)
        elif bg_style == "gradient":
            top_color, bottom_color = bg_data
            for y in range(GRID_HEIGHT):
                t = y / GRID_HEIGHT
                r = int(top_color[0] * (1 - t) + bottom_color[0] * t)
                g = int(top_color[1] * (1 - t) + bottom_color[1] * t)
                b = int(top_color[2] * (1 - t) + bottom_color[2] * t)
                for x in range(GRID_WIDTH):
                    self.draw_pixel(surface, (r, g, b), x, y)
    
    def draw_body(self, surface, cloth_color):
        """Draw body/torso"""
        # Shoulders (wide rectangle)
        for y in range(4):
            for x in range(-10, 11):
                self.draw_pixel(surface, cloth_color, CENTER_X + x, BODY_Y + y)
        
        # Torso (narrower, extends down)
        for y in range(4, 20):
            width = 8
            for x in range(-width, width + 1):
                self.draw_pixel(surface, cloth_color, CENTER_X + x, BODY_Y + y)
        
        # Add simple details (darker shade for outline)
        dark_cloth = tuple(max(0, c - 40) for c in cloth_color)
        # Collar
        for x in range(-6, 7):
            self.draw_pixel(surface, dark_cloth, CENTER_X + x, BODY_Y)
    
    def draw_neck(self, surface, skin_color):
        """Draw neck connecting head to body"""
        for y in range(4):
            for x in range(-3, 4):
                self.draw_pixel(surface, skin_color, CENTER_X + x, NECK_Y + y)
    
    def draw_head(self, surface, skin_color):
        """Draw head (oval shape)"""
        # Main head shape (centered)
        for y in range(12):
            if y < 3 or y > 8:
                width = 6  # Narrower at top and bottom
            else:
                width = 8  # Wider in middle
            
            for x in range(-width, width + 1):
                self.draw_pixel(surface, skin_color, CENTER_X + x, HEAD_Y + y)
        
        # Ears
        self.draw_pixel(surface, skin_color, CENTER_X - 9, HEAD_Y + 5, 2, 3)
        self.draw_pixel(surface, skin_color, CENTER_X + 8, HEAD_Y + 5, 2, 3)
    
    def draw_face(self, surface):
        """Draw facial features"""
        # Eyes (white)
        self.draw_pixel(surface, (255, 255, 255), CENTER_X - 4, HEAD_Y + 5, 3, 2)
        self.draw_pixel(surface, (255, 255, 255), CENTER_X + 2, HEAD_Y + 5, 3, 2)
        
        # Pupils (black)
        pupil_offset = random.choice([-1, 0, 1])  # Random gaze direction
        self.draw_pixel(surface, (0, 0, 0), CENTER_X - 3 + pupil_offset, HEAD_Y + 5)
        self.draw_pixel(surface, (0, 0, 0), CENTER_X + 3 + pupil_offset, HEAD_Y + 5)
        
        # Mouth (random expression)
        mouth_type = random.choice(["smile", "neutral", "cute"])
        
        if mouth_type == "smile":
            # Curved smile
            for x in range(-2, 3):
                self.draw_pixel(surface, (0, 0, 0), CENTER_X + x, HEAD_Y + 9)
            self.draw_pixel(surface, (0, 0, 0), CENTER_X - 3, HEAD_Y + 8)
            self.draw_pixel(surface, (0, 0, 0), CENTER_X + 3, HEAD_Y + 8)
        elif mouth_type == "neutral":
            # Straight line
            for x in range(-2, 3):
                self.draw_pixel(surface, (0, 0, 0), CENTER_X + x, HEAD_Y + 9)
        else:  # cute
            # Small round mouth
            self.draw_pixel(surface, (255, 150, 150), CENTER_X, HEAD_Y + 9, 2, 2)
            # Blush
            self.draw_pixel(surface, (255, 180, 180), CENTER_X - 6, HEAD_Y + 7, 2, 1)
            self.draw_pixel(surface, (255, 180, 180), CENTER_X + 5, HEAD_Y + 7, 2, 1)
    
    def draw_hair(self, surface, hair_color):
        """Draw hair"""
        hair_style = random.choice(["short", "long", "spiky", "bald"])
        
        if hair_style == "bald":
            return
        
        if hair_style == "short":
            # Cover top and sides of head
            for y in range(5):
                width = 8 if y > 2 else 6
                for x in range(-width, width + 1):
                    self.draw_pixel(surface, hair_color, CENTER_X + x, HEAD_Y + y)
        
        elif hair_style == "long":
            # Top of head
            for y in range(5):
                width = 8 if y > 2 else 6
                for x in range(-width, width + 1):
                    self.draw_pixel(surface, hair_color, CENTER_X + x, HEAD_Y + y)
            # Long sides
            for y in range(5, 12):
                self.draw_pixel(surface, hair_color, CENTER_X - 8, HEAD_Y + y, 2, 1)
                self.draw_pixel(surface, hair_color, CENTER_X + 7, HEAD_Y + y, 2, 1)
        
        else:  # spiky
            # Base
            for y in range(5):
                width = 8 if y > 2 else 6
                for x in range(-width, width + 1):
                    self.draw_pixel(surface, hair_color, CENTER_X + x, HEAD_Y + y)
            # Spikes
            for spike_x in [-6, -2, 2, 6]:
                for spike_y in range(3):
                    self.draw_pixel(surface, hair_color, CENTER_X + spike_x, HEAD_Y - spike_y)
    
    def draw_hat(self, surface):
        """Draw hat/headwear"""
        hat_type = random.choice(["none", "none", "wizard", "crown", "helmet", "hood"])
        
        if hat_type == "none":
            return
        
        if hat_type == "wizard":
            # Wizard hat (tall cone)
            hat_color = random.choice([(50, 50, 120), (120, 50, 120), (50, 120, 50)])
            # Brim
            for x in range(-10, 11):
                self.draw_pixel(surface, hat_color, CENTER_X + x, HEAD_Y)
            # Cone
            for h in range(8):
                width = 6 - h // 2
                for x in range(-width, width + 1):
                    self.draw_pixel(surface, hat_color, CENTER_X + x, HEAD_Y - h)
            # Star
            self.draw_pixel(surface, (255, 255, 100), CENTER_X, HEAD_Y - 8)
        
        elif hat_type == "crown":
            # Crown
            gold = (255, 215, 0)
            for x in range(-6, 7):
                self.draw_pixel(surface, gold, CENTER_X + x, HEAD_Y)
            # Points
            for x in [-5, 0, 5]:
                self.draw_pixel(surface, gold, CENTER_X + x, HEAD_Y - 1, 1, 2)
            # Gems
            self.draw_pixel(surface, (255, 50, 50), CENTER_X - 5, HEAD_Y - 2)
            self.draw_pixel(surface, (50, 255, 50), CENTER_X, HEAD_Y - 2)
            self.draw_pixel(surface, (50, 50, 255), CENTER_X + 5, HEAD_Y - 2)
        
        elif hat_type == "helmet":
            # Knight helmet
            gray = (150, 150, 150)
            for y in range(4):
                width = 8 if y > 1 else 7
                for x in range(-width, width + 1):
                    self.draw_pixel(surface, gray, CENTER_X + x, HEAD_Y + y)
            # Horns
            self.draw_pixel(surface, (200, 200, 180), CENTER_X - 9, HEAD_Y, 2, 3)
            self.draw_pixel(surface, (200, 200, 180), CENTER_X + 8, HEAD_Y, 2, 3)
        
        else:  # hood
            # Hood
            hood_color = random.choice([(100, 80, 60), (60, 80, 60), (60, 60, 80)])
            for y in range(6):
                width = 10 if y > 2 else 8
                for x in range(-width, width + 1):
                    self.draw_pixel(surface, hood_color, CENTER_X + x, HEAD_Y + y)
    
    def draw_accessory(self, surface):
        """Draw necklace or accessory"""
        acc_type = random.choice(["none", "none", "pendant", "collar", "scarf"])
        
        if acc_type == "none":
            return
        
        if acc_type == "pendant":
            # Chain
            for x in range(-2, 3):
                self.draw_pixel(surface, (150, 150, 170), CENTER_X + x, NECK_Y + 3)
            # Pendant
            pendant_color = random.choice([(100, 200, 255), (255, 50, 50), (100, 255, 100)])
            self.draw_pixel(surface, pendant_color, CENTER_X - 1, NECK_Y + 4, 2, 2)
        
        elif acc_type == "collar":
            # Gold collar
            for x in range(-6, 7):
                self.draw_pixel(surface, (255, 215, 0), CENTER_X + x, NECK_Y + 3)
        
        else:  # scarf
            # Scarf
            scarf_color = random.choice([(200, 50, 50), (50, 200, 50), (200, 200, 50)])
            for x in range(-6, 7):
                self.draw_pixel(surface, scarf_color, CENTER_X + x, NECK_Y + 3)
            # Hanging ends
            self.draw_pixel(surface, scarf_color, CENTER_X - 7, NECK_Y + 4, 1, 4)
            self.draw_pixel(surface, scarf_color, CENTER_X + 7, NECK_Y + 4, 1, 4)
    
    def generate(self, surface):
        """Generate a complete random avatar"""
        # Random colors
        skin_color = random.choice(self.skin_colors)
        hair_color = random.choice(self.hair_colors)
        cloth_color = random.choice(self.cloth_colors)
        bg_type = random.choice(self.backgrounds)
        
        # Draw in correct layer order
        self.draw_background(surface, bg_type)
        self.draw_body(surface, cloth_color)
        self.draw_neck(surface, skin_color)
        self.draw_head(surface, skin_color)
        self.draw_face(surface)
        self.draw_hair(surface, hair_color)
        self.draw_hat(surface)
        self.draw_accessory(surface)


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
    pygame.display.set_caption("Fantasy Avatar Generator")
    
    # Create generator
    generator = AvatarGenerator()
    
    # Generate initial avatar
    avatar_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    generator.generate(avatar_surface)
    
    # Font for instructions
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    
    # Main loop
    running = True
    show_instructions = True
    instruction_timer = pygame.time.get_ticks()
    
    print("🎨 Fantasy Avatar Generator")
    print("Controls:")
    print("  - Click or press R: Generate new avatar")
    print("  - Press S: Save avatar")
    print("  - Press ESC: Quit")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Generate new avatar on click
                generator.generate(avatar_surface)
                print("🎲 New avatar generated!")
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Generate new avatar on R key
                    generator.generate(avatar_surface)
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
