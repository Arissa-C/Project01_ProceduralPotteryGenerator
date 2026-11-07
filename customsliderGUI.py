from PySide2 import QtWidgets, QtCore
from enum import Enum


class Bounding_Type(Enum):
    # used in customsliderGUI, potteryGUI
    # used to link customsliders together and flag their relationships
    NONE = 0
    MIN = 1
    MAX = 2


class Custom_Slider(QtWidgets.QSlider):

    def __init__(self, name: str, scaling=None, value=100, min=0, max=200):
        super().__init__()

        # custom slider values
        self.name: str = name
        self.scaling = scaling
        self.bounded_slider: QtWidgets.QSlider
        self.bounded_slider_type: Bounding_Type = Bounding_Type.NONE

        # base slider values
        self.setRange(min, max)
        self.setValue(value)
        self.setOrientation(QtCore.Qt.Horizontal)

        # handle labels, signal connections
        self.set_label()
        self.label_decimal_places = self.get_decimal_places_from_scaling()
        self.valueChanged.connect(self.update_slider_text)
        self.sliderReleased.connect(self.enforce_slider_bounds)

    def get_decimal_places_from_scaling(self):
        # if scaling is a decimal, return how many decimal places are provided
        pass

    def get_scaled_value(self):
        # scaled value allows me to bypass QSlider being restricted to ints
        # ex. value = 10, scaling = 0.01, scaled_value = 0.1
        # if no scaling, then treat slider as normal and return int value
        #
        # need to handle if scaling requires more decimal places than .1f
        if self.scaling:
            return float(format(self.value()*self.scaling, '.1f'))
        return self.value()

    def set_label(self):
        # create label for slider, displays name and value
        self.assigned_label = QtWidgets.QLabel()
        self.assigned_label.setText(
            self.name + ": " + str(self.get_scaled_value()))

    def get_label(self):
        # this method mostly used by QFormLayouts in potteryGUI
        return self.assigned_label

    def update_slider_text(self, value):
        # connected to QSlider.valueChanged
        # lets label display slider scaled_value
        self.assigned_label.setText(
            self.name + ": " + str(self.get_scaled_value()))

    def set_bounded_slider(
            self, slider: QtWidgets.QSlider, type: Bounding_Type):
        # if slider is in a MIN-MAX pair, declare explicitly with this method
        # makes sliders subject to enforce_slider_bounds
        self.bounded_slider = slider
        self.bounded_slider_type = type
        if self.bounded_slider_type is Bounding_Type.MAX:
            self.setMaximum(self.bounded_slider.value())
        elif self.bounded_slider_type is Bounding_Type.MIN:
            self.setMinimum(self.bounded_slider.value())

    def enforce_slider_bounds(self):
        # connected to QSlider.sliderReleased
        #
        # works as input validation for sliders
        # prevents MIN-type sliders from exceeding MAX counterpart & vice-versa
        # this is done by making the value of MIN the lower bound of MAX
        # and value of MAX becomes the lower bound of MIN
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
