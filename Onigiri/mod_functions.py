







import uuid
import time

import mathutils
from mathutils import Vector
import decimal
import importlib
from math import *

import re
import os

import traceback








    
    
    

    
    
    
import bpy
from . import mod_flags
from . import mod_data
from .mod_flags import *
from .mod_data import *
from . import mod_settings
from .mod_settings import *






script_dir = os.path.dirname(os.path.abspath(__file__))
presets_path    =   bb_settings['paths']['presets']
data_path       =   bb_settings['paths']['data']











def terminate(state=""):
    if state == "":
        if bb_settings['terminate'] == True:
            bb_settings['terminate'] = False
            return True
    elif state == True:
        bb_settings['terminate'] = True
    else:
        print("terminate reports: unknown state setting -", state)
    return None





def selected_pose_bones():
    if len(bpy.context.selected_objects) > 1:
        return False
    if len(bpy.context.selected_objects) == 0:
        return False
    o = bpy.context.selected_objects[0]
    if o.type != 'ARMATURE':
        return False
    if bpy.context.mode != 'POSE':
        return False
    if len(bpy.context.selected_pose_bones) == 0:
        return False
    return len(bpy.context.selected_pose_bones)



def enable_pose_bone_priority():
    for boneObj in bpy.context.selected_pose_bones:
        boneObj['priority_enabled'] = 1



def disable_pose_bone_priority():
    for boneObj in bpy.context.selected_pose_bones:
        boneObj['priority_enabled'] = 0



def set_pose_bone_priority(priority=2):

    
    for boneObj in bpy.context.selected_pose_bones:
        boneObj['priority'] = priority



def apply_transforms(object="", scale=False, rotation=False, location=False):
    
    

    obj = bpy.data.objects
    if bpy.context.active_object == None:
        bpy.context.view_layer.objects.active = obj[object]
    for o in bpy.context.selected_objects:
        o.select_set(False)
    obj[object].select_set(True)
    bpy.ops.object.mode_set(mode='OBJECT')

    
    print("Making single user:", object)
    bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False)

    bpy.ops.object.transform_apply(scale=scale, rotation=rotation, location=location)






def apply_rest_pose(armature=""):
    if armature =="":
        print("apply_rest_pose: What?... nothing to clear!")
        return
    if armature not in bpy.data.objects.keys():
        print("apply_rest_pose: We don't have that object dood:", armature)
        return
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[armature].select_set(True)

    
    
    bpy.context.view_layer.objects.active = bpy.data.objects[armature]

    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.armature_apply()
    bpy.ops.object.mode_set(mode='OBJECT')
    return







def clear_pose(armature=""):
    if armature =="":
        print("clear_pose: What?... nothing to clear!")
        return
    if armature not in bpy.data.objects.keys():
        print("clear_pose: We don't have that object dood:", armature)
        return

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[armature].select_set(True)

    
    
    bpy.context.view_layer.objects.active = obj[target_rig]

    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action = 'SELECT')
    bpy.ops.pose.transforms_clear()
    bpy.ops.pose.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    return



def get_target_bones(arm, target_bones):
    
    
    
    

    
    
    

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]
    bpy.ops.object.mode_set(mode='EDIT')

    if bb_flags['debug'] == 1:
        print("Generating target bone list for:", arm)

    for bPart in bpy.data.objects[arm].data.bones:
        target_bones.append(bPart.name)

    bpy.ops.object.mode_set(mode='OBJECT')

    return













def save_target_links(obj, arm):

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]
    bpy.ops.object.mode_set(mode='EDIT')

    if bb_flags['debug'] == 1:
        print("Entering save_target_links with armature:", arm)

    
    if bb_flags['debug'] == 1:
        print("Generating child_list hash ...")

    for child_bone in bpy.data.objects[arm].data.edit_bones:
        parent_bone = ""
        try:
            parent_bone = getattr(bpy.data.objects[arm].data.edit_bones[child_bone.name].parent, "name")
            obj[arm].setdefault(parent_bone, [])
            obj[arm][parent_bone].append(child_bone.name)
        except:
            if bb_flags['debug'] == 1:
                print("no parent for, ", child_bone.name)
            pass

    bpy.ops.object.mode_set(mode='OBJECT')

    return



def save_source_links(arm, child_list):

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]
    bpy.ops.object.mode_set(mode='EDIT')

    if bb_flags['debug'] == 1:
        print("Entering save_soure_links with armature:", arm)

    
    if bb_flags['debug'] == 1:
        print("Generating child_list hash ...")

    for child_bone in bpy.data.objects[arm].data.edit_bones:
        parent_bone = ""
        try:
            parent_bone = getattr(bpy.data.objects[arm].data.edit_bones[child_bone.name].parent, "name")
            child_list.setdefault(parent_bone, [])
            child_list[parent_bone].append(child_bone.name)
        except:
            if bb_flags['debug'] == 1:
                print("no parent for, ", child_bone.name)
            pass

    bpy.ops.object.mode_set(mode='OBJECT')

    return



def apply_inheritance(arm, bone_list):





    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]
    bpy.ops.object.mode_set(mode='EDIT')

    for bone in bone_list:
        bpy.data.objects[arm].data.edit_bones[bone].use_local_location = bb_flags['inherit_location']
        bpy.data.objects[arm].data.edit_bones[bone].use_inherit_rotation = bb_flags['inherit_rotation']
        bpy.data.objects[arm].data.edit_bones[bone].use_inherit_scale = bb_flags['inherit_scale']

    bpy.ops.object.mode_set(mode='OBJECT') 

    return




def unhide_animation_bones(arm):
    

    
    l = range(0, 31) 
    for bone in all_pbones:
        for i in l:
            bpy.data.objects[arm].data.bones[bone].layers[i] = False

    set_mode(arm, "edit")

    
    for bone in all_pbones:
        bpy.data.objects[arm].data.edit_bones[bone].hide = False

    bpy.ops.object.mode_set(mode='POSE') 
    for bone in all_pbones:
        bpy.data.objects[arm].data.bones[bone].hide = False

    bpy.ops.object.mode_set(mode='OBJECT') 

    return



def view_required_layers(arm, layers_visible):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action = 'DESELECT')

    
    
    
    
    
    for vLayer in layers_visible:
        bpy.context.object.data.layers[vLayer] = True

    bpy.ops.object.mode_set(mode='OBJECT')

    return



def view_extras(arm, layers_extra):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]
    bpy.ops.object.mode_set(mode='POSE')

    for vLayer in layers_extra:
        bpy.context.object.data.layers[vLayer] = True

    bpy.ops.object.mode_set(mode='OBJECT')
    return



def hide_extras(arm, layers_extra):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]
    bpy.ops.object.mode_set(mode='POSE')

    for vLayer in layers_extra:
        bpy.context.object.data.layers[vLayer] = False

    bpy.ops.object.mode_set(mode='OBJECT')
    return



def force_unhide(arm, hidden_bones):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]

    
    
    
    
    bpy.ops.object.mode_set(mode='EDIT')

    for pBone in hidden_bones:
        bpy.data.objects[arm].data.edit_bones[pBone].hide = False
    bpy.ops.object.mode_set(mode='OBJECT') 
    for pBone in hidden_bones:
        bpy.data.objects[arm].data.bones[pBone].hide = False

    return



def remove_shapes(arm, bb_flags):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action = 'DESELECT')

    


    

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    arm = bpy.data.objects[arm].pose.bones
    for pBone in arm:
        if pBone.custom_shape is not None:
            cs = pBone.custom_shape
            if bb_flags['debug'] == 1:
                print("removing custom shape:", cs.name)
            pBone.custom_shape = None
            bpy.ops.object.delete()

            bpy.ops.object.select_all(action='DESELECT')

    bpy.ops.object.mode_set(mode='OBJECT')




def remove_constraints(arm):

    
    

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action = 'DESELECT')

    
    if bb_flags['remove_constraints_pbones'] == 1:
        if bb_flags['debug'] == 1:
            print("Removing constraints for pBones")
        for pBone in source_pbones:
            bpy.context.object.pose.bones[pBone].lock_location[0] = False 
            bpy.context.object.pose.bones[pBone].lock_location[1] = False
            bpy.context.object.pose.bones[pBone].lock_location[2] = False

            bpy.context.object.pose.bones[pBone].lock_rotation[0] = False 
            bpy.context.object.pose.bones[pBone].lock_rotation[1] = False
            bpy.context.object.pose.bones[pBone].lock_rotation[2] = False

            
            for pbC in bpy.context.object.pose.bones[pBone].constraints:
                bpy.context.object.pose.bones[pBone].constraints.remove(pbC)
    
    if bb_flags['remove_constraints_mbones'] == 1:
        if bb_flags['debug'] == 1:
            print("Removing constraints for mBones")
        for mBone in source_mbones:
            bpy.context.object.pose.bones[mBone].lock_location[0] = False 
            bpy.context.object.pose.bones[mBone].lock_location[1] = False
            bpy.context.object.pose.bones[mBone].lock_location[2] = False

            bpy.context.object.pose.bones[mBone].lock_rotation[0] = False 
            bpy.context.object.pose.bones[mBone].lock_rotation[1] = False
            bpy.context.object.pose.bones[mBone].lock_rotation[2] = False

            
            for pbC in bpy.context.object.pose.bones[mBone].constraints:
                bpy.context.object.pose.bones[mBone].constraints.remove(pbC)
    
    if bb_flags['remove_constraints_vbones'] == 1:
        if bb_flags['debug'] == 1:
            print("Removing constraints for vBones")
        for vBone in vBones:
            bpy.context.object.pose.bones[vBone].lock_location[0] = False 
            bpy.context.object.pose.bones[vBone].lock_location[1] = False
            bpy.context.object.pose.bones[vBone].lock_location[2] = False

            bpy.context.object.pose.bones[vBone].lock_rotation[0] = False 
            bpy.context.object.pose.bones[vBone].lock_rotation[1] = False
            bpy.context.object.pose.bones[vBone].lock_rotation[2] = False

            
            for pbC in bpy.context.object.pose.bones[vBone].constraints:
                bpy.context.object.pose.bones[vBone].constraints.remove(pbC)
    
    if bb_flags['remove_constraints_excluded'] == 1:
        if bb_flags['debug'] == 1:
            print("Removing constraints for excluded_bones")
        for eb in excluded_bones:
            bpy.context.object.pose.bones[eb].lock_location[0] = False 
            bpy.context.object.pose.bones[eb].lock_location[1] = False
            bpy.context.object.pose.bones[eb].lock_location[2] = False

            bpy.context.object.pose.bones[eb].lock_rotation[0] = False 
            bpy.context.object.pose.bones[eb].lock_rotation[1] = False
            bpy.context.object.pose.bones[eb].lock_rotation[2] = False

            
            for pbC in bpy.context.object.pose.bones[eb].constraints:
                bpy.context.object.pose.bones[eb].constraints.remove(pbC)
    
    
    
    if bb_flags['remove_constraints_problem'] == 1:
        if bb_flags['debug'] == 1:
            print("Removing constraints for problem_bones")
        for mBone in problem_bones:
            pb = mBone[1:] 
            bpy.context.object.pose.bones[pb].lock_location[0] = False 
            bpy.context.object.pose.bones[pb].lock_location[1] = False
            bpy.context.object.pose.bones[pb].lock_location[2] = False

            bpy.context.object.pose.bones[pb].lock_rotation[0] = False 
            bpy.context.object.pose.bones[pb].lock_rotation[1] = False
            bpy.context.object.pose.bones[pb].lock_rotation[2] = False

            
            for pbC in bpy.context.object.pose.bones[pb].constraints:
                bpy.context.object.pose.bones[pb].constraints.remove(pbC)
    
    
    
    
    if bb_flags['remove_constraints_ik'] == 1:
        if bb_flags['debug'] == 1:
            print("Removing constraints for ik bones")

        
        

        
        
        
        
        ik_bones = []
        for ikBone in bpy.context.object.pose.bones:
            if ikBone.name[:2] == "ik":
                ik_bones.append(ikBone.name)

        for ikName in ik_bones:

            
            bpy.ops.object.mode_set(mode='EDIT')

            
            

            
            
            bpy.data.objects[arm].data.edit_bones[ikName].hide_select = False

            bpy.ops.object.mode_set(mode='POSE')
            bpy.context.object.pose.bones[ikName].lock_location[0] = False 
            bpy.context.object.pose.bones[ikName].lock_location[1] = False
            bpy.context.object.pose.bones[ikName].lock_location[2] = False

            bpy.context.object.pose.bones[ikName].lock_rotation[0] = False 
            bpy.context.object.pose.bones[ikName].lock_rotation[1] = False
            bpy.context.object.pose.bones[ikName].lock_rotation[2] = False

            
            for ikC in bpy.context.object.pose.bones[ikName].constraints:
                bpy.context.object.pose.bones[ikName].constraints.remove(ikC)

    
    if bb_flags['remove_constraints_misc'] == 1:
        if bb_flags['debug'] == 1:
            print("Removing constraints for misc_bones")
        for mb in misc_bones:
            bpy.context.object.pose.bones[mb].lock_location[0] = False 
            bpy.context.object.pose.bones[mb].lock_location[1] = False
            bpy.context.object.pose.bones[mb].lock_location[2] = False

            bpy.context.object.pose.bones[mb].lock_rotation[0] = False 
            bpy.context.object.pose.bones[mb].lock_rotation[1] = False
            bpy.context.object.pose.bones[mb].lock_rotation[2] = False

            
            for pbC in bpy.context.object.pose.bones[mb].constraints:
                bpy.context.object.pose.bones[mb].constraints.remove(pbC)
    
    bpy.ops.object.mode_set(mode='OBJECT')
    return




def constrain_bones(arm):

    if bb_flags['debug'] == 1:
        print("Constraining any used source bones to the corresponding proxy rig bones")
        print("Constraint Parameters:")
        print("    constraint_child_of:        ", bb_flags['constraint_child_of'])
        print("    constraint_copy_location:   ", bb_flags['constraint_copy_location'])
        print("    constraint_copy_rotation:   ", bb_flags['constraint_copy_rotation'])
        print("    constraint_copy_scale:      ", bb_flags['constraint_copy_scale'])
        print("    constraint_copy_transforms: ", bb_flags['constraint_copy_transforms'])

    if bb_flags['apply_restpose_before_constraints'] == 1:
        print("Applying new rest pose before constraints.  Try doing it after if this fails and/or/with apply visual transform")
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[arm].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[arm]
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.armature_apply()
        bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action = 'DESELECT')

    
    
    for target_arm in source_used:
        if bb_flags['debug'] == 1:
            print("constrain to target_arm", target_arm)
        tBones = source_used[target_arm]
        for tBone in tBones:
            pBone = tBones[tBone]
            if bb_flags['debug'] == 1:
                print("     tBone/pBone:", tBone, pBone)
            obj = bpy.data.objects
            
            bone_const = bpy.data.objects[arm].pose.bones[pBone].constraints
            
            pbone_obj = bpy.data.objects[arm].pose.bones[pBone]

            
            
            target_arm_obj = bpy.data.objects[target_arm]

            if bb_flags['constraint_child_of'] == 1:
                if bb_flags['debug'] == 1:
                    print("Adding [Child Of] constraint for", target_arm, pBone, tBone)
                bone_const.new('CHILD_OF')
                bone_const['Child Of'].target = obj[target_arm]
                bone_const['Child Of'].subtarget = tBone
                bpy.context.object.pose.bones[pBone].constraints['Child Of'].name = "BB Child Of"

            
            if bb_flags['constraint_copy_location'] == 1:
                if bb_flags['debug'] == 1:
                    print("Adding [Copy Location] constraint for", target_arm, pBone, tBone)
                bone_const.new('COPY_LOCATION')
                bone_const['Copy Location'].target = obj[target_arm]
                bone_const['Copy Location'].subtarget = tBone
                bone_const['Copy Location'].target_space = 'WORLD'
                bone_const['Copy Location'].owner_space = 'WORLD'
                bpy.context.object.pose.bones[pBone].constraints['Copy Location'].name = "BB Copy Location"

            if bb_flags['constraint_copy_rotation'] == 1:
                if bb_flags['debug'] == 1:
                    print("Adding [Copy Rotation] constraint for", target_arm, pBone, tBone)
                bone_const.new('COPY_ROTATION')
                bone_const['Copy Rotation'].target = obj[target_arm]
                bone_const['Copy Rotation'].subtarget = tBone
                bone_const['Copy Rotation'].target_space = 'WORLD'
                bone_const['Copy Rotation'].owner_space = 'WORLD'
                bpy.context.object.pose.bones[pBone].constraints['Copy Rotation'].name = "BB Copy Rotation"

            if bb_flags['constraint_copy_scale'] == 1:
                if bb_flags['debug'] == 1:
                    print("Adding [Copy Scale] constraint for", target_arm, pBone, tBone)
                bone_const.new('COPY_SCALE')
                bone_const['Copy Scale'].target = obj[target_arm]
                bone_const['Copy Scale'].subtarget = tBone
                bone_const['Copy Scale'].target_space = 'WORLD'
                bone_const['Copy Scale'].owner_space = 'WORLD'
                bpy.context.object.pose.bones[pBone].constraints['Copy Scale'].name = "BB Copy Scale"

            if bb_flags['constraint_copy_transforms'] == 1:
                if bb_flags['debug'] == 1:
                    print("Adding [Copy Transforms] constraint for", target_arm, pBone, tBone)
                bone_const.new('COPY_TRANSFORMS')
                bone_const['Copy Transforms'].target = obj[target_arm]
                bone_const['Copy Transforms'].subtarget = tBone
                bone_const['Copy Transforms'].target_space = 'WORLD'
                bone_const['Copy Transforms'].owner_space = 'WORLD'
                bpy.context.object.pose.bones[pBone].constraints['Copy Transforms'].name = "BB Copy Transforms"

            bpy.ops.pose.select_all(action = 'DESELECT')

        
        

        
        if bb_flags['constraint_child_of'] == 1:
            if bb_flags['debug'] == 1:
                print("Setting inverse for [Child Of] constraint for", target_arm, pBone, tBone)
            ob = bpy.context.active_object
            for b in ob.pose.bones:
                for c in b.constraints: 
                    if c.type == "CHILD_OF":
                        context_py = bpy.context.copy()
                        context_py["constraint"] = c

                        ob.data.bones.active = b.bone
                        
                        
                        
                        
                        bpy.ops.constraint.childof_set_inverse(context_py, constraint="BB Child Of", owner='BONE')

    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    
    
    
    
    
    
    if bb_flags['apply_restpose_after_constraints'] == 1:
        print("Applying new rest pose after constraints.  My note above was right, but I should make flags for these.")
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[arm].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[arm]
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.armature_apply()
        bpy.ops.object.mode_set(mode='OBJECT')

    return



