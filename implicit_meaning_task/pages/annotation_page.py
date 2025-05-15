import os

import streamlit as st

from core.scripts import user_repository
from core.scripts.utils import read_json_from_file, handle_next_button, handle_back_button, TASK_INFO, skip_to_next_sample
from implicit_meaning_task.common import utils

# TODO: save progress during annotation

samples = read_json_from_file(TASK_INFO["implicit_meaning_task"]["annotation_filepath"])

if "progress" not in st.session_state:
    st.session_state.progress = user_repository.get_checkpoint("annotation")
    if not st.session_state.progress:  # no checkpoint yet -> simply go to the first relevant sample
        st.session_state.progress = skip_to_next_sample(0, samples, st.session_state.user[3], 1, 
                                                        "annotation", qualification_function=None)
st.session_state.page = "implicit_meaning_task_annotation_page_sample" + str(st.session_state.progress)

if user_repository.get_qualification() != 1:
    st.write("## You must pass qualification before starting annotation. \n\n Select **Qualification** in the navigation bar to your left to try the qualification test.")
elif user_repository.check_if_done(st.session_state.user_id):
    st.write("## You have finished annotation. \n\nThank you for your time!")
    st.write("\n\n\n")
    st.write("**Your Prolific Completion Code:**")
    st.write("# " + os.getenv("PROLIFIC_COMPLETION_CODE"))
else:
    index = int(st.session_state.progress)

    back_button = st.button(label="Back", key = 10 * index + 9, help="Go back to the previous sample.")

    question, implicit, checkboxes, comment_implicit, comment_not_implicit, next_input = utils.print_annotation_schema(samples, index, "annotation")

    annotation = {"sentence_1": question["sentence_1"], "sentence_2": question["sentence_2"], "implicit_meaning": implicit, "if_implicit": checkboxes, "comment_implicit": comment_implicit, "comment_not_implicit": comment_not_implicit}

    if next_input:
        handle_next_button(annotation, index, samples, "annotation")

    if back_button:
        handle_back_button(annotation, index, samples, "annotation")