import sys
from PySide2 import QtWidgets, QtCore
import maya.cmds as cmds


class Pottery():

    def __init__(self):
        # distribution parameters
        self.total_pots = 3
        # pot size parameters
        self.pot_height = 7
        self.pot_width = 5
        self.pot_radius = 1

        # both placeholder parameters
        pass

    def create(self):
        # creates whole set of pots
        # call create one pot method in loop
        # loop as many times as input says to do (total pots)
        pass

    def create_pot(self):
        # creates one pot, given position, rotation, size
        pass
