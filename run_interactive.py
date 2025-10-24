#!/usr/bin/env python3
"""
Interactive version of the AI Assistant with automation control
"""
import sys
import os
import threading
import time

sys.path.insert(0, os.path.dirname(__file__))

from src.main import AIAssistant

def interactive_controller(assistant):
    """Handle user commands while the assistant is running"""
    while assistant.is_running:
        try:
            command = input("\n🎮 Enter command (auto/enable/disable/stop/help): ").strip().lower()
            
            if command == 'enable' or command == 'auto':
                assistant.enable_automation()
            elif command == 'disable':
                assistant.disable_automation()
            elif command == 'stop' or command == 'exit':
                assistant.stop()
                break
            elif command == 'help':
                print("\n📋 Available commands:")
                print("  enable/auto - Enable workflow automation")
                print("  disable     - Disable workflow automation") 
                print("  stop/exit   - Stop the AI Assistant")
                print("  help        - Show this help message")
            else:
                print("❌ Unknown command. Type 'help' for available commands.")
                
        except (KeyboardInterrupt, EOFError):
            print("\n🛑 Stopping AI Assistant...")
            assistant.stop()
            break
        except Exception as e:
            print(f"❌ Command error: {e}")

def main():
    assistant = AIAssistant()
    
    print("🎮 Starting Interactive AI Assistant...")
    print("💡 You can control automation while it's running!")
    
    # Start the assistant
    assistant.start()
    
    # Start interactive controller in separate thread
    controller_thread = threading.Thread(target=interactive_controller, args=(assistant,))
    controller_thread.daemon = True
    controller_thread.start()
    
    try:
        # Keep main thread alive
        while assistant.is_running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Received interrupt signal...")
    finally:
        if assistant.is_running:
            assistant.stop()

if __name__ == "__main__":
    main()