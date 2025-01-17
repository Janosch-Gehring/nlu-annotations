import streamlit as st

from core.scripts import sheet_repository, utils
from example_task.common import utils as example_utils


# qualification progress dictates the current sample to show. Qualifications always need to have it
if "qualification_progress" not in st.session_state:
    st.session_state.qualification_progress = sheet_repository.get_checkpoint(subtask="qualification")
st.session_state.page = "example_task_qualification_page_sample" + str(st.session_state.qualification_progress)

# user qualification of -1 or 1 mean that the test was already attempted
user_qualification = st.session_state.user["qualified"]
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
    question, checkbox, text_input, next_button = example_utils.print_annotation_schema("qualification", index)

    samples = utils.read_json_from_file(utils.TASK_INFO["example_task"]["qualification_filepath"])
    annotation = {"sentence": question["sentence"], "checkbox": checkbox, "textinput": text_input}

    if next_button:
        utils.handle_next_button(annotation, index, samples, "qualification", example_utils.check_if_qualified)

    if back_button:
        utils.handle_back_button(annotation, index, samples, "qualification")