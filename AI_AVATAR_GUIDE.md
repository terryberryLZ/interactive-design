# AI Fantasy Avatar Generator - LoRA Model Guide

## 📋 Overview

This guide explains how to use the **pixel-art-xl-v1.1.safetensors** LoRA model with Stable Diffusion XL to generate fantasy pixel art avatars.

## 🔍 About Your LoRA Model

**File:** `pixel-art-xl-v1.1.safetensors`  
**Hash:** AUTOV2/BBF3D8DEFB  
**Type:** LoRA (Low-Rank Adaptation) weights for Stable Diffusion XL  
**Purpose:** Fine-tuned to generate pixel art style images

### What is a LoRA Model?

LoRA (Low-Rank Adaptation) is a lightweight model that modifies a base AI model (like Stable Diffusion XL) to specialize in a specific style (in this case, pixel art). Instead of training an entire model from scratch, LoRA only trains small additional layers, making it:
- **Smaller** (~100-200MB vs 6GB for full models)
- **Faster** to load and use
- **Style-specific** for better quality in that style

### How SafeTensors Works

The `.safetensors` format is a safe way to store AI model weights:
- **Secure:** Prevents malicious code execution
- **Fast:** Quick to load
- **Compatible:** Works with most modern AI frameworks

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **pygame** - For the UI
- **torch** - PyTorch deep learning framework
- **diffusers** - Stable Diffusion pipeline
- **transformers** - Model loading utilities
- **safetensors** - To load your LoRA weights
- **accelerate** - Optimization library

### 2. Run the Generator

```bash
python ai_avatar_generator.py
```

### 3. System Requirements

#### Minimum (CPU):
- **RAM:** 16GB+
- **Storage:** 10GB free space
- **Generation Time:** 2-5 minutes per image
- **Note:** Very slow but functional

#### Recommended (GPU):
- **GPU:** NVIDIA GPU with 6GB+ VRAM (RTX 2060 or better)
- **RAM:** 16GB+
- **Storage:** 10GB free space
- **Generation Time:** 10-30 seconds per image
- **CUDA:** Required for GPU acceleration

## 🎨 How to Use

### Interface Layout

```
┌─────────────────────────────────────────┐
│   AI Fantasy Avatar Generator          │
├─────────────────────────────────────────┤
│                                         │
│         [Avatar Display Area]           │
│              512x512                    │
│                                         │
├─────────────────────────────────────────┤
│ Prompt: [_____________________] [Generate]│
│                                  [Save] │
└─────────────────────────────────────────┘
```

### Step-by-Step:

1. **Enter a Prompt**
   - Type your description in the text box
   - Examples:
     - "a brave warrior knight with golden armor"
     - "a mystical elf mage with purple robes"
     - "a fierce dragon warrior with red scales"
     - "a cute forest fairy with wings"

2. **Generate**
   - Click "Generate" button or press Enter
   - First generation will load the model (1-2 minutes)
   - Wait for generation to complete (10-30 seconds with GPU)

3. **Save**
   - Click "Save" to save your avatar
   - Files saved to `output/ai_avatar_YYYYMMDD_HHMMSS.png`

## 💡 Prompt Tips

### Good Prompts Include:

1. **Character Type**
   - warrior, mage, knight, elf, dwarf, dragon, goblin

2. **Appearance**
   - armor color, clothing style, hair, accessories

3. **Style Keywords** (optional, automatically added):
   - The system automatically adds "pixel art" and "fantasy character"

### Example Prompts:

```
✅ "a heroic knight with shining silver armor and red cape"
✅ "a mysterious wizard with purple robes and magical staff"
✅ "a cute goblin merchant with green skin and leather vest"
✅ "a fierce orc warrior with battle axe and tribal paint"
✅ "an elegant elven archer with bow and forest green cloak"
```

### Avoid:

```
❌ "realistic photo" - contradicts pixel art style
❌ "3d render" - not compatible with pixel art
❌ Too complex scenes - focus on single character
```

## 🔧 Technical Details

### How the Code Works:

1. **Model Loading (`load_model` method)**
   ```python
   - Downloads Stable Diffusion XL base model (first time only)
   - Loads your pixel-art-xl-v1.1.safetensors LoRA weights
   - Configures memory optimizations
   ```

