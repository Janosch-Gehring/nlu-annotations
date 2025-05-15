import streamlit as st

with open("implicit_meaning_task/resources/annotation_guidelines_implicit_meaning.md", "r") as md:
    markdown = md.read()

split_md = markdown.split("==SPLIT==")
first_md, second_md = split_md[0], split_md[1]

st.write(first_md)
st.write("")
st.write("")
st.markdown(":grey-background[Does the first sentence implicitly convey the same meaning as the second one?]")

implicit = st.segmented_control("", ["Yes", "No"])

if implicit == "Yes":
    st.markdown("Please specify one or multiple reasons for your choice:")

    col1, col2 = st.columns(2)

    with col1:
        context = st.checkbox(label="Context")
        reasoning = st.checkbox(label="Logical Reasoning")
        complement = st.checkbox(label="Omitted Complement")
        instruction = st.checkbox(label="Recoverable Instruction")

    with col2:
        other = st.checkbox("Other")
        comment_implicit = st.text_input(label="Specify any other reason that led to your decision:")
        if comment_implicit:
            st.write(r"$\textsf{\scriptsize Thanks for your input!}$")
else:
    comment_not_implicit = st.text_input(label="If you are unsure, select \"No\" and explain your thoughts here:")
    if comment_not_implicit:
        st.write(r"$\textsf{\scriptsize Thanks for your input!}$")


st.write("If you are ready to proceed with the guidelines, click the button below.")
if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

st.button('Proceed', on_click=click_button)

if st.session_state.clicked:
    st.write(second_md)