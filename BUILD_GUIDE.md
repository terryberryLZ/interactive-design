# Building the Windows Executable

This guide explains how to build a standalone Windows .exe from the Pixel-Art Avatar Generator.

## Overview

The build process uses **PyInstaller** to bundle:
- Python runtime (3.6+)
- Pygame library
- Avatar generator code
- Color palette JSON file

The result is a single-file executable (~15-25 MB) that runs on Windows 10/11 without requiring Python installation.

## Prerequisites

### On the Build Machine
- Windows 10 or Windows 11
- Python 3.6 or higher installed and added to PATH
- Internet connection (for downloading dependencies)

To verify Python is installed:
```batch
python --version
```

## Build Methods

### Method 1: Automated Build Script (Recommended)

#### Using Batch Script

1. Open **Command Prompt** in the project directory
2. Run the build script:
   ```batch
   build_exe.bat
   ```
3. Wait for the build to complete (2-5 minutes)
4. Find the executable in `dist\PixelAvatarGenerator.exe`

#### Using PowerShell Script

1. Open **PowerShell** in the project directory
2. Run the build script:
   ```powershell
   .\build_exe.ps1
   ```
3. Wait for the build to complete
4. Find the executable in `dist\PixelAvatarGenerator.exe`

### Method 2: Manual Build

If you prefer to build manually or customize the process:

1. **Install dependencies:**
   ```batch
   python -m pip install --upgrade pip
   python -m pip install pygame pyinstaller
   ```

2. **Clean previous builds (optional but recommended):**
   ```batch
   rmdir /s /q build
   rmdir /s /q dist
   rmdir /s /q __pycache__
   ```

3. **Build with PyInstaller:**
   ```batch
   pyinstaller --clean --onefile avatar_generator.spec
   ```

4. **Copy required files:**
   ```batch
   copy color_palette.json dist\
   ```

## Build Output

After a successful build, you'll find:

```
dist/
├── PixelAvatarGenerator.exe   (Main executable, ~15-25 MB)
└── color_palette.json          (Required color data)
```

**Important:** Both files must be distributed together. The .exe looks for `color_palette.json` in the same directory.

## Testing the Build

### Basic Test
1. Navigate to the `dist` folder
2. Double-click `PixelAvatarGenerator.exe`
3. Verify the window opens
4. Click to generate avatars
5. Press 'S' to save an avatar
6. Close the window

### Clean Environment Test

For a proper test, run the .exe on a machine without Python installed:

**Option A: Use Windows Sandbox**
1. Enable Windows Sandbox (Windows 10 Pro+)
2. Copy the `dist` folder into the Sandbox
3. Run the .exe inside the Sandbox

**Option B: Use a VM**
1. Set up a clean Windows VM
2. Copy the `dist` folder to the VM
3. Test all functionality

**Option C: Another Computer**
1. Copy the `dist` folder to another Windows PC
2. Verify it has no Python installed
3. Test the .exe

### Test Checklist
- [ ] .exe starts without errors
- [ ] Window displays correctly
- [ ] Click generates new avatars
- [ ] Colors look correct (palette loaded)
- [ ] Press 'S' saves PNG files
- [ ] Saved images look correct
- [ ] Window closes properly

## Troubleshooting

### Build Errors

**"Python is not recognized"**
- Python is not installed or not in PATH
- Install Python from https://www.python.org/
- During installation, check "Add Python to PATH"

**"pip: command not found"**
```batch
python -m ensurepip --upgrade
```

**"Module not found" during build**
```batch
python -m pip install --upgrade pygame pyinstaller
```

**Build fails with permission errors**
- Run Command Prompt as Administrator
- Or build in a user-writable directory

**Build freezes or hangs**
- Close any antivirus temporarily
- Clear build cache: delete `build`, `dist`, `__pycache__`
- Try again

### Runtime Errors

**"color_palette.json not found"**
- Ensure `color_palette.json` is in the same folder as the .exe
- Check the file isn't corrupted (should be valid JSON)

