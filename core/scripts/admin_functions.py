import os
import sqlite3
import streamlit as st

from core.scripts import utils, user_repository, database_repository

def generate_users(task: str, amount_per_group: int = 1):
    """
    Generate an amount of users (determined by amount_per_group parameter).
    The generated user ids are printed and become valid. 
    The 'account' gets created once that ID logs in.

    :param task: e.g. ambiguity_task
    :param amount_per_group:
    :return: None
    """
    try:
        amount_of_groups = utils.TASK_INFO[task]["number_of_annotator_groups"]
    except:
        st.write("There is either no task selected or the number of annotation groups is not specified")
        return

    new_users = []

    st.write("List of new user ids:")
    conn = st.session_state.conn
    cursor = conn.cursor()
    for i in range(amount_of_groups):
        for j in range(amount_per_group):
            new_user = utils.generate_random_string(size=8)
            new_users.append(new_user)
            st.write(f"User{i}-{j}, {new_user}")
            cursor.execute('''
            INSERT INTO valid_ids (user_id, task, annotator_group)
            VALUES (%s, %s, %s)
        ''', (new_user, task, i))
            conn.commit()

    
    # conn.close()
    st.markdown("**Copy these IDs so you don't lose them!**")

def list_user_codes(relevant_task):
    conn = st.session_state.conn
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM valid_ids")
    valid_id_rows = cursor.fetchall()

    # get set of users that has logged in before (entries in user_data)
    cursor.execute("SELECT * FROM user_data")
    user_rows = cursor.fetchall()
    users = [row[0] for row in user_rows]

    entries = []
    for id_row in valid_id_rows:
        user_id, task, annotator_group = id_row
        if relevant_task != task:
            continue
        has_logged_in = (user_id in users)
        entries.append([user_id, annotator_group, has_logged_in])
    # get number of annotation groups
    max_group = max([x[1] for x in entries])

    st.write("Delete all unused user codes for this task.")
    st.write("(Whoever has received a code but not yet logged in will not be able to anymore.)")
    delete_codes = st.text_input("Type DELETE to delete unused user codes.")
    if delete_codes == "DELETE":
        st.write("Deleting...")
        cursor.execute("DELETE FROM valid_ids WHERE user_id NOT IN (SELECT user_id FROM USER_DATA)")
        conn.commit()
        # conn.close()
        st.write("Done")

    # sort primarily by has_logged_in and secondarily by group
    sorted_entries = sorted(entries, key = lambda x: (not x[2], x[1]))
    for entry in sorted_entries:
        st.markdown("---")
        col1, col2, col3 = st.columns([0.5, 0.2, 0.3])
        with col1:
            st.markdown(f"User: {entry[0]}\t| Group: {entry[1]}\t| Used: {entry[2]}")

        with col2:
            st.write("Delete ID")
            if not entry[2]:  # don't delete logged in users. They should be banned instead.
                delete_button = st.button("Delete", key="delete_id_" + entry[0])
                if delete_button:
                    cursor.execute("DELETE FROM valid_ids WHERE user_id = %s", (entry[0], ))
                    conn.commit()
                    st.write("User deleted")
            else:
                delete_button = st.button("Delete", key="delete_id_" + entry[0], disabled=True, help="Registered users cannot be deleted. You can instead set them to unqualified to ban them.")

        with col3:
            if not entry[2]:  # again, once the user already started, it's too late
                group_change = st.number_input("Change Group", min_value=0, max_value=max_group, value=None, key="change_id_" + entry[0])
                if group_change:
                    cursor.execute("UPDATE valid_ids SET annotator_group = %s WHERE user_id = %s", (group_change, entry[0]))
                    conn.commit()
                    st.write("Group changed.")


def list_user_progress(task):

    if task == "Select A Task":
        st.write("Select a task to show user progress.")
        return

    conn = st.session_state.conn
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
                            

    # conn.close()


def reset_database():
    """
    Empty all tables.
    Dont do this...
    """
    # os.remove("database.db")
    conn = st.session_state.conn
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE user_data")
    cursor.execute("TRUNCATE TABLE valid_ids")
    conn.commit()
