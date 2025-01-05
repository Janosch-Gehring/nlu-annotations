import json
import streamlit as st

from core.scripts import user_repository
from core.scripts.utils import read_json_from_file
from ambiguity_task.common import constants

st.session_state.page = "ambiguity_task_annotation_page"


if "progress" not in st.session_state:
    st.session_state.progress = user_repository.get_checkpoint(st.session_state.user_id, "annotation")
st.session_state.page = "ambiguity_task_annotation_page_sample" + str(st.session_state.progress)

samples = read_json_from_file(constants.SAMPLES_FILEPATH)

def format_sentence(sentence):
    sentence = sentence.replace("[", ":blue-background[")
    return sentence

def finish_annotation():
    st.write("You finished the annotation!")
    user_repository.mark_as_done(st.session_state.user_id)
    st.rerun()
    st.write("Thank you for submitting your annotations.")

if user_repository.get_qualification(st.session_state.user_id) != 1:
    st.write("## You must pass qualification before starting annotation. \n\n Select **Qualification** in the navigation bar to your left to try the qualification test.")
elif user_repository.check_if_done(st.session_state.user_id):
    st.write("## You have finished annotation. \n\nThank you for your time!")
else:
    index = int(st.session_state.progress)

    while True:
        question = samples[str(index)]
        grouping = user_repository.get_user(st.session_state.user_id)[3]
        if grouping != question["grouping"]:
            st.session_state.progress = int(st.session_state.progress) + 1
            index += 1
            if index >= len(samples):
                finish_annotation()
        else:
            break

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

    if st.button(key = -10 * index + 9, label="Next"):
        annotation = {"sentence": question["sentence"], "meaning1": checkbox1, "meaning2": checkbox2, "other_label": text_input1, "nonsensical": checkbox3, "comment": text_input2}
        user_repository.save_one_annotation(st.session_state.user_id, "annotation", st.session_state.progress, annotation)
        if st.session_state.progress < len(samples):
            st.session_state.progress += 1
            st.rerun()
        else:
            finish_annotation()