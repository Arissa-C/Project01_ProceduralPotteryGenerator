import string
from PySide2 import QtGui


class Pottery_Name_Validator(QtGui.QValidator):

    def __init__(self):
        super().__init__()

    def validate(validator_class, input_string, cursor_position):
        # Called whenever user types into QLineEdit that has this validator set
        # prevents invalid chars from being entered
        # allows acceptable or intermediate actions to occur
        #
        # Arguments (this isn't in documentation for some reason):
        # 1st is validator class (don't know if this is instance or type)
        # maybe first argument is a self instance?
        # 2nd is full input string
        # 3rd is cursor position int
        #
        # Return states:
        # Acceptable = alphanumeric, underscores
        # Intermediate = empty string, digit in first position
        # Invalid = anything else

        valid_chars = string.ascii_letters + string.digits + "_"

        # If user wants to erase entire string, return intermediate
        if not input_string and cursor_position == 0:
            return QtGui.QValidator.Intermediate

        # If string is only alphanumeric or underscores, return acceptable
        elif all(input_char in valid_chars for input_char in input_string):
            return QtGui.QValidator.Acceptable

        # In all other cases, return invalid
        return QtGui.QValidator.Invalid
