import math

from PySide2 import QtWidgets, QtCore
from enum import Enum

import maya.cmds as cmds
import random


class Bounding_Type(Enum):
    MIN = 0
    MAX = 1


class Custom_Slider(QtWidgets.QSlider):
    def __init__(self, name: str, min=0, max=20, value=10):
        super().__init__()
        self.name: str = name
        self.bounded_slider: QtWidgets.QSlider
        self.bounded_slider_type: Bounding_Type

        self.setRange(min, max)
        self.setValue(value)
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

    def set_bounded_slider(
            self, slider: QtWidgets.QSlider, type: Bounding_Type):
        self.bounded_slider = slider
        self.bounded_slider_type = type
        if self.bounded_slider_type is Bounding_Type.MAX:
            self.setMaximum(self.bounded_slider.value())
        elif self.bounded_slider_type is Bounding_Type.MIN:
            self.setMinimum(self.bounded_slider.value())

    def enforce_slider_bounds(self):
        if self.bounded_slider_type is Bounding_Type.MAX:
            new_min = self.value()
            self.bounded_slider.setMinimum(new_min)
            if self.bounded_slider.value() < new_min:
                self.bounded_slider.setValue(new_min)
        elif self.bounded_slider_type is Bounding_Type.MIN:
            new_max = self.value()
            self.bounded_slider.setMaximum(new_max)
            if self.bounded_slider.value() > new_max:
                self.bounded_slider.setValue(new_max)


class Pottery_GUI(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        # self.pottery_generator = Pottery()
        self.setWindowTitle("Pot Generator 9000")
        self.create_layout()
        # self.create_connections()

    def create_layout(self):
        self.main_window = QtWidgets.QVBoxLayout()

        self.main_window.addWidget(self.create_height_section())
        self.main_window.addWidget(self.create_width_section())
        self.main_window.addWidget(self.create_distribution_section())

        self.create_btn = QtWidgets.QPushButton("Create")
        self.main_window.addWidget(self.create_btn)
        self.setLayout(self.main_window)

    def create_height_section(self):
        section_form_layout = QtWidgets.QFormLayout()

        # height sliders
        self.slider_max_height = Custom_Slider("Max height")
        self.slider_min_height = Custom_Slider("Min height")
        self.slider_max_height.set_bounded_slider(
            self.slider_min_height, Bounding_Type.MIN)
        self.slider_min_height.set_bounded_slider(
            self.slider_max_height, Bounding_Type.MAX)
        section_form_layout.addRow(
            self.slider_max_height.get_label(), self.slider_max_height)
        section_form_layout.addRow(
            self.slider_min_height.get_label(), self.slider_min_height)

        # add sliders to groupbox
        section_group_box = QtWidgets.QGroupBox("Pots height")
        section_group_box.setLayout(section_form_layout)

        return section_group_box

    def create_width_section(self):
        section_form_layout = QtWidgets.QFormLayout()

        # width sliders
        self.slider_max_width = Custom_Slider("Max width")
        self.slider_min_width = Custom_Slider("Min width")
        self.slider_max_width.set_bounded_slider(
            self.slider_min_width, Bounding_Type.MIN)
        self.slider_min_width.set_bounded_slider(
            self.slider_max_width, Bounding_Type.MAX)
        section_form_layout.addRow(
            self.slider_max_width.get_label(), self.slider_max_width)
        section_form_layout.addRow(
            self.slider_min_width.get_label(), self.slider_min_width)

        # add sliders to groupbox
        section_group_box = QtWidgets.QGroupBox("Pots width (radius)")
        section_group_box.setLayout(section_form_layout)

        return section_group_box

    def create_distribution_section(self):
        section_form_layout = QtWidgets.QFormLayout()

        # distribution parameters
        self.slider_rotation_jitter = Custom_Slider(
            "Rotation jitter", 0, 360, 180)
        section_form_layout.addRow(self.slider_rotation_jitter.get_label(),
                                   self.slider_rotation_jitter)

        # add parameters to groupbox
        section_group_box = QtWidgets.QGroupBox("Pots distribution")
        section_group_box.setLayout(section_form_layout)

        return section_group_box

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
