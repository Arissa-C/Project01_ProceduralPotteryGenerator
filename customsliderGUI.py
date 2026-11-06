from PySide2 import QtWidgets, QtCore
from enum import Enum


class Bounding_Type(Enum):
    NONE = 0
    MIN = 1
    MAX = 2


class Custom_Slider(QtWidgets.QSlider):
    def __init__(self, name: str, scaling=None, value=100, min=0, max=200):
        super().__init__()
        self.name: str = name
        self.scaling = scaling
        self.bounded_slider: QtWidgets.QSlider
        self.bounded_slider_type: Bounding_Type = Bounding_Type.NONE

        self.setRange(min, max)
        self.setValue(value)
        self.setOrientation(QtCore.Qt.Horizontal)

        self.set_label()
        self.valueChanged.connect(self.update_slider_text)
        self.sliderReleased.connect(self.enforce_slider_bounds)

    def get_scaled_value(self):
        if self.scaling:
            return float(format(self.value()*self.scaling, '.1f'))
        return self.value()

    def set_label(self):
        self.assigned_label = QtWidgets.QLabel()
        self.assigned_label.setText(
            self.name + ": " + str(self.get_scaled_value()))

    def get_label(self):
        return self.assigned_label

    def update_slider_text(self, value):
        self.assigned_label.setText(
            self.name + ": " + str(self.get_scaled_value()))

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
