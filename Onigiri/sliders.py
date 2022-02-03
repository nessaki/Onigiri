
import os
import bpy
import sys
#import time
import mathutils

from . import utils

# from . import mod_settings
# from .mod_settings import bb_settings

# ------------------------------------------------------------------------------------------------
# props
# ------------------------------------------------------------------------------------------------
if 1 == 1:

    props = {}

    # NOPE: I have to call the enabler multiple times, 1 for each pole that needs it, well... not
    # really but it's goofy inconsistent if I do it for just one unless that ONE is dedicated FOR
    # the purpose.
    #
    # These enablers are set by the operator poll method so that I don't have to do it in both the
    # operator and in the UI.  In this way we can test directly for it in the UI and choose to
    # display, enable or disable the view of the option all-together.

    # I think I'm not using these now.  I'll just disable them until I'm sure.
    if 1 == 0:
        props['add_selected_enabled'] = False
        props['del_selected_enabled'] = False
        props['pose_bones'] = []
        props['ui'] = set('bb_sliders_scale')

    # Using this instead of loading mod_settings.
    props['terminate'] = False

    # In order to know about a select state I am using two containers.  They will come from ...
    # bpy.context.selected_objects and are used only for their test for equality, the items do
    # not need to be checked for usability.  I will use this along with 'last_rig' to know what
    # needs to be changed.  If these to properties do not contain exactly the same thing then I
    # may have some work to do so I check 'last_rig' for that.  After the work I'll check to see
    # if I have a qualified, and single, rig selected and, if so, that becomes my 'last_rig' after
    # the fact.
    props['this_selection'] = None
    props['last_selection'] = None

    # I want to record what the last rig was before the current one was selected.  This way I can
    # revert the last rig back to the original bone scale inheritance if they select a new rig or
    # object.  Once I find the last rig I restore all of the bones 'bb_sliders_inherit' properties,
    # set the last_rig to None and let the UI detect that it will be a first run on the new object.
    props['last_rig'] = None
    props['this_rig'] = None

# ------------------------------------------------------------------------------------------------
# pose boe property updaters for the sliders
# ------------------------------------------------------------------------------------------------
def update_location_x(self, context):
    if props['terminate'] == True:
        print("Terminating recursion")
        props['terminate'] = False
        return
    armObj = bpy.context.selected_objects[0]
    boneObj = armObj.pose.bones[self.name]
    boneObj.location[0] = self.bb_sliders_location_x
def update_location_y(self, context):
    if props['terminate'] == True:
        print("Terminating recursion")
        props['terminate'] = False
        return
    armObj = bpy.context.selected_objects[0]
    boneObj = armObj.pose.bones[self.name]
    boneObj.location[1] = self.bb_sliders_location_y
def update_location_z(self, context):
    if props['terminate'] == True:
        print("Terminating recursion")
        props['terminate'] = False
        return
    armObj = bpy.context.selected_objects[0]
    boneObj = armObj.pose.bones[self.name]
    boneObj.location[2] = self.bb_sliders_location_z

def update_scale_x(self, context):
    if props['terminate'] == True:
        print("Terminating recursion")
        props['terminate'] = False
        return
    armObj = bpy.context.selected_objects[0]
    boneObj = armObj.pose.bones[self.name]
    boneObj.scale[0] = 1 + self.bb_sliders_scale_x
    if self.bb_sliders_scale_y_lock == True:
        boneObj.scale[1] = 1 + self.bb_sliders_scale_x
    if self.bb_sliders_scale_z_lock == True:
        boneObj.scale[2] = 1 + self.bb_sliders_scale_x
def update_scale_y(self, context):
    if props['terminate'] == True:
        print("Terminating recursion")
        props['terminate'] = False
        return
    armObj = bpy.context.selected_objects[0]
    boneObj = armObj.pose.bones[self.name]
    boneObj.scale[1] = 1 + self.bb_sliders_scale_y
    if self.bb_sliders_scale_x_lock == True:
        boneObj.scale[0] = 1 + self.bb_sliders_scale_y
    if self.bb_sliders_scale_z_lock == True:
        boneObj.scale[2] = 1 + self.bb_sliders_scale_y
