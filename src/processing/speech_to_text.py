import whisper
import os
import numpy as np
from datetime import datetime
from src.config.settings import WHISPER_MODEL

class SpeechToText:
    def __init__(self):
        print("🔄 Loading Whisper model...")
        try:
            self.model = whisper.load_model(WHISPER_MODEL)
            print("✅ Whisper model loaded!")
        except Exception as e:
            print(f"❌ Failed to load Whisper model: {e}")
            self.model = None

    def _load_audio_without_ffmpeg(self, filename):
        """Load audio directly from WAV file without FFmpeg"""
        try:
            import wave
            with wave.open(filename, 'rb') as wf:
                # Read audio data
                audio_data = wf.readframes(wf.getnframes())
                
                # Convert to numpy array
                audio = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
                
                # Resample if needed (Whisper expects 16kHz)
                sample_rate = wf.getframerate()
                if sample_rate != 16000:
                    try:
                        from scipy import signal
                        num_samples = int(len(audio) * 16000 / sample_rate)
                        audio = signal.resample(audio, num_samples)
                    except ImportError:
                        # Fallback: simple resampling
                        ratio = 16000 / sample_rate
                        new_length = int(len(audio) * ratio)
                        audio = np.interp(
                            np.linspace(0, len(audio)-1, new_length),
                            np.arange(len(audio)),
                            audio
                        )
                
                return audio
        except Exception as e:
            print(f"Audio loading error: {e}")
            return None

    def _cleanup_audio_file(self, audio_path):
        """Remove audio file after processing"""
        try:
            if os.path.exists(audio_path):
                os.remove(audio_path)
                print(f"🗑️ Cleaned up audio file: {os.path.basename(audio_path)}")
        except Exception as e:
            print(f"Cleanup error: {e}")

    def transcribe_audio(self, audio_path, cleanup=True):
        """Transcribe audio file to text and optionally clean up"""
        try:
            if not os.path.exists(audio_path) or self.model is None:
                return {"text": "", "confidence": 0.0}

            # Load audio without FFmpeg
            audio = self._load_audio_without_ffmpeg(audio_path)
            if audio is None:
                return {"text": "", "confidence": 0.0}

            # Transcribe
            result = self.model.transcribe(audio)
            text = result["text"].strip()
            
            # Clean up audio file if requested
            if cleanup:
                self._cleanup_audio_file(audio_path)

            return {
                "text": text,
                "confidence": 0.8 if text else 0.0,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"Transcription error: {e}")
            # Still try to clean up on error
            if cleanup:
                self._cleanup_audio_file(audio_path)
            return {"text": "", "confidence": 0.0}