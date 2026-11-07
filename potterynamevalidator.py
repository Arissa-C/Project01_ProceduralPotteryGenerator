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
        # Intermediate = NONE
        # Invalid = anything else ESPECIALLY special chars, blank chars

        # If string is only alphanumeric or underscores, return acceptable
        valid_characters = string.ascii_letters + string.digits + "_"

        if any(input_char in valid_characters for input_char in input_string):
            print("Acceptable")
            return QtGui.QValidator.Acceptable
        # In all other cases, return invalid
        print("Invalid")
        return QtGui.QValidator.Invalid
