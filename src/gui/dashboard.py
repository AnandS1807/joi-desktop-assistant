import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
from datetime import datetime
import psutil
import os

# Import components
from src.gui.components.status_panel import StatusPanel
from src.gui.components.control_panel import ControlPanel
from src.gui.components.workflow_panel import WorkflowPanel
from src.gui.components.activity_log import ActivityLog

class AssistantDashboard:
    def __init__(self, assistant):
        self.assistant = assistant
        self.root = tk.Tk()
        self.setup_gui()
        self.is_updating = True
        self.is_updating = True
        
    def setup_gui(self):
        self.root.title("🤖 AI Desktop Assistant")
        self.root.geometry("600x700")
        self.root.configure(bg='#2b2b2b')
        
        # Create style for dark theme
        self.setup_styles()
        
        # Header
        header_frame = ttk.Frame(self.root, style='Dark.TFrame')
        header_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(header_frame, text="AI Desktop Assistant", 
                 style='Header.TLabel', font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Status Panel
        self.status_panel = StatusPanel(self.root, self.assistant)
        self.status_panel.pack(fill="x", padx=10, pady=5)
        
        # Control Panel
        self.control_panel = ControlPanel(self.root, self.assistant)
        self.control_panel.pack(fill="x", padx=10, pady=5)
        
        # Workflow Panel
        self.workflow_panel = WorkflowPanel(self.root, self.assistant)
        self.workflow_panel.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Activity Log
        self.activity_log = ActivityLog(self.root)
        self.activity_log.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Start GUI update thread
        self.update_thread = threading.Thread(target=self.update_gui, daemon=True)
        self.update_thread.start()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles for dark theme
        style.configure('Dark.TFrame', background='#2b2b2b')
        style.configure('Dark.TLabelframe', background='#2b2b2b', foreground='white')
        style.configure('Dark.TLabelframe.Label', background='#2b2b2b', foreground='white')
        
        style.configure('Header.TLabel', background='#2b2b2b', foreground='#4FC3F7', 
                       font=('Arial', 16, 'bold'))
        
        style.configure('Status.TLabel', background='#37474F', foreground='white')
        style.configure('Green.TLabel', background='#37474F', foreground='#4CAF50')
        style.configure('Red.TLabel', background='#37474F', foreground='#F44336')
        style.configure('Yellow.TLabel', background='#37474F', foreground='#FFC107')
        
        style.configure('Action.TButton', background='#1976D2', foreground='white')
        style.map('Action.TButton',
                 background=[('active', '#1565C0'), ('pressed', '#0D47A1')])
    
    def update_gui(self):
        while self.is_updating:
            try:
                # Update all panels
                self.status_panel.update()
                self.workflow_panel.update()
                self.control_panel.update()
                
                time.sleep(1)
            except Exception as e:
                print(f"GUI update error: {e}")
                time.sleep(2)
    
    def on_closing(self):
        self.is_updating = False
        if self.assistant.is_running:
            self.assistant.stop()
        self.root.destroy()
    
    def log_activity(self, message):
        self.activity_log.add_entry(message)
    
    def run(self):
        self.root.mainloop()