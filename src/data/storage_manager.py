import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from src.config.settings import OBSERVATIONS_DIR, WORKFLOWS_DIR, MAX_LOCAL_STORAGE_GB

class StorageManager:
    def __init__(self):
        self.insights_file = OBSERVATIONS_DIR / "insights.jsonl"
        self.workflows_file = WORKFLOWS_DIR / "workflows.json"
        
    def save_insight(self, insight_data):
        """Save insight data to file"""
        try:
            with open(self.insights_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(insight_data) + '\n')
        except Exception as e:
            print(f"Save insight error: {e}")
    
    def cleanup_old_data(self, max_age_days=7):
        """Clean up data older than specified days"""
        cutoff_time = datetime.now() - timedelta(days=max_age_days)
        
        # Clean up old screenshots
        screenshot_dir = OBSERVATIONS_DIR / "screenshots"
        if screenshot_dir.exists():
            for file in screenshot_dir.glob("*.jpg"):
                if file.stat().st_mtime < cutoff_time.timestamp():
                    file.unlink()
        
        # Clean up old audio files
        audio_dir = OBSERVATIONS_DIR / "audio"
        if audio_dir.exists():
            for file in audio_dir.glob("*.wav"):
                if file.stat().st_mtime < cutoff_time.timestamp():
                    file.unlink()