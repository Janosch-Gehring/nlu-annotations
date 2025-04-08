import streamlit as st
import pandas as pd
import time
import random

from core.scripts.utils import read_json_from_file, TASK_INFO, skip_to_next_sample, get_amount_of_samples_for_group, handle_next_button
from core.scripts import user_repository

samples = read_json_from_file(TASK_INFO["memory_experiment"]["annotation_filepath"])

placeholder = st.empty()

if "shuffled_keys_presentation" not in st.session_state:
    st.session_state.progress = user_repository.get_checkpoint("memory")
    shuffled_keys = [key for key, value in samples.items() if value["grouping"] == st.session_state.user[3]]
    random.shuffle(shuffled_keys)
    st.session_state.shuffled_keys_presentation = shuffled_keys
    print("Added shuffled keys:", st.session_state.shuffled_keys_presentation)
    st.session_state.index = 0

while st.session_state.index < len(st.session_state.shuffled_keys_presentation): 
    print("Progress: ", st.session_state.index)
    index = int(st.session_state.progress)
    key = st.session_state.shuffled_keys_presentation[st.session_state.index]
    placeholder.write(samples[key]["headline"])
    time.sleep(2)
    st.session_state.index += 1
    print("In loop, presented samples: ", st.session_state.index)

st.switch_page("memory_experiment/pages/distractor_page.py")