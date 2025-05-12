import os

import streamlit as st

from core.scripts import user_repository
from core.scripts.utils import read_json_from_file, handle_next_button, handle_back_button, TASK_INFO, skip_to_next_sample
from plausibility_demo.common import utils


samples = read_json_from_file(TASK_INFO["plausibility_demo"]["annotation_filepath"])

if "progress" not in st.session_state:
    st.session_state.progress = 1
st.session_state.page = "plausibility_demo_annotation_page_sample" + str(st.session_state.progress)

if st.session_state.progress > 5:
    st.write("## Das war's! Sehen wir uns die Ergebnisse an.")

else:
    index = int(st.session_state.progress)

    question, slider_choice, nonsensical_input, comment_input, next_input = utils.print_annotation_schema_sliders("annotation", index)
    annotation = {"question": question, "slider": slider_choice, "nonsensical": nonsensical_input, "comment": comment_input}

    if next_input:
        handle_next_button(annotation, index, samples, "annotation")
