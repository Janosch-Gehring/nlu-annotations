from core.scripts.utils import read_json_from_file, TASK_INFO

def check_if_qualified(annotations: dict) -> bool:
    """
    Check if the given annotations (from a user's annotation field) would pass the qualification test.

    :param annotations: user's annotation in dict form, should have a 'qualification' key
    :return bool: True if passed, False if not
    """
    qualification_questions = read_json_from_file(TASK_INFO["rewriting_judgement_task"]["qualification_filepath"])

    needed_score = 4
    score = 0
    for question_id in qualification_questions:
        if (annotations["qualification"][int(question_id)-1]["accuracy"] == qualification_questions[question_id]["correct_accuracy_answer"] and
        annotations["qualification"][int(question_id)-1]["style"] == qualification_questions[question_id]["correct_style_answer"] and
        annotations["qualification"][int(question_id)-1]["accuracy_subclass"] == qualification_questions[question_id]["correct_accuracy_subclass"] and
        annotations["qualification"][int(question_id)-1]["style_subclass"] == qualification_questions[question_id]["correct_style_subclass"]):
            score += 1

    return score >= needed_score