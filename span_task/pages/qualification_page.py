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

    back_button = st.button(label="Back", key = 10 * index + 7)

    st.write("""
# Guidelines

On each page, you will be presented with a short story where one of the words has multiple meanings (like how 'bat' can refer to both an animal or a baseball bat). You are presented with one of the meanings. Then, you will have to do three things:

## 1) Rate how plausible a meaning of a word is in the context of the short story using one of five scores:

* **1**: The displayed meaning is not plausible at all given the context.
* **2**: The displayed meaning is theoretically conceivable, but less plausible than other meanings.
* **3**: The displayed meaning represents one of multiple, similarly plausible interpretations.
* **4**: The displayed meaning represents the most plausible interpretation; other meanings may still be conceivable.
* **5**: The displayed meaning is the only plausible meaning given the context.

There will be times where this is highly subjective. Read the story carefully and think about how you would interpret it.

## 2) Explain what influenced your decision

Explain why you thought that the meaning was plausible or implausible. You must select at least one of the following categories:

#### 1) "There are words in the context that by themselves are obviously associated with one meaning."

**Example:**: *He showed me the [bat] he found. The wings appear to be in poor shape.*

-> Even without any further context, the word 'wings' practically confirms that [bat] is an animal, not a baseball bat.

#### 2) "The general premise or location makes the meaning more/less plausible."

There may not be any words that give away the meaning by themselves, but given the entire context (premise, location, characters...), one seems more plausible.

**Example:** *The cats sit outside peacefully. One of them keeps looking at a [star].*

-> While not inconceivable that they are looking at a famous person, it seems more plausible given the general situation that they are looking at the sky.

#### 3) "Logically, the events that occur make the most sense with a certain meaning."

With one meaning, the story makes sense, and with the other meaning it would either be illogical or just a bit odd.

**Example**: *He finally finished his [sentence]. He is very happy about it.*

-> Sentence here probably means verdict/punishment instead of a grammatical sentence, because finishing a grammatical sentence would not result in such an emotional reaction. This would count as social reasoning (as it relates to expected human behavior).

#### 4) "It is more/less plausible for reasons that not everyone may know."

Your reasoning for why you think the meaning is plausible or implausible is related to something you know about the world. **You should pick this option if you think it is conceivable that some people may not possess the necessary knowledge.**

**Example**: *The golf player's round was below [par]. She threw away her golf club in frustration.*

-> "Below par" generally refers to a bad performance. However, in the context of golf, being "below par" is actually a good thing. So, it's not the golf meaning of "par" here.
If you knew this, you would pick this option, and also 3) in addition.
If you didn't know this, you would pick a different option, like 2).

#### 5) "I can imagine multiple interpretations, but there aren't really any hints in the context."

You can pick this if you think multiple interpretations are equally plausible. You can also pick this if you think that one meaning seems more intuitive because it is more common or sounds better or for another reason.

#### 6) "I don't understand what the other meanings of that word would be."

Only pick this if you legitimately cannot think of another sense for the word.


## 3) Annotate spans of text that influenced your decision the most

The story will be shown again. Annotate the words or phrases that are relevant for the reasons you gave above by marking them with your mouse. You must mark at least 1 word.

    
    """)

    # print text and widgets
    question, slider, reason, spans, comment, next_input = utils.print_annotation_schema_sliders("qualification", index)

    annotation = {"question": question, "slider": slider, "reasons": reason, "spans": spans, "comment": comment}
    samples = core_utils.read_json_from_file(core_utils.TASK_INFO["span_task"]["qualification_filepath"])

    if next_input:
        core_utils.handle_next_button(annotation, index, samples, "qualification", logic.check_if_qualified)

    if back_button:
        core_utils.handle_back_button(annotation, index, samples, "qualification")
