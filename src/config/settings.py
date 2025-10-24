import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
OBSERVATIONS_DIR = DATA_DIR / "observations"
WORKFLOWS_DIR = DATA_DIR / "workflows"

# Create directories
for directory in [DATA_DIR, MODELS_DIR, OBSERVATIONS_DIR, WORKFLOWS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Observation settings
CAPTURE_INTERVAL = 2.0  # seconds
MAX_OBSERVATION_HISTORY = 1000
SCREEN_CAPTURE_QUALITY = 0.7  # Compression quality

# Audio settings
AUDIO_CHUNK = 1024
AUDIO_CHANNELS = 1
AUDIO_FORMAT = 'pyaudio.paInt16'
AUDIO_RATE = 16000
AUDIO_RECORD_SECONDS = 10

# Model settings
WHISPER_MODEL = "base"  # "tiny", "base", "small", "medium", "large"
LLM_MODEL = "microsoft/DialoGPT-medium"

# Automation settings
AUTOMATION_CONFIDENCE_THRESHOLD = 0.7
MIN_PATTERN_OCCURRENCES = 3

# Privacy settings
ENABLE_CLOUD_UPLOAD = False
MAX_LOCAL_STORAGE_GB = 5