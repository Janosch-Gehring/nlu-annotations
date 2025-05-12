import streamlit as st

from core.scripts.utils import display_progress, read_json_from_file, load_annotation, TASK_INFO


def format_sentence(sentence):
    return "***" + sentence.replace("[", ":blue-background[") + "***\n"

slider_labels = {
        1: "Definitiv nicht",
        2: "Abwegig",
        3: "Schwer zu sagen",
        4: "Plausibel",
        5: "Ganz eindeutig"
}

label_sliders = {
    "Definitiv nicht": 1,
    "Abwegig": 2,
    "Schwer zu sagen": 3,
    "Plausibel": 4,
    "Ganz eindeutig": 5
}

slider_label_list = list(slider_labels.values())

def print_annotation_schema_sliders(subtask: str, index: int) -> tuple:
    """
    Prints the annotation schema for the annotation with the sliders. 

    :param subtask: str
    :param index: The number sample to show
    :return: The stuff to return
    """
    samples = read_json_from_file(TASK_INFO["big_eval_ending_task"]["annotation_filepath"])

    
    value_slider, value_nonsensical, value_comment = None, None, ""

    question = samples[str(index)]
    # display the "Sample 1/5" thing
    display_progress(key=subtask)


    if question["judged_meaning"] == question["sentence_info"]["meaning1"]:
        question["displayed_meaning_example"] = question["sentence_info"]["meaning1_example"]
    else:
        question["displayed_meaning_example"] = question["sentence_info"]["meaning2_example"]


    st.markdown("")

    st.write("---")

    st.markdown(question["precontext"] + " " + format_sentence(question["sentence"]) + " " + question["ending"])

    st.write("---")

    st.markdown("Konzentriere dich auf das Wort: :blue-background[" + question["word"] + "].\n")


    st.write(f"""Für wie plausibel hältst du es, dass das Wort "{question["word"]}" in diesem Kontext diese Bedeutung hat:
    
    
#### {question["judged_meaning"]}
##### (wie z.B. in: "{question["displayed_meaning_example"]}")
    """)

    slider_choice = st.segmented_control(
        "Wähle aus:",
        options=slider_label_list,
        selection_mode="single",
        default=value_slider,
        key = 10 * index + 3
    )

    if slider_choice:
        next_input = st.button(key = 10 * index + 9, label="Weiter")
    else:
        next_input = None

    if slider_choice:
        slider_choice = label_sliders[slider_choice]

    return_sample = {
        "index": str(index),
        "sentence": question["sentence"],
        "ending": question["ending"],
        "word": question["word"],
        "judged_meaning": question["judged_meaning"]
    }
    
    return return_sample, slider_choice, next_input
