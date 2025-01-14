import streamlit as st

st.session_state.cookies["logged_in_user"] = ""
st.session_state.user_id = ""
st.rerun()