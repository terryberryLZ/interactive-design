"""
Fantasy Avatar Renderer - High-quality SVG-based rendering module
Generates fantasy-style avatar components using vector graphics
"""

import io
import math
import random
from PIL import Image
import pygame

# Try to import cairosvg, if not available, fall back to simple mode
try:
    import cairosvg
    CAIRO_AVAILABLE = True
except ImportError:
    CAIRO_AVAILABLE = False
    print("Warning: cairosvg not available. Install with: pip install cairosvg")

# Cache for rendered surfaces
_SURFACE_CACHE = {}


def pil_to_pygame(img):
    """Convert PIL Image to pygame Surface"""
    mode = img.mode
    size = img.size
    data = img.tobytes()
    return pygame.image.fromstring(data, size, mode).convert_alpha()


def svg_to_pil(svg_text, size=(512, 512)):
    """Render SVG text to PIL Image"""
    if not CAIRO_AVAILABLE:
        # Fallback: create a simple colored surface
        return Image.new("RGBA", size, (200, 200, 200, 255))
    
    try:
        png_bytes = cairosvg.svg2png(
            bytestring=svg_text.encode('utf-8'),
            output_width=size[0],
            output_height=size[1]
        )
        return Image.open(io.BytesIO(png_bytes)).convert("RGBA")
    except Exception as e:
        print(f"SVG rendering error: {e}")
        return Image.new("RGBA", size, (200, 200, 200, 255))


def render_svg_to_surface(name, svg_text, size=(512, 512)):
    """Render SVG to pygame Surface with caching"""
    key = (name, size)
    if key in _SURFACE_CACHE:
        return _SURFACE_CACHE[key]
    
    pil_img = svg_to_pil(svg_text, size)
    surf = pil_to_pygame(pil_img)
    _SURFACE_CACHE[key] = surf
    return surf


def generate_background_svg(bg_type, width=512, height=512):
    """Generate fantasy background in SVG"""
    svg_parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">']
    
    if bg_type == "solid_purple":
        svg_parts.append(f'<rect width="100%" height="100%" fill="rgb(180,160,200)"/>')
    
    elif bg_type == "solid_blue":
        svg_parts.append(f'<rect width="100%" height="100%" fill="rgb(160,180,210)"/>')
    
    elif bg_type == "solid_pink":
        svg_parts.append(f'<rect width="100%" height="100%" fill="rgb(240,200,220)"/>')
    
    elif bg_type == "gradient_sunset":
        svg_parts.append('''
            <defs>
                <linearGradient id="sunset" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:rgb(255,180,100);stop-opacity:1" />
                    <stop offset="100%" style="stop-color:rgb(150,100,180);stop-opacity:1" />
                </linearGradient>
            </defs>
            <rect width="100%" height="100%" fill="url(#sunset)"/>
        ''')
    
    elif bg_type == "gradient_ocean":
        svg_parts.append('''
            <defs>
                <linearGradient id="ocean" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:rgb(200,220,255);stop-opacity:1" />
                    <stop offset="100%" style="stop-color:rgb(60,100,180);stop-opacity:1" />
                </linearGradient>
            </defs>
            <rect width="100%" height="100%" fill="url(#ocean)"/>
        ''')
    
    elif bg_type == "pattern_stars":
        svg_parts.append('<rect width="100%" height="100%" fill="rgb(40,40,70)"/>')
        # Add stars
        random.seed(42)  # Consistent stars
        for _ in range(30):
            x = random.randint(20, width - 20)
            y = random.randint(20, height - 20)
            r = random.randint(1, 3)
            opacity = random.uniform(0.5, 1.0)
            svg_parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="rgb(255,255,200)" opacity="{opacity}"/>')
    
    elif bg_type == "pattern_dots":
        svg_parts.append('<rect width="100%" height="100%" fill="rgb(230,230,250)"/>')
        # Add dots
        for x in range(0, width, 32):
            for y in range(0, height, 32):
                if (x + y) % 64 == 0:
                    svg_parts.append(f'<circle cx="{x}" cy="{y}" r="4" fill="rgb(200,200,230)"/>')
    
    svg_parts.append('</svg>')
    return ''.join(svg_parts)


