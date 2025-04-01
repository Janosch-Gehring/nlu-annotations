import streamlit as st

import pandas as pd
import random 
from core.scripts.utils import read_json_from_file, TASK_INFO, skip_to_next_sample, get_amount_of_samples_for_group, handle_next_button
from core.scripts import user_repository

st.write("Next, we will show you some more headlines. For each headline, decide whether you have seen it before or not.")

samples = read_json_from_file(TASK_INFO["memory_experiment"]["annotation_filepath"])
print(st.session_state)
if "shuffled_keys" not in st.session_state:
    shuffled_keys = list(samples.keys())
    random.shuffle(shuffled_keys)
    st.session_state.shuffled_keys = shuffled_keys
    print("Added shuffled keys:", st.session_state.shuffled_keys)
    st.session_state.index = 0
placeholder = st.empty()
key = st.session_state.shuffled_keys[st.session_state.index]
placeholder.write(samples[key]["headline"])
user_response = st.radio("Have you seen the text above before?", ["Yes, this was shown to me in the initial task", "No, this headline is new"])
show_next = st.button("Show next", key="show_next_button")
st.session_state.index += 1
while st.session_state.index < len(st.session_state.shuffled_keys) -1:
    if show_next:
        samples[key]["response"] = user_response
        samples[key]["sample_id"] = key
        print("key:", key)
        print("response:", user_response)
        user_repository.save_one_annotation(st.session_state.user_id, "recognition", int(key), samples[key])
        key = st.session_state.shuffled_keys[st.session_state.index]
        placeholder.write(samples[key]["headline"])
        st.session_state.index += 1
        show_next = None

samples[key]["response"] = user_response
samples[key]["sample_id"] = key
user_repository.save_one_annotation(st.session_state.user_id, "recognition", int(key), samples[key])

st.switch_page("memory_experiment/pages/demographics_page.py")