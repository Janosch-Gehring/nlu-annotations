import datetime, os, json, sqlite3, re

import streamlit as st

def format_sample(question: dict) -> str:

    match = re.findall(r"<(.*)>", question["sentence_2"])
    blue_background = re.sub(r"<.*>", f":blue-background[{match[0]}]", question["sentence_2"])
    formatted_string = f"##### **Sentence 1:** {question["sentence_1"]}\n##### **Sentence 2:** {blue_background}\n\n*Article name:* &emsp;{question["article_name"]}\n\n*Context before:* &nbsp;{question["context_before"]}\n\n*Context after:* &emsp;{question["context_after"]}"
    
    return formatted_string

# Check if user exists in the database
def get_user(user_id: str):
    """
    Get a user from any task by user id.
    Returns None if no user found.

    :param user_id: ID-string of user
    :return: User or None
    """
    conn = st.session_state.conn
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data WHERE user_id=%s", (user_id,))
    user = cursor.fetchone()
    # conn.close()
    return user

def create_user(user_id: str, task: str = "ambiguity_task", data: dict = {}):
    """
    Creates a user with the specified user id.

    :param user_id: ID-string of user
    :param task:
    :param data: optional user metadata dict
    :return: None
    """
    conn = st.session_state.conn
    cursor = conn.cursor()

    # find annotator group
    cursor.execute("SELECT * from valid_ids WHERE user_id=%s", (user_id,))
    id_data = cursor.fetchone()
    annotator_group = id_data[2]

    data = json.dumps(data)

    cursor.execute("""
        INSERT INTO user_data (user_id, task, annotator_group, data)
        VALUES (%s, %s, %s, %s)
    """, (user_id, task, annotator_group, data))
    
    conn.commit()  # Commit changes to the database
    # conn.close()

def add_log(user_id: str, text: str):
    """
    Add the entry to the log of the given user id. The current time is also appended to the log.

    :param user_id:
    :param text: Whatever you want to log
    """
    user = get_user(user_id)

    logs = user[6]["log"]
    logs.append(text + "|" + str(datetime.datetime.now()))

    new_data = user[6]
    user[6]["log"] = logs

    new_data_str = json.dumps(new_data)

    conn = st.session_state.conn
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE user_data
        SET data = %s
        WHERE user_id = %s
    """, (new_data_str, user_id))
    st.session_state.user[6] = new_data_str
    conn.commit()


def save_one_annotation(user_id: str, key: str, question_index: int, question_annotation: dict):
    """
    Save one annotation for a sample to the database.
    
    :param user_id:
    :param key: The subcategory of sample, e.g. qualification or main
    :param question_index: At what index to save the annotation, e.g. 3 for the 3rd sample
    :param question_annotation: The annotation to save, which is a dict.
    """
    conn = st.session_state.conn
    cursor = conn.cursor()

    user = st.session_state.user

    annotations = user[5]

    if key not in annotations:
        annotations[key] = []

    # for new annotations, extend the saved annotation list to fit the new annotation at the proper spot.
    while len(annotations[key]) < question_index:
        annotations[key].append({})

    annotations[key][question_index - 1] = question_annotation
    annotations_json = json.dumps(annotations)
    cursor.execute("""
        UPDATE user_data
        SET annotations = %s
        WHERE user_id = %s
    """, (annotations_json, user_id))
    st.session_state.user[5] = annotations
    conn.commit()
    #conn.close()

def get_qualification() -> int:
    """
    Check if the user with the given id passed a qualification test.

    :param user_id: id-string of user
    :return: -1 if failed, 0 if no qualification, 1 if passed
    """
    qualified = st.session_state.user[2]
    return qualified


def get_checkpoint(key, print=True) -> int:
    """
    Find the last annotation that was being worked on for the given key (e.g. "qualification").
    Assumes that the samples are sorted. Return the highest index.
    """
    annotations = st.session_state.user[5]

    if key not in annotations:  # Did not even start the task, lead to first sample
        return 0
    
    if print:
        st.write("Returning to checkpoint from previous session")
    return len(annotations[key])

def reset_annotation(user_id: str, key: str):
    """
    Reset the user's annotation given a task key (like qualification or annotation)
    
    :param user_id:
    :param key: The key of the annotation data to delete, e.g. qualification
    """
    conn = st.session_state.conn
    cursor = conn.cursor()

    user = get_user(user_id)
    annotations = user[5]

    if key not in annotations:
        return
    del annotations[key]

    annotations_json = json.dumps(annotations)
    cursor.execute("""
        UPDATE user_data
        SET annotations = %s
        WHERE user_id = %s
    """, (annotations_json, user_id))
    conn.commit()
    # conn.close()

def set_qualification(user_id: str, setting: int=1):
    """
    Change the user's qualification setting.
    -1 = unqualified
    0 = not yet qualified
    1 = qualified

    :param user_id: 
    """
    conn = st.session_state.conn
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE user_data
        SET qualified = %s
        WHERE user_id = %s
    """, (setting, user_id,))
    conn.commit()
    # conn.close()
    
    if st.session_state.user_id == "admin":
        st.write("Qualification updated.")
    else:
        st.session_state.user[2] = setting