2. **Generation (`generate_avatar` method)**
   ```python
   - Takes your prompt
   - Adds pixel art style keywords
   - Generates 512x512 image
   - Returns PIL Image object
   ```

3. **LoRA Integration**
   ```python
   pipeline.load_lora_weights(".", weight_name="pixel-art-xl-v1.1.safetensors")
   ```
   This line loads your LoRA weights on top of the base SDXL model.

### Generation Parameters:

- **Size:** 512x512 pixels (optimal for pixel art)
- **Steps:** 30 (balance of quality vs speed)
- **Guidance Scale:** 7.5 (how closely to follow prompt)
- **Style:** Pixel art automatically enforced by LoRA

## 🐛 Troubleshooting

### Issue: "CUDA out of memory"
**Solution:** 
- Close other programs
- Reduce to 512x512 resolution (already default)
- Use CPU mode (slower but works)

### Issue: Generation is very slow
**Cause:** Running on CPU  
**Solution:**
- If you have NVIDIA GPU, install CUDA toolkit
- Or be patient (2-5 minutes is normal on CPU)

### Issue: "Model not loading"
**Solutions:**
1. Check internet connection (first download)
2. Ensure 10GB free disk space
3. Check requirements are installed: `pip install -r requirements.txt`

### Issue: LoRA file not found
**Solution:**
- Ensure `pixel-art-xl-v1.1.safetensors` is in the project folder
- Check the exact filename matches

## 📁 Project Structure

```
interactive-design/
├── ai_avatar_generator.py          # Main AI generator (NEW!)
├── fantasy_avatar_generator.py     # Original procedural generator
├── pixel-art-xl-v1.1.safetensors  # Your LoRA model
├── requirements.txt                # Python dependencies
├── AI_AVATAR_GUIDE.md             # This guide
└── output/                         # Generated avatars saved here
    └── ai_avatar_*.png
```

## 🎯 Features

- ✅ **Text-to-Image Generation** - Describe what you want
- ✅ **Pixel Art Style** - Enforced by LoRA model
- ✅ **Interactive UI** - Simple and intuitive
- ✅ **Save Functionality** - Keep your creations
- ✅ **GPU Acceleration** - Fast generation with CUDA
- ✅ **CPU Fallback** - Works without GPU (slower)

## 🔄 Comparison: Old vs New

### Original Generator (`fantasy_avatar_generator.py`):
- ✅ Fast (instant)
- ✅ No installation needed
- ❌ Random only, no control
- ❌ Limited variety

### New AI Generator (`ai_avatar_generator.py`):
- ✅ Full creative control via text
- ✅ Unlimited variety
- ✅ High-quality pixel art
- ❌ Requires model download
- ❌ Slower (10-30s per image)

## 📚 Additional Resources

### Learn More:
- **Stable Diffusion XL:** https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0
- **LoRA Training:** https://huggingface.co/docs/diffusers/training/lora
- **Diffusers Library:** https://huggingface.co/docs/diffusers/index

### Get More LoRA Models:
- **CivitAI:** https://civitai.com/ (thousands of LoRA models)
- **Hugging Face:** https://huggingface.co/models?other=lora

## 🎨 Example Gallery

Try these prompts to see what the system can create:

1. "a noble paladin with golden armor and holy sword"
2. "a sneaky rogue assassin in black leather"
3. "a powerful archmage with glowing staff"
4. "a friendly dwarf blacksmith with hammer"
5. "a mystical dragon knight with scale armor"
6. "a woodland druid with nature magic"
7. "a pirate captain with eye patch and hat"
8. "a samurai warrior with katana"

## 📝 Notes

- **First Run:** Expect 5-10 minute setup (model download)
- **Subsequent Runs:** 10-30 seconds per generation (GPU) or 2-5 minutes (CPU)
- **Model Location:** Downloaded to `~/.cache/huggingface/`
- **Output Format:** PNG with transparency support
- **Thread-Safe:** Uses background threads to keep UI responsive

## 🤝 Support

If you encounter issues:
1. Check this guide's Troubleshooting section
2. Ensure all requirements are installed
3. Verify your LoRA file is in the correct location
4. Check that you have enough free disk space and RAM

Happy avatar generating! 🎮✨
