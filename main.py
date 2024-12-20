import sqlite3
import streamlit as st



# todo database setup for prod
conn = sqlite3.connect('database.db')


# Emoticons can be copied from here: https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
# define pages
main_page = st.Page(
    "core/pages/main_page.py", title="Start Page", icon="🏚️", default=True
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


pg = st.navigation(
    {
        "Home": [main_page],
        "Ambiguity Task": [ambiguity_start_page, ambiguity_qualification_page, ambiguity_annotation_page],
    }
)
pg.run()