def assign_to_weakest_group(user_id: str, task: str):
    """
    Assign the user to the group that currently has the least amount of members.
    Test accounts and unqualified accounts do not count towards the numbers.
    Lower indices are prioritized.
    Typically to be used after qualification.

    :param user_id: user string
    :param task: task string
    """
    from core.scripts.utils import TASK_INFO  # probably not great to have utils importing from each other...

    conn = st.session_state.conn
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM user_data
    """)
    users = cursor.fetchall()

    group_counts = {}
    for i in range(TASK_INFO[task]["number_of_annotator_groups"]):
        group_counts[i] = 0

    for user in users:
        u_id, user_task, qualified, group, progress, _, data = user
        if (user_task != task) or (qualified != 1) or (u_id == user_id):
            continue
        if "test" in data["prolific_id"].lower():
            continue
        group_counts[group] += 1

    weakest_group = min(group_counts, key = group_counts.get)

    if task == "eval_ending_task":
        # I have gotten to a point where I really only need group 1 anymore.
        weakest_group = 1

    print(task, group_counts, weakest_group)

    cursor.execute("""
        UPDATE user_data
        SET annotator_group = %s
        WHERE user_id = %s
    """, (weakest_group, user_id))
    st.session_state.user[3] = weakest_group
    conn.commit()

def mark_as_done(user_id):
    conn = st.session_state.conn
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE user_data
        SET progress = -1
        WHERE user_id = %s
    """, (user_id,))
    conn.commit()
    st.session_state.user[4] = -1
    # conn.close()
    print("User ", user_id, " finished annotation!")

def check_if_done(user_id):
    if st.session_state.user[4] == -1:
        return True

def fetch_user_data():
    """
    DEBUG function.
    Fetch and display all rows from the user_data table.
    not used or tested currently
    """
    conn = st.session_state.conn
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")
    rows = cursor.fetchall()
    for row in rows:
        user_id, task, qualified, annotator_group, progress, annotations, data = row
        st.write(f"User ID: {user_id}, Qualified: {qualified}, Task: {task} Progress: {progress}, Annotations: {annotations}")
    # conn.close()


def skip_to_next_sample(index: int, samples: dict, grouping: int, direction: int=1, 
                        subtask: str="annotation", qualification_function=None) -> int:
    """
    From the specified index, move in the specified direction to find the next sample relevant to the group.

    :param index: Index of the current page/sample
    :param samples: dict of all the samples (keys are "1", "2", ...)
    :param grouping: group of user
    :param direction: 1 for going forward, -1 for going backward
    :param subtask: e.g. annotation or qualification
    :param qualification function: Function to evaluate whether qualification was passed, not needed if subtask!=qualification
    :return: Index of the next (or previous) sample
    """
    index += direction
    if index < 1:
        return 1
    while True:
        if index > len(samples):
            finish_subtask(subtask, qualification_function)
            break
        if str(index) not in samples:  # account for samples having id gaps
            index += direction
            continue
        checked_sample = samples[str(index)]
        if ("grouping" not in checked_sample) or (grouping == checked_sample["grouping"]):
            break  # break when finding relevant sample
        else:
            index += direction
            if index < 1:  # went back too far
                index = 1
                direction = 1  # reverse to find first sample again
    # return index where it found a sample
    return index


