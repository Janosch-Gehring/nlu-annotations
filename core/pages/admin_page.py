import streamlit as st

from core.scripts import database_repository

if "database" not in st.session_state:
    st.session_state.database = "Press the other button first"

st.write("# Welcome to the Admin Area.\n\nHere, you can manage annotations and users.")

st.write("Click on the button below for managing the database.")

if st.button(label="Click Here to Get Database File Before Downloading!"):
    st.session_state.database = database_repository.convert_database_to_json()
    st.rerun()
    st.write("OK!")

st.download_button(label="Then click here to download", data = st.session_state.database, file_name="database.json")

