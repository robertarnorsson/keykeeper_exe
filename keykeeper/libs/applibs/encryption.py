import base64
import os
import uuid
from cryptography.exceptions import InvalidTag
from cryptography.fernet import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

class Security():
    def __init__(self, lvl: int):
        self.ITERATION_COUNT = 100000
        lvl = int(lvl)
        if lvl <= 1:
            self.ITERATION_COUNT = 100000
        else:
            self.ITERATION_COUNT = lvl * 100000

    def encrypt(self, plaintext: str, password: str):
        """Encrypts a string using a password"""

        plaintext = plaintext.encode()
        password = password.encode()

        salt = os.urandom(32)  # Use a secure random salt

        # Generate a 256-bit key using PBKDF2HMAC
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA384(),
            salt=salt,
            iterations=self.ITERATION_COUNT,  # Use a larger iteration count for increased security
            length=32,
            backend=default_backend()
        )
        key = kdf.derive(password)

        # Generate a random 16-byte nonce
        nonce = os.urandom(32) + uuid.uuid4().bytes + uuid.uuid4().bytes
        
        # Use AES-GCM for authenticated encryption
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        # Serialize the nonce and tag with the ciphertext
        ciphertext_with_nonce_tag = encryptor.tag + ciphertext

        return base64.urlsafe_b64encode(salt + nonce + ciphertext_with_nonce_tag).decode()

    def decrypt(self, ciphertext, password):
        """Decrypts a string using a password and salt."""

        password = password.encode()

        # Decode the base64-encoded ciphertext
        ciphertext = base64.urlsafe_b64decode(ciphertext)

        # Extract the salt, nonce, and tag
        salt = ciphertext[:32]
        nonce = ciphertext[32:96]
        tag = ciphertext[96:112]
        ciphertext = ciphertext[112:]  # Fix: Extract the ciphertext after tag

        # Generate the same 256-bit key using PBKDF2HMAC
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA384(),
            salt=salt,
            iterations=self.ITERATION_COUNT,  # Use the same iteration count as during encryption
            length=32,
            backend=default_backend()
        )
        key = kdf.derive(password)

        # Use AES-GCM for authenticated decryption
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag))
        decryptor = cipher.decryptor()

        try:
            # Decrypt the ciphertext
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            return plaintext.decode()
        except InvalidTag:
            # Handle invalid tag exception (e.g., tampered ciphertext)
            #print("Error: Invalid tag. The ciphertext may have been tampered with.")
            return None

"""
cipher = Security(2)
pw = "Pas$W0rI)"

# Encrypt a string
ciphertextwis = cipher.encrypt('hello world', pw)
print(ciphertextwis)

# Decrypt the ciphertext
plaintext = cipher.decrypt(ciphertextwis, pw)
print(plaintext)
"""