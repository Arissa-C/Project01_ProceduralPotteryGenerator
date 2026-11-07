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

        # remember defaults
        self.default_value = value
        self.default_min = min
        self.default_max = max
        self.reset_to_defaults()
        self.setOrientation(QtCore.Qt.Horizontal)

        # handle labels, signal connections
        self.label_decimal_places = self.get_decimal_places_from_scaling()
        self.set_label()
        self.valueChanged.connect(self.update_slider_text)
        self.sliderReleased.connect(self.enforce_slider_bounds)

    def reset_to_defaults(self):
        self.setRange(self.default_min, self.default_max)
        self.setValue(self.default_value)
        self.enforce_own_bounds()

    def get_decimal_places_from_scaling(self):
        # if scaling is a decimal, return how many decimal places are provided
        if not self.scaling or self.scaling is int:
            return 0
        else:
            return str(self.scaling)[::-1].find('.')

    def get_scaled_value(self):
        # scaled value allows me to bypass QSlider being restricted to ints
        # ex. value = 10, scaling = 0.01, scaled_value = 0.1
        # if no scaling, then treat slider as normal and return int value
        if self.scaling:
            return float(self.value()*self.scaling)
        return self.value()

    def get_display_value(self):
        # called by labels
        # truncates scaled value based on decimal places given in scaling
        if self.label_decimal_places > 0:
            return format(self.get_scaled_value(),
                          '.' + str(self.label_decimal_places) + 'f')
        return str(self.get_scaled_value())

    def set_label(self):
        # create label for slider, displays name and value
        self.assigned_label = QtWidgets.QLabel()
        self.update_slider_text(0)

    def get_label(self):
        # this method mostly used by QFormLayouts in potteryGUI
        return self.assigned_label

    def update_slider_text(self, value):
        # connected to QSlider.valueChanged
        # lets label display slider scaled_value
        self.assigned_label.setText(
            self.name + ": " + self.get_display_value())

    def set_bounded_slider(
            self, slider: QtWidgets.QSlider, type: Bounding_Type):
        # if slider is in a MIN-MAX pair, declare explicitly with this method
        # makes sliders subject to enforce_slider_bounds
        self.bounded_slider = slider
        self.bounded_slider_type = type
        # self.enforce_own_bounds()
        self.enforce_own_bounds()

    def enforce_own_bounds(self):
        '''
        # ad-hoc enum equality check here too
        '''
        # if connected slider is a max type, set its value as this sliders max
        # if connected slider is a min type, set its value as this sliders min
        if str(self.bounded_slider_type) == str(Bounding_Type.MAX):
            self.setMaximum(self.bounded_slider.value())
        elif str(self.bounded_slider_type) == str(Bounding_Type.MIN):
            self.setMinimum(self.bounded_slider.value())

    def enforce_slider_bounds(self):
        # connected to QSlider.sliderReleased
        #
        # works as input validation for sliders
        # prevents MIN-type sliders from exceeding MAX counterpart & vice-versa
        # this is done by making the value of MIN the lower bound of MAX
        # and value of MAX becomes the lower bound of MIN

        '''
        # had to change enum comparison via "is" keyword
        # it used to look like self.bounded_slider_type is Bounding_Type.Max
        # now, it converts enums to str and check literal equality via ==
        # this is because out of nowhere, the code here stopped working
        #
        # debugging via print isolated that the enum equality booleans
        # were the problem
        # in essence, "Bounding_Type.MAX is Bounding_Type.MAX" was
        # returning false and StackOverflow says its a module import problem
        '''
        if str(self.bounded_slider_type) == str(Bounding_Type.MAX):
            new_min = self.value()
            self.bounded_slider.setMinimum(new_min)
            if self.bounded_slider.value() < new_min:
                self.bounded_slider.setValue(new_min)
        elif str(self.bounded_slider_type) == str(Bounding_Type.MIN):
            new_max = self.value()
            self.bounded_slider.setMaximum(new_max)
            if self.bounded_slider.value() > new_max:
                self.bounded_slider.setValue(new_max)
