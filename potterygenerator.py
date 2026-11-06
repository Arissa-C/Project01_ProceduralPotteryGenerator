import math

from PySide2 import QtWidgets, QtCore
from enum import Enum

import maya.cmds as cmds
import random


class Bounding_Type(Enum):
    MIN = 0
    MAX = 1


class Custom_Slider(QtWidgets.QSlider):
    def __init__(self, name: str):
        super().__init__()
        self.name: str = name
        self.bounding_slider: QtWidgets.QSlider
        self.bounding_slider_type: Bounding_Type

        self.setMinimum(0)
        self.setMaximum(10)
        self.setValue(5)
        self.setOrientation(QtCore.Qt.Horizontal)

        self.set_label()
        self.sliderMoved.connect(self.update_slider_text)
        self.sliderReleased.connect(self.enforce_slider_bounds)

    def set_label(self):
        self.assigned_label = QtWidgets.QLabel()
        self.assigned_label.setText(
            self.name + ": " + str(self.value()))

    def get_label(self):
        return self.assigned_label

    def update_slider_text(self, position):
        self.assigned_label.setText(
            self.name + ": " + str(position))

    def set_bounding_slider(
            self, slider: QtWidgets.QSlider, type: Bounding_Type):
        self.bounding_slider = slider
        self.bounding_slider_type = type

    def enforce_slider_bounds(self):
        if self.bounding_slider_type is Bounding_Type.MAX:
            self.setMaximum(self.bounding_slider.value())
        elif self.bounding_slider_type is Bounding_Type.MIN:
            self.setMinimum(self.bounding_slider.value())


class Pottery_GUI(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        # self.pottery_generator = Pottery()
        self.setWindowTitle("Pot Generator 9000")
        self.create_layout()
        # self.create_connections()

    def create_layout(self):
        self.main_window = QtWidgets.QVBoxLayout()
        self._form_ui()
        self.create_btn = QtWidgets.QPushButton("Create")
        self.main_window.addWidget(self.create_btn)
        self.setLayout(self.main_window)

    def _form_ui(self):
        self.form_lay = QtWidgets.QFormLayout()

        # example double spin box
        self.torso_rad_dspnbx = QtWidgets.QDoubleSpinBox()
        self.torso_rad_dspnbx.setValue(0.5)

        self.form_lay.addRow("Torso radius", self.torso_rad_dspnbx)

        # height sliders
        self.slider_max_height = Custom_Slider("Max height")
        self.slider_min_height = Custom_Slider("Min height")
        self.slider_max_height.set_bounding_slider(
            self.slider_min_height, Bounding_Type.MIN)
        self.slider_min_height.set_bounding_slider(
            self.slider_max_height, Bounding_Type.MAX)
        self.form_lay.addRow(
            self.slider_max_height.get_label(), self.slider_max_height)
        self.form_lay.addRow(
            self.slider_min_height.get_label(), self.slider_min_height)

        self.main_window.addLayout(self.form_lay)

    '''
    def _fix_slider_position(self):
        pass

    def create_connections(self):
        self.create_btn.clicked.connect(self.create)

    @QtCore.Slot()
    def create(self):
        self.pottery_generator.torso_radius = self.torso_rad_dspnbx.value()
        self.pottery_generator.create()
    '''


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
        # naming parameters
        self.grp_name = "potSet"
        pass

    def create(self):
        # creates whole set of pots
        # call create one pot method in loop
        # use for loop, loop based on range(total_pots)
        # inside loop
        group_objs = []

        for pot_index in range(self.total_pots):
            group_objs.append(self.create_pot(self.min_height, self.max_height,
                              self.min_radius, self.max_radius,
                              self.rotation_jitter, self.spacing_between_pots,
                              self.angle_between_pots, self.first_pot_spacing,
                              pot_index))

        cmds.group(group_objs, name=self.grp_name)

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

        pot_base_obj, pot_base_node = cmds.polyCylinder(
            name="pot_base", radius=radius, height=height)
        cmds.xform(rotation=[0, angle, 0], translation=[x_coord, 0, z_coord])

        return pot_base_obj

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


# Create objects and run
potterygui1 = Pottery_GUI()
potterygui1.show()
