#!/usr/bin/env python3
"""
Launch the AI Assistant with GUI
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.main import AIAssistant

def main():
    print("🚀 Starting AI Assistant with GUI...")
    assistant = AIAssistant()
    assistant.start_with_gui()

if __name__ == "__main__":
    main()