from core.scripts.utils import read_json_from_file, TASK_INFO

def check_if_qualified(annotations: dict) -> bool:
    """
    Check if the given annotations (from a user's annotation field) would pass the qualification test.

    :param annotations: user's annotation in dict form, should have a 'qualification' key
    :return bool: True if passed, False if not
    """
    qualification_questions = read_json_from_file(TASK_INFO["implicit_meaning_task"]["qualification_filepath"])

    try:
        if set([qualification_questions[question_id]["correct_answer"] == annotations["qualification"][int(question_id)-1]["implicit_meaning"] for question_id in qualification_questions]) == {True}:
            return True
        else:
            return False
    except KeyError:
        print(annotations)