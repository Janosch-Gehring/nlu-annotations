import streamlit as st

from core.scripts.utils import display_progress, read_json_from_file
from ambiguity_task.common import constants


def format_sentence(sentence):
    sentence = sentence.replace("[", ":blue-background[")
    return sentence

def print_annotation_schema(subtask: str, index: int) -> list:
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
    
    question = samples[str(index)]
    # display the "Sample 1/5" thing
    display_progress(key=subtask)

    st.markdown("\n**Read the following text**:  ")
    st.markdown(format_sentence(question["sentence"]) + "\n")
    st.markdown("Focus on the word :blue-background[" + question["word"] + "]\n")
    st.write("Which of these senses seem plausible?")
    checkbox1 = st.checkbox(key = 10 * index + 1, label=question["meaning1"])
    checkbox2 = st.checkbox(key = 10 * index + 2, label=question["meaning2"])
    text_input1 = st.text_input(key = 10 * index + 3, label = "(Only if you picked neither) Define a better label.", max_chars=200)
    checkbox3 = st.checkbox(key = 10 * index + 4, label = "Check here if the sentence appears to be nonsensical.")
    st.write("\n\n")

    text_input2 = st.text_input(key = 10 * index + 8, label = "Comments (optional)")

    next_input = st.button(key = 10 * index + 9, label="Next")

    return question, checkbox1, checkbox2, text_input1, checkbox3, text_input2, next_input