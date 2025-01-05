import os
import streamlit as st

from core.scripts.utils import authenticate_id, TASK_INFO
from core.scripts import user_repository

st.session_state.page = "authentication_page"

def log_in(user_id: str, as_admin=False) -> None:
    """
    Log in a user.

    :param user_id: The ID of the user who requested the login.
    :param as_admin: Whether to log in as admin.
    """
    target_id = user_id
    if as_admin:
        target_id = "admin"

    user = user_repository.get_user(target_id)
    if not user:
        user_repository.create_user(target_id)
        user = user_repository.get_user(target_id)
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

def authenticate_user(user_id: str) -> bool:
    """
    Check if the given user id is valid and log in if so.

    :param user_id: ID of user to check
    :return: True if log in was successful, False if not
    """
    for task in TASK_INFO:
        if authenticate_id(task, user_id):
            return True
    return False
        

user_id = st.text_input("Enter the User ID you received:")
if user_id:
    # check if user id is the secret admin password
    if authenticate_admin(user_id):
        log_in(user_id, as_admin=True)
    elif authenticate_user(user_id):
        log_in(user_id)
    else:
        st.write("The entered ID does not exist. Please only enter the ID that was sent to you.")
        