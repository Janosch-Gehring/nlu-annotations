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
        key = 50 * index + 1
    )

    if st.toggle("Show guidelines for rating plausibility", key = 50 * index + 2):
        st.markdown("""
**Annotate how plausible a meaning of a word is in the context of the short text using one of five scores:**

* **1**: The displayed meaning is not plausible at all given the context.
* **2**: The displayed meaning is theoretically conceivable, but less plausible than other meanings.
* **3**: The displayed meaning represents one of multiple, similarly plausible interpretations.
* **4**: The displayed meaning represents the most plausible interpretation; other meanings may still be conceivable.
* **5**: The displayed meaning is the only plausible meaning given the context.
        """)


    st.write("\n")

    slider_reason_labels = ["Not at all", "A little", "Somewhat", "A lot", "Almost entirely"]

    reason_story = None
    reason_logic = None
    reason_properties = None
    reason_location = None
    reason_characters = None
    reason_events = None
    reason_setting = None
    reason_other = None
    reason_story_other_comment = None
    reason_common = None
    reason_domain = None
    reason_causal = None
    reason_temporal = None
    reason_social = None
    reason_logic_other = None
    reason_logic_other_comment = None
    reason_other = None

    # ---------------------------- REASONS ------------------------------------

    st.write("What shaped your rating? (Both can be high)")

    reason_story = st.segmented_control(
        "How much did the story itself shape your rating?",
        options=slider_reason_labels,
        selection_mode="single",
        default=None,
        key = 50 * index + 3
    )

    if reason_story not in [None, slider_reason_labels[0]]:

        st.write("What in the story? (Check all that apply)")

        reason_location = st.checkbox(label="**Location**: The physical place where the story happens.", key = 50 * index + 4, 
                                      help="**Example**: *At the baseball stadium, for some reason, I keep staring at the [bats].*  \n Given the location, a baseball bat seems very plausible.")

        reason_characters = st.checkbox(label="**Characters**: Who is involved, and what they do or are like.", key = 50 * index + 5, 
                                        help="**Example**: *The student complained about the wrong [note].  \n Given that the character is a student, the 'grade'-note meaning becomes more plausible than the 'music'-note meaning.")

        reason_properties = st.checkbox(label="**Properties**: What things are involved, and what the story says about them.", key = 50 * index + 22, 
                                        help="**Example**: *I found a [bat]. The wings are broken.*  \n It refers to the animal because they have wings. You can also use this category for other properties, such as size, appearance, functions, etc.")

        reason_events = st.checkbox(label="**Event**: What happens in the story.", key = 50 * index + 6, 
                                    help="**Example**: *When the lights went out, a [bat] flew past his face.  \n The events that happen appear more plausible if bat is an animal.")

        reason_setting = st.checkbox(label="**General Setting**: The overall situation or activity, beyond the specific place.", key = 50 * index + 7, 
                                     help="**Example**: *During their piano practice, she looked through the [notes].*  \n The described activity implies the music-related meaning of 'notes'.")

        reason_story_other = st.checkbox(label="**Other**: Anything else in the story. Describe below.", key = 50 * index + 8, help="")

        if reason_story_other:
            reason_story_other_comment = st.text_input(key = 50 * index + 9, label = "What in the story shaped your rating?", max_chars=500)



    reason_logic = st.segmented_control(
        "How much did you rely on things the story doesn't explicitly state?",
        options=slider_reason_labels,
        selection_mode="single",
        default=None,
        key = 50 * index + 10
    )

    if reason_logic not in [None, slider_reason_labels[0]]:

        st.write("What kind of knowledge or reasoning? (Check all that apply)")

        reason_common = st.checkbox(label="**Most familiar meaning**: It's the word's more common meaning.", key = 50 * index + 11, 
                                    help="**Example**: *That thing was so [lousy].  \n 'Lousy' probably means 'bad' instead of 'infested with lice', because that meaning is just not as common.")

        reason_domain = st.checkbox(label="**Domain**: Knowledge in a specific field (e.g. medicine, sports, law)", key = 50 * index + 12, help="")

        reason_causal = st.checkbox(label="**Causal**: What tends to cause or result from what.", key = 50*index + 13, help="")

        reason_spatial = st.checkbox(label="**Spatial**: Sizes, distances and how things are positioned.", key = 50 * index + 14, help="")

        reason_temporal = st.checkbox(label="**Temporal**: The order, timing and duration of things.", key = 50 * index + 15, help="")

        reason_social = st.checkbox(label="**Social**: What people usually feel, intend or how they interact.", key = 50 * index + 16, help="")

        reason_logic_other = st.checkbox(label="**Other**: Any other kind of knowledge or reasoning. Describe below.", key = 50 * index + 17)

        if reason_logic_other:
            reason_logic_other_comment = st.text_input(key = 50 * index + 18, label = "What shaped your rating?", max_chars=500)

    if reason_logic in [slider_reason_labels[0]] and reason_story in [slider_reason_labels[0]]:

        reason_other = st.text_input(key = 50 * index + 19, label = "Something else shaped your rating? Describe it below.", help="If it is neither implicit nor explicit information in the story, what influenced your rating?")

    has_annotated_reasons = ((reason_story) and (reason_logic) and 
                             (reason_story and (reason_location or reason_characters or reason_events or reason_setting or (reason_story_other and reason_story_other_comment))) or
                             (reason_logic and (reason_domain or reason_causal or reason_temporal or reason_social or reason_spatial or (reason_logic_other and reason_logic_other_comment))) or
                             reason_other)

    annotated_reasons = {
        "story": reason_story,
        "logic": reason_logic,
        "location": reason_location,
        "characters": reason_characters,
        "events": reason_events,
        "properties": reason_properties,
        "setting": reason_setting,
        "story_other": reason_other,
        "story_comment": reason_story_other_comment,
        "common": reason_common,
        "domain": reason_domain,
        "causal": reason_causal,
        "temporal": reason_temporal,
        "social": reason_social,
        "logic_other": reason_logic_other,
        "logic_comment": reason_logic_other_comment,
        "other": reason_other
    }


    # ----------------------------- NONSENSICAL INPUT ---------------------------

    nonsense_input = None#st.checkbox(key = 10 * index + 4, label = "Check this box if the text is nonsensical.", value=value_nonsensical)
    #st.write("\n\n")



    # ---------------------------- HIGHLIGHTING -----------------------------------

    text = "  \n\n" + part1 + " " + question["sentence"] + " " + part3 + "  \n\n "

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

    comment_input = st.text_input(key = 50 * index + 20, label = "Comments (optional)", value=value_comment, help="Optional free text for comments and thoughts", max_chars=1000)

    if slider_choice and has_annotated_reasons:
        next_input = st.button(key = 50 * index + 21, label="Next", help="Save this annotation and advance to the next one.")
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
