import speech_recognition as sr
import threading
import time
import queue

class SpeechProcessor:
    """Handles voice input and conversion to text commands"""
    
    def __init__(self, command_callback=None):
        """Initialize the speech processor"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.audio_queue = queue.Queue()
        self.text_queue = queue.Queue()
        self.command_callback = command_callback
        self.listen_thread = None
        self.process_thread = None
        
        # Adjust for ambient noise
        with self.microphone as source:
            print("Calibrating for ambient noise... Please wait.")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("Calibration complete!")
    
    def start_listening(self):
        """Start listening to the microphone in a separate thread"""
        if self.is_listening:
            print("Already listening!")
            return
            
        self.is_listening = True
        self.listen_thread = threading.Thread(target=self._listen_loop)
        self.process_thread = threading.Thread(target=self._process_loop)
        
        self.listen_thread.daemon = True
        self.process_thread.daemon = True
        
        self.listen_thread.start()
        self.process_thread.start()
        
        print("Now listening to your microphone...")
    
    def stop_listening(self):
        """Stop listening to the microphone"""
        self.is_listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
        if self.process_thread:
            self.process_thread.join(timeout=2)
        print("Stopped listening.")
    
    def _listen_loop(self):
        """Continuously listen to the microphone and queue audio chunks"""
        while self.is_listening:
            try:
                with self.microphone as source:
                    print("Listening for speech...")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    self.audio_queue.put(audio)
                    print("Audio captured!")
            except sr.WaitTimeoutError:
                print("No speech detected. Still listening...")
            except Exception as e:
                print(f"Error capturing audio: {e}")
                time.sleep(1)  # Prevent tight loop on error
    
    def _process_loop(self):
        """Process audio chunks from the queue and convert to text"""
        while self.is_listening or not self.audio_queue.empty():
            try:
                if not self.audio_queue.empty():
                    audio = self.audio_queue.get()
                    text = self.process_audio_chunk(audio)
                    if text:
                        print(f"Recognized: {text}")
                        self.text_queue.put(text)
                        if self.command_callback:
                            command = self.detect_command(text)
                            if command:
                                self.command_callback(command)
                else:
                    time.sleep(0.1)  # Small delay to prevent CPU spinning
            except Exception as e:
                print(f"Error processing audio: {e}")
    
    def process_audio_chunk(self, audio_chunk):
        """Convert audio to text using speech recognition API"""
        try:
            # Use Google's speech recognition service
            text = self.recognizer.recognize_google(audio_chunk)
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
    
    def detect_command(self, transcript):
        """Parse transcript to identify commands"""
        if not transcript:
            return None
            
        transcript = transcript.lower()
        
        # Command patterns
        if "create" in transcript and "agent" in transcript:
            # Extract agent name
            # Simple extraction - in a real app, use NLP for better extraction
            parts = transcript.split("named")
            if len(parts) > 1:
                agent_name = parts[1].strip()
                return {
                    "type": "create_agent",
                    "name": agent_name,
                    "description": "Agent created from voice command"
                }
        
        if "set scope" in transcript or "define scope" in transcript:
            # Extract agent name and scope
            # This is simplified - would need more robust parsing in production
            for agent_name in self.get_known_agents():
                if agent_name in transcript:
                    scope_parts = transcript.split("to")
                    if len(scope_parts) > 1:
                        scope = scope_parts[1].strip()
                        return {
                            "type": "define_scope",
                            "agent_name": agent_name,
                            "scope": scope
                        }
        
        if "add instruction" in transcript:
            # Extract agent name and instruction
            for agent_name in self.get_known_agents():
                if agent_name in transcript:
                    instruction_parts = transcript.split("instruction")
                    if len(instruction_parts) > 1:
                        instruction = instruction_parts[1].strip()
                        return {
                            "type": "add_instruction",
                            "agent_name": agent_name,
                            "instruction": instruction
                        }
        
        # More command patterns could be added here
        
        return None
    
    def get_known_agents(self):
        """Returns a list of known agent names - would be populated from AgentManager"""
        # This is a placeholder - in a real app, this would get the list from AgentManager
        return ["assistant", "researcher", "writer"]