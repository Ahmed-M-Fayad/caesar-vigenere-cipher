"""
app.py — Cipher Lab Dashboard
Security (College Course) Project · 2026
"""

import streamlit as st
import plotly.graph_objects as go

from core.caesar    import encrypt as c_enc, decrypt as c_dec, brute_force
from core.vigenere  import encrypt as v_enc, decrypt as v_dec
from core.frequency import get_frequency, recover_caesar_key, ENGLISH_FREQ, score_text
from utils.text_utils import validate_keyword

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Cipher Lab",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# DESIGN TOKENS + GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>

/* ── Fonts ──────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Design tokens ──────────────────────────────────────── */
:root {
    --bg-base:        #07090f;
    --bg-surface:     #0b0e1a;
    --bg-raised:      #0d1120;
    --bg-overlay:     #09090f;

    --border-subtle:  #0f1525;
    --border-default: #141c30;
    --border-strong:  #1a2540;

    --accent-blue:    #3d6fff;
    --accent-blue-hi: #6a96ff;
    --accent-green:   #00c97a;
    --accent-purple:  #9b6fff;

    --text-primary:   #dde4f0;
    --text-secondary: #8090b0;
    --text-muted:     #5a6a94;
    --text-faint:     #2e3d5c;

    --font-mono: 'IBM Plex Mono', monospace;
    --font-sans: 'DM Sans', sans-serif;

    --radius-sm:  6px;
    --radius-md:  10px;
    --radius-lg:  14px;
    --radius-xl:  18px;
    --radius-pill: 999px;
}

/* ── Base ───────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: var(--font-sans);
}
.main .block-container {
    padding-top: 2rem;
    max-width: 1080px;
}

/* ══════════════════════════════════════════════════════════
   SIDEBAR — flex column so footer always sits at the bottom
   regardless of sidebar width
══════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: var(--bg-base) !important;
    border-right: 1px solid #0f1422;
}

/* Make the inner wrapper a full-height flex column */
[data-testid="stSidebar"] > div:first-child {
    display: flex !important;
    flex-direction: column !important;
    height: 100vh !important;
    padding-top: 1.8rem !important;
    padding-bottom: 0 !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
}

/* Nav section grows to fill available space */
[data-testid="stSidebar"] .element-container {
    /* default flow */
}

/* ── Sidebar brand header ───────────────────────────────── */
.sb-brand {
    font-family: var(--font-mono);
    font-size: 15px;
    font-weight: 700;
    color: var(--text-primary);
    padding: 0 18px 24px;
    letter-spacing: 0.02em;
    flex-shrink: 0;
}

/* ── Nav radio: hide widget label ──────────────────────── */
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
    display: none !important;
}

/* Nav items — vertical stack */
[data-testid="stSidebar"] .stRadio > div {
    flex-direction: column !important;
    gap: 1px !important;
}

[data-testid="stSidebar"] .stRadio label {
    width: 100% !important;
    padding: 10px 20px !important;
    border-radius: var(--radius-sm) !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    color: var(--text-muted) !important;
    cursor: pointer !important;
    transition: background 0.15s, color 0.15s !important;
    border-left: 2px solid transparent !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    margin: 0 !important;
    line-height: 1.4 !important;
}

/* Hide only the radio dot, not the text */
[data-testid="stSidebar"] .stRadio label > div:first-child {
    display: none !important;
}
[data-testid="stSidebar"] .stRadio label > div:last-child,
[data-testid="stSidebar"] .stRadio label p {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    color: inherit !important;
    font-size: inherit !important;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background: var(--bg-raised) !important;
    color: var(--text-primary) !important;
}
[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: var(--bg-raised) !important;
    color: var(--accent-blue-hi) !important;
    border-left-color: var(--accent-blue) !important;
    font-weight: 600 !important;
}

