import streamlit as st

from core.scripts import user_repository
from core.scripts.utils import read_json_from_file, handle_next_button, handle_back_button, TASK_INFO
from ambiguity_task.common import constants, utils

if "progress" not in st.session_state:
    st.session_state.progress = user_repository.get_checkpoint(st.session_state.user_id, "annotation")
    st.session_state.progression_direction = 1  # 1 -> user wants to go forward, -1 -> user wants to go backwards (pressed back button)
st.session_state.page = "ambiguity_task_annotation_page_sample" + str(st.session_state.progress)


samples = read_json_from_file(TASK_INFO["ambiguity_task"]["annotation_filepath"])


if user_repository.get_qualification(st.session_state.user_id) != 1:
    st.write("## You must pass qualification before starting annotation. \n\n Select **Qualification** in the navigation bar to your left to try the qualification test.")
elif user_repository.check_if_done(st.session_state.user_id):
    st.write("## You have finished annotation. \n\nThank you for your time!")
else:
    index = int(st.session_state.progress)

    back_button = st.button(label="Back", key = 10 * index + 7)

    question, checkbox1, checkbox2, text_input1, checkbox3, text_input2, next_input = utils.print_annotation_schema("annotation", index)
    annotation = {"sentence": question["sentence"], "meaning1": checkbox1, "meaning2": checkbox2, "other_label": text_input1, "nonsensical": checkbox3, "comment": text_input2}

    if next_input:
        handle_next_button(annotation, index, samples, "annotation")

    if back_button:
        handle_back_button(annotation, index, samples, "annotation")