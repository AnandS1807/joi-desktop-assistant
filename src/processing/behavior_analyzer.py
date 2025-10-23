import json
import re
from datetime import datetime

class BehaviorAnalyzer:
    def __init__(self):
        self.workflow_patterns = []
        self.observed_actions = []
        
    def analyze_behavior(self, screen_data, audio_data, input_events):
        """Analyze user behavior and generate insights"""
        
        # Build context from observations
        context = self._build_context(screen_data, audio_data, input_events)
        
        # Generate analysis
        analysis = self._generate_analysis(context)
        
        # Check for automation patterns
        automation_suggestion = self._check_automation_patterns(analysis)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis,
            "automation_suggestion": automation_suggestion,
            "context": context
        }
    
    def _build_context(self, screen_data, audio_data, input_events):
        """Build context from all observations"""
        context = {
            "current_window": screen_data.get('active_window', 'Unknown') if screen_data else 'Unknown',
            "window_title": screen_data.get('window_title', 'Unknown') if screen_data else 'Unknown',
            "mouse_position": f"{screen_data.get('mouse_x', 0)},{screen_data.get('mouse_y', 0)}" if screen_data else "0,0",
            "audio_command": audio_data.get('text', '') if audio_data else '',
            "recent_actions": [event.event_type for event in input_events[-5:]] if input_events else []
        }
        return context
    
    def _generate_analysis(self, context):
        """Generate behavior analysis using rule-based approach"""
        
        # Rule-based analysis
        current_window = context["current_window"].lower()
        window_title = context["window_title"].lower()
        audio_text = context["audio_command"].lower()
        
        if "excel" in current_window or "excel" in window_title:
            task = "Excel Data Processing"
            steps = ["Opening Excel", "Entering data", "Applying formulas", "Saving file"]
            automation_potential = "High"
            confidence = 0.8
            
        elif "chrome" in current_window or "browser" in current_window or "mozilla" in current_window:
            task = "Web Browsing"
            steps = ["Navigating websites", "Filling forms", "Searching information"]
            automation_potential = "Medium"
            confidence = 0.6
            
        elif "explorer" in current_window or "folder" in window_title or "file" in window_title:
            task = "File Management"
            steps = ["Opening files", "Moving files", "Renaming files"]
            automation_potential = "High"
            confidence = 0.7
            
        else:
            task = "General Computer Usage"
            steps = ["Various desktop activities"]
            automation_potential = "Low"
            confidence = 0.3
        
        # Enhance with audio commands
        if "open" in audio_text and "excel" in audio_text:
            task = "Opening Excel Application"
            automation_potential = "High"
            confidence = 0.9
        elif "save" in audio_text and "file" in audio_text:
            task = "Saving Document"
            automation_potential = "High"
            confidence = 0.9
        elif "create" in audio_text and "document" in audio_text:
            task = "Creating New Document"
            automation_potential = "High"
            confidence = 0.8
        
        return {
            "current_task": task,
            "observed_steps": steps,
            "automation_potential": automation_potential,
            "confidence": confidence,
            "recommendation": f"Consider automating this {task} workflow"
        }
    
    def _check_automation_patterns(self, analysis):
        """Check if current activity suggests automatable workflow"""
        if analysis["confidence"] > 0.7:
            return {
                "workflow_name": analysis["current_task"],
                "description": f"Automate {analysis['current_task']}",
                "confidence": analysis["confidence"],
                "recommended_actions": analysis["observed_steps"]
            }
        return None