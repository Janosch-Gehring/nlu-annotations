import streamlit as st

from core.scripts.utils import display_progress, read_json_from_file, load_annotation, TASK_INFO


def format_sentence(sentence):
    return "***" + sentence.replace("[", ":blue-background[") + "***\n"

def print_annotation_schema_sliders(subtask: str, index: int) -> tuple:
    """
    Prints the annotation schema for the annotation with the sliders. 

    :param subtask: str
    :param index: The number sample to show
    :return: The stuff to return
    """
    if subtask == "qualification":
        samples = read_json_from_file(TASK_INFO["rewriting_judgement_task"]["qualification_filepath"])
    else:
        samples = read_json_from_file(TASK_INFO["rewriting_judgement_task"]["annotation_filepath"])

    '''sample_preload = load_annotation(subtask, index)
    if not sample_preload:
        value_slider, value_nonsensical, value_comment = None, None, ""
    else:
        value_slider, value_nonsensical, value_comment = (sample_preload["slider"], sample_preload["nonsensical"], sample_preload["comment"])
        if value_slider in slider_labels:
            value_slider = slider_labels[value_slider]
        else:
            value_slider = None'''

    question = samples[str(index)]
    # display the "Sample 1/5" thing
    display_progress(key=subtask)

    st.markdown("Read the following headline and revision")

    st.write("---")

    st.markdown("**Original**: " + question["original"])

    st.write("---")

    st.markdown("**Revision**: " + question["revision"])

    st.write("---")

    accuracy = st.radio("Does the content in the revised version accurately reflect the content of the source text?",
                        ["Yes", "No"], index=None)
    
    misrepresentation, omission, addition = False, False, False
    if accuracy == "No":
        accuracy_col = st.columns(3)
        with accuracy_col[0]:
            misrepresentation = st.checkbox("Misrepresentation")
        with accuracy_col[1]:
            omission = st.checkbox("Omission")
        with accuracy_col[2]:
            addition = st.checkbox("Addition")

    if st.toggle("Show guidelines for rating accuracy"):
        st.markdown("""
**Select "no" if any of the following violations are found in the revision and check all that apply:**

* **Misrepresentation**: the revision misrepresents information provided in the original headline
* **Addition**: The revision includes content not present in the original headline
* **Omission**: The revision is missing content present in the original headline
        """)
    accuracy_subclass = [misrepresentation, omission, addition]

    st.write("\n")

    style = st.radio("Is the language style of the revised headline appropriate?",
                        ["Yes", "No"], index=None)
    
    grammar, awkward, register, inconsistent = False, False, False, False
    if style == "No":
        style_col = st.columns(4)
        with style_col[0]:
            grammar = st.checkbox("Grammar")
        with style_col[1]:
            awkward = st.checkbox("Awkward Style")
        with style_col[2]:
            register = st.checkbox("Register")
        with style_col[3]:
            inconsistent = st.checkbox("Inconsistent Style")

    style_subclass = [grammar, awkward, register, inconsistent]

    if st.toggle("Show guidelines for rating style"):
        st.markdown("""          
**Check "no" if any of the following are found in the revision and check all that apply:**
* **Grammar**: The revision contains grammar or language errors
* **Awkward Style**: The revision is grammatical, but unnatural as a news headline or awkward (e.g it involves excessive wordiness or overly embedded clauses)
* **Register**: The revision does not match the tone or level of formality exhibited by the original headline. The inclusion of first/second person pronouns generally changes how personal the headline is, which in this case does not qualify as a shift in formality
* **Inconsistent Style**: The style or tone is inconsistent within the revision (e.g. factual, dry information is paired with sensationalism)
        """)
    st.write("\n\n")

    comment_input = st.text_input(key = 10 * index + 8, label = "Comments (optional)", value="", help="Optional free text for comments and thoughts", max_chars=1000)

    if accuracy and style:
        next_input = st.button(key = 10 * index + 9, label="Next", help="Save this annotation and advance to the next one.")
    else:
        next_input = None

    return_sample = {
        "index": str(index),
        "original": question["original"],
        "revision": question["revision"],
    }
    
    return return_sample, accuracy, accuracy_subclass, style, style_subclass, comment_input, next_input

def skip_to_next_sample():
    return

def handle_next_button():
    return

def handle_back_button():
    return