from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from base64 import b64encode, b64decode
import os

# AES Encryption/Decryption class
class AESCipher:
    def __init__(self, password: str):
        # Use PBKDF2HMAC to derive a secure key from the password
        salt = b'\x00' * 16  # In a real scenario, store and retrieve the salt securely
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        self.key = kdf.derive(password.encode())

    def encrypt(self, plaintext: str) -> str:
        # AES requires the data to be padded to a specific block size (128 bits)
        iv = os.urandom(16)  # Initialization vector for AES in CBC mode
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Pad the plaintext to a multiple of 128 bits
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()

        # Encrypt the padded plaintext
        encrypted = encryptor.update(padded_data) + encryptor.finalize()

        # Return the IV and the encrypted data (both encoded in base64)
        return b64encode(iv + encrypted).decode('utf-8')

    def decrypt(self, encrypted_text: str) -> str:
        # Decode the encrypted text from base64
        encrypted_data = b64decode(encrypted_text)

        # Split the IV and the encrypted data
        iv = encrypted_data[:16]
        encrypted_message = encrypted_data[16:]

        # Decrypt using AES with the same key and IV
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt the data and remove padding
        decrypted_padded = decryptor.update(encrypted_message) + decryptor.finalize()

        # Unpad the decrypted data
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()

        # Return the original plaintext
        return decrypted.decode('utf-8')

# Example Usage
if __name__ == "__main__":
    # Password for key derivation (this would be stored securely in a real app)
    password = "my_secure_password"

    # Initialize AES Cipher with password
    aes_cipher = AESCipher(password)

    # Example extracted text to encrypt
    extracted_text = "This is the text extracted from the document that needs to be encrypted."

    # Encrypt the extracted text
    encrypted_text = aes_cipher.encrypt(extracted_text)
    print("Encrypted Text:", encrypted_text)

    # Decrypt the encrypted text
    decrypted_text = aes_cipher.decrypt(encrypted_text)
    print("Decrypted Text:", decrypted_text)
