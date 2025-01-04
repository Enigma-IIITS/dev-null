"""
Module: cipher_chase

This module defines a class `CipherChase` representing a
challenge related to decrypting an encrypted.txt file based on the encryption.py file.
The class provides methods for generating
the question, validating the response, and providing the solution.
"""

import os
import string
import shutil
import hashlib
from pathlib import Path
from itertools import cycle
from config import SUBMISSION_LINK, FILE_LINK
from ....base_challenge import Challenge


class CipherChase(Challenge):
    """
    Represents a challenge question using custom encryption methods.
    The encryption consists of three layers:
    1. Columnar Transposition Cipher
    2. Vigenère Cipher
    3. Substitution Cipher

    This class handles the generation of encrypted files, decryption methods,
    and question creation for teams.
    """

    SCRIPT_PATH: Path = Path(__file__).resolve()
    ENCRYPTION_LOCATION: Path = SCRIPT_PATH.with_name("encryption.py")
    FILES_DIR_LOCATION: Path = SCRIPT_PATH.with_name("files")

    def __init__(self):
        # Define the encryption key and substitution alphabet
        self.key = "enigma"
        self.key = self.key.lower()
        self.substitution_alphabet = self.generate_substitution_alphabet(self.key)
        hints = [(100, "In the art of encryption, not every key is what it seems.")]
        super().__init__(points=500, penalty=50, hints=hints)

    async def generate_files(self, team_id: str) -> tuple[str, str]:
        """
        Retrieve or generate encoded and decoded strings for a team.

        Args:
            team_id (str): The ID of the team.

        Returns:
            tuple[str, str]: The encoded and decoded strings.
        """
        team = await self.db.get_team(team_id)
        zip_path = self.db.get_nested_value(team, "questions.CipherChase.location")
        flag_value = self.db.get_nested_value(team, "data_to_validate.CipherChase.flag")
        if zip_path and flag_value and os.path.exists(zip_path):
            return zip_path, flag_value

        # Generate a unique flag for the team
        message = team_id + "3nigm4_s3cRet_For_cilpher_chase"
        md5 = hashlib.md5()
        md5.update(message.encode())
        flag = "D3crypt!_C0mp13t3_" + md5.hexdigest()
        flag = flag.lower()

        # Create folder for storing files
        folder_path = self.FILES_DIR_LOCATION / f"CipherChase_{team_id}"
        os.makedirs(folder_path, exist_ok=True)
        shutil.copy(self.ENCRYPTION_LOCATION, folder_path)

        # Write the encrypted text to a file
        with open(folder_path / "encrypted.txt", "w") as file:
            plain_txt = (
                "WAh, you've found your way here—impressive.\n"
                "If you're truly here to seek the flag, "
                "then your efforts have earned you a reward.\n"
                f"Here is what you came for: ENIGMA{{{flag}}}\n\n"
                "Enigma is in capital letters, and the flag is enclosed in curly braces. "
            )
            data = self.encrypt(plain_txt)
            file.write(data)

        # Zip the folder
        zip_path = str(folder_path) + ".zip"
        self.zip_folder(folder_path, zip_path)

        # Save the paths and flag to the database
        self.db.teams.update_one(
            {"team_id": team_id},
            {
                "$set": {
                    "questions.CipherChase": {
                        "location": zip_path,
                    },
                    "data_to_validate.CipherChase": {
                        "flag": f"ENIGMA{{{flag}}}",
                    },
                }
            },
        )
        return zip_path, flag_value

    async def generate_question(self, team_id: str) -> dict:
        """
        Generate the full question text for the team.

        Args:
            team_id (str): The ID of the team.

        Returns:
            dict: The formatted question.
        """
        # Load the question template from a text file
        path = self.SCRIPT_PATH.with_name("question.txt")

        # Format the question description with placeholders replaced
        description = self.get_question_template(path).format(
            submission_url=SUBMISSION_LINK,
            challenge_id=self.challenge_id,
            file_url=f"{FILE_LINK}?team_id={team_id}&challenge_id={self.challenge_id}",
        )
        question_json = {"title": "Cipher Chase", "description": description}

        return self.generate_full_question(question_json)

    async def get_file_location(self, team_id: str) -> str:
        """
        Get the location of the generated Git repository for the team.

        Args:
            team_id (str): The ID of the team.

        Returns:
            str: The location of the generated repository.
        """
        repo_path, _ = await self.generate_files(team_id)
        return repo_path

    def generate_substitution_alphabet(self, key: str) -> dict:
        """
        Generates a substitution alphabet based on the key, rearranging the alphabet in a unique order.

        Args:
            key (str): The key used for the substitution cipher.

        Returns:
            dict: A dictionary mapping each letter to a substituted letter.
        """
        alphabet = list(string.ascii_lowercase)
        shuffled_key = sorted(set(key), key=key.index)
        remaining_chars = [char for char in alphabet if char not in shuffled_key]
        substitution_order = shuffled_key + remaining_chars
        return dict(zip(alphabet, substitution_order))

    def columnar_transpose_encrypt(self, text: str, key: str) -> str:
        """
        Encrypts text using a columnar transposition cipher (Level 1 encryption).

        Args:
            text (str): The plaintext to be encrypted.
            key (str): The key used for the columnar transposition cipher.

        Returns:
            str: The columnar transposition encrypted text.
        """
        num_columns = len(key)
        text_padded = text.ljust(
            (len(text) + num_columns - 1) // num_columns * num_columns
        )
        columns = ["" for _ in range(num_columns)]

        for i, char in enumerate(text_padded):
            columns[i % num_columns] += char

        key_order = sorted(range(len(key)), key=lambda k: key[k])
        encrypted_text = "".join(columns[i] for i in key_order)
        return encrypted_text

    def vigenere_cipher_encrypt(self, text: str, key: str) -> str:
        """
        Encrypts text using a Vigenère cipher (Level 2 encryption).

        Args:
            text (str): The plaintext to be encrypted.
            key (str): The key used for the Vigenère cipher.

        Returns:
            str: The Vigenère cipher encrypted text.
        """
        encrypted_text = []
        for char, key_char in zip(text, cycle(key)):
            if char.isalpha():
                shift = ord(key_char.lower()) - ord("a")
                encrypted_char = chr(
                    ((ord(char.lower()) - ord("a") + shift) % 26) + ord("a")
                )
                encrypted_text.append(encrypted_char)
            else:
                encrypted_text.append(char)
        return "".join(encrypted_text)

    def substitution_cipher_encrypt(self, text: str) -> str:
        """
        Encrypts text using a substitution cipher (Level 3 encryption).

        Args:
            text (str): The Vigenère cipher encrypted text.

        Returns:
            str: The substitution cipher encrypted text.
        """
        return "".join(self.substitution_alphabet.get(char, char) for char in text)

    def encrypt(self, text: str) -> str:
        """
        Applies three levels of encryption: columnar transposition cipher, Vigenère cipher, and substitution cipher.

        Args:
            text (str): The plaintext to encrypt.

        Returns:
            str: The fully encrypted text.
        """
        # Level 1: Columnar Transposition Cipher
        level_1_encryption = self.columnar_transpose_encrypt(text.lower(), self.key)
        # Level 2: Vigenère Cipher
        level_2_encryption = self.vigenere_cipher_encrypt(level_1_encryption, self.key)
        # Level 3: Substitution Cipher
        return self.substitution_cipher_encrypt(level_2_encryption)
