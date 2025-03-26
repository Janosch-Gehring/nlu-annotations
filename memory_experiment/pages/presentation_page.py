import streamlit as st
import pandas as pd
import time
from core.scripts.utils import read_json_from_file, TASK_INFO, skip_to_next_sample, get_amount_of_samples_for_group
from core.scripts import user_repository

samples = read_json_from_file(TASK_INFO["memory_experiment"]["memory_filepath"])

#st.markdown("""
#            <style>
#                .stMarkdown {
#                    background-color: white;
#            color:black;
#            height: 100px;
#            }
#            </style>
#""", unsafe_allow_html=True)

placeholder = st.empty()

if "progress" not in st.session_state:
    st.session_state.progress = user_repository.get_checkpoint("memory")
    st.session_state.progress = skip_to_next_sample(1, samples, st.session_state.user[3], 1, "memory", qualification_function=None)
    index = int(st.session_state.progress)
    num_samples = get_amount_of_samples_for_group(samples, st.session_state.user[3])
    while index <= num_samples:
        placeholder.write(samples[index]["sentence"])
        time.sleep(60)
        index += 1

st.switch_page("memory_experiment/pages/recall_page.py")