def disconnect(arm):
    
    
    
    

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]
    bpy.ops.object.mode_set(mode='EDIT')

    for dBone in bpy.data.objects[arm].data.edit_bones:
        bpy.data.objects[arm].data.edit_bones[dBone.name].use_connect = False

    bpy.ops.object.mode_set(mode='OBJECT')




def unlink_bones(arm):

    if bb_flags['unlink_all'] == 1:
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[arm].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[arm]
        bpy.ops.object.mode_set(mode='EDIT')
        print("Unlinking all bones")
        for bone in source_bones:
            try:
                bpy.data.objects[arm].data.edit_bones[bone].parent =  None
            except:
                print(" unlink all on", arm, "reports no parent for", bone)
        print("nothing else to unlink, returning")
        return

    if bb_flags['unlink_pbones'] == 1:
        unlink_child_bones(arm, source_pbones, source_links)
    if bb_flags['unlink_mbones'] == 1:
        unlink_child_bones(arm, source_mbones, source_links)
    
    if bb_flags['unlink_vbones'] == 1:
        unlink_child_bones(arm, vBones, source_links)
    if bb_flags['unlink_used_pbones'] == 1:
        unlink_child_bones(arm, target_pbones, source_links)
    if bb_flags['unlink_used_mbones'] == 1:
        unlink_child_bones(arm, target_mbones, source_links)
    if bb_flags['unlink_problem_bones'] == 1:
        unlink_child_bones(arm, problem_bones, source_links)
    if bb_flags['unlink_excluded_bones'] == 1:
        unlink_child_bones(arm, excluded_bones, source_links)

    
    if bb_flags['anchor_vbones'] == 1:
        set_mode(arm, "edit")
        for bone in vBones:
            bpy.data.objects[arm].data.edit_bones[bone].parent = bpy.data.objects[arm].data.edit_bones[vbone_anchor]

    return





def unlink_child_bones(arm, bone_list, source_link_data):

    if bb_flags['debug'] == 1:
        print("Entering unlink_child_bones")

    
    
    

    
    
    
    

    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]
    bpy.ops.object.mode_set(mode='EDIT')

    
    parent_keys = source_link_data.keys()

    
    for bone in bone_list:
        

        bpy.data.objects[arm].data.edit_bones[bone].parent =  None
        if bone in parent_keys:
            children = source_link_data[bone]
            for child in children:
                try:
                    bpy.data.objects[arm].data.edit_bones[child].parent =  None
                except:
                    print("bone missing", child)

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    return



def add_empties(bb_flags):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    
    if bb_flags['remove_empties'] == 1:
        
        empty_head = bpy.data.objects.new( "empty.head", None )
        bpy.context.scene.collection.objects.link( empty_head )
        empty_head.empty_display_size = 2
        empty_head.empty_display_type = 'PLAIN_AXES'
        empty_tail = bpy.data.objects.new( "empty.tail", None )
        bpy.context.scene.collection.objects.link( empty_tail )
        empty_tail.empty_display_size = 2
        empty_tail.empty_display_type = 'PLAIN_AXES'
        bpy.ops.object.select_all(action='DESELECT')
    else:
        try:
            empty_head = bpy.data.objects["empty.head"]
            empty_tail = bpy.data.objects["empty.tail"]
        except:
            print("remove_empties flag is cleared but no empties found, creating...")
            empty_head = bpy.data.objects.new( "empty.head", None )
            bpy.context.scene.collection.objects.link( empty_head )
            empty_head.empty_display_size = 2
            empty_head.empty_display_type = 'PLAIN_AXES'
            empty_tail = bpy.data.objects.new( "empty.tail", None )
            bpy.context.scene.collection.objects.link( empty_tail )
            empty_tail.empty_display_size = 2
            empty_tail.empty_display_type = 'PLAIN_AXES'
            bpy.ops.object.select_all(action='DESELECT')

    
    
    return empty_head, empty_tail



def remove_empties(bb_flags, empty_head, empty_tail):

    
    empty_head = g_var['empty_head']
    empty_tail = g_var['empty_tail']

    
    
    
    

    bpy.data.objects[empty_head].select_set(True)
    bpy.ops.object.delete()
    bpy.data.objects[empty_tail].select_set(True)
    bpy.ops.object.delete()

    return


def popup(message = "", title = "Message Box", icon =  'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
    return






def get_ebone_loc(arm, bone):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]

    bpy.ops.object.mode_set(mode='EDIT')

    e_head = bpy.data.objects[arm].data.edit_bones[bone].head
    e_tail = bpy.data.objects[arm].data.edit_bones[bone].tail
    e_roll = bpy.data.objects[arm].data.edit_bones[bone].roll

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    return (e_head, e_tail, e_roll)












def get_pbone_loc(arm, bone):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action = 'DESELECT')

    
    
    
    bpy.data.objects[arm].data.bones.active = bpy.data.objects[arm].pose.bones[bone].bone






    p_head = bpy.context.active_pose_bone.head
    p_tail = bpy.context.active_pose_bone.tail



    
    bpy.ops.pose.select_all(action = 'DESELECT')

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')


    return (p_head, p_tail)





def map_to_tbones(arm):

    
    empty_head = g_var['empty_head']
    empty_tail = g_var['empty_tail']

    if bb_flags['debug'] == 1:
        print("Entering map_to_tbones")
        print("Source rig is:", arm)
        print("target_skels:", target_skels)

    
    for target_arm in target_skels:
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[target_arm].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[target_arm]

        
        
        print("WARN: pose mode disabled")



        if bb_flags['debug'] == 1:
            print(" ======================================")
            print("target:", target_arm)

        
        tBones = target_bone[target_arm]
        for bone in tBones:
            pBone = source_used[target_arm][bone]
            mBone = target_pbones[pBone] 
            
            l_head = target_head[target_arm][bone]
            l_tail = target_tail[target_arm][bone]
            l_roll = target_roll[target_arm][bone]

            if bb_flags['debug'] == 1:
                print("  pBone:", pBone)
                print("  mBone:", mBone)
                print(" l_head:", l_head)
                print(" l_tail:", l_tail)
                print(" l_roll:", l_roll)
 
            
            
            
            if bb_flags['use_world_matrix'] == 0:
                
                
                target_world_mat_head = bpy.context.scene.objects[target_arm].matrix_world @ l_head
                target_world_mat_tail = bpy.context.scene.objects[target_arm].matrix_world @ l_tail
            else:
                target_world_mat_head = l_head
                target_world_mat_tail = l_tail

            
            
            

            bpy.data.objects[empty_head.name].location = target_world_mat_head
            bpy.data.objects[empty_tail.name].location = target_world_mat_tail

            bpy.data.objects[arm].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects[arm]
            bpy.ops.object.mode_set(mode='EDIT')

            
            
            
            if bb_flags['match_roll'] == 1:
                bpy.data.objects[arm].data.edit_bones[mBone].roll = l_roll
                bpy.data.objects[arm].data.edit_bones[pBone].roll = l_roll

            
            
            
            
            bpy.data.objects[arm].data.edit_bones[mBone].head = bpy.data.objects[empty_head.name].location
            bpy.data.objects[arm].data.edit_bones[mBone].tail = bpy.data.objects[empty_tail.name].location
            bpy.data.objects[arm].data.edit_bones[pBone].head = bpy.data.objects[empty_head.name].location
            bpy.data.objects[arm].data.edit_bones[pBone].tail = bpy.data.objects[empty_tail.name].location
            bpy.ops.object.mode_set(mode='OBJECT')
 
        if bb_flags['debug'] == 1:
            print(" ======================================")

    bpy.ops.object.mode_set(mode='OBJECT')
    return









def map_to_mbones(animation_arm):

    if bb_flags['debug'] == 1:
        print("Entering map_to_mbones")
        print("Source rig is:", animation_arm)
        print("target_skels:", target_skels)

    
    
    

    

    unmatched_bones = {}
    bones_failed = 0 
    for target_arm in qualified_armatures:
        unmatched_bones.setdefault(target_arm, [])
        tBones = qualified_armatures[target_arm]
        for bone in tBones:
            if bone not in all_mbones:
                bones_failed = 1
                unmatched_bones[target_arm].append(bone)
    if bones_failed == 1:
        print("Your armature is not name compatible with Second Life, try a different mapping.")
        print("The following bones did not match a proper mBone for Second Life")
        print("UB:", unmatched_bones)
        popup("Your target rig is not compatible with Second Life, try a different mapping.  See console for details.", "Error", "ERROR")
        return

    
    empty_head = g_var['empty_head']
    empty_tail = g_var['empty_tail']

    if bb_flags['debug'] == 1:
        print("Entering move_source_bones")
        print("Source rig is:", animation_arm)
        print("target_skels:", target_skels)

    
    
    
    
    
    
    mbone_to_pbone = {}
    for mBone, pBone in zip(all_mbones, all_pbones):
        mbone_to_pbone.update({mBone:pBone})

    
    
    

    
    
    
    for target_arm in qualified_armatures:
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[target_arm].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[target_arm]

        if bb_flags['debug'] == 1:
            print(" ======================================")
            print("target:", target_arm)

        
        tBones = qualified_armatures[target_arm]
        
        for mBone in tBones:
            pBone = mbone_to_pbone[mBone] 
            
            l_head = target_head[target_arm][mBone]
            l_tail = target_tail[target_arm][mBone]
            l_roll = target_roll[target_arm][mBone]

            if bb_flags['debug'] == 1:
                print("  pBone:", pBone)
                print("  mBone:", mBone)
                print(" l_head:", l_head)
                print(" l_tail:", l_tail)
                print(" l_roll:", l_roll)
 
            
            
            
            if bb_flags['use_world_matrix'] == 0:
                
                
                target_world_mat_head = bpy.context.scene.objects[target_arm].matrix_world @ l_head
                target_world_mat_tail = bpy.context.scene.objects[target_arm].matrix_world @ l_tail
            else:
                target_world_mat_head = l_head
                target_world_mat_tail = l_tail

            
            
            

            bpy.data.objects[empty_head.name].location = target_world_mat_head
            bpy.data.objects[empty_tail.name].location = target_world_mat_tail

            bpy.data.objects[animation_arm].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects[animation_arm]
            bpy.ops.object.mode_set(mode='EDIT')

            
            
            
            if bb_flags['match_roll'] == 1:
                bpy.data.objects[animation_arm].data.edit_bones[mBone].roll = l_roll
                bpy.data.objects[animation_arm].data.edit_bones[pBone].roll = l_roll

            
            
            bpy.data.objects[animation_arm].data.edit_bones[mBone].head = bpy.data.objects[empty_head.name].location
            bpy.data.objects[animation_arm].data.edit_bones[mBone].tail = bpy.data.objects[empty_tail.name].location
            bpy.data.objects[animation_arm].data.edit_bones[pBone].head = bpy.data.objects[empty_head.name].location
            bpy.data.objects[animation_arm].data.edit_bones[pBone].tail = bpy.data.objects[empty_tail.name].location
            bpy.ops.object.mode_set(mode='OBJECT')
 
        if bb_flags['debug'] == 1:
            print(" ======================================")

    bpy.ops.object.mode_set(mode='OBJECT')
    return



def map_to_template(animation_arm):

    if bb_flags['debug'] == 1:
        print("Entering map_to_template")
        print("Source rig is:", animation_arm)
        print("target_skels:", target_skels)

    
    
    
    

    
    

    
    template_list = {} 
    for arm in template_map:
        template_list.setdefault(arm, [])
        for bone in template_map[arm]:
            template_list[arm].append(template_map[arm][bone])
    
    
    
    missing = 0
    for arm in qualified_armatures:
        for bone in qualified_armatures[arm]:
            if bone not in template_list[arm]:
                missing = 1
                print("Missing scene bone [" + bone + "] on armature [" + arm + "]")
    for arm in template_list:
        for bone in template_list[arm]:
            if bone not in qualified_armatures[arm]:
                missing = 1
                print("Missing template bone [" + bone + "] found in scene armature [" + arm + "]")

    if missing == 1:
        print("The above list aught to be examined before you try again")
        popup("Bone mismatch between scene and template, see console for details.", "Missing bones", "ERROR")
        return

    
    empty_head = g_var['empty_head']
    empty_tail = g_var['empty_tail']

    
    
    
    
    
    
    
    
    mbone_to_pbone = {}
    for mBone, pBone in zip(all_mbones, all_pbones):
        mbone_to_pbone.update({mBone:pBone})
    
    

    
    

    
    

    
    
    
    global source_used
    source_used.clear()
    target_mbones.clear()
    target_pbones.clear()

    for tSkel in template_map:
        source_used.setdefault(tSkel, {})
        for mBone in template_map[tSkel]:
            
            
            tBone = template_map[tSkel][mBone]
            
            pBone = mbone_to_pbone[mBone]
            source_used[tSkel][tBone] = pBone
            target_mbones[mBone] = pBone
            target_pbones[pBone] = mBone

    
    

    
    for target_arm in target_skels:
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[target_arm].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[target_arm]

        if bb_flags['debug'] == 1:
            print(" ======================================")
            print("target:", target_arm)

        
        tBones = target_bone[target_arm]
        for bone in tBones:
            pBone = source_used[target_arm][bone]
            mBone = target_pbones[pBone] 
            
            l_head = target_head[target_arm][bone]
            l_tail = target_tail[target_arm][bone]
            l_roll = target_roll[target_arm][bone]

            if bb_flags['debug'] == 1:
                print("  pBone:", pBone)
                print("  mBone:", mBone)
                print(" l_head:", l_head)
                print(" l_tail:", l_tail)
                print(" l_roll:", l_roll)
 
            
            
            
            if bb_flags['use_world_matrix'] == 0:
                
                
                target_world_mat_head = bpy.context.scene.objects[target_arm].matrix_world @ l_head
                target_world_mat_tail = bpy.context.scene.objects[target_arm].matrix_world @ l_tail
            else:
                target_world_mat_head = l_head
                target_world_mat_tail = l_tail

            
            
            

            bpy.data.objects[empty_head.name].location = target_world_mat_head
            bpy.data.objects[empty_tail.name].location = target_world_mat_tail

            bpy.data.objects[animation_arm].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects[animation_arm]
            bpy.ops.object.mode_set(mode='EDIT')

            
            
            
            if bb_flags['match_roll'] == 1:
                bpy.data.objects[animation_arm].data.edit_bones[mBone].roll = l_roll
                bpy.data.objects[animation_arm].data.edit_bones[pBone].roll = l_roll

            
            
            
            
            bpy.data.objects[animation_arm].data.edit_bones[mBone].head = bpy.data.objects[empty_head.name].location
            bpy.data.objects[animation_arm].data.edit_bones[mBone].tail = bpy.data.objects[empty_tail.name].location
            bpy.data.objects[animation_arm].data.edit_bones[pBone].head = bpy.data.objects[empty_head.name].location
            bpy.data.objects[animation_arm].data.edit_bones[pBone].tail = bpy.data.objects[empty_tail.name].location
            bpy.ops.object.mode_set(mode='OBJECT')
 
        if bb_flags['debug'] == 1:
            print(" ======================================")

    bpy.ops.object.mode_set(mode='OBJECT')

    return True



def create_bone_group(armature="", group="", theme=""):
    arm = armature
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[arm].select_set(True)
    
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]
    bpy.ops.object.mode_set(mode='POSE')

    



    try:
        
        existing = bpy.context.object.pose.bone_groups[group]
        if bb_flags['debug'] == 1:
            print("Bone group already exists for", "[" + arm + "] " + "[" + group + "] " + "- skipping add function")
        return bpy.data.objects[arm].pose.bone_groups.active.name
    except:
        pass
    

    bpy.ops.pose.group_add()
    bpy.data.objects[arm].pose.bone_groups.active.name = group
    bpy.data.objects[arm].pose.bone_groups.active.color_set = theme

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    
    
    return bpy.data.objects[arm].pose.bone_groups.active.name



def add_bone_to_group(armature="", bone="", group=""):



    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[armature].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[armature]
    bpy.ops.object.mode_set(mode='POSE')



    bpy.data.objects[armature].pose.bones[bone].bone_group =        bpy.data.objects[armature].pose.bone_groups[group]




    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')




    return



