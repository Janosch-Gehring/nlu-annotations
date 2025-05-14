import json, os, sys
import streamlit as st
sys.path.append('..')
from core.scripts import user_repository, utils as core_utils
from implicit_meaning_task.common import logic, utils

if "qualification_progress" not in st.session_state:
    st.session_state.qualification_progress = user_repository.get_checkpoint("qualification") or 1
st.session_state.page = "ambistory_task_qualification_page_sample" + str(st.session_state.qualification_progress)

# user qualification of -1 or 1 mean that the test was already attempted
user_qualification = user_repository.get_qualification()
if user_qualification == 1:
    st.markdown("\n## You have successfully completed the qualification test. \n\n Remember that checking **both** meanings could also be correct in truly ambiguous stories. \n\n Select **Annotation** on the navigation bar to your left to do some annotating.")
elif user_qualification == -1:
    st.markdown("\n## You did not pass the qualification test. \n\n You have already attempted the qualification test and failed. Sorry about that! Please copy the below completion code into Prolific.\n\n")
    st.markdown("## Your completion code: " + os.getenv("PROLIFIC_SCREENOUT_CODE"))

else:
    # get index of sample
    index = int(st.session_state.qualification_progress)

    if index == 1:
        st.write("Remember to read the Ambiguous Story Task Intro before attempting the qualification test!")

    back_button = st.button(label="Back", key = 10 * index + 9)
    st.markdown("# Qualification Task\n\nIn order to proceed with the annotation task you must first pass this qualification test. Before attempting this task, please read the intro carefully.\n\n")

    if "qualification_index" not in st.session_state:
        st.session_state.qualification_index = 1
    if "save_annotations" not in st.session_state:
        st.session_state.save_annotations = {}


    with open("../resources/qualification_samples.json", "r") as jsn:
        samples = json.load(jsn)
    # print text and widgets
    question, implicit, checkboxes, comment_implicit, comment_not_implicit, next_input = utils.print_annotation_schema(samples, index)

    annotation = {"sentence": question["sentence"], "implicit_meaning": implicit, "if_implicit": checkboxes, "comment_implicit": comment_implicit, "comment_not_implicit": comment_not_implicit}
    samples = core_utils.read_json_from_file(core_utils.TASK_INFO["implicit_meaning_task"]["qualification_filepath"])
    if next_input:
        if st.session_state.qualification_index == len(samples):
            if set([truth_val for idx,truth_val in st.session_state.save_annotations.items()]) == {True}:
                st.markdown("#### You have completed the qualification test. Thank you!")
            else:
                st.markdown("#### You have failed the qualification test. Better luck next time!")
        else:
            st.session_state.qualification_index += 1

    # if st.session_state.qualification_index != index:
    #     st.session_state.save_annotations[index] = implicit == question["correct_answer"]
    #     st.rerun()

    if next_input:
        core_utils.handle_next_button(annotation, index, samples, "qualification", logic.check_if_qualified)

    if back_button:
        core_utils.handle_back_button(annotation, index, samples, "qualification")