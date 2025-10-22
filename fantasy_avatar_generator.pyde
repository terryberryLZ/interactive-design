# Fantasy Pixel Avatar Generator
# Click anywhere or press R to generate a new random avatar
# Supports --seed parameter for reproducible generation
# 使用 Processing Python Mode 运行此程序

import random as py_random

# Global variables for avatar components
current_avatar = {}
random_seed = None

# Avatar component options
GENDERS = ["male", "female"]
RACES = ["human", "orc", "elf", "dwarf", "goblin"]
SKIN_COLORS = [
    color(120, 180, 120),  # Green (orc/goblin)
    color(255, 220, 177),  # Light (elf/human)
    color(210, 140, 100),  # Tan (dwarf/human)
    color(180, 255, 180),  # Light green
    color(200, 200, 240),  # Pale blue
    color(255, 200, 150),  # Peach (human)
    color(245, 210, 180),  # Light tan (human)
    color(160, 120, 90),   # Dark tan (human)
]
EXPRESSIONS = ["handsome", "serious", "cute", "goofy"]
HEADWEAR = ["horn_helmet", "flower_crown", "wizard_hat", "tentacle_hat", "headband", "none"]
NECKLACES = ["skull_pendant", "gem_collar", "leaf_necklace", "rune_pendant", "none"]
EARRINGS = ["hoop", "feather", "bone", "stud", "none"]
CLOTHES = ["robe", "armor", "tunic", "cloak", "hoodie"]
BACKGROUNDS = ["solid_purple", "solid_blue", "solid_pink", "gradient_sunset", "gradient_ocean", "pattern_stars", "pattern_dots"]

# Pixel size for drawing (4 pixels = 1 logical pixel, for 512x512 output from 128x128 logical)
PIXEL = 4

def setup():
    global random_seed
    size(512, 512)
    noStroke()
    
    # Check for --seed parameter in command line args (if available)
    # Note: In Processing, command line args are not directly available
    # This is a placeholder for future implementation
    
    generateAvatar()

def draw():
    pass  # Static image, redraw only on click or key press

def mousePressed():
    generateAvatar()

def keyPressed():
    # Press R to regenerate avatar
    if key == 'r' or key == 'R':
        generateAvatar()

def generateAvatar():
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
    drawBackground(current_avatar["background"])
    
    # Draw avatar components in order (back to front)
    drawClothes(current_avatar["clothes"], current_avatar["skin_color"])
    drawHead(current_avatar["race"], current_avatar["skin_color"])
    drawExpression(current_avatar["expression"])
    drawEarrings(current_avatar["earring"])
    drawNecklace(current_avatar["necklace"])
    drawHeadwear(current_avatar["headwear"], current_avatar["race"])

def random_choice(lst):
    """Helper function to pick random item from list"""
    return lst[int(random(len(lst)))]

# ============ Background Drawing Functions ============

def drawBackground(bg_type):
    """Draw background"""
    if bg_type == "solid_purple":
        background(180, 160, 200)
    elif bg_type == "solid_blue":
        background(160, 180, 210)
    elif bg_type == "solid_pink":
        background(240, 200, 220)
    elif bg_type == "gradient_sunset":
        # Orange to purple gradient
        for i in range(128):
            t = float(i) / 128
            r = lerp(255, 150, t)
            g = lerp(180, 100, t)
            b = lerp(100, 180, t)
            fill(r, g, b)
            for j in range(128):
                rect(j * PIXEL, i * PIXEL, PIXEL, PIXEL)
    elif bg_type == "gradient_ocean":
        # Light blue to dark blue gradient
        for i in range(128):
            t = float(i) / 128
            r = lerp(200, 60, t)
            g = lerp(220, 100, t)
            b = lerp(255, 180, t)
            fill(r, g, b)
            for j in range(128):
                rect(j * PIXEL, i * PIXEL, PIXEL, PIXEL)
    elif bg_type == "pattern_stars":
        # Dark background with stars
        background(40, 40, 70)
        fill(255, 255, 200)
        for i in range(20):
            x = int(random(128)) * PIXEL
            y = int(random(128)) * PIXEL
            rect(x, y, PIXEL, PIXEL)
    elif bg_type == "pattern_dots":
        # Light background with dots
        background(230, 230, 250)
        fill(200, 200, 230)
        for i in range(0, 128, 8):
            for j in range(0, 128, 8):
                if (i + j) % 16 == 0:
                    rect(i * PIXEL, j * PIXEL, PIXEL, PIXEL)

# ============ Head Drawing Functions ============