/* ── Sidebar footer — pushed to bottom via spacer div ───── */
.sb-footer {
    margin-top: auto;
    padding: 14px 18px 20px;
    border-top: 1px solid var(--border-subtle);
    flex-shrink: 0;
}
.sb-footer-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(61,111,255,0.08);
    border: 1px solid rgba(61,111,255,0.18);
    border-radius: var(--radius-pill);
    padding: 4px 11px;
    font-family: var(--font-mono);
    font-size: 9.5px;
    font-weight: 700;
    color: var(--accent-blue);
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 9px;
}
.sb-footer-dot {
    width: 5px; height: 5px;
    background: var(--accent-blue);
    border-radius: 50%;
}
.sb-footer-title {
    font-family: var(--font-sans);
    font-size: 12px;
    font-weight: 600;
    color: var(--text-secondary);
    line-height: 1.55;
    margin-bottom: 4px;
}
.sb-footer-meta {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--text-faint);
    letter-spacing: 0.05em;
}

/* ══════════════════════════════════════════════════════════
   PAGE TYPOGRAPHY
══════════════════════════════════════════════════════════ */
.pg-title {
    font-family: var(--font-mono);
    font-size: 26px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.02em;
    margin-bottom: 4px;
    line-height: 1.2;
}
.pg-sub {
    font-size: 13.5px;
    color: var(--text-secondary);
    margin-bottom: 28px;
    max-width: 640px;
    line-height: 1.65;
}
.field-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 8px;
    font-family: var(--font-sans);
}

/* ── Widget labels (sliders, text inputs, etc.) ─────────── */
[data-testid="stSlider"] label,
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stSelectbox"] label {
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}

/* ══════════════════════════════════════════════════════════
   ENCRYPT / DECRYPT PILL TOGGLE
   (scoped to main content, not sidebar)
══════════════════════════════════════════════════════════ */
.main .stRadio [data-testid="stWidgetLabel"] p,
section[data-testid="stMainBlockContainer"] .stRadio [data-testid="stWidgetLabel"] p {
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
    margin-bottom: 6px !important;
}
.main .stRadio > div,
section[data-testid="stMainBlockContainer"] .stRadio > div {
    flex-direction: row !important;
    gap: 0 !important;
    flex-wrap: nowrap !important;
}
.main .stRadio label,
section[data-testid="stMainBlockContainer"] .stRadio label {
    background: var(--bg-raised) !important;
    border: 1px solid var(--border-strong) !important;
    color: var(--text-muted) !important;
    padding: 8px 22px !important;
    font-size: 12.5px !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: background 0.15s, color 0.15s !important;
    border-radius: 0 !important;
    white-space: nowrap !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    min-width: 90px !important;
}
.main .stRadio label:first-of-type,
section[data-testid="stMainBlockContainer"] .stRadio label:first-of-type {
    border-radius: var(--radius-sm) 0 0 var(--radius-sm) !important;
}
.main .stRadio label:last-of-type,
section[data-testid="stMainBlockContainer"] .stRadio label:last-of-type {
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0 !important;
    border-left: none !important;
}
.main .stRadio label:hover,
section[data-testid="stMainBlockContainer"] .stRadio label:hover {
    background: #131b30 !important;
    color: var(--text-secondary) !important;
}
.main .stRadio label:has(input:checked),
section[data-testid="stMainBlockContainer"] .stRadio label:has(input:checked) {
    background: linear-gradient(135deg, #1a3080, #2040a0) !important;
    color: #c4d8ff !important;
    border-color: var(--accent-blue) !important;
}
.main .stRadio label > div:first-child,
section[data-testid="stMainBlockContainer"] .stRadio label > div:first-child {
    display: none !important;
}
.main .stRadio label > div:last-child,
.main .stRadio label > span,
section[data-testid="stMainBlockContainer"] .stRadio label > div:last-child,
section[data-testid="stMainBlockContainer"] .stRadio label > span {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    color: inherit !important;
}

/* ══════════════════════════════════════════════════════════
   OUTPUT BOXES
══════════════════════════════════════════════════════════ */
.box-plain {
    background: var(--bg-surface);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-lg);
    padding: 18px 20px;
    font-family: var(--font-mono);
    font-size: 13.5px;
    line-height: 1.8;
    color: #b0bcd8;
    min-height: 76px;
    word-break: break-all;
    white-space: pre-wrap;
}
.box-cipher {
    background: #07091a;
    border: 1px solid var(--border-strong);
    border-left: 3px solid var(--accent-blue);
    border-radius: 0 var(--radius-lg) var(--radius-lg) 0;
    padding: 18px 20px;
    font-family: var(--font-mono);
    font-size: 13.5px;
    line-height: 1.8;
    color: var(--accent-blue-hi);
    min-height: 76px;
    word-break: break-all;
    white-space: pre-wrap;
    letter-spacing: 0.03em;
}
.box-success {
    background: #020e09;
    border: 1px solid #0a2e1c;
    border-left: 3px solid var(--accent-green);
    border-radius: 0 var(--radius-lg) var(--radius-lg) 0;
    padding: 18px 20px;
    font-family: var(--font-mono);
    font-size: 13.5px;
    line-height: 1.8;
    color: var(--accent-green);
    min-height: 76px;
    word-break: break-all;
    white-space: pre-wrap;
}
.box-empty {
    background: var(--bg-overlay);
    border: 1px dashed #1a2240;
    border-radius: var(--radius-lg);
    padding: 30px 20px;
    font-family: var(--font-mono);
    font-size: 12px;
    color: #3a4a6a;
    text-align: center;
    min-height: 76px;
}

