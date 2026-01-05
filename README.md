# 🐠 Coral Reef Aquarium - Sharing Guide

An interactive aquarium simulator with fish breeding, predators, water chemistry, and more!

## 📦 Sharing Options

### Option 1: Standalone Executable (RECOMMENDED - Easiest for Classmates)

This is the best option if your classmates aren't familiar with Python.

**Steps to build:**

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Run the build script:
   ```bash
   python build_aquarium.py
   ```

3. Find your executable in `dist/CoralReefAquarium/`

4. **Share with classmates:**
   - Zip the entire `dist/CoralReefAquarium` folder
   - Send the zip file
   - They extract and double-click `CoralReefAquarium.exe`
   - **No installation needed!** ✨

**Note:** The executable will be Windows-only. For Mac/Linux classmates, use Option 2.

---

### Option 2: Share Python Source Code

If your classmates are comfortable with Python, share the source code:

**What to send:**
- `aquarium__6_.py`
- `requirements.txt`
- This README

**Instructions for classmates:**

1. **Install Python** (if not already installed):
   - Download from [python.org](https://python.org)
   - Use Python 3.8 or newer

2. **Install pygame:**
   ```bash
   pip install pygame
   ```
   
   Or using the requirements file:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the aquarium:**
   ```bash
   python aquarium__6_.py
   ```

**Troubleshooting pygame installation:**
- Windows: `pip install pygame`
- Mac: `pip3 install pygame` or `python3 -m pip install pygame`
- Linux: `sudo apt install python3-pygame` or `pip install pygame`

---

### Option 3: Share via Cloud/GitHub

**Using Google Drive / Dropbox:**
1. Upload `aquarium__6_.py` and `requirements.txt`
2. Share the link
3. Classmates download and follow Option 2 instructions

**Using GitHub:**
1. Create a repository
2. Upload files
3. Share repository link
4. Classmates clone and follow Option 2 instructions

---

## 🎮 Game Controls

Once running, here are the controls:

**Fish Styles:**
- `F` - Cycle through fish styles
- `1` - Realistic fish
- `2` - Cartoon fish
- `3` - Pixel art fish
- `4` - Tropical fish
- `5-8` - Military themed fish (Army, Air Force, Space Force, Navy)

**Background Scenes:**
- `B` - Cycle through background scenes
- `0` - Turn off background scene

**Aquarium Management:**
- `W` - Perform water change (reduces nitrates)
- **Click anywhere** - Drop food for fish
- `H` - Hide/show UI

**Exit:**
- `ESC` - Exit aquarium

---

## ⚙️ System Requirements

- **Windows 10 or newer** (for executable)
- **1 GB RAM minimum**
- **Supports 1200x800 resolution** (automatically adjusts)

---

## 🎓 Why This is Better Than "Just Install Pygame"

Your classmates will appreciate the standalone executable because:
- ✅ No Python installation needed
- ✅ No pip/package manager confusion
- ✅ No "it doesn't work on my computer" issues
- ✅ Just download, extract, and run!

The file will be larger (50-100 MB) but it includes everything needed.

---

## 🐛 If Something Goes Wrong

**For executable users:**
- Make sure to extract the ENTIRE folder, not just the .exe
- Windows might show a security warning - click "More info" → "Run anyway"
- Some antivirus software may flag unknown executables - this is a false positive

**For source code users:**
- Make sure Python 3.8+ is installed
- Try: `python --version` or `python3 --version`
- Make sure pygame installed successfully: `pip show pygame`

---

## 📝 Credits

Created by [Your Name]
Built with Python and Pygame

Enjoy the aquarium! 🐠🐟🦈
