import streamlit as st
from streamlit_annotation_tools import text_highlighter

from core.scripts.utils import display_progress, read_json_from_file, load_annotation, TASK_INFO


def format_sentence(sentence):
    return "***" + sentence.replace("[", ":blue-background[") + "***\n"

slider_labels = {
        1: "1",
        2: "2",
        3: "3",
        4: "4",
        5: "5"
}  # now that the string labels were replaced with numbers. this code is pretty dumb.

label_sliders = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5
}

slider_label_list = list(slider_labels.values())

def print_annotation_schema_sliders(subtask: str, index: int) -> tuple:
    """
    Prints the annotation schema for the annotation with the sliders. 

    :param subtask: str
    :param index: The number sample to show
    :return: The stuff to return
    """
    if subtask == "qualification":
        samples = read_json_from_file(TASK_INFO["span_task"]["qualification_filepath"])
    else:
        samples = read_json_from_file(TASK_INFO["span_task"]["annotation_filepath"])

    # ----------------- LOADING -----------------

    #sample_preload = load_annotation(subtask, index)
    #if not sample_preload:
    value_slider, value_nonsensical, value_comment = None, None, ""
    #else:
    #    value_slider, value_nonsensical, value_comment = (sample_preload["slider"], sample_preload["nonsensical"], sample_preload["comment"])
    #    if value_slider in slider_labels:
    #        value_slider = slider_labels[value_slider]
    #    else:
    #        value_slider = None

    question = samples[str(index)]
    # display the "Sample 1/5" thing
    display_progress(key=subtask)



    # ------------------- FIRST STORY PRINT -------------------------

    if question["focus_meaning"] == "meaning1":
        question["displayed_meaning_example"] = question["example1"]
    else:
        question["displayed_meaning_example"] = question["example2"]

    st.markdown("Read the following story")

    print(question)

    st.write("---")

    part1 = question["context"]["part1"]
    if "No text necessary" in part1:
        part1 = ""
    part3 = question["context"]["part3"]
    if "No text necessary" in part3:
        part3 = ""

    st.markdown(part1 + " " + format_sentence(question["sentence"]) + " " + part3)

    st.write("---")



    # --------------- PLAUSIBILITY RATING ---------------------

    st.markdown("Focus on the word: :blue-background[" + question["word"] + "].\n")


    st.write(f"""Given the context of the story, how plausible is the following meaning of the word?
    
    
#### {question["focus_meaning_gloss"]}
##### (as in: "{question["displayed_meaning_example"]}")
    """)

    slider_choice = st.segmented_control(
        "Select the plausibility of this meaning.",
        options=slider_label_list,
        selection_mode="single",
        default=value_slider,
        key = 50 * index + 3
    )

    if st.toggle("Show guidelines for rating plausibility", key = 50 * index + 5):
        st.markdown("""
**Annotate how plausible a meaning of a word is in the context of the short text using one of five scores:**

* **1**: The displayed meaning is not plausible at all given the context.
* **2**: The displayed meaning is theoretically conceivable, but less plausible than other meanings.
* **3**: The displayed meaning represents one of multiple, similarly plausible interpretations.
* **4**: The displayed meaning represents the most plausible interpretation; other meanings may still be conceivable.
* **5**: The displayed meaning is the only plausible meaning given the context.
        """)


    st.write("\n")

    # ---------------------------- REASONS ------------------------------------


    st.write(f"""Which of these best describes the reason for why you rated the word sense as you did? Pick (at least) 1. """)
    reason7 = None
    reason8 = None
    reason9 = None
    reason7_comment = ""
    reason9_comment = ""

    reason1_string = "There are words in the context that by themselves are associated with one of the meanings."
    if slider_choice in ["1", "2"]:
        reason1_string = "There are words in the context that by themselves are associated with another meaning."
    if slider_choice in ["4", "5"]:
        reason1_string = "There are words in the context that by themselves are associated with this meaning."

    reason1 = st.checkbox(label=reason1_string, value=False, key= 50 * index + 11,
                          help="This should be picked if there are words that are directly associated with one meaning. The association is obvious, no further thinking is required.")

    reason2_string = "The general premise or location makes a meaning more/less plausible."
    if slider_choice in ["1", "2"]:
        reason2_string = "The general premise or location makes another meaning more plausible."
    if slider_choice in ["4", "5"]:
        reason2_string = "The general premise or location makes this meaning plausible."

    reason2 = st.checkbox(label=reason2_string, value=False, key= 50 * index + 12,
                          help="This should be picked if the setting of the story fits better with a particular sense.")

    if reason2:
        reason7 = st.radio("What is the most deciding factor?", options=["It's because of the general setting of the story.", "It's because of the location of the story.", "It's because of who the characters in the story are.", "Something else. (Leave comment)"],
            index=None, key= 50 * index + 17)

        if reason7 == "Something else. (Leave comment)":
            reason7_comment = st.text_input(key = 50 * index + 20, label = "", value=value_comment, help="What is the most deciding factor?", max_chars=1000)

        

    reason3_string = "The events that occur make more/less sense with a certain meaning."
    if slider_choice in ["1", "2"]:
        reason3_string = "The events that occur make more sense with another meaning."
    if slider_choice in ["4", "5"]:
        reason3_string = "The events that occur make the most sense with this meaning."

    reason3 = st.checkbox(label=reason3_string, value=False, key= 50 * index + 13,
                          help="This should be picked if the words and setting aren't particularly associated with the meaning, but logically, one meaning makes more sense.")

    if reason3:
        reason9 = st.radio("How would you classify the type of reasoning you used?", index=None, options=["**Causal**: relating to expected causes and effects.", "**Temporal**: relating to time, sequences and durations.", "**Spatial**: relating to locations, directions and spatial relationships.", "**Social**: relating to expectations of how humans interact with each other.", "Something else. (Leave comment)"])

        if reason9 == "Something else. (Leave comment)":
            reason9_comment = st.text_input(key = 50 * index + 21, label = "", value=value_comment, help="What reasoning did you use?", max_chars=1000)

    reason4_string = "Given my background knowledge, I find that one meaning becomes more/less plausible."
    if slider_choice in ["1", "2"]:
        reason4_string =" Given my background knowledge, I find another meaning more plausible."
    if slider_choice in ["4", "5"]:
        reason4_string = "Given my background knowledge, I find this meaning plausible."

    reason4 = st.checkbox(label=reason4_string, value=False, key= 50 * index + 14,
                          help="You should pick this if your rating was influenced by your background knowledge. If it's something everyone knows, you should pick another option.")

    reason5 = st.checkbox(label="I can imagine multiple interpretations, but there aren't really any hints in the context.", value=False, key= 50 * index + 15,
                          help="You should pick this if multiple meanings are equally plausible to you, or if you can't explain from the context why one is more plausible.")


    if reason5 and slider_choice != "3":
        reason8_label = "Why do you rate the displayed meaning as less plausible?"
        if slider_choice in ["4", "5"]:
            reason8_label = "Why do you rate the displayed meaning as more plausible?"

        reason8 = st.radio(reason8_label, options=["I find one meaning more plausible, because it's the more common meaning.", "I find one meaning more plausible, because the phrasing is more intuitive.", "I find one meaning more plausible for no particular reason."],
                           index=None, key= 50 * index + 18)

    if slider_choice == "5":
        reason6 = st.checkbox(label="I don't understand what the other meanings of that word would be.", value=False, key= 50 * index + 16,
                            help="ONLY pick this if you don't know the other meanings of the word.")
    else:
        reason6 = None


    has_annotated_reasons = (reason1) or (reason2 and reason7) or (reason3) or (reason4) or (reason5 and reason8) or reason6
    annotated_reasons  = {
        "keywords": reason1,
        "premise": reason2,
        "premise_reason": reason7,
        "premise_comment": reason7_comment,
        "logic": reason3,
        "logic_reason": reason9,
        "logic_comment": reason9_comment,
        "knowledge": reason4,
        "equal": reason5,
        "equal_reason": reason8,
        "idk": reason6
    }


    # ----------------------------- NONSENSICAL INPUT ---------------------------

    nonsense_input = None#st.checkbox(key = 10 * index + 4, label = "Check this box if the text is nonsensical.", value=value_nonsensical)
    #st.write("\n\n")



    # ---------------------------- HIGHLIGHTING -----------------------------------

    text = " \n\n" + part1 + " " + question["sentence"] + " " + part3 + " \n\n "

    prehighlight = [
        [
            {"start": 0, "end": 0, "label": "Mark words by selecting them with the mouse cursor."},
            {"start": len(text), "end": len(text), "label": "Mark words by selecting them with the mouse cursor."},
        ],
    ]

    st.write("Now please go through the story again and mark the words that influenced your decision for the reasons you gave above.")

    st.write("---")

    st.write("Select spans of text in the story below by holding left-click and dragging the mouse cursor over them. Mark a word again to undo. (You don't need to press the orange buttons)")

    annotations = text_highlighter(text, highlights=prehighlight)

    st.write("---")

    print(annotations)


    #------------------------------- COMMENTS --------------------------------

    comment_input = st.text_input(key = 50 * index + 8, label = "Comments (optional)", value=value_comment, help="Optional free text for comments and thoughts", max_chars=1000)

    if slider_choice and has_annotated_reasons:
        next_input = st.button(key = 50 * index + 9, label="Next", help="Save this annotation and advance to the next one.")
    else:
        next_input = None
        st.write("You need to at least indicate a reason and select a plausibility rating to advance to the next sample.")

    if slider_choice:
        slider_choice = label_sliders[slider_choice]

    return_sample = {
        "index": str(index),
        "sentence": question["sentence"],
        "context": question["context"],
        "word": question["word"],
        "focus_meaning": question["focus_meaning"],
    }
    
    return return_sample, slider_choice, annotated_reasons, annotations, comment_input, next_input
