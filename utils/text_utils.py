"""
utils/text_utils.py
-------------------
Shared helper functions used across the project.
Handles input validation, text cleaning, and file I/O.

No cipher logic lives here — this module is purely utility.
"""

import os


# ── Validation ────────────────────────────────────────────────────────────────

def validate_shift(shift: int) -> int:
    """
    Normalise a Caesar shift to the range [0, 25].

    A shift of 26 is identical to 0 (full rotation), so we use mod 26.

    Args:
        shift: Any integer shift value.

    Returns:
        The equivalent shift in [0, 25].
    """
    return shift % 26


def validate_keyword(keyword: str) -> bool:
    """
    Return True if the keyword is non-empty and contains only letters.

    Vigenère keywords must be purely alphabetic — digits and symbols
    have no defined shift value in the 26-letter alphabet.

    Args:
        keyword: The candidate keyword string.

    Returns:
        True if valid, False otherwise.
    """
    return bool(keyword) and all(c.isalpha() for c in keyword)


# ── Text cleaning ─────────────────────────────────────────────────────────────

def clean_for_display(text: str) -> str:
    """
    Strip leading/trailing whitespace for clean UI display.

    Args:
        text: Raw input string.

    Returns:
        Stripped string.
    """
    return text.strip()


# ── File I/O ──────────────────────────────────────────────────────────────────

def read_from_file(filepath: str) -> str:
    """
    Read and return the full contents of a .txt file.

    Args:
        filepath: Absolute or relative path to a .txt file.

    Returns:
        File content as a string.

    Raises:
        ValueError: If the file is not a .txt file.
        FileNotFoundError: If the file does not exist.
    """
    if not filepath.lower().endswith(".txt"):
        raise ValueError(f"Only .txt files are supported. Got: '{filepath}'")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: '{filepath}'")

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def write_to_file(filepath: str, content: str) -> None:
    """
    Write a string to a .txt file, creating the file if it does not exist.

    Args:
        filepath: Destination path. Must end in .txt.
        content:  String content to write.

    Raises:
        ValueError: If the destination is not a .txt file.
    """
    if not filepath.lower().endswith(".txt"):
        raise ValueError(f"Output file must be a .txt file. Got: '{filepath}'")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
