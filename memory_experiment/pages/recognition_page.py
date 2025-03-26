import streamlit as st

import pandas as pd
import random 
from core.scripts.utils import read_json_from_file, TASK_INFO, skip_to_next_sample, get_amount_of_samples_for_group, handle_next_button
from core.scripts import user_repository

st.write("Next, we will show you some more headlines. For each headline, decide whether you have seen it before or not.")

samples = read_json_from_file(TASK_INFO["memory_experiment"]["recognition_filepath"])

if "shuffled_keys" not in st.session_state:
    st.session_state.shuffled_keys = random.shuffle(list(samples.keys()))
    st.session_state.index = 0

if st.session_state.index < len(st.session_state.shuffled_keys):
    key = st.session_state.shuffled_keys[st.session_state.index]
    st.write(samples[key]["headline"])
    user_response = st.radio("Have you seen the text above before?", ["Yes, this was shown to me in the initial task", "No, this headline is new"])
    if st.button("Show next"):
        # TODO handle saving of recognition judgements



if st.session_state.index < len(st.session_state.shuffled_keys):
    key = st.session_state.shuffled_keys[st.session_state.index]
    st.write(f"**{key}**: {data[key]}")

    # Button to show next key-value pair
    if st.button("Next"):
        st.session_state.index += 1
        st.experimental_rerun()
else:
    st.write("All keys have been displayed!")