def create_links(animation_arm):


    




    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[animation_arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[animation_arm]
    bpy.ops.object.mode_set(mode='EDIT')

    
    for target_arm in target_links:
        parent_dict = target_links[target_arm]
        for parent in parent_dict:
            src_p = source_used[target_arm][parent]
            
            children = parent_dict[parent]
            for child in children:
                
                src_c = source_used[target_arm][child]
                
                bpy.data.objects[animation_arm].data.edit_bones[src_c].parent =                    bpy.data.objects[animation_arm].data.edit_bones[src_p]
                
                if bb_flags['use_connect_state'] == 1:
                    bpy.data.objects[animation_arm].data.edit_bones[src_c].use_connect =                        connect_state[target_arm][child]



    return






def rename_to():

    

    
    for target_arm in qualified_armatures:
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[target_arm].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[target_arm]
        bpy.ops.object.mode_set(mode='POSE')

        


        for tBone in source_used[target_arm]:


            
            
            
            if bb_flags['rename_to_source'] == 1:
                bpy.data.objects[target_arm].pose.bones[tBone].name = source_used[target_arm][tBone]
            
            if bb_flags['rename_to_mbones'] == 1:
                pBone = source_used[target_arm][tBone]
                mBone = source_pbones[pBone] 
                bpy.data.objects[target_arm].pose.bones[tBone].name = mBone

    
    
    bpy.ops.object.mode_set(mode='OBJECT')

    return






def get_mode():
    if bpy.context.active_object == None:
        return None
    elif bpy.context.mode == 'EDIT_ARMATURE':
        return 'EDIT'
    else:
        return bpy.context.mode
    print("mod_functions::get_mode reports : should not have passed")
    return False



def set_mode(arm, mode):

    
    
    
        

    
    
    

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]
    if mode == "edit":
        bpy.ops.object.mode_set(mode='EDIT')
    if mode == "pose":
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action = 'DESELECT')
    if mode == "object":
        
        bpy.ops.object.mode_set(mode='OBJECT')
    return



def set_obj_mode(mode="", objects=[]):

    
    
    
    
    
    
    
    
    
    
    
        

    modes = ['POSE', 'EDIT', 'OBJECT']
    
    mode = mode.upper()
    if mode not in modes:
        print("set_obj_mode: error - incompatible mode", mode)
        return False

    

    obj = bpy.data.objects

    
    if len(objects) == 0:
        print("set_obj_mode: error - set_obj_mode expects a list of objects, none were given")
        return False

    
    for ob in objects:
        if ob not in obj:
            print("set_obj_mode: error - an object in the list passed to this function does not exist", ob)
            return False

    
    
    type = None
    last_type = None
    for ob in objects:
        if type == None:
            
            last_type = obj[ob].type
        type = obj[ob].type
        if type != last_type:
            print("set_obj_mode: error - this function can only process objects of the same type")
            return False
        last_type = type

    
    selected = bpy.context.selected_objects
    if len(selected) > 0:

        
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

    
    
    for ob in objects:
        obj[ob].select_set(True)
        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')

    
    
    
    for ob in objects:
        obj[ob].select_set(True)

    
    last_obj = objects[-1]
    activate(last_obj)

    bpy.ops.object.mode_set(mode=mode)

    return True 



def set_obj_mode_multi(mode="object", objects=[]):

    modes = ['POSE', 'EDIT', 'OBJECT']
    
    mode = mode.upper()
    if mode not in modes:
        print("set_obj_mode: error - incompatible mode", mode_settting)
        return False

    

    obj = bpy.data.objects

    
    if len(objects) == 0:
        print("set_obj_mode: error - set_obj_mode expects a list of objects, none were given")
        return False

    
    for ob in objects:
        if ob not in obj:
            print("set_obj_mode: error - an object in the list passed to this function does not exist", ob)
            return False

    
    
    type = None
    last_type = None
    for ob in objects:
        if type == None:
            
            last_type = obj[ob].type
        type = obj[ob].type
        if type != last_type:
            print("set_obj_mode: error - this function can only process objects of the same type")
            return False
        last_type = type

    
    selected = bpy.context.selected_objects
    if len(selected) > 0:

        
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

    
    
    for ob in objects:
        obj[ob].select_set(True)
        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')

    
    
    
    for ob in objects:
        obj[ob].select_set(True)

    
    last_obj = objects[-1]
    activate(last_obj)

    bpy.ops.object.mode_set(mode=mode)

    return True






def safe_select(object=""):
    if object == "":
        print("safe_select reports: nothing to do")
        return False
    obj = bpy.data.objects
    if object not in obj:
        print("safe_select reports: object not in scene -", object)
        return False

    
    
    if bpy.context.active_object == None:
        bpy.context.view_layer.objects.active = bpy.data.objects[object]

    if len(bpy.context.selected_objects) != 0:
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

    obj[object].select_set(True)
    bpy.ops.object.mode_set(mode='OBJECT')

    
    
    
    bpy.context.view_layer.objects.active = bpy.data.objects[object]

    return True





def remove_object(object=""):
    obj = bpy.data.objects

    if object == "":
        print("nothing to do")
        return False
    if object not in obj:
        print("object not in scene:", object)
        return False

    
    obj[object].hide_set(False)
    obj[object].hide_select = False
    if object in bpy.context.selected_objects:
        obj[object].select_set(False)

    state = save_state()

    if len(bpy.context.selected_objects) > 0:
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

    
    safe_select(object=object)
    bpy.ops.object.delete() 

    restore_state(state)

    return True




def set_select_enabled(select="enabled", armatures=[]):
    s = ["enabled", "disabled"]
    obj = bpy.data.objects
    ani = bpy.context.window_manager.bb_animesh

    for o in armatures:
        if obj[o].type != 'ARMATURE':
            print("set_select_enabled reports: non-armature objects have no bones")
            return False
    if select not in s:
        print("set_select_enabled reports: unknown setting", select)
        return False

    if select == "enabled":
        setting = False
    if select == "disabled":
        setting = True
    for arm in armatures:
        for boneObj in obj[arm].data.bones:
            boneObj.hide_select = setting
    
    if bpy.context.mode == 'POSE':
        bpy.ops.pose.select_all(action = 'DESELECT')

    return True






def select_map_mode(type=""):
    ccp = bpy.context.window_manager.cc_props
    obj = bpy.data.objects

    
    
    
    obj_list = list()
    obj_list.append(ccp.source_rig_name)
    obj_list.append(ccp.target_rig_name)

    print("select_map_mode reports: obj_list", obj_list)

    
    
    set_obj_mode(mode="object", objects=obj_list)
    bpy.ops.object.select_all(action='DESELECT')

    if type == "edit":
        for ob in obj_list:
            obj[ob].select_set(True)
            bpy.ops.object.mode_set(mode='OBJECT')
            for bone in obj[ob].pose.bones:
                obj[ob].data.bones[bone.name].hide_select = False
        bpy.ops.object.select_all(action='DESELECT')
    elif type == "map":
        rename = ccp['remap_stored']['rename'].to_dict()
        reskin = ccp['remap_stored']['reskin'].to_dict()



        for name in rename:
            
            rname = rename[name]
            
            if name in obj[ccp.source_rig_name].data.bones:
                obj[ccp.source_rig_name].data.bones[name].hide_select = True

            
            if rname in obj[ccp.target_rig_name].data.bones:
                obj[ccp.target_rig_name].data.bones[rname].hide_select = True

        for name in reskin:
            children = reskin[name]
            for child in children:
                obj[ccp.source_rig_name].data.bones[child].hide_select = True

    return True



def pretty_bones(arm):

    print("Applying groups to various bones")

    if bb_flags['debug'] == 1:
        print("Applying groups to used bones")

    
    for target_arm in target_skels:
        create_bone_group(target_arm, bento_buddy_group_name, bento_buddy_theme)

    
    animation_arm = arm 
    create_bone_group(animation_arm, pose_bones_group_name, pose_bone_theme)
    create_bone_group(animation_arm, mbones_group_name, mbone_theme)
    create_bone_group(animation_arm, excluded_bones_group_name, excluded_bone_theme)
    create_bone_group(animation_arm, problem_bones_group_name, problem_bone_theme)
    create_bone_group(animation_arm, misc_bones_group_name, misc_bone_theme)
    create_bone_group(animation_arm, unused_bones_group_name, unused_bone_theme)
    create_bone_group(animation_arm, vbones_group_name, vbone_theme)

    
    if bb_flags['debug'] == 1:
        print("Applying group to unusable bones")
    for eBone in excluded_bones:
        add_bone_to_group(animation_arm, eBone, excluded_bones_group_name)

    if bb_flags['debug'] == 1:
        print("Applying group to problem bones")
    for probBone in problem_bones:
        pBone = probBone[1:] 
        add_bone_to_group(animation_arm, pBone, problem_bones_group_name)

    if bb_flags['debug'] == 1:
        print("Applying group to misc bones")
    for mb in misc_bones:
        add_bone_to_group(animation_arm, mb, misc_bones_group_name)

    if bb_flags['debug'] == 1:
        print("Applying group to unused bones")

    
    for ub in unused_bones:
        add_bone_to_group(animation_arm, ub, unused_bones_group_name)

    if bb_flags['debug'] == 1:
        print("Applying group to volume bones")
    for vBone in vBones:
        add_bone_to_group(animation_arm, vBone, vbones_group_name)

    

    
    
    for pBone in target_pbones:

        slBone = target_pbones[pBone]
        add_bone_to_group(animation_arm, pBone, pose_bones_group_name)

        
        
        
        
        
        if slBone == pBone:
            add_bone_to_group(animation_arm, slBone, pose_bones_group_name)
        
        else:
            add_bone_to_group(animation_arm, slBone, mbones_group_name)

    

    
    
    for target_arm in target_skels:
        for tBone in source_used[target_arm]:
            add_bone_to_group(target_arm, tBone, bento_buddy_group_name)

    return






def pretty_places(arm):

    

    
    
    
    
    
    

    t_world_x,     t_world_y,     t_world_z     = bb_data['pretty_places_transform_world']
    t_spacing_x,   t_spacing_y,   t_spacing_z   = bb_data['pretty_places_transform_spacing']
    t_length_x,    t_length_y,    t_length_z    = bb_data['pretty_places_transform_length']
    t_separator_x, t_separator_y, t_separator_z = bb_data['pretty_places_transform_separator']

    t_offset_x,    t_offset_y,    t_offset_z    = bb_data['pretty_places_transform_offset']
    t_groups = bb_data['pretty_places_transform_groups']

    

    
    head_x, head_y, head_z = t_world_x + t_spacing_x, t_world_y + t_spacing_y, t_world_z + t_spacing_z
    
    tail_x, tail_y, tail_z = head_x + t_length_x, head_y + t_length_y, head_z + t_length_z

    animation_arm = arm 

    print("Putting bones from", animation_arm, "into bone bucket")
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[animation_arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[animation_arm]
    bpy.ops.object.mode_set(mode='EDIT')

    
    groups_count = 0
    
    head_local_x = 0
    head_local_y = 0
    head_local_z = 0
    tail_local_x = 0
    tail_local_y = 0
    tail_local_z = 0

    if bb_flags['pretty_places_set_pbones'] == 1:
        for pBone in unused_bones:
            mBone = unused_bones[pBone] 
            bpy.data.objects[animation_arm].data.edit_bones[pBone].head.x = head_x + head_local_x
            bpy.data.objects[animation_arm].data.edit_bones[pBone].head.y = head_y + head_local_y
            bpy.data.objects[animation_arm].data.edit_bones[pBone].head.z = head_z + head_local_z

            bpy.data.objects[animation_arm].data.edit_bones[pBone].tail.x = tail_x + tail_local_x
            bpy.data.objects[animation_arm].data.edit_bones[pBone].tail.y = tail_y + tail_local_y
            bpy.data.objects[animation_arm].data.edit_bones[pBone].tail.z = tail_z + tail_local_z
            
            bpy.data.objects[animation_arm].data.edit_bones[mBone].head.x = head_x + head_local_x
            bpy.data.objects[animation_arm].data.edit_bones[mBone].head.y = head_y + head_local_y
            bpy.data.objects[animation_arm].data.edit_bones[mBone].head.z = head_z + head_local_z

            bpy.data.objects[animation_arm].data.edit_bones[mBone].tail.x = tail_x + tail_local_x
            bpy.data.objects[animation_arm].data.edit_bones[mBone].tail.y = tail_y + tail_local_y
            bpy.data.objects[animation_arm].data.edit_bones[mBone].tail.z = tail_z + tail_local_z

            groups_count += 1
            
            if groups_count == t_groups:
                groups_count = 0
                head_x, head_y, head_z = head_x + t_offset_x, head_y + t_offset_y, head_z + t_offset_z
                tail_x, tail_y, tail_z = tail_x + t_offset_x, tail_y + t_offset_y, tail_z + t_offset_z
                head_local_x = 0
                head_local_y = 0
                head_local_z = 0
                tail_local_x = 0
                tail_local_y = 0
                tail_local_z = 0
            else:
                head_local_x, head_local_y, head_local_z = head_local_x + t_spacing_x, head_local_y + t_spacing_y, head_local_z + t_spacing_z
                tail_local_x, tail_local_y, tail_local_z = tail_local_x + t_spacing_x, tail_local_y + t_spacing_y, tail_local_z + t_spacing_z

        
        
        
        head_x, head_y, head_z = head_x + t_separator_x, head_y + t_separator_y, head_z + t_separator_z
        tail_x, tail_y, tail_z = head_x + t_separator_x, head_y + t_separator_y, head_z + t_separator_z

    if bb_flags['pretty_places_set_vbones'] == 1:
        pass



    if bb_flags['pretty_places_set_misc'] == 1:
        pass
    if bb_flags['pretty_places_set_problem'] == 1:
        pass
    if bb_flags['pretty_places_set_excluded'] == 1:
        pass

    bpy.ops.object.mode_set(mode='OBJECT')
    return









def link_animation(arm):

    
    
    
    
        
        
            
    
    

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='DESELECT')

    
    
    
    
    for tArm in source_used:
        for tBone in source_used[tArm]:
            pBone = source_used[tArm][tBone]
            bpy.data.objects[arm].pose.bones[pBone].keyframe_insert(data_path="location", frame=1)
            bpy.data.objects[arm].pose.bones[pBone].keyframe_insert(data_path="rotation_quaternion", frame=1)





    bpy.ops.object.mode_set(mode='OBJECT')
    return
























def create_default_reference_rig(bb_arm, add_control_rig=False):

    print("Create default ref rig")

    
    
    
    
    
    
    
    
    

    filename = script_dir + presets_path + "default_reference.py"
    default_reference = {}

    try:
        namespace = {}
        exec(open(filename, 'r', encoding='UTF8').read(), namespace)
        default_reference.update(namespace['default_reference'])
    except Exception as e:
        print(traceback.format_exc())

    
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

    
    arm_thing = bpy.data.armatures.new(bb_data['bb_arm'])
    armObj = bpy.data.objects.new(bb_data['bb_arm'], arm_thing)

    
    bpy.context.scene.collection.objects.link(armObj)
    bpy.context.view_layer.update()
    arm = armObj.name 
    armObj.location = (0.0, 0.0, 0.0)
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]
    bpy.ops.object.mode_set(mode='EDIT')

    
    for bone in default_reference:
        newbone = armObj.data.edit_bones.new(bone)
        newbone.head = default_reference[bone]['head_edit'] 
        newbone.tail = default_reference[bone]['tail_edit']
        
        
        newbone.matrix = mathutils.Matrix(default_reference[bone]['matrix_edit'])

        
        
        if add_control_rig == 1:
            
            cr_bone_name = cr_bones_map[bone]
            cr_bone = armObj.data.edit_bones.new(cr_bone_name)
            cr_bone.head = default_reference[bone]['head_edit'] 
            cr_bone.tail = default_reference[bone]['tail_edit']
            cr_bone.matrix = mathutils.Matrix(default_reference[bone]['matrix_edit'])
            bpy.data.objects[arm].data.edit_bones[cr_bone_name].use_deform = False

    
    bpy.ops.object.mode_set(mode='OBJECT')

    
    
    apply_sl_rotations(armature=arm)

    bpy.ops.object.mode_set(mode='EDIT')

    
    for bone in default_reference:
        connected = default_reference[bone]['connected']
        bpy.data.objects[arm].data.edit_bones[bone].use_connect = connected
        parent = default_reference[bone]['parent']
        if parent == "":
            continue
        bpy.data.objects[arm].data.edit_bones[bone].parent = bpy.data.objects[arm].data.edit_bones[parent]

        
        
        if add_control_rig == 1:
            cr_bone_name = cr_bones_map[bone]
            bpy.data.objects[arm].data.edit_bones[cr_bone_name].use_connect = connected
            if parent != "":
                
                cr_bone_parent = cr_bones_map[parent]
                bpy.data.objects[arm].data.edit_bones[cr_bone_name].parent = bpy.data.objects[arm].data.edit_bones[cr_bone_parent]

    bpy.ops.object.mode_set(mode='OBJECT')

    create_bone_group(arm, ref_mbones_group_name, ref_mbones_theme)
    create_bone_group(arm, ref_vbones_group_name, ref_vbones_theme)

    
    if add_control_rig == 1:

        create_bone_group(arm, cr_mbones_group_name, cr_mbones_theme)
        create_bone_group(arm, cr_vbones_group_name, cr_vbones_theme)

    for bone in default_reference:
        
        if default_reference[bone]['type'] == 'bone':
            add_bone_to_group(arm, bone, ref_mbones_group_name)
        else:
            add_bone_to_group(arm, bone, ref_vbones_group_name)

    
    
    if add_control_rig == 1:
        for mBone in cr_bones_map:
            cr_bone_name = cr_bones_map[mBone] 
            if default_reference[mBone]['type'] == 'bone':
                add_bone_to_group(arm, cr_bones_map[mBone], cr_mbones_group_name)
            else:
                add_bone_to_group(arm, cr_bones_map[mBone], cr_vbones_group_name)

                
                bpy.data.objects[arm].data.bones[cr_bone_name].layers[bb_vbones_layer] = True
                
                bpy.data.objects[arm].data.bones[cr_bone_name].layers[bb_base_layer] = False
                if bb_rig['vbones_selectable'] == 0:
                    
                    bpy.data.objects[arm].data.bones[cr_bone_name].hide_select = True

    
    
    if add_control_rig == 1:
        set_mode(arm, "pose")
        for bone in cr_bones_map:
            
            
            for con in bb_const["constraint_types"]:
                add_constraint(arm, bone, arm, cr_bones_map[bone], con, bb_const['constraint_influence'])

            
            bpy.data.objects[arm].data.bones[bone].layers[bb_mbones_layer] = True
            bpy.data.objects[arm].data.bones[bone].layers[bb_base_layer] = False

    bpy.ops.object.mode_set(mode='OBJECT')

    
    
    bpy.context.object.data.layers[bb_vbones_layer] = True

    armObj.select_set(True)
    bpy.context.view_layer.objects.active = armObj

    apply_sl_bone_roll(arm)

    return armObj




















