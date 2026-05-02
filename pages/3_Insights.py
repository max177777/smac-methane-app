"""
Insights dashboard.
KPIs, time series with period filter, GWP comparison, top emitters, pathway table.
"""

import altair as alt
import pandas as pd
import streamlit as st

from utils.theme import inject_theme, eyebrow
from utils.data_loader import (
    COUNTRY_META, COUNTRY_ORDER, country_monthly,
    location_yearly_ranking, country_yearly,
    fmt_int, fmt_mt, pct_change,
)
from utils.policy_content import PATHWAYS, GWP100, GWP20
from utils.charts import time_series_plotly, INK, INK_SOFT, COPPER, MOSS, LINE_SOFT, PAPER


inject_theme()

# ============== HEADER ==============
col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    st.markdown("<h1>Insights <em>dashboard</em></h1>", unsafe_allow_html=True)
    st.markdown('<div class="smac-meta">monthly subnational methane · climate trace 2021–2024</div>',
                unsafe_allow_html=True)
with col_h2:
    if "dash_country" not in st.session_state:
        st.session_state.dash_country = "USA"
    selected = st.selectbox(
        "Country",
        options=COUNTRY_ORDER,
        index=COUNTRY_ORDER.index(st.session_state.dash_country),
        format_func=lambda x: f"{COUNTRY_META[x]['name']} ({x})",
        key="dash_country_select",
    )
    st.session_state.dash_country = selected

iso = st.session_state.dash_country
meta = COUNTRY_META[iso]

st.markdown("<br>", unsafe_allow_html=True)

# ============== KPIs ==============
yearly = country_yearly(iso)
y23 = float(yearly[yearly["year"] == 2023]["ch4_tonnes"].iloc[0]) if 2023 in yearly["year"].values else 0
y24 = float(yearly[yearly["year"] == 2024]["ch4_tonnes"].iloc[0]) if 2024 in yearly["year"].values else 0
yoy = pct_change(y24, y23)

ranking = location_yearly_ranking(iso, year=2024)
total = ranking["ch4_tonnes_year"].sum()
top1 = ranking.iloc[0]
top1_share = top1["share"]

kpi_cols = st.columns(4)
with kpi_cols[0]:
    st.metric("2024 Total CH₄", f"{fmt_mt(y24)} Mt",
              f"{yoy:+.2f}% YoY", delta_color="inverse" if yoy > 0 else "normal")
with kpi_cols[1]:
    st.metric("CO₂e · GWP100", f"{fmt_mt(y24 * GWP100)} Mt", f"×{GWP100} IPCC AR6", delta_color="off")
with kpi_cols[2]:
    st.metric("CO₂e · GWP20", f"{fmt_mt(y24 * GWP20)} Mt", f"×{GWP20} IPCC AR6", delta_color="off")
with kpi_cols[3]:
    st.metric("Top subunit share", f"{top1_share:.1f}%", str(top1["location"]), delta_color="off")

st.markdown("<br>", unsafe_allow_html=True)

# ============== TIME SERIES + GWP ==============
col_t, col_g = st.columns([1.3, 1], gap="large")

with col_t:
    eyebrow("National time series")
    st.markdown("<h3>Monthly CH₄ · tonnes · all subnational units</h3>", unsafe_allow_html=True)
    period = st.radio("Period", options=["All years", "2023–2024"],
                      horizontal=True, key=f"period_{iso}", label_visibility="collapsed")
    monthly = country_monthly(iso)
    if period == "2023–2024":
        monthly = monthly[monthly["year"] >= 2023]
    st.plotly_chart(time_series_plotly(monthly, height=320), use_container_width=True,
                    config={"displayModeBar": False})

