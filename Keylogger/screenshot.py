# screenshot.py
import os
import threading
import time
import logging
from datetime import datetime
try:
    from mss import mss  # Cross-platform screenshot library
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mss"])
    from mss import mss

class ScreenshotCaptor:
    def __init__(self, file_path, interval=60):
        self.file_path = file_path
        self.interval = interval  # Seconds between screenshots
        self.running = False
        self.thread = None

    def capture(self):
        """Capture screenshots periodically using mss."""
        with mss() as sct:
            while self.running:
                try:
                    output_file = os.path.join(self.file_path, f"f_screenshot_{int(datetime.now().timestamp())}.png")
                    sct.shot(output=output_file, mon=-1)  # Capture all screens
                    logging.info(f"Screenshot captured: {output_file}")
                    time.sleep(self.interval)
                except Exception as e:
                    logging.error(f"Screenshot error: {e}")
                    time.sleep(5)  # Retry delay

    def start(self):
        """Start capturing in a thread."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.capture, daemon=True)
            self.thread.start()

    def stop(self):
        """Stop capturing."""
        self.running = False
        if self.thread:
            self.thread.join()

def capture_screenshot(file_path):
    """Entry point for main.py to start screenshot capture."""
    captor = ScreenshotCaptor(file_path, interval=60)  # Every 60s
    captor.start()
    return captor