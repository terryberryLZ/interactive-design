#!/usr/bin/env python3
"""
Pixel Art Fantasy Character Generator
Uses Stable Diffusion XL with LoRA (pixel-art-xl-v1.1) to generate pixel-art style fantasy characters.
Features:
- Text prompt input for custom character generation
- Click generate to create a character
- Save generated characters
- Pixel art style via LoRA
"""

import pygame
import sys
from datetime import datetime
from pathlib import Path
import threading

# Import AI libraries
try:
    from diffusers import StableDiffusionXLPipeline
    import torch
except ImportError as e:
    print("❌ Required libraries not installed!")
    print(f"Missing: {e}")
    print("Please run: pip install diffusers transformers accelerate torch torchvision safetensors peft")
    sys.exit(1)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
AVATAR_SIZE = 512
AVATAR_Y_OFFSET = 50

# Debug logging toggle
DEBUG = False

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (100, 100, 100)
BLUE = (70, 130, 220)
HOVER_BLUE = (90, 150, 240)
GREEN = (80, 200, 120)


class AIAvatarGenerator:
    """AI-powered pixel art fantasy character generator using Stable Diffusion with LoRA"""

    def __init__(self, lora_path="pixel-art-xl-v1.1.safetensors"):
        self.lora_path = Path(lora_path)
        self.pipeline = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.is_loading = False
        self.is_generating = False
        self.model_loaded = False
        self.progress = 0
        self.progress_text = ""

        print(f"🔧 Device: {self.device}")
        if self.device == "cpu":
            print("⚠️  Warning: Using CPU. Generation will be slow (2-5 minutes per image)")
            print("   For better performance, use a CUDA-compatible GPU")
    # Generation is text-only; no external image inputs

    def load_model(self):
        """Load Stable Diffusion XL model with LoRA"""
        if self.model_loaded:
            return

        self.is_loading = True
        print("🔄 Loading Stable Diffusion XL model...")
        print("   (First time will download ~6GB, please be patient)")

        try:
            # Load base SDXL model
            model_id = "stabilityai/stable-diffusion-xl-base-1.0"

            self.pipeline = StableDiffusionXLPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                use_safetensors=True,
                variant="fp16" if self.device == "cuda" else None,
            )

            self.pipeline = self.pipeline.to(self.device)

            # Load LoRA weights if file exists
            if self.lora_path.exists():
                print(f"🎨 Loading LoRA model: {self.lora_path}")
                self.pipeline.load_lora_weights(".", weight_name=str(self.lora_path))
                print("✅ LoRA model loaded successfully!")
            else:
                print(f"⚠️  LoRA file not found: {self.lora_path}")
                print("   Continuing with base SDXL model (results may vary)")

            # Enable memory optimizations
            if self.device == "cuda":
                self.pipeline.enable_attention_slicing()
                # Try to enable xformers for faster generation
                try:
                    self.pipeline.enable_xformers_memory_efficient_attention()
                    print("✅ xformers enabled for faster generation")
                except Exception:
                    print("ℹ️  xformers not available (optional optimization)")

            self.model_loaded = True
            print("✅ Model loaded and ready!")

        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model_loaded = False
        finally:
            self.is_loading = False
            print(f"📊 Model loading complete: model_loaded={self.model_loaded}, is_loading={self.is_loading}")

    def generate_avatar(self, prompt, negative_prompt=None):
        """Generate pixel-art fantasy character from text prompt"""
        if not self.model_loaded:
            print("❌ Model not loaded yet!")
            return None

        self.is_generating = True
        self.progress = 0
        self.progress_text = "Starting generation..."

        # Default negative prompt for better quality
        if negative_prompt is None:
            negative_prompt = (
                "blurry, low quality, realistic photo, 3d render, photorealistic, deformed, disfigured, duplicate, watermark, text, signature, busy background, detailed scene, complex scenery"
            )

        # Enhance prompt for pixel art fantasy character style
        enhanced_prompt = (
            f"pixel art, {prompt}, fantasy character, full body, centered, standing on a small display stand base under the feet, flat pixel-art platform with subtle shadow, neutral plain background, vibrant palette, clean outlines, front view, game sprite, 16-bit style"
        )

        print(f"🎨 Generating: {enhanced_prompt}")

        try:
            # Progress callback function
            def progress_callback(step, timestep, latents):
                self.progress = int((step / 30) * 100)  # 30 steps total
                self.progress_text = f"Step {step}/30 ({self.progress}%)"
                print(f"   Progress: {self.progress_text}")

            # Generate image with progress tracking
            image = self.pipeline(
                prompt=enhanced_prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=30,
                guidance_scale=7.5,
                width=1024,
                height=1024,
                callback=progress_callback,
                callback_steps=1,
            ).images[0]
            # The stand look is driven by the prompt only

            self.progress = 100
            self.progress_text = "Complete!"
            print("✅ Character generated successfully!")
            return image

        except Exception as e:
            print(f"❌ Error generating character: {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            self.is_generating = False
            self.progress = 0
            self.progress_text = ""

    # Stand aesthetics are prompt-driven; no image compositing


class TextInputBox:
    """Text input box for prompt entry"""

    def __init__(self, x, y, width, height, font, initial_text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = initial_text
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0

    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return "submit"
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                # Add character if it's printable
                if event.unicode.isprintable():
                    self.text += event.unicode

        return None

    def update(self, dt):
        """Update cursor blink"""
        self.cursor_timer += dt
        if self.cursor_timer >= 500:  # Blink every 500ms
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def draw(self, surface):
        """Draw the text input box"""
        # Background
        color = WHITE if self.active else LIGHT_GRAY
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, DARK_GRAY if self.active else GRAY, self.rect, 2)

        # Text
        text_surface = self.font.render(self.text, True, BLACK)
        surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 10))

        # Cursor
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 5 + text_surface.get_width()
            pygame.draw.line(
                surface,
                BLACK,
                (cursor_x, self.rect.y + 8),
                (cursor_x, self.rect.y + self.rect.height - 8),
                2,
            )


