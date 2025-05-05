import streamlit as st
from core.scripts import user_repository
import time
from datetime import datetime

political_labels = {
    0: "1 - left",
    1: "2",
    2: "3 - center",
    3: "4",
    4: "5 - right",
}
demographics = {}
with st.form("Please provide the following information about yourself:"):
    age = st.number_input("How old are you?", min_value=0, max_value=100, key="age", placeholder=None)
    education = st.radio("What's your highest education level?", ["no formal education", "high school diploma", "college degree", "graduate degree"],index=None, key="education")
    occupation = st.radio("What is your current occupation?", ["employed", "unemployed", "self-employed", "retired", "homemaker", "student", "other"],index=None)
    political_party = st.select_slider("What is your political orientation?", options=[
        political_labels[0],
        political_labels[1],
        political_labels[2],
        political_labels[3],
        political_labels[4],
    ])
    news_consumption = st.text_input("Where do you get most of your news from (i.e. newspapers, TV, radio, internet, social media,...)?")
    submitted = st.form_submit_button("Submit")
if submitted:
    demographics["age"] = age
    demographics["education"] = education
    demographics["occupation"] = occupation
    demographics["political_party"] = political_party
    demographics["news_consumption"] = news_consumption
    demographics["experiment_start_time"] = st.session_state.experiment_start_time
    demographics["recall_start_time"] = st.session_state.recall_start_time
    demographics["recall_end_time"] = st.session_state.recall_end_time
    demographics["recognition_end_time"] = st.session_state.recognition_end_time
    demographics["truth_judgement_end_time"] = st.session_state.truth_judgement_end_time
    demographics["experiment_end_time"] = time.time()
    user_repository.update_demographics(st.session_state.user_id, demographics)
    st.switch_page("memory_experiment/pages/thank_you_page.py")