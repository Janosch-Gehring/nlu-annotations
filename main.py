import streamlit as st

from core.scripts import database_repository, utils

if "user_id" not in st.session_state:
    st.session_state.user_id = ""

if "page" not in st.session_state:
    st.session_state.page = "main"

database_repository.init_db()


# Emoticons can be copied from here: https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
# define pages
main_page = st.Page(
    "core/pages/main_page.py", title="Start Page", icon="🏚️"
)
authentication_page = st.Page(
    "core/pages/authentication_page.py", title="Log In", icon="🎟️", url_path="authentication"
)
admin_page = st.Page(
    "core/pages/admin_page.py", title="Admin Area", icon="💻"
)
logout_page = st.Page(
    "core/pages/logout_page.py", title="Log Out", icon="↩️"
)

# Example Task Pages 
example_start_page = st.Page(
    "example_task/pages/introduction_page.py", title="Introduction", icon="📜", url_path="example_task_introduction"
)
example_qualification_page = st.Page(
    "example_task/pages/qualification_page.py", title="Qualification", icon="🔑"
)
example_annotation_page = st.Page(
    "example_task/pages/annotation_page.py", title="Annotation", icon="🏭"
)

# Ambiguity Task Pages
ambiguity_start_page = st.Page(
    "ambiguity_task/pages/introduction_page.py", title="The Ambiguity Task", icon="📜", url_path="ambiguity_task_introduction"
)
ambiguity_qualification_page = st.Page(
    "ambiguity_task/pages/qualification_page.py", title="Qualification", icon="🔑"
)
ambiguity_annotation_page = st.Page(
    "ambiguity_task/pages/annotation_page.py", title="Annotation", icon="🏭"
)

# Memory Experiment Pages
presentation_page = st.Page(
    "memory_experiment/pages/presentation_page.py", title="Memory Experiment", icon="🧠", url_path="memory_experiment_presentation", default=True
)

recall_page = st.Page(
    "memory_experiment/pages/recall_page.py", title="Recall", icon="🔍", url_path="memory_experiment_recall"
)

recognition_page = st.Page(
    "memory_experiment/pages/recognition_page.py", title="Recognition", icon="🔍", url_path="memory_experiment_recognition"
)

# Create navigation bar

if st.session_state.user_id == "admin":
    pg = st.navigation(
        {
            "Home": [main_page, admin_page],
        }
    )
elif st.session_state.user_id:
    available_pages = {
        "Home": [main_page]
    }
    if utils.authenticate_id("ambiguity_task", st.session_state.user_id):
        available_pages["Ambiguity Task"] = [ambiguity_start_page, ambiguity_qualification_page, ambiguity_annotation_page]

    elif utils.authenticate_id("example_task", st.session_state.user_id):
        available_pages["Example Task"] = [example_start_page, example_qualification_page, example_annotation_page]

    pg = st.navigation(available_pages)

else:
    pg = st.navigation(
        {
        "Home": [main_page, authentication_page],
        "Task Previews": [presentation_page, recall_page, recognition_page]
        },
        position="hidden"
    )

pg.run()