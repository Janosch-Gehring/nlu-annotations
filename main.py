import psycopg2
import streamlit as st

from core.scripts import database_repository, utils

if "user_id" not in st.session_state:
    st.session_state.user_id = ""

if "page" not in st.session_state:
    st.session_state.page = "main"

if "conn" not in st.session_state:
    st.session_state.conn = database_repository.db_connection()

# database_repository.init_db()  # can comment out now, since it already exists...


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
    "ambiguity_task/pages/introduction_page.py", title="Ambiguous Generations Task Intro", icon="🤖", url_path="ambiguity_task_introduction"
)
ambiguity_qualification_page = st.Page(
    "ambiguity_task/pages/qualification_page.py", title="Qualification", icon="🔑"
)
ambiguity_annotation_page = st.Page(
    "ambiguity_task/pages/annotation_page.py", title="Annotation", icon="🏭"
)

# Ambistory Task Pages
ambistory_start_page = st.Page(
    "ambistory_task/pages/introduction_page.py", title="Ambiguous Story Task Intro", icon="📕", url_path="ambistory_task_introduction"
)
ambistory_qualification_page = st.Page(
    "ambistory_task/pages/qualification_page.py", title="Qualification", icon="🔑"
)
ambistory_annotation_page = st.Page(
    "ambistory_task/pages/annotation_page.py", title="Annotation", icon="🏭"
)

# Ambisentence Task Pages
ambisentence_start_page = st.Page(
    "ambisentence_task/pages/introduction_page.py", title="Ambiguous Sentence Task Intro", icon="❓", url_path="ambistory_task_introduction"
)
ambisentence_qualification_page = st.Page(
    "ambisentence_task/pages/qualification_page.py", title="Qualification", icon="🔑"
)
ambisentence_annotation_page = st.Page(
    "ambisentence_task/pages/annotation_page.py", title="Writing", icon="✏️"
)

# Eval Ambisentence Task Pages
eval_ambisentence_start_page = st.Page(
    "eval_ambisentence_task/pages/introduction_page.py", title="Ambiguous Sentence Evaluation Task Intro", icon="🕵️‍♂️", url_path="eval_ambisentence_task_introduction"
)
eval_ambisentence_qualification_page = st.Page(
    "eval_ambisentence_task/pages/qualification_page.py", title="Qualification", icon="🔑"
)
eval_ambisentence_annotation_page = st.Page(
    "eval_ambisentence_task/pages/annotation_page.py", title="Annotation", icon="🏭"
)

# Ambistory2 Task Pages
ambistory2_start_page = st.Page(
    "ambistory2_task/pages/introduction_page.py", title="Ambiguous Story Task Intro", icon="📖", url_path="ambistory2_task_introduction"
)
ambistory2_qualification_page = st.Page(
    "ambistory2_task/pages/qualification_page.py", title="Qualification", icon="🔑"
)
ambistory2_annotation_page = st.Page(
    "ambistory2_task/pages/annotation_page.py", title="Annotation", icon="🏭"
)

# Ending Task Pages
ending_start_page = st.Page(  # How truly ironic
    "ending_task/pages/introduction_page.py", title="Story Ending Task Intro", icon="📙", url_path="ending_task_introduction"
)
ending_qualification_page = st.Page(
    "ending_task/pages/qualification_page.py", title="Qualification", icon="🔑"
)
ending_annotation_page = st.Page(
    "ending_task/pages/annotation_page.py", title="Writing", icon="✏️"
)

# Eval Ending Task Pages
eval_ending_start_page = st.Page(
    "eval_ending_task/pages/introduction_page.py", title="Story Interpretation Task Intro", icon="📖"
)
eval_ending_qualification_page = st.Page(
    "eval_ending_task/pages/qualification_page.py", title="Qualification", icon="🔑"
)
eval_ending_annotation_page = st.Page(
    "eval_ending_task/pages/annotation_page.py", title="Annotation", icon="🏭"
)

# Memory Experiment Pages

if st.session_state.user_id == "":
    authentication_page_experiments = st.Page(
        "core/pages/authentication_page_experiments.py", title="Log In", icon="🎟️", url_path="authentication_experiments", default=True
    )
    presentation_page = st.Page(
        "memory_experiment/pages/presentation_page.py", title="Memory Experiment", icon="🧠", url_path="memory_experiment_presentation"
    )
else:
    authentication_page_experiments = st.Page(
        "core/pages/authentication_page_experiments.py", title="Log In", icon="🎟️", url_path="authentication_experiments"
    )
    presentation_page = st.Page(
        "memory_experiment/pages/presentation_page.py", title="Memory Experiment", icon="🧠", url_path="memory_experiment_presentation",default=True
    )


recall_page = st.Page(
    "memory_experiment/pages/recall_page.py", title="Recall", icon="🔍", url_path="memory_experiment_recall"
)

recognition_page = st.Page(
    "memory_experiment/pages/recognition_page.py", title="Recognition", icon="🔍", url_path="memory_experiment_recognition"
)

demographics_page = st.Page(
    "memory_experiment/pages/demographics_page.py", title="demographics", icon="🔍", url_path="demographics_info"
)

distractor_page = st.Page(
    "memory_experiment/pages/distractor_page.py", title="Distractor", icon="🔍", url_path="distractor"
)

# Create navigation bar

if st.session_state.user_id == "admin":
    pg = st.navigation(
        {
            "Home": [main_page, admin_page, logout_page],
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

    elif utils.authenticate_id("ambistory_task", st.session_state.user_id):
        available_pages["Ambistory Task"] = [ambistory_start_page, ambistory_qualification_page, ambistory_annotation_page]

    elif utils.authenticate_id("ambisentence_task", st.session_state.user_id):
        available_pages["Ambiguous Sentence Task"] = [ambisentence_start_page, ambisentence_qualification_page, ambisentence_annotation_page]

    elif utils.authenticate_id("eval_ambisentence_task", st.session_state.user_id):
        available_pages["Ambiguous Sentence Evaluation Task"] = [eval_ambisentence_start_page, eval_ambisentence_qualification_page, eval_ambisentence_annotation_page]

    elif utils.authenticate_id("ambistory2_task", st.session_state.user_id):
        available_pages["Ambiguous Story Task"] = [ambistory2_start_page, ambistory2_qualification_page, ambistory2_annotation_page]

    elif utils.authenticate_id("ending_task", st.session_state.user_id):
        available_pages["Story Ending Task"] = [ending_start_page, ending_qualification_page, ending_annotation_page]

    elif utils.authenticate_id("eval_ending_task", st.session_state.user_id):
        available_pages["Story Interpretation Task"] = [eval_ending_start_page, eval_ending_qualification_page, eval_ending_annotation_page]

    elif utils.authenticate_id("memory_experiment", st.session_state.user_id):
        available_pages["Memory Experiment"] = [presentation_page, recall_page, recognition_page, demographics_page, distractor_page]

    available_pages["Other"] = [logout_page]

    if utils.authenticate_id("memory_experiment", st.session_state.user_id):
        print("user_id", st.session_state.user_id)
        pg = st.navigation(available_pages["Memory Experiment"], position="hidden")
    else:
        pg = st.navigation(available_pages)
        

else:
    pg = st.navigation([authentication_page_experiments])
try:
    pg.run()
except (psycopg2.InterfaceError, psycopg2.OperationalError) as e:
    st.markdown("# Your session was cancelled, likely due to prolonged inactivity. Please log out, then log in again.")
    print(e)