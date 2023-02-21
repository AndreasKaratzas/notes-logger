import os


def is_dir_empty(dir_path):
    """
    Checks if a directory is empty (contains no files or subdirectories).
    Ignores the .gitkeep file.

    Args:
        dir_path (str): path to the directory

    Returns:
        bool: True if directory is empty, False otherwise
    """
    # Check if directory exists
    if not os.path.isdir(dir_path):
        raise ValueError("Invalid directory path")

    # Check if directory contains only the .gitkeep file
    if len(os.listdir(dir_path)) == 1 and os.listdir(dir_path)[0] == ".gitkeep":
        return True

    # Check if directory contains any files or subdirectories
    for file_name in os.listdir(dir_path):
        if file_name != ".gitkeep":
            return False

    return True


def check_for_notes_log(directory):
    """
    Checks if there is an 'notes.log' file in a directory.
    
    Args:
    - directory (str): the path to the directory to check
    
    Returns:
    - True if an 'notes.log' file exists in the directory, False otherwise
    """
    
    # loop through each file in the directory
    for file in os.listdir(directory):
        if file == 'notes.log':
            # if an 'notes.log' file is found, return True
            return True
    
    # if no 'notes.log' file is found, return False
    return False


def init_nltk(directory_path: str):
    if not check_for_notes_log(directory_path):
        import nltk
        nltk.download('stopwords')
        nltk.download('punkt')
