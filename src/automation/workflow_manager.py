import json
import os
from datetime import datetime
from pathlib import Path
from src.config.settings import WORKFLOWS_DIR

class WorkflowManager:
    def __init__(self):
        self.workflows_file = WORKFLOWS_DIR / "learned_workflows.json"
        self.workflows_file.parent.mkdir(exist_ok=True)
        self.learned_workflows = self._load_workflows()
    
    def _load_workflows(self):
        """Load learned workflows from file"""
        if self.workflows_file.exists():
            try:
                with open(self.workflows_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_workflow(self, workflow_data):
        """Save a detected workflow"""
        workflow_id = f"{workflow_data['workflow_name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        workflow = {
            'id': workflow_id,
            'name': workflow_data['workflow_name'],
            'description': workflow_data.get('description', ''),
            'confidence': workflow_data.get('confidence', 0),
            'trigger_conditions': workflow_data.get('trigger_conditions', []),
            'recommended_actions': workflow_data.get('recommended_actions', []),
            'detected_at': datetime.now().isoformat(),
            'execution_count': 0
        }
        
        # Check if similar workflow already exists
        existing_idx = -1
        for i, wf in enumerate(self.learned_workflows):
            if wf['name'] == workflow['name']:
                existing_idx = i
                break
        
        if existing_idx >= 0:
            # Update existing workflow
            self.learned_workflows[existing_idx] = workflow
        else:
            # Add new workflow
            self.learned_workflows.append(workflow)
        
        self._save_workflows()
        print(f"💾 Saved workflow: {workflow['name']}")
    
    def _save_workflows(self):
        """Save workflows to file"""
        try:
            with open(self.workflows_file, 'w') as f:
                json.dump(self.learned_workflows, f, indent=2)
        except Exception as e:
            print(f"❌ Failed to save workflows: {e}")
    
    def get_workflows(self):
        """Get all learned workflows"""
        return self.learned_workflows
    
    def get_high_confidence_workflows(self, min_confidence=0.8):
        """Get workflows with high confidence"""
        return [wf for wf in self.learned_workflows if wf['confidence'] >= min_confidence]
    
    def increment_execution_count(self, workflow_name):
        """Increment execution count for a workflow"""
        for workflow in self.learned_workflows:
            if workflow['name'] == workflow_name:
                workflow['execution_count'] = workflow.get('execution_count', 0) + 1
                workflow['last_executed'] = datetime.now().isoformat()
                break
        self._save_workflows()