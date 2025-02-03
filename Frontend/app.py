import streamlit as st

start = st.Page("pages/start_page.py", title="Main Page", default=True)
personality_test = st.Page("pages/personality_test.py", title="Personality Test")
other = st.Page("pages/other.py", title="Other")

pg = st.navigation(
    {
        "Apps": [start, personality_test, other]
    }
)



pg.run()