import streamlit as st

from core.scripts import database_repository, admin_functions



if "database" not in st.session_state:
    st.session_state.database = "Press the other button first"

st.write("# Welcome to the Admin Area.\n\nHere, you can manage annotations and users.")

st.write("## Download Annotation Data")

if st.button(label="Click Here to Get Database File Before Downloading!"):
    st.session_state.database = database_repository.convert_database_to_json()
    st.rerun()
    st.write("OK!")

st.download_button(label="Then click here to download", data = st.session_state.database, file_name="database.json")


st.markdown("""
            ## Generate New User Codes 
            
            Here you can generate new annotator codes to share with your annotators.
            The amount that is generated equals the amount of annotation groups for the task.
            (e.g. if there are 5 annotation groups, the first ID belongs to the first group, second to the second group, etc)

            """)

generation_option = st.selectbox(
     "For which task to generate new users?",
     ("None selected", "ambiguity_task"))

if generation_option:
    admin_functions.generate_users(generation_option)

st.markdown("""
            ## Manage And Track User Progress
            
            Select a task below to see users' progress and qualification success on this task.
            """)

tracking_option = st.selectbox(
    "Which task to check progress on?", ("None selected", "ambiguity_task")
)
if tracking_option:
    admin_functions.list_user_progress(tracking_option)

st.markdown("---")

danger_on = st.toggle("Enter Danger Zone")

if danger_on:
    text_input = st.text_input("Type DELETE in the field below to reset the local database.db file. Please don't do this on the deployed app without telling other admins.", max_chars=200)

    if st.button(label="Confirm") and (text_input == "DELETE"):
        st.write("OK :( Deleting")
        admin_functions.reset_database()
        st.write("Done. Please refresh the page.")



