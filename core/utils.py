import json

def read_json_from_file(path: str) -> dict:
    """
    Read a Json-file into a dict from a path.
    :param path: String filepath

    :return: dictionary object
    """
    # TODO Error handling
    with open(path, "r") as f:
        return json.loads(f.read())
    

def authenticate_id(task: str, user_id: id):
    """
    Check if the user id trying to log in for a specific task is valid.
    It does by checking the list under <taskname>/resources/user_ids.csv

    :param task: task name as it is in the folder's name, e.g. ambiguity_task
    :param user_id: the checked user id
    """
    with open(task + "/resources/user_ids.csv", "r") as f:
        users = f.readlines()
    users = [user.strip() for user in users]
    return user_id in users