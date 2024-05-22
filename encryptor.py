import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.backends import default_backend
from decouple import config
import base64
import os

class AESCipher:
    """
    A class used to encrypt and decrypt data using AES encryption.

    Attributes
    ----------
    key : str
        The secret key to use in the symmetric cipher.

    Methods
    -------
    encrypt(data: str) -> str
        Encrypts the provided data using AES encryption.
    decrypt(encrypted_data: str) -> str
        Decrypts the provided data using AES encryption.
    save_to_json(encrypted_string: str, filename: str) -> None
        Saves the encrypted string to a JSON file.
    """

    def __init__(self, key: str):
        """
        Constructs all the necessary attributes for the AESCipher object.

        Parameters
        ----------
        key : str
            The secret key to use in the symmetric cipher.
        """
        self.key = key

    def encrypt(self, data: str) -> str:
        """
        Encrypts the provided data using AES encryption.

        Parameters
        ----------
        data : str
            The data to encrypt.

        Returns
        -------
        str
            The encrypted data, as a base64-encoded string.
        """
        backend = default_backend()
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=1000000,  # Increased iterations
            backend=backend
        )
        key = (kdf.derive(self.key.encode()))
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=backend)
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data.encode()) + padder.finalize()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return base64.urlsafe_b64encode(salt + iv + encryptor.tag + encrypted_data).decode()  # Include the tag

    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypts the provided data using AES encryption.

        Parameters
        ----------
        encrypted_data : str
            The data to decrypt, as a base64-encoded string.

        Returns
        -------
        str
            The decrypted data.
        """
        encrypted_data = base64.urlsafe_b64decode(encrypted_data.encode())
        salt = encrypted_data[:16]
        iv = encrypted_data[16:32]
        tag = encrypted_data[32:48]  # Extract the tag
        ciphertext = encrypted_data[48:]
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=1000000,  # Increased iterations
            backend=default_backend()
        )
        key = (kdf.derive(self.key.encode()))
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())  # Using GCM mode
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = unpadder.update(decryptor.update(ciphertext) + decryptor.finalize()) + unpadder.finalize()
        return decrypted_data.decode()

    def save_to_json(self, encrypted_string: str, filepath: str) -> None:
        """
        Saves the encrypted string to a JSON file.

        Parameters
        ----------
        encrypted_string : str
            The encrypted string to save.
        filepath : str
            The path of the JSON file to save to.
        """
        with open(filepath, 'w') as f:
            json.dump({'encrypted_string': encrypted_string}, f)
        print("Data encrypted and saved to your config file")



    
