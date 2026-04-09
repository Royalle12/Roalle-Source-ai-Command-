import asyncio
import edge_tts
import os
import requests
from config import ELEVENLABS_API_KEY, VOICE_ID, ASSETS_DIR

class VoiceEngine:
    def __init__(self):
        self.elevenlabs_api_key = ELEVENLABS_API_KEY
        self.voice_id = VOICE_ID

    async def generate_audio_edge(self, text, save_path, voice="en-US-EmmaMultilingualNeural"):
        """
        Generates high-quality free voiceover using Microsoft Edge TTS.
        """
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(save_path)
        return save_path

    def generate_audio_elevenlabs(self, text, save_path):
        """
        Generates voiceover using ElevenLabs (Cloned Voice).
        """
        if self.elevenlabs_api_key == "YOUR_ELEVENLABS_API_KEY":
            print("Warning: ELEVENLABS_API_KEY not set. Falling back to Edge-TTS.")
            return None

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.elevenlabs_api_key
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(response.content)
            return save_path
        except Exception as e:
            print(f"Error generating ElevenLabs audio: {e}")
            return None

    def generate_narration(self, text, filename, use_cloned=True):
        """
        Main method to generate narration.
        """
        save_path = os.path.join(ASSETS_DIR, f"{filename}.mp3")
        
        if use_cloned and self.elevenlabs_api_key != "YOUR_ELEVENLABS_API_KEY":
            path = self.generate_audio_elevenlabs(text, save_path)
            if path: return path
            
        # Fallback to Edge-TTS
        asyncio.run(self.generate_audio_edge(text, save_path))
        return save_path

if __name__ == "__main__":
    # Test narration
    engine = VoiceEngine()
    print("Testing Edge-TTS Narration...")
    path = engine.generate_narration("Welcome to Royalle Source. This is your daily wellness tip.", "test_voice")
    if path:
        print(f"Success! Narration saved to: {path}")
