import os


def relative_path(file_name):
    """
    Returns relative path to the current __file__ for file_name. Useful for relative imports

    :type file_name: str
    :rtype: str
    """
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.dirname(path_to_current_file)
    return os.path.join(current_directory, file_name)