**Antivirus blocks the .exe**
- This is common with PyInstaller executables (false positive)
- Add the .exe to your antivirus whitelist
- Or disable antivirus temporarily for testing

**"Failed to execute script"**
- The build may be incomplete
- Rebuild: `pyinstaller --clean --onefile avatar_generator.spec`
- Check for error messages during build

**Window doesn't appear**
- The .exe might be running in the background
- Check Task Manager for "PixelAvatarGenerator.exe"
- Kill the process and try again

**Colors are wrong or missing**
- `color_palette.json` is missing or corrupted
- Copy a fresh version from the source directory
- Ensure the JSON is valid

## Distribution

### For End Users

Package the following for distribution:

```
PixelAvatarGenerator.zip
├── PixelAvatarGenerator.exe
├── color_palette.json
└── README.txt (optional usage instructions)
```

### Sample README.txt for Users

```
Pixel-Art Avatar Generator
===========================

How to Use:
1. Double-click PixelAvatarGenerator.exe
2. Click anywhere in the window to generate a random avatar
3. Press 'S' to save the current avatar as PNG
4. Press 'Q' or close the window to quit

Saved Images:
- avatar_N.png (160×160 pixels)
- avatar_N_4x.png (640×640 pixels)

System Requirements:
- Windows 10 or 11
- No additional software needed

Note: Your antivirus may show a warning (false positive).
This is common with bundled Python applications.
Click "Run anyway" if you trust the source.
```

## Known Limitations

### Large File Size
- The .exe is 15-25 MB due to bundled Python runtime and Pygame
- This is normal for PyInstaller executables
- Consider using UPX compression (enabled by default in spec file)

### Antivirus False Positives
- Many antivirus programs flag PyInstaller executables
- This is a known issue, not a virus
- Users may need to whitelist or temporarily disable antivirus
- Consider code signing (expensive but prevents warnings)

### Slow Startup
- First launch may take 2-5 seconds
- This is due to unpacking the bundled Python runtime
- Subsequent launches in the same session are faster

### Windows Only
- This build process creates Windows .exe only
- For macOS: Use `py2app`
- For Linux: PyInstaller can create Linux binaries
- For cross-platform: Distribute Python source code

## Advanced Customization

### Custom Icon

Add an icon to the .exe:

1. Create or download a `.ico` file
2. Save it as `icon.ico` in the project directory
3. Edit `avatar_generator.spec`:
   ```python
   exe = EXE(
       ...
       icon='icon.ico',
   )
   ```
4. Rebuild

### Reducing File Size

1. **Use UPX compression** (already enabled in spec file)
2. **Exclude unused modules** in spec file:
   ```python
   excludes=['tkinter', 'matplotlib', ...]
   ```
3. **Use --onedir instead of --onefile** (creates folder but loads faster)

### Adding More Files

To bundle additional assets (fonts, images, etc.):

1. Edit `avatar_generator.spec`:
   ```python
   datas=[
       ('color_palette.json', '.'),
       ('assets/*.png', 'assets'),
   ],
   ```
2. Rebuild

## Platform-Specific Notes

### Building on macOS (for macOS executables)

```bash
pip install py2app
python setup.py py2app
```

This creates a `.app` bundle in `dist/`.

### Building on Linux (for Linux executables)

```bash
pyinstaller --onefile avatar_generator.spec
```

This creates a Linux binary in `dist/`.

Consider creating an AppImage for easier distribution:
```bash
# Install AppImage tools
# Package the binary as AppImage
```

## Support

If you encounter issues:

1. Check this document for solutions
2. Verify all prerequisites are met
3. Try a clean rebuild
4. Check the PyInstaller documentation: https://pyinstaller.org/
5. Open an issue on GitHub with:
   - Error messages
   - Build log output
   - System information

## Resources

- PyInstaller Documentation: https://pyinstaller.org/en/stable/
- Pygame Documentation: https://www.pygame.org/docs/
- Python Packaging: https://packaging.python.org/
