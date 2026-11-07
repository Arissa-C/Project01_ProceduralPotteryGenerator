from PySide2 import QtGUI


class Pottery_Name_Validator(QtGUI.QValidator):

    def __init__(self):
        super().__init__()

    def validate(string, integer):
        # Return states:
        # Acceptable = alphanumeric, underscores
        # Intermediate = NONE
        # Invalid = blank characters (spaces, newline, etc.), special characters
        return QtGUI.QValidator.Acceptable
