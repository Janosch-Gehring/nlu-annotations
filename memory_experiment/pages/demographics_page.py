import streamlit as st
from core.scripts import user_repository

demographics = {}
with st.form("Please provide the following information about yourself:"):
    age = st.number_input("How old are you?", min_value=0, max_value=100, key="age")
    education = st.radio("What's your highest education level?", ["no formal education", "high school diploma", "college degree", "graduate degree"], key="education")
    occupation = st.radio("What is your current occupation?", ["employed", "unemployed", "self-employed", "retired", "homemaker", "student", "other"])
    political_party = st.radio("Which political party did you vote for in the last election?", ["Republicans", "Democrats", "Independent", "I did not vote"])
    news_consumption = st.text_input("Where do you get most of your news from (i.e. newspapers, TV, radio, internet, social media,...)?")
    submitted = st.form_submit_button("Submit")
if submitted:
    demographics["age"] = age
    demographics["education"] = education
    demographics["occupation"] = occupation
    demographics["political_party"] = political_party
    demographics["news_consumption"] = news_consumption
    user_repository.update_demographics(st.session_state.user_id, demographics)
    st.switch_page("memory_experiment/pages/thank_you_page.py")