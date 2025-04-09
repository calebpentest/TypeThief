# microphone.py
import os
import threading
import logging
try:
    import pyaudio
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyaudio"])
    import pyaudio
import wave
from datetime import datetime

class AudioRecorder:
    def __init__(self, file_path, duration=30):
        self.file_path = file_path
        self.duration = duration  # Recording duration in seconds
        self.recording = False
        self.thread = None

    def record(self):
        """Record audio in a thread."""
        try:
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 44100
            output_file = os.path.join(self.file_path, f"f_microphone_{int(datetime.now().timestamp())}.wav")

            audio = pyaudio.PyAudio()
            stream = audio.open(format=FORMAT, channels=CHANNELS,
                                rate=RATE, input=True,
                                frames_per_buffer=CHUNK)
            frames = []

            for _ in range(0, int(RATE / CHUNK * self.duration)):
                if not self.recording:
                    break
                data = stream.read(CHUNK)
                frames.append(data)

            stream.stop_stream()
            stream.close()
            audio.terminate()

            with wave.open(output_file, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(audio.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
            logging.info(f"Audio recorded: {output_file}")
        except Exception as e:
            logging.error(f"Audio recording error: {e}")

    def start(self):
        """Start recording in a background thread."""
        if not self.recording:
            self.recording = True
            self.thread = threading.Thread(target=self.record, daemon=True)
            self.thread.start()

    def stop(self):
        """Stop recording."""
        self.recording = False
        if self.thread:
            self.thread.join()

def record_microphone(file_path):
    """Entry point for main.py to start audio recording."""
    recorder = AudioRecorder(file_path, duration=30)  # 30-second clips
    recorder.start()
    return recorder