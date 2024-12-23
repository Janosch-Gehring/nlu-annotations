import json

import streamlit as st

from core.utils import read_json_from_file
from core.scripts import user_repository
from ambiguity_task.common import constants, logic

if "qualification_progress" not in st.session_state:
    st.session_state.qualification_progress = user_repository.get_checkpoint(st.session_state.user_id, "qualification")
st.session_state.page = "ambiguity_task_qualification_page_sample" + str(st.session_state.qualification_progress)

qualification_questions = read_json_from_file(constants.QUALIFICATION_QUESTIONS_PATH)

def format_sentence(sentence):
    sentence = sentence.replace("[", ":blue-background[")
    return sentence

index = int(st.session_state.qualification_progress)
question = qualification_questions[str(index)]
st.markdown("\n**Read the following text**:  ")
st.markdown(format_sentence(question["sentence"]) + "\n")
st.markdown("Focus on the word :blue-background[" + question["word"] + "]\n")
st.write("Which of these senses seem plausible?")
checkbox1 = st.checkbox(key = 10 * index + 1, label=question["meaning1"])
checkbox2 = st.checkbox(key = 10 * index + 2, label=question["meaning2"])
text_input1 = st.text_input(key = 10 * index + 3, label = "(Only if you picked neither) Define a better label.", max_chars=200)
checkbox3 = st.checkbox(key = 10 * index + 4, label = "Check here if the sentence appears to be nonsensical.")
st.write("\n\n")

text_input2 = st.text_input(key = 10 * index + 8, label = "Comments (optional)")

if st.button(key = 10 * index + 9, label="Next"):
    annotation = {"sentence": question["sentence"], "meaning1": checkbox1, "meaning2": checkbox2, "other_label": text_input1, "nonsensical": checkbox3, "comment": text_input2}
    user_repository.save_one_annotation(st.session_state.user_id, "qualification", st.session_state.qualification_progress, annotation)
    if st.session_state.qualification_progress < len(qualification_questions):
        st.session_state.qualification_progress += 1
        st.rerun()
    else:
        user = user_repository.get_user(st.session_state.user_id)
        annotations = json.loads(user[5])
        print("Annotations", annotations)
        if logic.check_if_qualified(annotations):
            st.write("Congrats, youre qualified!")
            user_repository.make_qualified(st.session_state.user_id)
        else:
            st.write("Oops, you failed the qualification.")