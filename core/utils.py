import json

import streamlit as st

from core.scripts import user_repository

def read_json_from_file(path: str) -> dict:
    """
    Read a Json-file into a dict from a path.
    :param path: String filepath

    :return: dictionary object
    """
    # TODO Error handling
    with open(path, "r") as f:
        return json.loads(f.read())
    

def authenticate_id(task: str, user_id: id):
    """
    Check if the user id trying to log in for a specific task is valid.
    It does by checking the list under <taskname>/resources/user_ids.csv

    :param task: task name as it is in the folder's name, e.g. ambiguity_task
    :param user_id: the checked user id
    """
    with open(task + "/resources/user_ids.csv", "r") as f:
        users = f.readlines()
    users = [user.strip() for user in users]
    return user_id in users

def display_progress(max_samples: int, key="annotation"):
    """
    Displays the progress (x/y) for a user on a subtask.

    :param max_samples: The amount of samples that have to be annotated in total.
    :param key: The subtask, e.g. annotation or qualification
    :return: None, prints progress directly to the user.
    """
    user = user_repository.get_user(st.session_state.user_id)

    # TODO show progress even when all annotations are finished, for now just hide the bugged progress display
    
    annotations = json.loads(user[5])
    if key not in annotations:
        st.write("Sample 1" + "/" + str(max_samples))
        return
    annotations = annotations[key]

    count_finished = 0
    for annotation in annotations:
        if annotation:  # "unfinished" annotations will be empty
            count_finished += 1
    st.write("Sample " + str(count_finished+1) + "/" + str(max_samples))