def create_neutral_reference_rig(bb_arm, add_control_rig=False):

    print("Create neutral ref rig")

    
    
    
    
    
    
    
    
    




    
    

    filename = script_dir + presets_path + "neutral_reference.py"

    neutral_reference = {}

    try:
        namespace = {}
        exec(open(filename, 'r', encoding='UTF8').read(), namespace)
        neutral_reference.update(namespace['neutral_reference'])
    except Exception as e:
        print(traceback.format_exc())

    
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

    
    arm_thing = bpy.data.armatures.new(bb_data['bb_arm'])
    armObj = bpy.data.objects.new(bb_data['bb_arm'], arm_thing)

    
    bpy.context.scene.collection.objects.link(armObj)
    bpy.context.view_layer.update()
    arm = armObj.name 
    armObj.location = (0.0, 0.0, 0.0)
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]
    bpy.ops.object.mode_set(mode='EDIT')

    
    for bone in neutral_reference:
        newbone = armObj.data.edit_bones.new(bone)
        newbone.head = neutral_reference[bone]['head_edit'] 
        newbone.tail = neutral_reference[bone]['tail_edit']
        
        
        newbone.matrix = mathutils.Matrix(neutral_reference[bone]['matrix_edit'])

        
        
        if add_control_rig == 1:
            
            cr_bone_name = cr_bones_map[bone]
            cr_bone = armObj.data.edit_bones.new(cr_bone_name)
            cr_bone.head = neutral_reference[bone]['head_edit'] 
            cr_bone.tail = neutral_reference[bone]['tail_edit']
            cr_bone.matrix = mathutils.Matrix(neutral_reference[bone]['matrix_edit'])
            bpy.data.objects[arm].data.edit_bones[cr_bone_name].use_deform = False

    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT')

    
    for bone in neutral_reference:
        connected = neutral_reference[bone]['connected']
        bpy.data.objects[arm].data.edit_bones[bone].use_connect = connected
        parent = neutral_reference[bone]['parent']
        if parent == "":
            continue
        bpy.data.objects[arm].data.edit_bones[bone].parent = bpy.data.objects[arm].data.edit_bones[parent]

        
        
        if add_control_rig == 1:
            cr_bone_name = cr_bones_map[bone]
            bpy.data.objects[arm].data.edit_bones[cr_bone_name].use_connect = connected
            if parent != "":
                
                cr_bone_parent = cr_bones_map[parent]
                bpy.data.objects[arm].data.edit_bones[cr_bone_name].parent = bpy.data.objects[arm].data.edit_bones[cr_bone_parent]

    bpy.ops.object.mode_set(mode='OBJECT')

    create_bone_group(arm, ref_mbones_group_name, ref_mbones_theme)
    create_bone_group(arm, ref_vbones_group_name, ref_vbones_theme)

    
    if add_control_rig == 1:
        create_bone_group(arm, cr_mbones_group_name, cr_mbones_theme)
        create_bone_group(arm, cr_vbones_group_name, cr_vbones_theme)

    for bone in neutral_reference:
        
        if neutral_reference[bone]['type'] == 'bone':
            add_bone_to_group(arm, bone, ref_mbones_group_name)
        else:
            add_bone_to_group(arm, bone, ref_vbones_group_name)

    
    
    if add_control_rig == 1:
        for mBone in cr_bones_map:
            cr_bone_name = cr_bones_map[mBone] 
            if neutral_reference[mBone]['type'] == 'bone':
                add_bone_to_group(arm, cr_bones_map[mBone], cr_mbones_group_name)
            else:
                add_bone_to_group(arm, cr_bones_map[mBone], cr_vbones_group_name)

                
                
                bpy.data.objects[arm].data.bones[cr_bone_name].layers[bb_vbones_layer] = True
                
                bpy.data.objects[arm].data.bones[cr_bone_name].layers[bb_base_layer] = False
                if bb_rig['vbones_selectable'] == 0:
                    
                    bpy.data.objects[arm].data.bones[cr_bone_name].hide_select = True

    
    
    if add_control_rig == 1:
        for bone in cr_bones_map:
            
            
            for con in bb_const["constraint_types"]:
                add_constraint(arm, bone, arm, cr_bones_map[bone], con, bb_const['constraint_influence'])
            
            bpy.data.objects[arm].data.bones[bone].layers[bb_mbones_layer] = True
            bpy.data.objects[arm].data.bones[bone].layers[bb_base_layer] = False

    bpy.ops.object.mode_set(mode='OBJECT')

    
    
    
    apply_sl_bone_roll(arm)

    
    
    bpy.context.object.data.layers[bb_vbones_layer] = True
    armObj.select_set(True)
    bpy.context.view_layer.objects.active = armObj


    return armObj











def generate_human_ref():
    
    print("mod_functions::generate_human_ref reports : THIS FUNCTION IS USELESS, FIND OUT WHAT RAN IT")

    

    
    
    



    
    
    
    
    
    
    
    

    
    srcObj = bpy.context.active_object
    arm = srcObj.name
    set_mode(arm, "edit")

    
    
    from . import avatar_skeleton
    from .avatar_skeleton import avatar_skeleton

    
    human_reference = {}
    for bone in avatar_skeleton:

        
        
        
        
        
        
        
        matrix_pose = matrix_to_tuples(bpy.data.objects[arm].pose.bones[bone].matrix.copy())
        matrix_edit = matrix_to_tuples(bpy.data.objects[arm].data.edit_bones[bone].matrix.copy())
        head_edit = tuple_to_list(bpy.data.objects[arm].data.edit_bones[bone].head.copy())
        tail_edit = tuple_to_list(bpy.data.objects[arm].data.edit_bones[bone].tail.copy())
        roll_edit = bpy.data.objects[arm].data.edit_bones[bone].roll
        parent = avatar_skeleton[bone]['parent']
        use_connect = bpy.data.objects[arm].data.edit_bones[bone].use_connect
        bone_type = avatar_skeleton[bone]['type']

        
        
        human_reference[bone] = {
            "type": bone_type,
            "matrix_pose_edit": matrix_pose,
            "matrix_edit": matrix_edit,
            "head_edit": head_edit,
            "tail_edit": tail_edit,
            "roll_edit": roll_edit,
            "parent": parent,
            "connected": use_connect
            }
    
    set_mode(arm, "pose")
    for bone in all_mbones:
        matrix_pose = matrix_to_tuples(bpy.data.objects[arm].pose.bones[bone].matrix.copy())
        human_reference[bone].update({
            "matrix_pose": matrix_pose,
            })


    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    
    arm_thing = bpy.data.armatures.new(bb_data['bb_arm'])
    armObj = bpy.data.objects.new(bb_data['bb_arm'], arm_thing)

    
    bpy.context.scene.collection.objects.link(armObj)
    bpy.context.view_layer.update()
    arm = armObj.name 
    armObj.location = (0.0, 0.0, 0.0)
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]
    bpy.ops.object.mode_set(mode='EDIT')

    
    for bone in human_reference:
        newbone = armObj.data.edit_bones.new(bone)
        newbone.head = human_reference[bone]['head_edit'] 
        newbone.tail = human_reference[bone]['tail_edit']
        
        
        newbone.matrix = mathutils.Matrix(human_reference[bone]['matrix_edit'])

    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT')

    
    for bone in human_reference:
        connected = human_reference[bone]['connected']
        bpy.data.objects[arm].data.edit_bones[bone].use_connect = connected
        parent = human_reference[bone]['parent']
        if parent == "":
            continue
        bpy.data.objects[arm].data.edit_bones[bone].parent = bpy.data.objects[arm].data.edit_bones[parent]

    bpy.ops.object.mode_set(mode='OBJECT')


    
    
    if 1 == 0:
        from . import human_reference
        from .human_reference import human_reference
        
        bpy.ops.object.mode_set(mode='EDIT')
        tups = human_reference['mWristRight']['matrix_edit']
        bpy.data.objects[arm].data.edit_bones['mWristLeft'].use_connect = False
        bpy.data.objects[arm].data.edit_bones['mWristLeft'].parent = None
        bpy.data.objects[arm].data.edit_bones['mWristLeft'].matrix = mathutils.Matrix(tups)
        return



    
    import sys
    import os
    out_file = os.path.dirname(os.path.abspath(__file__))
    out_file += "/human_reference.py"
    f = open(out_file,"w", encoding='UTF8')
    f.write('neutral_reference = {}' + "\n")
    for bone in human_reference:
        
        t = human_reference[bone]['type']
        mpe = human_reference[bone]['matrix_pose_edit']
        mp  = human_reference[bone]['matrix_pose']
        me  = human_reference[bone]['matrix_edit']
        he  = human_reference[bone]['head_edit']
        te  = human_reference[bone]['tail_edit']
        re  = human_reference[bone]['roll_edit']
        p   = human_reference[bone]['parent']
        c   = human_reference[bone]['connected']
        f.write(
            'neutral_reference["' + bone + '"] = {' + "\n" +
            "   " + '"type": "' + t + '"' + ",\n" +
            "   " + '"matrix_pose_edit": ' + str(mpe) + ",\n" +
            "   " + '"matrix_pose": ' + str(mp) + ",\n" +
            "   " + '"matrix_edit": ' + str(me) + ",\n" +
            "   " + '"head_edit": ' + str(he) + ",\n" +
            "   " + '"tail_edit": ' + str(te) + ",\n" +
            "   " + '"roll_edit": ' + str(re) + ",\n" +
            "   " + '"parent": "' + str(p) + '"' + ",\n" +
            "   " + '"connected": ' + str(c) + "\n" +
            "}\n"
        )
    f.close()




    return armObj




    
    mat = human_reference['mWristRight']['matrix_edit']
    tups = matrix_to_tuples(mat)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.data.objects[arm].data.edit_bones['mWristLeft'].use_connect = False
    bpy.data.objects[arm].data.edit_bones['mWristLeft'].parent = None
    bpy.data.objects[arm].data.edit_bones['mWristLeft'].matrix = mathutils.Matrix(tups)

    bpy.ops.object.mode_set(mode='OBJECT')

    return armObj













def create_selected_reference_rig(arm, bb_arm, add_control_rig=False):

    print("create_selected_reference_rig - needs rotation values when Avastar is present")

    print("Create from Avastar reference")

    try:
        set_mode(arm, "edit")
    except:
        popup("Make sure the reference rig is visible, are you on the correct layer?", "Inaccessible Object", "ERROR")
        print("It would appear that the active object is not accessible")
        return None

    
    
    from . import avatar_skeleton
    from .avatar_skeleton import avatar_skeleton

    
    human_reference = {}
    for bone in avatar_skeleton:

        
        matrix_pose = matrix_to_tuples(bpy.data.objects[arm].pose.bones[bone].matrix.copy())
        matrix_edit = matrix_to_tuples(bpy.data.objects[arm].data.edit_bones[bone].matrix.copy())
        head_edit = tuple_to_list(bpy.data.objects[arm].data.edit_bones[bone].head.copy())
        tail_edit = tuple_to_list(bpy.data.objects[arm].data.edit_bones[bone].tail.copy())
        roll_edit = bpy.data.objects[arm].data.edit_bones[bone].roll
        parent = avatar_skeleton[bone]['parent']
        use_connect = bpy.data.objects[arm].data.edit_bones[bone].use_connect
        bone_type = avatar_skeleton[bone]['type']

        
        human_reference[bone] = {
            "type": bone_type,
            "matrix_pose_edit": matrix_pose,
            "matrix_edit": matrix_edit,
            "head_edit": head_edit,
            "tail_edit": tail_edit,
            "roll_edit": roll_edit,
            "parent": parent,
            "connected": use_connect
            }

    set_mode(arm, "pose")

    arm_matrix_world = bpy.data.objects[arm].matrix_world

    for bone in all_mbones:

        location = bpy.data.objects[arm].pose.bones[bone].location.copy()
        matrix = bpy.data.objects[arm].pose.bones[bone].matrix.copy()
        human_reference[bone].update({
            "matrix": matrix,
            "location": location
            })

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    
    arm_thing = bpy.data.armatures.new(bb_arm)
    armObj = bpy.data.objects.new(bb_arm, arm_thing)

    
    bpy.context.scene.collection.objects.link(armObj)
    bpy.context.view_layer.update()
    
    arm = armObj.name 
    armObj.location = (0.0, 0.0, 0.0)
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]
    bpy.ops.object.mode_set(mode='EDIT')

    
    

    for bone in human_reference:
        newbone = armObj.data.edit_bones.new(bone)
        newbone.head = human_reference[bone]['head_edit'] 
        newbone.tail = human_reference[bone]['tail_edit']
        
        
        newbone.matrix = mathutils.Matrix(human_reference[bone]['matrix_edit'])
        
        
        if add_control_rig == 1:
            
            cr_bone_name = cr_bones_map[bone]
            cr_bone = armObj.data.edit_bones.new(cr_bone_name)
            cr_bone.head = human_reference[bone]['head_edit'] 
            cr_bone.tail = human_reference[bone]['tail_edit']
            cr_bone.matrix = mathutils.Matrix(human_reference[bone]['matrix_edit'])
            bpy.data.objects[arm].data.edit_bones[cr_bone_name].use_deform = False

    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT')

    control_bones = {}
    
    for bone in human_reference:
        connected = human_reference[bone]['connected']
        bpy.data.objects[arm].data.edit_bones[bone].use_connect = connected
        parent = human_reference[bone]['parent']
        if parent == "":
            continue
        bpy.data.objects[arm].data.edit_bones[bone].parent = bpy.data.objects[arm].data.edit_bones[parent]

        
        
        if add_control_rig == 1:
            cr_bone_name = cr_bones_map[bone]
            bpy.data.objects[arm].data.edit_bones[cr_bone_name].use_connect = connected
            if parent != "":
                
                cr_bone_parent = cr_bones_map[parent]
                bpy.data.objects[arm].data.edit_bones[cr_bone_name].parent = bpy.data.objects[arm].data.edit_bones[cr_bone_parent]
 
    bpy.ops.object.mode_set(mode='OBJECT')

    
    create_bone_group(arm, ref_mbones_group_name, ref_mbones_theme)
    create_bone_group(arm, ref_vbones_group_name, ref_vbones_theme)

    
    if add_control_rig == 1:
        create_bone_group(arm, cr_mbones_group_name, cr_mbones_theme)
        create_bone_group(arm, cr_vbones_group_name, cr_vbones_theme)

    

    for bone in human_reference:
        
        if avatar_skeleton[bone]['type'] == 'bone':
            add_bone_to_group(arm, bone, ref_mbones_group_name)
        else:
            add_bone_to_group(arm, bone, ref_vbones_group_name)
            bpy.data.objects[arm].data.bones[bone].layers[bb_vbones_layer] = True
            
            bpy.data.objects[arm].data.bones[cr_bone_name].layers[bb_base_layer] = False

    
    
    if add_control_rig == 1:
        for mBone in cr_bones_map:
            cr_bone_name = cr_bones_map[mBone] 
            if avatar_skeleton[mBone]['type'] == 'bone':
                add_bone_to_group(arm, cr_bones_map[mBone], cr_mbones_group_name)
            else:
                add_bone_to_group(arm, cr_bones_map[mBone], cr_vbones_group_name)

                
                
                bpy.data.objects[arm].data.bones[cr_bone_name].layers[bb_vbones_layer] = True
                
                bpy.data.objects[arm].data.bones[cr_bone_name].layers[bb_base_layer] = False
                if bb_rig['vbones_selectable'] == 0:
                    
                    bpy.data.objects[arm].data.bones[cr_bone_name].hide_select = True

    bpy.ops.object.mode_set(mode='POSE')

    for bone in all_mbones:
        bpy.data.objects[arm].pose.bones[bone].matrix = human_reference[bone]['matrix']
        
        if add_control_rig == 1:
            cr_bone_name = cr_bones_map[bone]
            bpy.data.objects[arm].pose.bones[cr_bone_name].matrix = human_reference[bone]['matrix']

        bpy.context.view_layer.update()

    
    
    if add_control_rig == 1:
        for bone in cr_bones_map:
            
            
            for con in bb_const["constraint_types"]:
                add_constraint(arm, bone, arm, cr_bones_map[bone], con, bb_const['constraint_influence'])
            
            bpy.data.objects[arm].data.bones[bone].layers[bb_mbones_layer] = True
            bpy.data.objects[arm].data.bones[bone].layers[bb_base_layer] = False

    
    
    bpy.context.object.data.layers[bb_vbones_layer] = True

    
    
    
    apply_sl_bone_roll(arm)

    return armObj







