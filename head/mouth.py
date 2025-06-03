import asyncio
import threading
import os
import tempfile
import time
from pathlib import Path
import edge_tts 
import pygame
from typing import Optional

# Configuration constants
VOICE = "en-AU-WilliamNeural"
AUDIO_FORMAT = ".mp3"

class TTSManager:
    """
    A comprehensive Text-to-Speech manager that handles audio generation,
    playback, and cleanup in a coordinated manner.
    """
    
    def __init__(self, voice: str = VOICE):
        """
        Initialize the TTS manager with a specific voice.
        
        Args:
            voice: The edge-tts voice identifier to use
        """
        self.voice = voice
        self.pygame_initialized = False
        
    def _ensure_pygame_initialized(self):
        """
        Initialize pygame mixer if not already done.
        This approach prevents repeated initialization/quit cycles.
        """
        if not self.pygame_initialized:
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
            pygame.mixer.init()
            self.pygame_initialized = True
    
    def _create_temp_file(self) -> str:
        """
        Create a temporary file for audio storage using Python's tempfile module.
        This is safer than creating files in the current working directory.
        
        Returns:
            str: Path to the temporary file
        """
        # Create a temporary file that won't be automatically deleted
        # We'll manage deletion ourselves to ensure proper cleanup timing
        temp_fd, temp_path = tempfile.mkstemp(suffix=AUDIO_FORMAT, prefix="tts_")
        os.close(temp_fd)  # Close the file descriptor, keep the path
        return temp_path
    
    def _safe_file_removal(self, file_path: str, max_attempts: int = 5, delay: float = 0.1):
        """
        Safely remove a file with retry logic and proper error handling.
        
        Args:
            file_path: Path to the file to remove
            max_attempts: Maximum number of removal attempts
            delay: Delay between attempts in seconds
        """
        if not os.path.exists(file_path):
            return  # File already gone, nothing to do
            
        for attempt in range(max_attempts):
            try:
                os.remove(file_path)
                #print(f"✓ Cleaned up temporary file: {Path(file_path).name}")
                return
            except PermissionError:
                # File might still be in use, wait and retry
                if attempt < max_attempts - 1:
                    #print(f"File in use, retrying in {delay}s... (attempt {attempt + 1}/{max_attempts})")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                # else:
                    # print(f"⚠️ Could not remove {file_path} after {max_attempts} attempts")
            except Exception as ex:
                # print(f"❌ Unexpected error removing file: {ex}")
                break
    
    def _play_audio_sync(self, file_path: str):
        """
        Play audio file synchronously using pygame.
        This method blocks until playback is complete.
        
        Args:
            file_path: Path to the audio file to play
        """
        try:
            self._ensure_pygame_initialized()
            
            # Load and play the sound
            sound = pygame.mixer.Sound(file_path)
            channel = sound.play()
            
            if channel is None:
                raise RuntimeError("Failed to start audio playback")
            
            # Wait for playback to complete with more efficient polling
            while channel.get_busy():
                pygame.time.wait(50)  # Check every 50ms instead of 100ms
                
        except pygame.error as ex:
            # print(f"❌ Pygame audio error: {ex}")
            raise
        except Exception as ex:
            # print(f"❌ Audio playback error: {ex}")
            raise
    
    async def _generate_audio(self, text: str, output_file: str):
        """
        Generate audio file from text using edge-tts.
        
        Args:
            text: Text to convert to speech
            output_file: Path where audio file should be saved
        """
        try:
            # Create the TTS communication object
            communicate = edge_tts.Communicate(text, self.voice)
            await communicate.save(output_file)
            # print(f"✓ Audio generated: {Path(output_file).name}")
        except Exception as ex:
            # print(f"❌ TTS generation failed: {ex}")
            raise
    
    async def speak_async(self, text: str, output_file: Optional[str] = None) -> None:
        """
        Asynchronously convert text to speech and play it.
        This is the main async interface for the TTS system.
        
        Args:
            text: Text to convert to speech
            output_file: Optional custom output file path
        """
        # Use temporary file if no output file specified
        temp_file_created = output_file is None
        if temp_file_created:
            output_file = self._create_temp_file()
        
        try:
            # print(f"🗣️ Converting to speech: '{text[:50]}{'...' if len(text) > 50 else ''}'")
            
            # Generate the audio file
            await self._generate_audio(text, output_file)
            
            # Play the audio in a separate thread to avoid blocking the async loop
            # Using threading here is appropriate because audio playback is I/O bound
            def play_in_thread():
                self._play_audio_sync(output_file)
            
            thread = threading.Thread(target=play_in_thread, daemon=True)
            thread.start()
            thread.join()  # Wait for playback to complete
            
            # print("✓ Playback completed")
            
        except Exception as ex:
            # print(f"❌ TTS operation failed: {ex}")
            raise
        finally:
            # Clean up temporary file only if we created it
            if temp_file_created and output_file:
                # Small delay to ensure audio playback has fully released the file
                await asyncio.sleep(0.1)
                self._safe_file_removal(output_file)
    
    def speak(self, text: str, output_file: Optional[str] = None):
        """
        Synchronous wrapper for speak_async.
        This provides a simple interface for non-async code.
        
        Args:
            text: Text to convert to speech
            output_file: Optional custom output file path
        """
        # Run the async function in a new event loop
        asyncio.run(self.speak_async(text, output_file))
    
    def cleanup(self):
        """
        Clean up pygame resources when done.
        Call this when you're finished using the TTS system.
        """
        if self.pygame_initialized:
            pygame.mixer.quit()
            self.pygame_initialized = False
            # print("✓ TTS system cleaned up")

def speak(text: str, output_file: Optional[str] = None):
    """
    Simple function interface for text-to-speech.
    Creates a TTS manager, speaks the text, and cleans up.
    
    Args:
        text: Text to convert to speech
        output_file: Optional custom output file path
    """
    tts = TTSManager()
    try:
        tts.speak(text, output_file)
    finally:
        tts.cleanup()

# # Example usage and testing
# if __name__ == "__main__":
#     # Test the improved system
#     print("🎵 Testing improved TTS system...")
    
#     # Test basic functionality
#     speak("Welcome to the improved Alfred world. This system is more robust and efficient.")
    
#     # Test with custom file (optional)
#     # speak("This is a test with a custom file.", "custom_speech.mp3")
    
#     print("✅ TTS testing completed!")