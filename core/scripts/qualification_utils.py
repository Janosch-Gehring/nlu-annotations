import json
import streamlit as st

from core.scripts.utils import read_json_from_file
from core.scripts import user_repository      


def finish_qualification(qualification_function: str):
    """
    Finish the current user's qualification and judge if they are qualified.
    Sets their qualification accordingly.
    
    :param qualification_function: function that returns True/False based on the user's annotations.
    """
    # if this is the last question, check for qualification
    user = user_repository.get_user(st.session_state.user_id)
    annotations = json.loads(user[5])
    # check if the qualification was successful and set user state accordingly
    if qualification_function(annotations):
        st.write("Congrats, you're qualified!")
        user_repository.set_qualification(st.session_state.user_id)
        st.rerun()
    else:
        st.write("Oops, you failed the qualification.")
        user_repository.set_qualification(st.session_state.user_id, setting=-1)
        user_repository.reset_annotation(st.session_state.user_id, key="qualification")
        st.rerun()

    # reset progress to beginning (important in case an admin decides to reset qualification)
    st.session_state.qualification_progress = 1

def advance_qualification(qualification_questions_path: str, qualification_function):
    """
    Advance the qualification to the next sample. Also finishes it if it is done.
    Logic function should link to a function that dictates whether the qualification was succesful.
    st.session_state.qualification_progress has to be set before calling the function.

    :param qualification_questions_path: str filepath
    :param logic_function: a function that takes dict (annotation) as argument and returns bool (true = passed)
    """
    qualification_questions = read_json_from_file(qualification_questions_path)
    if st.session_state.qualification_progress < len(qualification_questions):
        # there are more questions, so advance to next one
        st.session_state.qualification_progress += 1
        st.rerun()
    else:
        # if this is the last question, finish qualification
        finish_qualification(qualification_function)