import streamlit as st

from core.utils import authenticate_id
from core.scripts import user_repository

st.session_state.page = "ambiguity_task_authentication_page"

user_id = st.text_input("Enter the User ID you received:")
if user_id:
    # show error message if user id is not in the list of valid ids
    if not authenticate_id("ambiguity_task", user_id):
        st.write("This is not a valid ID.")
    else:
        user = user_repository.get_user(user_id)
        if not user:
            user_repository.create_user(user_id)
            user = user_repository.get_user(user_id)

        st.write("Welcome!")
        st.session_state.user_id = user_id
        user_repository.fetch_user_data()
        st.rerun()
    