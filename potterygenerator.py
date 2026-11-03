import sys
import math

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCharts import QtCharts
from PySide2.QtGui import QtPainter

import maya.cmds as cmds
import random


class Pottery():

    def __init__(self):
        # All placeholder values until GUI is done
        # distribution parameters
        self.total_pots = 3
        self.rotation_jitter = 180
        self.spacing_between_pots = 2
        self.angle_between_pots = 1
        self.first_pot_spacing = 3
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

    def create_pot(self,
                   min_height, max_height,
                   min_radius, max_radius,
                   rotation_jitter,
                   spacing_between_pots, angle_between_pots,
                   first_pot_spacing, current_pot_index):
        # creates one pot, given position, rotation, size
        (height, radius) = \
            self.calculate_size(min_height, max_height, min_radius, max_radius)
        angle = self.calculate_rotation(rotation_jitter)
        (x_coord, z_coord) =\
            self.calculate_position(
                spacing_between_pots, angle_between_pots,
                first_pot_spacing, current_pot_index)

        cmds.polyCylinder(name="pot_base", radius=radius, height=height)
        cmds.xform(rotation=[angle], translation=[x_coord, 0, z_coord])

    def calculate_position(self, spacing_between_pots,
                           angle_between_pots, first_pot_spacing,
                           current_pot_index):
        # INPUT: current pot #, first pot spacing, general pot spacing,
        # pot angle
        # OUTPUT: x and y coords (floats) of pot in scene space
        #
        # create right triangle from origin, with angle as a parameter and
        # hypotenuse length as a parameter
        # (each parameter will be multiplied by pot index
        # to create increasing distance from center.
        # this creates a spiral of pots outwards as pot index goes up)
        # return x and y coordinates of farthest point,
        # where pot will ultimately be positioned
        #
        # following formulas are based on sohcahtoa
        # modified to fit my needs
        # x = (distance * index + initial_distance) * cos(angle * index)
        # y is same but sin instead of cos
        # returns (x_coord, y_coord)

        x_coord = (spacing_between_pots * current_pot_index +
                   first_pot_spacing) * math.cos(angle_between_pots *
                                                 current_pot_index)
        z_coord = (spacing_between_pots * current_pot_index +
                   first_pot_spacing) * math.sin(angle_between_pots *
                                                 current_pot_index)
        return (x_coord, z_coord)

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
