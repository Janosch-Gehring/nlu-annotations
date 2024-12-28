import sqlite3
import streamlit as st

from core.scripts import database_repository

if "user_id" not in st.session_state:
    st.session_state.user_id = ""

if "page" not in st.session_state:
    st.session_state.page = "main"

# todo database setup for prod
conn = sqlite3.connect('database.db')

database_repository.init_db()


# Emoticons can be copied from here: https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
# define pages
main_page = st.Page(
    "core/pages/main_page.py", title="Start Page", icon="🏚️", default=True
)
authentication_page = st.Page(
    "ambiguity_task/pages/authentication_page.py", title="Log In", icon="🎟️"
)
admin_page = st.Page(
    "core/pages/admin_page.py", title="Admin Area", icon="💻"
)

# Ambiguity Task Pages
ambiguity_start_page = st.Page(
    "ambiguity_task/pages/introduction_page.py", title="Introduction", icon="📜"
)
ambiguity_qualification_page = st.Page(
    "ambiguity_task/pages/qualification_page.py", title="Qualification", icon="🔑"
)
ambiguity_annotation_page = st.Page(
    "ambiguity_task/pages/annotation_page.py", title="Annotation", icon="🏭"
)


# Create navigation bar

if st.session_state.user_id == "admin6427":
    pg = st.navigation(
        {
            "Home": [main_page, admin_page],
        }
    )
elif st.session_state.user_id:
    pg = st.navigation(
        {
            "Home": [main_page],
            "Ambiguity Task": [ambiguity_start_page, ambiguity_qualification_page, ambiguity_annotation_page],
        }
    )
else:
    pg = st.navigation(
        {
        "Home": [main_page, authentication_page]
        }
    )

pg.run()