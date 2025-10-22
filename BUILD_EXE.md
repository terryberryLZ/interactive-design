# Building Windows .exe for Fantasy Avatar Generator

This guide explains how to build a standalone Windows executable that users can run without installing Python or Pygame.

## Prerequisites

You need Python 3.8+ and pip installed on your Windows machine.

## Step 1: Install Dependencies

```bash
pip install pygame pyinstaller
```

## Step 2: Build the Executable

Run PyInstaller with the provided spec file:

```bash
pyinstaller fantasy_avatar_generator.spec
```

This will create:
- `build/` folder (temporary build files)
- `dist/` folder containing `FantasyAvatarGenerator.exe`

## Step 3: Test the Executable

Navigate to the `dist/` folder and run:

```bash
cd dist
FantasyAvatarGenerator.exe
```

Or with a seed:

```bash
FantasyAvatarGenerator.exe --seed 12345
```

## Distribution

The `FantasyAvatarGenerator.exe` file in the `dist/` folder is a standalone executable that can be distributed to users. They don't need Python, Pygame, or any other dependencies installed.

## Features

- **Click** or **Press R**: Generate a new random avatar
- **Press S**: Save current avatar as PNG image
- **Press ESC**: Exit the program
- **--seed parameter**: Use a specific seed for reproducible generation

## Size Optimization

The default .exe is around 10-15 MB. To reduce size:

1. Use UPX compression (already enabled in the spec file)
2. Exclude unnecessary modules in the Analysis section
3. Use PyInstaller's `--onefile` option (already configured)

## Troubleshooting

### "Failed to execute script"

This usually means a missing dependency. Try:
- Run in console mode to see errors (change `console=True` in .spec file)
- Check that all imports are available

### Antivirus False Positives

Some antivirus software may flag PyInstaller executables. This is a known issue. To resolve:
- Sign the executable with a code signing certificate
- Submit to antivirus vendors as false positive
- Distribute source code as alternative

### Large File Size

The .exe includes the Python interpreter and all dependencies. This is normal for PyInstaller builds. Consider:
- Using alternative packaging tools like cx_Freeze or Nuitka
- Distributing as a ZIP file
- Using an installer like Inno Setup to compress further

## Alternative: Direct Python Distribution

If executable size is a concern, you can also distribute the Python script with a simple batch file:

**run_avatar_generator.bat:**
```batch
@echo off
python -m pip install -q pygame
python fantasy_avatar_generator.py
pause
```

Users would need Python installed, but the distribution would be much smaller.

## Building on Linux/Mac

For cross-platform distribution, build on each target platform:
- Windows: Use PyInstaller on Windows
- Linux: Use PyInstaller on Linux (creates ELF binary)
- Mac: Use PyInstaller on macOS (creates .app bundle)

Cross-compilation is not officially supported by PyInstaller.
