import os

import streamlit as st

from core.scripts import sheet_repository
from core.scripts.sheet_repository import authenticate_id

st.session_state.page = "authentication_page"

def log_in(user_id: str, task=None, as_admin=False) -> None:
    """
    Log in a user. Authentication check has to be called before this function.

    :param user_id: The ID of the user who requested the login.
    :param as_admin: Whether to log in as admin.
    """
    target_id = user_id
    if as_admin:
        target_id = "admin"

    user = sheet_repository.get_user(target_id)
    if not user:
        sheet_repository.create_user(target_id, task=task)
        user = sheet_repository.get_user(target_id)
    st.session_state.user = user
    st.session_state.user_id = target_id
    st.write("Welcome!")
    st.rerun()

def authenticate_admin(user_id: str) -> bool:
    """
    Check if the given user id is an admin and log in if so.

    :param user_id: ID of user to check
    :return: True if log in successful, False if not
    """
    return user_id == os.getenv("ADMIN_PASSWORD")

def authenticate_user(user_id: str) -> str:
    """
    Check if the given user id is valid and log in if so.

    :param user_id: ID of user to check
    :return: Task name if log in was successful, None if not
    """
    if authenticate_id(user_id):
        return True
        

user_id = st.text_input("Enter the User ID you received:")
if user_id:
    # check if user id is the secret admin password
    if authenticate_admin(user_id):
        log_in(user_id, as_admin=True)
    elif task := authenticate_user(user_id):
        log_in(user_id, task=task)
    else:
        st.write("The entered ID does not exist. Please only enter the ID that was sent to you.")
        