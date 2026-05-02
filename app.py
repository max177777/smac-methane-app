"""
SMAC — Subnational Methane Atlas & Chat
Main entry point. Uses st.navigation for proper multi-page routing.

Run with:
    streamlit run app.py
"""

import streamlit as st


st.set_page_config(
    page_title="SMAC · Subnational Methane Atlas & Chat",
    page_icon="🌫",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "About": "SMAC is a prototype methane decision-support tool. Climate TRACE data 2021-2024.",
    },
)

overview = st.Page("pages/1_Overview.py", title="Overview", default=True)
atlas = st.Page("pages/2_Atlas.py", title="Atlas")
insights = st.Page("pages/3_Insights.py", title="Insights")
chat = st.Page("pages/4_Chat.py", title="Chat")

pg = st.navigation([overview, atlas, insights, chat], position="top")
pg.run()
