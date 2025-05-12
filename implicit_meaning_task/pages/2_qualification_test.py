import json, os, sys
import streamlit as st
sys.path.append('..')
from common import utils


st.markdown("# Qualification Task\n\nIn order to proceed with the annotation task you must first pass this qualification test. Before attempting this task, please read the intro carefully.\n\n")

if "qualification_index" not in st.session_state:
    st.session_state.qualification_index = 1
if "save_annotations" not in st.session_state:
    st.session_state.save_annotations = {}

index = st.session_state.qualification_index

back_button = st.button(label="Back", key = 10 * index + 9)

with open("/home/laura/Work_Area/prolific/streamlit_test/resources/qualification_samples.json", "r") as jsn:
    samples = json.load(jsn)
# print text and widgets
question, implicit, checkboxes, comment_implicit, comment_not_implicit, next_input = utils.print_annotation_schema(samples, index)

if next_input:
    if st.session_state.qualification_index == len(samples):
        if set([truth_val for idx,truth_val in st.session_state.save_annotations.items()]) == {True}:
            st.markdown("#### You have completed the qualification test. Thank you!")
        else:
            st.markdown("#### You have failed the qualification test. Better luck next time!")
    else:
        st.session_state.qualification_index += 1

if st.session_state.qualification_index != index:
    st.session_state.save_annotations[index] = implicit == question["correct_answer"]
    st.rerun()
# if back_button:
#     core_utils.handle_back_button(annotation, index, samples, "qualification")