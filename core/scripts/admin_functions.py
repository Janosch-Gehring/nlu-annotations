import os
import sqlite3
import streamlit as st

from core.scripts import utils, user_repository

def generate_users(task):
    """
    Generate an amount of users (one for each grouping).
    The generated user ids are printed and become valid. 
    The 'account' gets created once that ID logs in.

    :param task: e.g. ambiguity_task
    :return: None
    """
    try:
        amount = utils.TASK_INFO[task]["number_of_annotator_groups"]
    except:
        st.write("There is either no task selected or the number of annotation groups is not specified")
        return

    new_users = []

    st.write("List of new user ids:")
    conn = sqlite3.connect('database.db')
    for i in range(amount):
        new_user = utils.generate_random_string(size=8)
        new_users.append(new_user)
        st.write(f"Group {i} - {new_user}")
        conn.execute('''
        INSERT INTO valid_ids (user_id, task, annotator_group)
        VALUES (?, ?, ?)
    ''', (new_user, task, i))
        conn.commit()

    conn.close()

def list_user_progress(task):

    if task == "Select A Task":
        st.write("Select a task to show user progress.")
        return

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")
    rows = cursor.fetchall()
    for row in rows:
        user_id, user_task, qualified, annotator_group, progress, annotations_json, data = row

        if task == user_task:
            user_progress = utils.display_progress("annotation", user_id=user_id, print_progress=False)
            st.markdown(f"""---

**User**: {user_id}
                        
**Qualified**: {qualified}

**Progress**: {user_progress}""")
            
            advanced_on = st.toggle("Show Advanced Options", key = "toggle_" + user_id)

            if advanced_on:
                st.write("Change Qualification Setting")
                qualify_option = st.selectbox(
                    "Change user qualification",
                    ("None selected", "Mark as unqualified", "No qualification yet", "Mark as qualified"),
                    key="qualification_selection" + user_id)

                if qualify_option:
                    if qualify_option == "None selected":
                        pass
                    elif qualify_option == "Mark as unqualified":
                        user_repository.set_qualification(user_id, -1)
                    elif qualify_option == "No qualification yet":
                        user_repository.set_qualification(user_id, 0)
                    elif qualify_option == "Mark as qualified":
                        user_repository.set_qualification(user_id, 1)
                            

    conn.close()


def reset_database():
    """
    Delete the database file. This will cause a new one to be created when the website is next called.
    This deletes all data, of course...
    """
    os.remove("database.db")

