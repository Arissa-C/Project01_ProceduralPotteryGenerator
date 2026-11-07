import maya.OpenMayaUI as omui
import importlib
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
        self.setLayout(self.main_window)

    def create_height_section(self):
        # pot height related widgets, enclosed in a groupbox
        section_form_layout = QtWidgets.QFormLayout()

        # height sliders
        self.slider_max_height = Custom_Slider("Max height", 0.01, 150)
        self.slider_min_height = Custom_Slider("Min height", 0.01, 50)
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
        # pot width related widgets, enclosed in a groupbox
        section_form_layout = QtWidgets.QFormLayout()

        # width sliders
        self.slider_max_width = Custom_Slider("Max width", 0.01, 50)
        self.slider_min_width = Custom_Slider("Min width", 0.01, 20)
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
        # pot distribution related widgets, enclosed in a groupbox
        section_form_layout = QtWidgets.QFormLayout()

        # distribution parameters
        self.slider_total_pots = Custom_Slider(
            "Total pots", None, 10, 0, 50)
        self.slider_rotation_jitter = Custom_Slider(
            "Rotation jitter", None, 180, 0, 360)
        self.slider_pot_angle = Custom_Slider(
            "Distribution angle", None, 30, 0, 180)
        self.slider_pot_spacing = Custom_Slider(
            "Distribution spacing", 0.01, 20, 0, 200)
        self.slider_first_pot_spacing = Custom_Slider(
            "Distance from center", 0.1, 7, 0, 100)
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
        section_group_box = QtWidgets.QGroupBox("Pots distribution")
        section_group_box.setLayout(section_form_layout)

        return section_group_box

    def create_group_name_edit(self):
        # QLineEdit widget that lets user change group name
        section_form_layout = QtWidgets.QFormLayout()

        self.group_name_edit = QtWidgets.QLineEdit()
        self.group_name_edit.setMaxLength(50)
        self.group_name_edit.setValidator(Pottery_Name_Validator)
        self.group_name_edit.setText("pots_grp")

        self.group_name_label = QtWidgets.QLabel()
        self.group_name_label.setText("Group Name")

        section_form_layout.addRow(self.group_name_label, self.group_name_edit)
        return section_form_layout

    def create_connections(self):
        self.create_btn.clicked.connect(self.create)

    @QtCore.Slot()
    def create(self):
        # when create button is clicked
        # send values to potterygenerator and create pot set
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
            self.group_name_edit.text())
        self.pottery_generator.create()


# Create objects and run
potterygui1 = Pottery_GUI()
potterygui1.show()
