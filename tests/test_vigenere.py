"""
tests/test_vigenere.py
----------------------
pytest test suite for core/vigenere.py

Run with:
    pytest tests/test_vigenere.py -v
"""

import pytest
from core.vigenere import encrypt, decrypt


# ── Encryption ────────────────────────────────────────────────────────────────

class TestVigenereEncrypt:

    def test_basic_example(self):
        """Manual worked example: ATTACK + KEY → KXRKGI."""
        assert encrypt("ATTACK", "KEY") == "KXRKGI"

    def test_keyword_cycles(self):
        """
        With keyword 'ABC' (shifts 0,1,2), encrypting 'AAAAAAA' should
        produce 'ABCABCA' — the keyword cycling is visible.
        """
        assert encrypt("AAAAAAA", "ABC") == "ABCABCA"

    def test_single_letter_keyword(self):
        """A single-letter keyword degenerates to a Caesar cipher."""
        from core.caesar import encrypt as caesar_encrypt
        assert encrypt("HELLO", "D") == caesar_encrypt("HELLO", 3)  # D = shift 3

    def test_preserves_spaces(self):
        """Spaces must pass through unchanged and must NOT advance keyword index."""
        result = encrypt("A A", "BC")
        # 'A' shifted by B(1) = 'B', space unchanged, 'A' shifted by C(2) = 'C'
        assert result == "B C"

    def test_preserves_punctuation(self):
        result = encrypt("HELLO, WORLD!", "KEY")
        assert result[5] == ","   # comma at index 5
        assert result[12] == "!"  # exclamation mark at index 12

    def test_case_insensitive_keyword(self):
        """Keyword case must not affect the output."""
        assert encrypt("HELLO", "key") == encrypt("HELLO", "KEY")
        assert encrypt("HELLO", "Key") == encrypt("HELLO", "KEY")

    def test_lowercase_plaintext_preserved(self):
        """Lowercase input letters must produce lowercase ciphertext letters."""
        result = encrypt("hello", "KEY")
        assert result == result.lower()

    def test_mixed_case_plaintext(self):
        """Each letter's case is preserved independently."""
        result = encrypt("Hello", "KEY")
        assert result[0].isupper()
        assert result[1:].islower() or all(c.islower() or not c.isalpha() for c in result[1:])

    def test_numbers_preserved(self):
        result = encrypt("abc123", "KEY")
        assert result[3:] == "123"

    def test_invalid_keyword_digits_raises(self):
        with pytest.raises(ValueError):
            encrypt("HELLO", "K3Y")

    def test_invalid_keyword_empty_raises(self):
        with pytest.raises(ValueError):
            encrypt("HELLO", "")

    def test_invalid_keyword_only_digits_raises(self):
        with pytest.raises(ValueError):
            encrypt("HELLO", "123")

    def test_empty_plaintext(self):
        assert encrypt("", "KEY") == ""


# ── Decryption ────────────────────────────────────────────────────────────────

class TestVigenereDecrypt:

    def test_basic_example(self):
        """Reverse of the encrypt test: KXRKGI + KEY → ATTACK."""
        assert decrypt("KXRKGI", "KEY") == "ATTACK"

    def test_roundtrip_simple(self):
        assert decrypt(encrypt("HELLO", "KEY"), "KEY") == "HELLO"

    def test_roundtrip_with_spaces_and_punctuation(self):
        original = "Hello, World! This is a test."
        assert decrypt(encrypt(original, "SECRET"), "SECRET") == original

    def test_roundtrip_all_keywords(self):
        """Round-trip test across multiple keywords and texts."""
        keywords = ["A", "Z", "KEY", "SECRET", "PYTHON", "VIGENERE"]
        texts = [
            "ATTACK AT DAWN",
            "The quick brown fox jumps over the lazy dog",
            "Hello, World! 123",
        ]
        for kw in keywords:
            for text in texts:
                assert decrypt(encrypt(text, kw), kw) == text, (
                    f"Round-trip failed for keyword='{kw}', text='{text}'"
                )

    def test_keyword_cycling_roundtrip(self):
        """Verify correctness over a text longer than the keyword."""
        original = "A" * 30
        kw = "XYZ"
        assert decrypt(encrypt(original, kw), kw) == original

    def test_invalid_keyword_raises(self):
        with pytest.raises(ValueError):
            decrypt("KXRKGI", "123")

    def test_empty_ciphertext(self):
        assert decrypt("", "KEY") == ""
