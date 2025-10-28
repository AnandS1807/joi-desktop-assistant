import tkinter as tk
from tkinter import ttk
from datetime import datetime

class WorkflowPanel(ttk.LabelFrame):
    def __init__(self, parent, assistant):
        super().__init__(parent, text="Detected Workflows", style='Dark.TLabelframe', padding=10)
        self.assistant = assistant
        self.setup_panel()
        self.workflows = []
    
    def setup_panel(self):
        # Create treeview for workflows
        columns = ('name', 'confidence', 'last_detected', 'executions')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=8)
        
        # Define headings
        self.tree.heading('name', text='Workflow Name')
        self.tree.heading('confidence', text='Confidence')
        self.tree.heading('last_detected', text='Last Detected')
        self.tree.heading('executions', text='Executions')
        
        # Define columns
        self.tree.column('name', width=200)
        self.tree.column('confidence', width=80)
        self.tree.column('last_detected', width=120)
        self.tree.column('executions', width=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Context menu
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Execute Now", command=self.execute_selected)
        self.context_menu.add_command(label="View Details", command=self.view_details)
        
        self.tree.bind("<Button-3>", self.show_context_menu)
    
    def update(self):
        try:
            # Get workflows from manager
            workflows = self.assistant.workflow_manager.get_high_confidence_workflows(0.5)
            
            # Update if changed
            if workflows != self.workflows:
                self.workflows = workflows
                self.refresh_treeview()
        except Exception as e:
            print(f"Workflow panel update error: {e}")
    
    def refresh_treeview(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add workflows to treeview
        for wf in self.workflows:
            confidence_percent = f"{wf.get('confidence', 0) * 100:.0f}%"
            last_detected = wf.get('detected_at', 'Never')
            executions = wf.get('execution_count', 0)
            
            # Format timestamp if it exists
            if last_detected != 'Never':
                try:
                    dt = datetime.fromisoformat(last_detected.replace('Z', '+00:00'))
                    last_detected = dt.strftime('%H:%M')
                except:
                    pass
            
            self.tree.insert('', 'end', values=(
                wf['name'],
                confidence_percent,
                last_detected,
                executions
            ))
    
    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def execute_selected(self):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            workflow_name = item['values'][0]
            
            # Find and execute the workflow
            for wf in self.workflows:
                if wf['name'] == workflow_name:
                    success = self.assistant.workflow_executor.execute_workflow(wf)
                    if success:
                        print(f"✅ Manually executed: {workflow_name}")
                    break
    
    def view_details(self):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            workflow_name = item['values'][0]
            
            # Show details in a simple dialog
            details_window = tk.Toplevel(self)
            details_window.title(f"Workflow: {workflow_name}")
            details_window.geometry("400x300")
            
            ttk.Label(details_window, text=f"Details for: {workflow_name}", 
                     font=('Arial', 12, 'bold')).pack(pady=10)
            
            # Add more details here as needed
            ttk.Label(details_window, text="Workflow details coming soon...").pack(pady=5)
            
            ttk.Button(details_window, text="Close", 
                      command=details_window.destroy).pack(pady=10)