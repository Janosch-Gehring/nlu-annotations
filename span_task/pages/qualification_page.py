import streamlit as st
import os

from core.scripts import user_repository, utils as core_utils
from span_task.common import logic, utils

if "qualification_progress" not in st.session_state:
    st.session_state.qualification_progress = user_repository.get_checkpoint("qualification") or 1
st.session_state.page = "span_task_qualification_samples" + str(st.session_state.qualification_progress)

# user qualification of -1 or 1 mean that the test was already attempted
user_qualification = user_repository.get_qualification()
if user_qualification > 0:
    st.markdown("\n## You have finished Qualification successfully. \n\n Time for the main study.")

elif user_qualification == -1:
    st.markdown("\n## You did not pass the qualification test. \n\n You have already attempted the qualification test and failed. Sorry about that! Please copy the below completion code into Prolific.\n\n")
    st.markdown("## Your completion code: " + os.getenv("PROLIFIC_SCREENOUT_CODE"))

else:
    # get index of sample
    index = int(st.session_state.qualification_progress)

    if index == 1:
        st.write("Remember to read the Task Intro before attempting the qualification test! \n\n *If you make a mistake here, you will get screened out early.*")

    back_button = None# st.button(label="Back", key = 10 * index + 7)

    st.write("""

## Before you start 

Each page shows a short story, one word in it, and one possible meaning of that word. For each page you will:

1. *Rate* how plausible the meaning is in this story.

2. *Explain* what shaped your rating: the story itself, what you know about the world, or both.

3. *Mark* the words that mattered most.
    
    """)

    # print text and widgets
    question, slider, reason, spans, comment, next_input = utils.print_annotation_schema_sliders("qualification", index)

    annotation = {"question": question, "slider": slider, "reasons": reason, "spans": spans, "comment": comment}
    samples = core_utils.read_json_from_file(core_utils.TASK_INFO["span_task"]["qualification_filepath"])

    if next_input:
        core_utils.handle_next_button(annotation, index, samples, "qualification", logic.check_if_qualified)

    if back_button:
        core_utils.handle_back_button(annotation, index, samples, "qualification")
