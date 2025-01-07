import json
import streamlit as st

from core.scripts.utils import display_progress, read_json_from_file
from core.scripts import user_repository
from ambiguity_task.common import constants


def format_sentence(sentence):
    return sentence.replace("[", ":blue-background[")

def load_annotation(user_id: str, subtask: str, index: int) -> tuple:
    """
    Load one specific annotation from a user's saved data. 
    Useful for prefilling annotations the user already made when they look at previous samples.
    If the sample does not exist or is empty, all loaded values are None.

    :param user_id: id string of user to load from
    :param subtask: qualification or annotation
    :param index: the sample index to load
    :return: meaning1 checkbox (bool), meaning2 checkbox (bool), alt meaning (str), nonsensical checkbox (bool), comment (str)
    """
    empty_response = (None, None, "", None, "")
    user = user_repository.get_user(user_id)
    annotations = json.loads(user[5])
    if subtask not in annotations:
        return empty_response
    print(index, annotations[subtask])
    if len(annotations[subtask]) < index:
        return empty_response
    sample = annotations[subtask][index-1]
    return sample["meaning1"], sample["meaning2"], sample["other_label"], sample["nonsensical"], sample["comment"]
    

def print_annotation_schema(subtask: str, index: int) -> tuple:
    """
    Prints the annotation schema that is seen on the qualification and annotation page.

    :param subtask: qualification or annotation
    :param index: The number sample to show
    :return: The sentence and widget inputs in the order they are displayed to the user.
    """
    if subtask == "qualification":
        samples = read_json_from_file(constants.QUALIFICATION_QUESTIONS_PATH)
    else:
        samples = read_json_from_file(constants.SAMPLES_FILEPATH)

    # load values previously filled in checkboxes or None if this is first time annotating this sample
    value_checkbox1, value_checkbox2, value_textinput1, value_checkbox3, value_textinput2 = load_annotation(st.session_state.user_id, subtask, index)
    
    question = samples[str(index)]
    # display the "Sample 1/5" thing
    display_progress(key=subtask)

    st.markdown("\n**Read the following text**:  ")
    st.markdown(format_sentence(question["sentence"]) + "\n")
    st.markdown("Focus on the word :blue-background[" + question["word"] + "].\n")
    st.write("Which of these senses seem plausible?")
    checkbox1 = st.checkbox(key = 10 * index + 1, label=question["meaning1"], value=value_checkbox1)
    checkbox2 = st.checkbox(key = 10 * index + 2, label=question["meaning2"], value=value_checkbox2)
    text_input1 = st.text_input(key = 10 * index + 3, label = "(Only if you picked neither) Define a better label.", max_chars=200, value=value_textinput1)
    checkbox3 = st.checkbox(key = 10 * index + 4, label = "Check here if the sentence appears to be nonsensical.", value=value_checkbox3)
    st.write("\n\n")

    text_input2 = st.text_input(key = 10 * index + 8, label = "Comments (optional)", value=value_textinput2)

    if checkbox1 or checkbox2 or text_input1:
        next_input = st.button(key = 10 * index + 9, label="Next")
    else:
        next_input = None

    return question, checkbox1, checkbox2, text_input1, checkbox3, text_input2, next_input