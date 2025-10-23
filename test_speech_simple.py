#!/usr/bin/env python3
"""
Simple standalone speech-to-text test
"""
import whisper
import pyaudio
import wave
import time
import numpy as np

def record_audio(duration=5, filename="test_speech.wav"):
    """Record audio for testing"""
    print("🎤 Recording audio for 5 seconds... Speak now!")
    
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    frames = []
    
    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)
        if i % 10 == 0:
            print(f"⏺️ Recording... {i/10}/5 seconds")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # Save the recorded data
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    print(f"✅ Audio saved as {filename}")
    return filename

def load_audio_without_ffmpeg(filename):
    """Load audio directly from WAV file without FFmpeg"""
    with wave.open(filename, 'rb') as wf:
        # Read audio data
        audio_data = wf.readframes(wf.getnframes())
        
        # Convert to numpy array
        audio = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
        
        # Resample if needed (Whisper expects 16kHz)
        sample_rate = wf.getframerate()
        if sample_rate != 16000:
            # Simple resampling (you might want to use scipy for better quality)
            from scipy import signal
            num_samples = int(len(audio) * 16000 / sample_rate)
            audio = signal.resample(audio, num_samples)
        
        return audio

def test_whisper():
    """Test Whisper directly"""
    print("🧪 Loading Whisper model...")
    model = whisper.load_model("base")
    print("✅ Model loaded!")
    
    # Record audio
    audio_file = record_audio()
    
    # Load audio without FFmpeg
    print("📝 Loading audio...")
    audio = load_audio_without_ffmpeg(audio_file)
    
    # Transcribe
    print("📝 Transcribing...")
    result = model.transcribe(audio)
    
    print("\n🎯 RESULTS:")
    print(f"Text: '{result['text']}'")
    print(f"Language: {result['language']}")

if __name__ == "__main__":
    test_whisper()