def handle_back_button(annotation: dict, index: int, samples: dict, subtask="annotation"):
    """
    All-in-one behaviour of the back button: Saves revised annotations and skips to the next-oldest relevant sample.

    :param annotation: The annotation of the currently displayed sample
    :param index: The index of the current sample
    :param samples: List with all of the samples (including irrelevant ones for the grouping) for the current subtask
    :param subtask: The current subtask, e.g. annotation or qualification
    """
    # don't save when pressing back on the newest sample, since it will otherwise get skipped when returning later
    if index < get_checkpoint(key=subtask, print=False):
        save_one_annotation(st.session_state.user_id, subtask, index, annotation)

    grouping = st.session_state.user[3]
    # skip backwards over the samples of the other groups to arrive at the new index
    new_index = skip_to_next_sample(index, samples, grouping, direction=-1)

    if subtask == "qualification":
        st.session_state.qualification_progress = new_index
    else:
        st.session_state.progress = new_index

    st.rerun()



def handle_next_button(annotation: dict, index: int, samples: dict, subtask="annotation", qualification_function=None):
    """
    All-in-one behaviour of the next button: Saves annotation, skips to next relevant sample and finishes the annotation if the end is reached.
    
    :param annotation: The annotation of the current sample that should be saved.
    :param index: The index of the current sample
    :param samples: List with all of the samples (including irrelevant ones for the grouping) for the current subtask
    :param subtask: The current subtask, e.g. annotation or qualification
    :param qualification_function: If subtask=qualification, a function that evaluates success of qualification given user annotations
    """
    save_one_annotation(st.session_state.user_id, subtask, index, annotation)

    if index >= len(samples):
        finish_subtask(subtask, qualification_function=qualification_function)
    else:
        grouping = st.session_state.user[3]
        # proceed until we find the next sample relevant for the grouping
        new_index = skip_to_next_sample(index, samples, grouping, direction=1)

    if subtask == "qualification":
        st.session_state.qualification_progress = new_index
    else:
        st.session_state.progress = new_index

    if new_index != index:
        st.rerun()


def finish_subtask(subtask: str="annotation", qualification_function=None):
    """
    Finish the current subtask. If it is the qualification, call the qualification function to check if the user passed.

    :param subtask: annotation or qualification
    :param qualification_function: a function that returns True/False depending on the user passing
    """
    print("Finishing subtask.")
    if subtask == "annotation":
        finish_annotation()
    elif subtask == "qualification":
        finish_qualification(qualification_function)


def finish_annotation():
    st.write("You finished the annotation!")
    mark_as_done(st.session_state.user_id)
    st.rerun()
    st.write("Thank you for submitting your annotations.")


def finish_qualification(qualification_function: str):
    """
    Finish the current user's qualification and judge if they are qualified.
    Sets their qualification accordingly.
    
    :param qualification_function: function that returns True/False based on the user's annotations.
    """
    # if this is the last question, check for qualification
    user = st.session_state.user
    annotations = user[5]
    # check if the qualification was successful and set user state accordingly
    if qualification_function(annotations):
        st.write("The qualification test has ended. Please wait a moment...")
        set_qualification(st.session_state.user_id)
        # Since the user is qualified, automatic group assignment can now take place...
        if "group_assignment" in TASK_INFO[user[1]] and TASK_INFO[user[1]]["group_assignment"] == "post-qualification":
            assign_to_weakest_group(st.session_state.user_id, user[1])
        st.rerun()
    else:
        st.write("The qualification test has ended. Please wait a moment...")
        set_qualification(st.session_state.user_id, setting=-1)
        # user_repository.reset_annotation(st.session_state.user_id, key="qualification")
        st.rerun()

    # reset progress to beginning (important in case an admin decides to reset qualification)
    st.session_state.qualification_progress = 1


