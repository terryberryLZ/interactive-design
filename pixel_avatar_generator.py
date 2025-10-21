#!/usr/bin/env python3
"""
Enhanced Pixel-Art Avatar Generator
Reference images: GitHub issue attachments showing high-quality pixel-art avatars
- Canvas: 160x160 logical pixels
- Style: Crisp pixel-art with nearest-neighbor scaling
- Features: Detailed faces, hair, clothing, accessories
"""

import pygame
import random
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Initialize Pygame
pygame.init()

# Canvas settings - logical pixel grid
LOGICAL_WIDTH = 160
LOGICAL_HEIGHT = 160
SCALE_FACTOR = 4  # Display at 4x size (640x640)
DISPLAY_WIDTH = LOGICAL_WIDTH * SCALE_FACTOR
DISPLAY_HEIGHT = LOGICAL_HEIGHT * SCALE_FACTOR

class ColorPalette:
    """Load and manage color palettes"""
    def __init__(self, palette_file: str = "color_palette.json"):
        self.palette_file = palette_file
        self.colors = self._load_palette()
    
    def _load_palette(self) -> Dict:
        """Load color palette from JSON file"""
        try:
            with open(self.palette_file, 'r') as f:
                data = json.load(f)
                return data['palettes']
        except FileNotFoundError:
            print(f"Warning: {self.palette_file} not found, using default colors")
            return self._default_palette()
    
    def _default_palette(self) -> Dict:
        """Fallback palette if JSON file is missing"""
        return {
            "backgrounds": {"cyan_blue": [173, 216, 230]},
            "skin_tones": {"light": [255, 224, 189]},
            "skin_shadows": {"light": [232, 190, 150]},
            "skin_highlights": {"light": [255, 240, 220]},
            "hair_colors": {"brown": [101, 67, 33]},
            "hair_shadows": {"brown": [70, 45, 20]},
            "hair_highlights": {"brown": [130, 90, 50]},
            "eyes": {"white": [255, 255, 255], "black": [28, 28, 28]},
            "clothing": {"purple_light": [186, 164, 212]},
            "accents": {"outline_black": [0, 0, 0]}
        }
    
    def get(self, category: str, name: str) -> Tuple[int, int, int]:
        """Get a specific color from the palette"""
        try:
            color = self.colors[category][name]
            return tuple(color)
        except KeyError:
            return (255, 0, 255)  # Magenta for missing colors

