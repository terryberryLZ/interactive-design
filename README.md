## Pixel Art Fantasy Character Generator

Text-to-image generator using Stable Diffusion XL with a pixel-art LoRA.

### Features
- Prompt input + one-click Generate
- Progress overlay while generating
- Save button and Quit (ESC)
- GPU acceleration (falls back to CPU)

### Requirements
- Python 3.11 recommended (works on 3.8+)
- Windows 10/11; NVIDIA GPU preferred
- `requirements.txt` installed

### Install
```powershell
pip install -r requirements.txt
```

**Important:** Download the LoRA model separately:
- File: `pixel-art-xl-v1.1.safetensors` (162 MB)
- Source: [Civitai - Pixel Art XL](https://civitai.com/models/120096/pixel-art-xl) or [Hugging Face](https://huggingface.co/)
- Place it in the project root folder alongside `ai_avatar_generator.py`

### Run
```powershell
python ai_avatar_generator.py
```

### Tips
- Use simple, specific prompts: "a brave warrior knight with golden armor"
- The “stand” is prompt-only; no reference images are used
- First run may download ~6GB for SDXL

### Troubleshooting
- If GPU isn’t used, ensure this Python is the one where torch was installed
- For CUDA OOM, close apps or let it run on CPU
- If build tool errors appear, install MSVC build tools

### Files
- `ai_avatar_generator.py` — main app
- `pixel-art-xl-v1.1.safetensors` — LoRA weights (download separately, see Install)
- `requirements.txt` — dependencies

License: Personal/educational use.
