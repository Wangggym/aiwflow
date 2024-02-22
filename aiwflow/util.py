import os
import string


def get_env_variable(variable_name: str):
    my_variable = os.environ.get(variable_name)
    if my_variable is not None:
        return my_variable
    # else:
    #     print(f"Variable {variable_name} not found in the environment.")


def contains_only_english_with_special_chars(text):
    # Define allowed special characters, including all ASCII punctuation characters
    allowed_special_chars = set(string.punctuation)

    # Check if the string contains only English characters and allowed special characters
    for char in text:
        if (ord(char) < 0x20 or ord(char) > 0x7E) and char not in allowed_special_chars:
            return False
    return True


def is_long_desc(text: str) -> bool:
    length_threshold = 100
    return len(text) > length_threshold
