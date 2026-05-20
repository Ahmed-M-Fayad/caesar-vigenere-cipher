"""
core/caesar.py
--------------
Caesar Cipher implementation.

The Caesar cipher shifts every alphabetic character in the plaintext
by a fixed number of positions in the alphabet (the 'key').

    Encryption: C = (P + key) mod 26
    Decryption: P = (C - key + 26) mod 26

Non-alphabetic characters (spaces, punctuation, digits) are passed
through unchanged. Letter case is preserved: uppercase stays uppercase,
lowercase stays lowercase.

Public API
----------
    encrypt(text, shift) -> str
    decrypt(text, shift) -> str
    brute_force(ciphertext) -> list[tuple[int, str]]
"""

_ALPHABET_SIZE = 26


# ── Internal helpers ──────────────────────────────────────────────────────────

def _shift_char(char: str, shift: int) -> str:
    """
    Shift a single character by `shift` positions.

    Only alphabetic characters are shifted. All others are returned as-is.
    Case is preserved: 'a' stays lowercase, 'A' stays uppercase.

    Args:
        char:  A single character.
        shift: Number of positions to shift (can be negative for decryption).

    Returns:
        The shifted character, or the original if non-alphabetic.
    """
    if char.isalpha():
        # Choose the correct ASCII base so case is preserved after shift
        base = ord("A") if char.isupper() else ord("a")
        return chr((ord(char) - base + shift) % _ALPHABET_SIZE + base)
    return char


# ── Public API ────────────────────────────────────────────────────────────────

def encrypt(text: str, shift: int) -> str:
    """
    Encrypt plaintext using Caesar cipher.

    Each alphabetic character is shifted forward by `shift` positions.
    Non-alphabetic characters and letter case are preserved.

    Args:
        text:  The plaintext to encrypt.
        shift: The shift key (any integer; reduced mod 26 internally).

    Returns:
        The encrypted ciphertext.

    Example:
        >>> encrypt("Hello, World!", 3)
        'Khoor, Zruog!'
    """
    shift = shift % _ALPHABET_SIZE
    return "".join(_shift_char(c, shift) for c in text)


def decrypt(text: str, shift: int) -> str:
    """
    Decrypt a Caesar-encrypted ciphertext.

    Decryption is simply encryption with the negative shift.

    Args:
        text:  The ciphertext to decrypt.
        shift: The shift key used during encryption.

    Returns:
        The recovered plaintext.

    Example:
        >>> decrypt("Khoor, Zruog!", 3)
        'Hello, World!'
    """
    # Decrypting with shift k == encrypting with shift (26 - k)
    return encrypt(text, -shift)


def brute_force(ciphertext: str) -> list[tuple[int, str]]:
    """
    Try all 25 possible Caesar shifts and return every decryption.

    Shift 0 is excluded (no change — not a real key).
    Results are returned in ascending shift order (1 → 25).
    The caller is responsible for identifying the correct plaintext
    (typically by using frequency scoring from core.frequency).

    Args:
        ciphertext: The Caesar-encrypted text to attack.

    Returns:
        A list of (shift, decrypted_text) tuples for shifts 1 through 25.

    Example:
        >>> results = brute_force("Khoor!")
        >>> results[2]   # shift=3 → "Hello!"
        (3, 'Hello!')
    """
    return [(shift, decrypt(ciphertext, shift)) for shift in range(1, _ALPHABET_SIZE)]