def check_all_checkboxes(implicit: str, checkboxes: list, comment: str) -> bool:

    if implicit == "No":
        return True
    elif implicit == "Yes" and checkboxes[-1]:
        if comment:
            return True
    elif implicit == "Yes" and len([box for box in checkboxes[:-1] if box]) >= 1:
        return True
    else:
        return False
    
def display_progress(key="annotation", user_id=None, print_progress: bool = True) -> str:
    """
    Returns the progress x/y ("x out of y") for a user on a subtask.

    :param key: The subtask, e.g. annotation or qualification
    :param user_id: Id of user to check, if None, display logged in user's progress
    :param print_progress: Whether to print the progress immediately instead of just returning the string
    :return: str
    """
    if not user_id:
        user = st.session_state.user
    else:
        user = user_repository.get_user(user_id)

    user_group = user[3]
    task = user[1]
    max_samples = get_amount_of_samples_for_group(key, task, user_group)

    if not user:
        return "NOT STARTED"

    # TODO show progress even when all annotations are finished (when revising annotations)
    
    # handle case that there are no annotations
    annotations = user[5]
    if key not in annotations:
        if print_progress:
            st.write("Sample 1")
        return "Annotation not started"
    annotations = annotations[key]

    count_finished = 0
    for annotation in annotations:
        if annotation:  # "unfinished" annotations will be empty
            count_finished += 1
    if print_progress:
        st.write("*Finished Samples*: " + str(count_finished) + "/" + str(max_samples))
    return str(count_finished) + "/" + str(max_samples)

def print_annotation_schema(samples: dict, index: int) -> tuple[dict, str, list, str, str, bool]:
    """
    Prints the annotation schema that is seen on the qualification and annotation page.

    :param subtask: qualification or annotation
    :param index: The number sample to show
    :return: The sentence and widget inputs in the order they are displayed to the user.
    """
    question = samples[str(index)]
    # # display the "Sample 1/5" thing
    display_progress(key=subtask)

    st.markdown("Read the following sentences and the contexts.\n")
    st.write(format_sample(question))

    context, reasoning, complement, instruction, other = False, False, False, False, False
    comment_implicit, comment_not_implicit = "", ""
    # implicit = st.radio(
    #     ":grey-background[Does the first sentence implicitely convey the same meaning as the second one?]",
    #     ["Yes", "No"],
    #     key="implicit",
    #     horizontal=True,
    #     index=None,)

    st.markdown(":grey-background[Does the first sentence implicitly convey the same meaning as the second one?]")

    implicit = st.segmented_control("", ["Yes", "No"], key=10 * index + 1)
    # col1, col2 = st.columns(2)
    # with col1:
    #     implicit = st.checkbox(key=10 * index + 1, label="Yes", value=None)
    # with col2:
    #     not_implicit = st.checkbox(key=10 * index + 2, label="No", value=None) 
    if implicit == "Yes":
        st.markdown("Please specify one or multiple reasons for your choice:")

        col1, col2 = st.columns(2)

        with col1:
            context = st.checkbox(key=10 * index + 2, label="Context", value=None)
            reasoning = st.checkbox(key=10 * index + 3, label="Logical Reasoning", value=None)
            complement = st.checkbox(key=10 * index + 4, label="Omitted Complement", value=None)
            instruction = st.checkbox(key=10 * index + 5, label="Recoverable Instruction", value=None)

        with col2:
            other = st.checkbox("Other", value=None)
            comment_implicit = st.text_input(key=10 * index + 6, label="If applicable, specify other reasons that led to your decision:")
            if comment_implicit:
                st.write(r"$\textsf{\scriptsize Thanks for your input!}$")
    else:
        comment_not_implicit = st.text_input(key=10 * index + 7, label="If you are unsure, tick \"No\" and explain your thoughts here:")
        if comment_not_implicit:
            st.write(r"$\textsf{\scriptsize Thanks for your input!}$")

    checkboxes = [context, reasoning, complement, instruction, other]
    if check_all_checkboxes(implicit, checkboxes, comment_implicit):
        next_input = st.button(key = 10 * index + 8, label="Next", help="Save this annotation and advance to the next one.")
    else:
        next_input = None

    return question, implicit, checkboxes, comment_implicit, comment_not_implicit, next_input