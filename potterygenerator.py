import math

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
        # other parameters
        self.grp_name = "myPottery"

    def set_values(self, total_pots,
                   rotation_jitter,
                   spacing_between_pots, angle_between_pots,
                   first_pot_spacing,
                   min_height, max_height,
                   min_radius, max_radius, grp_name):
        # allows external dump of parameters into Pottery properties
        # to be called before create()
        self.total_pots, self.rotation_jitter, self.spacing_between_pots, \
            self.angle_between_pots, self.first_pot_spacing, \
            self.min_height, self.max_height, \
            self.min_radius, self.max_radius, \
            self.grp_name = \
            (total_pots,
                rotation_jitter,
                spacing_between_pots, angle_between_pots,
                first_pot_spacing,
                min_height, max_height,
                min_radius, max_radius, grp_name)

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

        final_group = cmds.group(group_objs, name=self.grp_name)
        self.color_pots(final_group)

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
        cmds.xform(rotation=[0, angle, 0],
                   translation=[x_coord, height/2, z_coord])

        # create spherical pot top based on same arguments
        pot_top_obj = self.create_pot_top(radius, angle,
                                          [x_coord, height, z_coord])

        # create torus pot mouth based on same arguments
        pot_mouth_obj = self.create_pot_mouth(radius, angle,
                                              [x_coord,
                                               height+(radius*0.9),
                                               z_coord])

        pot_group = cmds.group([pot_base_obj,
                                pot_top_obj,
                                pot_mouth_obj],
                               name="pot_GRP")

        return pot_group

    def create_pot_top(self, radius, rotation, translation):
        # create sphere of same radius as base cylinder
        pot_top_obj, pot_top_node = cmds.polySphere(
            name="pot_top", radius=radius)

        # translate to top of cylinder, rotate to same angle
        cmds.xform(rotation=[0, rotation, 0],
                   translation=translation)

        return pot_top_obj

    def create_pot_mouth(self, radius, rotation, translation):
        # create torus of smaller radius as base cylinder
        major_radius = radius/2
        minor_radius = radius/16

        pot_mouth_obj, pot_mouth_node = cmds.polyTorus(
            name="pot_mouth", radius=major_radius,
            sectionRadius=minor_radius)

        # translate to top of pot_top, rotate to same angle
        cmds.xform(rotation=[0, rotation, 0],
                   translation=translation)

        return pot_mouth_obj

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

    def color_pots(self, group):
        # get pot shapes, shaders, set color
        shape = cmds.ls(o=True, shapes=True)
        shadingGrps = cmds.listConnections(shape, type='shadingEngine')
        shaders = cmds.ls(cmds.listConnections(shadingGrps),
                          materials=True)
        cmds.setAttr(shaders[0]+".baseColor",
                     150/255, 76/255, 55/255, type="double3")
