import streamlit as st

from core.scripts.utils import read_json_from_file, TASK_INFO, display_progress, load_annotation


def check_if_qualified(annotations: dict):
    """
    Checks if the user's annotations are enough to pass the qualification test.

    :param annotations: User annotations, should have a 'qualification' key.
    """
    qualification_questions = read_json_from_file(TASK_INFO["example_task"]["qualification_filepath"])

    needed_score = 2
    score = 0
    for question_id in qualification_questions:
        if qualification_questions[question_id]["correct_answer"] == annotations["qualification"][int(question_id)-1]["checkbox"]:
            score += 1
    return score >= needed_score

def print_annotation_schema(subtask: str, index: int) -> tuple:
    """
    Prints the annotation schema that is seen on the qualification and annotation page.

    :param subtask: qualification or annotation
    :param index: The number sample to show
    :return: The sentence and widget inputs in the order they are displayed to the user.
    """
    if subtask == "qualification":
        samples = read_json_from_file(TASK_INFO["example_task"]["qualification_filepath"])
    else:
        samples = read_json_from_file(TASK_INFO["example_task"]["annotation_filepath"])

    # load values previously filled in checkboxes or None if this is first time annotating this sample
    sample_preload = load_annotation(subtask, index)
    if sample_preload is None:
        value_checkbox, value_textinput = None, ""
    else:
        value_checkbox, value_textinput = (sample_preload["checkbox"], sample_preload["textinput"])
    
    question = samples[str(index)]
    # display the "Sample 1/5" thing
    display_progress(key=subtask)

    st.markdown("\n**Do what the text says**:  ")

    # Display the input widgets.
    # Note that widget objects that have the same labels need to have different keys.
    checkbox = st.checkbox(key = 10 * index + 1, label=question["sentence"], value=value_checkbox)
    text_input = st.text_input(key = 10 * index + 2, label = "Obligatory text field. Write something.", max_chars=200, value=value_textinput)

    if text_input:  # only show the next button once something is in the text field
        next_input = st.button(key = 10 * index + 3, label="Next")
    else:
        next_input = None

    # return all the given input
    return question, checkbox, text_input, next_input