def drawHead(race, skin_col):
    """Draw the head/face based on race"""
    fill(skin_col)
    
    # Head base (all races have similar large head shape)
    # Head is centered around x=256 (64 * 4), y=256 (64 * 4) for 512x512 canvas
    # Using logical coordinates: x_center = 64, y_center = 56 (in logical pixels)
    x_center = 256
    y_center = 224
    
    if race == "human":
        # Balanced, round head
        for i in range(7, 13):
            for j in range(4, 12):
                rect(x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL)
        # Normal ears
        fill(skin_col)
        rect(x_center - 64, y_center + 4, PIXEL * 2, PIXEL * 3)
        rect(x_center + 56, y_center + 4, PIXEL * 2, PIXEL * 3)
    
    elif race == "orc":
        # Broad, square head
        for i in range(6, 14):
            for j in range(3, 13):
                rect(x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL)
        # Tusks
        fill(255, 255, 220)
        rect(x_center - 40, y_center + 20, PIXEL * 2, PIXEL * 3)
        rect(x_center + 32, y_center + 20, PIXEL * 2, PIXEL * 3)
        
    elif race == "elf":
        # Elegant, oval head
        for i in range(7, 13):
            for j in range(4, 12):
                rect(x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL)
        # Pointed ears
        fill(skin_col)
        rect(x_center - 72, y_center, PIXEL * 2, PIXEL * 2)
        rect(x_center - 88, y_center - 8, PIXEL * 2, PIXEL * 2)
        rect(x_center + 64, y_center, PIXEL * 2, PIXEL * 2)
        rect(x_center + 80, y_center - 8, PIXEL * 2, PIXEL * 2)
        
    elif race == "dwarf":
        # Stocky, round head with beard
        for i in range(7, 13):
            for j in range(5, 11):
                rect(x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL)
        # Beard
        fill(100, 60, 30)  # Brown beard
        for i in range(7, 13):
            for j in range(10, 14):
                rect(x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL)
                
    elif race == "goblin":
        # Small, pointy head
        for i in range(7, 13):
            for j in range(5, 12):
                rect(x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL)
        # Large ears
        fill(skin_col)
        rect(x_center - 72, y_center + 8, PIXEL * 2, PIXEL * 3)
        rect(x_center + 64, y_center + 8, PIXEL * 2, PIXEL * 3)
    
    # Draw eyes (all races)
    fill(255)  # White
    rect(x_center - 32, y_center + 8, PIXEL * 3, PIXEL * 2)
    rect(x_center + 16, y_center + 8, PIXEL * 3, PIXEL * 2)
    fill(0)  # Black pupils
    rect(x_center - 24, y_center + 8, PIXEL, PIXEL)
    rect(x_center + 24, y_center + 8, PIXEL, PIXEL)

def drawExpression(expression):
    """Draw facial expression"""
    x_center = 256
    y_center = 224
    
    fill(0)
    
    if expression == "handsome":
        # Confident smile with raised eyebrows
        rect(x_center - 16, y_center + 32, PIXEL * 4, PIXEL)
        rect(x_center - 24, y_center + 24, PIXEL, PIXEL)
        rect(x_center + 16, y_center + 24, PIXEL, PIXEL)
        # Raised eyebrows
        rect(x_center - 40, y_center - 4, PIXEL * 3, PIXEL)
        rect(x_center + 24, y_center - 4, PIXEL * 3, PIXEL)
        
    elif expression == "serious":
        # Straight mouth with stern eyebrows
        rect(x_center - 16, y_center + 32, PIXEL * 4, PIXEL)
        # Furrowed eyebrows
        rect(x_center - 40, y_center, PIXEL * 3, PIXEL)
        rect(x_center + 24, y_center, PIXEL * 3, PIXEL)
        
    elif expression == "cute":
        # Round mouth
        fill(255, 150, 150)
        rect(x_center - 8, y_center + 28, PIXEL * 2, PIXEL * 2)
        # Blush
        fill(255, 180, 180, 150)
        rect(x_center - 48, y_center + 24, PIXEL * 2, PIXEL)
        rect(x_center + 40, y_center + 24, PIXEL * 2, PIXEL)
        
    elif expression == "goofy":
        # Tongue out with one eye closed
        fill(255, 100, 120)
        rect(x_center - 8, y_center + 32, PIXEL * 2, PIXEL * 2)
        # One eye wink
        fill(0)
        rect(x_center - 32, y_center + 8, PIXEL * 3, PIXEL)
        # Silly raised eyebrow on other side
        rect(x_center + 24, y_center - 4, PIXEL * 3, PIXEL)

