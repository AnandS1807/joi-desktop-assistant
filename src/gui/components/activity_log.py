import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime

class ActivityLog(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Activity Log", style='Dark.TLabelframe', padding=10)
        self.setup_panel()
        self.entries = []
        self.max_entries = 50
    
    def setup_panel(self):
        # Create text widget with scrollbar
        self.text_widget = tk.scrolledtext.ScrolledText(  # Changed from scrolledtext to tk.scrolledtext
            self, 
            wrap=tk.WORD, 
            width=60, 
            height=8,
            bg='#1e1e1e',
            fg='white',
            insertbackground='white',
            font=('Consolas', 9)
        )
        self.text_widget.pack(fill="both", expand=True)
        self.text_widget.config(state=tk.DISABLED)
        
        # Clear button
        clear_frame = ttk.Frame(self, style='Dark.TFrame')
        clear_frame.pack(fill="x", pady=5)
        
        ttk.Button(clear_frame, text="Clear Log", 
                  command=self.clear_log, style='Action.TButton').pack(side="right")
    
    def add_entry(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.entries.append(formatted_message)
        
        # Keep only recent entries
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[-self.max_entries:]
        
        # Update text widget
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, formatted_message)
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)
    
    def clear_log(self):
        self.entries = []
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.config(state=tk.DISABLED)