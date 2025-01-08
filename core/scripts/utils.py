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
    },
    "example_task": {
        "annotation_filepath": "example_task/resources/samples.json",
        "qualification_filepath": "example_task/resources/qualification_samples.json"
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
    """
    conn = sqlite3.connect('database.db')
    # Check if the user_id exists in the table
    cursor = conn.execute('''
        SELECT 1 FROM valid_ids WHERE user_id = ?
                          AND task = ?
    ''', (user_id, task))
    result = cursor.fetchone()

    conn.close()
    
    if result:
        return True
    return False


def get_amount_of_samples_for_group(key: str, task: str, group: int) -> int:
    """
    Find the amount of samples a member of a specific group has to do.

    :param task: str, e.g. ambiguity_task
    :param group: integer group index
    :return: int
    """
    if key == "qualification":
        samples = read_json_from_file(TASK_INFO[task]["qualification_filepath"])
    else:
        samples = read_json_from_file(TASK_INFO[task]["annotation_filepath"])
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
    task = user[1]
    max_samples = get_amount_of_samples_for_group(key, task, user_group)

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
        st.write("Finished Samples: " + str(count_finished) + "/" + str(max_samples))
    return str(count_finished) + "/" + str(max_samples)

def load_annotation(user_id: str, subtask: str, index: int) -> tuple:
    """
    Load one specific annotation from a user's saved data. 
    Useful for prefilling annotations the user already made when they look at previous samples.
    If the sample does not exist or is empty, all loaded values are None.

    :param user_id: id string of user to load from
    :param subtask: qualification or annotation
    :param index: the sample index to load
    :return: loaded sample
    """
    user = user_repository.get_user(user_id)
    annotations = json.loads(user[5])
    if subtask not in annotations:
        return None
    print(index, annotations[subtask])
    if len(annotations[subtask]) < index:
        return None
    return annotations[subtask][index-1]

def finish_annotation():
    st.write("You finished the annotation!")
    user_repository.mark_as_done(st.session_state.user_id)
    st.rerun()
    st.write("Thank you for submitting your annotations.")

def handle_next_button(annotation: dict, amount_of_samples: int):
    """
    Behaviour of the next button: Saves annotation, increases the progress, calls finish_annotation if amount of samples is reached.

    :param annotation: annotation of the current sample.
    :param amount_of_samples: the last sample index (for all groups)
    """
    user_repository.save_one_annotation(st.session_state.user_id, "annotation", st.session_state.progress, annotation)
    if st.session_state.progress < amount_of_samples:
        st.session_state.progress += 1
        st.rerun()
    else:
        finish_annotation()
    
def find_next_valid_sample(samples: dict, index: int):
    """
    Displays the next - or previous, if st.session_state.progression_direction=-1 - sample in the annotation.
    This skips samples irrelevant to the grouping of the current user.
    If there is no next sample, finish the annotation (mark user as done).
    If there is no previous sample, print Already at first sample! And do nothing.
    Reverse progression direction back to normal if set to -1 and rerun.

    :param samples: dict of samples
    :param index: current index
    """
    while True:
        question = samples[str(index)]
        grouping = user_repository.get_user(st.session_state.user_id)[3]
        print(index, st.session_state.progression_direction)
        if grouping != question["grouping"]:
            st.session_state.progress = int(st.session_state.progress) + st.session_state.progression_direction 
            index = index + st.session_state.progression_direction
            if index >= len(samples):
                finish_annotation()
            elif index < 1:
                st.write("Already at first sample!")
                index = 1
                st.session_state.progress = 1
                st.session_state.progression_direction = 1  # go forwards again until first grouping-relevant sample is reached
            st.rerun()
        else:
            break


    if st.session_state.progression_direction == -1:
        # if user pressed on back button: now that previous sample has been found, return default to forward
        st.session_state.progression_direction = 1
        st.rerun()