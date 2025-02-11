
import streamlit as st

st.session_state.page = "main_page"

if not st.session_state.user_id:
    st.markdown("""
    # Welcome!
                
    This is the annotation website for the Natural Language Understanding Lab at UTN Nuremberg.

    ## Are you here for annotation?
                
    If you were redirected here for the purpose of annotation, find the 'Log In' option in the sidebar to your left.
    Then, enter the unique annotator ID that we shared with you.
    Once you have successfully logged in, new options will become available to you so you can start reading the introduction and taking the qualification test.
    """)

else:
    st.markdown("""
    # Welcome!
                
    This is the annotation website for the Natural Language Understanding Lab at UTN Nuremberg.

    ## Are you here for annotation?
                
    **You have successfully logged in as an annotator.**  
    Please read the task's introduction page before starting the qualification test.
    """)
