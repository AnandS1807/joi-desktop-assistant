#!/usr/bin/env python3
"""
Independent test for Speech-to-Text functionality
Records audio from microphone and transcribes it
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))


import pyaudio
import wave
import time

def record_test_audio(duration=5, filename="test_audio.wav"):
    """Record audio for testing"""
    print("\n🎤 Recording audio for 5 seconds... Speak now!")
    print("💡 Tip: Speak clearly into your microphone\n")
    
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    
    p = pyaudio.PyAudio()
    
    try:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        
        frames = []
        
        for i in range(0, int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK)
            frames.append(data)
            # Show recording progress
            if i % 10 == 0:
                print(f"⏺️  Recording... {int(i/10)}/5 seconds")
        
        print("⏺️  Recording... 5/5 seconds")
        
        stream.stop_stream()
        stream.close()
        
    except Exception as e:
        print(f"❌ Error during recording: {e}")
        return None
    finally:
        p.terminate()
    
    # Save the recorded data
    try:
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        print(f"\n✅ Audio saved as {filename}")
        return filename
    except Exception as e:
        print(f"❌ Error saving audio: {e}")
        return None

def test_speech_to_text():
    """Test the speech to text functionality"""
    print("=" * 60)
    print("🧪 SPEECH-TO-TEXT TEST")
    print("=" * 60)
    
    # Initialize the speech-to-text engine
    print("\n📦 Initializing Whisper model...")
    stt = SpeechToText()
    
    # Record new audio
    print("\n" + "=" * 60)
    print("STEP 1: Recording Audio")
    print("=" * 60)
    audio_file = record_test_audio(duration=5)
    
    if audio_file is None:
        print("❌ Recording failed. Exiting...")
        return
    
    # Test transcription
    print("\n" + "=" * 60)
    print("STEP 2: Transcribing Audio")
    print("=" * 60)
    print("🔄 Processing audio with Whisper AI...")
    
    result = stt.transcribe_audio(audio_file)
    
    print("\n" + "=" * 60)
    print("📝 TRANSCRIPTION RESULTS")
    print("=" * 60)
    
    if result['text']:
        print(f"\n✅ Transcribed Text:\n   \"{result['text']}\"")
        print(f"\n📊 Confidence: {result['confidence']}")
        print(f"🌍 Language: {result.get('language', 'N/A')}")
    else:
        print(f"\n❌ No text transcribed")
        if 'error' in result:
            print(f"   Error: {result['error']}")
    
    # Test with non-existent file (error handling)
    print("\n" + "=" * 60)
    print("STEP 3: Testing Error Handling")
    print("=" * 60)
    print("🧪 Testing with non-existent file...")
    result = stt.transcribe_audio("non_existent_file.wav")
    
    if 'error' in result:
        print(f"✅ Error handling works correctly: {result['error']}")
    else:
        print(f"Result: {result}")
    
    print("\n" + "=" * 60)
    print("✅ TEST COMPLETE")
    print("=" * 60)
    
    # Cleanup
    if os.path.exists(audio_file):
        try:
            os.remove(audio_file)
            print(f"\n🧹 Cleaned up temporary file: {audio_file}")
        except:
            pass

if __name__ == "__main__":
    try:
        test_speech_to_text()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()