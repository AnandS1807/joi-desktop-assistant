import json
import re
from datetime import datetime, timedelta
from collections import defaultdict, deque

class BehaviorAnalyzer:
    def __init__(self):
        self.workflow_patterns = []
        self.observed_actions = deque(maxlen=100)  # Keep last 100 actions
        self.session_start = datetime.now()
        self.application_usage = defaultdict(int)
        self.action_sequences = defaultdict(list)
        
    def analyze_behavior(self, screen_data, audio_data, input_events):
        """Enhanced behavior analysis with temporal context"""
        
        # Build comprehensive context
        context = self._build_enhanced_context(screen_data, audio_data, input_events)
        
        # Update session tracking
        self._update_session_tracking(context)
        
        # Generate multi-level analysis
        analysis = self._generate_enhanced_analysis(context)
        
        # Check for automation patterns with temporal awareness
        automation_suggestion = self._check_enhanced_automation_patterns(analysis, context)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis,
            "automation_suggestion": automation_suggestion,
            "context": context,
            "session_duration": (datetime.now() - self.session_start).total_seconds()
        }
    
    def _build_enhanced_context(self, screen_data, audio_data, input_events):
        """Build comprehensive context with temporal data"""
        current_window = screen_data.get('active_window', 'Unknown') if screen_data else 'Unknown'
        window_title = screen_data.get('window_title', 'Unknown') if screen_data else 'Unknown'
        
        # Extract application name from window title
        app_name = self._extract_application_name(current_window, window_title)
        
        # Analyze input patterns
        input_pattern = self._analyze_input_pattern(input_events)
        
        context = {
            "application": app_name,
            "current_window": current_window,
            "window_title": window_title,
            "mouse_position": f"{screen_data.get('mouse_x', 0)},{screen_data.get('mouse_y', 0)}" if screen_data else "0,0",
            "audio_command": audio_data.get('text', '') if audio_data else '',
            "audio_confidence": audio_data.get('confidence', 0) if audio_data else 0,
            "recent_actions": [event.event_type for event in input_events[-10:]] if input_events else [],
            "input_pattern": input_pattern,
            "timestamp": datetime.now().isoformat(),
            "application_usage_count": self.application_usage[app_name]
        }
        
        # Store for pattern recognition
        self.observed_actions.append({
            "app": app_name,
            "action": input_pattern,
            "timestamp": datetime.now(),
            "audio": audio_data.get('text', '') if audio_data else ''
        })
        
        return context
    
    def _extract_application_name(self, current_window, window_title):
        """Extract clean application name from window data"""
        # Common application patterns
        app_patterns = {
            'excel': ['excel', 'xlsx', 'xls'],
            'word': ['word', 'docx', 'doc'],
            'chrome': ['chrome', 'google'],
            'firefox': ['firefox', 'mozilla'],
            'explorer': ['explorer', 'file', 'folder'],
            'vscode': ['code', 'visual studio'],
            'notepad': ['notepad', 'txt'],
            'powerpoint': ['powerpoint', 'ppt'],
            'outlook': ['outlook', 'email']
        }
        
        combined_text = (current_window + ' ' + window_title).lower()
        
        for app_name, patterns in app_patterns.items():
            if any(pattern in combined_text for pattern in patterns):
                return app_name
        
        return 'unknown'
    
    def _analyze_input_pattern(self, input_events):
        """Analyze input events to detect patterns"""
        if not input_events:
            return "no_input"
        
        events = input_events[-20:]  # Last 20 events
        
        # Count event types
        event_counts = defaultdict(int)
        for event in events:
            event_counts[event.event_type] += 1
        
        # Detect patterns
        if event_counts['key_press'] > 10:
            return "typing"
        elif event_counts['mouse_click'] > 5:
            return "clicking"
        elif event_counts['mouse_move'] > 15:
            return "navigating"
        elif event_counts['mouse_scroll'] > 3:
            return "scrolling"
        else:
            return "mixed_input"
    
    def _update_session_tracking(self, context):
        """Update session-level tracking"""
        app_name = context['application']
        self.application_usage[app_name] += 1
        
        # Track action sequences per application
        if len(self.observed_actions) > 0:
            last_action = self.observed_actions[-1]
            if last_action['app'] == app_name:
                self.action_sequences[app_name].append(context['input_pattern'])
                # Keep only recent sequences
                if len(self.action_sequences[app_name]) > 10:
                    self.action_sequences[app_name] = self.action_sequences[app_name][-10:]
    
    def _generate_enhanced_analysis(self, context):
        """Generate comprehensive behavior analysis"""
        app_name = context['application']
        audio_text = context['audio_command'].lower()
        input_pattern = context['input_pattern']
        window_title = context['window_title'].lower()
        
        # Base analysis by application
        base_analysis = self._get_application_analysis(app_name, window_title, input_pattern)
        
        # Enhance with audio commands
        audio_enhanced = self._enhance_with_audio(base_analysis, audio_text, context['audio_confidence'])
        
        # Add temporal context
        temporal_enhanced = self._add_temporal_context(audio_enhanced, context)
        
        return temporal_enhanced
    
    def _get_application_analysis(self, app_name, window_title, input_pattern):
        """Get detailed analysis based on application and behavior"""
        
        application_profiles = {
            'excel': {
                'tasks': {
                    'data_entry': ['typing', 'navigating'],
                    'formula_work': ['typing', 'mixed_input'],
                    'formatting': ['clicking', 'mixed_input'],
                    'chart_creation': ['clicking', 'navigating']
                },
                'confidence_base': 0.8
            },
            'word': {
                'tasks': {
                    'document_writing': ['typing', 'mixed_input'],
                    'editing': ['typing', 'clicking'],
                    'formatting': ['clicking', 'mixed_input'],
                    'reviewing': ['scrolling', 'mixed_input']
                },
                'confidence_base': 0.7
            },
            'chrome': {
                'tasks': {
                    'web_browsing': ['navigating', 'scrolling'],
                    'form_filling': ['typing', 'clicking'],
                    'research': ['typing', 'mixed_input'],
                    'shopping': ['clicking', 'scrolling']
                },
                'confidence_base': 0.6
            },
            'explorer': {
                'tasks': {
                    'file_organization': ['clicking', 'navigating'],
                    'file_search': ['typing', 'mixed_input'],
                    'copy_move_operations': ['clicking', 'mixed_input']
                },
                'confidence_base': 0.75
            },
            'vscode': {
                'tasks': {
                    'coding': ['typing', 'mixed_input'],
                    'debugging': ['clicking', 'mixed_input'],
                    'file_navigation': ['navigating', 'clicking']
                },
                'confidence_base': 0.8
            }
        }
        
        profile = application_profiles.get(app_name, {
            'tasks': {'general_usage': ['mixed_input']},
            'confidence_base': 0.5
        })
        
        # Find best matching task
        best_task = 'general_usage'
        best_confidence = profile['confidence_base']
        
        for task, patterns in profile['tasks'].items():
            if input_pattern in patterns:
                best_task = task
                best_confidence = profile['confidence_base'] + 0.15
                break
        
        # Enhance with window title keywords
        title_enhancement = self._analyze_window_title(window_title, app_name)
        if title_enhancement:
            best_task = title_enhancement['task']
            best_confidence += 0.1
        
        return {
            "current_task": f"{app_name}_{best_task}",
            "observed_steps": self._get_task_steps(app_name, best_task),
            "automation_potential": self._get_automation_potential(app_name, best_task),
            "confidence": min(best_confidence, 0.95),  # Cap at 0.95
            "application": app_name,
            "input_pattern": input_pattern
        }
    
    def _analyze_window_title(self, window_title, app_name):
        """Analyze window title for specific task clues"""
        title_lower = window_title.lower()
        
        title_patterns = {
            'excel': {
                'budget': {'task': 'budget_management', 'confidence_boost': 0.1},
                'report': {'task': 'report_generation', 'confidence_boost': 0.1},
                'sales': {'task': 'sales_analysis', 'confidence_boost': 0.1},
                'invoice': {'task': 'invoice_processing', 'confidence_boost': 0.15}
            },
            'word': {
                'report': {'task': 'report_writing', 'confidence_boost': 0.1},
                'resume': {'task': 'resume_creation', 'confidence_boost': 0.1},
                'letter': {'task': 'letter_writing', 'confidence_boost': 0.1},
                'proposal': {'task': 'proposal_creation', 'confidence_boost': 0.15}
            },
            'chrome': {
                'google': {'task': 'searching', 'confidence_boost': 0.1},
                'youtube': {'task': 'video_watching', 'confidence_boost': 0.05},
                'mail': {'task': 'email_management', 'confidence_boost': 0.1},
                'shopping': {'task': 'online_shopping', 'confidence_boost': 0.1}
            }
        }
        
        patterns = title_patterns.get(app_name, {})
        for keyword, enhancement in patterns.items():
            if keyword in title_lower:
                return enhancement
        
        return None
    
    def _get_task_steps(self, app_name, task):
        """Get typical steps for a task"""
        task_steps = {
            'excel_data_entry': ["Open Excel", "Select cells", "Enter data", "Save file"],
            'excel_formula_work': ["Open Excel", "Select cells", "Enter formulas", "Calculate results", "Save file"],
            'word_document_writing': ["Open Word", "Type content", "Format text", "Save document"],
            'chrome_web_browsing': ["Open browser", "Navigate to website", "Scroll content", "Click links"],
            'explorer_file_organization': ["Open File Explorer", "Select files", "Move/copy files", "Create folders"]
        }
        
        key = f"{app_name}_{task}"
        return task_steps.get(key, [f"Working in {app_name}", "Performing various actions"])
    
    def _get_automation_potential(self, app_name, task):
        """Determine automation potential"""
        high_potential_tasks = [
            'excel_data_entry', 'excel_formula_work', 'excel_report_generation',
            'word_document_writing', 'explorer_file_organization'
        ]
        
        medium_potential_tasks = [
            'chrome_form_filling', 'chrome_research', 'word_editing'
        ]
        
        task_key = f"{app_name}_{task}"
        
        if task_key in high_potential_tasks:
            return "High"
        elif task_key in medium_potential_tasks:
            return "Medium"
        else:
            return "Low"
    
    def _enhance_with_audio(self, analysis, audio_text, audio_confidence):
        """Enhance analysis with audio commands"""
        if not audio_text or audio_confidence < 0.5:
            return analysis
        
        audio_commands = {
            'open': {'task_modifier': 'opening', 'confidence_boost': 0.2},
            'save': {'task_modifier': 'saving', 'confidence_boost': 0.25},
            'create': {'task_modifier': 'creating', 'confidence_boost': 0.2},
            'search': {'task_modifier': 'searching', 'confidence_boost': 0.15},
            'send': {'task_modifier': 'sending', 'confidence_boost': 0.2}
        }
        
        for command, enhancement in audio_commands.items():
            if command in audio_text:
                analysis['current_task'] = f"{analysis['application']}_{enhancement['task_modifier']}"
                analysis['confidence'] = min(analysis['confidence'] + enhancement['confidence_boost'], 0.95)
                analysis['audio_triggered'] = True
                break
        
        return analysis
    
    def _add_temporal_context(self, analysis, context):
        """Add temporal context to analysis"""
        app_usage_count = context['application_usage_count']
        
        # Boost confidence for frequently used applications
        if app_usage_count > 5:
            analysis['confidence'] = min(analysis['confidence'] + 0.1, 0.95)
            analysis['frequently_used'] = True
        
        # Add sequence awareness
        recent_sequences = self.action_sequences.get(context['application'], [])
        if len(recent_sequences) > 3:
            analysis['sequence_aware'] = True
            analysis['confidence'] = min(analysis['confidence'] + 0.05, 0.95)
        
        return analysis
    
    def _check_enhanced_automation_patterns(self, analysis, context):
        """Check for automation patterns with enhanced logic"""
        confidence = analysis['confidence']
        automation_potential = analysis['automation_potential']
        
        if confidence > 0.75 and automation_potential in ["High", "Medium"]:
            return {
                "workflow_name": analysis['current_task'],
                "description": f"Automate {analysis['current_task'].replace('_', ' ')}",
                "confidence": confidence,
                "automation_potential": automation_potential,
                "recommended_actions": analysis['observed_steps'],
                "application": analysis['application'],
                "trigger_conditions": self._get_trigger_conditions(analysis, context)
            }
        return None
    
    def _get_trigger_conditions(self, analysis, context):
        """Get conditions that trigger this workflow"""
        conditions = [
            f"Application: {analysis['application']}",
            f"Window contains: {context['window_title']}",
            f"Input pattern: {context['input_pattern']}"
        ]
        
        if context['audio_command']:
            conditions.append(f"Voice command: {context['audio_command']}")
        
        return conditions