def map_from_bentobuddy(arm, template, add_control_rig=False):

    print("map from bb running")

    
    
    
    
    set_mode(arm, "object")
    bpy.ops.object.transform_apply(scale=True, rotation=True, location=True)

    
    

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    empty_head = bpy.data.objects.new( "empty.head", None )
    bpy.context.scene.collection.objects.link( empty_head )

    empty_head.empty_display_size = 2
    empty_head.empty_display_type = 'PLAIN_AXES'
    empty_tail = bpy.data.objects.new( "empty.tail", None )
    bpy.context.scene.collection.objects.link( empty_tail )
    empty_tail.empty_display_size = 2
    empty_tail.empty_display_type = 'PLAIN_AXES'
    bpy.ops.object.select_all(action='DESELECT')


    
    
    
    

    
    
    
    

    target_data = {}
    for skel in template:
        set_mode(skel, "edit")

        target_data[skel] = {}
        target_data[skel]["matrix_world"] = bpy.data.objects[skel].matrix_world.copy()
        target_data[skel]["location"] = bpy.data.objects[skel].location.copy()
        target_data[skel]["bones"] = {}
        for boneObj in bpy.data.objects[skel].data.edit_bones:
            
            bone = boneObj.name
            parentObj = bpy.data.objects[skel].data.edit_bones[bone].parent
            if parentObj is not None:
                parent = parentObj.name
            else:
                parent = None

            matrix_tuples = matrix_to_tuples(bpy.data.objects[skel].data.edit_bones[bone].matrix.copy())
            matrix = bpy.data.objects[skel].data.edit_bones[bone].matrix.copy()
            connected = bpy.data.objects[skel].data.edit_bones[bone].use_connect
            head = bpy.data.objects[skel].data.edit_bones[bone].head.copy()
            tail = bpy.data.objects[skel].data.edit_bones[bone].tail.copy()
            roll = bpy.data.objects[skel].data.edit_bones[bone].roll
            head_list = tuple_to_list(bpy.data.objects[skel].data.edit_bones[bone].head.copy())
            tail_list = tuple_to_list(bpy.data.objects[skel].data.edit_bones[bone].tail.copy())
            matrix_tup = matrix_to_tuples(bpy.data.objects[skel].data.edit_bones[bone].matrix.copy())

            target_data[skel]['bones'][bone] = {
                "matrix_tup": matrix_tup,
                "matrix": matrix,
                "matrix_tuples": matrix_tuples,
                "connected": connected,
                "parent":       parent,
                "head": head,
                "tail": tail,
                "roll": roll,
                "head_list": head_list,
                "tail_list": tail_list,
            }
        
        bpy.ops.object.mode_set(mode='OBJECT')

    
    set_mode(arm, "pose")
    for skel in template:
        for boneObj in bpy.data.objects[skel].pose.bones:
            bone = boneObj.name
            rm = boneObj.rotation_mode
            boneObj.rotation_mode = 'XYZ'
            target_data[skel]['bones'][bone].update({
                "rotation": bpy.data.objects[skel].pose.bones[bone].rotation_euler.copy(),
                "translation": bpy.data.objects[skel].pose.bones[bone].matrix.translation.copy(),
                "location": bpy.data.objects[skel].pose.bones[bone].location.copy(),
                "matrix_basis": bpy.data.objects[skel].pose.bones[bone].matrix_basis.copy(),
                "matrix_pose": bpy.data.objects[skel].pose.bones[bone].matrix.copy(),
                "matrix_channel": bpy.data.objects[skel].pose.bones[bone].matrix_channel.copy(),
            })
            boneObj.rotation_mode = rm
        

    
    
    set_mode(arm, "edit")

    
    
    for boneObj in bpy.data.objects[arm].data.edit_bones:
        boneObj.use_connect = False
        boneObj.use_local_location = False
        boneObj.use_inherit_rotation = False
        boneObj.use_inherit_scale = False
    bpy.context.view_layer.update()

    
    
    used_bones = {}

    
    
    has_control_rig = 0

    
    if bpy.data.objects[arm].get('bentobuddy_control_rig') is not None:
        
        
        if bpy.data.objects[arm].get('bentobuddy_control_rig') == 1:
            has_control_rig = 1
            print(arm, "has a control rig")
            print("removing parent from control rig on", arm)
            for bone in cr_bones_map:
                cr_bone = cr_bones_map[bone]
                bpy.data.objects[arm].data.edit_bones[cr_bone].parent = None
        elif bpy.data.objects[arm].get('bentobuddy_control_rig') == 0:
            print(arm, "has no control rig")
            
            has_control_rig = 0

    
    
    
    
    for skel in template:
        used_bones[skel] = {}
        target_matrix = target_data[skel]['matrix_world']
        
        

        for bone in template[skel]:
            target_bone = template[skel][bone]

            
            if bb_flags['target_non_deformable'] == 1:
                used_bones[skel][bone] = target_bone

            
            else:
                if bpy.data.objects[skel].data.bones[target_bone].use_deform == True:
                    used_bones[skel][bone] = target_bone
                else:
                    continue

            
            final_matrix_head = target_matrix @ target_data[skel]['bones'][target_bone]['head']
            final_matrix_tail = target_matrix @ target_data[skel]['bones'][target_bone]['tail']




            bpy.data.objects[empty_head.name].location = final_matrix_head
            bpy.data.objects[empty_tail.name].location = final_matrix_tail

            if has_control_rig == 1:
                cr_bone = cr_bones_map[bone]
                bpy.data.objects[arm].data.edit_bones[cr_bone].head = bpy.data.objects[empty_head.name].location
                bpy.data.objects[arm].data.edit_bones[cr_bone].tail = bpy.data.objects[empty_tail.name].location

            
            
            
            
                
                
            bpy.data.objects[arm].data.edit_bones[bone].head = bpy.data.objects[empty_head.name].location
            bpy.data.objects[arm].data.edit_bones[bone].tail = bpy.data.objects[empty_tail.name].location

            bpy.context.view_layer.update()

            
            
            

            
                
                
                





            
            
            
            
            
            


    
    
    set_mode(arm, "object")
    bpy.ops.object.transform_apply(scale=True, rotation=True, location=True)
    bpy.ops.object.mode_set(mode='POSE')
    bpy.data.objects[arm].data.display_type = 'STICK'
    bpy.data.objects[arm].show_in_front = True

    
    
    
    
    
    
    

    
    
    
    
    
    

    if bb_flags['constrain_bones'] == 1:
        for skel in used_bones:
            for bone in used_bones[skel]:
                source_bone = bone 
                
                
                if has_control_rig == 1:
                    source_bone = cr_bones_map[bone]
                target_bone = used_bones[skel][bone]
                if bb_flags['constraint_copy_transforms'] == 1:
                    add_constraint(arm, source_bone, skel, target_bone, 'COPY_TRANSFORMS', bb_const['constraint_influence'])
                if bb_flags['constraint_copy_location'] == 1:
                    add_constraint(arm, source_bone, skel, target_bone, 'COPY_LOCATION', bb_const['constraint_influence'])
                if bb_flags['constraint_copy_rotation'] == 1:
                    add_constraint(arm, source_bone, skel, target_bone, 'COPY_ROTATION', bb_const['constraint_influence'])
                if bb_flags['constraint_copy_scale'] == 1:
                    add_constraint(arm, source_bone, skel, target_bone, 'COPY_SCALE', bb_const['constraint_influence'])
                if bb_flags['constraint_child_of'] == 1:
                    add_constraint(arm, source_bone, skel, target_bone, 'CHILD_OF', bb_const['constraint_influence'])

        
        
        
            

    
    

    if bb_flags['create_links'] == 1:
        if has_control_rig == 1:
            
            template_rev = {}
            for skel in template:
                template_rev[skel] = {}
                for mbone in template[skel]:
                    tbone = template[skel][mbone]
                    template_rev[skel][tbone] = mbone

            
            
            set_mode(arm, "edit")
            for skel in template:
                for mbone in template[skel]:
                    tbone = template[skel][mbone]

                    if bpy.data.objects[skel].data.bones[tbone].parent is not None:
                        
                        target_parent = bpy.data.objects[skel].data.bones[tbone].parent.name

                        source_parent = template_rev[skel][target_parent]

                        cr_bone = cr_bones_map[mbone]
                        cr_bone_parent = cr_bones_map[source_parent]
                        bpy.data.objects[arm].data.edit_bones[cr_bone].parent =                            bpy.data.objects[arm].data.edit_bones[cr_bone_parent]


    
    
    set_mode(arm, "pose")
    bpy.ops.pose.armature_apply()
    set_mode(arm, "object")

    
    
    if bb_flags['rename_to'] == 1:
        print("entering rename bones")
        uhash = {}
        for skel in used_bones:
            uhash[skel] = {}
            
            
            for mbone in used_bones[skel]:
                ubone = get_unique_name_short()
                tbone = used_bones[skel][mbone]
                uhash[skel][ubone] = mbone
                bpy.data.objects[skel].data.bones[tbone].name = ubone
        for skel in uhash:
            for ubone in uhash[skel]:
                mbone = uhash[skel][ubone]
                bpy.data.objects[skel].data.bones[ubone].name = mbone

    if bb_flags['disable_relationship_lines'] == 1:
        
            
                
        bpy.context.space_data.overlay.show_relationship_lines = False

    
    
    
    
    
    if bb_flags['change_inherit'] == 1:

        
        

        set_mode(arm, "edit")
        for boneObj in bpy.data.objects[arm].data.edit_bones:
            boneObj.use_local_location = bb_flags['inherit_rotation']
            boneObj.use_inherit_rotation = bb_flags['inherit_location']
            boneObj.use_inherit_scale = bb_flags['inherit_scale']
            boneObj.use_connect = False

    bpy.ops.object.mode_set(mode='OBJECT')

    
    
    
    
    
    
        

        
        

        
            
            

    
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[empty_head.name].select_set(True)
    bpy.data.objects[empty_tail.name].select_set(True)
    bpy.ops.object.delete()

    
    bpy.ops.object.select_all(action='DESELECT')
    for skel in target_data:
        bpy.data.objects[skel].select_set(True)

    return







def map_from_unknown(arm, target_arms, template):

    target_data = {}
    for skel in target_arms:
        set_mode(skel, "edit")

        target_data[skel] = {}
        target_data[skel]["matrix_world"] = bpy.data.objects[skel].matrix_world.copy()
        target_data[skel]["location"] = bpy.data.objects[skel].location
        target_data[skel]["bones"] = {}
        for boneObj in bpy.data.objects[skel].data.edit_bones:
            
            bone = boneObj.name
            parentObj = bpy.data.objects[skel].data.edit_bones[bone].parent
            if parentObj is not None:
                parent = parentObj.name
            else:
                parent = None

            matrix_tuples = matrix_to_tuples(bpy.data.objects[skel].data.edit_bones[bone].matrix.copy())
            matrix = bpy.data.objects[skel].data.edit_bones[bone].matrix.copy()
            connected = bpy.data.objects[skel].data.edit_bones[bone].use_connect
            head = bpy.data.objects[skel].data.edit_bones[bone].head.copy()
            tail = bpy.data.objects[skel].data.edit_bones[bone].tail.copy()
            roll = bpy.data.objects[skel].data.edit_bones[bone].roll
            head_list = tuple_to_list(bpy.data.objects[skel].data.edit_bones[bone].head.copy())
            tail_list = tuple_to_list(bpy.data.objects[skel].data.edit_bones[bone].tail.copy())
            matrix_tup = matrix_to_tuples(bpy.data.objects[skel].data.edit_bones[bone].matrix.copy())

            target_data[skel]['bones'][bone] = {
                "matrix_tup": matrix_tup,
                "matrix": matrix,
                "matrix_tuples": matrix_tuples,
                "connected": connected,
                "parent":       parent,
                "head": head,
                "tail": tail,
                "roll": roll,
                "head_list": head_list,
                "tail_list": tail_list,
            }
        
        bpy.ops.object.mode_set(mode='OBJECT')

    
    set_mode(arm, "pose")
    for skel in target_arms:
        for boneObj in bpy.data.objects[skel].pose.bones:
            bone = boneObj.name
            rm = boneObj.rotation_mode
            boneObj.rotation_mode = 'XYZ'
            target_data[skel]['bones'][bone].update({
                "rotation": bpy.data.objects[skel].pose.bones[bone].rotation_euler.copy(),
                "translation": bpy.data.objects[skel].pose.bones[bone].matrix.translation.copy(),
                "location": bpy.data.objects[skel].pose.bones[bone].location.copy(),
                "matrix_basis": bpy.data.objects[skel].pose.bones[bone].matrix_basis.copy(),
                "matrix_pose": bpy.data.objects[skel].pose.bones[bone].matrix.copy(),
                "matrix_channel": bpy.data.objects[skel].pose.bones[bone].matrix_channel.copy(),
            })
            boneObj.rotation_mode = rm
        

    
    set_mode(arm, "edit")

    
    
    for boneObj in bpy.data.objects[arm].data.edit_bones:
        boneObj.use_connect = False
    bpy.context.view_layer.update()

    
    
    
    used_bones = {}
    for skel in template:
        used_bones[skel] = {}
        target_matrix = target_data[skel]['matrix_world']
        for bone in template[skel]:
            target_bone = template[skel][bone]
            
            if bb_flags['target_non_deformable'] == 1:
                used_bones[skel][bone] = target_bone
            
            else:
                if bpy.data.objects[skel].data.bones[target_bone].use_deform == True:
                    used_bones[skel][bone] = target_bone

            bpy.data.objects[arm].data.edit_bones[bone].head = target_data[skel]['bones'][target_bone]['head']
            bpy.data.objects[arm].data.edit_bones[bone].tail = target_data[skel]['bones'][target_bone]['tail']
            bpy.data.objects[arm].data.edit_bones[bone].matrix = target_data[skel]['bones'][target_bone]['matrix']


    set_mode(arm, "object")
    
    bpy.ops.object.transform_apply(scale=True, rotation=True, location=True)

    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.armature_apply()

    
    bpy.data.objects[arm].data.display_type = 'STICK'
    bpy.data.objects[arm].show_in_front = True
    

    for skel in used_bones:
        for bone in used_bones[skel]:
            target_bone = used_bones[skel][bone]
            bpy.data.objects[arm].data.bones.active = bpy.data.objects[arm].data.bones[bone]

            

            bc = bpy.data.objects[arm].pose.bones[bone].constraints

                
            if 1 == 1:
                
                
                bc.new('COPY_TRANSFORMS')
                
                bc['Copy Transforms'].target = bpy.data.objects[skel]
                bc['Copy Transforms'].subtarget = target_bone
                bc['Copy Transforms'].target_space = 'POSE'
                bc['Copy Transforms'].owner_space = 'WORLD'
                bc['Copy Transforms'].influence = 0.999
                bc['Copy Transforms'].name = "Temp Copy TRS"

                bpy.ops.pose.select_all(action = 'DESELECT')

                
            elif 1 == 0:
                
                
                print("----- separate constraints -----")
                bc.new('COPY_LOCATION')
                bc['Copy Location'].target = bpy.data.objects[skel]
                bc['Copy Location'].subtarget = target_bone
                bc['Copy Location'].target_space = 'WORLD'
                bc['Copy Location'].owner_space = 'WORLD'
                bc['Copy Location'].influence = 0.999
                bc['Copy Location'].name = "Temp Copy Loc"

                bc.new('COPY_ROTATION')
                bc['Copy Rotation'].target = bpy.data.objects[skel]
                bc['Copy Rotation'].subtarget = target_bone
                bc['Copy Rotation'].target_space = 'WORLD'
                bc['Copy Rotation'].owner_space = 'WORLD'
                bc['Copy Rotation'].influence = 0.999
                bc['Copy Rotation'].name = "Temp Copy Rot"

                bpy.ops.pose.select_all(action = 'DESELECT')
                
            else:
                
                print("----- bpy.ops transform constraint -----")
                pb = bpy.context.active_pose_bone
                nc = pb.constraints.new(type='COPY_ROTATION')
                nc.target = bpy.data.objects[skel]
                nc.subtarget = target_bone
                nc.influence = 0.999
                


    bpy.ops.pose.select_all(action = 'SELECT')

    
    
    bpy.ops.pose.select_all(action = 'DESELECT')

    if bb_flags['change_inherit'] == 1:
        for boneObj in bpy.data.objects[arm].data.edit_bones:
            boneObj.use_local_location = False
            boneObj.use_inherit_rotation = False
            boneObj.use_inherit_scale = False

    set_mode(arm, "object")

    
    
    if bb_flags['rename_to'] == 1:
        print("unknown: entering rename bones")
        for bone in used_bones:
            print("unknown: TAGGED in rename cycle, not finished:", bone, used_bones[bone])

    return



def create_reference_pose(arm):

    armObj = bpy.context.active_object

    
    if bpy.data.objects[armObj.name].get('bb_fixed_rig') == 1:
        print("Rig animation fix already processed for", armObj.name)
        return

    print("Set animation fix flag on", armObj.name)
    bpy.data.objects[armObj.name]["bb_fixed_rig"] = 1

    
    start_frame, end_frame = bpy.data.objects[armObj.name].animation_data.action.frame_range
    print("start_frame", str(start_frame))

    move_to = 2 - start_frame

    bpy.ops.object.mode_set(mode='POSE')

    
    anim = armObj.animation_data
    if anim is not None and anim.action is not None:
        for fcurve in anim.action.fcurves:
            for point in fcurve.keyframe_points:
                
                
                
                point.co.x += move_to

    
    
    for pbone in bpy.context.active_object.pose.bones:
        pbone.bone.select = True

    
    
    
    
    
    bpy.ops.pose.transforms_clear()

    
    

    for pbone in bpy.context.active_object.pose.bones:
        
        
        pbone.keyframe_insert(data_path="location", frame=1)
        
        
        pbone.keyframe_insert(data_path="rotation_quaternion", frame=1)

    return



def show_states():
    
    print("active mode:", bpy.context.active_object.mode)
    print("active object:", bpy.context.active_object)
    return



def reset_flags():
    
    print(bb_flags)

    pkl_file = open(reset_path, 'rb')
    bb_flags = pickle.load(pkl_file)
    pkl_file.close()
    for flag in bb_flags:
        bpy.context.scene[pre_flag + flag] = bb_flags[flag]
    return






def matrix_to_tuples(mat):
    l_mat = list()
    l = list()
    for f in mat:
        l.clear()
        for v in f:
            l.append(v)
        l_mat.append(tuple(l))
    return l_mat




def tuple_to_list(t):
    l = list()
    for f in t:
        l.append(f)
    return l





