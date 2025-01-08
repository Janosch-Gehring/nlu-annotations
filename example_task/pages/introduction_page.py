import streamlit as st

st.session_state.page = "example_task_introduction_page"

with open("example_task/resources/intro_text.md", "r") as f:
    intro_text = f.read()

st.markdown(intro_text)