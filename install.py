#!/usr/bin/env python3
import subprocess
import sys
import os

def install_requirements():
    """Install all required packages"""
    print("📦 Installing dependencies...")
    
    requirements = [
        "torch", "torchaudio", "opencv-python", "pyautogui", 
        "pyaudio", "openai-whisper", "transformers", "pynput",
        "numpy", "pillow", "pygetwindow", "pyperclip", "psutil"
    ]
    
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
    
    print("🎉 Installation complete!")

if __name__ == "__main__":
    install_requirements()