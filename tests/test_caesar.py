"""
tests/test_caesar.py
--------------------
pytest test suite for core/caesar.py

Run with:
    pytest tests/test_caesar.py -v
"""

import pytest
from core.caesar import encrypt, decrypt, brute_force


# ── Encryption ────────────────────────────────────────────────────────────────

class TestCaesarEncrypt:

    def test_basic_uppercase(self):
        """Classic textbook example: HELLO shifted by 3 → KHOOR."""
        assert encrypt("HELLO", 3) == "KHOOR"

    def test_basic_lowercase(self):
        """Lowercase input should produce lowercase output."""
        assert encrypt("hello", 3) == "khoor"

    def test_preserves_mixed_case(self):
        """Each letter's case must be preserved independently."""
        assert encrypt("Hello", 3) == "Khoor"

    def test_wrap_around_end_of_alphabet(self):
        """X, Y, Z should wrap around to A, B, C with shift 3."""
        assert encrypt("XYZ", 3) == "ABC"

    def test_wrap_around_lowercase(self):
        assert encrypt("xyz", 3) == "abc"

    def test_non_alpha_characters_preserved(self):
        """Spaces, punctuation, and digits must not be altered."""
        assert encrypt("Hello, World! 123", 3) == "Khoor, Zruog! 123"

    def test_shift_zero_returns_unchanged(self):
        """Shift 0 is a no-op — output equals input."""
        assert encrypt("HELLO", 0) == "HELLO"

    def test_shift_26_equals_shift_zero(self):
        """A full rotation of 26 is the same as no shift."""
        assert encrypt("HELLO", 26) == "HELLO"

    def test_shift_modulo_normalisation(self):
        """Shifts beyond 25 are silently reduced mod 26."""
        assert encrypt("HELLO", 29) == encrypt("HELLO", 3)

    def test_single_character(self):
        assert encrypt("A", 1) == "B"
        assert encrypt("Z", 1) == "A"

    def test_empty_string(self):
        """Empty input must return empty output without error."""
        assert encrypt("", 5) == ""

    def test_only_non_alpha(self):
        """Input with no letters returns identical output."""
        assert encrypt("123 !@#", 7) == "123 !@#"


# ── Decryption ────────────────────────────────────────────────────────────────

class TestCaesarDecrypt:

    def test_basic_uppercase(self):
        assert decrypt("KHOOR", 3) == "HELLO"

    def test_basic_lowercase(self):
        assert decrypt("khoor", 3) == "hello"

    def test_wrap_around(self):
        """A, B, C decrypted with shift 3 → X, Y, Z."""
        assert decrypt("ABC", 3) == "XYZ"

    def test_non_alpha_preserved(self):
        assert decrypt("Khoor, Zruog! 123", 3) == "Hello, World! 123"

    def test_roundtrip_all_shifts(self):
        """Encrypting then decrypting must recover the original for all valid shifts."""
        original = "The Quick Brown Fox Jumps Over The Lazy Dog!"
        for shift in range(0, 26):
            assert decrypt(encrypt(original, shift), shift) == original

    def test_shift_zero_returns_unchanged(self):
        assert decrypt("HELLO", 0) == "HELLO"

    def test_empty_string(self):
        assert decrypt("", 3) == ""


# ── Brute Force ───────────────────────────────────────────────────────────────

class TestBruteForce:

    def test_returns_exactly_25_results(self):
        """There are exactly 25 non-trivial Caesar keys (1–25)."""
        results = brute_force("KHOOR")
        assert len(results) == 25

    def test_shift_values_are_1_to_25(self):
        """The shift values in the output must be 1, 2, ..., 25 in order."""
        results = brute_force("KHOOR")
        assert [r[0] for r in results] == list(range(1, 26))

    def test_correct_decryption_present_in_results(self):
        """The correct plaintext must appear somewhere in the results."""
        results = brute_force("KHOOR")
        plaintexts = [r[1] for r in results]
        assert "HELLO" in plaintexts

    def test_correct_shift_paired_with_correct_plaintext(self):
        """Shift 3 must decrypt 'KHOOR' to 'HELLO'."""
        results = brute_force("KHOOR")
        result_dict = dict(results)
        assert result_dict[3] == "HELLO"

    def test_with_sentence(self):
        """Brute force must work on a full sentence with spaces."""
        ciphertext = encrypt("Hello, World!", 13)
        results = brute_force(ciphertext)
        result_dict = dict(results)
        assert result_dict[13] == "Hello, World!"

    def test_empty_input(self):
        """Brute force on empty string should return 25 empty strings."""
        results = brute_force("")
        assert all(r[1] == "" for r in results)
