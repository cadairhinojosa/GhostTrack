# Building GhostTrack Executable

This guide explains how to create a standalone executable file for GhostTrack.

## Prerequisites

Make sure you have Python and pip installed.

## Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

## Step 2: Build the Executable

Run this command in the GhostTrack directory:

```bash
pyinstaller --onefile GhostTR.py
```

### Additional Build Options (Optional)

For a more customized build:

```bash
pyinstaller --onefile --name GhostTrack --icon=asset/icon.ico GhostTR.py
```

Options explained:
- `--onefile`: Packages everything into a single executable
- `--name GhostTrack`: Names the output file "GhostTrack.exe"
- `--icon=asset/icon.ico`: Adds a custom icon (if you have one)
- `--noconsole`: Hide console window (not recommended for this tool)

### Advanced Build (Cleaner Output)

```bash
pyinstaller --onefile --clean --distpath . --workpath build --specpath build GhostTR.py
```

This creates:
- `GhostTrack.exe` in the current directory
- Build files in the `build` folder

## Step 3: Locate Your Executable

After building, you'll find:
- **Executable**: `dist/GhostTR.exe` (or `dist/GhostTrack.exe` if you used `--name`)
- **Build files**: `build/` folder
- **Spec file**: `GhostTR.spec`

## Step 4: Test the Executable

```bash
cd dist
.\GhostTR.exe
```

## Step 5: Clean Up (Optional)

After successful build, you can delete:
- `build/` folder
- `GhostTR.spec` file

Keep the executable from the `dist/` folder.

## Distribution

You can now share the single `.exe` file. Users won't need Python installed!

**Note**: The executable will be larger (20-30MB) because it includes Python and all dependencies.

## Troubleshooting

### Missing Module Errors
If PyInstaller misses some modules, create a spec file and add hidden imports:

```bash
pyinstaller --onefile GhostTR.py
# Edit GhostTR.spec and add to hiddenimports:
hiddenimports=['phonenumbers', 'requests', 'json']
# Rebuild:
pyinstaller GhostTR.spec
```

### Antivirus False Positives
Some antivirus programs may flag PyInstaller executables. This is normal. You can:
1. Add the file to your antivirus exclusions
2. Submit it to your antivirus vendor as a false positive
3. Code-sign the executable (requires certificate)

## Quick Reference

```bash
# Install PyInstaller
pip install pyinstaller

# Simple build
pyinstaller --onefile GhostTR.py

# Custom name and clean build
pyinstaller --onefile --name GhostTrack --clean GhostTR.py

# Run the executable
cd dist
.\GhostTrack.exe
```