def generate_head_svg(race, skin_color, width=512, height=512):
    """Generate fantasy head/face in SVG"""
    svg_parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">']
    
    cx, cy = width // 2, height // 2 - 30
    skin_rgb = f"rgb({skin_color[0]},{skin_color[1]},{skin_color[2]})"
    
    if race == "human":
        # Oval face with smooth features
        svg_parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="85" ry="110" fill="{skin_rgb}" stroke="rgba(0,0,0,0.1)" stroke-width="2"/>')
        # Ears
        svg_parts.append(f'<ellipse cx="{cx-85}" cy="{cy+10}" rx="15" ry="25" fill="{skin_rgb}"/>')
        svg_parts.append(f'<ellipse cx="{cx+85}" cy="{cy+10}" rx="15" ry="25" fill="{skin_rgb}"/>')
        # Neck
        svg_parts.append(f'<rect x="{cx-35}" y="{cy+90}" width="70" height="60" fill="{skin_rgb}"/>')
        
    elif race == "orc":
        # Broad, strong face
        svg_parts.append(f'<rect x="{cx-95}" y="{cy-100}" width="190" height="200" rx="30" fill="{skin_rgb}" stroke="rgba(0,0,0,0.2)" stroke-width="3"/>')
        # Tusks
        svg_parts.append(f'<path d="M {cx-40} {cy+40} L {cx-45} {cy+80} L {cx-30} {cy+75} Z" fill="rgb(255,255,220)" stroke="rgb(200,200,180)" stroke-width="2"/>')
        svg_parts.append(f'<path d="M {cx+40} {cy+40} L {cx+45} {cy+80} L {cx+30} {cy+75} Z" fill="rgb(255,255,220)" stroke="rgb(200,200,180)" stroke-width="2"/>')
        # Neck
        svg_parts.append(f'<rect x="{cx-45}" y="{cy+90}" width="90" height="60" fill="{skin_rgb}"/>')
        
    elif race == "elf":
        # Elegant, elongated face
        svg_parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="80" ry="115" fill="{skin_rgb}" stroke="rgba(0,0,0,0.05)" stroke-width="1"/>')
        # Pointed ears
        svg_parts.append(f'<path d="M {cx-80} {cy-10} L {cx-110} {cy-30} L {cx-85} {cy+20} Z" fill="{skin_rgb}" stroke="rgba(0,0,0,0.1)" stroke-width="1"/>')
        svg_parts.append(f'<path d="M {cx+80} {cy-10} L {cx+110} {cy-30} L {cx+85} {cy+20} Z" fill="{skin_rgb}" stroke="rgba(0,0,0,0.1)" stroke-width="1"/>')
        # Neck
        svg_parts.append(f'<rect x="{cx-30}" y="{cy+95}" width="60" height="55" fill="{skin_rgb}"/>')
        
    elif race == "dwarf":
        # Stocky, round face
        svg_parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="90" ry="95" fill="{skin_rgb}" stroke="rgba(0,0,0,0.15)" stroke-width="2"/>')
        # Ears
        svg_parts.append(f'<ellipse cx="{cx-85}" cy="{cy+5}" rx="12" ry="22" fill="{skin_rgb}"/>')
        svg_parts.append(f'<ellipse cx="{cx+85}" cy="{cy+5}" rx="12" ry="22" fill="{skin_rgb}"/>')
        # Beard
        svg_parts.append(f'<ellipse cx="{cx}" cy="{cy+70}" rx="95" ry="60" fill="rgb(100,60,30)"/>')
        svg_parts.append(f'<ellipse cx="{cx}" cy="{cy+80}" rx="85" ry="50" fill="rgb(120,70,35)"/>')
        # Mustache
        svg_parts.append(f'<ellipse cx="{cx-30}" cy="{cy+35}" rx="35" ry="15" fill="rgb(100,60,30)"/>')
        svg_parts.append(f'<ellipse cx="{cx+30}" cy="{cy+35}" rx="35" ry="15" fill="rgb(100,60,30)"/>')
        # Neck
        svg_parts.append(f'<rect x="{cx-40}" y="{cy+90}" width="80" height="60" fill="{skin_rgb}"/>')
        
    elif race == "goblin":
        # Small, angular face
        svg_parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="75" ry="95" fill="{skin_rgb}" stroke="rgba(0,0,0,0.2)" stroke-width="2"/>')
        # Large ears
        svg_parts.append(f'<ellipse cx="{cx-85}" cy="{cy+15}" rx="20" ry="40" fill="{skin_rgb}" stroke="rgba(0,0,0,0.15)" stroke-width="1"/>')
        svg_parts.append(f'<ellipse cx="{cx+85}" cy="{cy+15}" rx="20" ry="40" fill="{skin_rgb}" stroke="rgba(0,0,0,0.15)" stroke-width="1"/>')
        # Neck
        svg_parts.append(f'<rect x="{cx-30}" y="{cy+85}" width="60" height="65" fill="{skin_rgb}"/>')
    
    # Eyes (for all races)
    svg_parts.append(f'<ellipse cx="{cx-35}" cy="{cy-10}" rx="22" ry="18" fill="white" stroke="rgba(0,0,0,0.3)" stroke-width="1"/>')
    svg_parts.append(f'<ellipse cx="{cx+35}" cy="{cy-10}" rx="22" ry="18" fill="white" stroke="rgba(0,0,0,0.3)" stroke-width="1"/>')
    svg_parts.append(f'<circle cx="{cx-35}" cy="{cy-10}" r="8" fill="rgb(80,120,180)"/>')
    svg_parts.append(f'<circle cx="{cx+35}" cy="{cy-10}" r="8" fill="rgb(80,120,180)"/>')
    svg_parts.append(f'<circle cx="{cx-32}" cy="{cy-12}" r="3" fill="black"/>')
    svg_parts.append(f'<circle cx="{cx+38}" cy="{cy-12}" r="3" fill="black"/>')
    # Eye highlights
    svg_parts.append(f'<circle cx="{cx-30}" cy="{cy-15}" r="4" fill="white" opacity="0.8"/>')
    svg_parts.append(f'<circle cx="{cx+40}" cy="{cy-15}" r="4" fill="white" opacity="0.8"/>')
    
    svg_parts.append('</svg>')
    return ''.join(svg_parts)


