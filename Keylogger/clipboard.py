# clipboard.py
import os
import threading
import time
import logging
try:
    import pyperclip
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip"])
    import pyperclip

class ClipboardMonitor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.last_clipboard = ""
        self.running = False
        self.thread = None

    def monitor_clipboard(self):
        """Continuously monitor clipboard changes."""
        while self.running:
            try:
                current_clipboard = pyperclip.paste()
                if current_clipboard and current_clipboard != self.last_clipboard:
                    self.last_clipboard = current_clipboard
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    with open(os.path.join(self.file_path, "f_clipboard.txt"), "a") as f:
                        f.write(f"[{timestamp}] {current_clipboard}\n")
                    logging.info(f"Clipboard captured: {current_clipboard[:50]}...")
                time.sleep(1)  # Poll every second
            except Exception as e:
                logging.error(f"Clipboard monitor error: {e}")

    def start(self):
        """Start the clipboard monitor in a thread."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
            self.thread.start()
            logging.info("Clipboard monitor started.")

    def stop(self):
        """Stop the clipboard monitor."""
        self.running = False
        if self.thread:
            self.thread.join()
            logging.info("Clipboard monitor stopped.")

def copy_clipboard(file_path):
    """Entry point for main.py to start clipboard monitoring."""
    monitor = ClipboardMonitor(file_path)
    monitor.start()
    return monitor  # Return monitor object to allow stopping later if needed