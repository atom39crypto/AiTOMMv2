import pvporcupine
import pyaudio
import numpy as np
import keyboard
from Audio.STT import *

recognizer = sr.Recognizer()

def text_detection():
    prompt = input("whats on your mind ? ")
    return prompt



def hot_word_detection():
    print("<=- Hot Word Detection -=>")
    ACCESS_KEY = r"8FeipUjzyoEpneO9Ro05n8L0diIEs9/ZQwvnJ+WrS+vOzwUacbeRUw=="
    KEYWORD_FILE_1 = r"Audio/hey-Atom_en_windows_v3_0_0.ppn"
    KEYWORD_FILE_2 = r"Audio/Atom-Listen_en_windows_v3_0_0.ppn"

    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY,
        keyword_paths=[KEYWORD_FILE_1,KEYWORD_FILE_2]
    )

    def get_next_audio_frame():
        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=512)

        audio_data = stream.read(512)

        if audio_data is None:
            print("Error: Failed to capture audio frame.")
            return None

        audio_frame = np.frombuffer(audio_data, dtype=np.int16)
        return audio_frame

    try:
        while True:
            audio_frame = get_next_audio_frame()

            if audio_frame is None:
                continue

            keyword_index = porcupine.process(audio_frame)

            if keyword_index == 0:
                print("Keyword detected: 'hey Atom'")
                keyboard.press("esc")
                prompt = speech_to_text()
                return prompt
                
            elif keyword_index == 1:
                print("Keyword detected: 'Atom listen'")
                keyboard.press("esc")
                prompt = continuous_sst()
                return prompt
                
    except KeyboardInterrupt:
        print("Process interrupted")

    finally:
        porcupine.delete()



if __name__ == "__main__":
    hot_word_detection()
