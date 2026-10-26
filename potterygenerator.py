import sys
from PySide2 import QtWidgets, QtCore
import maya.cmds as cmds
import random


class Pottery():

    def __init__(self):
        # All placeholder values until GUI is done
        # distribution parameters
        self.total_pots = 3
        self.pot_spacing = 2
        self.spiral_angle = 1
        self.rotation_jitter = 180
        # pot size parameters
        self.min_height = 1
        self.max_height = 7
        self.min_radius = 1
        self.max_radius = 6
        pass

    def create(self):
        # creates whole set of pots
        # call create one pot method in loop
        # loop as many times as input says to do (total pots)
        pass

    def create_pot(self, min_height, max_height,
                   min_radius, max_radius, rotation_jitter):
        # creates one pot, given position, rotation, size
        (height, radius) = \
            self.calculate_size(min_height, max_height, min_radius, max_radius)
        angle = self.calculate_rotation(rotation_jitter)
        cmds.polyCylinder(name="pot_base", radius=radius, height=height)
        cmds.xform(rotation=angle)
        pass

    def calculate_position(self):
        # INPUT: current pot #, Pot spacing, spiral angle
        # OUTPUT: Position of pot in scene space
        pass

    def calculate_rotation(self, rotation_jitter):
        # INPUT: Rotation jitter
        # OUTPUT: Rotation of the pot
        return random.random() * rotation_jitter
    
    def calculate_size(self, min_height, max_height, min_radius, max_radius):
        # INPUT: min and max values (height and radius)
        # OUTPUT: randomized value in that range, for one pot
        height = random.uniform(min_height, max_height)
        radius = random.uniform(min_radius, max_radius)
        return (height, radius)
