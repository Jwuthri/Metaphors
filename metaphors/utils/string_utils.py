import re


def string_contains_digit(string: str) -> bool:
    """
    It returns True if the string contains a digit, and False otherwise

    :param string: str
    :type string: str
    :return: True or False
    """
    if re.search("\d", string):
        return True
    else:
        return False
