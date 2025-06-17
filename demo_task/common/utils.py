import streamlit as st
import copy

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


def get_and_increment_counts(question_id, pred=None):

    conn = st.session_state.conn
    cursor = conn.cursor()

    # find annotator group
    cursor.execute("SELECT * from frequencies WHERE question_id=%s", (question_id,))
    data = cursor.fetchone()

    counts = [data[1], data[2], data[3], data[4], data[5]]
    precounts = copy.deepcopy(counts)

    if pred:
        counts[pred-1] += 1

        if pred == 1:
            cursor.execute("UPDATE frequencies SET count1=%s WHERE question_id=%s", (counts[pred-1], question_id))
        # oh god am i really gonna do it like this
        elif pred == 2:
            cursor.execute("UPDATE frequencies SET count2=%s WHERE question_id=%s", (counts[pred-1], question_id))
        elif pred == 3:
            cursor.execute("UPDATE frequencies SET count3=%s WHERE question_id=%s", (counts[pred-1], question_id))
        elif pred == 4:
            cursor.execute("UPDATE frequencies SET count4=%s WHERE question_id=%s", (counts[pred-1], question_id))
        elif pred == 5:
            cursor.execute("UPDATE frequencies SET count5=%s WHERE question_id=%s", (counts[pred-1], question_id))

    conn.commit()

    return counts, precounts

def print_annotation_schema_sliders(subtask: str, index: int) -> tuple:
    """
    Prints the annotation schema for the annotation with the sliders. 

    :param subtask: str
    :param index: The number sample to show
    :return: The stuff to return
    """
    samples = read_json_from_file(TASK_INFO["demo_task"]["qualification_filepath"])

    value_slider = None
    question = samples[str(index)]


    if question["judged_meaning"] == question["sentence_info"]["meaning1"]:
        question["displayed_meaning_example"] = question["sentence_info"]["meaning1_example"]
    else:
        question["displayed_meaning_example"] = question["sentence_info"]["meaning2_example"]


    st.markdown("Sieh dir den folgenden Text an:")

    print(question)

    st.write("---")

    st.markdown("#### " + question["precontext"] + " " + question["sentence"] + " " + question["ending"])

    st.write("---")

    st.markdown("Achte auf das Wort: :blue-background[" + question["word"] + "].\n")


    st.write(f"""Für wie plausibel hältst du hier diese Bedeutung des Wortes:
    
    
#### {question["judged_meaning"]}
    """)

    slider_choice = st.segmented_control(
        "Gar nicht ---- Möglich ---- Definitiv",
        options=slider_label_list,
        selection_mode="single",
        default=value_slider,
        key = 10 * index + 3
    )

    st.write("\n")

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
