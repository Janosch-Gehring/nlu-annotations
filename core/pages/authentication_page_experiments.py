import json
import os

import streamlit as st

from core.scripts.utils import authenticate_id, TASK_INFO
from core.scripts import user_repository, database_repository
import random
import time

st.session_state.page = "authentication_page"

if st.session_state.conn.closed:
    # upon logout, connection will be closed until revisiting the authentication page
    st.session_state.conn = database_repository.db_connection()

def log_in(user_id: str, task=None, as_admin=False) -> None:
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
        with st.container():
            st.html("<h1>Welcome to this Experiment!")
            st.html("""<h2>This is the informed consent form for the experiment. Please read it carefully before continuing.
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                    Morbi faucibus, magna non egestas varius, ante mi hendrerit tortor, non volutpat dolor risus id eros. 
                    Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; 
                    Pellentesque pharetra luctus felis blandit feugiat. Pellentesque rhoncus bibendum rhoncus. 
                    Nam luctus velit ante, nec laoreet ipsum porta eget. Suspendisse potenti. Ut maximus malesuada quam ac euismod.
                    Pellentesque imperdiet, elit ac rutrum efficitur, urna ipsum molestie lorem, sit amet consectetur risus nulla at diam. 
                    Pellentesque in purus ut erat egestas dapibus ac eget erat.
                    
                    <h2>Suspendisse sed neque lorem. Quisque a felis sit amet turpis semper efficitur. 
                    <p>Cras lacinia eget sapien vel malesuada. 
                    Praesent pretium rhoncus justo, sit amet viverra nulla tempus id. 
                    Proin nec posuere dolor. Phasellus fermentum vel arcu eu sagittis. 
                    Donec egestas vitae justo et sodales. Mauris non ipsum leo. Suspendisse potenti. 
                    Praesent at bibendum purus, quis auctor nunc. Nunc nisi tortor, varius volutpat efficitur ut, 
                    ullamcorper a mi. Ut felis nunc, blandit sagittis tellus sit amet, sagittis tristique justo. 
                    Suspendisse potenti.
                    
                    <p>Please enter your prolific ID below:""")

            prolific_id = st.text_input("Prolific ID:", max_chars=200)
        if prolific_id:
            user_repository.create_user(target_id, task=task, data={"prolific_id": prolific_id})
            user = user_repository.get_user(target_id)
        else:
            return
    st.session_state.user_id = target_id
    st.session_state.user = list(user)
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
    for task in TASK_INFO:
        if authenticate_id(task, user_id):
            return task
        
with st.empty():
    user_id = st.text_input("Please enter the 8-digit User ID (password) you received:", max_chars=100)
    if user_id:
        # check if user id is the secret admin password
        if authenticate_admin(user_id):
            log_in(user_id, as_admin=True)
        elif task := authenticate_user(user_id):
            log_in(user_id, task=task)
        else:
            st.write("The entered ID does not exist. Please only enter the 8 digit password (not name!) that was sent to you on Prolific.")

if not user_id:
    st.markdown("""\n\n## Where is my ID?

Prolific likely opened this website in a new window. If you go back to the Prolific window, you will see your credentials: a username and a password. The username is not that important. Simply use the password directly to log in.
    """)