import time
import threading
import json
from datetime import datetime
from pathlib import Path

from src.observation.audio_capture import AudioCapture
from src.observation.screen_capture import ScreenCapture
from src.observation.input_tracker import InputTracker
from src.processing.speech_to_text import SpeechToText
from src.processing.behavior_analyzer import BehaviorAnalyzer
from src.data.storage_manager import StorageManager
from src.config.settings import CAPTURE_INTERVAL

class AIAssistant:
    def __init__(self):
        print("🚀 Initializing AI Assistant...")
        
        # Initialize components
        self.screen_capture = ScreenCapture()
        self.audio_capture = AudioCapture()
        self.input_tracker = InputTracker()
        self.speech_to_text = SpeechToText()
        self.behavior_analyzer = BehaviorAnalyzer()
        self.storage_manager = StorageManager()
        
        self.is_running = False
        self.observation_thread = None
        
        # Data buffers
        self.recent_audio = []
        self.insights_history = []
        
        print("✅ AI Assistant initialized!")
    
    def start(self):
        """Start the AI assistant"""
        if self.is_running:
            print("⚠️ Assistant is already running!")
            return
        
        print("🎯 Starting AI Assistant...")
        self.is_running = True
        
        # Start all observers
        self.audio_capture.start_recording()
        self.input_tracker.start_tracking()
        
        # Start main observation loop
        self.observation_thread = threading.Thread(target=self._observation_loop)
        self.observation_thread.start()
        
        # Start audio processing thread
        self.audio_processing_thread = threading.Thread(target=self._audio_processing_loop)
        self.audio_processing_thread.start()
        
        print("🔍 AI Assistant is now observing your desktop...")
        print("💡 Say commands like 'open Excel' or 'save file'")
        print("⏹️  Press Ctrl+C to stop")
    
    def stop(self):
        """Stop the AI assistant"""
        print("🛑 Stopping AI Assistant...")
        self.is_running = False
        
        # Stop all components
        self.audio_capture.stop_recording()
        self.input_tracker.stop_tracking()
        
        # Wait for threads to finish
        if self.observation_thread:
            self.observation_thread.join()
        if self.audio_processing_thread:
            self.audio_processing_thread.join()
        
        print("✅ AI Assistant stopped!")
    
    def _observation_loop(self):
        """Main observation loop"""
        while self.is_running:
            try:
                # Capture screen
                screen_data = self.screen_capture.capture_screenshot()
                
                # Get recent input events
                input_events = self.input_tracker.get_recent_events(10)
                
                # Get latest audio transcript
                audio_data = self._get_latest_audio()
                
                # Analyze behavior
                if screen_data:
                    analysis = self.behavior_analyzer.analyze_behavior(
                        screen_data, audio_data, input_events
                    )
                    
                    # Store insights
                    self.storage_manager.save_insight(analysis)
                    self.insights_history.append(analysis)
                    
                    # Display insights
                    self._display_insights(analysis)
                
                time.sleep(CAPTURE_INTERVAL)
                
            except Exception as e:
                print(f"❌ Observation error: {e}")
                time.sleep(1)
    
# In the _audio_processing_loop method, replace the transcription part:
    def _audio_processing_loop(self):
        """Process audio files in background with context"""
        while self.is_running:
            try:
                # Check for new audio files
                if hasattr(self.audio_capture, 'audio_queue') and not self.audio_capture.audio_queue.empty():
                    audio_path = self.audio_capture.audio_queue.get()
                    
                    # Get conversation context
                    conversation_context = self.audio_capture.get_conversation_context()
                    
                    # Transcribe with context
                    transcript = self.speech_to_text.transcribe_audio(
                        audio_path, 
                        cleanup=True, 
                        conversation_context=conversation_context
                    )
                    
                    if transcript["text"] and len(transcript["text"].strip()) > 2:
                        # Update conversation context
                        self.audio_capture.update_conversation_context(transcript["text"])
                        self.recent_audio.append(transcript)
                        print(f"🎤 Voice: '{transcript['text']}'")
                        
                        # Show context if available
                        if transcript.get('has_context'):
                            context = self.audio_capture.get_conversation_context()
                            if len(context) > 1:
                                print(f"   📝 Context: {len(context)} previous utterances")
                        
                        # Keep only recent audio
                        if len(self.recent_audio) > 5:
                            self.recent_audio = self.recent_audio[-5:]
                
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Audio processing error: {e}")
                time.sleep(1)
    
    def _get_latest_audio(self):
        """Get most recent audio transcript"""
        return self.recent_audio[-1] if self.recent_audio else None
    
    def _display_insights(self, analysis):
        """Display behavior insights"""
        task = analysis["analysis"]["current_task"]
        confidence = analysis["analysis"]["confidence"]
        
        if confidence > 0.7:
            print(f"🔍 Detected: {task} (Confidence: {confidence:.2f})")
            
            if analysis["automation_suggestion"]:
                suggestion = analysis["automation_suggestion"]
                print(f"💡 Suggestion: {suggestion['workflow_name']}")

def main():
    assistant = AIAssistant()
    
    try:
        assistant.start()
        
        # Keep main thread alive
        while assistant.is_running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Received interrupt signal...")
    finally:
        assistant.stop()

if __name__ == "__main__":
    main()