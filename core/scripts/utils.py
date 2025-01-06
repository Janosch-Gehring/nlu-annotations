import json
import random
import string
import sqlite3

import streamlit as st

from core.scripts import user_repository

TASK_INFO = {
    "ambiguity_task": {
        "annotation_filepath": "ambiguity_task/resources/pilot_samples.json",
        "qualification_filepath": "ambiguity_task/resources/qualification_questions.json"
    }
}

def read_json_from_file(path: str) -> dict:
    """
    Read a Json-file into a dict from a path.
    :param path: String filepath

    :return: dictionary object
    """
    # TODO Error handling
    with open(path, "r") as f:
        return json.loads(f.read())
    
def generate_random_string(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def authenticate_id(task: str, user_id: id):
    """
    Check if the user id trying to log in for a specific task is valid.
    TODO make it task dependent
    """
    conn = sqlite3.connect('database.db')
    # Check if the user_id exists in the table
    cursor = conn.execute('''
        SELECT 1 FROM valid_ids WHERE user_id = ?
    ''', (user_id,))
    result = cursor.fetchone()

    conn.close()
    
    if result:
        return True
    return False


def get_amount_of_samples_for_group(task: str, group: int) -> int:
    """
    Find the amount of samples a member of a specific group has to do.

    :param task: str, e.g. ambiguity_task
    :param group: integer group index
    :return: int
    """
    if task == "qualification":
        samples = read_json_from_file(TASK_INFO["ambiguity_task"]["qualification_filepath"])
    else:
        samples = read_json_from_file(TASK_INFO["ambiguity_task"]["annotation_filepath"])
    number_of_samples = len([x for x in samples if ("grouping" not in samples[x]) or (samples[x]["grouping"] == group)])
    return number_of_samples



def display_progress(key="annotation", user_id=None, print_progress: bool = True) -> str:
    """
    Returns the progress x/y ("x out of y") for a user on a subtask.

    :param key: The subtask, e.g. annotation or qualification
    :param user_id: Id of user to check, if None, display logged in user's progress
    :param print_progress: Whether to print the progress immediately instead of just returning the string
    :return: str
    """
    if not user_id:
        user_id = st.session_state.user_id

    user = user_repository.get_user(user_id)
    user_group = user[3]
    max_samples = get_amount_of_samples_for_group(key, user_group)

    if not user:
        return "NOT STARTED"

    # TODO show progress even when all annotations are finished (when revising annotations)
    
    # handle case that there are no annotations
    annotations = json.loads(user[5])
    if key not in annotations:
        if print_progress:
            st.write("Sample 1")
        return "Annotation not started"
    annotations = annotations[key]


    count_finished = 0
    for annotation in annotations:
        if annotation:  # "unfinished" annotations will be empty
            count_finished += 1
    if print_progress:
        st.write("Sample " + str(count_finished+1) + "/" + str(max_samples))
    return str(count_finished+1) + "/" + str(max_samples)