import string
from PySide2 import QtGui


class Pottery_Name_Validator(QtGui.QValidator):

    def __init__(self):
        super().__init__()

    def validate(validator_class, input_string, cursor_position):
        # Arguments (this isn't in documentation for some reason):
        # 1st is validator class (don't know if this is instance or type)
        # 2nd is full input string
        # 3rd is cursor position int
        #
        # Return states:
        # Acceptable = alphanumeric, underscores
        # Intermediate = empty string
        # Invalid = anything else, or digit in first position

        valid_characters = string.ascii_letters + string.digits + "_"

        # If user wants to erase entire string, return intermediate
        if not input_string and cursor_position == 0:
            return QtGui.QValidator.Intermediate

        # If number in first position, return invalid
        if input_string and input_string in string.digits:
            return QtGui.QValidator.Invalid

        # If string is only alphanumeric or underscores, return acceptable
        elif any(input_char in valid_characters for input_char in input_string):
            return QtGui.QValidator.Acceptable

        # In all other cases, return invalid
        return QtGui.QValidator.Invalid
