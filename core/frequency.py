"""
core/frequency.py
-----------------
Letter frequency analysis for cryptanalysis of Caesar ciphers.

KEY IDEA
--------
English text follows a well-known statistical distribution — 'E' appears
~12.7% of the time, 'T' ~9.1%, etc. Because Caesar is a monoalphabetic
cipher (every 'E' always maps to the same ciphertext letter), this
distribution is preserved in the ciphertext — just shifted.

By measuring which shift makes the ciphertext distribution most closely
match standard English, we can recover the key WITHOUT trying all 25 shifts.

The metric used is chi-squared distance:

    χ² = Σ (observed_freq - expected_freq)² / expected_freq

A lower chi-squared score means the distribution is more English-like.

Public API
----------
    ENGLISH_FREQ          — dict[str, float]: reference letter frequencies
    get_frequency(text)   — dict[str, float]: letter frequencies in text
    score_text(text)      — float: chi-squared distance from English
    recover_caesar_key(ciphertext) -> int: best-guess Caesar shift
"""

from collections import Counter

# ── English reference frequencies (%) ────────────────────────────────────────
# Source: Relative frequencies of letters in the English language
# (Lewand, 2000 — standard cryptography reference values)
ENGLISH_FREQ: dict[str, float] = {
    "A": 8.17, "B": 1.49, "C": 2.78, "D": 4.25, "E": 12.70,
    "F": 2.23, "G": 2.02, "H": 6.09, "I": 6.97, "J": 0.15,
    "K": 0.77, "L": 4.03, "M": 2.41, "N": 6.75, "O": 7.51,
    "P": 1.93, "Q": 0.10, "R": 5.99, "S": 6.33, "T": 9.06,
    "U": 2.76, "V": 0.98, "W": 2.36, "X": 0.15, "Y": 1.97,
    "Z": 0.07,
}


# ── Public functions ──────────────────────────────────────────────────────────

def get_frequency(text: str) -> dict[str, float]:
    """
    Compute the letter frequency distribution of a text (as percentages).

    Non-alphabetic characters are ignored. All letters are counted
    case-insensitively (mapped to uppercase keys).

    If the text contains no alphabetic characters, all frequencies are 0.0.

    Args:
        text: Any string (ciphertext or plaintext).

    Returns:
        A dict mapping each uppercase letter A–Z to its frequency (%).
        All 26 letters are always present as keys.

    Example:
        >>> freq = get_frequency("HELLO")
        >>> freq["L"]
        40.0
    """
    letters = [c.upper() for c in text if c.isalpha()]

    if not letters:
        return {letter: 0.0 for letter in ENGLISH_FREQ}

    counts = Counter(letters)
    total = len(letters)

    return {
        letter: round(counts.get(letter, 0) / total * 100, 2)
        for letter in ENGLISH_FREQ
    }


def score_text(text: str) -> float:
    """
    Score how English-like a text is using chi-squared distance.

    Lower score → closer to English → more likely to be the correct plaintext.
    This is the core metric used by brute-force ranking and key recovery.

    Args:
        text: The candidate plaintext string to evaluate.

    Returns:
        A non-negative float. 0.0 would be a perfect match to English
        frequencies (never achieved in practice).

    Note:
        Texts with no alphabetic content return a very high penalty score
        to avoid them being incorrectly ranked as "good" candidates.
    """
    letters = [c.upper() for c in text if c.isalpha()]

    # Penalise empty or near-empty texts heavily
    if len(letters) < 2:
        return float("inf")

    freq = get_frequency(text)

    # Chi-squared: measures deviation of observed from expected distribution
    chi_squared = sum(
        (freq.get(letter, 0.0) - ENGLISH_FREQ[letter]) ** 2 / ENGLISH_FREQ[letter]
        for letter in ENGLISH_FREQ
    )

    return chi_squared


def recover_caesar_key(ciphertext: str) -> int:
    """
    Recover the most likely Caesar shift using frequency analysis.

    For each of the 25 possible shifts, the function decrypts the ciphertext
    and scores the result against English letter frequencies using chi-squared.
    The shift that produces the most English-like output is returned.

    Args:
        ciphertext: A Caesar-encrypted string.

    Returns:
        The integer shift (1–25) most likely used to encrypt the text.

    Raises:
        ValueError: If the ciphertext contains no alphabetic characters
                    (frequency analysis requires letter content).

    Example:
        >>> recover_caesar_key("Khoor, Zruog!")
        3
    """
    from core.caesar import decrypt  # local import to avoid circular dependency

    letters = [c for c in ciphertext if c.isalpha()]
    if not letters:
        raise ValueError(
            "Frequency analysis requires at least some alphabetic characters in the ciphertext."
        )

    best_shift = 1
    best_score = float("inf")

    for shift in range(1, 26):
        candidate = decrypt(ciphertext, shift)
        s = score_text(candidate)
        if s < best_score:
            best_score = s
            best_shift = shift

    return best_shift
