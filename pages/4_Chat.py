"""
Chat page. Dual mode:
  - Methane Specialist: data-grounded, structured 5-block response, sidebar with country/sub/metric/output
  - General Assistant: scripted conversational, no sidebar
"""

import streamlit as st

from utils.theme import inject_theme
from utils.data_loader import (
    COUNTRY_META, COUNTRY_ORDER, list_locations, country_yearly, fmt_mt,
)
from utils.policy_content import POLICY
from utils.chat_engine import (
    MethaneContext, build_methane_response, build_general_response, ChatBlock,
)
from utils.charts import time_series_plotly


inject_theme()


# ============== STATE ==============
if "chat_mode" not in st.session_state:
    st.session_state.chat_mode = "methane"  # "methane" | "general"
if "chat_country" not in st.session_state:
    st.session_state.chat_country = "USA"
if "chat_location" not in st.session_state:
    st.session_state.chat_location = "__all__"
if "chat_metric" not in st.session_state:
    st.session_state.chat_metric = "ch4"
if "chat_output" not in st.session_state:
    st.session_state.chat_output = "data"
if "messages_methane" not in st.session_state:
    st.session_state.messages_methane = [
        {"role": "assistant",
         "type": "welcome",
         "content": (
             "I am the SMAC methane specialist. I read your sidebar selections (country, "
             "subunit, metric, output type) and answer with structured reasoning grounded in "
             "real Climate TRACE data.\n\nUse the chips below or ask freely. Switch to "
             "**General Assistant** at the top for off-topic conversation."
         )}
    ]
if "messages_general" not in st.session_state:
    st.session_state.messages_general = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# ============== MODE TABS ==============
mode_col1, mode_col2, _ = st.columns([1, 1, 2])
with mode_col1:
    if st.button("◉ Methane Specialist",
                 type="primary" if st.session_state.chat_mode == "methane" else "secondary",
                 use_container_width=True):
        st.session_state.chat_mode = "methane"
        st.rerun()
with mode_col2:
    if st.button("◉ General Assistant",
                 type="primary" if st.session_state.chat_mode == "general" else "secondary",
                 use_container_width=True):
        st.session_state.chat_mode = "general"
        st.rerun()

st.markdown(
    '<div style="border-bottom:1px solid var(--line);margin-bottom:18px;"></div>',
    unsafe_allow_html=True,
)


# ============== METHANE SIDEBAR ==============
def methane_sidebar():
    with st.sidebar:
        st.markdown(
            '<div class="smac-eyebrow">Country</div>',
            unsafe_allow_html=True,
        )
        country = st.selectbox(
            "country_select",
            options=COUNTRY_ORDER,
            index=COUNTRY_ORDER.index(st.session_state.chat_country),
            format_func=lambda x: COUNTRY_META[x]["name"],
            label_visibility="collapsed",
            key="sb_country",
        )
        if country != st.session_state.chat_country:
            st.session_state.chat_country = country
            st.session_state.chat_location = "__all__"
            st.rerun()

        # Show country quick stat
        cy = country_yearly(country)
        y24 = float(cy[cy["year"] == 2024]["ch4_tonnes"].iloc[0]) if 2024 in cy["year"].values else 0
        st.markdown(
            f"<div class='smac-meta' style='margin:-8px 0 18px;font-size:10px;'>"
            f"{fmt_mt(y24)} Mt CH₄ in 2024 · {COUNTRY_META[country]['subunit_type']}s</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="smac-eyebrow">Subnational unit</div>',
            unsafe_allow_html=True,
        )
        locations = list_locations(country)
        location_options = ["__all__"] + locations[:30]
        loc = st.selectbox(
            "location_select",
            options=location_options,
            index=location_options.index(st.session_state.chat_location)
                  if st.session_state.chat_location in location_options else 0,
            format_func=lambda x: f"All {COUNTRY_META[country]['subunit_type']}s (national aggregate)" if x == "__all__" else x,
            label_visibility="collapsed",
            key="sb_location",
        )
        if loc != st.session_state.chat_location:
            st.session_state.chat_location = loc
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<div class="smac-eyebrow">Metric</div>',
            unsafe_allow_html=True,
        )
        metric_options = {
            "ch4": "CH₄ emissions",
            "gwp100": "CO₂e · GWP100 (×27)",
            "gwp20": "CO₂e · GWP20 (×80)",
        }
        metric = st.radio(
            "metric_select",
            options=list(metric_options.keys()),
            format_func=lambda x: metric_options[x],
            index=list(metric_options.keys()).index(st.session_state.chat_metric),
            label_visibility="collapsed",
            key="sb_metric",
        )
        if metric != st.session_state.chat_metric:
            st.session_state.chat_metric = metric
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<div class="smac-eyebrow">Output type</div>',
            unsafe_allow_html=True,
        )
        output_options = {
            "data": "Data summary",
            "trend": "Trend analysis",
            "policy": "Policy analysis",
            "pathway": "Mitigation pathway",
            "method": "Method explanation",
        }
        output = st.radio(
            "output_select",
            options=list(output_options.keys()),
            format_func=lambda x: output_options[x],
            index=list(output_options.keys()).index(st.session_state.chat_output),
            label_visibility="collapsed",
            key="sb_output",
        )
        if output != st.session_state.chat_output:
            st.session_state.chat_output = output
            st.rerun()

        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Reset conversation", use_container_width=True):
            st.session_state.messages_methane = st.session_state.messages_methane[:1]  # keep welcome
            st.rerun()


