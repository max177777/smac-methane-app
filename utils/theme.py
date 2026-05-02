"""
Shared theme. Injects custom CSS to give Streamlit pages the SMAC editorial look.
Call inject_theme() at the top of every page.
"""

import streamlit as st


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,500;9..144,700&family=JetBrains+Mono:wght@300;400;500;700&family=Inter+Tight:wght@300;400;500;600;700&display=swap');

:root {
  --paper: #f4efe6;
  --paper-2: #ebe4d6;
  --paper-3: #e0d7c4;
  --ink: #1a1f1a;
  --ink-soft: #3a4239;
  --line: #3a4239;
  --line-soft: #c4bca8;
  --moss: #2d4a36;
  --copper: #b5612a;
  --rust: #7a3a1a;
  --good: #4a6b3e;
}

/* base */
html, body, [class*="css"], .stApp {
  font-family: 'Inter Tight', sans-serif !important;
  background-color: var(--paper) !important;
  color: var(--ink) !important;
}

.stApp {
  background-image:
    radial-gradient(1200px 800px at 80% -10%, rgba(181,97,42,0.05), transparent 60%),
    radial-gradient(900px 700px at -10% 90%, rgba(45,74,54,0.08), transparent 55%);
}

/* main container - widen a bit */
.main .block-container {
  padding-top: 2rem;
  padding-bottom: 4rem;
  max-width: 1280px;
}

/* sidebar */
[data-testid="stSidebar"] {
  background-color: var(--paper-2) !important;
  border-right: 1px solid var(--line);
}
[data-testid="stSidebar"] .stMarkdown {
  font-family: 'Inter Tight', sans-serif;
}

/* headings - serif display */
h1, h2, h3, h4 {
  font-family: 'Fraunces', serif !important;
  font-weight: 300 !important;
  letter-spacing: -0.02em;
  color: var(--ink) !important;
}
h1 { font-size: 3.2rem !important; line-height: 1 !important; }
h2 { font-size: 2.2rem !important; }
h3 { font-size: 1.4rem !important; font-weight: 400 !important; }

em, i { color: var(--moss); font-style: italic; }

/* dividers */
hr { border-color: var(--line-soft) !important; }

/* buttons */
.stButton > button {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 11px !important;
  letter-spacing: 0.14em !important;
  text-transform: uppercase !important;
  border: 1.5px solid var(--ink) !important;
  background: var(--ink) !important;
  color: var(--paper) !important;
  border-radius: 0 !important;
  padding: 8px 18px !important;
  font-weight: 500 !important;
  transition: all 0.2s ease;
}
.stButton > button:hover {
  background: var(--moss) !important;
  border-color: var(--moss) !important;
  transform: translateY(-1px);
}
.stButton > button[kind="secondary"] {
  background: transparent !important;
  color: var(--ink) !important;
}
.stButton > button[kind="secondary"]:hover {
  background: var(--ink) !important;
  color: var(--paper) !important;
}

/* select boxes */
.stSelectbox label, .stRadio label {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 10px !important;
  letter-spacing: 0.16em !important;
  text-transform: uppercase !important;
  color: var(--copper) !important;
  font-weight: 500 !important;
}
[data-baseweb="select"] > div {
  background: var(--paper) !important;
  border-color: var(--line-soft) !important;
  border-radius: 0 !important;
}

/* radios */
.stRadio > div { gap: 4px !important; }
.stRadio [data-baseweb="radio"] {
  background: var(--paper);
  border: 1px solid var(--line-soft);
  padding: 8px 14px;
}

/* metric cards */
[data-testid="stMetric"] {
  background: var(--paper-2);
  border: 1px solid var(--line);
  padding: 18px 22px;
}
[data-testid="stMetricLabel"] {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 10px !important;
  letter-spacing: 0.14em !important;
  text-transform: uppercase !important;
  color: var(--ink-soft) !important;
}
[data-testid="stMetricValue"] {
  font-family: 'Fraunces', serif !important;
  font-weight: 300 !important;
  font-size: 2.2rem !important;
  letter-spacing: -0.02em !important;
}
[data-testid="stMetricDelta"] {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 11px !important;
  letter-spacing: 0.06em !important;
}

/* tabs */
.stTabs [data-baseweb="tab-list"] {
  gap: 0;
  border-bottom: 1px solid var(--line);
}
.stTabs [data-baseweb="tab"] {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 11px !important;
  letter-spacing: 0.14em !important;
  text-transform: uppercase !important;
  color: var(--ink-soft) !important;
  padding: 12px 20px !important;
  border-radius: 0 !important;
  background: transparent !important;
  border-bottom: 2px solid transparent !important;
  margin-bottom: -1px !important;
}
.stTabs [aria-selected="true"] {
  color: var(--ink) !important;
  border-bottom-color: var(--copper) !important;
  font-weight: 500 !important;
}

/* tables / dataframes */
[data-testid="stDataFrame"], [data-testid="stTable"] {
  border: 1px solid var(--line);
  font-family: 'Inter Tight', sans-serif;
}
[data-testid="stDataFrame"] thead tr th {
  background: var(--paper-2) !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 10px !important;
  text-transform: uppercase !important;
  letter-spacing: 0.12em !important;
  color: var(--ink-soft) !important;
}

/* chat messages */
[data-testid="stChatMessage"] {
  background: var(--paper-2) !important;
  border-left: 3px solid var(--copper) !important;
  border-radius: 0 !important;
  padding: 18px 22px !important;
  margin-bottom: 16px;
}
[data-testid="stChatMessage"][data-testid*="user"] {
  background: var(--ink) !important;
  color: var(--paper) !important;
  border-left: none !important;
  border-right: 3px solid var(--copper) !important;
}
[data-testid="stChatMessage"][data-testid*="user"] p {
  color: var(--paper) !important;
}

/* chat input */
[data-testid="stChatInput"] {
  border: 1.5px solid var(--ink) !important;
  border-radius: 0 !important;
  background: var(--paper) !important;
}

/* eyebrow class for section labels */
.smac-eyebrow {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--copper);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.smac-eyebrow::before {
  content: "";
  width: 24px;
  height: 1px;
  background: var(--copper);
}

/* monospace meta line */
.smac-meta {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--ink-soft);
}

/* struct chat blocks */
.smac-struct-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--copper);
  margin-bottom: 6px;
  margin-top: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.smac-struct-label::before {
  content: "";
  width: 14px;
  height: 1px;
  background: var(--copper);
}
.smac-method-block {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11.5px;
  color: var(--ink-soft);
  background: var(--paper);
  padding: 10px 14px;
  border: 1px dashed var(--line-soft);
  line-height: 1.6;
  margin-top: 6px;
}

/* greenwashing flag */
.smac-flag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: var(--copper);
  letter-spacing: 0.04em;
}

/* hide streamlit footer */
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }

/* nicer expander */
.streamlit-expanderHeader {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 11px !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  color: var(--ink-soft) !important;
}
</style>
"""


def inject_theme():
    """Inject the shared CSS. Call once at the top of each page."""
    st.markdown(CSS, unsafe_allow_html=True)


def eyebrow(text: str):
    """Render a small section eyebrow label."""
    st.markdown(f'<div class="smac-eyebrow">{text}</div>', unsafe_allow_html=True)


def meta_line(text: str):
    st.markdown(f'<div class="smac-meta">{text}</div>', unsafe_allow_html=True)
