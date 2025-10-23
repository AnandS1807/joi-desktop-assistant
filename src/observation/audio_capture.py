import pyaudio
import wave
import threading
import queue
import os
from datetime import datetime
from src.config.settings import OBSERVATIONS_DIR, AUDIO_CHUNK, AUDIO_CHANNELS, AUDIO_RATE

class AudioCapture:
    def __init__(self):
        self.audio_dir = OBSERVATIONS_DIR / "audio"
        self.audio_dir.mkdir(exist_ok=True)
        self.audio_queue = queue.Queue()
        self.is_recording = False
        self.audio = pyaudio.PyAudio()
        
    def start_recording(self):
        """Start audio recording in separate thread"""
        self.is_recording = True
        self.record_thread = threading.Thread(target=self._record_audio)
        self.record_thread.start()
        
    def stop_recording(self):
        """Stop audio recording"""
        self.is_recording = False
        if hasattr(self, 'record_thread'):
            self.record_thread.join()
            
    def _record_audio(self):
        """Continuous audio recording"""
        stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=AUDIO_CHANNELS,
            rate=AUDIO_RATE,
            input=True,
            frames_per_buffer=AUDIO_CHUNK
        )
        
        frames = []
        chunk_count = 0
        max_chunks = (AUDIO_RATE // AUDIO_CHUNK) * 5  # 5 seconds
        
        while self.is_recording:
            try:
                data = stream.read(AUDIO_CHUNK)
                frames.append(data)
                chunk_count += 1
                
                # Save every 5 seconds
                if chunk_count >= max_chunks:
                    self._save_audio_chunk(frames)
                    frames = []
                    chunk_count = 0
                    
            except Exception as e:
                print(f"Audio recording error: {e}")
                break
        
        stream.stop_stream()
        stream.close()
    
    def _save_audio_chunk(self, frames):
        """Save audio chunk to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"audio_{timestamp}.wav"
        filepath = self.audio_dir / filename
        
        try:
            wf = wave.open(str(filepath), 'wb')
            wf.setnchannels(AUDIO_CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(AUDIO_RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            # Add to processing queue
            self.audio_queue.put(str(filepath))
            
        except Exception as e:
            print(f"Audio save error: {e}")