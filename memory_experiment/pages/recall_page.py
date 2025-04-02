import streamlit as st
from core.scripts import user_repository

recall = st.text_area("""Please write down as many headlines as you remember here. Try to write downthe exact wording of each headline. "
Write each headline in a new line:""")
recall_dict = {}

if st.button("Submit"):
    if recall is None:
        st.warning("Please write down at least one headline before submitting. "
        "If you don't remember the exact wording of any headlines, try to write down as much as you remember")
    else:
        textsplit = recall.splitlines()
        recall_dict["recall"] = []
        for x in textsplit:
            recall_dict["recall"].append(x)
        user_repository.save_one_annotation(st.session_state.user_id, "recall", 1, recall_dict)
        st.switch_page("memory_experiment/pages/recognition_page.py")