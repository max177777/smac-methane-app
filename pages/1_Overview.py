"""
Overview / landing page.
"""

import streamlit as st

from utils.theme import inject_theme, eyebrow
from utils.data_loader import (
    COUNTRY_META, COUNTRY_ORDER, all_countries_2024_total,
    country_monthly, country_yearly, fmt_mt, pct_change,
)
from utils.charts import sparkline_plotly


inject_theme()

# ============== HERO ==============
col1, col2 = st.columns([1.4, 1], gap="large")

with col1:
    eyebrow("Subnational Climate Decision Tool · 2026")
    st.markdown(
        "<h1 style='margin-bottom:0;'>Translating <em>methane data</em> into "
        "<span style='color:var(--copper);font-style:italic;'>policy pathways.</span></h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="font-family:Fraunces,serif;font-size:18px;line-height:1.55;'
        'color:var(--ink-soft);max-width:520px;margin-top:24px;font-weight:300;">'
        "An AI-assisted reasoning interface for subnational governments. Eleven countries, "
        "280+ subnational units, 48 months of methane emissions data — paired with a chat that "
        "reasons through IPCC GWP frameworks and policy context."
        "</p>",
        unsafe_allow_html=True,
    )

    st.write("")
    cta1, cta2, _ = st.columns([1, 1, 2])
    with cta1:
        if st.button("Open Chat →", use_container_width=True, type="primary"):
            st.switch_page("pages/4_Chat.py")
    with cta2:
        if st.button("Browse Atlas", use_container_width=True):
            st.switch_page("pages/2_Atlas.py")