def generate_expression_svg(expression, width=512, height=512):
    """Generate facial expression overlay in SVG"""
    svg_parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">']
    
    cx, cy = width // 2, height // 2 - 30
    
    if expression == "handsome":
        # Confident smile
        svg_parts.append(f'<path d="M {cx-40} {cy+40} Q {cx} {cy+55} {cx+40} {cy+40}" stroke="rgb(100,50,50)" stroke-width="3" fill="none" stroke-linecap="round"/>')
        # Raised eyebrows
        svg_parts.append(f'<path d="M {cx-55} {cy-45} Q {cx-35} {cy-50} {cx-15} {cy-45}" stroke="rgb(80,50,40)" stroke-width="3" fill="none" stroke-linecap="round"/>')
        svg_parts.append(f'<path d="M {cx+15} {cy-45} Q {cx+35} {cy-50} {cx+55} {cy-45}" stroke="rgb(80,50,40)" stroke-width="3" fill="none" stroke-linecap="round"/>')
        
    elif expression == "serious":
        # Straight mouth
        svg_parts.append(f'<line x1="{cx-35}" y1="{cy+45}" x2="{cx+35}" y2="{cy+45}" stroke="rgb(100,50,50)" stroke-width="3" stroke-linecap="round"/>')
        # Furrowed brows
        svg_parts.append(f'<path d="M {cx-55} {cy-40} L {cx-20} {cy-48}" stroke="rgb(80,50,40)" stroke-width="3.5" stroke-linecap="round"/>')
        svg_parts.append(f'<path d="M {cx+55} {cy-40} L {cx+20} {cy-48}" stroke="rgb(80,50,40)" stroke-width="3.5" stroke-linecap="round"/>')
        
    elif expression == "cute":
        # Small smile
        svg_parts.append(f'<ellipse cx="{cx}" cy="{cy+42}" rx="18" ry="12" fill="rgb(255,150,150)"/>')
        # Blush
        svg_parts.append(f'<ellipse cx="{cx-55}" cy="{cy+25}" rx="20" ry="12" fill="rgb(255,180,180)" opacity="0.6"/>')
        svg_parts.append(f'<ellipse cx="{cx+55}" cy="{cy+25}" rx="20" ry="12" fill="rgb(255,180,180)" opacity="0.6"/>')
        # Sparkles
        svg_parts.append(f'<circle cx="{cx-70}" cy="{cy-60}" r="3" fill="rgb(255,200,220)" opacity="0.8"/>')
        svg_parts.append(f'<circle cx="{cx+70}" cy="{cy-60}" r="3" fill="rgb(255,200,220)" opacity="0.8"/>')
        
    elif expression == "goofy":
        # Tongue out
        svg_parts.append(f'<ellipse cx="{cx}" cy="{cy+50}" rx="15" ry="20" fill="rgb(255,100,120)"/>')
        svg_parts.append(f'<line x1="{cx}" y1="{cy+35}" x2="{cx}" y2="{cy+55}" stroke="rgb(200,80,100)" stroke-width="2"/>')
        # One eye wink
        svg_parts.append(f'<line x1="{cx-50}" y1="{cy-10}" x2="{cx-20}" y2="{cy-10}" stroke="rgb(50,30,20)" stroke-width="3" stroke-linecap="round"/>')
        # Raised eyebrow
        svg_parts.append(f'<path d="M {cx+15} {cy-50} Q {cx+35} {cy-55} {cx+55} {cy-48}" stroke="rgb(80,50,40)" stroke-width="3" fill="none" stroke-linecap="round"/>')
    
    svg_parts.append('</svg>')
    return ''.join(svg_parts)


