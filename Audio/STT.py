import time
import threading
import speech_recognition as sr
from Frontend.background.STT_UI import create_wave_animation

def continuous_sst():
    """
    Listens for speech input while displaying an animated wave UI.
    """
    animation_thread = threading.Thread(target=create_wave_animation)
    animation_thread.start()

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=6)
                break  # Exit loop if speech is detected
            except sr.WaitTimeoutError:
                print("Listening timed out. No speech detected. Retrying...")

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except Exception:
        query = ""

    return query.lower()

def speech_to_text():
    """
    Continuously listens for speech input and processes recognized text.
    Stops when "ok reply" is spoken.
    """
    animation_thread = threading.Thread(target=create_wave_animation)
    animation_thread.start()
    recognizer = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.pause_threshold = 1
            recognizer.adjust_for_ambient_noise(source)

            while True:
                try:
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=6)
                    break  # Exit loop if speech is detected
                except sr.WaitTimeoutError:
                    print("Listening timed out. No speech detected. Retrying...")

            try:
                print("Recognizing...")
                query = recognizer.recognize_google(audio, language='en-in')
                print(f"User said: {query}")

                if query.lower() == "ok reply":
                    print("Exit command received. Stopping...")
                    break  # Stop the function

                time.sleep(2)
            except sr.UnknownValueError:
                print("Sorry, could not understand the audio.")
            except sr.RequestError:
                print("Could not request results, check internet connection.")
            except Exception as e:
                print(f"Error: {e}")

    return query.lower()

if __name__ == "__main__":
    print(continuous_sst())
