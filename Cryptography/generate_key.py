import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode
import logging

def generate_key(password: str, salt: bytes) -> bytes:
    """
    Generate a Fernet key using a password and salt.

    :param password: The password to derive the key from.
    :param salt: The salt to use for key derivation.
    :return: The generated Fernet key.
    """
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
        backend=default_backend()
    )
    key = urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def save_key(key: bytes, file_path: str):
    """
    Save the encryption key to a file.

    :param key: The encryption key to save.
    :param file_path: The path to the file where the key will be saved.
    """
    try:
        with open(file_path, 'wb') as file:
            file.write(key)
        logging.info(f"Key successfully saved to {file_path}")
    except Exception as e:
        logging.error(f"Error saving key: {e}")

def main():
    password = input("Enter a secure password: ")
    salt = os.urandom(16)  
    key = generate_key(password, salt)
    file_path = "encryption_key.txt"

    save_key(key, file_path)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()