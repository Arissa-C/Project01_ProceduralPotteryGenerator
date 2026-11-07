import maya.OpenMayaUI as omui
import importlib
import string
import customsliderGUI
import potterygenerator
import potterynamevalidator

from customsliderGUI import Bounding_Type, Custom_Slider
from potterygenerator import Pottery
from potterynamevalidator import Pottery_Name_Validator
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance

importlib.reload(customsliderGUI)
importlib.reload(potterygenerator)
importlib.reload(potterynamevalidator)


def get_main_maya_window():
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window), QtWidgets.QWidget)


class Pottery_GUI(QtWidgets.QDialog):

    def __init__(self):
        super().__init__(parent=get_main_maya_window())
        self.default_max_height = 70
        self.default_min_height = 40
        self.default_max_width = 50
        self.default_min_width = 20
        self.default_total_pots = 10
        self.default_rotation_jitter = 180
        self.default_angle = 30
        self.default_spacing = 20
        self.default_distance = 7
        self.default_group_name = "myPots"
        self.default_color = (150/255, 76/255, 55/255)

        self.pottery_generator = Pottery()
        self.setWindowTitle("Pot Generator 9000")
        self.setWindowFlag(QtCore.Qt.WindowType.Tool)
        self.create_layout()
        self.create_connections()

    def create_layout(self):
        # Overall window layout, smaller sections and widgets added here
        self.main_window = QtWidgets.QVBoxLayout()

        self.main_window.addWidget(self.create_height_section())
        self.main_window.addWidget(self.create_width_section())
        self.main_window.addWidget(self.create_distribution_section())

        self.main_window.addLayout(self.create_group_name_edit())
        self.create_btn = QtWidgets.QPushButton("Create")
        self.main_window.addWidget(self.create_btn)
        self.reset_btn = QtWidgets.QPushButton("Reset")
        self.main_window.addWidget(self.reset_btn)
        self.setLayout(self.main_window)

    def create_height_section(self):
        # pot height related widgets, enclosed in a groupbox
        section_form_layout = QtWidgets.QFormLayout()

        # height sliders
        self.slider_max_height = Custom_Slider(
            "Max height", 0.01, self.default_max_height)
        self.slider_min_height = Custom_Slider(
            "Min height", 0.01, self.default_min_height)
        self.slider_max_height.set_bounded_slider(
            self.slider_min_height, Bounding_Type.MIN)
        self.slider_min_height.set_bounded_slider(
            self.slider_max_height, Bounding_Type.MAX)
        section_form_layout.addRow(
            self.slider_max_height.get_label(), self.slider_max_height)
        section_form_layout.addRow(
            self.slider_min_height.get_label(), self.slider_min_height)

        # add sliders to groupbox
        section_group_box = QtWidgets.QGroupBox("Height range")
        section_group_box.setLayout(section_form_layout)

        return section_group_box

    def create_width_section(self):
        # pot width related widgets, enclosed in a groupbox
        section_form_layout = QtWidgets.QFormLayout()

        # width sliders
        self.slider_max_width = Custom_Slider(
            "Max width", 0.01, self.default_max_width)
        self.slider_min_width = Custom_Slider(
            "Min width", 0.01, self.default_min_width)
        self.slider_max_width.set_bounded_slider(
            self.slider_min_width, Bounding_Type.MIN)
        self.slider_min_width.set_bounded_slider(
            self.slider_max_width, Bounding_Type.MAX)
        section_form_layout.addRow(
            self.slider_max_width.get_label(), self.slider_max_width)
        section_form_layout.addRow(
            self.slider_min_width.get_label(), self.slider_min_width)

        # add sliders to groupbox
        section_group_box = QtWidgets.QGroupBox("Width (radius) range")
        section_group_box.setLayout(section_form_layout)

        return section_group_box

    def create_distribution_section(self):
        # pot distribution related widgets, enclosed in a groupbox
        section_form_layout = QtWidgets.QFormLayout()

        # distribution parameters
        self.slider_total_pots = Custom_Slider(
            "Total pots", None, self.default_total_pots, 0, 50)
        self.slider_rotation_jitter = Custom_Slider(
            "Rotation jitter", None, self.default_rotation_jitter, 0, 360)
        self.slider_pot_angle = Custom_Slider(
            "Distribution angle", None, self.default_angle, 0, 180)
        self.slider_pot_spacing = Custom_Slider(
            "Distribution spacing", 0.01, self.default_spacing, 0, 200)
        self.slider_first_pot_spacing = Custom_Slider(
            "Distance from center", 0.1, self.default_distance, 0, 100)
        section_form_layout.addRow(self.slider_total_pots.get_label(),
                                   self.slider_total_pots)
        section_form_layout.addRow(self.slider_rotation_jitter.get_label(),
                                   self.slider_rotation_jitter)
        section_form_layout.addRow(self.slider_pot_angle.get_label(),
                                   self.slider_pot_angle)
        section_form_layout.addRow(self.slider_pot_spacing.get_label(),
                                   self.slider_pot_spacing)
        section_form_layout.addRow(self.slider_first_pot_spacing.get_label(),
                                   self.slider_first_pot_spacing)

        # add parameters to groupbox
        section_group_box = QtWidgets.QGroupBox("Distribution")
        section_group_box.setLayout(section_form_layout)

        return section_group_box

    def create_group_name_edit(self):
        # QLineEdit widget that lets user change group name
        section_form_layout = QtWidgets.QFormLayout()

        self.group_name_edit = QtWidgets.QLineEdit()
        self.group_name_edit.setMaxLength(50)
        self.group_name_edit.setText(self.default_group_name)
        self.group_name_edit.setPlaceholderText(
            "Cannot be blank or begin with digit")

        self.name_validator = Pottery_Name_Validator()
        self.group_name_edit.setValidator(self.name_validator)

        self.group_name_label = QtWidgets.QLabel()
        self.group_name_label.setText("Group Name")

        section_form_layout.addRow(self.group_name_label, self.group_name_edit)
        return section_form_layout

    def check_valid_group_name(self):
        text_to_check = self.group_name_edit.text()

        # if group name is empty, has digit in first position
        # return False
        if not text_to_check:
            return False
        elif text_to_check[0] in string.digits:
            return False

        # if all checks pass, return True
        return True

    def create_connections(self):
        self.create_btn.clicked.connect(self.create)
        self.reset_btn.clicked.connect(self.reset)

    @QtCore.Slot()
    def reset(self):
        # reset all values to defaults
        self.slider_max_height.setValue(self.default_max_height)
        self.slider_min_height.setValue(self.default_min_height)
        self.slider_max_width.setValue(self.default_max_width)
        self.slider_min_width.setValue(self.default_min_width)
        self.slider_total_pots.setValue(self.default_total_pots)
        self.slider_rotation_jitter.setValue(self.default_rotation_jitter)
        self.slider_pot_angle.setValue(self.default_angle)
        self.slider_pot_spacing.setValue(self.default_spacing)
        self.slider_first_pot_spacing.setValue(self.default_distance)
        self.group_name_edit.setText(self.default_group_name)

    @QtCore.Slot()
    def create(self):
        # when create button is clicked
        # check if group name is valid
        # namevalidator class cannot address intermediate states
        if self.check_valid_group_name():
            # if valid, send values to potterygenerator and create pot set
            self.group_name_label.setText("Group Name")
            self.pottery_generator.set_values(
                self.slider_total_pots.get_scaled_value(),
                self.slider_rotation_jitter.get_scaled_value(),
                self.slider_pot_spacing.get_scaled_value(),
                self.slider_pot_angle.get_scaled_value(),
                self.slider_first_pot_spacing.get_scaled_value(),
                self.slider_min_height.get_scaled_value(),
                self.slider_max_height.get_scaled_value(),
                self.slider_min_width.get_scaled_value(),
                self.slider_max_width.get_scaled_value(),
                self.group_name_edit.text(),
                self.default_color)
            self.pottery_generator.create()
        else:
            self.group_name_label.setText("Invalid Name")


# Create objects and run
potterygui1 = Pottery_GUI()
potterygui1.show()
