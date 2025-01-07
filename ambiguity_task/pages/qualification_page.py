import json

import streamlit as st

from core.scripts.utils import read_json_from_file
from core.scripts import user_repository
from ambiguity_task.common import constants, logic, utils

if "qualification_progress" not in st.session_state:
    st.session_state.qualification_progress = user_repository.get_checkpoint(st.session_state.user_id, "qualification")
st.session_state.page = "ambiguity_task_qualification_page_sample" + str(st.session_state.qualification_progress)

# user qualification of -1 or 1 mean that the test was already attempted
user_qualification = user_repository.get_qualification(st.session_state.user_id)
if user_qualification == 1:
    st.markdown("\n## You have completed the qualification test. \n\n Select **Annotation** on the navigation bar to your left to do some annotating.")
elif user_qualification == -1:
    st.markdown("\n## You have already attempted the qualification test. \n\n Unfortunately, you did not pass the qualification test. Contact us if you want to try again.")

else:
    # get index of sample
    index = int(st.session_state.qualification_progress)

    if index > 1:
        back_button = st.button(label="Back", key = 10 * index + 7)

        if back_button:
            st.session_state.qualification_progress -= 1
            st.rerun()
    
    # print text and widgets
    question, checkbox1, checkbox2, text_input1, checkbox3, text_input2, next_input = utils.print_annotation_schema("qualification", index)

    # behavior when pushing the next-button
    if next_input:
        # save annotation
        annotation = {"sentence": question["sentence"], "meaning1": checkbox1, "meaning2": checkbox2, "other_label": text_input1, "nonsensical": checkbox3, "comment": text_input2}
        user_repository.save_one_annotation(st.session_state.user_id, "qualification", st.session_state.qualification_progress, annotation)

        # check if there are more samples to go through
        qualification_questions = read_json_from_file(constants.QUALIFICATION_QUESTIONS_PATH)
        if st.session_state.qualification_progress < len(qualification_questions):
            st.session_state.qualification_progress += 1
            st.rerun()
        else:
            # if not, check for qualification
            user = user_repository.get_user(st.session_state.user_id)
            annotations = json.loads(user[5])
            if logic.check_if_qualified(annotations):
                st.write("Congrats, youre qualified!")
                user_repository.set_qualification(st.session_state.user_id)
                st.rerun()
            else:
                st.write("Oops, you failed the qualification.")
                user_repository.set_qualification(st.session_state.user_id, setting=-1)
                user_repository.reset_annotation(st.session_state.user_id, key="qualification")
                st.rerun()

            # reset progress to beginning
            st.session_state.qualification_progress = 1