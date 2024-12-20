import streamlit as st

with open("ambiguity_task/resources/intro_text.md", "r") as f:
    intro_text = f.read()

st.markdown(intro_text)