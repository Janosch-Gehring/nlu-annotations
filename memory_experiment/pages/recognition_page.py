import streamlit as st
import time
import pandas as pd
import random 
from core.scripts.utils import read_json_from_file, TASK_INFO, skip_to_next_sample, get_amount_of_samples_for_group, handle_next_button
from core.scripts import user_repository

st.write("""<p>Below, you will again see some news headlines on the screen, one after the other. 
         <p>You might have seen some of them before during this experiment, others are new.
         <p>For each headline, please indicate whether it is a headline you have seen in the initial memorization task or a new headline you have not seen in the memorization task.""")

samples = read_json_from_file(TASK_INFO["memory_experiment"]["annotation_filepath"])
sample_response = {}
print(st.session_state)
if "shuffled_keys_recognition" not in st.session_state:
    shuffled_keys = [key for key, value in samples.items() if st.session_state.user[3] in value["presentation_grouping"] and value["grouping"] != 5]
    random.shuffle(shuffled_keys)
    st.session_state.shuffled_keys_recognition = shuffled_keys
    print("Added shuffled keys:", st.session_state.shuffled_keys_recognition)
    st.session_state.index = 0

if st.session_state.index < len(st.session_state.shuffled_keys_recognition):
    print("In Fragment!")
    key = st.session_state.shuffled_keys_recognition[st.session_state.index]
    st.write(samples[key]["headline"])
    user_response = st.radio("Have you seen the text above before?", ["Yes, this was shown to me in the initial task", "No, this headline is new"], 
                            index=None, 
                            key=st.session_state.index)
    show_next = st.button("Show next", key="show_next_button")
else:
    st.session_state.recognition_end_time = time.time()
    st.switch_page("memory_experiment/pages/truthjudgement_page.py")

if show_next:
    if user_response is None:
        st.warning("Please select an answer before proceeding.")
    else:
        sample_response["response"] = user_response
        sample_response["sample_id"] = int(key)
        print("key:", key)
        print("response:", user_response)
        user_repository.save_one_annotation(st.session_state.user_id, "recognition", int(key), sample_response)
        #key = st.session_state.shuffled_keys[st.session_state.index]
        #placeholder.write(samples[key]["headline"])
        st.session_state.index += 1
        print("Rerunning with new key", st.session_state.index)
        st.rerun()