# ============ Accessory Drawing Functions ============

def drawHeadwear(headwear_type, race):
    """Draw headwear"""
    x_center = 256
    y_center = 224
    
    if headwear_type == "headband":
        # Simple headband
        fill(200, 150, 100)
        for i in range(7, 13):
            rect(x_center - 80 + i * PIXEL, y_center - 16, PIXEL, PIXEL)
        # Small decoration
        fill(255, 200, 100)
        rect(x_center - 4, y_center - 16, PIXEL, PIXEL)
    
    elif headwear_type == "horn_helmet":
        # Metal helmet
        fill(150, 150, 150)
        for i in range(7, 13):
            for j in range(3, 6):
                rect(x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL)
        # Horns
        fill(240, 240, 220)
        rect(x_center - 64, y_center - 40, PIXEL * 2, PIXEL * 4)
        rect(x_center + 56, y_center - 40, PIXEL * 2, PIXEL * 4)
        rect(x_center - 72, y_center - 56, PIXEL * 2, PIXEL * 2)
        rect(x_center + 64, y_center - 56, PIXEL * 2, PIXEL * 2)
        
    elif headwear_type == "flower_crown":
        # Flowers
        fill(255, 100, 150)
        rect(x_center - 48, y_center - 32, PIXEL * 2, PIXEL * 2)
        fill(255, 200, 100)
        rect(x_center - 16, y_center - 40, PIXEL * 2, PIXEL * 2)
        fill(150, 100, 255)
        rect(x_center + 24, y_center - 32, PIXEL * 2, PIXEL * 2)
        # Leaves
        fill(100, 200, 100)
        for i in range(7, 13):
            rect(x_center - 80 + i * PIXEL, y_center - 24, PIXEL, PIXEL)
            
    elif headwear_type == "wizard_hat":
        # Tall pointed hat
        fill(50, 50, 120)
        # Brim
        for i in range(6, 14):
            rect(x_center - 80 + i * PIXEL, y_center - 24, PIXEL, PIXEL)
        # Cone
        for i in range(8, 12):
            for j in range(5, 12):
                if j < 9 - abs(i - 10):
                    rect(x_center - 80 + i * PIXEL, y_center - 40 - j * PIXEL, PIXEL, PIXEL)
        # Star decoration
        fill(255, 255, 100)
        rect(x_center - 8, y_center - 64, PIXEL, PIXEL)
        
    elif headwear_type == "tentacle_hat":
        # Octopus-like hat
        fill(200, 100, 200)
        # Main body
        for i in range(7, 13):
            for j in range(3, 6):
                rect(x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL)
        # Tentacles
        rect(x_center - 56, y_center - 16, PIXEL, PIXEL * 3)
        rect(x_center - 32, y_center - 24, PIXEL, PIXEL * 3)
        rect(x_center + 24, y_center - 24, PIXEL, PIXEL * 3)
        rect(x_center + 48, y_center - 16, PIXEL, PIXEL * 3)

def drawNecklace(necklace_type):
    """Draw necklace"""
    x_center = 256
    y_center = 224
    
    if necklace_type == "rune_pendant":
        # Chain
        fill(150, 150, 170)
        for i in range(8, 12):
            rect(x_center - 80 + i * PIXEL, y_center + 64, PIXEL, PIXEL)
        # Glowing rune
        fill(100, 200, 255)
        rect(x_center - 16, y_center + 72, PIXEL * 4, PIXEL * 3)
        fill(200, 230, 255)
        rect(x_center - 8, y_center + 76, PIXEL, PIXEL)
    
    elif necklace_type == "skull_pendant":
        # Chain
        fill(200, 200, 200)
        for i in range(8, 12):
            rect(x_center - 80 + i * PIXEL, y_center + 64, PIXEL, PIXEL)
        # Skull
        fill(240, 240, 230)
        rect(x_center - 16, y_center + 72, PIXEL * 4, PIXEL * 3)
        fill(0)
        rect(x_center - 8, y_center + 72, PIXEL, PIXEL)
        rect(x_center + 8, y_center + 72, PIXEL, PIXEL)
        
    elif necklace_type == "gem_collar":
        # Gold collar
        fill(255, 215, 0)
        for i in range(7, 13):
            rect(x_center - 80 + i * PIXEL, y_center + 64, PIXEL, PIXEL)
        # Gems
        fill(255, 50, 50)
        rect(x_center - 32, y_center + 64, PIXEL, PIXEL)
        fill(50, 50, 255)
        rect(x_center, y_center + 64, PIXEL, PIXEL)
        fill(50, 255, 50)
        rect(x_center + 24, y_center + 64, PIXEL, PIXEL)
        
    elif necklace_type == "leaf_necklace":
        # Vine
        fill(100, 150, 80)
        for i in range(8, 12):
            rect(x_center - 80 + i * PIXEL, y_center + 64, PIXEL, PIXEL)
        # Leaves
        fill(120, 200, 100)
        rect(x_center - 24, y_center + 72, PIXEL * 2, PIXEL * 2)
        rect(x_center + 8, y_center + 72, PIXEL * 2, PIXEL * 2)

