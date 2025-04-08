import streamlit as st

import pandas as pd
import random 
from core.scripts.utils import read_json_from_file, TASK_INFO, skip_to_next_sample, get_amount_of_samples_for_group, handle_next_button
from core.scripts import user_repository

st.write("You will now see the same headlines again. This time, for each headline, indicate how credibe this news item is to you.")

samples = read_json_from_file(TASK_INFO["memory_experiment"]["annotation_filepath"])
print(st.session_state)
if "shuffled_keys_credibility" not in st.session_state:
    shuffled_keys = list(samples.keys())
    random.shuffle(shuffled_keys)
    st.session_state.shuffled_keys_credibility = shuffled_keys
    print("Added shuffled keys:", st.session_state.shuffled_keys_credibility)
    st.session_state.index = 0

if st.session_state.index < len(st.session_state.shuffled_keys_credibility):
    print("In Fragment!")
    key = st.session_state.shuffled_keys_credibility[st.session_state.index]
    st.write(samples[key]["headline"])
    user_response = st.slider("How credible is this news headline to you? (From 0 not at all to 7 very credible)", 0, 7, None, 1, 
                            index=None, 
                            key=st.session_state.index)
    show_next = st.button("Show next", key="show_next_button")
else:
    st.switch_page("memory_experiment/pages/demographics_page.py")

if show_next:
    if user_response is None:
        st.warning("Please select an answer before proceeding.")
    else:
        samples[key]["credibility_rating"] = user_response
        samples[key]["sample_id"] = int(key)
        print("key:", key)
        print("response:", user_response)
        user_repository.save_one_annotation(st.session_state.user_id, "recognition", int(key), samples[key])
        #key = st.session_state.shuffled_keys[st.session_state.index]
        #placeholder.write(samples[key]["headline"])
        st.session_state.index += 1
        print("Rerunning with new key", st.session_state.index)
        st.rerun()