/* ══════════════════════════════════════════════════════════
   COMPONENTS
══════════════════════════════════════════════════════════ */

/* Key badge pill */
.key-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #0b1228;
    border: 1px solid #182040;
    border-radius: var(--radius-pill);
    padding: 5px 14px;
    font-family: var(--font-mono);
    font-size: 12.5px;
    color: var(--accent-blue);
    font-weight: 700;
    letter-spacing: 0.03em;
}

/* Info callout strip */
.callout {
    background: #070f1a;
    border: 1px solid #0f2040;
    border-left: 3px solid var(--accent-blue);
    border-radius: 0 var(--radius-md) var(--radius-md) 0;
    padding: 10px 16px;
    margin-bottom: 16px;
    font-size: 12.5px;
    color: #6a85c0;
    line-height: 1.6;
}

/* Live indicator */
.live-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
}
.live-dot {
    width: 7px; height: 7px;
    background: var(--accent-green);
    border-radius: 50%;
    flex-shrink: 0;
    animation: pulse 1.6s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: .3; transform: scale(.8); }
}
.live-label {
    font-size: 11px;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.14em;
}

/* Stat cards grid */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 28px;
}
.stat-card {
    background: var(--bg-overlay);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 22px 16px;
    text-align: center;
    transition: border-color 0.2s;
}
.stat-card:hover { border-color: #1a2a50; }
.stat-value {
    display: block;
    font-family: var(--font-mono);
    font-size: 30px;
    font-weight: 700;
    color: var(--accent-blue);
    line-height: 1;
    margin-bottom: 10px;
}
.stat-label {
    font-size: 10.5px;
    color: var(--text-muted);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}

/* Brute-force detected key badge */
.bf-badge {
    background: #020e09;
    border: 1px solid #0a2e1c;
    border-left: 3px solid var(--accent-green);
    border-radius: 0 var(--radius-md) var(--radius-md) 0;
    padding: 9px 14px;
    font-family: var(--font-mono);
    font-size: 11.5px;
    color: var(--accent-green);
    font-weight: 600;
}

/* ── Buttons ─────────────────────────────────────────────── */
[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-purple) 100%);
    border: none;
    border-radius: var(--radius-md);
    font-weight: 600;
    font-size: 14px;
    letter-spacing: 0.03em;
    color: #fff !important;
    transition: opacity 0.15s;
}
[data-testid="stButton"] button[kind="primary"]:hover { opacity: 0.88; }