def add_trs_constraint(arm, bone, target_arm, target_bone):
    




    bpy.data.objects[arm].data.bones.active = bpy.data.objects[arm].data.bones[bone]
    bc = bpy.data.objects[arm].pose.bones[bone].constraints
    bc.new('COPY_LOCATION')
    bc['Copy Location'].target = bpy.data.objects[target_arm]
    bc['Copy Location'].subtarget = target_bone
    bc['Copy Location'].target_space = 'WORLD'
    bc['Copy Location'].owner_space = 'WORLD'
    bc['Copy Location'].influence = 1
    bc['Copy Location'].name = "BB Copy Loc"
    bc.new('COPY_ROTATION')
    bc['Copy Rotation'].target = bpy.data.objects[target_arm]
    bc['Copy Rotation'].subtarget = target_bone
    bc['Copy Rotation'].target_space = 'WORLD'
    bc['Copy Rotation'].owner_space = 'WORLD'
    bc['Copy Rotation'].influence = 1
    bc['Copy Rotation'].name = "BB Copy Rot"
    bc.new('COPY_SCALE')
    bc['Copy Scale'].target = bpy.data.objects[target_arm]
    bc['Copy Scale'].subtarget = target_bone
    bc['Copy Scale'].target_space = 'WORLD'
    bc['Copy Scale'].owner_space = 'WORLD'
    bc['Copy Scale'].influence = 1
    bc['Copy Scale'].name = "BB Copy Scale"
    return















def add_constraint(
    source="", sbone="", target="", tbone="",
    type="COPY_TRANSFORMS", influence=1,
    target_space="WORLD", owner_space="WORLD",
    invert=True,
    owner="BONE"
    ):

    
    

    
    


    
    
    if bpy.data.objects[source].type == 'ARMATURE':
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects[source].data.bones.active = bpy.data.objects[source].data.bones[sbone]
        bc = bpy.data.objects[source].pose.bones[sbone].constraints
    else:
        bpy.ops.object.mode_set(mode='OBJECT')
        bc = bpy.data.objects[source].constraints

    if type == 'CHILD_OF':
        bc.new('CHILD_OF')
        bc['Child Of'].target =  bpy.data.objects[target]
        bc['Child Of'].subtarget = tbone
        bc['Child Of'].influence = influence
        bc['Child Of'].name = "BB Child Of"
        if invert == True:
            context_py = bpy.context.copy()
            context_py["constraint"] = bc.active
            bpy.ops.constraint.childof_set_inverse(context_py, constraint="BB Child Of", owner=owner)

        return
    elif type == 'COPY_LOCATION':
        bc.new('COPY_LOCATION')
        bc['Copy Location'].target = bpy.data.objects[target]
        bc['Copy Location'].subtarget = tbone
        bc['Copy Location'].target_space = target_space
        bc['Copy Location'].owner_space = owner_space
        bc['Copy Location'].influence = influence
        bc['Copy Location'].name = "BB Copy Loc"
        return
    elif type == 'COPY_ROTATION':
        bc.new('COPY_ROTATION')
        bc['Copy Rotation'].target = bpy.data.objects[target]
        bc['Copy Rotation'].subtarget = tbone
        bc['Copy Rotation'].target_space = target_space
        bc['Copy Rotation'].owner_space = owner_space
        bc['Copy Rotation'].influence = influence
        bc['Copy Rotation'].name = "BB Copy Rot"
        return
    elif type == 'COPY_SCALE':
        bc.new('COPY_SCALE')
        bc['Copy Scale'].target = bpy.data.objects[target]
        bc['Copy Scale'].subtarget = tbone
        bc['Copy Scale'].target_space = target_space
        bc['Copy Scale'].owner_space = owner_space
        bc['Copy Scale'].influence = influence
        bc['Copy Scale'].name = "BB Copy Scale"
        return
    elif type == 'COPY_TRANSFORMS':
        bc.new('COPY_TRANSFORMS')
        bc['Copy Transforms'].target = bpy.data.objects[target]
        bc['Copy Transforms'].subtarget = tbone
        bc['Copy Transforms'].target_space = target_space
        bc['Copy Transforms'].owner_space = owner_space
        bc['Copy Transforms'].influence = influence
        bc['Copy Transforms'].name = "BB Copy TRS"
        return
    else:
        print("add_constraint called with unknown type", type)


    restore_state(state)


    return







def get_unique_name():
    
    import uuid
    import time
    idn = str(uuid.uuid4())
    name = idn.replace("-", "")
    idt = str(time.time())
    time_now = idt.replace(".", "_")
    unique_name = name + "_" + time_now
    return unique_name



def get_unique_name_short(prefix=None):
    if prefix:
        name = prefix + "_"
    else:
        name = ""
    for i in range(100):
        unique_name = str(uuid.uuid4())
        result = name + unique_name.split('-', 1)[0]
        if result not in bpy.data.objects:
            break
    if i > 98:
        print("get_unique_name_short reports: 99 iterations searched and found, this probably can't happen:", result)
        return False
    return result









    
    

    
    
    
        

        
        

        
            
            
            
                
            
                

            
            
            
                

    
    
    

    
    
        
        
        
        
            
            
            
                
            
                
            
            
                
                    
                        





def combine_weights(group_new, groups, target):
    group_input = groups.copy()

    
    
    
    group_input.add(target)

    
    ob = bpy.context.active_object

    group_lookup = {g.index: g.name for g in ob.vertex_groups}
    group_candidates = {n for n in group_lookup.values() if n in group_input}

    
    if all(n in group_lookup.values() for n in group_candidates):
        pass

    
    if (len(group_candidates) and ob.type == 'MESH' and
        bpy.context.mode == 'OBJECT'):
        
        
        vertex_weights = {}
        for vert in ob.data.vertices:
            if len(vert.groups):  
                for item in vert.groups:
                    vg = ob.vertex_groups[item.group]
                    if vg.name in group_candidates:
                        if vert.index in vertex_weights:    
                            vertex_weights[vert.index] += vg.weight(vert.index)
                        else:
                            vertex_weights[vert.index] = vg.weight(vert.index)
            
        
        for key in vertex_weights.keys():
            if (vertex_weights[key] > 1.0): vertex_weights[key] = 1.0
        
        

        vgroup = ob.vertex_groups.new(name=group_new)
        
        
        for key, value in vertex_weights.items():
            vgroup.add([key], value ,'REPLACE') 


    return











def remove_empty_groups():

    state = False 
    ob = bpy.context.active_object
    ob.update_from_editmode()

    vgroup_used = {i: False for i, k in enumerate(ob.vertex_groups)}
    vgroup_names = {i: k.name for i, k in enumerate(ob.vertex_groups)}

    for v in ob.data.vertices:
        for g in v.groups:
            if g.weight > 0.0:
                vgroup_used[g.group] = True
                vgroup_name = vgroup_names[g.group]
                armatch = re.search('((.R|.L)(.(\d){1,}){0,1})(?!.)', vgroup_name)
                if armatch != None:
                    tag = armatch.group()
                    mirror_tag =  tag.replace(".R", ".L") if armatch.group(2) == ".R" else tag.replace(".L", ".R") 
                    mirror_vgname = vgroup_name.replace(tag, mirror_tag)
                    for i, name in sorted(vgroup_names.items(), reverse=True):
                        if mirror_vgname == name:
                            vgroup_used[i] = True
                            break
    for i, used in sorted(vgroup_used.items(), reverse=True):
        if not used:
            ob.vertex_groups.remove(ob.vertex_groups[i])
            state = True
    return state




def fix_bind_matrices(root, transform=0):
    
    
    
    

    
    
    
    n = '{http://www.collada.org/2005/11/COLLADASchema}'

    
    
        
        
        

    
    
    
    
    
    
    controllers = dict() 

    
    
    
    
    
    
    
    
    

    
    lib_con = root.find(f'{n}library_controllers')
    print("lib_con", lib_con)
    for controller in lib_con:
        
        id = controller.get('id')
        
        controllers[id] = dict()
        
        print("Saving bind matrix for", id)
        bind_shape_matrix = controller.find(f'{n}skin/{n}bind_shape_matrix')
        controllers[id]['bind_shape_matrix'] = bind_shape_matrix.text

        sources = controller.findall(f'{n}skin/{n}source')
        for source in sources:

            na = controller.find(f'{n}skin/{n}source/{n}Name_array')
            fa = controller.find(f'{n}skin/{n}source/{n}float_array')
            if na != None:
                controllers[id]['Name_array'] = na
            if fa != None:
                controllers[id]['float_array'] = fa


    
    
    
    
    
    
    


    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    if transform == 1:
        print("transform set, editing matrices...")
        
        

        
        for id in controllers:
            print("id:", id)
            na = controllers[id]['Name_array']
            bones = na.text.split()

            fa = controllers[id]['float_array']

            
            matrices = [float(i) for i in fa.text.split()]
            matrices_buffer = list()

            for bone in bones:
                if bone not in vol_joints:
                    
                    matrices_buffer.extend(matrices[:16])
                    del matrices[:16]
                    continue 

                
                
                
                

                
                print("Found volume", bone)

                
                
                floats = matrices[:16]
                del matrices[:16]

                
                scales = vol_joints[bone]['scale']

                
                factor_0 = 1 / scales[0]
                factor_1 = 1 / scales[1]
                factor_2 = 1 / scales[2]

                
                
                
                
                testing_scale = 0
                global_scale = 0.01
                if testing_scale == 1:
                    factor_0 = (1 + global_scale) / scales[0]
                    factor_1 = (1 + global_scale) / scales[1]
                    factor_2 = (1 + global_scale) / scales[2]

                
                
                
                

                floats[ 0] *= factor_0
                floats[ 3] *= factor_0
                floats[ 5] *= factor_1
                floats[ 7] *= factor_1
                floats[10] *= factor_2
                floats[11] *= factor_2

                
                
                all_floats = 0
                if all_floats == 1:
                    
                    floats[ 0] *= factor_0
                    floats[ 1] *= factor_0
                    floats[ 2] *= factor_0
                    floats[ 3] *= factor_0

                    floats[ 4] *= factor_1
                    floats[ 5] *= factor_1
                    floats[ 6] *= factor_1
                    floats[ 7] *= factor_1

                    floats[ 8] *= factor_2
                    floats[ 9] *= factor_2
                    floats[10] *= factor_2
                    floats[11] *= factor_2

                
                
                
                
                
                
                    
                    
                    
                    
                    
                    

                
                matrices_buffer.extend(floats)
                floats.clear()

            
            matrices_back = " ".join(str(item) for item in matrices_buffer)

            
            fa.text = matrices_back

    return controllers





def condition_matrices(controllers):
    
    
    for id in controllers:
        fa = controllers[id]['float_array']

        matrices_buffer = [float(i) for i in fa.text.split()]

        matrices_back = ""
        mat_fix = "\n"
        count = 0
        seg = 0
        for mat in matrices_buffer:
            count += 1
            seg += 1
            
            
            mat_str = str(mat)
            if mat_str.startswith("-"):
                space = " "
            else:
                space = "  "
            mat_fix += space + str(round(mat, 7))
            if count == 4:
                mat_fix += "\n"
                count = 0
            if seg == 16:
                mat_fix += "\n" 
                seg = 0
            matrices_back += mat_fix
            mat_fix = ""

        
        fa.text = matrices_back

    return



def activate(name):
    bpy.data.objects[name].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[name]
    return



def hide_volume_bones(arm):
    armObj = bpy.data.objects[arm]
    for boneObj in armObj.data.bones:
        bone = boneObj.name
        if bone in vbones_only:
            boneObj.hide = True
            if "bb_" + bone in armObj.data.bones:
                armObj.data.bones["bb_"+bone].hide = True
    armObj['hide_volume_bones'] = True
    return

def unhide_volume_bones(arm):
    armObj = bpy.data.objects[arm]
    for boneObj in armObj.data.bones:
        bone = boneObj.name
        if bone in vbones_only:
            boneObj.hide = False
            if "bb_" + bone in armObj.data.bones:
                armObj.data.bones["bb_"+bone].hide = False
    armObj['hide_volume_bones'] = False
    return



def hide_extended_bones(arm):
    armObj = bpy.data.objects[arm]
    for bone in extended_bones:
        mbone = "m" + bone
        bbone = "bb_" + bone
        if mbone in  armObj.data.bones:
            armObj.data.bones[mbone].hide = True
        if bbone in  armObj.data.bones:
            armObj.data.bones[bbone].hide = True
    armObj['hide_extended_bones'] = True
    return
def unhide_extended_bones(arm):
    armObj = bpy.data.objects[arm]
    for bone in extended_bones:
        mbone = "m" + bone
        bbone = "bb_" + bone
        if mbone in  armObj.data.bones:
            armObj.data.bones[mbone].hide = False
        if bbone in  armObj.data.bones:
            armObj.data.bones[bbone].hide = False
    armObj['hide_extended_bones'] = False
    return



def hide_face_bones(arm):
    armObj = bpy.data.objects[arm]
    for bone in face_bones:
        mbone = "m" + bone
        bbone = "bb_" + bone
        if mbone in  armObj.data.bones:
            armObj.data.bones[mbone].hide = True
        if bbone in  armObj.data.bones:
            armObj.data.bones[bbone].hide = True
    armObj['hide_face_bones'] = True
    return
def unhide_face_bones(arm):
    armObj = bpy.data.objects[arm]
    for bone in face_bones:
        mbone = "m" + bone
        bbone = "bb_" + bone
        if mbone in  armObj.data.bones:
            armObj.data.bones[mbone].hide = False
        if bbone in  armObj.data.bones:
            armObj.data.bones[bbone].hide = False
    armObj['hide_face_bones'] = False
    return



def hide_hand_bones(arm):
    armObj = bpy.data.objects[arm]
    for bone in hand_bones:
        mbone = "m" + bone
        bbone = "bb_" + bone
        if mbone in  armObj.data.bones:
            armObj.data.bones[mbone].hide = True
        if bbone in  armObj.data.bones:
            armObj.data.bones[bbone].hide = True
    armObj['hide_hand_bones'] = True
    return
def unhide_hand_bones(arm):
    armObj = bpy.data.objects[arm]
    for bone in hand_bones:
        mbone = "m" + bone
        bbone = "bb_" + bone
        if mbone in  armObj.data.bones:
            armObj.data.bones[mbone].hide = False
        if bbone in  armObj.data.bones:
            armObj.data.bones[bbone].hide = False
    armObj['hide_hand_bones'] = False
    return














def apply_sl_rotations(armature=""):
    obj = bpy.data.objects

    if armature == "":
        print("apply_sl_rotations reports: nothing to do")
        return False

    filename = script_dir + presets_path + "avatar_skeleton.py"
    avatar_skeleton = {}

    try:
        namespace = {}
        exec(open(filename, 'r', encoding='UTF8').read(), namespace)
        avatar_skeleton.update(namespace['avatar_skeleton'])
    except Exception as e:
        print(traceback.format_exc())

    armObj = obj[armature]

    
    set_mode(armature, "pose")
    for boneObj in armObj.data.bones:
        bone = boneObj.name

        
        
        
        
        
        if bone in cr_bones_hash:
            mbone = cr_bones_hash[bone]
            rot = avatar_skeleton[mbone]['rot']
        else:
            rot = avatar_skeleton[bone]['rot']

        
        
        
        xrot = radians(rot[0])
        yrot = radians(rot[1])
        zrot = radians(rot[2])

        armObj.data.bones[bone].select = True
        old_rotation_mode = armObj.pose.bones[bone].rotation_mode
        armObj.pose.bones[bone].rotation_mode = 'XYZ'
        armObj.pose.bones[bone].rotation_euler = (xrot, yrot, zrot)
        armObj.pose.bones[bone].rotation_mode = old_rotation_mode
        armObj.data.bones[bone].select = False

    return












def apply_sl_bone_roll(arm=""):

    
    
    
    
    
    
    

    print("applying stable bone roll", arm)

    if arm == "":
        print("apply_sl_bone_roll reports: nothing to do")
        return False
    obj = bpy.data.objects
    if arm not in obj:
        print("apply_sl_bone_roll reports: object not in scene -", arm)
        return False
    if obj[arm].type != 'ARMATURE':
        print("apply_sl_bone_roll reports: not an armature -", arm)
        return False
    

    
    
    

    mode = bpy.context.mode
    if len(bpy.context.selected_objects) > 0:
        selected = bpy.context.selected_objects
    else:
        selected = None

    if mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]
    bpy.ops.object.mode_set(mode='EDIT')

    
    

    
    
    for boneObj in obj[arm].data.edit_bones:
        boneObj.select = True
        boneObj.select_head = True
        boneObj.select_tail = True
    bpy.ops.armature.roll_clear(roll=0.0)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='POSE')

    
    
    bpy.ops.pose.select_all(action='DESELECT')

    
    bpy.ops.object.mode_set(mode='EDIT')
    for bone in bb_const['bone_roll']:
        if bone not in obj[arm].data.edit_bones:
            continue

        obj[arm].data.edit_bones[bone].select = True
        obj[arm].data.edit_bones[bone].select_head = True
        obj[arm].data.edit_bones[bone].select_tail = True

        obj[arm].data.edit_bones[bone].roll = bb_const['bone_roll'][bone]

        obj[arm].data.edit_bones[bone].select = False
        obj[arm].data.edit_bones[bone].select_head = False
        obj[arm].data.edit_bones[bone].select_tail = False

        
        
        
        if obj[arm].get('bentobuddy_control_rig') == 1:
            cr_bone = cr_bones_map[bone]
            obj[arm].data.edit_bones[cr_bone].select = True
            obj[arm].data.edit_bones[cr_bone].select_head = True
            obj[arm].data.edit_bones[cr_bone].select_tail = True

            obj[arm].data.edit_bones[cr_bone].roll = bb_const['bone_roll'][bone]

            obj[arm].data.edit_bones[cr_bone].select = False
            obj[arm].data.edit_bones[cr_bone].select_head = False
            obj[arm].data.edit_bones[cr_bone].select_tail = False

 
    
    
    
    
    
    
    
    
    
    
    
    


    
    

    
    bpy.ops.object.mode_set(mode='OBJECT')


    
    
    
    
        

    


    return True









