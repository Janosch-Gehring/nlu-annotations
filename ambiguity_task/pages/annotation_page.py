import json
import streamlit as st

from core.scripts import user_repository
from core.scripts.utils import read_json_from_file
from ambiguity_task.common import constants, utils

st.session_state.page = "ambiguity_task_annotation_page"


if "progress" not in st.session_state:
    st.session_state.progress = user_repository.get_checkpoint(st.session_state.user_id, "annotation")
st.session_state.page = "ambiguity_task_annotation_page_sample" + str(st.session_state.progress)

samples = read_json_from_file(constants.SAMPLES_FILEPATH)

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

    question, checkbox1, checkbox2, text_input1, checkbox3, text_input2, next_input = utils.print_annotation_schema("annotation", index)

    if next_input:
        annotation = {"sentence": question["sentence"], "meaning1": checkbox1, "meaning2": checkbox2, "other_label": text_input1, "nonsensical": checkbox3, "comment": text_input2}
        user_repository.save_one_annotation(st.session_state.user_id, "annotation", st.session_state.progress, annotation)
        if st.session_state.progress < len(samples):
            st.session_state.progress += 1
            st.rerun()
        else:
            finish_annotation()