def generate_headwear_svg(headwear_type, race, width=512, height=512):
    """Generate headwear in SVG"""
    if headwear_type == "none":
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"></svg>'
    
    svg_parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">']
    
    cx, cy = width // 2, height // 2 - 30
    
    if headwear_type == "headband":
        # Decorative headband
        svg_parts.append(f'<ellipse cx="{cx}" cy="{cy-70}" rx="90" ry="12" fill="rgb(200,150,100)" stroke="rgb(180,130,80)" stroke-width="2"/>')
        svg_parts.append(f'<circle cx="{cx}" cy="{cy-70}" r="10" fill="rgb(255,200,100)" stroke="rgb(220,170,60)" stroke-width="2"/>')
        # Decorative gems
        svg_parts.append(f'<circle cx="{cx-25}" cy="{cy-70}" r="5" fill="rgb(100,200,255)" opacity="0.8"/>')
        svg_parts.append(f'<circle cx="{cx+25}" cy="{cy-70}" r="5" fill="rgb(255,100,200)" opacity="0.8"/>')
    
    elif headwear_type == "horn_helmet":
        # Metal helmet
        svg_parts.append(f'<ellipse cx="{cx}" cy="{cy-75}" rx="100" ry="40" fill="rgb(150,150,150)" stroke="rgb(100,100,100)" stroke-width="3"/>')
        svg_parts.append(f'<rect x="{cx-95}" y="{cy-90}" width="190" height="30" rx="5" fill="rgb(170,170,170)" stroke="rgb(120,120,120)" stroke-width="2"/>')
        # Horns
        svg_parts.append(f'<path d="M {cx-70} {cy-90} Q {cx-85} {cy-140} {cx-75} {cy-160}" stroke="rgb(240,240,220)" stroke-width="15" fill="none" stroke-linecap="round"/>')
        svg_parts.append(f'<path d="M {cx+70} {cy-90} Q {cx+85} {cy-140} {cx+75} {cy-160}" stroke="rgb(240,240,220)" stroke-width="15" fill="none" stroke-linecap="round"/>')
        # Metal shine
        svg_parts.append(f'<ellipse cx="{cx-30}" cy="{cy-80}" rx="20" ry="10" fill="rgb(200,200,220)" opacity="0.5"/>')
        
    elif headwear_type == "flower_crown":
        # Flower crown base
        svg_parts.append(f'<ellipse cx="{cx}" cy="{cy-75}" rx="95" ry="10" fill="rgb(100,200,100)" stroke="rgb(80,160,80)" stroke-width="2"/>')
        # Flowers
        flowers = [
            (cx-60, cy-85, "rgb(255,100,150)"),
            (cx-30, cy-90, "rgb(255,200,100)"),
            (cx, cy-92, "rgb(200,100,255)"),
            (cx+30, cy-90, "rgb(255,150,200)"),
            (cx+60, cy-85, "rgb(255,220,120)")
        ]
        for fx, fy, color in flowers:
            for angle in range(0, 360, 72):
                rad = math.radians(angle)
                px = fx + 8 * math.cos(rad)
                py = fy + 8 * math.sin(rad)
                svg_parts.append(f'<circle cx="{px}" cy="{py}" r="5" fill="{color}" opacity="0.9"/>')
            svg_parts.append(f'<circle cx="{fx}" cy="{fy}" r="4" fill="rgb(255,255,100)"/>')
    
    elif headwear_type == "wizard_hat":
        # Wizard hat
        # Brim
        svg_parts.append(f'<ellipse cx="{cx}" cy="{cy-75}" rx="110" ry="15" fill="rgb(50,50,120)" stroke="rgb(30,30,80)" stroke-width="2"/>')
        # Cone
        svg_parts.append(f'<path d="M {cx-80} {cy-75} L {cx} {cy-220} L {cx+80} {cy-75} Z" fill="rgb(50,50,120)" stroke="rgb(30,30,80)" stroke-width="2"/>')
        # Stars decoration
        for i, (sx, sy) in enumerate([(cx-20, cy-140), (cx+15, cy-170), (cx, cy-200)]):
            svg_parts.append(f'<path d="M {sx} {sy-8} L {sx+2} {sy-2} L {sx+8} {sy} L {sx+2} {sy+2} L {sx} {sy+8} L {sx-2} {sy+2} L {sx-8} {sy} L {sx-2} {sy-2} Z" fill="rgb(255,255,100)" stroke="rgb(220,220,60)" stroke-width="1"/>')
        
    elif headwear_type == "tentacle_hat":
        # Octopus-like hat
        svg_parts.append(f'<ellipse cx="{cx}" cy="{cy-80}" rx="95" ry="45" fill="rgb(200,100,200)" stroke="rgb(160,80,160)" stroke-width="2"/>')
        # Tentacles
        tentacles = [
            (cx-70, cy-70, -30),
            (cx-40, cy-80, -15),
            (cx+40, cy-80, 15),
            (cx+70, cy-70, 30)
        ]
        for tx, ty, angle in tentacles:
            svg_parts.append(f'<path d="M {tx} {ty} Q {tx+angle} {ty+30} {tx+angle*0.7} {ty+60}" stroke="rgb(200,100,200)" stroke-width="12" fill="none" stroke-linecap="round"/>')
            # Suckers
            for i in range(3):
                sy = ty + 20 + i * 15
                svg_parts.append(f'<circle cx="{tx+angle*0.5}" cy="{sy}" r="4" fill="rgb(220,140,220)" opacity="0.7"/>')
    
    svg_parts.append('</svg>')
    return ''.join(svg_parts)


