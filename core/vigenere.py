"""
core/vigenere.py
----------------
Vigenère Cipher implementation.

The Vigenère cipher is a polyalphabetic substitution cipher. Instead of
using a single fixed shift (Caesar), it uses a keyword where each letter
of the keyword defines the shift for the corresponding plaintext letter.

The keyword cycles — for a keyword of length k, letter i of the plaintext
is shifted by keyword[i mod k].

    Encryption: C_i = (P_i + K_i) mod 26
    Decryption: P_i = (C_i - K_i + 26) mod 26

Where K_i is the numeric value (0–25) of the i-th keyword letter.

Non-alphabetic characters are passed through unchanged (they do NOT
advance the keyword index). Letter case is preserved.

Public API
----------
    encrypt(text, keyword) -> str
    decrypt(text, keyword) -> str
"""

_ALPHABET_SIZE = 26


# ── Internal helpers ──────────────────────────────────────────────────────────

def _keyword_shifts(keyword: str) -> list[int]:
    """
    Convert a keyword string into a list of integer shift values.

    Only alphabetic characters in the keyword are used. Each letter is
    mapped to its 0-based alphabet position (A/a=0, B/b=1, ..., Z/z=25).

    Args:
        keyword: The encryption keyword (letters only).

    Returns:
        A list of integer shifts, one per keyword letter.

    Raises:
        ValueError: If the keyword contains no alphabetic characters.
    """
    if not keyword:
        raise ValueError("Keyword must not be empty.")

    non_alpha = [c for c in keyword if not c.isalpha()]
    if non_alpha:
        raise ValueError(
            f"Keyword must contain letters only. "
            f"Invalid characters found: {non_alpha}"
        )

    return [ord(c.upper()) - ord("A") for c in keyword]


def _process(text: str, shifts: list[int], mode: str) -> str:
    """
    Core encrypt/decrypt loop shared by both public functions.

    Iterates over every character in `text`. Alphabetic characters are
    shifted according to the cycling keyword; all others pass through
    unchanged. The keyword index only advances on alphabetic characters
    so that non-letter characters (spaces, punctuation) do not disturb
    the keyword alignment.

    Args:
        text:   Input string (plaintext or ciphertext).
        shifts: Pre-computed list of keyword shift values.
        mode:   'encrypt' for forward shift, 'decrypt' for reverse shift.

    Returns:
        Processed string with the same length as `text`.
    """
    result = []
    key_idx = 0  # Tracks position in the cycling keyword

    for char in text:
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            k = shifts[key_idx % len(shifts)]

            if mode == "encrypt":
                shifted = (ord(char) - base + k) % _ALPHABET_SIZE
            else:
                shifted = (ord(char) - base - k) % _ALPHABET_SIZE

            result.append(chr(shifted + base))
            key_idx += 1  # Only advance keyword index for alphabetic chars
        else:
            result.append(char)

    return "".join(result)


# ── Public API ────────────────────────────────────────────────────────────────

def encrypt(text: str, keyword: str) -> str:
    """
    Encrypt plaintext using the Vigenère cipher.

    Args:
        text:    The plaintext to encrypt.
        keyword: The encryption keyword (letters only).

    Returns:
        The encrypted ciphertext.

    Raises:
        ValueError: If the keyword contains no alphabetic characters.

    Example:
        >>> encrypt("ATTACK", "KEY")
        'KXRKGI'
    """
    shifts = _keyword_shifts(keyword)
    return _process(text, shifts, mode="encrypt")


def decrypt(text: str, keyword: str) -> str:
    """
    Decrypt a Vigenère-encrypted ciphertext.

    Args:
        text:    The ciphertext to decrypt.
        keyword: The keyword used during encryption.

    Returns:
        The recovered plaintext.

    Raises:
        ValueError: If the keyword contains no alphabetic characters.

    Example:
        >>> decrypt("KXRKGI", "KEY")
        'ATTACK'
    """
    shifts = _keyword_shifts(keyword)
    return _process(text, shifts, mode="decrypt")
