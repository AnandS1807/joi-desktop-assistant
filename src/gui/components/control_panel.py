import tkinter as tk
from tkinter import ttk, messagebox
import threading

class ControlPanel(ttk.LabelFrame):
    def __init__(self, parent, assistant):
        super().__init__(parent, text="Controls", style='Dark.TLabelframe', padding=10)
        self.assistant = assistant
        self.setup_panel()
    
    def setup_panel(self):
        # Main control buttons
        button_frame = ttk.Frame(self, style='Dark.TFrame')
        button_frame.pack(fill="x", pady=5)
        
        self.start_btn = ttk.Button(button_frame, text="Start Observation", 
                                   command=self.start_assistant, style='Action.TButton')
        self.start_btn.pack(side="left", padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="Stop Observation", 
                                  command=self.stop_assistant, style='Action.TButton')
        self.stop_btn.pack(side="left", padx=5)
        
        self.auto_btn = ttk.Button(button_frame, text="Enable Automation", 
                                  command=self.toggle_automation, style='Action.TButton')
        self.auto_btn.pack(side="left", padx=5)
        
        # Settings button
        ttk.Button(button_frame, text="Settings", 
                  command=self.show_settings, style='Action.TButton').pack(side="right", padx=5)
    
    def start_assistant(self):
        def start_thread():
            try:
                self.assistant.start()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start: {e}")
        
        threading.Thread(target=start_thread, daemon=True).start()
    
    def stop_assistant(self):
        self.assistant.stop()
    
    def toggle_automation(self):
        if self.assistant.automation_enabled:
            self.assistant.disable_automation()
            self.auto_btn.config(text="Enable Automation")
        else:
            # Show confirmation for automation
            result = messagebox.askyesno(
                "Enable Automation", 
                "🤖 AUTOMATION WARNING:\n\nThe AI will automatically execute workflows!\n\n"
                "Make sure no important work is unsaved.\n\n"
                "Enable automation?"
            )
            if result:
                self.assistant.enable_automation()
                self.auto_btn.config(text="Disable Automation")
    
    def show_settings(self):
        # Simple settings dialog
        settings_window = tk.Toplevel(self)
        settings_window.title("Settings")
        settings_window.geometry("300x200")
        
        ttk.Label(settings_window, text="Settings Panel").pack(pady=10)
        ttk.Label(settings_window, text="Coming soon...").pack(pady=5)
        
        ttk.Button(settings_window, text="Close", 
                  command=settings_window.destroy).pack(pady=10)
    
    def update(self):
        # Update button states based on assistant status
        if self.assistant.is_running:
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
        else:
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
        
        # Update automation button text
        if self.assistant.automation_enabled:
            self.auto_btn.config(text="Disable Automation")
        else:
            self.auto_btn.config(text="Enable Automation")