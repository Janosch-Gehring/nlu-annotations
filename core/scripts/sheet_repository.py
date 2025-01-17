import json
import os

import streamlit as st
import gspread

def open_google_sheet():
    gc = gspread.service_account(filename=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    return gc.open_by_key("1eeT2uL68DNeUTVSC9vfODpe6PRfgYlfXHwZE53ViL18")

# Check if user exists in the database
def get_user(user_id: str):
    """
    Get a user from any task by user id.
    Returns None if no user found.

    :param user_id: ID-string of user
    :return: User or None
    """
    sh = st.session_state.sheet
    user_sheet = sh.worksheet("valid_ids")
    user_cell = user_sheet.find(user_id)
    if not user_cell:
        return None
    user_row = user_sheet.row_values(user_cell.row)
    user = {"user_id": user_id,
            "task": user_row[1],
            "qualified": user_row[2],
            "annotator_group": user_row[3],
            "progress": user_row[4],
            "data": user_row[5]}
    return user

def create_user(user_id: str, task: str = "ambiguity_task", grouping=0):
    """
    Creates a user with the specified user id.
    The newly created user is not assigned any values at this point.

    :user_id: ID-string of user
    :return: None
    """
    sh = st.session_state.sheet
    user_sheet = sh.worksheet("valid_ids")
    next_free_row = len(user_sheet.col_values(1)) + 1

    user_sheet.update(f"A{next_free_row}:F{next_free_row}", [user_id, task, 0, grouping, 0, {}])
    st.session_state.sheet = sh


def authenticate_id(user_id: id):
    """
    Check if the user id trying to log in is valid.

    :param user_id: id string of user
    :param task: Task
    """
    sh = st.session_state.sheet
    user_sheet = sh.worksheet("valid_ids")
    
    if user_cell := user_sheet.find(user_id):
        return True
    return False

def save_one_annotation(user_id: str, subtask: str, question_index: int, question_annotation: dict):
    """
    Save one annotation for a sample to the database.
    
    :param user_id:
    :param subtask: The subcategory of sample, e.g. qualification or annotation
    :param question_index: At what index to save the annotation, e.g. 3 for the 3rd sample
    :param question_annotation: The annotation to save, which is a dict.
    """
    sh = open_google_sheet()
    sheet = sh.worksheet(subtask)
    user_cell = sheet.find(user_id).row
    sheet.update_cell(user_cell.row, 1 + question_index, json.dumps(question_annotation))

def get_qualification(user_id: int) -> int:
    """
    Check if the user with the given id passed a qualification test.

    :param user_id: id-string of user
    :return: -1 if failed, 0 if no qualification, 1 if passed
    """
    user = get_user(user_id)
    return user["qualified"]

def get_checkpoint(subtask, print=True) -> int:
    """
    Find the last annotation that was being worked on for the given subtask (e.g. "qualification").
    Assumes that the samples are sorted. Return the highest index.
    """
    sh = open_google_sheet()
    sheet = sh.worksheet(subtask)
    user_row = sheet.find(st.session_state.user_id).row
    if print:
        st.write("Returning to checkpoint from previous session.")
    return len(user_row) - 1

def reset_annotation(user_id: str, subtask: str):
    """
    Reset the user's annotation given a subtask key (like qualification or annotation)
    
    :param user_id:
    :param subtask: The key of the annotation data to delete, e.g. qualification
    """
    st.write("not implemented yet with google sheets")
    return
    sh = open_google_sheet()
    sheet = sh.worksheet(subtask)
    user_cell = sheet.find(user_id)
    annotation_width = len(sheet.row_values(user_cell.row))
    
def mark_as_done(user_id):
    sh = open_google_sheet()
    sheet = sh.worksheet("valid_ids")
    user_cell = sheet.find(user_id)
    sheet.update_cell(user_cell.row, 5, "-1")
    print("User ", user_id, " finished annotation!")

def check_if_done(user_id):
    sh = open_google_sheet()
    sheet = sh.worksheet("valid_ids")
    user_cell = sheet.find(user_id)
    if sheet.cell(user_cell.row, 5) == -1:
        return True
    return False