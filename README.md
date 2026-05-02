# SMAC — Subnational Methane Atlas & Chat

A Streamlit prototype that translates Climate TRACE methane data into structured
policy guidance for subnational governments.

- **11 countries** · **287 subnational units** · **48 months** (2021–2024)
- **Four pages**: Overview, Atlas (country profiles), Insights (dashboard), Chat
- **Dual-mode chat**: Methane Specialist (data-grounded structured responses) +
  General Assistant (free-form conversational)
- **Scripted AI** — no API key required; all responses are generated locally from
  the CSV plus a curated policy/pathway knowledge base

## Quick start

```bash
# 1. Create a virtual env (recommended)
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate           # Windows PowerShell

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Project structure

```
smac_app/
├── app.py                          # entry point, st.navigation
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml                 # editorial theme colours
├── data/
│   └── SMAC_methane_monthly.csv    # raw Climate TRACE data
├── pages/
│   ├── 1_Overview.py               # landing page
│   ├── 2_Atlas.py                  # country profiles
│   ├── 3_Insights.py               # dashboard
│   └── 4_Chat.py                   # dual-mode chat
└── utils/
    ├── __init__.py
    ├── data_loader.py              # cached CSV → dataframes
    ├── policy_content.py           # curated policy + pathway knowledge
    ├── chat_engine.py              # scripted response builder
    ├── charts.py                   # Plotly + Altair helpers
    └── theme.py                    # CSS injection
```

## How the chat works

### Methane Specialist (default)
- Sidebar binds the response to one **country**, **subnational unit** (or national
  aggregate), **metric** (CH₄, GWP100, GWP20), and **output type** (data / trend
  / policy / pathway / method).
- The user's question is also analysed for keywords ("trend", "policy",
  "mitigation", "GWP") that override the sidebar's output type.
- Every response is rendered as a five-block structure: **Summary · Key Data
  Insight · Policy Context · Recommended Mitigation Pathway · Method · Uncertainty**.
- Inline mini time-series chart attached to each response.

### General Assistant
- No data sidebar. Open conversation.
- Pattern-matched scripted replies for common topics (climate, methane physics,
  email drafting, LA travel, etc.) plus a graceful fallback.

## Data

The CSV in `data/SMAC_methane_monthly.csv` is monthly subnational methane
emissions in tonnes from Climate TRACE, covering 11 countries from 2021 to 2024.

Columns:
- `iso3_country`
- `location` (state, province, autonomous community, etc.)
- `year`, `month`
- `total_emission` (tonnes CH₄)

## Customising

- **Add countries**: drop more rows into the CSV using the same schema; add an
  entry to `COUNTRY_META` in `utils/data_loader.py`, plus a `POLICY`,
  `SECTORS`, and `PATHWAYS` entry in `utils/policy_content.py`.
- **Swap the chat backend for real LLM**: replace
  `build_methane_response()` and `build_general_response()` in
  `utils/chat_engine.py` with calls to your provider (Claude / OpenAI / etc.).
  The data loader already exposes everything needed for grounded prompts.
- **Restyle**: edit `utils/theme.py` (CSS) and `.streamlit/config.toml`
  (Streamlit base theme).

## Notes

- All AI responses are scripted demos. Numbers are real (Climate TRACE 2024
  release) but recommendations are illustrative — not for policy use.
- IPCC AR6 GWP factors used: GWP100 = 27, GWP20 = 80 (non-fossil CH₄, rounded).
