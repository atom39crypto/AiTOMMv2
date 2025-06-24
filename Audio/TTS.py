import pygame
from Audio.TTS_Converter import tts
import os
import time
import keyboard
from pathlib import Path

class TTS:
    def __init__(self, text, language="bn", max_words=20):
        self.text = text
        self.language = language
        self.max_words = max_words
        self.text_chunks = self.chunk_text(text)
        pygame.init()

    def chunk_text(self, text):
        """Break text into chunks after detecting । or ."""
        words = text.split()
        chunks = []
        chunk = []

        for word in words:
            chunk.append(word)
            if len(chunk) >= self.max_words and word.endswith(("।", ".")):
                chunks.append(" ".join(chunk))
                chunk = []

        if chunk:  
            chunks.append(" ".join(chunk))

        return chunks

    def play_chunk(self, text, index):
        """Convert text to speech, save, and play audio."""
        base_dir = Path(__file__).parent  # Directory of this script
        output_dir = base_dir / "output"
        output_dir.mkdir(parents=True, exist_ok=True)

        filename = output_dir / f"output_{index}.wav"

        tts(prompt=text, file_path=str(filename))  # Save audio using tts()

        print(f"Playing chunk {index + 1}/{len(self.text_chunks)}: {text}")
        pygame.mixer.music.load(str(filename))
        pygame.mixer.music.set_volume(0.5)  # Reduce volume to 50%
        pygame.mixer.music.play()
        self.update_ui(text)
        self.detect_key_press(index)

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def detect_key_press(self, current_chunk):
        print("Press 'esc' to exit, 'p' to pause, 'c' to continue, '>' for next chunk, '<' for previous chunk.")
        esc_pressed_time = None

        while pygame.mixer.music.get_busy():
            if keyboard.is_pressed('esc'):
                if esc_pressed_time is None:
                    esc_pressed_time = time.time()
                elif time.time() - esc_pressed_time >= 1:
                    if hasattr(self, 'ui_close_callback'):
                        self.ui_close_callback()
                    os._exit(0)  # Force exit
                    return
            else:
                esc_pressed_time = None

            if keyboard.is_pressed('p'):
                print("Pausing...")
                pygame.mixer.music.pause()
                while not keyboard.is_pressed('c'):
                    time.sleep(0.1)  
                print("Continuing...")
                pygame.mixer.music.unpause()

            if keyboard.is_pressed('>') and current_chunk + 1 < len(self.text_chunks):
                pygame.mixer.music.stop()
                self.play_chunk(self.text_chunks[current_chunk + 1], current_chunk + 1)
                break

            if keyboard.is_pressed('<') and current_chunk > 0:
                pygame.mixer.music.stop()
                self.play_chunk(self.text_chunks[current_chunk - 1], current_chunk - 1)
                break

    def play_all(self):
        try:
            for idx, chunk in enumerate(self.text_chunks):
                self.play_chunk(chunk, idx)
            print("Speaking Over")
            if hasattr(self, 'ui_close_callback'):
                self.ui_close_callback()
        except Exception as e:
            print(f"Error during playback: {e}")

    def update_ui(self, text):
        if hasattr(self, 'ui_callback'):
            self.ui_callback(text)
