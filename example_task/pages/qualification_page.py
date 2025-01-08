import streamlit as st

from core.scripts import user_repository, qualification_utils, utils
from example_task.common import utils as example_utils


# qualification progress dictates the current sample to show. Qualifications always need to have it
if "qualification_progress" not in st.session_state:
    st.session_state.qualification_progress = user_repository.get_checkpoint(st.session_state.user_id, "qualification")
st.session_state.page = "example_task_qualification_page_sample" + str(st.session_state.qualification_progress)

# user qualification of -1 or 1 mean that the test was already attempted
user_qualification = user_repository.get_qualification(st.session_state.user_id)
if user_qualification == 1:
    st.markdown("\n## You have successfully completed the qualification test. \n\n Select **Annotation** on the navigation bar to your left to do some annotating.")
elif user_qualification == -1:
    st.markdown("\n## You have already attempted the qualification test. \n\n Unfortunately, you did not pass the qualification test. Contact us if you want to try again.")

else:
    # get index of sample
    index = int(st.session_state.qualification_progress)

    back_button = None
    if index > 1:
        # Print a back button
        back_button = st.button(label="Back", key = 10 * index + 7)
    
    # print text and widgets
    question, checkbox, text_input, next_input = example_utils.print_annotation_schema("qualification", index)

    # behavior when pushing the next-button
    if next_input:
        # save annotation (saving the sentence is not really necessary)
        # make sure these keys match up with those used when calling load_annotation
        annotation = {"sentence": question["sentence"], "checkbox": checkbox, "textinput": text_input}
        user_repository.save_one_annotation(st.session_state.user_id, "qualification", st.session_state.qualification_progress, annotation)

        # check if there are more samples to go through
        qualification_utils.advance_qualification(utils.TASK_INFO["example_task"]["qualification_filepath"], example_utils.check_if_qualified)

    if back_button:
        # since all users see all samples, back button here is much simpler than for the real annotation. Just return to the progress-1 question.
        if index < user_repository.get_checkpoint(st.session_state.user_id, "qualification"):
            annotation = {"sentence": question["sentence"], "checkbox": checkbox, "textinput": text_input}
            user_repository.save_one_annotation(st.session_state.user_id, "qualification", st.session_state.qualification_progress, annotation)
        st.session_state.qualification_progress -= 1
        st.rerun()