def get_armature():
    if len(bpy.context.selected_objects) != 1:
        return None
    armObj = bpy.context.selected_objects[0]
    if armObj.type != 'ARMATURE':
        return None
    return armObj



def remove_armature_groups(arm):
    obj = bpy.data.objects
    for g in obj[arm].pose.bone_groups:
        obj[arm].pose.bone_groups.remove(g)
    print("remove_armature_groups reports: finished")
    return



def remove_bone_groups(arm):
    selected = bpy.context.selected_objects
    if bpy.context.active_object != None:
        active = bpy.context.active_object.name
    else:
        active = None

    if bpy.context.mode == 'EDIT_ARMATURE':
        old_mode = 'EDIT'
    else:
        old_mode = bpy.context.mode

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='SELECT')

    bpy.ops.pose.group_unassign()

    
    bpy.ops.pose.select_all(action='DESELECT')

    
        
        
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    if len(selected) != 0:
        for o in selected:
            o.select_set(True)
        bpy.ops.object.mode_set(mode=old_mode)
        if active != None:
            bpy.context.view_layer.objects.active = bpy.data.objects[active]

    return





def store_bone_data():
    
    

    
    
    

    obj = bpy.data.objects
    bbr = bpy.context.window_manager.bb_retarget

    

    
    
    
    
    

    source_bone_data = dict()
    target_bone_data = dict()

    for boneObj in obj[bbr.retarget_source_name].pose.bones:
        head = boneObj.head.copy()
        tail = boneObj.tail.copy()

        source_bone_data.setdefault(boneObj.name, {})
        source_bone_data[boneObj.name].setdefault("pose", {})
        source_bone_data[boneObj.name]["pose"].update({
            "head": head,
            "tail": tail,
            })

    for boneObj in obj[bbr.retarget_target_name].pose.bones:
        head = boneObj.head.copy()
        tail = boneObj.tail.copy()

        target_bone_data.setdefault(boneObj.name, {})
        target_bone_data[boneObj.name].setdefault("pose", {})
        target_bone_data[boneObj.name]["pose"].update({
            "head": head,
            "tail": tail,
            })

    
    bpy.ops.object.mode_set(mode='EDIT')

    
    
    
    
    bpy.context.view_layer.objects.active = obj[bbr.retarget_source_name]

    for boneObj in obj[bbr.retarget_source_name].data.edit_bones:
        head = boneObj.head.copy()
        tail = boneObj.tail.copy()
        roll = boneObj.roll 
        connect = boneObj.use_connect

        source_bone_data.setdefault(boneObj.name, {})
        source_bone_data[boneObj.name].setdefault("edit", {})
        source_bone_data[boneObj.name]["edit"].update({
            "head": head,
            "tail": tail,
            "roll": roll,
            "connect": connect,
            })

    bpy.context.view_layer.objects.active = obj[bbr.retarget_target_name]

    for boneObj in obj[bbr.retarget_target_name].data.edit_bones:
        head = boneObj.head.copy()
        tail = boneObj.tail.copy()
        roll = boneObj.roll
        connect = boneObj.use_connect

        target_bone_data.setdefault(boneObj.name, {})
        target_bone_data[boneObj.name].setdefault("edit", {})
        target_bone_data[boneObj.name]["edit"].update({
            "head": head,
            "tail": tail,
            "roll": roll,
            "connect": connect,
            })

    obj[bbr.retarget_source_name]['bone_data'] = source_bone_data
    obj[bbr.retarget_target_name]['bone_data'] = target_bone_data

    bpy.ops.object.mode_set(mode='POSE')

    return











def restore_sources(type="pose"):
    obj = bpy.data.objects
    bbr = bpy.context.window_manager.bb_retarget

    bpy.ops.object.mode_set(mode='EDIT')

    
    
    

    
    
    
    
    
    source_location = obj[bbr.retarget_source_name_backup].matrix_world.to_translation().copy()

    
    bone_map = obj[bbr.retarget_source_name_backup]['bone_map'].to_dict()
    bone_data = obj[bbr.retarget_source_name_backup]['bone_data'].to_dict()

    
    for sbone in bone_map:
        tbone = bone_map[sbone]
        
        restore_source_bone(sbone, type)

    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action = 'DESELECT')



    return











def restore_source_bone(sbone, type):
    obj = bpy.data.objects
    bbr = bpy.context.window_manager.bb_retarget

    
    
    

    if type == "pose":
        obj[bbr.retarget_source_name_backup].data.edit_bones[sbone].head =            obj[bbr.retarget_source_name_backup]['bone_data'][sbone]['pose']['head']
        obj[bbr.retarget_source_name_backup].data.edit_bones[sbone].tail =            obj[bbr.retarget_source_name_backup]['bone_data'][sbone]['pose']['tail']
        obj[bbr.retarget_source_name_backup].data.edit_bones[sbone].roll =            obj[bbr.retarget_source_name_backup]['bone_data'][sbone]['edit']['roll']

    elif type == "edit":
        obj[bbr.retarget_source_name_backup].data.edit_bones[sbone].head =            obj[bbr.retarget_source_name_backup]['bone_data'][sbone]['edit']['head']
        obj[bbr.retarget_source_name_backup].data.edit_bones[sbone].tail =            obj[bbr.retarget_source_name_backup]['bone_data'][sbone]['edit']['tail']
        
            

    else:
        print("restore_source_bone reports bad restore type:", type)

    return




def clear_constraints(armature=""):
    if armature =="":
        print("clear_pose: What?... nothing to clear!")
        return
    obj = bpy.data.objects
    if armature not in bpy.data.objects.keys():
        print("clear_constraints reports: We don't have that object dood:", armature)
        return
    
    
    
    
    
    selected = bpy.context.selected_objects
    if len(selected) > 0:
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

    obj[armature].select_set(True)
    bpy.context.view_layer.objects.active = obj[armature]
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action = 'SELECT')

    bpy.ops.pose.constraints_clear()

    bpy.ops.pose.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    for o in selected:
        o.select_set(True)

    return










def clean_bone_groups(armatures=[]):
    obj = bpy.data.objects
    if len(armatures) == 0:
        print("clean_bone_groups reports: nothing to do, pass me some armatures")
        return False
    
        
        

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    for arm in armatures:



        obj[arm].select_set(True)
        bpy.context.view_layer.objects.active = obj[arm]
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action = 'SELECT')
        bpy.ops.pose.group_unassign()
        bpy.ops.pose.select_all(action = 'DESELECT')
        obj[arm].select_set(False)

    bpy.ops.object.mode_set(mode='OBJECT')

    return True


















def get_armatures_from_mesh():
    for o in bpy.context.selected_objects:
        if o.type == 'MESH':
            pass











def get_mesh_armature(mesh=""):
        obj = bpy.data.objects

        if mesh == "":
            print("get_mesh_armature reports: I need a mesh object to work with, I got nothing")
            return False

        if mesh not in obj:
            print("get_mesh_armature reports: mesh not in the viewable scene:", mesh)
            return False

        
        mods = []
        for m in obj[mesh].modifiers:
            if m.type == 'ARMATURE':
                mods.append(m.name)

        if len(mods) > 1:
            print("get_mesh_armature reports: too many armature modifiers")
            return False 
        if len(mods) == 0:
            print("get_mesh_armature reports: can't find an armature modifier")
            return False 

        mod = mods[0] 
        
        if obj[mesh].modifiers[mod].object == None:
            print("get_mesh_armature reports: armature modifier exists but doesn't point to anything")
            return False
        arm = obj[mesh].modifiers[mod].object.name 
        return arm





def get_mesh_armature_modifier(mesh=""):
        obj = bpy.data.objects
        if mesh == "":
            print("I need a mesh object to work with, I got nothing")
            return False
        if mesh not in obj:
            print("mesh not in the viewable scene:", mesh)
            return False
        
        
        has_arm = 0
        for m in obj[mesh].modifiers:
            if m.type == 'ARMATURE':
                has_arm = 1
                break
        if has_arm == 1:
            return m.name

        return False





def attach_armature_modifier(mesh="", mod="", arm=""):
    obj = bpy.data.objects
    obj[mesh].modifiers[mod].object = obj[arm]
    obj[mesh].parent = obj[arm]












def scale_transforms(elements, scale):
        Tx,Ty,Tz = elements
        Sx,Sy,Sz = scale
        sl = list()
        sl = Tx * (1/Sx), Ty * (1/Sy), Tz * (1/Sz)
        return sl




def has_action(armature=""):
    armObj = bpy.data.objects[armature]
    if armObj.animation_data == None:
        return False
    if armObj.animation_data.action == None:
        return False
    return True



def remove_unused_actions():
    for action in bpy.data.actions:
        if action.users == 0:
            bpy.data.actions.remove(action)














def make_lines(text="", before="", after="", max=1):
    if text == "":
        print("nothing to do")
        return
    buffer = list()
    line = before
    count = 0
    last_word = ""
    words = re.split(r'(\s+)', text)
    for word in words:
        count += len(word) + len(last_word)
        if count == max:
            buffer.append(line + word + after)
            line = before
            count = 0
        elif count > max:
            buffer.append(line + after)
            line = before
            last_word = word
            count = 0
        else:
            last_word = ""
            line += word
    return buffer


























    
    
    
    
    
    
    
    
    
    
    
        





















    










    










def matrix_world(armature_ob, bone_name):
    local = armature_ob.data.bones[bone_name].matrix_local
    basis = armature_ob.pose.bones[bone_name].matrix_basis

    parent = armature_ob.pose.bones[bone_name].parent
    if parent == None:
        return  local @ basis
    else:
        parent_local = armature_ob.data.bones[parent.name].matrix_local
        return matrix_world(armature_ob, parent.name) @ (parent_local.inverted() @ local) @ basis
    return

















def worldMatrix(ArmatureObject,Bone):
    _bone = ArmatureObject.pose.bones[Bone]
    _obj = ArmatureObject
    return _obj.matrix_world @ _bone.matrix
























def world_matrix(armature="", bone=""):
    ArmatureObject = bpy.data.objects[armature]
    
    Bone = ArmatureObject.pose.bones[bone]
    _bone = ArmatureObject.pose.bones[bone]
    _obj = ArmatureObject
    return _obj.matrix_world @ _bone.matrix






def limit_weights(mesh="", limit=4):


    obj = bpy.data.objects
    if mesh == "":
        print("nothing to do")
        return False
    if mesh not in obj:
        print("object not in scene:", mesh)
        return False
    if obj[mesh].type != 'MESH':
        print("only works on meshes:", obj[mesh].type)
        return False
    if bpy.context.mode != 'OBJECT':
        if len(bpy.context.selected_objects) != 0:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
    obj[mesh].select_set(True)
    bpy.context.view_layer.objects.active = obj[mesh]
    bpy.ops.object.mode_set(mode='WEIGHT_PAINT')



    bpy.ops.object.vertex_group_limit_total(limit=limit)
    bpy.ops.object.mode_set(mode='OBJECT')

    return True











def set_bvh_names(arm=""):
    obj = bpy.data.objects

    if arm == "":
        print("No object provided")
        return False
    if arm not in obj:
        print("Object not in scene", arm)
        return False
    if obj[arm].type != 'ARMATURE':
        print("Object is not an armature:", arm)

    
    
    
    
    for mbone in bvh_names:
        bvh_bone = bvh_names[mbone]
        if mbone in obj[arm].data.bones:
            obj[arm].data.bones[mbone].name = bvh_bone
    return True

    

    
    
    
    
    

    
    
    
    
    
    
        
        
            
        
        
    
    
        
        
            

    








def attach_control_rig(armature=""):
    if armature == "":
        print("attach_control_rig reports: nothing to do")
        return False
    if bpy.context.mode != 'OBJECT':
        print("attach_control_rig reports: wrong context, use OBJECT")
        return False
    obj = bpy.data.objects
    if obj[armature].type != 'ARMATURE':
        print("attach_control_rig reports: not an armature", armature)

    armObj = obj[armature]

    bpy.ops.object.select_all(action='DESELECT')
    armObj.select_set(True)
    bpy.context.view_layer.objects.active = armObj

    
    
    bpy.ops.object.duplicate()
    
    armCtrl = bpy.context.selected_objects[0]
    
    armCtrl.name = armObj.name + "_controller"
    
    for boneObj in armCtrl.data.bones:
        boneObj.use_deform = False

    
    
    

    bpy.ops.object.select_all(action='DESELECT')
    armObj.select_set(True)
    bpy.context.view_layer.objects.active = armObj
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='DESELECT')

    for boneObj in armObj.pose.bones:
        source = armObj.name
        target = armCtrl.name
        sbone = boneObj.name
        tbone = sbone
        add_constraint(source=source, sbone=sbone, target=target, tbone=tbone, type="COPY_TRANSFORMS", influence=1)

    
    clean_bone_groups(armatures=[armCtrl.name])
    
    create_bone_group(armCtrl.name, cr_vbones_group_name, cr_vbones_theme)
    create_bone_group(armCtrl.name, cr_mbones_group_name, cr_mbones_theme)
    for mbone in mbones_only:
        if mbone in armCtrl.data.bones:
            add_bone_to_group(armature=armCtrl.name, bone=mbone, group=cr_mbones_group_name)
    for vbone in vbones_only:
        if vbone in armCtrl.data.bones:
            add_bone_to_group(armature=armCtrl.name, bone=vbone, group=cr_vbones_group_name)

    
    armCtrl['base'] = armObj.name
    armObj['controller'] = armCtrl.name

    
    armObj.hide_set(True)
    
    bpy.ops.object.select_all(action='DESELECT')
    armCtrl.select_set(True)
    bpy.context.view_layer.objects.active = armCtrl

    return True








def scale_animation_y():
    for a in bpy.data.actions:
        for fc in a.fcurves:
            if "location" in fc.data_path:
                a.fcurves.remove(fc)
    ob = bpy.context.object
    for pb in ob.pose.bones:
        pb.location = (0, 0, 0)

    bpy.ops.object.transform_apply(scale=True)








































def rename_fcurve_channels(arm):
    obj = bpy.data.objects

    action_name = obj[arm].animation_data.action.name

    for mbone in obj[arm].pose.bones:
        if mbone in bvh_names:
            bvh_bone = bvh_names[mbone]
        else:
            print("Terminal error, mbone does not exist in bvh_names:", mbone)
            return Fase

    for fc in bpy.data.actions[action_name].fcurves:
        fc.data_path = fc.data_path.replace(mbone, bvh_bone)

    
    
    








    
    








def roll_rig_set(arm):
    obj = bpy.data.objects
    rotation_mode = obj[arm].rotation_mode
    obj[arm].rotation_mode = 'XYZ'
    x,y,z = obj[arm].rotation_euler
    if x == 0:
        obj[arm].rotation_euler = (1.5708, 0.0, 0.0)
    obj[arm].rotation_mode = rotation_mode













def rotate_toggle(arm, angle=[90, 0, 0]):
    
    obj = bpy.data.objects
    if arm == "":
        print("rotate_toggle reports: nothing to do")
    if arm not in obj:
        print("rotate_toggle reports: object  not in scene", arm)

    selected = bpy.context.selected_objects

    if bpy.context.active_object != None:
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]

    
    
    
    
    
    bpy.ops.object.transform_apply( rotation=True, location=False, scale=False )

    rotation_mode = obj[arm].rotation_mode
    obj[arm].rotation_mode = 'XYZ'

    
    
    
    
    
    

    
    
    rads = tuple(round(radians(i), 6) for i in angle)
    obj[arm].rotation_euler = (-rads[0], -rads[2], -rads[2])
    bpy.ops.object.transform_apply( rotation=True, location=False, scale=False )

    
    
    obj[arm].rotation_euler = rads
    obj[arm].rotation_mode = rotation_mode

    bpy.ops.object.select_all(action='DESELECT')

    for o in selected:
        o.select_set(True)

    return



def clear_transforms(object="", location=False, rotation=False, scale=False):
    
    obj = bpy.data.objects
    if object == "":
        print("clear_transforms reports: nothing to do")
    if object not in obj:
        print("clear_transforms reports: object  not in scene", arm)
    selected = bpy.context.selected_objects
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[object].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[object]

    if location == True:
        bpy.ops.object.location_clear()
    if rotation == True:
        bpy.ops.object.rotation_clear()
    if scale == True:
        bpy.ops.object.scale_clear()

    bpy.ops.object.select_all(action='DESELECT')
    for o in selected:
        o.select_set(True)
    return












def rotate_object(object="", angle="", apply_before=False, apply_after=False, apply_pose=False):
        
        obj = bpy.data.objects

        if object =="":
            print("rotate_object reports: nothing to do")
            return False
        if object not in obj:
            print("rotate_object reports: object not in scene -", object)
            return False
        if angle=="":
            print("rotate_object reports: no angle given")
            return False

        
        if len(bpy.context.selected_objects) == 1:
            selected = bpy.context.selected_objects[0]
            
            mode = bpy.context.mode
        else:
            selected = None

        
        
        safe_select(object)

        
        x,y,z = angle
        
        
        xrot = radians(x)
        yrot = radians(y)
        zrot = radians(z)

        print("rotate_object reports: selected =", bpy.context.selected_objects)

        if apply_before == True:
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

        old_rot_mode = obj[object].rotation_mode
        obj[object].rotation_mode = 'XYZ'

        
        
        ox, oy, oz = obj[object].rotation_euler
        xrot += ox
        yrot += oy
        zrot += oz




        obj[object].rotation_euler = (xrot, yrot, zrot)

        if apply_after == True:
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

        obj[object].rotation_mode = old_rot_mode

        
        
        
        
        if apply_pose == True:
            if obj[object].type != 'ARMATURE':
                print("rotate_object reports: apply_pose is True but it's not an armature")
            else:
                bpy.ops.object.mode_set(mode='POSE')
                bpy.ops.pose.armature_apply()
                bpy.ops.object.mode_set(mode='OBJECT')

        
        if selected != None:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            selected.select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects[selected.name]
            bpy.ops.object.mode_set(mode=mode)
           
        return True



