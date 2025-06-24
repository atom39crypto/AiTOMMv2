from pathlib import Path
from groq import Groq
import requests
from pydub import AudioSegment
import os


def playai(prompt,file_path):
    client = Groq(api_key="enter_your_api_key_here")  # Replace with your actual PlayAI API key
    speech_file_path = f"{file_path}"
    response = client.audio.speech.create(
    model="playai-tts",
    voice="Calum-PlayAI",
    response_format="wav",
    input=prompt,
    speed=1.0,
  )
    response.write_to_file(speech_file_path)



import requests
import os
from pydub import AudioSegment

def XI_labs(prompt, file_path):
    API_KEY = 'enter_your_api_key_here'  # Replace with your own ElevenLabs API key
    VOICE_ID = 'onwK4e9ZLuTAKqWW03F9'  # "Brian" (British male voice)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }

    data = {
        "text": prompt,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        temp_mp3 = f"{file_path}.tmp.mp3"

        with open(temp_mp3, "wb") as f:
            f.write(response.content)

        try:
            # Convert MP3 to WAV using pydub (ffmpeg must be installed and in PATH)
            audio = AudioSegment.from_mp3(temp_mp3)
            audio.export(file_path, format="wav")
            print(f"Audio saved to: {file_path}")
        except Exception as e:
            print(f"Error converting MP3 to WAV: {e}")
        finally:
            if os.path.exists(temp_mp3):
                os.remove(temp_mp3)
    else:
        print("Error:", response.status_code, response.text)




def tts(prompt,file_path="speech.wav"):
    try:
        playai(prompt,file_path)
    except Exception as e:
        print(f"Error with PlayAI TTS: {e}")
        try:
            XI_labs(prompt,file_path)
        except Exception as e:
            print(f"Error with ElevenLabs TTS: {e}")
            
if __name__ == "__main__":
    tts("Perform a longJump **NOW** !!!!!!!!!!!!!!!!!!!")
      
      