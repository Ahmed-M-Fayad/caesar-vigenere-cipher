# Caesar & Vigenère Cipher

A Python implementation of two classical encryption algorithms — Caesar Cipher and Vigenère Cipher — with cryptanalysis techniques including Brute Force attacks and Frequency Analysis, wrapped in an interactive Streamlit dashboard.

> Security Course (College Project) — Classical Encryption

---

## Features

- **Caesar Cipher** — encrypt & decrypt with a user-specified shift
- **Vigenère Cipher** — encrypt & decrypt with a user-specified keyword
- **Brute Force Attack** — exhaustive Caesar key search across all 25 shifts
- **Frequency Analysis** — statistical Caesar key recovery using English letter frequencies
- **File I/O** — read plaintext from `.txt`, export ciphertext to `.txt`
- **Streamlit Dashboard** — interactive UI with visualizations for all features

---

## Project Structure

```
caesar-vigenere-cipher/
│
├── core/
│   ├── __init__.py
│   ├── caesar.py           # Caesar encrypt, decrypt, brute force
│   ├── vigenere.py         # Vigenère encrypt, decrypt
│   └── frequency.py        # Frequency analysis & key recovery
│
├── utils/
│   ├── __init__.py
│   └── text_utils.py       # Input validation, file I/O, text cleaning
│
├── tests/
│   ├── __init__.py
│   ├── test_caesar.py
│   ├── test_vigenere.py
│   └── test_frequency.py
│
├── report/
│   └── report.pdf          # Project report (added upon completion)
│
├── app.py                  # Streamlit entry point
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
git clone https://github.com/<your-username>/caesar-vigenere-cipher.git
cd caesar-vigenere-cipher
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run app.py
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.9+ |
| Dashboard | Streamlit |
| Visualization | Plotly |
| Testing | pytest |

---

## Concepts Covered

- Symmetric substitution ciphers
- Monoalphabetic vs. polyalphabetic encryption
- Brute force attacks on small keyspaces
- Letter frequency cryptanalysis

---

## Team

| Name |
|---|
| Ahmed Mohammad Fayad |
| Ahmed Alaa Bahnasy |
| Mostafa Moheb Abo Elmakarim |
| Ahmed Abd Elwhab ElWakil |

---

## License

This project is licensed under the [MIT License](LICENSE).
