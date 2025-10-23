import pyautogui
import cv2
import numpy as np
from datetime import datetime
import os
from src.config.settings import OBSERVATIONS_DIR, SCREEN_CAPTURE_QUALITY

class ScreenCapture:
    def __init__(self):
        self.screenshot_dir = OBSERVATIONS_DIR / "screenshots"
        self.screenshot_dir.mkdir(exist_ok=True)
        
    def capture_screenshot(self):
        """Capture screen and save with metadata"""
        try:
            # Capture screenshot
            screenshot = pyautogui.screenshot()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"screenshot_{timestamp}.jpg"
            filepath = self.screenshot_dir / filename
            
            # Save compressed image
            screenshot.save(filepath, "JPEG", quality=int(SCREEN_CAPTURE_QUALITY * 100))
            
            # Get mouse position and active window
            mouse_x, mouse_y = pyautogui.position()
            active_window = self._get_active_window()
            
            return {
                'timestamp': timestamp,
                'screenshot_path': str(filepath),
                'mouse_x': mouse_x,
                'mouse_y': mouse_y,
                'active_window': active_window,
                'window_title': self._get_window_title()
            }
            
        except Exception as e:
            print(f"Screen capture error: {e}")
            return None
    
    def _get_active_window(self):
        """Get current active window name"""
        try:
            import pygetwindow as gw
            window = gw.getActiveWindow()
            return window.title if window else "Unknown"
        except:
            return "Unknown"
    
    def _get_window_title(self):
        """Get window title"""
        try:
            import pygetwindow as gw
            window = gw.getActiveWindow()
            return window.title if window else "Unknown"
        except:
            return "Unknown"