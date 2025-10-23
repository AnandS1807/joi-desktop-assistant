#!/usr/bin/env python3
"""
Desktop AI Assistant - Runner Script
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from src.main import main

if __name__ == "__main__":
    print("🏁 Starting Desktop AI Assistant...")
    main()