import streamlit as st
import time
import pandas as pd
import random 
from core.scripts.utils import read_json_from_file, TASK_INFO, skip_to_next_sample, get_amount_of_samples_for_group, handle_next_button
from core.scripts import user_repository

st.html("""<p>Below you will see some news headlines on the screen one after the other. 
         <p>For each headline, please indicate how false or true you personally think it is (scale from 1=false to 7=true).""")

samples = read_json_from_file(TASK_INFO["memory_experiment"]["annotation_filepath"])
sample_response = {}
print(st.session_state)
if "shuffled_keys_credibility" not in st.session_state:
    shuffled_keys = [key for key, value in samples.items() if st.session_state.user[3] in value["presentation_grouping"] and value["grouping"] != 4]
    random.shuffle(shuffled_keys)
    st.session_state.shuffled_keys_credibility = shuffled_keys
    print("Added shuffled keys:", st.session_state.shuffled_keys_credibility)
    st.session_state.index = 0

credibility_labels = {
        0: "1 - defininitely false",
        1: "2",
        2: "3",
        3: "4",
        4: "5",
        5: "6",
        6: "7 - definitely true"
}
if st.session_state.index < len(st.session_state.shuffled_keys_credibility):
    print("In Fragment!")
    key = st.session_state.shuffled_keys_credibility[st.session_state.index]
    st.html(f"<h2>{samples[key]["headline"]}")
    user_response = st.select_slider("How true do you think this news headline is", options=[
        credibility_labels[0],
        credibility_labels[1],
        credibility_labels[2],
        credibility_labels[3],
        credibility_labels[4],
        credibility_labels[5],
        credibility_labels[6]
    ], value=credibility_labels[2], key=st.session_state.index)
    show_next = st.button("Show next", key="show_next_button")
else:
    st.session_state.truth_judgement_end_time = time.time()
    st.switch_page("memory_experiment/pages/demographics_page.py")

if show_next:
    if user_response is None:
        st.warning("Please select an answer before proceeding.")
    else:
        sample_response["credibility_rating"] = user_response
        sample_response["sample_id"] = int(key)
        sample_response["seen_in_presentation"] = 1 if st.session_state.user[3] == samples[key]["grouping"] else 0
        sample_response["headline"] = samples[key]["headline"]
        sample_response["contains_pronoun"] = samples[key]["contains_pronoun"]
        sample_response["avg_word_length"] = samples[key]["avg_word_length"]
        sample_response["perc_long_words"] = samples[key]["perc_long_words"]
        sample_response["num_long_words"] = samples[key]["num_long_words"]
        print("key:", key)
        print("response:", user_response)
        user_repository.save_one_annotation(st.session_state.user_id, "truth_judgement", int(key), sample_response)
        #key = st.session_state.shuffled_keys[st.session_state.index]
        #placeholder.write(samples[key]["headline"])
        st.session_state.index += 1
        print("Rerunning with new key", st.session_state.index)
        st.rerun()