def drawEarrings(earring_type):
    """Draw earrings"""
    x_center = 256
    y_center = 224
    
    if earring_type == "stud":
        # Small stud earrings
        fill(255, 215, 0)
        rect(x_center - 64, y_center + 16, PIXEL, PIXEL)
        rect(x_center + 56, y_center + 16, PIXEL, PIXEL)
        # Shine effect
        fill(255, 255, 200)
        rect(x_center - 64, y_center + 16, PIXEL // 2, PIXEL // 2)
        rect(x_center + 56, y_center + 16, PIXEL // 2, PIXEL // 2)
    
    elif earring_type == "hoop":
        # Gold hoops
        fill(255, 215, 0)
        rect(x_center - 64, y_center + 16, PIXEL, PIXEL * 3)
        rect(x_center + 56, y_center + 16, PIXEL, PIXEL * 3)
        rect(x_center - 72, y_center + 24, PIXEL, PIXEL)
        rect(x_center + 64, y_center + 24, PIXEL, PIXEL)
        
    elif earring_type == "feather":
        # Feather earrings
        fill(100, 200, 200)
        rect(x_center - 64, y_center + 16, PIXEL, PIXEL * 4)
        rect(x_center + 56, y_center + 16, PIXEL, PIXEL * 4)
        rect(x_center - 72, y_center + 24, PIXEL, PIXEL * 2)
        rect(x_center + 64, y_center + 24, PIXEL, PIXEL * 2)
        
    elif earring_type == "bone":
        # Bone earrings
        fill(240, 240, 220)
        rect(x_center - 64, y_center + 16, PIXEL * 2, PIXEL * 3)
        rect(x_center + 56, y_center + 16, PIXEL * 2, PIXEL * 3)

def drawClothes(clothes_type, skin_col):
    """Draw clothing/armor"""
    x_center = 256
    y_center = 224
    
    if clothes_type == "hoodie":
        # Modern hoodie
        fill(80, 80, 100)
        for i in range(6, 14):
            for j in range(13, 20):
                rect(x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL)
        # Hood
        for i in range(7, 13):
            for j in range(3, 5):
                rect(x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL)
        # Drawstrings
        fill(200, 200, 200)
        rect(x_center - 16, y_center + 28, PIXEL, PIXEL * 2)
        rect(x_center + 8, y_center + 28, PIXEL, PIXEL * 2)
    
    elif clothes_type == "robe":
        # Flowing robe
        fill(80, 60, 140)
        for i in range(6, 14):
            for j in range(13, 20):
                rect(x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL)
        # Belt
        fill(150, 100, 50)
        for i in range(7, 13):
            rect(x_center - 80 + i * PIXEL, y_center + 48, PIXEL, PIXEL)
            
    elif clothes_type == "armor":
        # Plate armor
        fill(180, 180, 200)
        for i in range(7, 13):
            for j in range(13, 19):
                rect(x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL)
        # Armor details
        fill(120, 120, 140)
        for i in range(8, 12):
            rect(x_center - 80 + i * PIXEL, y_center + 40, PIXEL, PIXEL)
            
    elif clothes_type == "tunic":
        # Simple tunic
        fill(150, 100, 60)
        for i in range(7, 13):
            for j in range(13, 19):
                rect(x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL)
        # Collar
        fill(skin_col)
        for i in range(8, 12):
            rect(x_center - 80 + i * PIXEL, y_center + 24, PIXEL, PIXEL)
            
    elif clothes_type == "cloak":
        # Mysterious cloak
        fill(40, 40, 60)
        # Shoulders
        for i in range(6, 14):
            for j in range(12, 20):
                if i < 8 or i > 11:
                    rect(x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL)
        # Center
        for i in range(8, 12):
            for j in range(13, 19):
                rect(x_center - 80 + i * PIXEL, y_center - 40 + j * PIXEL, PIXEL, PIXEL)
        # Clasp
        fill(255, 215, 0)
        rect(x_center - 8, y_center + 24, PIXEL * 2, PIXEL)
