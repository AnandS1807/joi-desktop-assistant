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
        self.conversation_context = []  # Store recent transcripts for context
        self.max_context_length = 5     # Keep last 5 transcripts
        
    def start_recording(self):
        """Start audio recording in separate thread"""
        self.is_recording = True
        self.record_thread = threading.Thread(target=self._record_audio)
        self.record_thread.daemon = True
        self.record_thread.start()
        
    def stop_recording(self):
        """Stop audio recording"""
        self.is_recording = False
        
    def _record_audio(self):
        """Continuous audio recording with longer chunks"""
        try:
            stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=AUDIO_CHANNELS,
                rate=AUDIO_RATE,
                input=True,
                frames_per_buffer=AUDIO_CHUNK
            )
            
            frames = []
            chunk_count = 0
            max_chunks = (AUDIO_RATE // AUDIO_CHUNK) * 10  # INCREASED to 10 seconds
            
            while self.is_recording:
                try:
                    data = stream.read(AUDIO_CHUNK, exception_on_overflow=False)
                    frames.append(data)
                    chunk_count += 1
                    
                    # Save every 10 seconds (DOUBLE the duration)
                    if chunk_count >= max_chunks:
                        self._save_audio_chunk(frames)
                        frames = []
                        chunk_count = 0
                        
                except Exception as e:
                    print(f"Audio recording error: {e}")
                    break
            
            stream.stop_stream()
            stream.close()
            
        except Exception as e:
            print(f"Audio setup error: {e}")
    
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
            print(f"🎤 Audio chunk saved (10s): {filename}")
            
        except Exception as e:
            print(f"Audio save error: {e}")
    
    def get_queued_audio(self):
        """Get audio files from queue for processing"""
        audio_files = []
        while not self.audio_queue.empty():
            try:
                audio_files.append(self.audio_queue.get_nowait())
            except queue.Empty:
                break
        return audio_files
    
    def update_conversation_context(self, transcript):
        """Update conversation context with new transcript"""
        if transcript and transcript.strip():
            self.conversation_context.append({
                'text': transcript,
                'timestamp': datetime.now().isoformat()
            })
            # Keep only recent context
            if len(self.conversation_context) > self.max_context_length:
                self.conversation_context = self.conversation_context[-self.max_context_length:]

    def get_conversation_context(self):
        """Get recent conversation context"""
        return self.conversation_context.copy()