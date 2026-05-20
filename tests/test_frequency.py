"""
tests/test_frequency.py
-----------------------
pytest test suite for core/frequency.py

Run with:
    pytest tests/test_frequency.py -v
"""

import pytest
from core.frequency import get_frequency, score_text, recover_caesar_key, ENGLISH_FREQ
from core.caesar import encrypt


# ── ENGLISH_FREQ sanity checks ────────────────────────────────────────────────

class TestEnglishFreqTable:

    def test_has_all_26_letters(self):
        assert set(ENGLISH_FREQ.keys()) == set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def test_frequencies_sum_to_100(self):
        total = sum(ENGLISH_FREQ.values())
        assert abs(total - 100.0) < 0.5  # allow minor rounding

    def test_e_is_most_frequent(self):
        assert ENGLISH_FREQ["E"] == max(ENGLISH_FREQ.values())

    def test_z_is_least_frequent(self):
        assert ENGLISH_FREQ["Z"] == min(ENGLISH_FREQ.values())


# ── get_frequency ─────────────────────────────────────────────────────────────

class TestGetFrequency:

    def test_returns_all_26_letters(self):
        freq = get_frequency("HELLO")
        assert set(freq.keys()) == set(ENGLISH_FREQ.keys())

    def test_frequencies_sum_to_100(self):
        freq = get_frequency("Hello, World!")
        total = sum(freq.values())
        assert abs(total - 100.0) < 0.5

    def test_correct_percentage_simple(self):
        # "AAAB": A appears 3/4 = 75%, B appears 1/4 = 25%
        freq = get_frequency("AAAB")
        assert freq["A"] == pytest.approx(75.0, abs=0.1)
        assert freq["B"] == pytest.approx(25.0, abs=0.1)

    def test_case_insensitive(self):
        """'hello' and 'HELLO' must produce identical frequency dicts."""
        assert get_frequency("hello") == get_frequency("HELLO")

    def test_non_alpha_ignored(self):
        """Punctuation, spaces, and digits must not affect letter frequencies."""
        freq_clean = get_frequency("HELLO")
        freq_messy = get_frequency("H E L L O ! 1 2 3")
        assert freq_clean == freq_messy

    def test_empty_string_returns_zeros(self):
        freq = get_frequency("")
        assert all(v == 0.0 for v in freq.values())

    def test_only_non_alpha_returns_zeros(self):
        freq = get_frequency("123 !@#$")
        assert all(v == 0.0 for v in freq.values())

    def test_single_letter(self):
        freq = get_frequency("E")
        assert freq["E"] == 100.0
        non_e = {k: v for k, v in freq.items() if k != "E"}
        assert all(v == 0.0 for v in non_e.values())


# ── score_text ────────────────────────────────────────────────────────────────

class TestScoreText:

    def test_english_text_scores_lower_than_ciphertext(self):
        """
        A known English sentence should score (chi-squared) lower than
        the same sentence encrypted with Caesar — because frequency
        analysis measures closeness to English distribution.
        """
        plaintext = "The quick brown fox jumps over the lazy dog"
        ciphertext = encrypt(plaintext, 7)
        assert score_text(plaintext) < score_text(ciphertext)

    def test_returns_float(self):
        assert isinstance(score_text("HELLO"), float)

    def test_score_is_non_negative(self):
        assert score_text("Any text here") >= 0.0

    def test_empty_text_returns_inf(self):
        assert score_text("") == float("inf")

    def test_single_char_returns_inf(self):
        assert score_text("A") == float("inf")

    def test_correct_shift_has_lowest_score(self):
        """
        Among all 25 decryptions, the correct one should have the
        lowest chi-squared score (i.e., be the most English-like).
        This is the core guarantee of frequency analysis.
        """
        plaintext = "The quick brown fox jumps over the lazy dog" * 3
        shift = 11
        ciphertext = encrypt(plaintext, shift)
        from core.caesar import decrypt
        scores = {s: score_text(decrypt(ciphertext, s)) for s in range(1, 26)}
        best = min(scores, key=scores.get)
        assert best == shift


# ── recover_caesar_key ────────────────────────────────────────────────────────

class TestRecoverCaesarKey:

    @pytest.mark.parametrize("shift", [1, 3, 7, 13, 17, 19, 23, 25])
    def test_recovers_known_shifts(self, shift):
        """
        Use a long, representative English text to ensure the frequency
        fingerprint is strong enough for reliable key recovery.
        """
        plaintext = (
            "The quick brown fox jumps over the lazy dog. "
            "Pack my box with five dozen liquor jugs. "
            "How vexingly quick daft zebras jump. "
        ) * 3  # repeat to strengthen the signal
        ciphertext = encrypt(plaintext, shift)
        assert recover_caesar_key(ciphertext) == shift

    def test_returns_integer(self):
        ciphertext = encrypt("Hello World", 5)
        assert isinstance(recover_caesar_key(ciphertext), int)

    def test_result_in_valid_range(self):
        ciphertext = encrypt("Some text here for analysis purposes", 9)
        key = recover_caesar_key(ciphertext)
        assert 1 <= key <= 25

    def test_empty_ciphertext_raises(self):
        with pytest.raises(ValueError):
            recover_caesar_key("")

    def test_no_letters_raises(self):
        with pytest.raises(ValueError):
            recover_caesar_key("123 !@#$%")
