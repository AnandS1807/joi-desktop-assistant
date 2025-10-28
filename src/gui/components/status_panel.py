import tkinter as tk
from tkinter import ttk
import psutil
import os
from src.config.settings import DATA_DIR

class StatusPanel(ttk.LabelFrame):
    def __init__(self, parent, assistant):
        super().__init__(parent, text="Status", style='Dark.TLabelframe', padding=10)
        self.assistant = assistant
        self.setup_panel()
    
    def setup_panel(self):
        # Status row
        status_frame = ttk.Frame(self, style='Dark.TFrame')
        status_frame.pack(fill="x", pady=2)
        
        ttk.Label(status_frame, text="Observation:", style='Status.TLabel', width=12).pack(side="left")
        self.observation_status = ttk.Label(status_frame, text="STOPPED", style='Red.TLabel')
        self.observation_status.pack(side="left", padx=5)
        
        # Automation row
        auto_frame = ttk.Frame(self, style='Dark.TFrame')
        auto_frame.pack(fill="x", pady=2)
        
        ttk.Label(auto_frame, text="Automation:", style='Status.TLabel', width=12).pack(side="left")
        self.automation_status = ttk.Label(auto_frame, text="DISABLED", style='Red.TLabel')
        self.automation_status.pack(side="left", padx=5)
        
        # Storage row
        storage_frame = ttk.Frame(self, style='Dark.TFrame')
        storage_frame.pack(fill="x", pady=2)
        
        ttk.Label(storage_frame, text="Storage:", style='Status.TLabel', width=12).pack(side="left")
        self.storage_status = ttk.Label(storage_frame, text="Calculating...", style='Status.TLabel')
        self.storage_status.pack(side="left", padx=5)
        
        # CPU/Memory row
        sys_frame = ttk.Frame(self, style='Dark.TFrame')
        sys_frame.pack(fill="x", pady=2)
        
        ttk.Label(sys_frame, text="System:", style='Status.TLabel', width=12).pack(side="left")
        self.system_status = ttk.Label(sys_frame, text="", style='Status.TLabel')
        self.system_status.pack(side="left", padx=5)
    
    def update(self):
        # Update observation status
        if self.assistant.is_running:
            self.observation_status.config(text="OBSERVING", style='Green.TLabel')
        else:
            self.observation_status.config(text="STOPPED", style='Red.TLabel')
        
        # Update automation status
        if self.assistant.automation_enabled:
            self.automation_status.config(text="ENABLED", style='Green.TLabel')
        else:
            self.automation_status.config(text="DISABLED", style='Red.TLabel')
        
        # Update storage
        storage_used = self.get_storage_usage()
        self.storage_status.config(text=storage_used)
        
        # Update system info
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        self.system_status.config(text=f"CPU: {cpu_percent:.1f}% | RAM: {memory.percent:.1f}%")
    
    def get_storage_usage(self):
        try:
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(DATA_DIR):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
            
            mb_used = total_size / (1024 * 1024)
            return f"{mb_used:.1f}MB / 5000MB"
        except:
            return "Unknown"