def generate_necklace_svg(necklace_type, width=512, height=512):
    """Generate necklace in SVG"""
    if necklace_type == "none":
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"></svg>'
    
    svg_parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">']
    
    cx, cy = width // 2, height // 2 + 100
    
    if necklace_type == "rune_pendant":
        # Chain
        svg_parts.append(f'<path d="M {cx-60} {cy-30} Q {cx} {cy-20} {cx+60} {cy-30}" stroke="rgb(150,150,170)" stroke-width="3" fill="none"/>')
        # Glowing rune pendant
        svg_parts.append(f'<rect x="{cx-25}" y="{cy-10}" width="50" height="40" rx="5" fill="rgb(100,200,255)" stroke="rgb(80,180,235)" stroke-width="2"/>')
        svg_parts.append(f'<circle cx="{cx}" cy="{cy+10}" r="12" fill="rgb(200,230,255)" opacity="0.7"/>')
        # Rune symbol
        svg_parts.append(f'<path d="M {cx-10} {cy-5} L {cx+10} {cy-5} M {cx} {cy-5} L {cx} {cy+20}" stroke="rgb(255,255,255)" stroke-width="3" opacity="0.9"/>')
    
    elif necklace_type == "skull_pendant":
        # Chain
        svg_parts.append(f'<path d="M {cx-60} {cy-30} Q {cx} {cy-20} {cx+60} {cy-30}" stroke="rgb(200,200,200)" stroke-width="3" fill="none"/>')
        # Skull
        svg_parts.append(f'<ellipse cx="{cx}" cy="{cy+5}" rx="22" ry="25" fill="rgb(240,240,230)" stroke="rgb(200,200,190)" stroke-width="2"/>')
        svg_parts.append(f'<circle cx="{cx-8}" cy="{cy}" r="5" fill="rgb(50,50,50)"/>')
        svg_parts.append(f'<circle cx="{cx+8}" cy="{cy}" r="5" fill="rgb(50,50,50)"/>')
        svg_parts.append(f'<path d="M {cx-5} {cy+12} L {cx} {cy+18} L {cx+5} {cy+12}" stroke="rgb(50,50,50)" stroke-width="2" fill="none"/>')
    
    elif necklace_type == "gem_collar":
        # Gold collar
        svg_parts.append(f'<ellipse cx="{cx}" cy="{cy-25}" rx="85" ry="12" fill="rgb(255,215,0)" stroke="rgb(220,180,0)" stroke-width="2"/>')
        # Gems
        gems = [
            (cx-45, cy-25, "rgb(255,50,50)"),
            (cx-15, cy-25, "rgb(50,50,255)"),
            (cx+15, cy-25, "rgb(50,255,50)"),
            (cx+45, cy-25, "rgb(255,50,255)")
        ]
        for gx, gy, color in gems:
            svg_parts.append(f'<circle cx="{gx}" cy="{gy}" r="8" fill="{color}" stroke="rgba(0,0,0,0.3)" stroke-width="1"/>')
            svg_parts.append(f'<circle cx="{gx-2}" cy="{gy-2}" r="3" fill="white" opacity="0.6"/>')
    
    elif necklace_type == "leaf_necklace":
        # Vine
        svg_parts.append(f'<path d="M {cx-70} {cy-30} Q {cx} {cy-15} {cx+70} {cy-30}" stroke="rgb(100,150,80)" stroke-width="4" fill="none"/>')
        # Leaves
        leaves = [(cx-40, cy-20), (cx-15, cy-12), (cx+15, cy-12), (cx+40, cy-20)]
        for lx, ly in leaves:
            svg_parts.append(f'<ellipse cx="{lx}" cy="{ly}" rx="12" ry="18" fill="rgb(120,200,100)" stroke="rgb(90,160,70)" stroke-width="1" transform="rotate(25 {lx} {ly})"/>')
            svg_parts.append(f'<line x1="{lx}" y1="{ly-15}" x2="{lx}" y2="{ly+15}" stroke="rgb(90,160,70)" stroke-width="1.5"/>')
    
    svg_parts.append('</svg>')
    return ''.join(svg_parts)


