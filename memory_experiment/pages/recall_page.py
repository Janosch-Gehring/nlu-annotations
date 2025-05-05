import streamlit as st
from core.scripts import user_repository
import time

if "recall_start_time" not in st.session_state:
    st.session_state.recall_start_time = time.time()

st.html("""<p>Now please try to remember the headlines you learned at the beginning.
                    <br>The order of the headlines does not matter. Just write them down as you remember them, using a new line for each new headline. 
                    <p>If you can, please try to remember the headline in its original form as accurately as possible - but if you can't remember the exact headline, you can also paraphrase in your own words what the headline was about. 
                    <p>You should take approximately five minutes to write down as many headlines as possible from the memorization task.""")
recall = st.text_area("Headlines you remember:", key="recall", height=300)
if "recall_start_time" not in st.session_state:
    st.session_state.recall_start_time = time.time()
recall_dict = {}

if st.button("Submit"):
    if recall is None:
        st.warning("Please write down at least one headline before submitting."
        "If you don't remember the exact wording of any headlines, try to write down as much as you remember")
    elif time.time() - st.session_state.recall_start_time < 60: # change to 300
        if "recall_submit_attempts" not in st.session_state:
            st.session_state.recall_submit_attempts = 1
            st.warning("Please take your time to write down the headlines. You have 5 minutes for this task.")
        elif st.session_state.recall_submit_attempts < 2:
            st.session_state.recall_submit_attempts += 1
            st.warning("Please take your time to write down the headlines. You have 5 minutes for this task.")
        else: 
            textsplit = recall.splitlines()
            recall_dict["recall"] = []
            for x in textsplit:
                recall_dict["recall"].append(x)
            user_repository.save_one_annotation(st.session_state.user_id, "recall", 1, recall_dict)
            st.session_state.recall_end_time = time.time()
            st.switch_page("memory_experiment/pages/recognition_page.py")
    else:
        textsplit = recall.splitlines()
        recall_dict["recall"] = []
        for x in textsplit:
            recall_dict["recall"].append(x)
        user_repository.save_one_annotation(st.session_state.user_id, "recall", 1, recall_dict)
        st.session_state.recall_end_time = time.time()
        st.switch_page("memory_experiment/pages/recognition_page.py")