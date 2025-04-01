import streamlit as st
import pandas as pd
import time

from core.scripts.utils import read_json_from_file, TASK_INFO, skip_to_next_sample, get_amount_of_samples_for_group, handle_next_button
from core.scripts import user_repository

samples = read_json_from_file(TASK_INFO["memory_experiment"]["annotation_filepath"])

placeholder = st.empty()
if "progress" not in st.session_state:
    st.session_state.progress = user_repository.get_checkpoint("memory")
    if not st.session_state.progress:
        st.session_state.progress = skip_to_next_sample(0, samples, st.session_state.user[3], 1, "memory", qualification_function=None)
        st.session_state.presented_samples = 0
st.session_state.page = "memory_experiment_presentation_page_sample" + str(st.session_state.progress)
num_samples = get_amount_of_samples_for_group("memory", "memory_experiment", st.session_state.user[3])
print("Number of Samples to present:", num_samples)
while st.session_state.presented_samples < num_samples -1: 
    print("Progress: ", st.session_state.progress)
    index = int(st.session_state.progress)
    placeholder.write(samples[str(index)]["headline"])
    time.sleep(2)
    st.session_state.progress = skip_to_next_sample(index, samples, st.session_state.user[3], 1, "memory", qualification_function=None)
    st.session_state.presented_samples += 1
    print("In loop, presented samples: ", st.session_state.presented_samples)

index = int(st.session_state.progress)
print("Out of Loop, presetned samples: ", st.session_state.presented_samples)
placeholder.write(samples[str(index)]["headline"])
time.sleep(2)
st.switch_page("memory_experiment/pages/distractor_page.py")