class Button:
    """Button widget"""

    def __init__(self, x, y, width, height, text, font, color=BLUE, hover_color=HOVER_BLUE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.enabled = True

    def handle_event(self, event):
        """Handle button events"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.enabled and self.rect.collidepoint(event.pos):
                return True

        return False

    def draw(self, surface):
        """Draw the button"""
        color = self.hover_color if self.is_hovered and self.enabled else self.color
        if not self.enabled:
            color = GRAY

        pygame.draw.rect(surface, color, self.rect, border_radius=5)

        # Text
        text_color = WHITE if self.enabled else DARK_GRAY
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


def pil_to_pygame(pil_image):
    """Convert PIL Image to Pygame Surface"""
    import io

    # Convert PIL image to bytes
    img_bytes = io.BytesIO()
    pil_image.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    # Load as pygame surface
    surf = pygame.image.load(img_bytes)
    # Ensure surface matches display format with alpha for proper blitting
    try:
        return surf.convert_alpha()
    except pygame.error:
        # Fallback in case display not initialized yet
        return surf


def save_avatar(pil_image):
    """Save the current character to file"""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = output_dir / f"pixel_fantasy_character_{timestamp}.png"

    pil_image.save(str(filename))
    print(f"✅ Character saved: {filename}")
    return filename


def main():
    """Main application loop"""
    pygame.init()
    pygame.font.init()

    # Create window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pixel Art Fantasy Character Generator")

    # Fonts
    title_font = pygame.font.Font(None, 36)
    font = pygame.font.Font(None, 24)
    small_font = pygame.font.Font(None, 18)

    # UI Elements
    input_box = TextInputBox(
        50,
        SCREEN_HEIGHT - 130,
        SCREEN_WIDTH - 260,
        40,
        font,
        "a brave warrior knight with golden armor",
    )
    generate_button = Button(SCREEN_WIDTH - 190, SCREEN_HEIGHT - 130, 140, 40, "Generate", font)
    save_button = Button(SCREEN_WIDTH - 190, SCREEN_HEIGHT - 80, 140, 40, "Save", font, color=GREEN)
    quit_button = Button(
        SCREEN_WIDTH - 190, SCREEN_HEIGHT - 30, 140, 40, "Quit", font, color=(200, 50, 50)
    )

    # Create generator
    generator = AIAvatarGenerator()

    # Current character image
    current_avatar_pil = None
    current_avatar_surface = None

    # Loading / generation state
    loading_model = False
    generating = False
    pending_prompt = None

    # Clock
    clock = pygame.time.Clock()

    print("🎨 Pixel Art Fantasy Character Generator")
    print("=" * 50)
    print("Instructions:")
    print("1. Enter a text prompt describing your fantasy character")
    print("2. Click 'Generate' to create the character")
    print("3. Click 'Save' to save your creation")
    print("4. Press ESC to quit")
    print("=" * 50)

    running = True

    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if DEBUG:
                    print(f"🖱️ Mouse clicked at position: {event.pos}")

            # Handle input box
            result = input_box.handle_event(event)
            if result == "submit" and not generating and not loading_model:
                # Generate on Enter key
                prompt = input_box.text
                if not generator.model_loaded:
                    if prompt.strip():
                        pending_prompt = prompt
                    loading_model = True
                    threading.Thread(target=generator.load_model, daemon=True).start()
                else:
                    if prompt.strip():
                        generating = True
                        # Keep the last image visible; we'll gray it out with an overlay
                        # Generate in background thread
                        def generate_thread():
                            nonlocal current_avatar_pil, generating, current_avatar_surface
                            img = generator.generate_avatar(prompt)
                            if img is not None:
                                current_avatar_pil = img
                                # Invalidate surface to force re-conversion next frame
                                current_avatar_surface = None
                            generating = False

                        threading.Thread(target=generate_thread, daemon=True).start()

            # Handle generate button
            button_clicked = generate_button.handle_event(event)
            if button_clicked and DEBUG:
                print(
                    f"🔘 Generate button clicked! loading_model={loading_model}, generating={generating}, model_loaded={generator.model_loaded}"
                )

            if button_clicked and not generating and not loading_model:
                prompt = input_box.text
                if not generator.model_loaded:
                    if prompt.strip():
                        pending_prompt = prompt
                    loading_model = True
                    threading.Thread(target=generator.load_model, daemon=True).start()
                else:
                    if prompt.strip():
                        print(f"🎯 Generate button clicked! Prompt: {prompt}")
                        generating = True
                        # Keep the last image visible; we'll gray it out with an overlay

                        # Generate in background thread
                        def generate_thread():
                            nonlocal current_avatar_pil, generating, current_avatar_surface
                            print("🚀 Starting generation thread...")
                            img = generator.generate_avatar(prompt)
                            if img is not None:
                                current_avatar_pil = img
                                current_avatar_surface = None  # Force re-conversion on main thread
                                print("✅ Generation complete! Image ready.")
                            else:
                                print("❌ Generation failed - no image returned")
                            generating = False

                        threading.Thread(target=generate_thread, daemon=True).start()

            # Handle save button
            if save_button.handle_event(event):
                if current_avatar_pil is not None:
                    save_avatar(current_avatar_pil)

            # Handle quit button
            if quit_button.handle_event(event):
                running = False

        # Update
        input_box.update(dt)

        # Check if model finished loading
        if loading_model and not generator.is_loading:
            loading_model = False
            if DEBUG:
                print(f"✅ Model loading flag reset! loading_model={loading_model}")
            # Auto-start generation if a prompt was queued
            if generator.model_loaded and pending_prompt and not generating:
                print(f"🚀 Starting queued generation for prompt: {pending_prompt}")
                prompt = pending_prompt
                pending_prompt = None
                generating = True
                current_avatar_surface = None

                def generate_thread():
                    nonlocal current_avatar_pil, generating, current_avatar_surface
                    img = generator.generate_avatar(prompt)
                    if img is not None:
                        current_avatar_pil = img
                        current_avatar_surface = None
                        print("✅ Generation complete! Image ready.")
                    else:
                        print("❌ Generation failed - no image returned")
                    generating = False

                threading.Thread(target=generate_thread, daemon=True).start()

        # Update button states
        generate_button.enabled = not generating and not loading_model
        save_button.enabled = current_avatar_pil is not None

        # Debug: Check what's happening with image conversion
        if DEBUG and not generating and current_avatar_pil is not None:
            print(
                f"🔍 MAIN LOOP DEBUG: pil={current_avatar_pil is not None}, surface={current_avatar_surface is not None}, generating={generating}"
            )

        # Convert PIL image to pygame surface if new image available
        if current_avatar_pil is not None and current_avatar_surface is None:
            print("🖼️ Converting PIL image to Pygame surface...")
            try:
                current_avatar_surface = pil_to_pygame(current_avatar_pil)
                # Scale to fit display area
                current_avatar_surface = pygame.transform.scale(
                    current_avatar_surface, (AVATAR_SIZE, AVATAR_SIZE)
                )
                print("✅ Image converted and ready to display!")
            except Exception as e:
                print(f"❌ Error converting image: {e}")
                import traceback

                traceback.print_exc()

        # Clear screen
        screen.fill(WHITE)

        # Draw title
        title_text = title_font.render(
            "Pixel Art Fantasy Character Generator", True, BLACK
        )
        screen.blit(title_text, (20, 10))

        # Draw avatar display area
        avatar_rect = pygame.Rect(
            (SCREEN_WIDTH - AVATAR_SIZE) // 2, AVATAR_Y_OFFSET, AVATAR_SIZE, AVATAR_SIZE
        )
        pygame.draw.rect(screen, LIGHT_GRAY, avatar_rect)
        pygame.draw.rect(screen, GRAY, avatar_rect, 2)

        if current_avatar_surface is not None:
            screen.blit(current_avatar_surface, avatar_rect)
        else:
            # Show placeholder text
            if loading_model:
                text = small_font.render("Loading AI model...", True, DARK_GRAY)
                text_rect = text.get_rect(center=avatar_rect.center)
                screen.blit(text, text_rect)
            else:
                text = small_font.render(
                    "Enter a prompt and click Generate to create a fantasy character",
                    True,
                    DARK_GRAY,
                )
                text_rect = text.get_rect(center=avatar_rect.center)
                screen.blit(text, text_rect)

        # If generating, draw a grayed overlay and progress bar on top of the avatar area
        if generating:
            overlay = pygame.Surface((AVATAR_SIZE, AVATAR_SIZE), pygame.SRCALPHA)
            overlay.fill((240, 240, 240, 200))  # semi-transparent gray
            screen.blit(overlay, avatar_rect)

            # Progress text
            progress_text = font.render(
                f"Generating... {generator.progress}%", True, DARK_GRAY
            )
            text_rect = progress_text.get_rect(
                center=(avatar_rect.centerx, avatar_rect.centery - 30)
            )
            screen.blit(progress_text, text_rect)

            # Progress bar
            bar_width = 400
            bar_height = 30
            bar_x = (SCREEN_WIDTH - bar_width) // 2
            bar_y = avatar_rect.centery + 10

            # Background bar
            pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
            # Progress fill
            if generator.progress > 0:
                fill_width = int((generator.progress / 100) * bar_width)
                pygame.draw.rect(screen, BLUE, (bar_x, bar_y, fill_width, bar_height))
            # Border
            pygame.draw.rect(screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height), 2)

            # Step info
            if generator.progress_text:
                step_text = small_font.render(
                    generator.progress_text, True, DARK_GRAY
                )
                step_rect = step_text.get_rect(
                    center=(avatar_rect.centerx, bar_y + bar_height + 20)
                )
                screen.blit(step_text, step_rect)

        # Draw prompt label
        prompt_label = font.render("Prompt:", True, BLACK)
        screen.blit(prompt_label, (50, SCREEN_HEIGHT - 160))

        # Draw UI elements
        input_box.draw(screen)
        generate_button.draw(screen)
        save_button.draw(screen)
        quit_button.draw(screen)

        # Status text
        status_y = SCREEN_HEIGHT - 30
        if loading_model:
            status = small_font.render(
                "Loading model... (this may take a few minutes)", True, BLUE
            )
            screen.blit(status, (50, status_y))
        elif generating:
            status = small_font.render(
                "Generating character... please wait", True, BLUE
            )
            screen.blit(status, (50, status_y))
        elif not generator.model_loaded:
            status = small_font.render(
                "Click Generate to load the AI model", True, DARK_GRAY
            )
            screen.blit(status, (50, status_y))

        # Update display
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
