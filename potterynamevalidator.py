from PySide2 import QtGui


class Pottery_Name_Validator(QtGui.QValidator):

    def __init__(self):
        super().__init__()

    def validate(string, integer):
        # Return states:
        # Acceptable = alphanumeric, underscores
        # Intermediate = NONE
        # Invalid = anything else ESPECIALLY special chars, blank chars
        return QtGui.QValidator.Acceptable