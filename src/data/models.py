from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime

@dataclass
class ScreenObservation:
    timestamp: str
    screenshot_path: str
    mouse_x: int
    mouse_y: int
    active_window: str
    window_title: str

@dataclass
class AudioObservation:
    timestamp: str
    audio_path: str
    transcript: str
    confidence: float

@dataclass
class InputEvent:
    timestamp: str
    event_type: str  # 'mouse_click', 'key_press', 'mouse_move'
    details: Dict[str, Any]

@dataclass
class WorkflowStep:
    action: str
    target: str
    data: str
    timestamp: str

@dataclass
class AutomationSuggestion:
    workflow_name: str
    description: str
    steps: List[WorkflowStep]
    confidence: float
    frequency: int
    last_observed: str