def update():
    bpy.context.view_layer.update()











def save_state():

    
    
    if bb_settings['save_state'] == False:
        print("save_state reports: save_state is disabled")
        return False

    obj = bpy.data.objects
    bbm = bpy.context.window_manager.bb_misc

    state = get_unique_name()

    
    if bbm.get('states') == None:
        bbm['states'] = dict()
    else:
        if state in bbm['states']:
            print("save_state reports: state collision -", state)

    bbm['states'][state] = dict()
    bbm['states'][state]['mode'] = bpy.context.mode

    if bpy.context.active_object != None:
        bbm['states'][state]['active'] = bpy.context.active_object.name
    else:
        bbm['states'][state]['active'] = ""

    bbm['states'][state]['selected'] = list()
    
    selected = list()

    for o in bpy.context.selected_objects:
        print("appended selected object to state:", o.name)
        selected.append(o.name)
        
    bbm['states'][state]['selected'] = selected

    print("save_state reports: total states -", len(bbm['states']))
    return state

def restore_state(state):

    if bb_settings['save_state'] == False:
        print("save_state reports: save_state is disabled so restore_state is as well")
        return False

    if state == "":
        print("restore_state reports: nothing to do")
        return False
    obj = bpy.data.objects
    bbm = bpy.context.window_manager.bb_misc
    if state not in bbm['states']:
        print("restore_state reports: state doesn't exist -", state)
        return False

    if len(bpy.context.selected_objects) > 0:
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

    
    for object in bbm['states'][state]['selected']:
        obj[object].select_set(True)

    
    
    if bbm['states'][state]['active'] != "":
        object = bbm['states'][state]['active']
        bpy.context.view_layer.objects.active = obj[object]
    
    if len(bbm['states'][state]['selected']) > 0:
        
        
        try:
            bpy.ops.object.mode_set(mode=bbm['states'][state]['mode'])
        except:
            print("unable to set mode when restoring state for object:", object)

    del bbm['states'][state]
    print("restore_state reports: total states -", len(bbm['states']))

    return True








def save_armature_state(armature=""):
    obj = bpy.data.objects
    bbm = bpy.context.window_manager.bb_misc

    if armature == "":
        print("save_armature_states reports: nothing to do")
        return False
    if armature not in obj:
        print("save_armature_states reports: object missing from scene -", armature)
        return False

    state = get_unique_name()

    
    if bbm.get('arm_states') == None:
        bbm['arm_states'] = dict()
    else:
        if state in bbm['arm_states']:
            print("save_armature_state reports: state collision -", state)

    bbm['arm_states'][state] = dict()

    
    bbm['arm_states'][state]['armature'] = armature

    
    
    layers = list()
    for l in obj[armature].data.layers:
        layers.append(l)
    bbm['arm_states'][state]['view_layers'] = layers

    
    
    new_states = list()
    for s in obj[armature].data.layers:
        new_states.append(True)

    
    obj[armature].data.layers = new_states

    
    bone_properties = {}
    for boneObj in obj[armature].data.bones:
        bone_properties.setdefault(boneObj.name, {})
        bone_properties[boneObj.name]['hide_select'] = boneObj.hide_select
        
        boneObj.hide_select = False
        bone_properties[boneObj.name]['hide'] = boneObj.hide
        
        boneObj.hide = False

    bbm['arm_states'][state]['bones'] = bone_properties

    return state

def restore_armature_state(state):
    obj = bpy.data.objects
    bbm = bpy.context.window_manager.bb_misc

    if state == "":
        print("restore_armature_state reports: nothing to do")
        return False

    if state not in bbm['arm_states']:
        print("restore_armature_state reports: state doesn't exist -", state)
        return False

    arm = bbm['arm_states'][state]['armature']

    
    
    
    layers = list()
    for l in bbm['arm_states'][state]['view_layers']:
        if l == 1:
            layers.append(True)
        else:
            layers.append(False)
    
    obj[arm].data.layers = layers

    for boneObj in obj[arm].data.bones:
        bone = boneObj.name
        boneObj.hide_select = bbm['arm_states'][state]['bones'][bone]['hide_select']
        boneObj.hide = bbm['arm_states'][state]['bones'][bone]['hide']

    del bbm['arm_states'][state]
    print("restore_armature_state reports: remaining states after processing -", len(bbm['arm_states']))
    return True













def ccm_to_ctm(ccm=""):
    if ccm == "":
        print("ccm_to_ctm reports: nothing to do")
        return None
    
    
    target = "arm_" + get_unique_name_short()
    ctm = dict()
    for tbone in ccm:
        mbone = ccm[tbone]
        ctm[mbone] = {target: tbone}
    return ctm


def ctm_to_ccm(ctm=""):
    if ctm == "":
        print("ctm_to_ccm reports: nothing to do")
        return None
    
    
    
    
    
    
    
    ccm = dict()
    for sbone in ctm:
        (tarm, tbone), = ctm[sbone].items()
        ccm[tbone] = sbone
    return ccm




def read_ccm(path=""):
    if path == "":
        print("read_ccm reports: nothing to do")
        return None

    container = dict()
    rename = {}
    reskin = {}
    pose = {}

    try:
        namespace = {}
        exec(open(path, 'r', encoding='UTF8').read(), namespace)
    except Exception as e:
        print(traceback.format_exc())
        return None

    try:
        rename.update(namespace['rename'])
    except:
        print("no rename, nothing to do")
        ccp.icon_thumb = "thumb_down"
        ccp.load_map_info = "Damaged map file!"
        return False
    try:
        reskin.update(namespace['reskin'])
    except:
        print("no reskin, skipping")

    try:
        pose.update(namespace['pose'])
    except:
        print("no pose, skipping")

    container['rename'] = rename
    container['reskin'] = reskin
    container['pose'] = pose

    return container


def read_ctm(path=""):
    if path == "":
        print("read_ctm reports: nothing to do")
        return None
    container = dict()
    try:
        namespace = {}
        exec(open(path, 'r', encoding='UTF8').read(), namespace)
        container.update(namespace['template_map'])
    except Exception as e:
        print(traceback.format_exc())
        return False 
    return container













def write_ccm(path="", container="", rename="", reskin="", armature=""):
    if path =="":
        print("write_ccm reports: need a path")
        return None
    if rename =="":
        print("write_ccm reports: I need at least a rename sequence")
        return None

    obj = bpy.data.objects

    
    
    if container == "":
        container = {}
        container['rename'] = rename
        container['reskin'] = reskin

    for hash in container:
        if hash == "rename":
            rename_maps += "rename = {\n";
            for tbone in container[hash]:
                rename_maps += "    " + '"' + tbone + '": ' + '"' + container[hash][tbone] + '"' + ",\n"
            rename_maps += "    }\n"

        elif hash == "reskin":
            reskin_maps += "reskin = {\n";
            for anchor in container[hash]:
                reskin_maps += "    " + '"' + anchor + '": [' + "\n"
                for reskin in container[hash][anchor]:
                    reskin_maps += "        " + '"' + reskin + '"' + ",\n"
                reskin_maps += "        ],\n"
            reskin_maps += "    }\n"

        else:
            txt = "Internal Data Error, unknown storage type [" + hash + "]"
            print(txt)

    if armature != "":

        
        
        if armature in obj:
            
            pose_map = "pose = {\n"
            for pose_bone in obj[armature].pose.bones[:]:
                obj[armature].data.bones[pose_bone.name].select = True
                old_rotation_mode = obj[armature].pose.bones[pose_bone.name].rotation_mode
                obj[armature].pose.bones[pose_bone.name].rotation_mode = 'XYZ'

                float_0 = obj[armature].pose.bones[pose_bone.name].rotation_euler[0]
                float_1 = obj[armature].pose.bones[pose_bone.name].rotation_euler[1]
                float_2 = obj[armature].pose.bones[pose_bone.name].rotation_euler[2]

                pose_map += '    "' + pose_bone.name + '": ' + "(" + str(float_0) + ", " + str(float_1) + ", " + str(float_2) + "),\n"

                obj[armature].pose.bones[pose_bone.name].rotation_mode = old_rotation_mode
                obj[armature].data.bones[pose_bone.name].select = False
            pose_map += "    }\n"
        else:
            pose_map = "" 

        formatted_maps += rename_maps + reskin_maps + pose_map

        output = open(path, 'w', encoding='UTF8')
        output.write(formatted_maps)
        output.close()

    return True


def write_ctm(container="", path=""):
    if container == "" or path == "":
        print("write_ctm reports: nothing to do")
        return None

    template_map = "# Character Template Map auto-generated by Bento Buddy\n"
    template_map += "template_map = {\n"
    for sbone in container:
        (tarm, tbone), = container[sbone].items()
        template_map += "    " + '"' + sbone + '": ' + '{' + "\n"
        template_map += "        " + '"' + tarm +'": ' + '"' + tbone + '",' + "\n" + "        },\n"
    template_map += "    }\n"

    output = open(self.properties.filepath, 'w', encoding='UTF8')
    output.write(template_map)
    output.close()

    return True










def set_rotation_mode(armature="", mode="QUATERNION"):
    obj = bpy.data.objects
    bbm = bpy.context.window_manager.bb_misc

    if armature == "":
        print("set_rotation_mode reports: nothing to do")

    if bpy.context.mode != 'POSE':
        print("set_rotation_mode reports: not in pose mode, some coding error occurred")
        return False

    selected_bones = bpy.context.selected_pose_bones
    bpy.ops.pose.select_all(action = 'DESELECT')

    
    id = get_unique_name()

    if bbm.get('rotate_state') == None:
        bbm['rotate_state'] = {}
    if id in bbm['rotate_state']:
        print("set_rotation_mode reports: rotate state exists, overwriting:", rotate_state)
    bbm['rotate_state'][id] = {}

    armObj = obj[armature]

    for boneObj in bpy.context.selected_pose_bones:
        armObj.data.bones[boneObj.name].select = True
        bbm['rotate_state'][id][boneObj.name] = bone.rotation_mode
        armObj.pose.bones[boneObj.name].rotation_mode = mode
        armObj.data.bones[boneObj.name].select = False

    
    for poseBone in selected_bones:
        obj[armature].data.bones[poseBone.name].select = True

    return id


def restore_rotation_mode(armature="", id=""):
    obj = bpy.data.objects
    bbm = bpy.context.window_manager.bb_misc
    if id == "":
        print("get_rotation_mode reports: nothing to do")
        return False
    if id not in bbm['rotate_state']:
        print("get_rotation_mode reports: id does not exist -", id)
        return False

    selected_bones = bpy.context.selected_pose_bones
    bpy.ops.pose.select_all(action = 'DESELECT')

    for bone in bbm['rotate_state'][id]:
        obj[armature].data.bones[bone].select = True
        if bone not in armObj.pose.bones:
            print("restore_rotation_mode reports: missing bone in armature -", bone)
        armObj.pose.bones[boneObj.name].rotation_mode = bbm['rotate_state'][id]
    del bbm['rotate_state'][id]

    for poseBone in selected_bones:
        obj[armature].data.bones[poseBone.name].select = True

    return






def apply_transform_chain(object):
    if object == "":
        print("reset_transform_chain reports: no object")
        return False
    obj = bpy.data.objects
    if object not in obj:
        print("reset_transform_chain reports: object not in scene -", object)
        return False

    if obj[object].type == 'MESH':
        arm = get_mesh_armature(object)
        descendants = obj[arm].children
    elif obj[object].type == 'ARMATURE':
        arm = object
        descendants = obj[object].children
    else:
        print("I don't know what this is, I can process an armature or a mesh")
        return False

    
    
    
    

    
    try:
        obj[arm].select_set(True)
    except:
        txt = "Armature can't be selected.  Not in view? " + arm
        print(txt)
        popup(txt, "Error", "ERROR")
        return False
    
    for meshObj in descendants:
        if meshObj.type != 'MESH':
            continue
        try:
            meshObj.select_set(True)
        except:
            txt = "Mesh can't be selected, not in view? " + meshObj.name
            print(txt)
            popup(txt, "Error", "ERROR")
            return False

    apply_transforms(object=arm, scale=True, rotation=True, location=True)

    for d in descendants:
        if d.type == 'MESH':
            apply_transforms(object=d.name, scale=True, rotation=True, location=True)
        else:
            print("apply_transform_chain reports: found non mesh item", d.name)

    return True








def find_edge_loops(loop,max_loops=1000, type="object"):
    edgeObjProcessed = list()
    edgeIndexProcessed = list()

    i=0
    first_loop=loop
    while i<max_loops: 
        
        loop = loop.link_loop_next.link_loop_radial_next.link_loop_next
        loop.edge.select = True

        
        
        edgeObjProcessed.append(loop.edge)
        edgeIndexProcessed.append(loop.edge.index)

        i += 1
        
        if loop == first_loop:
            break        

    if type == "object":
        return edgeObjProcessed
    elif type == "index":
        return edgeIndexProcessed







    
    
    
    






def find_edge_rings(loop,max_loops=1000):
    i=0
    first_loop=loop
    while i<max_loops: 
        
        loop = loop.link_loop_radial_next.link_loop_next.link_loop_next
        loop.edge.select = True
        i += 1
        
        if loop == first_loop:
            break        





    
    
    
    





















def delete_geometry(object="", geometry="", context="EDGES"):
    if object == "":
        print("delete_geometry reports: no object")
        return None
    if geometry == "":
        print("delete_geometry reports: no geometry")
        return None
    obj = bpy.data.objects
    if object not in obj:
        print("delete_geometry reports: object not in scene -", object)
        return None
    if len(geometry) == 0:
        print("delete_geometry reports: no geometry to remove")
        return None

    
    
    
    
    
    
    
    
    

    
    
    
    
    

    
    
    
    
    
    bmesh.ops.delete(bm, geom=geometry, context=context)

    
    bmesh.update_edit_mesh(me, True)

    return





def get_selected_edges():
    ob = bpy.context.object
    
    
    me = ob.data
    se = list()
    for e in me.edges:
        if e.select == True:
            se.append(e.index)
    return se



def get_selected_polygons():
    polys = list()
    o = bpy.context.selected_objects[0]
    o.update_from_editmode()
    for p in o.data.polygons:
        if p.select == True:
            polys.append(p.index)
            
    return polys



def invert_polygon_selection():
    o = bpy.context.selected_objects[0]
    bpy.ops.object.mode_set(mode='OBJECT')
    for p in o.data.polygons:
        p.select = not p.select
    bpy.ops.object.mode_set(mode='EDIT')
    return









def select_element():
    bpy.ops.mesh.select_linked()





def matrix_to_degrees(matrix=""):
    eu = matrix.to_euler()
    rx,ry,rz = eu
    x = math.degrees(rx)
    y = math.degrees(ry)
    z = math.degrees(rz)
    
    return [x,y,z]



def create_collection(name=""):
    if name == "":
        print("create_collection reports: empty name")
        return False
    if name in bpy.data.collections:
        
        print("create_collection reports: collection prefix", [name], "exists, generating new collection")
    new_c = bpy.data.collections.new(name)
    
    bpy.context.scene.collection.children.link(new_c)
    
    
    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[new_c.name]
    print("Collection", new_c.name, "created and should be activated, see below...")
    print("Current active collection:", bpy.context.view_layer.active_layer_collection.name)
    

    return new_c



def remove_collection(name=""):
    if name == "":
        print("remove_collection reports: empty name")
        return False
    if name not in bpy.data.collections:
        print("remove_collection reports: collection", name, "does not exist")
        return False
    col = bpy.data.collections[name]
    to_delete = []
    for o in col.objects:
        to_delete.append(o)

    
    
    
    
    
    bpy.ops.object.delete({"selected_objects": to_delete})

    
        
        

    
    bpy.data.collections.remove(col)

    return True












    
    
    
    
    


    








def set_frame(frame=0):
    bpy.context.scene.frame_set(frame)
    return







def get_test_angles(reverse=False):

    bbm = bpy.context.window_manager.bb_misc

    pos =  90
    neg = -90
    x = bbm.test_angle_x
    y = bbm.test_angle_y
    z = bbm.test_angle_z

    if reverse == True:
        pos =  -90
        neg =  90
        x = -x
        y = -y
        z = -z
 
    angles = [
        x,
        y,
        z
        ]

    if bbm.test_angle_pos_x == True:
        angles[0] = pos
    if bbm.test_angle_neg_x == True:
        angles[0] = neg
    if bbm.test_angle_pos_y == True:
        angles[1] = pos
    if bbm.test_angle_neg_y == True:
        angles[1] = neg
    if bbm.test_angle_pos_z == True:
        angles[2] = pos
    if bbm.test_angle_neg_z == True:
        angles[2] = neg

    return angles















def close_enough(a, b, tol=0.000001):
    if a > b:
        n = round((a - b), 6)
    elif a < b:
        n = round((b - a), 6)
    elif a == b:
        return False
    if n > tol:
        return True
    return False








def ease_motion(a=None, b=None, amount=0.8):

    try:
        return a.slerp(b, amount)
    except:
        print("mod_functions::ease_motion complains : not sure what to do")
        return False

    

    Rz90 = mathutils.Matrix((
           ( 0.0, 1.0, 0.0, 0.0),
           (-1.0, 0.0, 0.0, 0.0),
           ( 0.0, 0.0, 1.0, 0.0),
           ( 0.0, 0.0, 0.0, 1.0)
           ))

    
    
    
    

    
    
    
    
    
    
    mat = bpy.context.object.matrix_world.copy()
    bpy.context.object.matrix_world = Rz90
    mat90 = bpy.context.object.matrix_world.copy()
    bpy.context.object.matrix_world = mathutils.Matrix()

    quat = mat.to_quaternion()
    quat90 = mat90.to_quaternion()
    mat_mid = quat.slerp(quat90, 0.5)
    qmat = mat_mid.to_matrix().to_4x4()
    bpy.context.object.matrix_world = qmat
    return