/* ── Divider ─────────────────────────────────────────────── */
hr { border-color: var(--bg-raised) !important; margin: 1.4rem 0 !important; }

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:

    st.markdown("<div class='sb-brand'>🔐 CIPHER LAB</div>", unsafe_allow_html=True)

    page = st.radio(
        "nav",
        label_visibility="collapsed",
        options=[
            "🏠   Overview",
            "⚔️   Caesar Cipher",
            "🗝️   Vigenère Cipher",
            "💥   Brute Force",
            "📊   Frequency Analysis",
            "📁   File Mode",
        ],
    )

    # Spacer pushes footer to the bottom via flex
    st.markdown(
        "<div style='flex:1; min-height:40px;'></div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sb-footer">
            <div class="sb-footer-badge">
                <div class="sb-footer-dot"></div>
                Security Course
            </div>
            <div class="sb-footer-title">
                Classical Cryptography<br>College Project
            </div>
            <div class="sb-footer-meta">MIT License &nbsp;&middot;&nbsp; 2026</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def render_io(label_in, text_in, label_out, text_out, success=False):
    """Render a two-column input/output display."""
    col_a, col_b = st.columns(2, gap="medium")
    with col_a:
        st.markdown(f"<div class='field-label'>{label_in}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='box-plain'>{text_in}</div>", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"<div class='field-label'>{label_out}</div>", unsafe_allow_html=True)
        box_cls = "box-success" if success else "box-cipher"
        st.markdown(f"<div class='{box_cls}'>{text_out}</div>", unsafe_allow_html=True)


def page_header(title: str, subtitle: str):
    st.markdown(f"<div class='pg-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='pg-sub'>{subtitle}</div>", unsafe_allow_html=True)


def callout(msg: str):
    st.markdown(f"<div class='callout'>{msg}</div>", unsafe_allow_html=True)


def empty_state(msg: str = "output appears here as you type…"):
    st.markdown(f"<div class='box-empty'>{msg}</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────

if page == "🏠   Overview":

    st.markdown("""
    <style>
    .hero {
        background: linear-gradient(135deg, #07090f 0%, #0a0e1e 55%, #060d1a 100%);
        border: 1px solid #111827;
        border-radius: var(--radius-xl);
        padding: 42px 48px 38px;
        margin-bottom: 32px;
        position: relative;
        overflow: hidden;
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -80px; right: -80px;
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(61,111,255,0.06) 0%, transparent 65%);
        pointer-events: none;
    }
    .hero::after {
        content: '';
        position: absolute;
        bottom: -40px; left: 30%;
        width: 200px; height: 200px;
        background: radial-gradient(circle, rgba(155,111,255,0.04) 0%, transparent 65%);
        pointer-events: none;
    }
    .hero-eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(61,111,255,0.08);
        border: 1px solid rgba(61,111,255,0.18);
        border-radius: var(--radius-pill);
        padding: 5px 14px;
        font-family: var(--font-mono);
        font-size: 10px;
        font-weight: 700;
        color: #5a88ff;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-bottom: 22px;
    }
    .hero-eyebrow-dot {
        width: 5px; height: 5px;
        background: var(--accent-blue);
        border-radius: 50%;
        animation: pulse 2s ease-in-out infinite;
    }
    .hero-h1 {
        font-family: var(--font-mono);
        font-size: 44px;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.03em;
        line-height: 1.15;
        margin-bottom: 18px;
    }
    .hero-h1 em {
        font-style: normal;
        background: linear-gradient(90deg, #5a88ff 0%, var(--accent-purple) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-desc {
        font-size: 15px;
        color: #6a7a9e;
        max-width: 560px;
        line-height: 1.75;
        margin-bottom: 28px;
    }
    .hero-tags { display: flex; gap: 8px; flex-wrap: wrap; }
    .hero-tag {
        background: var(--bg-surface);
        border: 1px solid var(--border-default);
        border-radius: var(--radius-sm);
        padding: 5px 13px;
        font-family: var(--font-mono);
        font-size: 10.5px;
        color: #4a5e88;
        font-weight: 600;
        letter-spacing: 0.05em;
    }
    .hero-tag.hi {
        color: var(--accent-blue);
        border-color: #1a2f5a;
        background: #080e1e;
    }
    </style>
    <div class="hero">
        <div class="hero-eyebrow">
            <div class="hero-eyebrow-dot"></div>
            Security (College Course) Project &nbsp;&middot;&nbsp; 2026
        </div>
        <div class="hero-h1">Classical<br><em>Cipher Lab</em></div>
        <p class="hero-desc">
            Two ciphers. Two ways to break them.
            Caesar shifts every letter by a fixed amount.
            Vigen&egrave;re cycles through a keyword.
            Neither survives modern cryptanalysis &mdash; and this lab shows exactly why.
        </p>
        <div class="hero-tags">
            <div class="hero-tag hi">Caesar Cipher</div>
            <div class="hero-tag hi">Vigen&egrave;re Cipher</div>
            <div class="hero-tag">Brute Force</div>
            <div class="hero-tag">Frequency Analysis</div>
            <div class="hero-tag">File Processing</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div class='stat-grid'>"
        "<div class='stat-card'><span class='stat-value'>25</span><span class='stat-label'>Caesar keyspace</span></div>"
        "<div class='stat-card'><span class='stat-value'>26ⁿ</span><span class='stat-label'>Vigenère keyspace</span></div>"
        "<div class='stat-card'><span class='stat-value'>12.7%</span><span class='stat-label'>English 'E' frequency</span></div>"
        "<div class='stat-card'><span class='stat-value'>χ²</span><span class='stat-label'>Analysis method</span></div>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        "<div class='live-row'><div class='live-dot'></div>"
        "<span class='live-label'>Live Demo — type to encrypt instantly</span></div>",
        unsafe_allow_html=True,
    )

    col_msg, col_shift = st.columns([3, 1], gap="large")
    with col_msg:
        demo_text = st.text_input("Message", value="Hello, World!", placeholder="Type your message…")
    with col_shift:
        demo_shift = st.slider("Shift amount", 1, 25, 3)

    if demo_text.strip():
        render_io(
            "Plaintext", demo_text,
            f"Caesar · shift {demo_shift}", c_enc(demo_text, demo_shift),
        )
    else:
        empty_state("ciphertext appears here as you type…")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: CAESAR
# ─────────────────────────────────────────────────────────────────────────────

elif page == "⚔️   Caesar Cipher":

    page_header(
        "Caesar Cipher",
        "C = (P + key) mod 26 &nbsp;·&nbsp; Every letter shifts by the same fixed amount.",
    )
    callout(
        "⚡ <strong style='color:var(--accent-blue-hi)'>Live mode</strong> — "
        "output updates instantly. Choose an operation and adjust the shift slider."
    )

    col_text, col_ctrl = st.columns([3, 1], gap="large")
    with col_text:
        c_text = st.text_area("Input text", height=160, placeholder="Type or paste your message…")
    with col_ctrl:
        c_shift = st.slider("Key (shift)", 1, 25, 3)
        st.markdown(
            f"<div class='field-label' style='margin-top:12px;'>Active key</div>"
            f"<div class='key-pill'>+ {c_shift}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        c_mode = st.radio("Operation", ["Encrypt", "Decrypt"], horizontal=True)

    if c_text.strip():
        result = c_enc(c_text, c_shift) if c_mode == "Encrypt" else c_dec(c_text, c_shift)
        lin  = "Plaintext"  if c_mode == "Encrypt" else "Ciphertext"
        lout = f"Ciphertext (shift {c_shift})" if c_mode == "Encrypt" else f"Plaintext (shift {c_shift})"
        render_io(lin, c_text, lout, result)
        st.markdown("<br>", unsafe_allow_html=True)
        st.code(result, language=None)
    else:
        empty_state()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: VIGENÈRE
# ─────────────────────────────────────────────────────────────────────────────

elif page == "🗝️   Vigenère Cipher":

    page_header(
        "Vigenère Cipher",
        "C<sub>i</sub> = (P<sub>i</sub> + K<sub>i</sub>) mod 26 &nbsp;·&nbsp; "
        "Each letter gets a different shift — determined by a cycling keyword.",
    )
    callout(
        "⚡ <strong style='color:var(--accent-blue-hi)'>Live mode</strong> — "
        "enter a keyword (letters only), pick an operation, then type your message."
    )

    col_text, col_ctrl = st.columns([3, 1], gap="large")
    with col_text:
        v_text = st.text_area("Input text", height=160, placeholder="Type or paste your message…")
    with col_ctrl:
        v_kw   = st.text_input("Keyword", value="KEY")
        v_mode = st.radio("Operation", ["Encrypt", "Decrypt"], horizontal=True)
        if v_kw:
            if validate_keyword(v_kw):
                st.markdown(
                    f"<div class='key-pill' style='margin-top:8px;'>key: {v_kw.upper()}</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.error("Letters only — no digits or symbols.")

    kw_valid = validate_keyword(v_kw)

    if v_text.strip() and kw_valid:
        try:
            result = v_enc(v_text, v_kw) if v_mode == "Encrypt" else v_dec(v_text, v_kw)
            lin  = "Plaintext"  if v_mode == "Encrypt" else "Ciphertext"
            lout = f"Ciphertext (key: {v_kw.upper()})" if v_mode == "Encrypt" else f"Plaintext (key: {v_kw.upper()})"
            render_io(lin, v_text, lout, result)

            st.divider()
            st.markdown("**Keyword Alignment**")

            kw_up  = v_kw.upper()
            shifts = [ord(c) - ord("A") for c in kw_up]
            pl     = [c for c in v_text   if c.isalpha()]
            cl_    = [c for c in result   if c.isalpha()]
            n      = min(24, len(pl))

            if n > 0:
                st.dataframe(
                    {
                        "#":      list(range(1, n + 1)),
                        "Plain":  [p.upper()               for p in pl[:n]],
                        "Key":    [kw_up[i % len(kw_up)]   for i in range(n)],
                        "Shift":  [shifts[i % len(shifts)]  for i in range(n)],
                        "Cipher": [c.upper()               for c in cl_[:n]],
                    },
                    use_container_width=True,
                    hide_index=True,
                )
                if len(pl) > 24:
                    st.caption(f"Showing 24 of {len(pl)} alphabetic characters.")

            st.code(result, language=None)

        except ValueError as e:
            st.error(str(e))

    elif v_text.strip() and not kw_valid:
        empty_state("fix the keyword above to see output…")
    else:
        empty_state()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: BRUTE FORCE
# ─────────────────────────────────────────────────────────────────────────────

elif page == "💥   Brute Force":

    page_header(
        "Brute Force Attack",
        "Caesar has exactly 25 non-trivial keys. "
        "We try all of them and rank each decryption against English letter frequencies. "
        "The top result is the statistically most likely plaintext.",
    )

    bf_text = st.text_area(
        "Ciphertext to attack",
        height=130,
        placeholder="Paste Caesar-encrypted text here…",
    )

    if st.button("🚀  Launch Attack", type="primary", use_container_width=True):
        text = bf_text.strip()
        if not text:
            st.warning("Paste a ciphertext to attack.")
        else:
            with st.status("Running brute force attack…", expanded=True) as status:
                st.write("Generating all 25 decryptions…")
                raw = brute_force(text)
                st.write("Scoring against English letter frequencies (χ²)…")
                scored = sorted(
                    [(sh, pt, score_text(pt)) for sh, pt in raw],
                    key=lambda x: x[2],
                )
                st.write("Ranking results…")
                status.update(label="Attack complete ✓", state="complete", expanded=False)

            best_sh, best_pt, _ = scored[0]

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Most Likely Decryption**")
            col_key, col_out = st.columns([1, 4], gap="medium")
            with col_key:
                st.metric("Key", best_sh)
            with col_out:
                st.markdown(f"<div class='box-success'>{best_pt}</div>", unsafe_allow_html=True)

            st.divider()
            st.markdown("**All 25 Shifts** — sorted by likelihood")
            st.dataframe(
                [
                    {
                        "Rank":           i + 1,
                        "Shift":          sh,
                        "Decrypted Text": pt[:88] + ("…" if len(pt) > 88 else ""),
                        "Confidence %":   round(100 / (1 + sc), 2),
                    }
                    for i, (sh, pt, sc) in enumerate(scored)
                ],
                use_container_width=True,
                hide_index=True,
            )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: FREQUENCY ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────

elif page == "📊   Frequency Analysis":

    page_header(
        "Frequency Analysis",
        "Caesar is monoalphabetic — every 'E' encrypts to the same letter. "
        "English's statistical fingerprint survives the cipher, just shifted. "
        "The chart makes the offset visible; the algorithm recovers the key.",
    )

    freq_text = st.text_area(
        "Ciphertext to analyse",
        height=130,
        placeholder="Paste Caesar-encrypted text here…",
    )

    if st.button("📊  Run Analysis", type="primary", use_container_width=True):
        text = freq_text.strip()
        if not text:
            st.warning("Paste a ciphertext first.")
        elif not any(c.isalpha() for c in text):
            st.error("Frequency analysis needs alphabetic characters.")
        else:
            try:
                cf    = get_frequency(text)
                key   = recover_caesar_key(text)
                plain = c_dec(text, key)
                top_l = max(cf, key=cf.get)

                m1, m2, m3 = st.columns(3)
                m1.metric("Recovered Key (shift)", key)
                m2.metric("Most Frequent Letter", f"{top_l}  ({cf[top_l]:.1f}%)")
                m3.metric("Expected (English)", f"{top_l} → E  (Δ{(ord(top_l) - ord('E')) % 26})")

                st.markdown(
                    "<div class='field-label' style='margin-top:16px;'>Recovered Plaintext</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(f"<div class='box-success'>{plain}</div>", unsafe_allow_html=True)
                st.divider()

                letters = list(ENGLISH_FREQ.keys())
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    name="Ciphertext",
                    x=letters,
                    y=[cf[l] for l in letters],
                    marker=dict(
                        color=[cf[l] for l in letters],
                        colorscale=[[0, "#0d1a3a"], [1, "#3d6fff"]],
                        line=dict(width=0),
                    ),
                    hovertemplate="%{x}: %{y:.2f}%<extra>Ciphertext</extra>",
                ))
                fig.add_trace(go.Bar(
                    name="English Reference",
                    x=letters,
                    y=[ENGLISH_FREQ[l] for l in letters],
                    marker_color="#00c97a",
                    opacity=0.30,
                    hovertemplate="%{x}: %{y:.2f}%<extra>English</extra>",
                ))
                fig.update_layout(
                    barmode="overlay",
                    bargap=0.08,
                    title=dict(
                        text="Letter Distribution — Ciphertext vs English",
                        font=dict(family="IBM Plex Mono", size=13, color="#c4cde6"),
                        x=0,
                    ),
                    xaxis=dict(title="Letter", color="#8090b0", gridcolor="#09090f", linecolor="#0d1120"),
                    yaxis=dict(title="Frequency (%)", color="#8090b0", gridcolor="#09090f", linecolor="#0d1120"),
                    plot_bgcolor="#07090f",
                    paper_bgcolor="#07090f",
                    font=dict(family="DM Sans", color="#8090b0"),
                    legend=dict(bgcolor="#09090f", bordercolor="#0f1525", borderwidth=1, font=dict(size=12)),
                    height=390,
                    margin=dict(l=40, r=10, t=50, b=30),
                )
                st.plotly_chart(fig, use_container_width=True)

            except ValueError as e:
                st.error(str(e))


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: FILE MODE
# ─────────────────────────────────────────────────────────────────────────────

elif page == "📁   File Mode":

    page_header(
        "File Mode",
        "Upload a .txt file, apply any cipher, and download the result. "
        "Caesar decrypt uses brute force — no shift required.",
    )

    uploaded = st.file_uploader("Choose a .txt file", type=["txt"])

    if uploaded:
        content = uploaded.read().decode("utf-8")

        st.markdown("<div class='field-label'>Preview</div>", unsafe_allow_html=True)
        preview = content[:500] + ("…" if len(content) > 500 else "")
        st.markdown(f"<div class='box-plain'>{preview}</div>", unsafe_allow_html=True)
        st.caption(
            f"**{uploaded.name}** · "
            f"{len(content):,} characters · "
            f"{sum(c.isalpha() for c in content):,} letters"
        )
        st.divider()

        col_cipher, col_mode, col_key = st.columns(3, gap="medium")
        with col_cipher:
            f_cipher = st.selectbox("Cipher", ["Caesar", "Vigenère"])
        with col_mode:
            f_mode = st.radio("Operation", ["Encrypt", "Decrypt"], horizontal=True)
        with col_key:
            f_shift = None
            f_kw    = None
            if f_cipher == "Caesar":
                if f_mode == "Encrypt":
                    f_shift = st.slider("Shift", 1, 25, 3)
                else:
                    # Decrypt: brute force — no shift needed
                    st.markdown(
                        "<div class='field-label'>Key detection</div>"
                        "<div class='bf-badge'>🔍 Auto &nbsp;&middot;&nbsp; Brute Force</div>",
                        unsafe_allow_html=True,
                    )
            else:
                f_kw = st.text_input("Keyword", value="KEY")

        if st.button("⚙️  Process File", type="primary", use_container_width=True):
            try:
                if f_cipher == "Caesar":
                    if f_mode == "Encrypt":
                        result = c_enc(content, f_shift)
                    else:
                        with st.status("Running brute force on file…", expanded=True) as status:
                            st.write("Trying all 25 shifts…")
                            raw = brute_force(content)
                            st.write("Scoring against English frequencies (χ²)…")
                            scored = sorted(
                                [(sh, pt, score_text(pt)) for sh, pt in raw],
                                key=lambda x: x[2],
                            )
                            best_sh, best_pt, _ = scored[0]
                            status.update(
                                label=f"Key found: shift {best_sh} ✓",
                                state="complete",
                                expanded=False,
                            )
                        result = best_pt
                        callout(
                            f"🔍 <strong style='color:{{}};'>Brute force recovered key:</strong>"
                            f" shift <strong style='color:var(--accent-blue-hi)'>{best_sh}</strong>"
                            .format("#00c97a")
                        )
                else:
                    if not validate_keyword(f_kw or ""):
                        st.error("Invalid keyword — letters only.")
                        st.stop()
                    result = v_enc(content, f_kw) if f_mode == "Encrypt" else v_dec(content, f_kw)

                st.markdown("<div class='field-label'>Output Preview</div>", unsafe_allow_html=True)
                out_preview = result[:500] + ("…" if len(result) > 500 else "")
                st.markdown(f"<div class='box-cipher'>{out_preview}</div>", unsafe_allow_html=True)

                action   = "encrypted" if f_mode == "Encrypt" else "decrypted"
                out_name = f"{action}_{uploaded.name}"

                st.download_button(
                    f"⬇️  Download  {out_name}",
                    data=result,
                    file_name=out_name,
                    mime="text/plain",
                    use_container_width=True,
                )
                st.toast(f"File {action} successfully.", icon="✅")

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        empty_state("drop a .txt file above to get started…")


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────

st.divider()
st.markdown(
    "<p style='text-align:center; color:var(--text-faint); font-size:11px;"
    "font-family:var(--font-mono);'>"
    "Security (College Course) Project &nbsp;&middot;&nbsp; "
    "Caesar &amp; Vigen&egrave;re Cipher &nbsp;&middot;&nbsp; "
    "MIT License &nbsp;&middot;&nbsp; 2026"
    "</p>",
    unsafe_allow_html=True,
)
