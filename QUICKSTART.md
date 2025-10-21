# Quick Start Guide

Get started with the Fantasy Pixel Avatar Generator in under 5 minutes!

## 🚀 Choose Your Method

### Method 1: Pygame (Recommended - Easiest)

**Perfect for**: Quick testing, command-line usage, or building executables

```bash
# 1. Install pygame
pip install pygame

# 2. Run the generator
python fantasy_avatar_generator.py

# 3. Use it!
# - Click anywhere to generate
# - Press R to generate
# - Press S to save
# - Press ESC to quit
```

**With seed for reproducible generation:**
```bash
python fantasy_avatar_generator.py --seed 42
```

---

### Method 2: Processing Python Mode

**Perfect for**: Learning Processing, creative coding classes

1. Download [Processing](https://processing.org/download)
2. Install Python Mode:
   - Click "Java" → "Add Mode..." → Install "Python Mode"
3. Open `fantasy_avatar_generator.pyde`
4. Click Run button (▶)
5. Click anywhere or press R to generate!

---

### Method 3: Windows .exe (No Python Needed!)

**Perfect for**: Sharing with non-programmers, distribution

See [BUILD_EXE.md](BUILD_EXE.md) for building instructions.

Once built, just double-click `FantasyAvatarGenerator.exe`!

---

## 📝 What You Get

- **1.68 million** unique avatar combinations
- **5 races**: Human, Orc, Elf, Dwarf, Goblin
- **4 expressions**: Handsome, Serious, Cute, Goofy
- **Multiple accessories**: Headwear, jewelry, clothing
- **7 backgrounds**: Solid colors, gradients, patterns
- **512×512 high-resolution** pixel art output

---

## 💡 Quick Tips

1. **Save favorites**: Press S (Pygame) or screenshot
2. **Reproducible**: Use `--seed 12345` to generate same avatars
3. **Fast browsing**: Press R repeatedly to quickly browse
4. **Share seeds**: Give friends your seed number to share exact avatars

---

## 🐛 Troubleshooting

**"No module named pygame"**
```bash
pip install pygame
```

**"Python not found"**
- Install Python from [python.org](https://python.org)
- Make sure to check "Add Python to PATH" during installation

**ALSA warnings (Linux)**
- These are harmless audio warnings, ignore them

**Want Processing instead?**
- See [USAGE.md](USAGE.md) for detailed Processing setup

---

## 📚 Next Steps

- Read [README.md](README.md) for full feature list
- Check [EXAMPLES.md](EXAMPLES.md) for combination ideas
- See [DEVELOPMENT.md](DEVELOPMENT.md) to add your own elements
- Try [BUILD_EXE.md](BUILD_EXE.md) to create a distributable .exe

---

## 🎮 Controls Summary

| Key/Action | Effect |
|------------|--------|
| Mouse Click | Generate new avatar |
| R | Generate new avatar |
| S | Save avatar as PNG (Pygame only) |
| ESC | Exit program (Pygame only) |
| --seed N | Use seed N for reproducible generation |

---

**Enjoy creating fantasy avatars!** 🎨✨