if st.session_state.chat_mode == "methane":
    methane_sidebar()


# ============== CONTEXT BAR / HEADER ==============
if st.session_state.chat_mode == "methane":
    country_name = COUNTRY_META[st.session_state.chat_country]["name"]
    subunit_type = COUNTRY_META[st.session_state.chat_country]["subunit_type"]
    loc_label = f"all {subunit_type}s" if st.session_state.chat_location == "__all__" else st.session_state.chat_location
    metric_label = {"ch4": "CH₄ emissions", "gwp100": "CO₂e · GWP100", "gwp20": "CO₂e · GWP20"}[st.session_state.chat_metric]
    output_label = {"data": "Data summary", "trend": "Trend analysis", "policy": "Policy analysis",
                    "pathway": "Mitigation pathway", "method": "Method explanation"}[st.session_state.chat_output]

    st.markdown(
        f"""
        <div style="display:flex;justify-content:space-between;align-items:center;padding:12px 0;margin-bottom:8px;">
          <div class="smac-meta" style="font-size:11px;">
            context: <strong style="color:var(--ink);">{country_name}</strong>
            <span style="color:var(--copper);margin:0 8px;">/</span>
            <strong style="color:var(--ink);">{loc_label}</strong>
            <span style="color:var(--copper);margin:0 8px;">/</span>
            <strong style="color:var(--ink);">{metric_label}</strong>
            <span style="color:var(--copper);margin:0 8px;">/</span>
            <strong style="color:var(--ink);">{output_label}</strong>
          </div>
          <div class="smac-meta" style="font-size:10px;">
            <span style="display:inline-block;width:6px;height:6px;background:var(--good);border-radius:50%;margin-right:6px;"></span>
            methane specialist · grounded in real data
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div style="display:flex;justify-content:space-between;align-items:center;padding:12px 0;margin-bottom:8px;">
          <div class="smac-meta" style="font-size:11px;">
            <strong style="color:var(--ink);">General Assistant</strong>
            <span style="color:var(--copper);margin:0 8px;">·</span>
            open conversation, no data binding
          </div>
          <div class="smac-meta" style="font-size:10px;">
            <span style="display:inline-block;width:6px;height:6px;background:var(--good);border-radius:50%;margin-right:6px;"></span>
            general · scripted response
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============== HELPERS TO RENDER MESSAGES ==============
def render_methane_message(msg: dict):
    """Render an assistant methane message (structured) or user message."""
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
        return

    with st.chat_message("assistant"):
        if msg.get("type") == "welcome":
            st.markdown(msg["content"])
            return
        # structured blocks
        for block in msg["blocks"]:
            label_html = (
                f'<div class="smac-struct-label">{block.label}</div>'
            )
            st.markdown(label_html, unsafe_allow_html=True)
            if block.is_method:
                st.markdown(
                    f'<div class="smac-method-block">{block.content}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(block.content)

        # inline mini chart
        if msg.get("chart_df") is not None:
            st.markdown(
                f'<div class="smac-meta" style="margin-top:14px;font-size:10px;">'
                f'{msg["chart_subject"]} · monthly CH₄ tonnes · 2021–2024</div>',
                unsafe_allow_html=True,
            )
            st.plotly_chart(
                time_series_plotly(msg["chart_df"], height=220),
                use_container_width=True,
                config={"displayModeBar": False},
                key=f"chart_{msg.get('id')}",
            )


def render_general_message(msg: dict):
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])


# ============== EMPTY STATE FOR GENERAL ==============
def render_general_empty():
    st.markdown(
        """
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
                    text-align:center;padding:60px 20px 30px;">
          <div style="width:64px;height:64px;border:1.5px solid var(--ink);border-radius:50%;
                      display:grid;place-items:center;font-family:Fraunces,serif;font-size:22px;
                      background:var(--moss);color:var(--paper);margin-bottom:24px;">G</div>
          <h2 style="font-size:2rem;margin-bottom:14px;">General <em>assistant</em></h2>
          <p style="font-family:Fraunces,serif;font-size:16px;line-height:1.5;color:var(--ink-soft);
                    max-width:520px;font-weight:300;margin-bottom:20px;">
            I'm a general-purpose chat. Same SMAC interface, no data sidebar, no required topic.
            Ask anything — I'll give a normal conversational answer.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============== SUGGESTED CHIPS ==============
def methane_chips():
    if st.session_state.chat_location != "__all__":
        loc = st.session_state.chat_location
        return [
            f"Show {loc}'s methane trend",
            f"Why is {loc} so high?",
            f"What policy fits {loc}?",
            f"Compare {loc} vs national",
        ]
    country_name = COUNTRY_META[st.session_state.chat_country]["name"]
    return [
        f"Top emitters in {country_name}",
        f"{country_name} 2021 to 2024 trend",
        f"How does GWP20 change {country_name}?",
        f"What policies should {country_name} prioritise?",
    ]


def general_chips():
    return [
        "What is climate change in one paragraph?",
        "Help me write an email asking for a meeting",
        "Give me three ideas for a weekend in Los Angeles",
        "Explain how a methane molecule warms the atmosphere",
    ]


# ============== RENDER MESSAGES ==============
mode = st.session_state.chat_mode
messages = (st.session_state.messages_methane if mode == "methane"
            else st.session_state.messages_general)

if mode == "general" and not messages:
    render_general_empty()
else:
    for m in messages:
        if mode == "methane":
            render_methane_message(m)
        else:
            render_general_message(m)


# ============== SUGGESTION CHIPS BUTTONS ==============
chip_list = methane_chips() if mode == "methane" else general_chips()
st.markdown("<br>", unsafe_allow_html=True)
chip_cols = st.columns(len(chip_list))
for i, q in enumerate(chip_list):
    with chip_cols[i]:
        if st.button(q, key=f"chip_{mode}_{i}_{hash(q)}", use_container_width=True):
            st.session_state.pending_question = q
            st.rerun()


# ============== CHAT INPUT ==============
user_input = st.chat_input(
    "Ask about emissions, policy, or mitigation pathways…"
    if mode == "methane"
    else "Ask anything — climate, policy, definitions, or just chat…"
)

# Resolve any pending input
final_input = user_input or st.session_state.pending_question
if final_input:
    st.session_state.pending_question = None

    if mode == "methane":
        # append user
        st.session_state.messages_methane.append({"role": "user", "content": final_input})
        # build response
        ctx = MethaneContext(
            iso=st.session_state.chat_country,
            location=st.session_state.chat_location,
            metric=st.session_state.chat_metric,
            output=st.session_state.chat_output,
        )
        resp = build_methane_response(final_input, ctx)
        st.session_state.messages_methane.append({
            "role": "assistant",
            "type": "structured",
            "blocks": resp.blocks,
            "chart_df": resp.chart_df,
            "chart_subject": resp.chart_subject,
            "id": len(st.session_state.messages_methane),
        })
    else:
        st.session_state.messages_general.append({"role": "user", "content": final_input})
        reply = build_general_response(final_input)
        st.session_state.messages_general.append({"role": "assistant", "content": reply})

    st.rerun()