with col2:
    summary = all_countries_2024_total()
    total_2024 = summary["ch4_2024_tonnes"].sum()
    total_loc = int(summary["n_locations"].sum())

    st.markdown(
        f"""
        <div style="border-top:1px solid var(--line);padding:20px 0;display:flex;justify-content:space-between;align-items:baseline;">
          <div style="font-family:Fraunces,serif;font-size:42px;font-weight:300;letter-spacing:-0.02em;line-height:1;">
            {len(COUNTRY_ORDER)}<span style="font-family:JetBrains Mono,monospace;font-size:11px;color:var(--ink-soft);margin-left:6px;letter-spacing:0.1em;">countries</span>
          </div>
          <div style="font-family:JetBrains Mono,monospace;font-size:10px;text-transform:uppercase;letter-spacing:0.12em;color:var(--ink-soft);text-align:right;max-width:180px;line-height:1.4;">Pre-loaded Atlas coverage</div>
        </div>
        <div style="border-top:1px solid var(--line);padding:20px 0;display:flex;justify-content:space-between;align-items:baseline;">
          <div style="font-family:Fraunces,serif;font-size:42px;font-weight:300;letter-spacing:-0.02em;line-height:1;">
            {total_loc}<span style="font-family:JetBrains Mono,monospace;font-size:11px;color:var(--ink-soft);margin-left:6px;letter-spacing:0.1em;">subunits</span>
          </div>
          <div style="font-family:JetBrains Mono,monospace;font-size:10px;text-transform:uppercase;letter-spacing:0.12em;color:var(--ink-soft);text-align:right;max-width:180px;line-height:1.4;">States, provinces, autonomous regions</div>
        </div>
        <div style="border-top:1px solid var(--line);padding:20px 0;display:flex;justify-content:space-between;align-items:baseline;">
          <div style="font-family:Fraunces,serif;font-size:42px;font-weight:300;letter-spacing:-0.02em;line-height:1;">
            48<span style="font-family:JetBrains Mono,monospace;font-size:11px;color:var(--ink-soft);margin-left:6px;letter-spacing:0.1em;">months</span>
          </div>
          <div style="font-family:JetBrains Mono,monospace;font-size:10px;text-transform:uppercase;letter-spacing:0.12em;color:var(--ink-soft);text-align:right;max-width:180px;line-height:1.4;">Monthly time series · 2021 to 2024</div>
        </div>
        <div style="border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:20px 0;display:flex;justify-content:space-between;align-items:baseline;">
          <div style="font-family:Fraunces,serif;font-size:42px;font-weight:300;letter-spacing:-0.02em;line-height:1;">
            {fmt_mt(total_2024)}<span style="font-family:JetBrains Mono,monospace;font-size:11px;color:var(--ink-soft);margin-left:6px;letter-spacing:0.1em;">Mt CH₄</span>
          </div>
          <div style="font-family:JetBrains Mono,monospace;font-size:10px;text-transform:uppercase;letter-spacing:0.12em;color:var(--ink-soft);text-align:right;max-width:180px;line-height:1.4;">Combined 2024 atlas emissions</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ============== WORKFLOW ==============
eyebrow("Methodology")
st.markdown("<h2 style='font-size:2.2rem;margin-bottom:32px;'>Five-stage <em>reasoning pipeline</em>, not a static dashboard.</h2>", unsafe_allow_html=True)

flow_steps = [
    ("01 / DATA", "Ingest", "Climate TRACE monthly methane at subnational resolution; 11 countries pre-loaded."),
    ("02 / INVENT.", "Reconcile", "Time-series check, year-over-year drift, location-level uncertainty flagging."),
    ("03 / INSIGHT", "Interpret", "CH₄ → CO₂e under both GWP100 and GWP20; hotspot detection by subunit."),
    ("04 / DECISION", "Reason", "AI chat synthesizes data, policy context, and method into a structured answer."),
    ("05 / PATHWAYS", "Recommend", "Mitigation actions sequenced by abatement density, with greenwashing checks."),
]
flow_cols = st.columns(5)
for i, (num, title, desc) in enumerate(flow_steps):
    with flow_cols[i]:
        is_last = i == len(flow_steps) - 1
        bg = "var(--moss)" if is_last else "var(--paper-2)"
        text_color = "var(--paper)" if is_last else "var(--ink)"
        soft_color = "var(--paper)" if is_last else "var(--ink-soft)"
        st.markdown(
            f"""
            <div style="padding:24px 18px;background:{bg};border:1px solid var(--line);height:100%;color:{text_color};">
              <div style="font-family:JetBrains Mono,monospace;font-size:10px;color:{soft_color};letter-spacing:0.14em;margin-bottom:10px;">{num}</div>
              <div style="font-family:Fraunces,serif;font-size:22px;font-weight:400;letter-spacing:-0.01em;margin-bottom:6px;">{title}</div>
              <div style="font-size:12px;line-height:1.5;color:{soft_color};">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# ============== COUNTRY GRID ==============
eyebrow("The Atlas")
st.markdown("<h2 style='font-size:2.2rem;margin-bottom:32px;'>Eleven countries, <em>distinct policy textures.</em></h2>", unsafe_allow_html=True)

# Build a 3-column responsive grid
cols_per_row = 3
for row_start in range(0, len(COUNTRY_ORDER), cols_per_row):
    cols = st.columns(cols_per_row, gap="small")
    for j, iso in enumerate(COUNTRY_ORDER[row_start:row_start + cols_per_row]):
        with cols[j]:
            meta = COUNTRY_META[iso]
            yearly = country_yearly(iso)
            y23 = float(yearly[yearly["year"] == 2023]["ch4_tonnes"].iloc[0]) if 2023 in yearly["year"].values else 0
            y24 = float(yearly[yearly["year"] == 2024]["ch4_tonnes"].iloc[0]) if 2024 in yearly["year"].values else 0
            yoy = pct_change(y24, y23)
            n_loc = (all_countries_2024_total().query(f"iso3 == '{iso}'")["n_locations"].iloc[0])
            arrow = "↑" if yoy > 0.5 else ("↓" if yoy < -0.5 else "→")
            arrow_color = "var(--copper)" if yoy > 0.5 else ("var(--good)" if yoy < -0.5 else "var(--ink-soft)")

            st.markdown(
                f"""
                <div style="border:1px solid var(--line);padding:24px 22px;background:var(--paper);height:100%;">
                  <div style="font-family:JetBrains Mono,monospace;font-size:10px;color:var(--ink-soft);letter-spacing:0.16em;display:flex;justify-content:space-between;margin-bottom:14px;">
                    <span>{meta['region'].upper()}</span><span>ISO · {iso}</span>
                  </div>
                  <div style="font-family:Fraunces,serif;font-size:30px;font-weight:400;letter-spacing:-0.02em;line-height:1;margin-bottom:4px;">{meta['name']}</div>
                  <div style="font-family:Inter Tight,sans-serif;font-size:12px;color:var(--ink-soft);margin-bottom:18px;">Federal + {n_loc} {meta['subunit_type']}{'s' if n_loc > 1 else ''}</div>
                  <div style="display:flex;flex-direction:column;gap:6px;margin-bottom:14px;">
                    <div style="display:flex;justify-content:space-between;border-bottom:1px dotted var(--line-soft);padding-bottom:5px;font-size:12px;">
                      <span style="color:var(--ink-soft);font-family:JetBrains Mono,monospace;font-size:10px;letter-spacing:0.08em;text-transform:uppercase;">2024 total</span>
                      <span style="font-family:JetBrains Mono,monospace;font-weight:500;">{fmt_mt(y24)} Mt CH₄</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;border-bottom:1px dotted var(--line-soft);padding-bottom:5px;font-size:12px;">
                      <span style="color:var(--ink-soft);font-family:JetBrains Mono,monospace;font-size:10px;letter-spacing:0.08em;text-transform:uppercase;">YoY 23→24</span>
                      <span style="font-family:JetBrains Mono,monospace;font-weight:500;color:{arrow_color};">{arrow} {yoy:+.2f}%</span>
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            # Sparkline
            monthly = country_monthly(iso)
            st.plotly_chart(sparkline_plotly(monthly, height=50), use_container_width=True,
                            config={"displayModeBar": False})

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    '<div style="text-align:center;font-family:JetBrains Mono,monospace;font-size:10px;color:var(--ink-soft);letter-spacing:0.14em;text-transform:uppercase;padding:24px 0;border-top:1px solid var(--line);">'
    'smac prototype <span style="color:var(--copper);">✦</span> climate trace data · 2021–2024 <span style="color:var(--copper);">✦</span> ai responses are scripted · not for policy use'
    '</div>',
    unsafe_allow_html=True,
)
