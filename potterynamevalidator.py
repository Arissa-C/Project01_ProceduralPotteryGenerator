from PySide2 import QtGui


class Pottery_Name_Validator(QtGui.QValidator):

    def __init__(self):
        super().__init__()

    def validate(input_string, cursor_position, wild_card_arg):
        # Return states:
        # Acceptable = alphanumeric, underscores
        # Intermediate = NONE
        # Invalid = anything else ESPECIALLY special chars, blank chars

        # If string is only alphanumeric or underscores, return acceptable
        if input_string:
            print("Acceptable")
            return QtGui.QValidator.Acceptable
        # In all other cases, return invalid
        print("Invalid")
        return QtGui.QValidator.Invalid
