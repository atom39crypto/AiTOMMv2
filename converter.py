import os
from groq import Groq

def transcribe_audio(audio_filename):
    # Initialize Groq client with API key
    client = Groq(api_key="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")

    # Get the absolute path of the received audio file (.m4a)
    filename = os.path.join(os.path.dirname(__file__), audio_filename)

    # Open the file in binary mode
    with open(filename, "rb") as file:
        # Send the audio file for transcription with explicit language set to English
        transcription = client.audio.transcriptions.create(
            file=file,  # just the file object
            model="whisper-large-v3",  # specify the model
            response_format="verbose_json",  # specify response format
            language="en"  # Force language to English
        )

    # Return the transcription text
    return transcription.text
