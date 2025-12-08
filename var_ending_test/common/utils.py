import json
import streamlit as st

from core.scripts.utils import display_progress, read_json_from_file, load_annotation, TASK_INFO

with open("var_ending_test/resources/tutorial_text.json", "r") as f:
    tutorial_texts = json.load(f)

def reset_sample_state():
    st.session_state["sample_state"] = {"Beginning": "Select the first part.", "Ending": "Select the second part.",
                                         "editing": {"Beginning": False, "Ending": False},
                                         "choice": {"Beginning": "Select the first part.", "Ending": "Select the second part."}}
    st.session_state["tutorial_stage"] = 0

if "sample_state" not in st.session_state:
    reset_sample_state()

print("running utils...")

def format_sentence(sentence):
    return "***" + sentence.replace("[", ":blue-background[") + "***\n"


def sentence_selection_box(sentences, index, part="Beginning"):
    if "sample_state" not in st.session_state: # no idea why this is necessary. man
        reset_sample_state()
        
    if not st.session_state["sample_state"]["editing"][part]:
        radio_selection = st.radio(part + ":", options=[st.session_state["sample_state"][part]] + sentences, key=index)
        if radio_selection != st.session_state["sample_state"][part]:
            st.session_state["sample_state"]["choice"][part] = radio_selection
            #print("updating selection state...")
            #st.rerun()

        if part == "Beginning" and st.session_state["tutorial_stage"] == 1:
            st.write(tutorial_texts['1'])
        elif part == "Beginning" and st.session_state["tutorial_stage"] == 2:
            st.write(tutorial_texts["2"])
        elif part == "Beginning" and st.session_state["tutorial_stage"] == 3:
            st.write(tutorial_texts["3"])

        if st.button("Edit selected sentence", key=index+1005):
            st.session_state["sample_state"]["editing"][part] = True
            st.session_state["sample_state"][part] = radio_selection
            st.rerun()
    else:
        custom_text = st.text_area("Write your edit here and confirm by pressing the button below.", value=st.session_state["sample_state"][part])
        if st.button("Confirm", key=index + 2006):
            st.session_state["sample_state"][part] = custom_text
            st.session_state["sample_state"]["editing"][part] = False
            st.session_state["sample_state"]["choice"][part] = custom_text
            st.rerun()
    


def print_annotation_schema(subtask: str, index: int) -> tuple:
    """
    Prints the annotation schema that is seen on the qualification and annotation page.

    :param subtask: qualification or annotation
    :param index: The number sample to show
    :return: The sentence and widget inputs in the order they are displayed to the user.
    """
    in_tutorial = False
    if subtask=="tutorial":
        in_tutorial = True


    if subtask == "qualification":
        samples = read_json_from_file(TASK_INFO["var_ending_test"]["qualification_filepath"])

        # load values previously filled in checkboxes or None if this is first time annotating this sample
        sample_preload = load_annotation(subtask, index)
        if sample_preload is None:
            value_checkbox1, value_checkbox2, value_textinput1, value_checkbox3, value_textinput2 = None, None, "", None, ""
        else:
            value_checkbox1, value_checkbox2, value_textinput1, value_checkbox3, value_textinput2 = (sample_preload["meaning1"], sample_preload["meaning2"], None, None, None)
        
        question = samples[str(index)]
        # display the "Sample 1/5" thing
        display_progress(key=subtask)

        st.markdown("Read the following story:")

        st.markdown("**" + question["precontext"] + "**")
        st.markdown(format_sentence(question["sentence"]))

        st.markdown("Focus on the highlighted word: :blue-background[" + question["word"] + "].\n")
        st.write("Which of these is more plausible?")
        checkbox1 = st.checkbox(key = 10 * index + 1, label=question["meaning1"], value=value_checkbox1)
        checkbox2 = st.checkbox(key = 10 * index + 2, label=question["meaning2"], value=value_checkbox2)

        if (checkbox1 or checkbox2) and not (checkbox1 and checkbox2):
            next_input = st.button(key = 10 * index + 9, label="Next", help="Save this annotation and advance to the next one.")
        else:
            next_input = None

        return question, checkbox1, checkbox2, next_input

    else:  # annotation and tutorial
        if subtask == "annotation":
            samples = read_json_from_file(TASK_INFO["var_ending_test"]["annotation_filepath"])
        else:
            samples = read_json_from_file(TASK_INFO["var_ending_test"]["tutorial_filepath"])

        # load values previously filled in checkboxes or None if this is first time annotating this sample
        sample_preload = load_annotation(subtask, index)
        if sample_preload is None:
            value_textbox1, value_textbox2 = "", ""
        else:
            value_textbox1, value_textbox2 = (sample_preload["ending"], sample_preload["comment"])

        display_progress(key=subtask)

        question = samples[str(index)]
        
        if subtask == "annotation":

            st.markdown(f"""
The following sentence contains the word {question["word"]}, which has these two meanings:

- {question["meaning1"]}

- {question["meaning2"]}

Use and edit the story building blocks so that the slightly more plausible sense of the word in this context becomes:

- {question["focus_meaning"]}

-------
            """)

        additional_choices_precontext = ["(No beginning necessary)"]
        additional_choices_ending = ["(No ending necessary)"]

        if in_tutorial:
            st.write(tutorial_texts["0"])
        
        # precontext
        sentence_selection_box(sentences=additional_choices_precontext + question["precontexts"], index=index*10+1, part="Beginning")

        if in_tutorial and st.session_state["tutorial_stage"] == 4:
            st.write(tutorial_texts["4"])

        sentence_box = st.radio("Central Sentence: (Cannot be changed)", options=[question["sentence"]], key=index*10+2)

        sentence_selection_box(sentences=additional_choices_ending + question["endings"], index=index*10+3, part="Ending")
                                
        if in_tutorial and st.session_state["tutorial_stage"] == 5:
            st.write(tutorial_texts["5"])
        elif in_tutorial and st.session_state["tutorial_stage"] == 6:
            st.write(tutorial_texts["6"])

        picked_precontext = st.session_state["sample_state"]["choice"]["Beginning"]
        picked_ending = st.session_state["sample_state"]["choice"]["Ending"]

        st.markdown(f"""
---------
Your constructed story:
                    
{"" if picked_precontext=="(No beginning necessary)" else picked_precontext} {sentence_box} {"" if picked_ending== "(No ending necessary)" else picked_ending}
---------
        """)

        if in_tutorial and st.session_state["tutorial_stage"] == 6:
            st.write(tutorial_texts["7"])

        next_input = False
        if not in_tutorial:
            if picked_precontext == "Select the first part.":
                st.write(":red[You need to select an option for the first part.]")
            elif picked_ending == "Select the second part.":
                st.write(":red[You need to select an option for the second part.]")
            elif question["word"] in picked_precontext:
                st.write(f":red[Your constructed story contains the focus word {question["word"]} in the first part. Please avoid that.]")
            elif question["word"] in picked_ending:
                st.write(f":red[Your constructed story contains the focus word {question["word"]} in the second part. Please avoid that.]")
            else:

                next_input = st.button(key = 10 * index + 9, label="Next", help="Save this story and advance to the next one.")

        return picked_precontext, sentence_box, picked_ending, next_input
