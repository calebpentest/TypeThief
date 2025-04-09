import platform
import os
import logging

def computer_information(file_path):
    """
    Gathers system information and saves it to a file.

    :param file_path: The path to the directory where the system information will be saved.
    """
    sysinfo_file = os.path.join(file_path, "f_sysinfo.txt")
    with open(sysinfo_file, "w") as f:
        f.write(f"System: {platform.system()}\n")
        f.write(f"Node Name: {platform.node()}\n")
        f.write(f"Release: {platform.release()}\n")
        f.write(f"Version: {platform.version()}\n")
        f.write(f"Machine: {platform.machine()}\n")
        f.write(f"Processor: {platform.processor()}\n")
    logging.info("System information saved.")