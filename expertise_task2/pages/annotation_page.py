import os

import streamlit as st
import random

from core.scripts import user_repository
from core.scripts.utils import display_progress, read_json_from_file, handle_next_button, handle_back_button, TASK_INFO, skip_to_next_sample, load_annotation


samples = read_json_from_file(TASK_INFO["expertise_task2"]["annotation_filepath"])



def print_annotation_schema_connections(samples, index):
    """
    Print annotation schema for connect-the-concept type annotatoin.
    """
    domain = st.session_state.domain_list[index]
    question = samples[domain]
    # display the "Sample 1/5" thing
    display_progress(key="annotation")

    st.markdown("""**Connect the terms on the left with the category that best describes it on the right. For example, if one of the terms on the left is 'cat', you should look for a fitting category such as 'feline' or 'mammal'.**
                
Many of the terms in this study will be rather obscure. You are not expected to know most terms. 
Once you finished connecting the terms that you know, you can press the 'I don't know the other terms' button. *Do not blindly guess or use search engines. Only connect terms that you feel somewhat confident about.*
                
Each term belongs to one category, and each category belongs to one term. If there are more terms than categories, then a category may fit multiple terms. You can use process of elimination to connect the last term.
                
You will not be rejected for knowing too little or too much, and it is okay to make mistakes. The most important thing is that you give it an honest shot without cheating or blindly guessing.
                    
To connect a word, first click on the term on the left side, then click on the category on the right. The connection will be displayed below.

There are 21 groups of 5 terms in total. Have fun!
                    
**Please note: Please do not leave/refresh the page or stay inactive for a prolonged period of time, or you will lose progress.**
                """)
    
    print(question)

    list_of_terms = [x[1] for x in question]
    print(list_of_terms)
    list_of_categories = list(set(x[3] for x in question))
    print(list_of_categories)

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Terms")
        for item in list_of_terms:
            if item in [x[0] for x in st.session_state.connections]:
                disable_item = True
            else:
                disable_item = False
            if st.session_state.clipboard == item:
                color = "primary"
            else:
                color = "secondary"

            if st.button(item, key=f"{20*index}_a_{item}", disabled=disable_item, type=color):
                st.write(f"Connect {item} with what?")
                st.session_state.clipboard = item

    with col_right:
        st.subheader("Categories")
        for item in list_of_categories:
            categories_disabled = False
            if not st.session_state.clipboard:
                categories_disabled = True
            if st.button(item, key=f"{20*index}_b_{item}", disabled=categories_disabled):
                if st.session_state.clipboard:  # JUST TO BE SURE
                    st.write(f"{st.session_state.clipboard} connected to {item}!")
                    st.session_state.connections.append([st.session_state.clipboard, item])
                    st.session_state.clipboard = None
                    st.rerun()
                


    st.write("Current connections:")
    for term, category in st.session_state.connections:
        st.write(f"{term} -> {category}")

    if st.button("Reset these connections (Start this page from beginning)", key=20 * int(index) + 18):
        st.session_state.connections = []
        st.session_state.clipboard = None
        st.rerun()

    st.write("When you're finished or stuck, press the button below.")

    if len(st.session_state.connections) == 0:
        label = "I don't know any of these words"
    elif len(st.session_state.connections) < 5:
        label = "I don't know the other words"
    else:
        label = "Next"
    next_input = st.button(key = 20 * int(index) + 19, label=label, help="Save this annotation and advance to the next one.")

    st.write("The terms above will update when you click the button. Be careful not to double-click it!")

    return st.session_state.connections, next_input

def print_annotation_schema(samples, index):
    """
    Prints the annotation schema for the annotation
    """
    
    domain = st.session_state.domain_list[index]
    question = samples[domain]
    # display the "Sample 1/5" thing
    display_progress(key="annotation")

    st.markdown("""**Tell us if you are familiar with the following terms.**
                
To be 'familiar' with a term, you must have heard of it before and have an understanding of the concept, but you are not expected to know the details or definition. 
For example, if the term is 'cello', you may say you are familiar with it if you at least know that it is some type of string instrument.
                
The purpose of this study is simply to check the familiarity of English speakers with these terms. There is no point in cheating or lying, so please be honest. 
You probably won't be familiar with most of the words, and we promise you will not get rejected for 'knowing too little' or anything like that.
                
There are 105 terms in total. Have fun!
                
**Please note: Please do not leave/refresh the page or stay inactive for a prolonged period of time, or you will lose progress.**
                """)


    st.write("\n")

    radio_outputs = {}
    for i, (wn_id, word, sc) in enumerate(question):
        radio_outputs[word] = "-"
    
    for i, (wn_id, word, sc) in enumerate(question):
        radio_outputs[word] = st.radio(label=word, options=["Familiar", "Not familiar"], index=None, key=int(index)*10 + i)

    if not None in list(radio_outputs.values()):
        next_input = st.button(key = 10 * int(index) + 9, label="Next", help="Save this annotation and advance to the next one.")
    else:
        next_input = None
    
    return radio_outputs, next_input

def handle_next_button(annotation, index, samples):
    user_repository.save_one_annotation(st.session_state.user_id, "annotation", index+1, annotation)

    if st.session_state.progress > 19:
        user_repository.mark_as_done(st.session_state.user_id)
        st.rerun()
    else:
        st.session_state.progress += 1

    st.rerun()

if "clipboard" not in st.session_state:
    st.session_state.clipboard = None

if "connections" not in st.session_state:
    st.session_state.connections = []

if "progress" not in st.session_state:
    st.session_state.progress = user_repository.get_checkpoint("annotation")
    if not st.session_state.progress:  # no checkpoint yet -> simply go to the first relevant sample

        # user will get a random sample order upon first visit.
        domains = list(samples)
        random.shuffle(domains)

        for domain in samples.values():
            random.shuffle(domain)

        randomized_samples = {k: samples[k] for k in domains}

        st.session_state.samples = randomized_samples
        st.session_state.domain_list = list(randomized_samples.keys())

        st.session_state.progress = 0

        user_repository.save_one_annotation(st.session_state.user_id, "samples", 1, randomized_samples)

st.session_state.page = "expertise_sample" + str(st.session_state.progress)

if user_repository.check_if_done(st.session_state.user_id):
    st.write("## You have finished annotation. \n\nThank you for your time!")
    st.write("\n\n\n")
    st.write("**Your Prolific Completion Code:**")
    st.write("# " + os.getenv("PROLIFIC_COMPLETION_CODE"))
else:
    index = int(st.session_state.progress)

    back_button = None#st.button(label="Back", key = 10 * index + 7, help="Go back to the previous sample.")

    if "samples" not in st.session_state:
        st.write("(Note: Using Failsafe after leaving page. You may experience unexpected behavior.)")
        st.session_state.samples = load_annotation("samples", 1)
        st.session_state.domain_list = list(st.session_state.samples.keys())

    choices, next_input = print_annotation_schema_connections(st.session_state.samples, index)
    domain = st.session_state.domain_list[index]
    annotation = {"domain": domain, "choices": choices}

    if next_input:
        st.session_state.connections = []
        st.session_state.clipboard = None
        handle_next_button(annotation, index, st.session_state.samples)