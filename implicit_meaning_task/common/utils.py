import re
import streamlit as st
from core.scripts.utils import display_progress, load_annotation, TASK_INFO

def remove_punctuation(text: str) -> str:

    text = " ".join(text.split("\n"))
    return re.sub(r"[”#*\+/<=>\[\]\\^_`{|}~]", "", text)


def format_sample(question: dict) -> None:

    def labeled_paragraph(label, text, font_size="16px", font_weight="normal", indent="45"):
        st.markdown(
            f"""
            <div style="margin-left: 0; padding-left: {indent}px; text-indent: -{indent}px; font-size: {font_size}; font-weight: {font_weight}">
                <span style="background-color: rgba(210, 215, 225, 0.32); color: inherit; padding: 2px 4px; border-radius: 4px;">
                    {label}
                </span>
                {text}
            </div>
            """,
            unsafe_allow_html=True
        )

    match = re.findall(r"<(.*)>", question["sentence_2"])
    blue_background = re.sub(r"<.*>", f'<span style="background-color: #1e3a56;\
            color: white;\
            padding: 2px 2px;\
            border-radius: 5px;">{match[0]}</span>', question["sentence_2"])
    # formatted_string = f"**S1:** {question["sentence_1"]}\n##### **S2:** {blue_background}\n\n:grey-background[*Article name:*] &emsp;{question["article_name"]}\n\n:grey-background[*Context before:*] &nbsp;{question["context_before"]}\n\n:grey-background[*Context after:*] &emsp;{question["context_after"]}"
    # return formatted_string

    labeled_paragraph("S1:", "&nbsp;" + question["sentence_1"], font_size="20px", font_weight="bold")
    st.markdown("<div style='height: 1.2em;'></div>", unsafe_allow_html=True)  # vertical space
    labeled_paragraph("S2:", "&nbsp;" + blue_background, font_size="20px", font_weight="bold")
    st.markdown("<div style='height: 2em;'></div>", unsafe_allow_html=True)  # vertical space
    labeled_paragraph("Article Name:", "&emsp;&ensp;" + question["article_name"])
    st.markdown("<div style='height: 1.2em;'></div>", unsafe_allow_html=True)  # vertical space
    labeled_paragraph("Context Before:", "&ensp;" + remove_punctuation(question["context_before"]), indent="124")
    st.markdown("<div style='height: 1.2em;'></div>", unsafe_allow_html=True)  # vertical space
    labeled_paragraph("Context After:", "&emsp;&nbsp;" + remove_punctuation(question["context_after"]), indent="122")
    st.markdown("<div style='height: 3em;'></div>", unsafe_allow_html=True)  # vertical space

def check_all_checkboxes(implicit: str, checkboxes: list, comment: str) -> bool:

    if implicit == "No":
        return True
    elif implicit == "Yes" and checkboxes[-1]:
        if comment:
            return True
    elif implicit == "Yes" and len([box for box in checkboxes[:-1] if box]) >= 1:
        return True
    else:
        return False


def print_annotation_schema(samples: dict, index: int, subtask: str="annotation") -> tuple[dict, str, list, str, str, bool]:
    """
    Prints the annotation schema that is seen on the qualification and annotation page.

    :param subtask: qualification or annotation
    :param index: The number sample to show
    :return: The sentence and widget inputs in the order they are displayed to the user.
    """
    question = samples[str(index)]
    # # display the "Sample 1/5" thing
    display_progress(key=subtask)

    st.markdown("Read the following sentences and the contexts.\n")
    format_sample(question)

    # load values previously filled in checkboxes or None if this is first time annotating this sample
    sample_preload = load_annotation(subtask, index)
    if sample_preload is None:
        implicit_val, context_val, reasoning_val, complement_val, instruction_val, other_val = None, None, None, None, None, None
        comment_implicit_val, comment_not_implicit_val = "", ""
    else:
        implicit_val, context_val, reasoning_val, complement_val, instruction_val, other_val = (sample_preload["implicit_meaning"], 
                                                                                                sample_preload["if_implicit"][0], 
                                                                                                sample_preload["if_implicit"][1], 
                                                                                                sample_preload["if_implicit"][2], 
                                                                                                sample_preload["if_implicit"][3], 
                                                                                                sample_preload["if_implicit"][4]
                                                                                                )
        comment_implicit_val, comment_not_implicit_val = (sample_preload["comment_implicit"], sample_preload["comment_not_implicit"])


    context, reasoning, complement, instruction, other = False, False, False, False, False
    comment_implicit, comment_not_implicit = "", ""
    # implicit = st.radio(
    #     ":grey-background[Does the first sentence implicitely convey the same meaning as the second one?]",
    #     ["Yes", "No"],
    #     key="implicit",
    #     horizontal=True,
    #     index=None,)

    st.markdown(":grey-background[Does the first sentence implicitly convey the same meaning as the second one?]")

    implicit = st.segmented_control("", ["Yes", "No"], key=10 * index + 1, default=implicit_val)
    # col1, col2 = st.columns(2)
    # with col1:
    #     implicit = st.checkbox(key=10 * index + 1, label="Yes", value=None)
    # with col2:
    #     not_implicit = st.checkbox(key=10 * index + 2, label="No", value=None) 
    if implicit == "Yes":
        st.markdown("Please specify one or multiple reasons for your choice:")

        col1, col2 = st.columns(2)

        with col1:
            context = st.checkbox(key=10 * index + 2, label="Context", value=context_val)
            reasoning = st.checkbox(key=10 * index + 3, label="Logical Reasoning", value=reasoning_val)
            complement = st.checkbox(key=10 * index + 4, label="Omitted Complement", value=complement_val)
            instruction = st.checkbox(key=10 * index + 5, label="Recoverable Instruction", value=instruction_val)

        with col2:
            other = st.checkbox("Other", value=other_val)
            comment_implicit = st.text_input(key=10 * index + 6, label="If applicable, specify other reasons that led to your decision:", value=comment_implicit_val)
            if comment_implicit:
                st.write(r"$\textsf{\scriptsize Thanks for your input!}$")
    else:
        comment_not_implicit = st.text_input(key=10 * index + 7, label="If you are unsure, select \"No\" and explain your thoughts here:", value=comment_not_implicit_val)
        if comment_not_implicit:
            st.write(r"$\textsf{\scriptsize Thanks for your input!}$")

    checkboxes = [context, reasoning, complement, instruction, other]
    if check_all_checkboxes(implicit, checkboxes, comment_implicit):
        next_input = st.button(key = 10 * index + 8, label="Next", help="Save this annotation and advance to the next one.")
    else:
        next_input = None

    return question, implicit, checkboxes, comment_implicit, comment_not_implicit, next_input