def generate_earrings_svg(earring_type, width=512, height=512):
    """Generate earrings in SVG"""
    if earring_type == "none":
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"></svg>'
    
    svg_parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">']
    
    cx, cy = width // 2, height // 2 - 30
    
    if earring_type == "stud":
        # Gold studs
        for ex in [cx-90, cx+90]:
            svg_parts.append(f'<circle cx="{ex}" cy="{cy+10}" r="6" fill="rgb(255,215,0)" stroke="rgb(220,180,0)" stroke-width="1"/>')
            svg_parts.append(f'<circle cx="{ex-2}" cy="{cy+8}" r="2" fill="white" opacity="0.8"/>')
    
    elif earring_type == "hoop":
        # Gold hoops
        for ex in [cx-90, cx+90]:
            svg_parts.append(f'<ellipse cx="{ex}" cy="{cy+25}" rx="8" ry="18" fill="none" stroke="rgb(255,215,0)" stroke-width="4"/>')
            svg_parts.append(f'<circle cx="{ex}" cy="{cy+10}" r="4" fill="rgb(255,215,0)"/>')
    
    elif earring_type == "feather":
        # Feather earrings
        for ex in [cx-92, cx+92]:
            direction = 1 if ex > cx else -1
            svg_parts.append(f'<path d="M {ex} {cy+12} L {ex+direction*3} {cy+40}" stroke="rgb(100,200,200)" stroke-width="3" stroke-linecap="round"/>')
            # Feather details
            for i in range(4):
                fy = cy + 15 + i * 7
                svg_parts.append(f'<line x1="{ex+direction*3}" y1="{fy}" x2="{ex+direction*12}" y2="{fy+3}" stroke="rgb(100,200,200)" stroke-width="2" opacity="0.7"/>')
    
    elif earring_type == "bone":
        # Bone earrings
        for ex in [cx-92, cx+92]:
            svg_parts.append(f'<rect x="{ex-4}" y="{cy+12}" width="8" height="25" rx="2" fill="rgb(240,240,220)" stroke="rgb(200,200,180)" stroke-width="1"/>')
            svg_parts.append(f'<circle cx="{ex}" cy="{cy+12}" r="5" fill="rgb(240,240,220)" stroke="rgb(200,200,180)" stroke-width="1"/>')
            svg_parts.append(f'<circle cx="{ex}" cy="{cy+37}" r="5" fill="rgb(240,240,220)" stroke="rgb(200,200,180)" stroke-width="1"/>')
    
    svg_parts.append('</svg>')
    return ''.join(svg_parts)


