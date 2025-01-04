import string
from itertools import cycle


def columnar_transpose_decrypt(encrypted_text: str, key: str) -> str:
    """
    Decrypts text encrypted by the columnar transposition cipher.

    Args:
        encrypted_text (str): The columnar transposition cipher encrypted text.
        key (str): The key used for the columnar transposition cipher.

    Returns:
        str: The decrypted text.
    """
    num_columns = len(key)
    num_rows = len(encrypted_text) // num_columns
    key_order = sorted(range(len(key)), key=lambda k: key[k])

    # Reconstruct columns based on key order
    columns = [""] * num_columns
    index = 0
    for i in key_order:
        columns[i] = encrypted_text[index : index + num_rows]
        index += num_rows

    # Read out the columns in original row order
    decrypted_text = "".join(
        columns[i % num_columns][i // num_columns]
        for i in range(num_rows * num_columns)
    )
    return decrypted_text.strip()


def vigenere_cipher_decrypt(text: str, key: str) -> str:
    """
    Decrypts text encrypted by the Vigenère cipher.

    Args:
        text (str): The Vigenère cipher encrypted text.
        key (str): The key used for the Vigenère cipher.

    Returns:
        str: The decrypted text.
    """
    decrypted_text = []
    for char, key_char in zip(text, cycle(key)):
        if char.isalpha():
            shift = ord(key_char.lower()) - ord("a")
            decrypted_char = chr(((ord(char) - ord("a") - shift + 26) % 26) + ord("a"))
            decrypted_text.append(decrypted_char)
        else:
            decrypted_text.append(char)
    return "".join(decrypted_text)


def substitution_cipher_decrypt(text: str) -> str:
    """
    Decrypts text encrypted by the substitution cipher.

    Args:
        text (str): The substitution cipher encrypted text.

    Returns:
        str: The decrypted text.
    """
    alphabet = list(string.ascii_lowercase)
    shuffled_key = sorted(set(key), key=key.index)
    remaining_chars = [char for char in alphabet if char not in shuffled_key]
    substitution_order = shuffled_key + remaining_chars
    substitution_alphabet = dict(zip(alphabet, substitution_order))

    inverse_substitution = {v: k for k, v in substitution_alphabet.items()}
    return "".join(inverse_substitution.get(char, char) for char in text)


def decrypt(encrypted_text: str, key: str) -> str:
    """
    Reverses three levels of encryption: substitution cipher, Vigenère cipher, and columnar transposition cipher.

    Args:
        encrypted_text (str): The fully encrypted text.
        key (str): Key that is used to decrypt the encrypted file
    Returns:
        str: The original plaintext.
    """
    # Level 3: Reverse Substitution Cipher
    level_3_decryption = substitution_cipher_decrypt(encrypted_text)
    # Level 2: Reverse Vigenère Cipher
    level_2_decryption = vigenere_cipher_decrypt(level_3_decryption, key)
    # Level 1: Reverse Columnar Transposition Cipher
    return columnar_transpose_decrypt(level_2_decryption, key)


if __name__ == "__main__":
    key = "enigma"  # Guess the key
    key = key.lower()

    # taking the encrypted.txt file location as input
    file_location = input("Enter the encrypted.txt file location: ") or "encrypted.txt"
    try:
        with open(file_location, "r") as file:
            encypted_txt = file.read()
    except FileNotFoundError:
        print(f"encrypted.txt file not found in the location: '{file_location}'")
        exit(1)

    # Decrypt and print the text
    decrypted_text = decrypt(encypted_txt, key)
    print()
    print("Decrypted:", decrypted_text)