def update_scale_z(self, context):
    if props['terminate'] == True:
        print("Terminating recursion")
        props['terminate'] = False
        return
    armObj = bpy.context.selected_objects[0]
    boneObj = armObj.pose.bones[self.name]
    boneObj.scale[2] = 1 + self.bb_sliders_scale_z
    if self.bb_sliders_scale_x_lock == True:
        boneObj.scale[0] = 1 + self.bb_sliders_scale_z
    if self.bb_sliders_scale_y_lock == True:
        boneObj.scale[1] = 1 + self.bb_sliders_scale_z

# ------------------------------------------------------------------------------------------------
# reset
# ------------------------------------------------------------------------------------------------
# UPDATE: location and scale are no longer useful, I'm resetting everything.  If I need that feature
# later I'll add a new function.
#
# resets a single bone and the associated slider for the active transform
#def reset(boneObj, location=False, scale=False):
def reset(boneObj):
    if boneObj:
        if isinstance(boneObj, str):
            print("Requires a bone object, not string")
            return False
    else:
        print("No bone object delivered")
        return False

    boneObj.matrix_basis = mathutils.Matrix()

    boneObj.property_unset("bb_sliders_location_x")
    boneObj.property_unset("bb_sliders_location_y")
    boneObj.property_unset("bb_sliders_location_z")

    boneObj.property_unset("bb_sliders_scale_x")
    boneObj.property_unset("bb_sliders_scale_y")
    boneObj.property_unset("bb_sliders_scale_z")
    boneObj.property_unset("bb_sliders_scale_x_lock")
    boneObj.property_unset("bb_sliders_scale_y_lock")
    boneObj.property_unset("bb_sliders_scale_z_lock")

# ------------------------------------------------------------------------------------------------
# set inherit
# ------------------------------------------------------------------------------------------------
# Record and then set the inherit_scale property of all data bones in this rig.
# UPDATE: added a matrix property to the bones.
def set_rig(armObj=None):
    if armObj == None:
        if props['this_rig'] == None:
            return
        armObj = props['this_rig']
        if utils.is_valid(armObj) == False:
            return
    for boneObj in armObj.pose.bones:
        dBone = boneObj.bone
        # Get our property or, if it doesn't exist, it's own for a filler hastening this function.
        boneObj['bb_sliders_inherit'] = dBone.inherit_scale
        dBone.inherit_scale = 'NONE'  # yes it's cap, it's a key word

        # UPDATE: I can't do this here!  I need to do it in "sliders_store".
        #
        # Note that these two properties are not the same, one is on the data bone and one is on
        # the pose bone for their corresponding data.  At the time of this writing I didn't
        # need the pose matrix but I may use it later to restore their previous pose.
#        boneObj['bb_sliders_matrix'] = boneObj.matrix.copy()
        # This will give me the same matrix as edit, minus the roll, which I can get from ...
        # utils.get_bone_roll(mat).  I'll only be using this if they want to restore the rig
        # to the state before the damage or to the "store" state.
 #       boneObj.bone['bb_sliders_matrix'] = boneObj.bone.matrix.copy()
 #       boneObj.bone['bb_sliders_head_local'] = boneObj.bone.head_local.copy()
 #       boneObj.bone['bb_sliders_tail_local'] = boneObj.bone.tail_local.copy()

    return True
# ------------------------------------------------------------------------------------------------
# restore rig
# ------------------------------------------------------------------------------------------------
# Restore the inherit_scale property of all data bones in this rig using our custom property.
def restore_rig(armObj=None):
    # If I enter this function with armObj set to False it means that I probably ran from the
    # updater that closed the menu.  In that case I find the object from props['last_rig'] if it
    # exists and I restore from that.
    if armObj == None:
        if props['last_rig'] == None:
            return
        armObj = props['last_rig']
        if utils.is_valid(armObj) == False:
            return
    # Sanity check, prolly never happen
    if armObj.type != 'ARMATURE':
        print("sliders::restore_inherit : object is not an armature")
        return
    for boneObj in armObj.pose.bones:
        dBone = boneObj.bone
        boneObj.matrix = mathutils.Matrix(matrix)

    return True
# ------------------------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------------------------








