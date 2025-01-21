import streamlit as st

# logout serves basically no function to the user since they can just refresh the page
# but at least they can close the db connection for us if they want to :) otherwise automatic disconnect after 1 hour

st.session_state.user_id = ""
st.session_state.user = []
st.session_state.conn.close()
st.rerun()