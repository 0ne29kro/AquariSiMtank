"""
Build Script for Coral Reef Aquarium
This script packages your pygame aquarium into a standalone executable
that your classmates can run without installing Python or pygame.

SETUP INSTRUCTIONS:
1. Install PyInstaller: pip install pyinstaller
2. Place this script in the same folder as aquarium__6_.py
3. Run: python build_aquarium.py
4. Find your executable in the 'dist' folder

SHARING INSTRUCTIONS:
- Windows: Share the entire 'dist/aquarium' folder (zip it first)
- Your classmates just double-click 'aquarium.exe' to run it
"""

import os
import subprocess
import sys

def build_executable():
    print("=" * 60)
    print("Building Coral Reef Aquarium Executable")
    print("=" * 60)
    
    # Check if pygame file exists
    if not os.path.exists("aquarium__6_.py"):
        print("ERROR: aquarium__6_.py not found in current directory!")
        print("Please place this build script in the same folder as your aquarium file.")
        sys.exit(1)
    
    # PyInstaller command
    # --onefile creates a single exe (but slower startup)
    # --onedir creates a folder with exe and dependencies (faster startup, recommended)
    # --windowed hides the console window
    # --name sets the executable name
    
    command = [
        "pyinstaller",
        "--onedir",  # Creates a folder (easier to distribute, faster startup)
        "--windowed",  # No console window
        "--name", "CoralReefAquarium",
        "--icon=NONE",  # Add --icon=youricon.ico if you have an icon
        "aquarium__6_.py"
    ]
    
    print("\nBuilding executable... This may take a few minutes.")
    print("Command:", " ".join(command))
    print()
    
    try:
        subprocess.run(command, check=True)
        print("\n" + "=" * 60)
        print("BUILD SUCCESSFUL!")
        print("=" * 60)
        print("\nYour executable is ready in the 'dist' folder:")
        print("  dist/CoralReefAquarium/CoralReefAquarium.exe")
        print("\nTO SHARE WITH CLASSMATES:")
        print("  1. Zip the entire 'dist/CoralReefAquarium' folder")
        print("  2. Send the zip file to your classmates")
        print("  3. They extract it and double-click CoralReefAquarium.exe")
        print("\nNo Python or pygame installation needed! ✨")
        
    except subprocess.CalledProcessError:
        print("\n" + "=" * 60)
        print("BUILD FAILED!")
        print("=" * 60)
        print("\nMake sure PyInstaller is installed:")
        print("  pip install pyinstaller")
        sys.exit(1)
    except FileNotFoundError:
        print("\n" + "=" * 60)
        print("ERROR: PyInstaller not found!")
        print("=" * 60)
        print("\nPlease install PyInstaller first:")
        print("  pip install pyinstaller")
        sys.exit(1)

if __name__ == "__main__":
    build_executable()