class PixelCanvas:
    """Manages a logical pixel grid that can be scaled"""
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.surface.set_colorkey(None)
    
    def clear(self, color: Tuple[int, int, int]):
        """Clear the canvas with a color"""
        self.surface.fill(color)
    
    def set_pixel(self, x: int, y: int, color: Tuple[int, int, int]):
        """Set a single pixel"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.surface.set_at((x, y), color)
    
    def draw_rect(self, x: int, y: int, w: int, h: int, color: Tuple[int, int, int]):
        """Draw a filled rectangle"""
        pygame.draw.rect(self.surface, color, (x, y, w, h))
    
    def draw_outline_rect(self, x: int, y: int, w: int, h: int, color: Tuple[int, int, int]):
        """Draw a rectangle outline"""
        pygame.draw.rect(self.surface, color, (x, y, w, h), 1)
    
    def get_scaled_surface(self, scale: int) -> pygame.Surface:
        """Return a scaled version using nearest-neighbor"""
        scaled = pygame.transform.scale(
            self.surface,
            (self.width * scale, self.height * scale)
        )
        return scaled
    
    def save_png(self, filename: str, scale: int = 1):
        """Save the canvas as PNG"""
        if scale == 1:
            pygame.image.save(self.surface, filename)
        else:
            scaled = self.get_scaled_surface(scale)
            pygame.image.save(scaled, filename)

class AvatarGenerator:
    """Generate pixel-art avatars with modular layers"""
    def __init__(self, palette: ColorPalette, seed: Optional[int] = None):
        self.palette = palette
        self.seed = seed
        if seed is not None:
            random.seed(seed)
        
        # Avatar configuration
        self.config = {}
        
        # Layer variants (at least 5 each as per requirements)
        self.hair_styles = ['short_curly', 'buns', 'long_straight', 'bob', 'messy', 'pixie']
        self.eye_styles = ['round', 'wide', 'sleepy', 'angry', 'cute']
        self.mouth_styles = ['smile', 'neutral', 'laugh', 'small', 'open']
        self.clothing_styles = ['hoodie', 'collar_shirt', 'suspenders', 'turtleneck', 'tank_top']
        self.accessory_styles = ['none', 'glasses', 'earrings', 'headband', 'bow']
    
    def generate_random(self):
        """Generate random avatar configuration"""
        self.config = {
            'background': random.choice(list(self.palette.colors['backgrounds'].keys())),
            'skin_tone': random.choice(list(self.palette.colors['skin_tones'].keys())),
            'hair_color': random.choice(list(self.palette.colors['hair_colors'].keys())),
            'hair_style': random.choice(self.hair_styles),
            'eye_color': random.choice(['brown', 'blue', 'green', 'gray']),
            'eye_style': random.choice(self.eye_styles),
            'mouth_style': random.choice(self.mouth_styles),
            'clothing': random.choice(self.clothing_styles),
            'clothing_color': random.choice(['purple_light', 'green_light', 'blue_light', 'red']),
            'accessory': random.choice(self.accessory_styles)
        }
    
    def draw(self, canvas: PixelCanvas):
        """Draw the complete avatar on the canvas"""
        # Draw layers from back to front
        self._draw_background(canvas)
        self._draw_body(canvas)
        self._draw_face_base(canvas)
        self._draw_eyes(canvas)
        self._draw_nose(canvas)
        self._draw_mouth(canvas)
        self._draw_hair(canvas)
        self._draw_accessories(canvas)
    
    def _draw_background(self, canvas: PixelCanvas):
        """Draw background with optional border"""
        bg_color = self.palette.get('backgrounds', self.config['background'])
        canvas.clear(bg_color)
        
        # Optional subtle border/vignette
        border_color = tuple(max(0, c - 20) for c in bg_color)
        # Top and bottom borders
        for i in range(8):
            canvas.draw_rect(0, i, LOGICAL_WIDTH, 1, border_color)
            canvas.draw_rect(0, LOGICAL_HEIGHT - i - 1, LOGICAL_WIDTH, 1, border_color)
        # Side borders
        for i in range(8):
            canvas.draw_rect(i, 0, 1, LOGICAL_HEIGHT, border_color)
            canvas.draw_rect(LOGICAL_WIDTH - i - 1, 0, 1, LOGICAL_HEIGHT, border_color)
    
    def _draw_body(self, canvas: PixelCanvas):
        """Draw neck and clothing/body"""
        # Neck (centered)
        skin = self.palette.get('skin_tones', self.config['skin_tone'])
        shadow = self.palette.get('skin_shadows', self.config['skin_tone'])
        
        # Neck position
        neck_x = 70
        neck_y = 90
        canvas.draw_rect(neck_x, neck_y, 20, 15, skin)
        # Neck shadow
        canvas.draw_rect(neck_x + 2, neck_y + 10, 16, 5, shadow)
        
        # Clothing based on style
        clothing_color_name = self.config['clothing_color']
        if clothing_color_name in self.palette.colors['clothing']:
            clothing_color = self.palette.get('clothing', clothing_color_name)
        else:
            clothing_color = (150, 150, 200)
        
        clothing_style = self.config['clothing']
        
        if clothing_style == 'hoodie':
            self._draw_hoodie(canvas, clothing_color)
        elif clothing_style == 'collar_shirt':
            self._draw_collar_shirt(canvas, clothing_color)
        elif clothing_style == 'suspenders':
            self._draw_suspenders(canvas, clothing_color)
        elif clothing_style == 'turtleneck':
            self._draw_turtleneck(canvas, clothing_color)
        else:  # tank_top
            self._draw_tank_top(canvas, clothing_color)
    
    def _draw_hoodie(self, canvas: PixelCanvas, color: Tuple[int, int, int]):
        """Draw a hoodie with drawstrings"""
        # Main body
        canvas.draw_rect(40, 105, 80, 55, color)
        
        # Hood/collar
        darker = tuple(max(0, c - 30) for c in color)
        canvas.draw_rect(55, 100, 50, 10, darker)
        
        # Drawstrings
        white = self.palette.get('clothing', 'white')
        canvas.draw_rect(70, 105, 2, 8, white)
        canvas.draw_rect(88, 105, 2, 8, white)
        
        # Pocket lines
        outline = self.palette.get('accents', 'outline_black')
        canvas.draw_rect(50, 130, 60, 1, outline)
    
    def _draw_collar_shirt(self, canvas: PixelCanvas, color: Tuple[int, int, int]):
        """Draw a collared shirt"""
        # Main shirt
        canvas.draw_rect(40, 105, 80, 55, color)
        
        # Collar
        white = self.palette.get('clothing', 'white')
        canvas.draw_rect(60, 105, 40, 8, white)
        
        # Collar fold line
        outline = self.palette.get('accents', 'outline_black')
        canvas.draw_rect(70, 105, 20, 1, outline)
    
    def _draw_suspenders(self, canvas: PixelCanvas, color: Tuple[int, int, int]):
        """Draw a shirt with suspenders"""
        # White shirt base
        white = self.palette.get('clothing', 'white')
        canvas.draw_rect(40, 105, 80, 55, white)
        
        # Suspenders (use provided color)
        canvas.draw_rect(55, 105, 8, 55, color)
        canvas.draw_rect(97, 105, 8, 55, color)
        
        # Buttons
        yellow = self.palette.get('clothing', 'yellow')
        canvas.draw_rect(58, 108, 3, 3, yellow)
        canvas.draw_rect(100, 108, 3, 3, yellow)
    
    def _draw_turtleneck(self, canvas: PixelCanvas, color: Tuple[int, int, int]):
        """Draw a turtleneck sweater"""
        # Main sweater
        canvas.draw_rect(40, 95, 80, 65, color)
        
        # Neck fold
        darker = tuple(max(0, c - 30) for c in color)
        canvas.draw_rect(50, 95, 60, 8, darker)
    
    def _draw_tank_top(self, canvas: PixelCanvas, color: Tuple[int, int, int]):
        """Draw a tank top"""
        # Main top
        canvas.draw_rect(45, 105, 70, 55, color)
        
        # Straps
        canvas.draw_rect(55, 100, 10, 10, color)
        canvas.draw_rect(95, 100, 10, 10, color)
    
    def _draw_face_base(self, canvas: PixelCanvas):
        """Draw the base face shape with shading"""
        skin = self.palette.get('skin_tones', self.config['skin_tone'])
        shadow = self.palette.get('skin_shadows', self.config['skin_tone'])
        highlight = self.palette.get('skin_highlights', self.config['skin_tone'])
        outline = self.palette.get('accents', 'outline_black')
        
        # Face center
        face_x = 60
        face_y = 35
        face_w = 40
        face_h = 55
        
        # Main face oval (simplified as rounded rectangle)
        canvas.draw_rect(face_x, face_y, face_w, face_h, skin)
        
        # Round the top
        canvas.draw_rect(face_x + 5, face_y - 5, face_w - 10, 5, skin)
        canvas.draw_rect(face_x + 10, face_y - 8, face_w - 20, 3, skin)
        
        # Round the bottom (chin)
        canvas.draw_rect(face_x + 5, face_y + face_h, face_w - 10, 5, skin)
        canvas.draw_rect(face_x + 10, face_y + face_h + 5, face_w - 20, 3, skin)
        
        # Cheek highlights
        canvas.draw_rect(face_x + 2, face_y + 25, 6, 8, highlight)
        canvas.draw_rect(face_x + face_w - 8, face_y + 25, 6, 8, highlight)
        
        # Face shadows (under cheekbones)
        canvas.draw_rect(face_x + 2, face_y + 35, 8, 4, shadow)
        canvas.draw_rect(face_x + face_w - 10, face_y + 35, 8, 4, shadow)
        
        # Outline the face
        self._draw_face_outline(canvas, face_x, face_y, face_w, face_h, outline)
    
    def _draw_face_outline(self, canvas: PixelCanvas, x: int, y: int, w: int, h: int, color: Tuple[int, int, int]):
        """Draw face outline"""
        # Simplified outline
        canvas.draw_outline_rect(x, y, w, h, color)
        # Top rounding
        canvas.draw_outline_rect(x + 5, y - 5, w - 10, 5, color)
        # Bottom rounding
        canvas.draw_outline_rect(x + 5, y + h, w - 10, 5, color)
    
    def _draw_eyes(self, canvas: PixelCanvas):
        """Draw eyes with highlights based on style"""
        eye_style = self.config['eye_style']
        eye_color = self.palette.get('eyes', self.config['eye_color'])
        white = self.palette.get('eyes', 'white')
        black = self.palette.get('eyes', 'black')
        highlight = self.palette.get('eyes', 'highlight')
        
        left_eye_x = 68
        right_eye_x = 88
        eye_y = 55
        
        if eye_style == 'round':
            # White of eyes
            canvas.draw_rect(left_eye_x, eye_y, 8, 8, white)
            canvas.draw_rect(right_eye_x, eye_y, 8, 8, white)
            # Iris
            canvas.draw_rect(left_eye_x + 2, eye_y + 2, 4, 5, eye_color)
            canvas.draw_rect(right_eye_x + 2, eye_y + 2, 4, 5, eye_color)
            # Pupil
            canvas.draw_rect(left_eye_x + 3, eye_y + 3, 2, 3, black)
            canvas.draw_rect(right_eye_x + 3, eye_y + 3, 2, 3, black)
            # Highlight
            canvas.set_pixel(left_eye_x + 2, eye_y + 3, highlight)
            canvas.set_pixel(right_eye_x + 2, eye_y + 3, highlight)
            
        elif eye_style == 'wide':
            # Larger, rounder eyes
            canvas.draw_rect(left_eye_x - 1, eye_y, 10, 9, white)
            canvas.draw_rect(right_eye_x - 1, eye_y, 10, 9, white)
            # Iris
            canvas.draw_rect(left_eye_x + 2, eye_y + 2, 4, 5, eye_color)
            canvas.draw_rect(right_eye_x + 2, eye_y + 2, 4, 5, eye_color)
            # Pupil
            canvas.draw_rect(left_eye_x + 3, eye_y + 4, 2, 2, black)
            canvas.draw_rect(right_eye_x + 3, eye_y + 4, 2, 2, black)
            # Large highlight
            canvas.draw_rect(left_eye_x + 2, eye_y + 2, 2, 2, highlight)
            canvas.draw_rect(right_eye_x + 2, eye_y + 2, 2, 2, highlight)
            
        elif eye_style == 'sleepy':
            # Half-closed eyes
            canvas.draw_rect(left_eye_x, eye_y + 2, 8, 5, white)
            canvas.draw_rect(right_eye_x, eye_y + 2, 8, 5, white)
            # Small pupils
            canvas.draw_rect(left_eye_x + 3, eye_y + 3, 2, 2, black)
            canvas.draw_rect(right_eye_x + 3, eye_y + 3, 2, 2, black)
            # Upper eyelid
            canvas.draw_rect(left_eye_x, eye_y, 8, 2, eye_color)
            canvas.draw_rect(right_eye_x, eye_y, 8, 2, eye_color)
            
        elif eye_style == 'angry':
            # Angled eyes
            canvas.draw_rect(left_eye_x, eye_y + 1, 8, 7, white)
            canvas.draw_rect(right_eye_x, eye_y + 1, 8, 7, white)
            # Pupils
            canvas.draw_rect(left_eye_x + 3, eye_y + 3, 2, 3, black)
            canvas.draw_rect(right_eye_x + 3, eye_y + 3, 2, 3, black)
            # Angry eyebrows
            canvas.draw_rect(left_eye_x, eye_y - 2, 6, 1, black)
            canvas.draw_rect(right_eye_x + 2, eye_y - 2, 6, 1, black)
            
        else:  # cute
            # Large round eyes
            canvas.draw_rect(left_eye_x - 1, eye_y, 9, 10, white)
            canvas.draw_rect(right_eye_x - 1, eye_y, 9, 10, white)
            # Large iris
            canvas.draw_rect(left_eye_x + 1, eye_y + 2, 5, 6, eye_color)
            canvas.draw_rect(right_eye_x + 1, eye_y + 2, 5, 6, eye_color)
            # Pupil
            canvas.draw_rect(left_eye_x + 3, eye_y + 5, 2, 2, black)
            canvas.draw_rect(right_eye_x + 3, eye_y + 5, 2, 2, black)
            # Large sparkle highlight
            canvas.draw_rect(left_eye_x + 1, eye_y + 3, 2, 2, highlight)
            canvas.draw_rect(right_eye_x + 1, eye_y + 3, 2, 2, highlight)
    
    def _draw_nose(self, canvas: PixelCanvas):
        """Draw subtle nose shading"""
        nose_shadow = self.palette.get('accents', 'nose_shadow')
        # Small L-shape nose
        nose_x = 78
        nose_y = 68
        canvas.draw_rect(nose_x, nose_y, 2, 4, nose_shadow)
        canvas.draw_rect(nose_x, nose_y + 3, 4, 2, nose_shadow)
    
    def _draw_mouth(self, canvas: PixelCanvas):
        """Draw mouth based on style"""
        mouth_style = self.config['mouth_style']
        mouth_dark = self.palette.get('accents', 'mouth_dark')
        mouth_light = self.palette.get('accents', 'mouth_light')
        
        mouth_x = 72
        mouth_y = 75
        
        if mouth_style == 'smile':
            # Curved smile
            canvas.draw_rect(mouth_x, mouth_y + 2, 16, 2, mouth_dark)
            canvas.draw_rect(mouth_x + 2, mouth_y, 12, 2, mouth_light)
            canvas.draw_rect(mouth_x + 4, mouth_y + 4, 8, 1, mouth_dark)
            
        elif mouth_style == 'neutral':
            # Straight line
            canvas.draw_rect(mouth_x + 2, mouth_y + 2, 12, 2, mouth_dark)
            
        elif mouth_style == 'laugh':
            # Wide open mouth
            canvas.draw_rect(mouth_x, mouth_y, 16, 6, mouth_dark)
            canvas.draw_rect(mouth_x + 2, mouth_y + 1, 12, 4, mouth_light)
            # Teeth
            white = self.palette.get('clothing', 'white')
            canvas.draw_rect(mouth_x + 4, mouth_y + 1, 8, 2, white)
            
        elif mouth_style == 'small':
            # Small 'o' shape
            canvas.draw_rect(mouth_x + 6, mouth_y + 1, 4, 4, mouth_light)
            canvas.draw_outline_rect(mouth_x + 6, mouth_y + 1, 4, 4, mouth_dark)
            
        else:  # open
            # Slightly open
            canvas.draw_rect(mouth_x + 4, mouth_y, 8, 4, mouth_dark)
            canvas.draw_rect(mouth_x + 5, mouth_y + 1, 6, 2, mouth_light)
    
    def _draw_hair(self, canvas: PixelCanvas):
        """Draw hair based on style"""
        hair_style = self.config['hair_style']
        hair = self.palette.get('hair_colors', self.config['hair_color'])
        shadow = self.palette.get('hair_shadows', self.config['hair_color'])
        highlight = self.palette.get('hair_highlights', self.config['hair_color'])
        outline = self.palette.get('accents', 'outline_black')
        
        if hair_style == 'short_curly':
            self._draw_short_curly_hair(canvas, hair, shadow, highlight, outline)
        elif hair_style == 'buns':
            self._draw_bun_hair(canvas, hair, shadow, highlight, outline)
        elif hair_style == 'long_straight':
            self._draw_long_straight_hair(canvas, hair, shadow, highlight, outline)
        elif hair_style == 'bob':
            self._draw_bob_hair(canvas, hair, shadow, highlight, outline)
        elif hair_style == 'messy':
            self._draw_messy_hair(canvas, hair, shadow, highlight, outline)
        else:  # pixie
            self._draw_pixie_hair(canvas, hair, shadow, highlight, outline)
    
    def _draw_short_curly_hair(self, canvas: PixelCanvas, hair: Tuple, shadow: Tuple, highlight: Tuple, outline: Tuple):
        """Short curly/wavy hair"""
        # Top of head
        canvas.draw_rect(55, 25, 50, 15, hair)
        # Sides
        canvas.draw_rect(50, 35, 10, 25, hair)
        canvas.draw_rect(100, 35, 10, 25, hair)
        # Curly texture
        canvas.draw_rect(60, 27, 8, 3, highlight)
        canvas.draw_rect(75, 30, 8, 3, shadow)
        canvas.draw_rect(90, 28, 8, 3, highlight)
        # Side curls
        canvas.draw_rect(52, 40, 4, 8, shadow)
        canvas.draw_rect(104, 40, 4, 8, shadow)
    
    def _draw_bun_hair(self, canvas: PixelCanvas, hair: Tuple, shadow: Tuple, highlight: Tuple, outline: Tuple):
        """Hair with buns (like reference image)"""
        # Center part
        canvas.draw_rect(70, 30, 20, 12, hair)
        # Left bun
        canvas.draw_rect(45, 30, 18, 18, hair)
        canvas.draw_rect(48, 33, 12, 12, shadow)
        canvas.draw_rect(50, 35, 6, 6, highlight)
        # Right bun
        canvas.draw_rect(97, 30, 18, 18, hair)
        canvas.draw_rect(100, 33, 12, 12, shadow)
        canvas.draw_rect(106, 35, 6, 6, highlight)
        # Hair strands
        canvas.draw_rect(52, 50, 3, 15, hair)
        canvas.draw_rect(105, 50, 3, 15, hair)
        # Outline buns
        canvas.draw_outline_rect(45, 30, 18, 18, outline)
        canvas.draw_outline_rect(97, 30, 18, 18, outline)
    
    def _draw_long_straight_hair(self, canvas: PixelCanvas, hair: Tuple, shadow: Tuple, highlight: Tuple, outline: Tuple):
        """Long straight hair"""
        # Top
        canvas.draw_rect(55, 25, 50, 20, hair)
        # Long sides
        canvas.draw_rect(48, 40, 14, 50, hair)
        canvas.draw_rect(98, 40, 14, 50, hair)
        # Highlights
        canvas.draw_rect(70, 30, 4, 30, highlight)
        canvas.draw_rect(86, 35, 4, 30, highlight)
        # Shadows
        canvas.draw_rect(50, 50, 6, 30, shadow)
        canvas.draw_rect(104, 50, 6, 30, shadow)
    
    def _draw_bob_hair(self, canvas: PixelCanvas, hair: Tuple, shadow: Tuple, highlight: Tuple, outline: Tuple):
        """Bob cut hair"""
        # Top
        canvas.draw_rect(58, 28, 44, 15, hair)
        # Sides (straight bob)
        canvas.draw_rect(48, 40, 15, 35, hair)
        canvas.draw_rect(97, 40, 15, 35, hair)
        # Bangs
        canvas.draw_rect(62, 40, 36, 8, hair)
        canvas.draw_rect(64, 48, 32, 3, shadow)
        # Highlights
        canvas.draw_rect(75, 32, 5, 20, highlight)
    
    def _draw_messy_hair(self, canvas: PixelCanvas, hair: Tuple, shadow: Tuple, highlight: Tuple, outline: Tuple):
        """Messy spiky hair (like reference image boy)"""
        # Base
        canvas.draw_rect(58, 30, 44, 20, hair)
        # Spiky top sections
        for i in range(5):
            x = 60 + i * 8
            canvas.draw_rect(x, 22 + (i % 3) * 2, 6, 8, hair)
            if i % 2 == 0:
                canvas.draw_rect(x + 1, 24, 4, 4, shadow)
            else:
                canvas.draw_rect(x + 1, 24, 4, 4, highlight)
        # Sides
        canvas.draw_rect(50, 35, 10, 20, hair)
        canvas.draw_rect(100, 35, 10, 20, hair)
    
    def _draw_pixie_hair(self, canvas: PixelCanvas, hair: Tuple, shadow: Tuple, highlight: Tuple, outline: Tuple):
        """Short pixie cut"""
        # Very short on top
        canvas.draw_rect(60, 28, 40, 18, hair)
        # Short sides
        canvas.draw_rect(54, 35, 8, 20, hair)
        canvas.draw_rect(98, 35, 8, 20, hair)
        # Texture
        canvas.draw_rect(65, 32, 8, 2, highlight)
        canvas.draw_rect(80, 30, 8, 2, shadow)
        canvas.draw_rect(90, 33, 6, 2, highlight)
    
    def _draw_accessories(self, canvas: PixelCanvas):
        """Draw accessories like glasses, earrings, etc."""
        accessory = self.config['accessory']
        outline = self.palette.get('accents', 'outline_black')
        
        if accessory == 'glasses':
            # Black frame glasses (like reference image)
            # Left lens
            canvas.draw_rect(66, 54, 10, 10, (255, 255, 255, 50))
            canvas.draw_outline_rect(66, 54, 10, 10, outline)
            # Right lens
            canvas.draw_rect(84, 54, 10, 10, (255, 255, 255, 50))
            canvas.draw_outline_rect(84, 54, 10, 10, outline)
            # Bridge
            canvas.draw_rect(76, 58, 8, 2, outline)
            # Temples
            canvas.draw_rect(95, 58, 8, 2, outline)
            canvas.draw_rect(57, 58, 8, 2, outline)
            
        elif accessory == 'earrings':
            # Simple round earrings
            gold = self.palette.get('clothing', 'yellow')
            canvas.draw_rect(56, 62, 3, 3, gold)
            canvas.draw_rect(101, 62, 3, 3, gold)
            canvas.draw_rect(56, 66, 3, 4, gold)
            canvas.draw_rect(101, 66, 3, 4, gold)
            
        elif accessory == 'headband':
            # Colored headband
            band_color = self.palette.get('clothing', 'red')
            canvas.draw_rect(58, 32, 44, 4, band_color)
            # Bow on side
            canvas.draw_rect(102, 30, 6, 8, band_color)
            
        elif accessory == 'bow':
            # Hair bow on top
            bow_color = self.palette.get('clothing', 'red')
            canvas.draw_rect(75, 22, 10, 6, bow_color)
            canvas.draw_rect(77, 24, 2, 2, outline)
            canvas.draw_rect(81, 24, 2, 2, outline)

def setup():
    """Initialize the Pygame window"""
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption("Pixel-Art Avatar Generator - Click to generate | S to save")
    return screen

def main():
    """Main application loop"""
    screen = setup()
    clock = pygame.time.Clock()
    
    # Load color palette
    palette = ColorPalette()
    
    # Create pixel canvas
    canvas = PixelCanvas(LOGICAL_WIDTH, LOGICAL_HEIGHT)
    
    # Create avatar generator
    generator = AvatarGenerator(palette)
    generator.generate_random()
    generator.draw(canvas)
    
    # Display
    scaled_surface = canvas.get_scaled_surface(SCALE_FACTOR)
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()
    
    save_counter = 0
    running = True
    
    print("=" * 60)
    print("Pixel-Art Avatar Generator")
    print("=" * 60)
    print("Controls:")
    print("  - Click anywhere to generate a new random avatar")
    print("  - Press 'S' to save current avatar as PNG")
    print("  - Press 'Q' or close window to quit")
    print("=" * 60)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Generate new random avatar
                generator.generate_random()
                generator.draw(canvas)
                scaled_surface = canvas.get_scaled_surface(SCALE_FACTOR)
                screen.blit(scaled_surface, (0, 0))
                pygame.display.flip()
                print("Generated new avatar")
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    # Save avatar
                    save_counter += 1
                    # Save at 1x (160x160)
                    filename_1x = f"avatar_{save_counter}.png"
                    canvas.save_png(filename_1x, scale=1)
                    # Save at 4x (640x640)
                    filename_4x = f"avatar_{save_counter}_4x.png"
                    canvas.save_png(filename_4x, scale=4)
                    print(f"Saved: {filename_1x} (160x160) and {filename_4x} (640x640)")
                
                elif event.key == pygame.K_q:
                    running = False
        
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
