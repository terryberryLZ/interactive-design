#!/usr/bin/env python3
"""
Simple test to verify the AI Avatar Generator setup
Tests that all required libraries can be imported
"""

import sys

print("🧪 Testing AI Avatar Generator Setup")
print("=" * 50)

# Test 1: Python version
print("\n1. Checking Python version...")
python_version = sys.version_info
if python_version >= (3, 8):
    print(f"   ✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
else:
    print(f"   ❌ Python {python_version.major}.{python_version.minor}.{python_version.micro} (need 3.8+)")
    sys.exit(1)

# Test 2: Pygame
print("\n2. Checking pygame...")
try:
    import pygame
    print(f"   ✅ pygame {pygame.version.ver}")
except ImportError:
    print("   ❌ pygame not installed")
    print("      Run: pip install pygame")

# Test 3: PyTorch
print("\n3. Checking PyTorch...")
try:
    import torch
    print(f"   ✅ torch {torch.__version__}")
    if torch.cuda.is_available():
        print(f"   ✅ CUDA available: {torch.cuda.get_device_name(0)}")
        print(f"      VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    else:
        print("   ⚠️  CUDA not available (will use CPU - slower)")
except ImportError:
    print("   ❌ torch not installed")
    print("      Run: pip install torch torchvision")

# Test 4: Diffusers
print("\n4. Checking diffusers...")
try:
    import diffusers
    print(f"   ✅ diffusers {diffusers.__version__}")
except ImportError:
    print("   ❌ diffusers not installed")
    print("      Run: pip install diffusers")

# Test 5: Transformers
print("\n5. Checking transformers...")
try:
    import transformers
    print(f"   ✅ transformers {transformers.__version__}")
except ImportError:
    print("   ❌ transformers not installed")
    print("      Run: pip install transformers")

# Test 6: Accelerate
print("\n6. Checking accelerate...")
try:
    import accelerate
    print(f"   ✅ accelerate {accelerate.__version__}")
except ImportError:
    print("   ❌ accelerate not installed")
    print("      Run: pip install accelerate")

# Test 7: SafeTensors
print("\n7. Checking safetensors...")
try:
    import safetensors
    print(f"   ✅ safetensors {safetensors.__version__}")
except ImportError:
    print("   ❌ safetensors not installed")
    print("      Run: pip install safetensors")

# Test 8: PIL/Pillow
print("\n8. Checking Pillow...")
try:
    from PIL import Image
    import PIL
    print(f"   ✅ Pillow {PIL.__version__}")
except ImportError:
    print("   ❌ Pillow not installed")
    print("      Run: pip install pillow")

# Test 9: LoRA file
print("\n9. Checking LoRA model file...")
from pathlib import Path
lora_file = Path("pixel-art-xl-v1.1.safetensors")
if lora_file.exists():
    size_mb = lora_file.stat().st_size / 1024 / 1024
    print(f"   ✅ Found: pixel-art-xl-v1.1.safetensors ({size_mb:.1f} MB)")
else:
    print("   ⚠️  pixel-art-xl-v1.1.safetensors not found")
    print("      Generator will use base SDXL model")

# Test 10: Disk space
print("\n10. Checking disk space...")
import shutil
stat = shutil.disk_usage(".")
free_gb = stat.free / 1024**3
if free_gb >= 10:
    print(f"   ✅ Free space: {free_gb:.1f} GB")
else:
    print(f"   ⚠️  Free space: {free_gb:.1f} GB (need 10GB+)")

# Summary
print("\n" + "=" * 50)
print("📊 Setup Summary:")
print("   If all checks pass (✅), you're ready to generate!")
print("   If any check fails (❌), install the missing package.")
print("\n🚀 To start generating, run:")
print("   python ai_avatar_generator.py")
print("=" * 50)
