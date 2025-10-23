from pynput import mouse, keyboard
from datetime import datetime
import json
import threading
from src.data.models import InputEvent

class InputTracker:
    def __init__(self):
        self.events = []
        self.max_events = 1000
        self.is_tracking = False
        
    def start_tracking(self):
        """Start tracking mouse and keyboard events"""
        self.is_tracking = True
        
        # Start mouse listener
        self.mouse_listener = mouse.Listener(
            on_move=self.on_mouse_move,
            on_click=self.on_mouse_click,
            on_scroll=self.on_mouse_scroll
        )
        
        # Start keyboard listener
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
        
        self.mouse_listener.start()
        self.keyboard_listener.start()
        
    def stop_tracking(self):
        """Stop tracking events"""
        self.is_tracking = False
        if hasattr(self, 'mouse_listener'):
            self.mouse_listener.stop()
        if hasattr(self, 'keyboard_listener'):
            self.keyboard_listener.stop()
            
    def on_mouse_move(self, x, y):
        if self.is_tracking:
            event = InputEvent(
                timestamp=datetime.now().isoformat(),
                event_type="mouse_move",
                details={"x": x, "y": y}
            )
            self._add_event(event)
    
    def on_mouse_click(self, x, y, button, pressed):
        if self.is_tracking:
            event = InputEvent(
                timestamp=datetime.now().isoformat(),
                event_type="mouse_click",
                details={"x": x, "y": y, "button": str(button), "pressed": pressed}
            )
            self._add_event(event)
    
    def on_mouse_scroll(self, x, y, dx, dy):
        if self.is_tracking:
            event = InputEvent(
                timestamp=datetime.now().isoformat(),
                event_type="mouse_scroll",
                details={"x": x, "y": y, "dx": dx, "dy": dy}
            )
            self._add_event(event)
    
    def on_key_press(self, key):
        if self.is_tracking:
            try:
                key_char = key.char
            except AttributeError:
                key_char = str(key)
                
            event = InputEvent(
                timestamp=datetime.now().isoformat(),
                event_type="key_press",
                details={"key": key_char}
            )
            self._add_event(event)
    
    def on_key_release(self, key):
        pass  # We mainly care about key presses
    
    def _add_event(self, event):
        """Add event to history with size limit"""
        self.events.append(event)
        if len(self.events) > self.max_events:
            self.events = self.events[-self.max_events:]
    
    def get_recent_events(self, count=10):
        """Get most recent events"""
        return self.events[-count:] if self.events else []