def generate_clothes_svg(clothes_type, skin_color, width=512, height=512):
    """Generate clothing in SVG"""
    svg_parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">']
    
    cx, cy = width // 2, height // 2 + 60
    
    if clothes_type == "hoodie":
        # Modern hoodie
        svg_parts.append(f'<rect x="{cx-110}" y="{cy}" width="220" height="200" rx="10" fill="rgb(80,80,100)" stroke="rgb(60,60,80)" stroke-width="2"/>')
        # Hood
        svg_parts.append(f'<path d="M {cx-90} {cy} Q {cx} {cy-80} {cx+90} {cy} L {cx+70} {cy+30} Q {cx} {cy-40} {cx-70} {cy+30} Z" fill="rgb(90,90,110)" stroke="rgb(70,70,90)" stroke-width="2"/>')
        # Drawstrings
        svg_parts.append(f'<circle cx="{cx-20}" cy="{cy+50}" r="5" fill="rgb(200,200,200)"/>')
        svg_parts.append(f'<circle cx="{cx+20}" cy="{cy+50}" r="5" fill="rgb(200,200,200)"/>')
        svg_parts.append(f'<rect x="{cx-22}" y="{cy+55}" width="4" height="30" fill="rgb(200,200,200)"/>')
        svg_parts.append(f'<rect x="{cx+18}" y="{cy+55}" width="4" height="30" fill="rgb(200,200,200)"/>')
        # Pocket
        svg_parts.append(f'<rect x="{cx-40}" y="{cy+80}" width="80" height="50" rx="5" fill="rgb(70,70,90)" stroke="rgb(50,50,70)" stroke-width="2"/>')
    
    elif clothes_type == "robe":
        # Flowing mystical robe
        svg_parts.append(f'<path d="M {cx-100} {cy} L {cx-120} {cy+200} L {cx+120} {cy+200} L {cx+100} {cy} Z" fill="rgb(80,60,140)" stroke="rgb(60,40,100)" stroke-width="2"/>')
        # Inner robe
        svg_parts.append(f'<path d="M {cx-70} {cy+20} L {cx-80} {cy+200} L {cx+80} {cy+200} L {cx+70} {cy+20} Z" fill="rgb(100,80,160)" opacity="0.7"/>')
        # Belt
        svg_parts.append(f'<rect x="{cx-90}" y="{cy+110}" width="180" height="15" fill="rgb(150,100,50)" stroke="rgb(120,80,30)" stroke-width="2"/>')
        svg_parts.append(f'<circle cx="{cx}" cy="{cy+117}" r="12" fill="rgb(200,150,70)" stroke="rgb(160,110,40)" stroke-width="2"/>')
        # Mystical symbols
        svg_parts.append(f'<circle cx="{cx-40}" cy="{cy+60}" r="8" fill="rgb(150,100,255)" opacity="0.5"/>')
        svg_parts.append(f'<circle cx="{cx+40}" cy="{cy+60}" r="8" fill="rgb(150,100,255)" opacity="0.5"/>')
    
    elif clothes_type == "armor":
        # Plate armor
        svg_parts.append(f'<rect x="{cx-100}" y="{cy}" width="200" height="200" rx="15" fill="rgb(180,180,200)" stroke="rgb(140,140,160)" stroke-width="3"/>')
        # Chest plate
        svg_parts.append(f'<ellipse cx="{cx}" cy="{cy+60}" rx="85" ry="90" fill="rgb(200,200,220)" stroke="rgb(160,160,180)" stroke-width="2"/>')
        # Shoulder guards
        svg_parts.append(f'<ellipse cx="{cx-80}" cy="{cy+30}" rx="35" ry="40" fill="rgb(190,190,210)" stroke="rgb(150,150,170)" stroke-width="2"/>')
        svg_parts.append(f'<ellipse cx="{cx+80}" cy="{cy+30}" rx="35" ry="40" fill="rgb(190,190,210)" stroke="rgb(150,150,170)" stroke-width="2"/>')
        # Armor lines
        for i in range(3):
            y_pos = cy + 70 + i * 30
            svg_parts.append(f'<line x1="{cx-70}" y1="{y_pos}" x2="{cx+70}" y2="{y_pos}" stroke="rgb(120,120,140)" stroke-width="3"/>')
        # Center emblem
        svg_parts.append(f'<circle cx="{cx}" cy="{cy+60}" r="20" fill="rgb(220,220,240)" stroke="rgb(180,180,200)" stroke-width="2"/>')
    
    elif clothes_type == "tunic":
        # Simple medieval tunic
        svg_parts.append(f'<rect x="{cx-95}" y="{cy}" width="190" height="200" rx="8" fill="rgb(150,100,60)" stroke="rgb(120,80,40)" stroke-width="2"/>')
        # V-neck
        skin_rgb = f"rgb({skin_color[0]},{skin_color[1]},{skin_color[2]})"
        svg_parts.append(f'<path d="M {cx-40} {cy} L {cx} {cy+50} L {cx+40} {cy} Z" fill="{skin_rgb}"/>')
        # Sleeves
        svg_parts.append(f'<rect x="{cx-120}" y="{cy+10}" width="25" height="100" rx="5" fill="rgb(150,100,60)" stroke="rgb(120,80,40)" stroke-width="2"/>')
        svg_parts.append(f'<rect x="{cx+95}" y="{cy+10}" width="25" height="100" rx="5" fill="rgb(150,100,60)" stroke="rgb(120,80,40)" stroke-width="2"/>')
        # Decorative stitching
        svg_parts.append(f'<line x1="{cx-70}" y1="{cy+30}" x2="{cx+70}" y2="{cy+30}" stroke="rgb(180,130,80)" stroke-width="2" stroke-dasharray="5,3"/>')
    
    elif clothes_type == "cloak":
        # Mysterious cloak
        svg_parts.append(f'<path d="M {cx-130} {cy} Q {cx} {cy-30} {cx+130} {cy} L {cx+140} {cy+200} L {cx-140} {cy+200} Z" fill="rgb(40,40,60)" stroke="rgb(20,20,40)" stroke-width="2"/>')
        # Inner shadow
        svg_parts.append(f'<ellipse cx="{cx}" cy="{cy+100}" rx="60" ry="100" fill="rgb(20,20,35)" opacity="0.5"/>')
        # Clasp
        svg_parts.append(f'<rect x="{cx-30}" y="{cy+10}" width="60" height="15" rx="7" fill="rgb(255,215,0)" stroke="rgb(220,180,0)" stroke-width="2"/>')
        svg_parts.append(f'<circle cx="{cx}" cy="{cy+17}" r="8" fill="rgb(200,50,50)" stroke="rgb(160,30,30)" stroke-width="1"/>')
    
    svg_parts.append('</svg>')
    return ''.join(svg_parts)


def clear_cache():
    """Clear the rendering cache"""
    global _SURFACE_CACHE
    _SURFACE_CACHE = {}