with col_g:
    eyebrow("CH₄ vs CO₂e")
    st.markdown("<h3>IPCC AR6 · GWP100 vs GWP20 · 2024</h3>", unsafe_allow_html=True)
    top3 = ranking.head(3)
    st.markdown(
        "<div style='font-family:JetBrains Mono,monospace;font-size:10px;color:var(--ink-soft);"
        "letter-spacing:0.12em;text-transform:uppercase;margin-bottom:14px;'>top 3 subnational units</div>",
        unsafe_allow_html=True,
    )
    for r in top3.itertuples():
        v100 = r.ch4_tonnes_year * GWP100 / 1000
        v20 = r.ch4_tonnes_year * GWP20 / 1000
        st.markdown(
            f"""
            <div style="border-top:1px solid var(--line-soft);padding-top:14px;margin-bottom:14px;">
              <div style="font-family:Fraunces,serif;font-size:18px;margin-bottom:3px;">{r.location}</div>
              <div style="font-family:JetBrains Mono,monospace;font-size:10px;color:var(--ink-soft);letter-spacing:0.1em;margin-bottom:10px;">{fmt_int(r.ch4_tonnes_year)} t CH₄ → CO₂e</div>
              <div style="display:flex;gap:18px;align-items:baseline;">
                <div>
                  <div style="font-family:Fraunces,serif;font-size:28px;font-weight:300;letter-spacing:-0.02em;line-height:1;">{fmt_int(v100)}<span style="font-size:13px;color:var(--ink-soft);">k</span></div>
                  <div style="font-family:JetBrains Mono,monospace;font-size:9px;color:var(--ink-soft);letter-spacing:0.12em;text-transform:uppercase;margin-top:4px;">t · GWP100</div>
                </div>
                <div style="font-family:JetBrains Mono,monospace;color:var(--copper);font-size:14px;">→</div>
                <div>
                  <div style="font-family:Fraunces,serif;font-size:28px;font-weight:300;letter-spacing:-0.02em;line-height:1;color:var(--copper);">{fmt_int(v20)}<span style="font-size:13px;color:var(--ink-soft);">k</span></div>
                  <div style="font-family:JetBrains Mono,monospace;font-size:9px;color:var(--ink-soft);letter-spacing:0.12em;text-transform:uppercase;margin-top:4px;">t · GWP20</div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ============== TOP EMITTERS TABLE ==============
eyebrow("Top subnational emitters")
st.markdown("<h3>2024 ranking · share of national CH₄</h3>", unsafe_allow_html=True)

display_df = ranking.head(12).copy()
display_df = display_df[["location", "ch4_tonnes_year", "share", "yoy_pct"]].rename(columns={
    "location": meta["subunit_type"].title(),
    "ch4_tonnes_year": "2024 CH₄ (t)",
    "share": "Share (%)",
    "yoy_pct": "YoY 23→24 (%)",
})

st.dataframe(
    display_df,
    hide_index=True,
    use_container_width=True,
    column_config={
        meta["subunit_type"].title(): st.column_config.TextColumn(width="medium"),
        "2024 CH₄ (t)": st.column_config.NumberColumn(format="%d"),
        "Share (%)": st.column_config.ProgressColumn(
            format="%.2f%%", min_value=0,
            max_value=float(display_df["Share (%)"].max()),
        ),
        "YoY 23→24 (%)": st.column_config.NumberColumn(format="%+.2f%%"),
    },
    height=460,
)

st.markdown("<br>", unsafe_allow_html=True)

# ============== CROSS-COUNTRY COMPARISON ==============
eyebrow("Cross-country view")
st.markdown("<h3>2024 totals across the atlas</h3>", unsafe_allow_html=True)

# Build a cross-country dataframe
rows = []
for c in COUNTRY_ORDER:
    cy = country_yearly(c)
    y_now = float(cy[cy["year"] == 2024]["ch4_tonnes"].iloc[0]) if 2024 in cy["year"].values else 0
    y_prev = float(cy[cy["year"] == 2023]["ch4_tonnes"].iloc[0]) if 2023 in cy["year"].values else 0
    rows.append({
        "Country": COUNTRY_META[c]["name"],
        "iso": c,
        "ch4_mt": y_now / 1e6,
        "yoy": pct_change(y_now, y_prev),
    })
cross_df = pd.DataFrame(rows).sort_values("ch4_mt", ascending=False)

bar = alt.Chart(cross_df).mark_bar(height=22).encode(
    y=alt.Y("Country:N", sort="-x",
            axis=alt.Axis(title=None, labelFontSize=12, labelFont="Inter",
                          labelColor=INK)),
    x=alt.X("ch4_mt:Q",
            axis=alt.Axis(title="2024 CH₄ (Mt)", titleFontSize=10,
                          titleFont="JetBrains Mono", titleColor=INK_SOFT,
                          labelFontSize=10, labelFont="JetBrains Mono",
                          labelColor=INK_SOFT, gridColor=LINE_SOFT, gridDash=[2, 2])),
    color=alt.condition(
        f"datum.iso === '{iso}'",
        alt.value(COPPER),
        alt.value(MOSS),
    ),
    tooltip=[
        "Country",
        alt.Tooltip("ch4_mt", format=".2f", title="Mt CH₄"),
        alt.Tooltip("yoy", format="+.2f", title="YoY %"),
    ],
).properties(height=380, background=PAPER).configure_view(strokeWidth=0)

st.altair_chart(bar, use_container_width=True)

st.markdown(
    f"<div class='smac-meta' style='margin-top:-12px;'>highlighted: <strong style='color:var(--copper)'>{meta['name']}</strong></div>",
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# ============== PATHWAY TABLE ==============
eyebrow("Policy pathway recommendations")
st.markdown(f"<h3>Mitigation actions for {meta['name']} · with anti-greenwashing flags</h3>",
            unsafe_allow_html=True)

pathways = PATHWAYS.get(iso, [])

# Render as a nicer custom HTML table for the pathway content
table_html = """
<table style="width:100%;border-collapse:collapse;font-family:Inter Tight,sans-serif;border:1px solid var(--line);">
<thead>
<tr>
  <th style="font-family:JetBrains Mono,monospace;font-size:10px;letter-spacing:0.14em;text-transform:uppercase;color:var(--ink-soft);font-weight:500;text-align:left;padding:14px 16px;border-bottom:1.5px solid var(--ink);background:var(--paper-2);">Sector</th>
  <th style="font-family:JetBrains Mono,monospace;font-size:10px;letter-spacing:0.14em;text-transform:uppercase;color:var(--ink-soft);font-weight:500;text-align:left;padding:14px 16px;border-bottom:1.5px solid var(--ink);background:var(--paper-2);">Main issue</th>
  <th style="font-family:JetBrains Mono,monospace;font-size:10px;letter-spacing:0.14em;text-transform:uppercase;color:var(--ink-soft);font-weight:500;text-align:left;padding:14px 16px;border-bottom:1.5px solid var(--ink);background:var(--paper-2);">Mitigation actions</th>
  <th style="font-family:JetBrains Mono,monospace;font-size:10px;letter-spacing:0.14em;text-transform:uppercase;color:var(--ink-soft);font-weight:500;text-align:left;padding:14px 16px;border-bottom:1.5px solid var(--ink);background:var(--paper-2);">Greenwashing flag</th>
</tr>
</thead>
<tbody>
"""

for p in pathways:
    actions_html = "".join(
        f'<span style="font-family:JetBrains Mono,monospace;font-size:10px;padding:4px 9px;background:var(--paper-2);border:1px solid var(--line-soft);letter-spacing:0.04em;display:inline-block;margin:2px 4px 2px 0;">{a}</span>'
        for a in p["actions"]
    )
    table_html += f"""
    <tr>
      <td style="padding:18px 16px;border-bottom:1px solid var(--line-soft);vertical-align:top;font-family:Fraunces,serif;font-size:17px;font-weight:400;width:18%;">{p['sector']}</td>
      <td style="padding:18px 16px;border-bottom:1px solid var(--line-soft);vertical-align:top;font-size:13.5px;line-height:1.55;color:var(--ink-soft);width:24%;">{p['issue']}</td>
      <td style="padding:18px 16px;border-bottom:1px solid var(--line-soft);vertical-align:top;width:34%;">{actions_html}</td>
      <td style="padding:18px 16px;border-bottom:1px solid var(--line-soft);vertical-align:top;font-family:JetBrains Mono,monospace;font-size:11.5px;color:var(--copper);line-height:1.5;">⚠ {p['flag']}</td>
    </tr>
    """

table_html += "</tbody></table>"
st.markdown(table_html, unsafe_allow_html=True)
