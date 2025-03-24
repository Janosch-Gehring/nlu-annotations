import streamlit as st

st.text_area("""Please write down as many headlines as you remember here. Try to write downthe exact wording of each headline. "
Write each headline in a new line:""")

if st.button("Submit"):
    st.switch_page("memory_experiment/pages/recognition_page.py")