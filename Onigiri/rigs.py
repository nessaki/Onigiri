
print("rigs loaded")
print(__name__, __file__)

import bpy
import sys
import math
import uuid
import time
import traceback

import mathutils
import xml.etree.ElementTree as ET

from . import utils
from . import visible
from . import globals
from . import mod_data
from . import mod_data as md
from . import mod_functions as mf
from . import animutils
from .presets import volumes
from .presets import rig_data
rd = rig_data

from .presets import skeleton as skel











vbones_to_mbones = {
    "PELVIS": "mPelvis",
    "BUTT": "mPelvis",
    "BELLY": "mTorso",
    "LEFT_HANDLE": "mTorso",
    "RIGHT_HANDLE": "mTorso",
    "LOWER_BACK": "mTorso",
    "CHEST": "mChest",
    "LEFT_PEC": "mChest",
    "RIGHT_PEC": "mChest",
    "UPPER_BACK": "mChest",
    "NECK": "mNeck",
    "HEAD": "mHead",
    "L_CLAVICLE": "mCollarLeft",
    "L_UPPER_ARM": "mShoulderLeft",
    "L_LOWER_ARM": "mElbowLeft",
    "L_HAND": "mWristLeft",
    "R_CLAVICLE": "mCollarRight",
    "R_UPPER_ARM": "mShoulderRight",
    "R_LOWER_ARM": "mElbowRight",
    "R_HAND": "mWristRight",
    "R_UPPER_LEG": "mHipRight",
    "R_LOWER_LEG": "mKneeRight",
    "R_FOOT": "mAnkleRight",
    "L_UPPER_LEG": "mHipLeft",
    "L_LOWER_LEG": "mKneeLeft",
    "L_FOOT": "mAnkleLeft",
    }



def get_unique_name():
    
    idn = str(uuid.uuid4())
    name = idn.replace("-", "")
    idt = str(time.time())
    time_now = idt.replace(".", "_")
    unique_name = name + "_" + time_now
    return unique_name









































def create_rig(target="default"):

    obj = bpy.data.objects

    
    

    

    if target == "default":
        print("Create default rig")
        rig_target = rd.default
    elif target == "neutral":
        print("Create neutral rig")
        rig_target = rd.neutral
    elif target == "male_default":
        print("Create default male rig")
        rig_target = rd.male_default
    elif target == "male_neutral":
        print("Create neutral male rig")
        rig_target = rd.male_neutral
    elif target == "basic":
        print("Create basic rig")
        rig_target = rd.basic

    else:
        print("rigs::create_rig reports: unknown rig target", target)
        return False

    
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

    
    arm_thing = bpy.data.armatures.new("BentoBuddy")
    armObj = bpy.data.objects.new("BentoBuddy", arm_thing)

    
    bpy.context.scene.collection.objects.link(armObj)
    bpy.context.view_layer.update()
    arm = armObj.name 
    armObj.location = (0.0, 0.0, 0.0)
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]
    bpy.ops.object.mode_set(mode='EDIT')

    
    
    
    
    
    for bone in skel.avatar_skeleton:

        
        if bone not in rig_target:
            continue

        newbone = armObj.data.edit_bones.new(bone)
        
        
        

        newbone.head = rig_target[bone]['head_edit'] 
        newbone.tail = rig_target[bone]['tail_edit']

        
        

        
        
        
        

        newbone.matrix = mathutils.Matrix(rig_target[bone]['matrix_edit'])

    
    
    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.mode_set(mode='POSE')
    for bone in rig_target:
        armObj.pose.bones[bone].matrix = mathutils.Matrix(rig_target[bone]['matrix_edit'])

    

    
    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.mode_set(mode='EDIT')

    
    for b in bpy.context.object.data.edit_bones:
        b.select = False
        b.select_head = False   
        b.select_tail = False

    
    for bone in rig_target:
        connected = rig_target[bone]['connected']
        bpy.data.objects[arm].data.edit_bones[bone].use_connect = connected
        parent = rig_target[bone]['parent']
        if parent == "":
            continue
        bpy.data.objects[arm].data.edit_bones[bone].parent = bpy.data.objects[arm].data.edit_bones[parent]

    bpy.ops.object.mode_set(mode='OBJECT')

    
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.group_add()
    obj[arm].pose.bone_groups.active.name = mod_data.rig_group_mbones
    obj[arm].pose.bone_groups.active.color_set = mod_data.rig_group_mtheme
    bpy.ops.pose.group_add()
    obj[arm].pose.bone_groups.active.name = mod_data.rig_group_vbones
    obj[arm].pose.bone_groups.active.color_set = mod_data.rig_group_vtheme

    bpy.context.view_layer.objects.active = obj[arm]
    for bone in rig_target:
        if rig_target[bone]['type'] == 'bone':
            group = mod_data.rig_group_mbones
        else:
            group = mod_data.rig_group_vbones
        obj[arm].pose.bones[bone].bone_group = obj[arm].pose.bone_groups[group]

    bpy.ops.object.mode_set(mode='OBJECT')

    

    
    
    
    
    
    bpy.context.object.data.layers[md.bb_all_bones_layer] = True

    armObj.select_set(True)
    bpy.context.view_layer.objects.active = armObj

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    save_rig(armature=armObj.name)  

    
    
    
    
    

    
    armObj['hide_extended_bones'] = 0
    armObj['hide_face_bones'] = 0
    armObj['hide_hand_bones'] = 0
    armObj['hide_volume_bones'] = 0
    for o in bpy.context.selected_objects:
        o.select_set(False)
    o.select_set(True)

    return armObj








def apply_sl_rotations(armature=""):
    obj = bpy.data.objects

    if armature == "":
        print("apply_sl_rotations reports: nothing to do")
        return False

    
    

    
        
        
        
    
        

    armObj = obj[armature]

    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    armObj.select_set(True)
    bpy.context.view_layer.objects.active = armObj

    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action = 'DESELECT')

    for boneObj in armObj.data.bones:
        bone = boneObj.name
        rot = skel.avatar_skeleton[bone]['rot']

        xrot = math.radians(rot[0])
        yrot = math.radians(rot[1])
        zrot = math.radians(rot[2])

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
    for bone in md.bb_const['bone_roll']:
        if bone not in obj[arm].data.edit_bones:
            continue

        obj[arm].data.edit_bones[bone].select = True
        obj[arm].data.edit_bones[bone].select_head = True
        obj[arm].data.edit_bones[bone].select_tail = True

        obj[arm].data.edit_bones[bone].roll = md.bb_const['bone_roll'][bone]

        obj[arm].data.edit_bones[bone].select = False
        obj[arm].data.edit_bones[bone].select_head = False
        obj[arm].data.edit_bones[bone].select_tail = False

 
    
    
    
    
    
    
    
    
    
    
    
    


    
    

    
    bpy.ops.object.mode_set(mode='OBJECT')


    
    
    
    
        

    

    return True








def force_rig_to_class(armature="", rig_class=""):
    if armature == "" or rig_class == "":
        print("force_rig_to_class reports: nothing to do")
        return False
    obj = bpy.data.objects
    armObj = obj[armature]
    if rig_class == "default":
        print("Convert to default rig")
        rig_target = rd.default
    elif rig_class == "neutral":
        print("Convert to neutral rig")
        rig_target = rd.neutral
    else:
        print("convert_to_class reports: unknown rig class [" + rig_class + "]")
        popup("This is a bug, please report it, check console for details", "Error", "ERROR")
        return False

    old_mode = bpy.context.mode
    if old_mode == "EDIT_ARMATURE":
        old_mode = "EDIT"

    
    
    
    
    
    restore_matrix = False
    if restore_matrix == True:
        matrix_world = armObj.matrix_world.inverted()
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.transform_apply(scale=True, rotation=True, location=False)

    
    bpy.ops.object.mode_set(mode='EDIT')

    
    for boneObj in armObj.data.edit_bones:
        bone = boneObj.name
        name = "m" + bone
        if name in skel.avatar_skeleton:
            armObj.data.edit_bones[bone].head = rig_target[name]['head_edit'] 
            armObj.data.edit_bones[bone].tail = rig_target[name]['tail_edit']
            armObj.data.edit_bones[bone].matrix = mathutils.Matrix(rig_target[name]['matrix_edit'])

    
    for bone in skel.avatar_skeleton:
        armObj.data.edit_bones[bone].head = rig_target[bone]['head_edit'] 
        armObj.data.edit_bones[bone].tail = rig_target[bone]['tail_edit']
        armObj.data.edit_bones[bone].matrix = mathutils.Matrix(rig_target[bone]['matrix_edit'])

    
    for b in bpy.context.object.data.edit_bones:
        b.select = False
        b.select_head = False   
        b.select_tail = False

    
    
    bpy.ops.object.mode_set(mode='OBJECT')

    
    bpy.ops.object.mode_set(mode='POSE')

    for boneObj in armObj.data.edit_bones:
        bone = boneObj.name
        name = "m" + bone
        if name in skel.avatar_skeleton:
            armObj.data.edit_bones[bone].head = rig_target[name]['head_edit'] 
            armObj.data.edit_bones[bone].tail = rig_target[name]['tail_edit']
            armObj.data.edit_bones[bone].matrix = mathutils.Matrix(rig_target[name]['matrix_edit'])

    for bone in rig_target:
        armObj.pose.bones[bone].matrix = mathutils.Matrix(rig_target[bone]['matrix_edit'])

    
    
    bpy.ops.object.mode_set(mode='OBJECT')

    
    bpy.ops.object.mode_set(mode=old_mode)

    
    
    if restore_matrix == True:
        armObj.matrix_world = matrix_world

    return True














def convert_rig_to_class_OLD(armature="", rig_class=""):
    if armature == "" or rig_class == "":
        print("convert_rig_to_class reports: Nothing to do")
        return False
    obj = bpy.data.objects
    armObj = obj[armature]
    if rig_class == "default":
        print("Convert to default rig")
        rig_target = rd.default
    elif rig_class == "neutral":
        print("Convert to neutral rig")
        rig_target = rd.neutral
    else:
        print("convert_to_class reports: unknown rig class [" + rig_class + "]")
        popup("This is a bug, please report it, check console for details", "Error", "ERROR")
        return False

    old_mode = bpy.context.mode
    if old_mode == "EDIT_ARMATURE":
        old_mode = "EDIT"

    
    
    
    
    
    restore_matrix = False
    if restore_matrix == True:
        matrix_world = armObj.matrix_world.inverted()
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.transform_apply(scale=True, rotation=True, location=False)

    
    bpy.ops.object.mode_set(mode='EDIT')

    for bone in skel.avatar_skeleton:
        armObj.data.edit_bones[bone].head = rig_target[bone]['head_edit'] 
        armObj.data.edit_bones[bone].tail = rig_target[bone]['tail_edit']
        armObj.data.edit_bones[bone].matrix = mathutils.Matrix(rig_target[bone]['matrix_edit'])

    
    for b in bpy.context.object.data.edit_bones:
        b.select = False
        b.select_head = False   
        b.select_tail = False

    
    
    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.mode_set(mode='POSE')
    for bone in rig_target:
        armObj.pose.bones[bone].matrix = mathutils.Matrix(rig_target[bone]['matrix_edit'])

    
    
    bpy.ops.object.mode_set(mode='OBJECT')

    
    bpy.ops.object.mode_set(mode=old_mode)

    
    
    if restore_matrix == True:
        armObj.matrix_world = matrix_world

    return True











def convert_rig_to_class(armature=None, rig_class=None, brand="bentobuddy"):

    obj = bpy.data.objects
    armObj = obj[armature]
    bbm = bpy.context.window_manager.bb_misc

    rig_classes = {'pivot', 'pos', 'default', 'neutral', 'male_default', 'male_neutral'}
    old_classes = {'default', 'neutral', 'male_default', 'male_neutral'}

    if rig_class not in rig_classes:
        print("convert_to_class reports: unknown rig class [" + rig_class + "]")
        popup("This is a bug, please report it, check console for details", "Error", "ERROR")
        return False
    else:
        print("Converting rig to class:", rig_class)

    
    nodes = [n.name for n in armObj.data.bones]
    bones = []
    for bone in nodes:
        if armObj.data.bones[bone].use_deform == True:
            bones.append(bone)
    
    print("rigs::convert_to_class : skipping count check")
    if 1 == 0:
    
        print("This is not a complete rig, number of bones:", len(bones))
        print("There's no reason to attempt to confert this to a kit compatible rig when it's not complete.")
        popup("Incomplete rig, see System Console", "Error", "ERROR")
        return False
    
    print("rigs::convert_to_class : skipping name check")
    if 1 == 0:
    
        if bone not in skel.avatar_skeleton:
            print("A bone was encountered that's used for controlling weights and is not part of the SL definition:", bone)
            print("It makes no sense to attempt to make this rig compatible with a kit")
            popup("Incompatible bone found in rig, see System Console", "Error", "ERROR")
            return False


    
    bone_roll = {
    "mHandThumb1Left": 0.7853981852531433,
    "mHandThumb2Left": 0.7853981852531433,
    "mHandThumb3Left": 0.7853981852531433,
    "mHandThumb1Right": -0.7853981852531433,
    "mHandThumb2Right": -0.7853981852531433,
    "mHandThumb3Right": -0.7853981852531433,
    "mHipRight": -0.13089969754219055,
    "mHipLeft": 0.13089969754219055,
    }

    matrix_world = armObj.matrix_world.copy()

    bpy.ops.object.mode_set(mode='EDIT')

    
    connected = {}
    for boneObj in armObj.data.edit_bones:
        connected[boneObj.name] = boneObj.use_connect
        boneObj.use_connect = False

    
    
    
    
    
    

    if rig_class in old_classes:
        if rig_class == "default":
            rig_target = rd.default
        elif rig_class == "neutral":
            rig_target = rd.neutral
        elif rig_class == "male_default":
            rig_target = rd.male_default
        elif rig_class == "male_neutral":
            rig_target = rd.male_neutral
        for boneObj in armObj.data.edit_bones:
            bone = boneObj.name
            if bone not in rig_target:
                continue
            boneObj.matrix = mathutils.Matrix(rig_target[bone]['matrix_edit'])
            boneObj.head = rig_target[bone]['head_edit']
            boneObj.tail = rig_target[bone]['tail_edit']
            boneObj.roll = rig_target[bone]['roll_edit']

        

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    

    elif rig_class == "pivot" or rig_class == "pos":
        
        
        avs = skel.avatar_skeleton
        muV = mathutils.Vector
        absolute = {}
        for bone in avs:
            
            
            if avs[bone]['type'] == 'collision':
                head = muV((avs[bone]['pos']))
            else:
                head = muV((avs[bone][rig_class]))

            has_parent = True
            bone_path = bone
            while(has_parent == True):
                
                parent = avs[bone_path]['parent']
                if parent == "":
                    has_parent = False
                else:
                    head += muV((avs[parent][rig_class]))

                bone_path = parent

            tail = head + muV((avs[bone]['end']))
            absolute[bone] = {}
            absolute[bone]['head'] = head
            absolute[bone]['tail'] = tail
            
                
                

        
        for boneObj in armObj.data.edit_bones:
            bone = boneObj.name
            boneObj.head = absolute[bone]['head']
            boneObj.tail = absolute[bone]['tail']
            
                
                

        
        
        
        if 1 == 1:
            bpy.ops.object.mode_set(mode='OBJECT')
            loc, rot, scale = armObj.matrix_world.decompose()
            smat = mathutils.Matrix()
            for i in range(3):
                smat[i][i] = scale[i]
            eu = mathutils.Euler(map(math.radians, (0, 0, -90)), 'XYZ')
            mat = mathutils.Matrix.Translation(loc) @ eu.to_matrix().to_4x4() @ smat
            armObj.matrix_world = mat
            bpy.ops.object.transform_apply( rotation=True, location=False, scale=False )
            bpy.ops.object.mode_set(mode='EDIT')

    
    for bone in connected:
        armObj.data.edit_bones[bone].use_connect = connected[bone]

    for boneObj in armObj.data.edit_bones:
        if boneObj.name in bone_roll:
            boneObj.roll = bone_roll[boneObj.name]
        else:
            boneObj.roll = 0.0

    
    for b in armObj.data.edit_bones:
        b.select = False
        b.select_head = False   
        b.select_tail = False

    bpy.ops.object.mode_set(mode='OBJECT')
    armObj.matrix_world = matrix_world

    
    
    armObj['rig_class'] = rig_class
    armObj[brand] = True 

    
    
    save_rig(armature=armObj.name, force=True)

    return True







def update(type="soft"):
    if type == "soft":
        bpy.context.view_layer.update()
    elif type == "hard":
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update() 
    else:
        print("update reports: unknown type")
        return False
    return True






def update_frame(frame=None):
    if frame == None:
        print("update_frame reports: no frame")
        return False
    bpy.context.scene.frame_set(last_start)
    return True







def fix_rig_orientation(armature="", bone=""):
    if armature == "" or bone == "":
        print("fix_rig_orientation reports: required parameter missing", armature, bone)
        return False

    obj = bpy.data.objects
    armObj = obj[armature]

    old_mode = bpy.context.mode
    if old_mode == "EDIT_ARMATURE":
        old_mode = "EDIT"

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = armObj

    matrix_bone = worldMatrix(armature=armature, bone=bone)

    
    
    
    

    
    l_arm, r_arm, s_arm = armObj.matrix_world.decompose()
    
    r_bone = matrix_bone.to_quaternion()

    
    scale = mathutils.Matrix()
    for i in range(3):
        scale[i][i] = s_arm[i]

    
    rmat4 = r_bone.to_matrix().to_4x4()

    
    rotI = rmat4.inverted()
    
    eu = mathutils.Euler(map(math.radians, (90, 0, 0)), 'XYZ')
    
    rot90neg = eu.to_matrix().to_4x4()
    
    rot = rot90neg @ rotI

    
    loc = mathutils.Matrix.Translation(l_arm)

    
    mat = loc @ rot @ scale

    
    
    bpy.ops.object.transform_apply( rotation=True, location=False, scale=False )

    armObj.matrix_world = mat

    
    bpy.ops.object.transform_apply( rotation=True, location=False, scale=False )
    bpy.ops.object.mode_set(mode=old_mode)

    return True




def set_angle(armature="", angle=[0,0,0]):
    if armature == "":
        print("rigs.save_orientation reports: I need a rig")
        return False
    restore = True
    if len(bpy.context.selected_objects) == 0:
        restore = False
    else:
        bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
        old_mode = bpy.context.mode
        if old_mode == 'EDIT_ARMATURE': old_mode = 'EDIT'

    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    armObj = bpy.data.objects[armature]

    for o in bpy.context.selected_objects:
        o.select_set(False)

    armObj.select_set(True)
    bpy.context.view_layer.objects.active = armObj

    loc, rot, scale = armObj.matrix_world.decompose()
    smat = mathutils.Matrix()
    for i in range(3):
        smat[i][i] = scale[i]


    eu = mathutils.Euler(map(math.radians, angle), 'XYZ')
    mat = mathutils.Matrix.Translation(loc) @ eu.to_matrix().to_4x4() @ smat
    armObj.matrix_world = mat

    bpy.ops.object.transform_apply( rotation=True, location=False, scale=False )

    if restore == True:
        bpy.ops.object.mode_set(mode=old_mode)

    return True






def worldMatrix(armature="", bone=""):
    ArmatureObject = bpy.data.objects[armature]
    Bone = ArmatureObject.pose.bones[bone]
    _bone = ArmatureObject.pose.bones[bone]
    _obj = ArmatureObject
    return _obj.matrix_world @ _bone.matrix







def save_hide_state(armature=""):
    obj = bpy.data.objects
    bbm = bpy.context.window_manager.bb_misc
    armObj = obj[armature]
    state = get_unique_name()
    
    if bbm.get('hide_states') == None:
        bbm['hide_states'] = dict()
    else:
        if state in bbm['hide_states']:
            print("save_hidden_states reports: state collision -", state)

    bbm['hide_states'][state] = dict()
    bbm['hide_states'][state]['hide'] = dict()
    bbm['hide_states'][state]['hide_select'] = dict()
    bbm['hide_states'][state]['layers'] = list()

    layers = list()
    for h in range(len(armObj.data.layers)):
        layers.append(armObj.data.layers[h])
        armObj.data.layers[h] = True
    bbm['hide_states'][state]['layers'] = layers

    
    
    for boneObj in armObj.data.bones:
        bbm['hide_states'][state]['hide_select'][boneObj.name] = boneObj.hide_select
        boneObj.hide_select = False
        bbm['hide_states'][state]['hide'][boneObj.name] = boneObj.hide
        boneObj.hide = False

    bbm['hide_states'][state]['armature'] = armature

    print("save_hidden_states reports: total states -", len(bbm['hide_states']))
    return state

def restore_hide_state(state):
    obj = bpy.data.objects
    bbm = bpy.context.window_manager.bb_misc
    if state not in bbm['hide_states']:
        print("restore_hide_state reports: state doesn't exist -", state)
        return False
    if state not in bbm['hide_states']:
        print("restore_state reports: state doesn't exist -", state)
        return False

    arm = bbm['hide_states'][state]['armature']
    armObj = obj[arm]

    for bone in bbm['hide_states'][state]['hide']:
        armObj.data.bones[bone].hide = bbm['hide_states'][state]['hide'][bone]
        armObj.data.bones[bone].hide_select = bbm['hide_states'][state]['hide_select'][bone]

    layers = bbm['hide_states'][state]['layers'].to_list()
    for h in range(len(layers)):
        armObj.data.layers[h] = layers[h]

    del bbm['hide_states'][state]

    return True







def get_armature_name(arm=None):
    print("rigs::get_armature_name : returns bpy.data.objects[" + arm + "].data.name")
    return bpy.data.objects[arm].data.name

get_rig_name = get_armature_name
get_rig = get_rig_name
rig_name = get_rig





def teflon(armature=None):

    bb = bpy.context.scene.bentobuddy
    animation_start_frame = bb.animation_start_frame
    animation_end_frame = bb.animation_end_frame
    bb_anim = bpy.context.scene.bb_anim
    frame_step = bb_anim.bake_frame_step
    old_mode = bpy.context.mode
    if old_mode == "EDIT_ARMATURE":
        old_mode = "EDIT"

    bpy.data.objects[armature].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[armature]
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.nla.bake(
        frame_start=animation_start_frame,
        frame_end=animation_end_frame,
        step=frame_step,
        only_selected=False,
        visual_keying=True,
        clear_constraints=True,
        clear_parents=False,
        use_current_action=True,
        bake_types={'POSE'},
        )
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.ops.object.mode_set(mode=old_mode)
    return True





























def save_rig(armature="", force=False):
    if armature == "":
        print("rigs::save_rig reports: nothing to do")
        return False

    armObj = bpy.data.objects[armature]

    if armObj.get('rig_data') != None:
        if force == False:
            print("rig_data exists already, use (force) to overwrite")
            return False
        else:
            print("rig_data exists but force is enabled, saving...")

    bpy.context.view_layer.objects.active = armObj

    
    
    bpy.context.view_layer.update()

    
    rig_data = dict()
    for boneObj in armObj.data.bones:
        rig_data[boneObj.name] = {}

    
    bpy.ops.object.mode_set(mode='EDIT')
    for eBone in armObj.data.edit_bones:
        bone = eBone.name
        rig_data[bone]["emat"] = eBone.matrix.copy()
        rig_data[bone]["roll"] = eBone.roll
        rig_data[bone]["head"] = eBone.head.copy() 
        rig_data[bone]["tail"] = eBone.tail.copy()
        rig_data[bone]["use_connect"] = eBone.use_connect

    bpy.ops.object.mode_set(mode='OBJECT')
    
    
    
    
    
    for pBone in armObj.pose.bones:
        dBone = pBone.bone
        bone = dBone.name

        rig_data[bone]["dmat"] = dBone.matrix.copy()
        rig_data[bone]["head_local"] = dBone.head_local.copy()
        rig_data[bone]["tail_local"] = dBone.tail_local.copy()
        rig_data[bone]["matrix_local"] = dBone.matrix_local.copy()

        
            
            
                

        rig_data[bone]["pmat"] = pBone.matrix.copy()
        rig_data[bone]["pmatb"] = pBone.matrix_basis.copy() 
        rig_data[bone]["pmatc"] = pBone.matrix_channel.copy()

    
    
    
    
    
    
    
    
    armObj['rig_data'] = rig_data
 



    return True





def get_rig_data(armObj):
    rig_data = {}
    for boneObj in armObj.data.bones:
        rig_data[boneObj.name] = {}
        rig_data[boneObj.name]['matrix_local'] = boneObj.matrix_local.copy()
    return rig_data






def restore_rig(arm):
    obj = bpy.data.objects
    if arm not in obj:
        print("The object", arm, "is not in the scene, can't restore")
        return False

    if obj[arm].type != 'ARMATURE':
        print("The object", arm, "is not an armature, can't restore")
        return False

    if obj[arm].get('rig_data') == None:
        print("Rig not frozen:", arm)
        return False

    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    for o in bpy.context.selected_objects:
        o.select_set(False)

    armObj = bpy.data.objects[arm]
    armObj.select_set(True)
    bpy.context.view_layer.objects.active = armObj

    rig_data = armObj['rig_data'].to_dict()

    
    bpy.ops.object.mode_set(mode='EDIT')

    
    for boneObj in armObj.data.edit_bones:
        boneObj.use_connect = False
    
    for boneObj in armObj.data.edit_bones:
        bone = boneObj.name
        boneObj.head = rig_data[bone]['head']
        boneObj.tail = rig_data[bone]['tail']
        boneObj.use_connect = rig_data[bone]['use_connect']
        boneObj.matrix = mathutils.Matrix(rig_data[bone]['emat'])
        boneObj.roll = rig_data[bone]['roll']

    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='POSE')

    
    for boneObj in armObj.pose.bones:
        boneObj.matrix = mathutils.Matrix(rig_data[boneObj.name]['pmat'])

    bpy.ops.object.mode_set(mode='OBJECT')

    return True



def restore_rig_from_map(armature=None, rig_data=None):
    """Send a map with head, tail, roll and use_connect
defined for each bone or let the function extract the
rig_data from the object and use that"""

    obj = bpy.data.objects
    armObj = obj[armature]
    if rig_data == None:
        rig_data = armObj.get('rig_data')
        if rig_data == None:
            print("No rig data delivered and none on the object")
            return False
    for o in bpy.context.selected_objects:
        o.select_set(False)
    armObj.select_set(True)
    bpy.context.view_layer.objects.active = armObj

    bpy.ops.object.mode_set(mode='POSE')
    
    bpy.ops.pose.armature_apply()
    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.mode_set(mode='EDIT')
    
    for boneObj in armObj.data.edit_bones:
        boneObj.use_connect = False
    
    for boneObj in armObj.data.edit_bones:
        bone = boneObj.name
        boneObj.head = rig_data[bone]['head']
        boneObj.tail = rig_data[bone]['tail']
        boneObj.roll = rig_data[bone]['roll']
    
    for boneObj in armObj.data.edit_bones:
        bone = boneObj.name
        boneObj.use_connect = rig_data[bone]['use_connect']
    bpy.ops.object.mode_set(mode='OBJECT')

    return True




def to_deg(mat):
    eu = mat.to_euler()
    return [math.degrees(round(a, 4)) for a in eu]










def write_bind_data(arm):
    rig_data = bpy.context.object['rig_data'].to_dict()
    fd = "bind_data.py"
    formatted = "# Generated by Bento Buddy\n"
    formatted += "rig_data = {\n"

    for bone in rig_data:
        formatted += '    "' + bone + '": {\n'
        for bkey in rig_data[bone]:
            formatted += '        "' + bkey + '": ' + str(rig_data[bone][bkey]) + ",\n"
        formatted += "    },\n"
    formatted += "}\n"

    f = open(fd, "w", encoding='UTF8')
    f.write(formatted)
    f.close()
    print("done writing bone data")
    return












def get_bone_prefix():
    
    if len(bpy.context.selected_objects) != 1:
        return ""
    if bpy.context.selected_objects[0].type != 'ARMATURE':
        return ""
    armObj = bpy.context.selected_objects[0]

    
    check_prefix = list()
    for boneObj in armObj.data.bones:
        check_prefix.append(boneObj.name)
    
    
    if len(check_prefix) == 0:
        return "" 
    prefix_len = len(check_prefix[0])
    for bone in check_prefix[1 : ]:
        prefix_len = min(prefix_len, len(bone))
        while not bone.startswith(check_prefix[0][ : prefix_len]):
            prefix_len -= 1
    prefix = check_prefix[0][ : prefix_len]
    return prefix





def rebind(arm, report=False):
    armObj = arm
    if isinstance(arm, str):
        armObj = bpy.data.objects[arm]

    state = utils.get_state()
    frame_start, frame_end = animutils.get_frame_range(armObj, start=True)
    mesh_list = get_associated_mesh(armObj, report=True)
    if mesh_list == False:
        if report == True:
            print("rigs::rebind reports : get_associated_mesh returned a False, no mesh found")
        utils.set_state(state)
        return False

    utils.make_single(armObj)
    armObj.animation_data_clear()

    
    
    select_error = []
    for meshObj in mesh_list:
        meshObj.select_set(True)

        
        is_selected = meshObj.select_get()
        if is_selected == False:
            select_error.append(meshObj)
            continue

        utils.activate(meshObj)
        utils.make_single(meshObj)
        
        if meshObj.data.shape_keys:
            bpy.ops.object.shape_key_add(from_mix=False)
            for k in meshObj.data.shape_keys.key_blocks:
                meshObj.shape_key_remove(k)
        
        
        for modObj in meshObj.modifiers:
            if modObj.type == 'ARMATURE':
                modObjCopy = bpy.ops.object.modifier_copy(modifier=modObj.name)

            
            
            try:
                if report == True:
                    print("B28-rigs::rebind[Attempting to apply modifiers]", meshObj.name)
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modObj.name)
            except Exception as e:
                txt = traceback.format_exc()
                if report == True:
                    print(txt)
                    print("B28-Failed!")
                    print("B29-rigs::rebind[Attempting to apply modifiers]", meshObj.name)
                try:
                    bpy.ops.object.modifier_apply(modifier=modObj.name)
                    if report == True:
                        print("Success for Blender 2.9")

                except Exception as e:
                    txt = traceback.format_exc()
                    if report == True:
                        print(txt)
                        if meshObj.select_get() == False:
                            print("rigs::rebind reports : An important object could not be selected:", meshObj.name)
                        print("rigs::rebind reports : rebind failed for Blender 2.9")
                        popup("Rebind Failed", "Fatal Error", "ERROR")

        meshObj.select_set(False)

    if len(select_error) > 0:
        if report == True:
            print("Some objects could not be processed because they are not selectable, below is a list of those items")
            for o in select_error:
                print(" -", o.name)
            pop_text = "Error selecting objects\n\n"
            pop_text += "Some objects could not be processed because they were not selectable.\n"
            pop_text += "Please bring up the (System Console) not the (Python Console) in order\n"
            pop_text += "to see which objects are affected by this.  If you see an excessive\n"
            pop_text += "amount of errors then this is most likely an Avastar issue and you may\n"
            pop_text += "be able to resolve it by using the tool (Remove Unusable Controllers)\n"
            pop_text += "that you can find in the (Rig Tools) area.  After using that tool try\n"
            pop_text += "the (rebind) again and note the errors produced.  Unhide and make\n"
            pop_text += "selectable the indicated objects in order to proceed.  It's possible\n"
            pop_text += "that these objects are not usable but because they are associated with\n"
            pop_text += "the armature they were not processed and are effectively damaged by the\n"
            pop_text += "attempt.  Noting this you'll want to load a known good file, do not\n"
            pop_text += "save this Blend file.\n"
            pop_text += "\n"
            utils.popup(pop_text, "Error", "ERROR")

    armObj.select_set(True)
    utils.activate(armObj)
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.armature_apply()
    bpy.ops.object.mode_set(mode='OBJECT')

    utils.set_state(state)

    return True





















def get_bind_data(armature=None, bone=None, rig_data=None):
    if armature == None:
        print("get_bind_data reports: no armature")
        return False

    if bone == None:
        print("get_bind_data reports: no bone")
        return False

    
    
    
    
    
    
    
    if rig_data == None:
        print("get_bind_data reports: no rig_data")
        return False

    obj = bpy.data.objects
    armObj = obj[armature]
    dBone = armObj.data.bones[bone]

    
    
    
    
    
    

    
    
    
    
    
    

    bb_devkit = bpy.context.scene.bb_devkit
    use_offset_location = bb_devkit.use_offset_location
    use_offset_rotation = bb_devkit.use_offset_rotation
    use_offset_scale = bb_devkit.use_offset_scale

    rotate_for_sl = bb_devkit.rotate_for_sl

    process_volume_bones = bb_devkit.process_volume_bones
    volume_bone_location = bb_devkit.volume_bone_location
    volume_bone_rotation = bb_devkit.volume_bone_rotation
    volume_bone_scale = bb_devkit.volume_bone_scale

    
    
    
        
        
        
        
        
    
        

    transforms = {}
    transforms[bone] = dict()
    transforms[bone]['global'] = dict()

    
    
    
    
    
    if rotate_for_sl == True:
        R90 = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Z')
    else:
        R90 = mathutils.Matrix.Rotation(math.radians(0.0), 4, 'Z')
    R90I = R90.inverted()

    
    
    
    
    dmg = mathutils.Matrix(rig_data[bone]['matrix_local'])

    
    
    
    





    
    
    
    
    
    
    
    
    
    
    if 1 == 1:
    
    
        
        
        
        matI = dmg.inverted()
        
        matI = matI @ dmg.inverted()
        

        l = matI.to_translation()
        L = mathutils.Matrix.Translation(l)
        dmg = dmg @ L









    
    
    
    

    dmgI = dBone.matrix_local @ dmg.inverted()
    dmgI = dmgI @ R90I
    dmgI = R90 @ dmgI

    
    
    
    
    
    
    if 1 == 0:
    
        print("dmgI before:")
        print(dmgI)
        OM = armObj.matrix_world.copy()
        OM = R90 @ OM
        OM = OM @ R90I
        dmgI = dmgI @ OM

        print("dmgI after :")
        print(dmgI)

    
    
    transforms[bone]['global']['matrix'] = dmgI

    if use_offset_location == True:
        l = dBone.head_local.copy()
    else:
        l = mathutils.Matrix(rig_data[bone]['matrix_local']).to_translation()

    L = mathutils.Matrix.Translation(l)

    R = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Z')
    RI = R.inverted()
    L = R @ L

    
    l = L.to_translation()
    L = mathutils.Matrix.Translation(l)
    l = L.to_translation()
    L = mathutils.Matrix.Translation(l)

    
    r = skel.avatar_skeleton[bone]['rot']  
    s = [ a for a in skel.avatar_skeleton[bone]['scale'] ] 


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    if get_rig_class() == "":

        
        
        
        
        
        
        if 1 == 0:
            if process_volume_bones == True:
                if volume_bone_rotation == True:
                    r = skel.avatar_skeleton[bone]['rot']  
                if volume_bone_scale == True:
                    s = [ a for a in skel.avatar_skeleton[bone]['scale'] ] 







    
    
    
        
            
                

    
    




    
    
    
    
    
    
    
    
    
    
    l_ofs, r_ofs, s_ofs = transforms[bone]['global']['matrix'].decompose()
    

    
    
    
    

    
    
    if 1 == 0:
        L = mathutils.Matrix.Translation(l)

    
    
    
    rot = [math.radians(a) for a in r] 
    R_mat = mathutils.Euler(rot,'XYZ').to_matrix().to_4x4()

    
    
    R_ofs = r_ofs.to_matrix().to_4x4()

    
    
    
    
    
    
    
    
    
    
    S = mathutils.Matrix()
    
    for i in range(3):
        
        S[i][i] = s[i]




    if use_offset_scale == True:
        s = armObj.pose.bones[bone].scale
        for i in range(3):
            S[i][i] = s[i]




    
    R = R_mat @ R_ofs
    

    
    M = L @ R @ S

    transforms[bone]['bind_data'] = M

    
    
    return transforms




















def get_joint_data(armature=None, bone=None, rig_data=None):
    if armature == None:
        print("get_joint_data reports: no armature")
        return False
    if rig_data == None:
        print("get_joint_data reports: no rig_data")
        return False
    if bone == None:
        print("get_joint_data reports: no bone")
        return False
    obj = bpy.data.objects
    armObj = obj[armature]
    dBone = armObj.data.bones[bone]

    
    
    
    
    bb_devkit = bpy.context.scene.bb_devkit
    use_offset_location = bb_devkit.use_offset_location
    use_offset_rotation = bb_devkit.use_offset_rotation
    use_offset_scale = bb_devkit.use_offset_scale
    rotate_for_sl = bb_devkit.rotate_for_sl

    
    
    
    
    
    
    
    
    process_volume_bones = bb_devkit.process_volume_bones

    transforms = {}
    transforms[bone] = {}

    
    
    tr_bone = get_bind_data(armature=armature, bone=bone, rig_data=rig_data)

    pbone = None

    if dBone.parent:
        pbone = dBone.parent.name

    
    
    
    
    
    
    
    
    
    
    

    
    
    
    if pbone in skel.avatar_skeleton:
        tr_parent = get_bind_data(armature=armature, bone=pbone, rig_data=rig_data)
        CBP = mathutils.Matrix(tr_bone[bone]['bind_data'])
        PBP = mathutils.Matrix(tr_parent[pbone]['bind_data'])
        M = PBP.inverted() @ CBP
        transforms[bone]['joint_data'] = M

    
    
    
    

    else:
        
        
        
        
        
        
        
        
        M = dBone.matrix_local.copy()

        
        l, r, s = M.decompose()
        L = mathutils.Matrix.Translation(l)
        R = mathutils.Matrix() 
        S = mathutils.Matrix()

        for i in range(3):
            S[i][i] = s[i]

        M = L @ R @ S

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        if rotate_for_sl == True:
            R90 = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Z')
        else:
            R90 = mathutils.Matrix.Rotation(math.radians(0.0), 4, 'Z')
        R90I = R90.inverted()

        
        
        
        
        if bone == 'mPelvis':
            L = R90 @ L
            L = L @ R90I
            
            
            M = L @ R @ S

            
            
            
            if 1 == 0:
                M = dBone.matrix_local.copy()

                l, r, s = M.decompose()
                L = mathutils.Matrix.Translation(l)
                R = r.to_matrix().to_4x4()
                S = mathutils.Matrix()
                for i in range(3):
                    S[i][i] = s[i]

                L = R90 @ L
                L = L @ R90I
                
                M = L @ R @ S

            if 1 == 0:
                M = dBone.matrix_local.copy()
                l, r, s = M.decompose()
                R = r.to_matrix().to_4x4()
                S = mathutils.Matrix()
                for i in range(3):
                    S[i][i] = s[i]
                L = mathutils.Matrix.Translation((0,0,0))
                M = L @ R @ S

        
        
        
        
        

        
        
        
        
        
        
        
        
        
        
        if 1 == 0:
            R90 = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Z')
            R90I = R90.inverted()
            OM = armObj.matrix_world.copy()
            OM = R90 @ OM
            OM = OM @ R90I
            M = M @ OM



        transforms[bone]['joint_data'] = M

    
    
    
    
    return transforms





























def get_bone_transforms(armature=None, rig_data=None):
    if armature == None:
        return False
    if rig_data == None:
        return False

    
    
    
    

    bb_devkit = bpy.context.scene.bb_devkit
    use_offset_location = bb_devkit.use_offset_location
    use_offset_rotation = bb_devkit.use_offset_rotation
    use_offset_scale = bb_devkit.use_offset_scale
    rotate_for_sl = bb_devkit.rotate_for_sl


    obj = bpy.data.objects

    if armature not in obj:
        print("Armature doesn't exist or is not available in the scene")
        return False
    if obj[armature].type != 'ARMATURE':
        print("The intended object is not an armature")
        return False

    
    
    
    
    
    
    
    
        
    
        

    R90 = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Z')
    R90I = R90.inverted()

    armObj = obj[armature]
    transforms = {}

    for pBone in armObj.pose.bones:
        dBone = pBone.bone
        bone = pBone.name

        if bone not in skel.avatar_skeleton:
            continue

        transforms[bone] = dict()
        transforms[bone]['global'] = dict()
        transforms[bone]['local'] = dict()

        
        
        
        
        dmg = mathutils.Matrix(rig_data[bone]['matrix_local'])

        
        
        
        
        dmgI = dBone.matrix_local @ dmg.inverted()

        
        
        
        
        
        
        dmgI = dmgI @ R90I
        dmgI = R90 @ dmgI
        transforms[bone]['global']['matrix'] = dmgI

        
        
        
        
        






        
        
        
        
        
        
        if bone in volumes.vol_joints:
            l = skel.avatar_skeleton[bone]['pos']
        else:
            l = skel.avatar_skeleton[bone]['absolute_pivot']
        r = skel.avatar_skeleton[bone]['rot']  
        s = skel.avatar_skeleton[bone]['scale'] 

        
        
        
        
        
        if use_offset_location == True:
            
            L_SKEL = mathutils.Matrix.Translation(l)
            L = mathutils.Matrix.Translation(l)
            M_OFF = transforms[bone]['global']['matrix']
            L = M_OFF @ L_SKEL
            
            
            l = L.to_translation()
        else:
            
            l = dBone.head_local.copy()
            
            
            L = mathutils.Matrix.Translation(l)

            
            
            
            
            
            
            

            L = R90 @ L

            
            
            
            
            l = L.to_translation()

        
        
        
        l_ofs, r_ofs, s_ofs = transforms[bone]['global']['matrix'].decompose()
        
        L_mat = mathutils.Matrix.Translation(l)
        L_ofs = mathutils.Matrix.Translation(l_ofs)

        
        
        
        rot = [math.radians(a) for a in r] 
        R_mat = mathutils.Euler(rot,'XYZ').to_matrix().to_4x4()

        
        
        
        if use_offset_rotation == True:
            
            R_ofs = r_ofs.to_matrix().to_4x4()
        else:
            
            R_ofs = mathutils.Euler((0,0,0),'XYZ').to_matrix().to_4x4()

        
        S_mat = mathutils.Matrix()
        S_ofs = mathutils.Matrix()
        for i in range(3):
            S_mat[i][i] = s[i]
        
        
        






        if use_offset_scale == True:
            
            
            
            
            if 1 == 0:
                
                for i in range(3):
                    S_ofs[i][i] = s_ofs[i]
            else:
                
                s = pBone.scale.copy()

                print("s:", s)
                print("S_ofs:", S_ofs)

                for i in range(3):
                    S_ofs[i][i] = s[i]




        
        
        R90y = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Y')
        R90yI = R90y.inverted()
        

        
        
        
        
        
        
        
        L = L_mat
        R = R_mat @ R_ofs
        S = S_mat @ S_ofs






        if use_offset_scale == True:
            S = S_ofs




        
        transforms[bone]['bind_data'] = L @ R @ S





        
        
        

        
        
        
        
        
        
        
        

        if dBone.parent and bone != 'mPelvis':
        
        
            parent = dBone.parent.name

            
            OM = mathutils.Matrix(rig_data[bone]['matrix_local'])
            OMP = mathutils.Matrix(rig_data[parent]['matrix_local'])

            
            
            
            OMG = OM @ OMP.inverted()

            
            CM = dBone.matrix_local.copy()
            CMP = dBone.parent.matrix_local.copy()

            
            
            CMO = CM @ OM.inverted()

            
            
            
            
            
            
            
            
            
            

            
            CMPO = CMP @ OMP.inverted()

            
            
            
            
            CML = CMPO.inverted() @ CMO













            
            
            

            
            if bone in volumes.vol_joints:
                l = skel.avatar_skeleton[bone]['pos']
                r = skel.avatar_skeleton[bone]['rot']
                s = skel.avatar_skeleton[bone]['scale']
                rot = [math.radians(a) for a in r] 
                R = mathutils.Euler(rot,'XYZ').to_matrix().to_4x4()

            else:
                
                r = CML.to_quaternion()
                R_mat = r.to_matrix().to_4x4()

                
                
                
                
                
                
                R = R_mat @ R90I
                R = R90 @ R

                
                
                l = skel.avatar_skeleton[bone]['pivot']
                s = R.to_scale()

            
            
            L = mathutils.Matrix.Translation(l)

            
            S = mathutils.Matrix()
            for i in range(3):
                S[i][i] = s[i]






            if use_offset_scale == True:
                S = S_ofs




            
            M = L @ R @ S

            
            transforms[bone]['local']['matrix'] = M

        
        
        
        
        
        
        else:
            
            
            if 1 == 0:
                
                OM = mathutils.Matrix(bind_data.rig_data[bone]['matrix_local'])
                OM = ms[bone]
                
                CM = dBone.matrix_local.copy()
                
                MO = CM @ OM.inverted()
                MO = OM.inverted() @ CM

            
            
            
            

            
            
            
            
            M = dBone.matrix_local.copy()
            
            l, r, s = M.decompose()
            L = mathutils.Matrix.Translation(l)
            R = mathutils.Matrix() 
            S = mathutils.Matrix()
            for i in range(3):
                S[i][i] = s[i]
            MF = L @ R @ S
            transforms[bone]['local']['matrix'] = MF
            
            
            transforms[bone]['joint_data'] = MF

    return transforms







def pose_bone(boneObj=None, axis='Z', angle=10):
    if boneObj == None:
        print("rigs::pose_bone reports: No bone object")
        return False
    rm = boneObj.rotation_mode
    boneObj.rotation_mode = 'XYZ'
    boneObj.rotation_euler.rotate_axis(axis, math.radians(angle))
    boneObj.rotation_mode = rm
    return True




def reset_pose(armature=None, location=False, rotation=True, scale=False, space="rig", bone=None):
    obj = bpy.data.objects
    arm = armature
    r = mathutils.Quaternion((0, 0, 0), 1 )
    s = mathutils.Vector((1,1,1))
    if space == "rig":
        for pBone in obj[arm].pose.bones:
            dBone = pBone.bone
            if location == True:
                pBone.location = dBone.head.copy()
            if rotation == True:
                rotation_mode = pBone.rotation_mode
                pBone.rotation_mode = 'QUATERNION'
                pBone.rotation_quaternion = r
                pBone.rotation_mode = rotation_mode
            if scale == True:
                pBone.scale = s
    elif space == "bone":
        pBone = obj[arm].pose.bone[bone]
        dBone = pBone.bone
        if location == True:
            pBone.location = dBone.head.copy()
        if rotation == True:
            rotation_mode = obj[arm].pose.bones[bone].rotation_mode
            obj[arm].pose.bones[bone].rotation_mode = 'QUATERNION'
            obj[arm].pose.bones[bone].rotation_quaternion = r
            obj[arm].pose.bones[bone].rotation_mode = rotation_mode
        if scale == True:
            obj[arm].pose.bones[bone].scale = s
    else:
        print("rigs::reset_pose reports: unknown directive - ", space)
        return False

    return True




def popup(message = "", title = "Message Box", icon =  'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
    return



def remove_deps(armature=None):
    obj = bpy.data.objects
    armObj = armature
    if isinstance(armature, str):
        armObj = obj[armature]
    for pBone in armObj.pose.bones:
        for pbC in pBone.constraints:
            pBone.constraints.remove(pbC)
    try:
        fcurves = armObj.animation_data.drivers
        for fc in fcurves:
            fcurves.remove(fc)
    except:
        print("No drivers, moving on")
    armObj.animation_data_clear()
    return True








def attach_slave_rig(
    armature=None, detach=False, remove_parent=False, use_offset=False,
    rig_class="pos", target_space="LOCAL", owner_space="LOCAL"):

    obj = bpy.data.objects
    master = armature
    masterObj = obj[master]
    selected = [o for o in bpy.context.selected_objects]
    active = bpy.context.active_object
    old_mode = bpy.context.mode

    if old_mode.startswith('EDIT'):
        old_mode = 'EDIT'
    if old_mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    for o in bpy.context.selected_objects:
        o.select_set(False)

    
    
    
    
    slaveObj = create_rig(target="neutral")
    if slaveObj == False:
        print("create_rig() failed")
        return False
    slave = slaveObj.name
    result = convert_rig_to_class(armature=slave, rig_class=rig_class)
    if result == False:
        print("convert_rig_class_to() failed")
        return False

    slaveObj.select_set(True)
    bpy.context.view_layer.objects.active = slaveObj

    slaveObj.data.display_type = 'OCTAHEDRAL'
    slaveObj.show_in_front = False

    
    if detach:
        bpy.ops.object.mode_set(mode='EDIT')
        for boneObj in slaveObj.data.edit_bones:
            boneObj.use_connect = False
        bpy.ops.object.mode_set(mode='OBJECT')

    
    
    
    
    
    
    if remove_parent:
        bpy.ops.object.mode_set(mode='EDIT')
        for boneObj in masterObj.data.edit_bones:
            boneObj.parent = None

    masterObj.data.display_type = 'STICK'
    masterObj.show_in_front = True

    
    for g in obj[slave].pose.bone_groups:
        obj[slave].pose.bone_groups.remove(g)

    bpy.ops.object.mode_set(mode='POSE')

    
    bpy.ops.pose.group_add()
    slaveObj.pose.bone_groups.active.name = mod_data.slave_group_name
    slaveObj.pose.bone_groups.active.color_set = mod_data.slave_group_theme
    
    for boneObj in slaveObj.pose.bones:
        boneObj.bone_group = slaveObj.pose.bone_groups[mod_data.slave_group_name]

    lname = "BB Copy Loc"
    rname = "BB Copy Rot"
    sname = "BB Copy Sca"




    
    bone_list = []
    for boneObj in obj[slave].pose.bones:
        if boneObj.name in obj[master].pose.bones:
            bone_list.append(boneObj)

    for boneObj in bone_list:
        sbone = boneObj.name
        obj[slave].data.bones.active = obj[slave].data.bones[sbone]
        bc = obj[slave].pose.bones[sbone].constraints
        bc.new('COPY_LOCATION')
        bc['Copy Location'].target = masterObj
        bc['Copy Location'].subtarget = sbone
        bc['Copy Location'].target_space = target_space
        bc['Copy Location'].owner_space = owner_space
        bc['Copy Location'].influence = 1
        bc['Copy Location'].name = lname
    for boneObj in bone_list:
        sbone = boneObj.name
        obj[slave].data.bones.active = obj[slave].data.bones[sbone]
        bc = obj[slave].pose.bones[sbone].constraints
        bc.new('COPY_ROTATION')
        bc['Copy Rotation'].target = masterObj
        bc['Copy Rotation'].subtarget = sbone
        bc['Copy Rotation'].target_space = target_space
        bc['Copy Rotation'].owner_space = owner_space
        bc['Copy Rotation'].influence = 1
        bc['Copy Rotation'].name = rname
    for boneObj in bone_list:
        sbone = boneObj.name
        obj[slave].data.bones.active = obj[slave].data.bones[sbone]
        bc = obj[slave].pose.bones[sbone].constraints
        bc.new('COPY_SCALE')
        bc['Copy Scale'].target = masterObj
        bc['Copy Scale'].subtarget = sbone
        bc['Copy Scale'].target_space = target_space
        bc['Copy Scale'].owner_space = owner_space
        bc['Copy Scale'].influence = 1
        bc['Copy Scale'].name = sname

    
    bpy.ops.object.mode_set(mode='OBJECT')

    
    
    obj[slave].select_set(False)
    for o in selected:
        o.select_set(True)
    if active != None:
        bpy.context.view_layer.objects.active = active
        bpy.ops.object.mode_set(mode=old_mode)

    return slaveObj






def attach_proxy_rig(armature=None, clean=False):

    sarm = armature

    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    for o in bpy.context.selected_objects:
        o.select_set(False)

    obj = bpy.data.objects
    sarmObj = obj[sarm]
    sarmObj.select_set(True)
    bpy.context.view_layer.objects.active = sarmObj

    sarmObj.data.display_type = 'OCTAHEDRAL'
    sarmObj.show_in_front = False

    
    if 1 == 0:
        bpy.ops.object.mode_set(mode='EDIT')
        for boneObj in sarmObj.data.edit_bones:
            boneObj.use_connect = False
        bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.duplicate()
    glueObj = bpy.context.object
    glueObj.name = "BentoBuddy_Controller"
    glue = glueObj.name

    glueObj.data.display_type = 'STICK'
    glueObj.show_in_front = True

    
    if clean == True:
        remove_deps(armature=sarmObj)

    
    if 1 == 0:
        bpy.ops.object.mode_set(mode='EDIT')
        for boneObj in glueObj.data.edit_bones:
            boneObj.parent = None

    
    bpy.ops.object.mode_set(mode='POSE')
    for b in obj[glue].pose.bones:
        for c in b.constraints:
            b.constraints.remove(c)
    
    for g in obj[glue].pose.bone_groups:
        obj[glue].pose.bone_groups.remove(g)
    
    bpy.ops.pose.group_add()
    glueObj.pose.bone_groups.active.name = "Glue"
    glueObj.pose.bone_groups.active.color_set = 'THEME07'
    
    for boneObj in glueObj.pose.bones:
        boneObj.bone_group = glueObj.pose.bone_groups["Glue"]

    
    bpy.ops.object.mode_set(mode='OBJECT')

    glueObj.select_set(False)
    sarmObj.select_set(True)
    bpy.context.view_layer.objects.active = sarmObj

    lname = "BB Copy Loc"
    rname = "BB Copy Rot"
    sname = "BB Copy Sca"
    bpy.ops.object.mode_set(mode='POSE')

    for boneObj in obj[sarm].pose.bones:
        sbone = boneObj.name
        obj[sarm].data.bones.active = obj[sarm].data.bones[sbone]
        bc = obj[sarm].pose.bones[sbone].constraints
        bc.new('COPY_LOCATION')
        bc['Copy Location'].target = glueObj
        bc['Copy Location'].subtarget = sbone
        bc['Copy Location'].target_space = 'WORLD'
        bc['Copy Location'].owner_space = 'WORLD'
        bc['Copy Location'].influence = 1
        bc['Copy Location'].name = lname
    for boneObj in obj[sarm].pose.bones:
        sbone = boneObj.name
        obj[sarm].data.bones.active = obj[sarm].data.bones[sbone]
        bc = obj[sarm].pose.bones[sbone].constraints
        bc.new('COPY_ROTATION')
        bc['Copy Rotation'].target = glueObj
        bc['Copy Rotation'].subtarget = sbone
        bc['Copy Rotation'].target_space = 'WORLD'
        bc['Copy Rotation'].owner_space = 'WORLD'
        bc['Copy Rotation'].influence = 1
        bc['Copy Rotation'].name = rname
    for boneObj in obj[sarm].pose.bones:
        sbone = boneObj.name
        obj[sarm].data.bones.active = obj[sarm].data.bones[sbone]
        bc = obj[sarm].pose.bones[sbone].constraints
        bc.new('COPY_SCALE')
        bc['Copy Scale'].target = glueObj
        bc['Copy Scale'].subtarget = sbone
        bc['Copy Scale'].target_space = 'WORLD'
        bc['Copy Scale'].owner_space = 'WORLD'
        bc['Copy Scale'].influence = 1
        bc['Copy Scale'].name = sname

    bpy.ops.object.mode_set(mode='OBJECT')
    obj[sarm].select_set(False)
    obj[glue].select_set(True)
    bpy.context.view_layer.objects.active = glueObj

    return glue








def clean_controllers(armature=None, all=False):

    obj = bpy.data.objects

    
    
    if all == True:
        targets = []
        for o in obj:
            if o.type == 'ARMATURE':
                targets.append(o)
    else:
        targets = [ obj[armature] ]

    for armObj in targets:
        remove_these = {}
        
        
        for boneObj in armObj.pose.bones:
            bone = boneObj.name
            remove_these[bone] = []
            for constObj in boneObj.constraints:
                
                
                
                
                
                

                

                
                
                
                
                
                
                
                
                

                
                
                
                
                t = hasattr(constObj, 'target')
                st = hasattr(constObj, 'subtarget')

                
                
                
                if t == False:
                    continue
                
                
                targetObj = getattr(constObj, 'target')
                if targetObj == None:
                    continue

                
                
                
                
                target = targetObj.name
                

                
                
                
                subtarget = constObj.subtarget
                if subtarget != '':
                    
                    if subtarget not in obj[target].pose.bones:
                        remove_these[bone].append(constObj)

        for bone in remove_these:
            if len(remove_these[bone]) > 0:
                for c in remove_these[bone]:
                    armObj.pose.bones[bone].constraints.remove( c )

    return True







def build_sl_rig(rig_class="pos", store=True, rotate=False):

    for o in bpy.context.selected_objects:
        o.select_set(False)

    obj = bpy.data.objects

    
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

    
    arm_thing = bpy.data.armatures.new("BentoBuddy")
    armObj = bpy.data.objects.new("BentoBuddy", arm_thing)

    
    bpy.context.scene.collection.objects.link(armObj)
    bpy.context.view_layer.update()
    arm = armObj.name 
    armObj.location = (0.0, 0.0, 0.0)
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]

    
    avs = skel.avatar_skeleton
    muV = mathutils.Vector
    absolute = {}
    for bone in avs:
        
        
        if avs[bone]['type'] == 'collision':
            head = muV((avs[bone]['pos']))
        else:
            head = muV((avs[bone][rig_class]))
        has_parent = True
        bone_path = bone
        while(has_parent == True):
            
            parent = avs[bone_path]['parent']
            if parent == "":
                has_parent = False
            else:
                head += muV((avs[parent][rig_class]))
            bone_path = parent
        tail = head + muV((avs[bone]['end']))
        absolute[bone] = {}
        absolute[bone]['head'] = head
        absolute[bone]['tail'] = tail

    
    bpy.ops.object.mode_set(mode='EDIT')
    for bone in skel.avatar_skeleton:
        newbone = armObj.data.edit_bones.new(bone)
        
        
        

        newbone.head = absolute[bone]['head'] 
        newbone.tail = absolute[bone]['tail']

    
    
    bpy.ops.object.mode_set(mode='OBJECT')

    
    bpy.ops.object.mode_set(mode='EDIT')
    for b in bpy.context.object.data.edit_bones:
        b.select = False
        b.select_head = False   
        b.select_tail = False

    
    for bone in skel.avatar_skeleton:
        parent = skel.avatar_skeleton[bone]['parent']
        if parent == "":
            continue
        bpy.data.objects[arm].data.edit_bones[bone].parent = bpy.data.objects[arm].data.edit_bones[parent]
        connected = skel.avatar_skeleton[bone]['connected']
        bpy.data.objects[arm].data.edit_bones[bone].use_connect = connected

    bpy.ops.object.mode_set(mode='OBJECT')

    
    
    bpy.context.view_layer.update()

    
    bone_roll = {
    "mHandThumb1Left": 0.7853981852531433,
    "mHandThumb2Left": 0.7853981852531433,
    "mHandThumb3Left": 0.7853981852531433,
    "mHandThumb1Right": -0.7853981852531433,
    "mHandThumb2Right": -0.7853981852531433,
    "mHandThumb3Right": -0.7853981852531433,
    "mHipRight": -0.13089969754219055,
    "mHipLeft": 0.13089969754219055,
    }
    
    
    
        
            
        
            




    bpy.ops.object.mode_set(mode='OBJECT')

    
    
    
    if rotate == True:
        loc, rot, scale = armObj.matrix_world.decompose()
        smat = mathutils.Matrix()
        for i in range(3):
            smat[i][i] = scale[i]
        eu = mathutils.Euler(map(math.radians, (0, 0, -90)), 'XYZ')
        mat = mathutils.Matrix.Translation(loc) @ eu.to_matrix().to_4x4() @ smat
        armObj.matrix_world = mat
        bpy.ops.object.transform_apply( rotation=True, location=False, scale=False )

    
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.group_add()
    obj[arm].pose.bone_groups.active.name = mod_data.rig_group_mbones
    obj[arm].pose.bone_groups.active.color_set = mod_data.rig_group_mtheme
    bpy.ops.pose.group_add()
    obj[arm].pose.bone_groups.active.name = mod_data.rig_group_vbones
    obj[arm].pose.bone_groups.active.color_set = mod_data.rig_group_vtheme

    bpy.context.view_layer.objects.active = obj[arm]
    for bone in skel.avatar_skeleton:
        if skel.avatar_skeleton[bone]['type'] == 'bone':
            group = mod_data.rig_group_mbones
        else:
            group = mod_data.rig_group_vbones
        obj[arm].pose.bones[bone].bone_group = obj[arm].pose.bone_groups[group]

    bpy.ops.object.mode_set(mode='OBJECT')

    
    bpy.context.object.data.layers[md.bb_all_bones_layer] = True
    armObj.select_set(True)
    bpy.context.view_layer.objects.active = armObj

    bpy.ops.object.mode_set(mode='EDIT')
    for boneObj in armObj.data.edit_bones:
        if boneObj.name in bone_roll:
            boneObj.roll = bone_roll[boneObj.name]
        else:
            boneObj.roll = 0.0




    bpy.ops.object.mode_set(mode='OBJECT')


    
    if store:
        save_rig(armature=armObj.name)  
        
        armObj['rig_class'] = rig_class

    
    print("rigs::build_sl_rig reports : Disabled version acquisition")
    if 1 == 0:
        for mod_name in bpy.context.preferences.addons.keys():
            mod = sys.modules[mod_name]
            name = mod.bl_info.get('name')
            if name == "Bento Buddy":
                version = mod.bl_info.get('version', (-1, -1, -1))
                break
        armObj['bentobuddy'] = utils.get_bento_buddy_version()
    armObj['bentobuddy'] = "Post 2.8.2 - see rigs : build_sl_rig to re-enable"

    
    armObj['hide_extended_bones'] = 0
    armObj['hide_face_bones'] = 0
    armObj['hide_hand_bones'] = 0
    armObj['hide_volume_bones'] = 0

    return armObj









def build_rig(rig_class="pos", rotate=False, connect=True):

    for o in bpy.context.selected_objects:
        o.select_set(False)

    obj = bpy.data.objects

    
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

    
    arm_thing = bpy.data.armatures.new("BentoBuddy")
    armObj = bpy.data.objects.new("BentoBuddy", arm_thing)

    
    bpy.context.scene.collection.objects.link(armObj)
    bpy.context.view_layer.update()
    arm = armObj.name 
    armObj.location = (0.0, 0.0, 0.0)
    bpy.data.objects[arm].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm]

    
    avs = skel.avatar_skeleton
    muV = mathutils.Vector
    absolute = {}
    for bone in avs:
        
        
        if avs[bone]['type'] == 'collision':
            head = muV((avs[bone]['pos']))
        else:
            head = muV((avs[bone][rig_class]))
        has_parent = True
        bone_path = bone
        while(has_parent == True):
            
            parent = avs[bone_path]['parent']
            if parent == "":
                has_parent = False
            else:
                head += muV((avs[parent][rig_class]))
            bone_path = parent
        tail = head + muV((avs[bone]['end']))
        absolute[bone] = {}
        absolute[bone]['head'] = head
        absolute[bone]['tail'] = tail

    
    bpy.ops.object.mode_set(mode='EDIT')
    for bone in skel.avatar_skeleton:
        newbone = armObj.data.edit_bones.new(bone)
        
        
        

        newbone.head = absolute[bone]['head'] 
        newbone.tail = absolute[bone]['tail']

    
    
    bpy.ops.object.mode_set(mode='OBJECT')

    
    print("use_deform disabled on attachment bones, use the (enable) tool to use them for skinning")
    bpy.ops.object.mode_set(mode='EDIT')
    for b in bpy.context.object.data.edit_bones:
        b.select = False
        b.select_head = False   
        b.select_tail = False
        
        
        
        
        if " " in b.name:  
            b.use_deform = False
        if b.name in skel.avatar_skeleton:
            if skel.avatar_skeleton[b.name]['type'] == "attachment":
                b.use_deform = False

    
    for bone in skel.avatar_skeleton:
        parent = skel.avatar_skeleton[bone]['parent']
        if parent == "":
            continue
        bpy.data.objects[arm].data.edit_bones[bone].parent = bpy.data.objects[arm].data.edit_bones[parent]
        connected = skel.avatar_skeleton[bone]['connected']
        if connect == True:
            bpy.data.objects[arm].data.edit_bones[bone].use_connect = connected

    bpy.ops.object.mode_set(mode='OBJECT')

    
    
    bpy.context.view_layer.update()

    
    bone_roll = {
    "mHandThumb1Left": 0.7853981852531433,
    "mHandThumb2Left": 0.7853981852531433,
    "mHandThumb3Left": 0.7853981852531433,
    "mHandThumb1Right": -0.7853981852531433,
    "mHandThumb2Right": -0.7853981852531433,
    "mHandThumb3Right": -0.7853981852531433,
    "mHipRight": -0.13089969754219055,
    "mHipLeft": 0.13089969754219055,
    }
    
    
    
        
            
        
            




    bpy.ops.object.mode_set(mode='OBJECT')

    
    
    
    if rotate == True:
        loc, rot, scale = armObj.matrix_world.decompose()
        smat = mathutils.Matrix()
        for i in range(3):
            smat[i][i] = scale[i]
        eu = mathutils.Euler(map(math.radians, (0, 0, -90)), 'XYZ')
        mat = mathutils.Matrix.Translation(loc) @ eu.to_matrix().to_4x4() @ smat
        armObj.matrix_world = mat
        bpy.ops.object.transform_apply( rotation=True, location=False, scale=False )

    
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.group_add()
    obj[arm].pose.bone_groups.active.name = mod_data.rig_group_mbones
    obj[arm].pose.bone_groups.active.color_set = mod_data.rig_group_mtheme
    bpy.ops.pose.group_add()
    obj[arm].pose.bone_groups.active.name = mod_data.rig_group_vbones
    obj[arm].pose.bone_groups.active.color_set = mod_data.rig_group_vtheme
    bpy.ops.pose.group_add()
    obj[arm].pose.bone_groups.active.name = mod_data.rig_group_abones
    obj[arm].pose.bone_groups.active.color_set = mod_data.rig_group_atheme
    bpy.ops.pose.group_add()
    obj[arm].pose.bone_groups.active.name = mod_data.rig_group_nbones
    obj[arm].pose.bone_groups.active.color_set = mod_data.rig_group_ntheme

    bpy.context.view_layer.objects.active = obj[arm]
    for bone in skel.avatar_skeleton:
        if skel.avatar_skeleton[bone]['type'] == 'bone':
            group = mod_data.rig_group_mbones
        elif skel.avatar_skeleton[bone]['type'] == 'attachment':
            if " " in bone:
                group = mod_data.rig_group_nbones
            else:
                group = mod_data.rig_group_abones
        else:
            group = mod_data.rig_group_vbones

        obj[arm].pose.bones[bone].bone_group = obj[arm].pose.bone_groups[group]

    bpy.ops.object.mode_set(mode='OBJECT')

    
    bpy.context.object.data.layers[md.bb_all_bones_layer] = True
    armObj.select_set(True)
    bpy.context.view_layer.objects.active = armObj

    bpy.ops.object.mode_set(mode='EDIT')
    for boneObj in armObj.data.edit_bones:
        if boneObj.name in bone_roll:
            boneObj.roll = bone_roll[boneObj.name]
        else:
            boneObj.roll = 0.0




    bpy.ops.object.mode_set(mode='OBJECT')

    
    
    if 1 == 0:
        for mod_name in bpy.context.preferences.addons.keys():
            mod = sys.modules[mod_name]
            name = mod.bl_info.get('name')
            if name == "Bento Buddy":
                version = mod.bl_info.get('version', (-1, -1, -1))
                break
        armObj['bentobuddy'] = utils.get_bento_buddy_version()
    
    armObj['bentobuddy'] = globals.version

    
    
    if 1 == 0:
        armObj['hide_extended_bones'] = 0
        armObj['hide_face_bones'] = 0
        armObj['hide_hand_bones'] = 0
        armObj['hide_volume_bones'] = 0
    
    

    show_bones(armature=armObj, default=True)

    return armObj








def set_bone_layers(armObj):

    

    
    
    
    
    
    layers_m = visible.layers['base']
    layers_v = visible.layers['volume']
    layers_a = visible.layers['attach']
    layers_n = visible.layers['attach2']
    layers_face = visible.layers['face']
    layers_hands = visible.layers['hand']
    layers_tail = visible.layers['tail']
    layers_wings = visible.layers['wing']
    layers_groin = visible.layers['groin']
    layers_hinds = visible.layers['hind']

    for boneObj in armObj.data.bones:
        
        boneObj.layers[0] = False
        bone = boneObj.name
        if bone not in skel.avatar_skeleton:
            continue
        if bone.startswith("m"):
            if "Face" in bone:
                boneObj.layers[layers_face] = True
            elif "Hand" in bone or "Wrist" in bone:
                boneObj.layers[layers_hands] = True
            elif "Wing" in bone:
                boneObj.layers[layers_wings] = True
            elif "Tail" in bone:
                boneObj.layers[layers_tail] = True
            elif "Groin" in bone:
                boneObj.layers[layers_groin] = True
            elif "Hind" in bone:
                boneObj.layers[layers_hinds] = True
            
            else:
                boneObj.layers[layers_m] = True

        elif skel.avatar_skeleton[bone]['type'] == "collision":
            boneObj.layers[layers_v] = True
        elif skel.avatar_skeleton[bone]['type'] == "attachment":
            
            if " " in bone:
                boneObj.layers[layers_n] = True
            else:
                boneObj.layers[layers_a] = True

    
    
    

    
    for boneObj in armObj.data.bones:
        boneObj.layers[0] = False
    
    
    if visible.layers.get('controller') != None:
        
        armObj.data.layers[layers_c] = True
    else:
        armObj.data.layers[layers_m] = True
        armObj.data.layers[layers_hands] = True
    
    
    
    armObj.data.layers[0] = True

    
    
    
    visible.layers.pop('groin', "")
    for group in visible.layers:
        if group == "base" or group == "hand":
            state = True
        else:
            state = False
        print("processing", group, "with state", state)
        show_bones(armature=armObj, group=group, state=state)

    return True







def get_layer_state(armature):
    if isinstance(armature, str):
        armObj = bpy.data.objects[armature]
    else:
        armObj = armature

    state = {}
    index = 0
    for s in armObj.data.layers:
        state[index] = s
        index += 1
    index = 0
    for s in armObj.data.layers:
        armObj.data.layers[index] = True
        index += 1

    return state



def set_layer_state(armature=None, state=None):
    if isinstance(armature, str):
        armObj = bpy.data.objects[armature]
    else:
        armObj = armature
    index = 0
    for s in armObj.data.layers:
        armObj.data.layers[index] = state[index]
        index += 1
    return True



def reset_layer_state(armature):
    if isinstance(armature, str):
        armObj = bpy.data.objects[armature]
    else:
        armObj = armature
    
    armObj.data.layers[0] = True
    
    for i in range(1, len(armObj.data.layers)):
        armObj.data.layers[i] = False
    
    for layer in visible.default:
        index = visible.layers[layer]
        armObj.data.layers[index] = True
    return True













def show_bones(armature=None, group=None, state=True, default=False):

    
    not_state = not state

    armObj = armature
    if isinstance(armature, str):
        armObj = bpy.data.objects[armature]

    
    get_layer_state(armObj)

    
    bone_groups = armObj.get('bb_bone_groups', {})

    
    if default == True:
        for group in visible.layers:
            bone_groups[group] = False
        bone_groups['base'] = True
        bone_groups['hand'] = True
        armObj['bb_bone_groups'] = bone_groups
        for boneObj in armObj.data.bones:
            boneObj.hide = True
        for boneObj in armObj.data.bones:
            bone = boneObj.name
            if bone in visible.bones['base']:
                boneObj.hide = False
            if "Hand" in bone and bone in skel.avatar_skeleton:
                if skel.avatar_skeleton[bone]['type'] == "bone":
                    boneObj.hide = False
        return True
    
    if group == None:
        print("rigs::show_bones reports : no group offered, hiding attachment bones instead")
        for boneObj in armObj.data.bones:
            bone = boneObj.name
            if skel.avatar_skeleton[bone]['type'] == "attachment":
                boneObj.hide = True
        armObj['bb_bone_groups']['attach'] = False
        armObj['bb_bone_groups']['attach2'] = False
        return True

    
    
    elif group == "base":
        for boneObj in armObj.data.bones:
            bone = boneObj.name
            if bone in visible.bones['base']:
                boneObj.hide = not_state
    elif group == "volume":
        for boneObj in armObj.data.bones:
            bone = boneObj.name
            if bone in skel.avatar_skeleton:
                if skel.avatar_skeleton[bone]['type'] == "collision":
                    boneObj.hide = not_state
    elif group == "attach":
        for boneObj in armObj.data.bones:
            bone = boneObj.name
            
            if bone in skel.avatar_skeleton and " " not in bone:
                if skel.avatar_skeleton[bone]['type'] == "attachment":
                    boneObj.hide = not_state
    elif group == "attach2":
        for boneObj in armObj.data.bones:
            bone = boneObj.name
            
            if bone in skel.avatar_skeleton and " " in bone:
                if skel.avatar_skeleton[bone]['type'] == "attachment":
                    boneObj.hide = not_state
    elif group == "face":
        for boneObj in armObj.data.bones:
            bone = boneObj.name
            if bone.startswith('m') and bone in skel.avatar_skeleton and "Face" in bone:
                boneObj.hide = not_state
    elif group == "hind":
        for boneObj in armObj.data.bones:
            bone = boneObj.name
            if bone.startswith('m') and bone in skel.avatar_skeleton and "Hind" in bone:
                boneObj.hide = not_state
    elif group == "hand":
        for boneObj in armObj.data.bones:
            bone = boneObj.name
            if bone.startswith('m') and bone in skel.avatar_skeleton and "Hand" in bone:
                boneObj.hide = not_state
    elif group == "wing":
        for boneObj in armObj.data.bones:
            bone = boneObj.name
            if bone.startswith('m') and bone in skel.avatar_skeleton and "Wing" in bone:
                boneObj.hide = not_state
    elif group == "tail":
        for boneObj in armObj.data.bones:
            bone = boneObj.name
            if bone.startswith('m') and bone in skel.avatar_skeleton and "Tail" in bone:
                boneObj.hide = not_state
    elif group == "spine":
        for boneObj in armObj.data.bones:
            bone = boneObj.name
            if bone.startswith('m') and bone in skel.avatar_skeleton and "Spine" in bone:
                boneObj.hide = not_state
    else:
        print("rigs::show_bones reports : unknown bone group:", group)
        return False

    
    armObj['bb_bone_groups'][group] = state

    return True





def is_armature():
    if len(bpy.context.selected_objects) != 1:
        return False
    if bpy.context.selected_objects[0].type != 'ARMATURE':
        return False
    return bpy.context.selected_objects[0]





def snap_to(source=None, target=None):
    
    obj = bpy.data.objects

    
    old_mode = bpy.context.mode
    if old_mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    if old_mode.startswith('EDIT'):
        old_mode = 'EDIT'

    selected = [o for o in bpy.context.selected_objects]
    active = bpy.context.active_object

    for o in bpy.context.selected_objects:
        o.select_set(False)
    obj[target].select_set(True)
    bpy.context.view_layer.objects.active = obj[target]
    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = {}
    for boneObj in obj[target].data.edit_bones:
        bone = boneObj.name
        edit_bones[bone] = {}
        edit_bones[bone]['head'] = boneObj.head.copy()
        edit_bones[bone]['tail'] = boneObj.tail.copy()
        edit_bones[bone]['roll'] = boneObj.roll
    bpy.ops.object.mode_set(mode='OBJECT')
    obj[target].select_set(False)

    
    obj[source].select_set(True)
    bpy.context.view_layer.objects.active = obj[source]

    
    bpy.ops.object.mode_set(mode='EDIT')
    for boneObj in obj[source].data.edit_bones:
        boneObj.use_connect = False
    
    
    
    for boneObj in obj[source].data.edit_bones:
        bone = boneObj.name
        if bone not in obj[target].data.bones:
            continue
        boneObj.head = edit_bones[bone]['head']
        boneObj.tail = edit_bones[bone]['tail']
        boneObj.roll = edit_bones[bone]['roll']

    bpy.ops.object.mode_set(mode='OBJECT')

    for o in bpy.context.selected_objects:
        o.select_set(False)
    for o in selected:
        o.select_set(True)
    bpy.context.view_layer.objects.active = active

    return True



















def add_constraints(
    source=None, target=None,
    bone_map=None, constraint="COPY_TRANSFORMS",
    space='WORLD', influence=1, name=None,
    ):

    obj = bpy.data.objects
    sourceObj = source
    targetObj = target
    if isinstance(source, str):
        sourceObj = obj[source]
    if isinstance(target, str):
        targetObj = obj[target]

    
    
    
    if bone_map == None:
        bone_map = {}
        for boneObj in sourceObj.data.bones:
            if boneObj.name not in targetObj.data.bones:
                continue
            bone_map[boneObj.name] = {"Armature": boneObj.name}

    
        
        
        
        
        
    

    
    
    
    
    
    state = utils.get_state()
    
    sourceObj.select_set(True)
    bpy.context.view_layer.objects.active = sourceObj

    for boneObj in sourceObj.pose.bones:
        sbone = boneObj.name
        if sbone not in bone_map:
            continue
        (arm, tbone), = bone_map[sbone].items()
        sourceObj.data.bones.active = boneObj.bone 
        bc = boneObj.constraints
        conObj = bc.new(constraint)
        cname = conObj.name
        conObj.target = targetObj
        conObj.subtarget = tbone
        conObj.target_space = space
        conObj.owner_space = space
        conObj.influence = influence
        if constraint == 'CHILD_OF':
            conObj.use_location_x = False
            conObj.use_location_y = False
            conObj.use_location_z = False
            conObj.use_scale_x = False
            conObj.use_scale_y = False
            conObj.use_scale_z = False
            context_py = bpy.context.copy()
            context_py["constraint"] = bc.active
            utils.set_inverse(context_py, cname)
            
            
        conObj.name = "BB " + cname
        if name != None:
            cnames = boneObj.get(name, [])
            cnames.append(conObj.name)
            boneObj[name] = cnames

        
        
        
        
        
        
        
        
        
        

    utils.set_state(state)

    return True





def add_controllers(
    source=None, target=None,
    bone_map=None, constraint="COPY_TRANSFORMS",
    target_space='WORLD', owner_space='WORLD',
    influence=1, name=None,
    location_x=False, location_y=False, location_z=False,
    rotation_x=True, rotation_y=True, rotation_z=True,
    scale_x=False, scale_y=False, scale_z=False,
    ):

    obj = bpy.data.objects
    sourceObj = source
    targetObj = target
    if isinstance(source, str):
        sourceObj = obj[source]
    if isinstance(target, str):
        targetObj = obj[target]

    
    
    
    if bone_map == None:
        bone_map = {}
        for boneObj in sourceObj.data.bones:
            if boneObj.name not in targetObj.data.bones:
                continue
            bone_map[boneObj.name] = {"Armature": boneObj.name}

    
    
    
    
    
    state = utils.get_state()
    
    sourceObj.select_set(True)
    bpy.context.view_layer.objects.active = sourceObj

    for boneObj in sourceObj.pose.bones:
        sbone = boneObj.name
        if sbone not in bone_map:
            continue
        tbone = bone_map[sbone]
        sourceObj.data.bones.active = boneObj.bone 
        bc = boneObj.constraints
        conObj = bc.new(constraint)
        cname = conObj.name
        conObj.target = targetObj
        conObj.subtarget = tbone
        conObj.target_space = target_space
        conObj.owner_space = owner_space
        conObj.influence = influence

        if constraint == 'CHILD_OF':
            conObj.target_space = 'WORLD'
            conObj.owner_space = 'POSE'
            conObj.use_location_x = location_x
            conObj.use_location_y = location_y
            conObj.use_location_z = location_z
            
            conObj.use_rotation_x = rotation_x
            conObj.use_rotation_y = rotation_y
            conObj.use_rotation_z = rotation_z
            
            conObj.use_scale_x = scale_x
            conObj.use_scale_y = scale_y
            conObj.use_scale_z = scale_z
            context_py = bpy.context.copy()
            context_py["constraint"] = bc.active
            utils.set_inverse(context_py, cname)
            
            
        conObj.name = "BB " + cname
        if name != None:
            cnames = boneObj.get(name, [])
            cnames.append(conObj.name)
            boneObj[name] = cnames

    utils.set_state(state)

    return True






















def freeze(armature=None, bones=[], transforms=True, influence=1):

    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    for o in bpy.context.selected_objects:
        o.select_set(False)

    obj = bpy.data.objects
    sarmObj = obj[armature]
    sarmObj.select_set(True)
    bpy.context.view_layer.objects.active = sarmObj

    sarmObj.data.display_type = 'OCTAHEDRAL'
    sarmObj.show_in_front = False

    
    bpy.ops.object.mode_set(mode='EDIT')
    for boneObj in sarmObj.data.edit_bones:
        boneObj.use_connect = False
    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.duplicate()
    glueObj = bpy.context.object
    glueObj.name = "_SNAP_RIG"
    glue = glueObj.name

    glueObj.data.display_type = 'STICK'
    glueObj.show_in_front = True

    
    sarmObj['bb_frozen_target'] = glueObj
    glueObj['bb_frozen_source'] = sarmObj

    
    bpy.ops.object.mode_set(mode='EDIT')
    for boneObj in glueObj.data.edit_bones:
        boneObj.parent = None

    
    bpy.ops.object.mode_set(mode='POSE')
    for b in obj[glue].pose.bones:
        for c in b.constraints:
            b.constraints.remove(c)
    
    for g in obj[glue].pose.bone_groups:
        obj[glue].pose.bone_groups.remove(g)
    
    bpy.ops.pose.group_add()
    glueObj.pose.bone_groups.active.name = "Glue"
    glueObj.pose.bone_groups.active.color_set = 'THEME07'
    
    for boneObj in glueObj.pose.bones:
        boneObj.bone_group = glueObj.pose.bone_groups["Glue"]

    
    bpy.ops.object.mode_set(mode='OBJECT')

    glueObj.select_set(False)
    sarmObj.select_set(True)
    bpy.context.view_layer.objects.active = sarmObj

    bpy.ops.object.mode_set(mode='POSE')

    
    if transforms == True:
        
        for boneObj in sarmObj.pose.bones:
            sbone = boneObj.name
            sarmObj.data.bones.active = sarmObj.data.bones[sbone]
            bc = sarmObj.pose.bones[sbone].constraints
            CO = bc.new('COPY_TRANSFORMS')
            CO.target = glueObj
            CO.subtarget = sbone
            CO.target_space = 'WORLD'
            CO.owner_space = 'WORLD'
            if sbone in bones:
                CO.influence = influence
            else:
                CO.influence = 0
            CO.name = "BB Frozen TRS"

    else:
        
        for boneObj in sarmObj.pose.bones:
            sbone = boneObj.name
            sarmObj.data.bones.active = sarmObj.data.bones[sbone]
            bc = sarmObj.pose.bones[sbone].constraints
            CO = bc.new('COPY_ROTATION')
            CO.target = glueObj
            CO.subtarget = sbone
            CO.target_space = 'WORLD'
            CO.owner_space = 'WORLD'
            if sbone in bones:
                CO.influence = influence
            else:
                CO.influence = 0
            CO.name = "BB Frozen ROT"
        for boneObj in sarmObj.pose.bones:
            sbone = boneObj.name
            sarmObj.data.bones.active = sarmObj.data.bones[sbone]
            bc = sarmObj.pose.bones[sbone].constraints
            CO = bc.new('COPY_LOCATION')
            CO.target = glueObj
            CO.subtarget = sbone
            CO.target_space = 'WORLD'
            CO.owner_space = 'WORLD'
            if sbone in bones:
                CO.influence = influence
            else:
                CO.influence = 0
            CO.name = "BB Frozen LOC"
        for boneObj in sarmObj.pose.bones:
            sbone = boneObj.name
            sarmObj.data.bones.active = sarmObj.data.bones[sbone]
            bc = sarmObj.pose.bones[sbone].constraints
            CO = bc.new('COPY_SCALE')
            CO.target = glueObj
            CO.subtarget = sbone
            CO.target_space = 'WORLD'
            CO.owner_space = 'WORLD'
            if sbone in bones:
                CO.influence = influence
            else:
                CO.influence = 0
            CO.name = "BB Frozen SCL"

    bpy.ops.object.mode_set(mode='OBJECT')
    sarmObj.select_set(False)
    glueObj.select_set(True)
    bpy.context.view_layer.objects.active = glueObj

    
    return glueObj











def get_controller_rig(armature=None):
    if armature == None:
        return False
    if armature not in bpy.context.scene.objects:
        return False
    obj = bpy.data.objects
    armObj = obj[armature]

    
    
    outRig = armObj.get('bb_controller_slave', None)
    inRig = armObj.get('bb_controller_master', None)

    
    
    if outRig == None and inRig == None:
        return False

    

    
    if outRig != None:
        return armObj
    
    if inRig.name not in bpy.context.scene.objects:
        return False
    
    return inRig





def add_empty_constraints(source=None, target=None, transform='COPY_TRANSFORMS', space='WORLD', influence=0):
    trs_names = {
        "COPY_TRANSFORMS": "BB TRS", "COPY_ROTATION": "BB ROT", "COPY_LOCATION": "BB LOC", "CHILD_OF": "BB CO"
        }
    if transform not in trs_names:
        print("add_empty_constraint reports: transform", transform, "is not a key in trs_names, update this later")
    obj = bpy.data.objects
    state = utils.get_state()
    
    
    
    con_objs = {}
    sarmObj = obj[source]
    tarmObj = obj[target]
    for boneObj in sarmObj.pose.bones:
        bone = boneObj.name
        sarmObj.data.bones.active = sarmObj.data.bones[bone]
        bc = sarmObj.pose.bones[bone].constraints
        CO = bc.new(transform)
        CO.target = tarmObj
        
        CO.target_space = space
        CO.owner_space = space
        CO.influence = influence
        
        if transform in trs_names:
            CO.name = trs_names[transform]
        else:
            CO.name = transform
        con_objs[bone] = CO

    utils.set_state(state)

    return con_objs













def get_bone_data(armature=None, deform_only=False, store=True, location=False, rotation=False, scale=True, pose=False):

    
    
    

    
    
    
    this_mode = bpy.context.mode
    if this_mode.startswith('EDIT'):
        old_mode == 'EDIT'
    else:
        old_mode = this_mode
    if bpy.context.active_object != None:
        bpy.ops.object.mode_set(mode='OBJECT')
    selected = bpy.context.selected_objects
    active = bpy.context.active_object
    for o in selected:
        o.select_set(False)
    


    
    armObj = bpy.data.objects[armature]
    armObj.select_set(True)
    bpy.context.view_layer.objects.active = armObj

    
    bpy.ops.object.duplicate()
    proxyObj = bpy.context.active_object


    
    
    
    


    
    
    
    proxyObj.animation_data_clear()
    if pose == True:
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.armature_apply()
    bpy.ops.object.mode_set(mode='OBJECT')

    
    
    print("Making single user...")
    bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False)

    bpy.ops.object.transform_apply(scale=scale, rotation=rotation, location=location)

    
    
    bone_data = {}
    bpy.ops.object.mode_set(mode='EDIT')
    for boneObj in proxyObj.data.edit_bones:
        bone = boneObj.name
        bone_data[bone] = {}
        bone_data[bone]['head'] = boneObj.head.copy()
        bone_data[bone]['tail'] = boneObj.tail.copy()
        bone_data[bone]['roll'] = boneObj.roll

    
    
    for boneObj in proxyObj.pose.bones:
        dBone = boneObj.bone
        bone = boneObj.name
        bone_data[bone]['matrix'] = boneObj.matrix.copy()
        bone_data[bone]['matrix_local'] = dBone.matrix_local.copy()

    bpy.ops.object.mode_set(mode='OBJECT')
    utils.delete()



    
    
    
    for o in selected:
        o.select_set(True)
    bpy.context.view_layer.objects.active = active
    
    
    

    if store == True:
        print("Storing bone data for", armObj.name)
        for boneObj in armObj.data.bones:
            bone = boneObj.name
            boneObj['head'] = bone_data[bone]['head'].copy()
            boneObj['tail'] = bone_data[bone]['tail'].copy()
            boneObj['roll'] = bone_data[bone]['roll']
            boneObj['matrix'] = bone_data[bone]['matrix'].copy()
            boneObj['matrix_local'] = bone_data[bone]['matrix_local'].copy()

    return bone_data




def get_rig_class():
    bb_devkit = bpy.context.scene.bb_devkit
    
    classes = {"default", "neutral", "male_default", "male_neutral"}
    rc = "rig_class_"
    for c in classes:
        if getattr(bb_devkit, rc + c) == True:
            return c
    return ""



def remove_pose_groups(arm):
    if isinstance(arm, str):
        obj = bpy.data.objects
        OBJ = obj[arm]
    else:
        OBJ = arm
    for g in OBJ.pose.bone_groups:
        OBJ.pose.bone_groups.remove(g)
    print("rigs::remove_pose_groups reports: finished")
    return











def get_mesh(arm):
    armObj = arm
    if isinstance(arm, str):
        if utils.is_valid(arm):
            armObj = bpy.data.objects[arm]
        else:
            print("The armature is not in the scene:", arm)
            return False

    
    selected = bpy.context.selected_objects
    active = bpy.context.active_object
    rigs = []
    for o in selected:
        if o.type == 'ARMATURE':
            rigs.append(o)
    if len(rigs) > 1:
        print("Too many rigs, expected 1")
        return False

    state = utils.get_state()

    mesh = []
    for o in bpy.data.objects:
        if o.type == 'MESH':
            for C in o.modifiers:
                if C.type == 'ARMATURE':
                    if C.object == armObj:
                        mesh.append(o)
                        break

    utils.set_state(state)

    if len(mesh) > 0:
        return mesh
    return False








def get_associated_mesh(arm, report=False):
    armObj = arm
    if isinstance(arm, str):
        if utils.is_valid(arm):
            armObj = bpy.data.objects[arm]
        else:
            if report == True:
                print("rigs::get_associated_mesh reports : the armature is not in the scene", arm)
            return False

    if len(armObj.children) == 0:
        if report == True:
            print("rigs::get_associated_mesh reports : no children", arm)
        return False

    
    mesh = []
    for cObj in armObj.children:
        if cObj.type != 'MESH':
            if report == True:
                print("rigs::get_associated_mesh reports : child object is not a mesh", cObj.name)
            continue
        mesh.append(cObj)
    
    if len(mesh) == 0:
        if report == True:
            print("rigs::get_associated_mesh reports : no mesh to process", cOBj.name)
        return False
    
    approved = []
    for meshObj in mesh:
        qualified = []
        for modObj in meshObj.modifiers:
            if modObj.type == 'ARMATURE':
                qualified.append(modObj)
        if len(qualified) == 0:
            if report == True:
                print("rigs::get_associated_mesh reports : no armature modifier on", meshObj.name)
        elif len(qualified) > 1:
            if report == True:
                print("rigs::get_associated_mesh reports : too many armature modifiers on", meshObj.name)
            continue
        if modObj.object == armObj:
            approved.append(meshObj)
        else:
            if report == True:
                print("rigs::get_associated_mesh reports : the mesh", meshObj.name, "has its armature modifier pointing to some other rig")
    if len(approved) == 0:
        if report == True:
            print("rigs::get_associated_mesh reports :  no approved mesh associated with", armObj.name)
        return False
    
    return approved

get_mesh_from_rig = get_associated_mesh










def check_maps(armature=None, rename=None, reskin=None, pose=None, report=False):
    if isinstance(armature, str):
        armObj = bpy.data.objects[armature]
    else:
        armObj = armature

    
    rename_map = rename
    reskin_map = reskin
    pose_map = pose

    
    if rename_map == None:
        rename_map = armObj.get('bb_onemap_rename', {})
    if reskin_map == None:
        reskin_map = armObj.get('bb_onemap_reskin', {})

    
    
    rename = {}
    bad_bones = []
    for bone in rename_map:
        if bone in armObj.data.bones:
            rename[bone] = rename_map[bone]
        else:
            bad_bones.append(bone)
    if len(rename) == 0:
        if report == True:
            print("None of the bone maps in your map file matched the rig.  The following is a list of bones in the file...")
            print(bad_bones)
        return False

    if report == True:
        print("The following anchors matched:", rename)
    
    
    
    reskin = {}
    if len(reskin_map) == 0:
        if report == True:
            print("No reskin bones")
    else:
        for anchor in reskin_map:
            bones = reskin_map[anchor]
            for rbone in bones:
                if rbone in armObj.data.bones:
                    if anchor not in reskin:
                        reskin[anchor] = {}
                    
                    
                    reskin[anchor][rbone] = ""
    if report == True:
        if len(reskin) == 0:
            print("There's a reskin map but no usable bones")
        else:
            print("The following reskin bones are available:", reskin)

        return True













def create_bone_name(armature=None, bones=[], max=100):
    armObj = armature
    if isinstance(armature, str):
        armObj = bpy.data.objects[armature]
    fail = 0
    for i in range(max):
        bone = utils.get_temp_name()
        if bone not in armObj.data.bones and bone not in bones:
            return bone
    print("rigs::create_bone_name reports : fall through, apparently there were", max, "collisions")

    return False



def apply_pose(armObj):
    if isinstance(armObj, str):
        armObj = bpy.data.objects[armObj]
    state = utils.get_state()
    armObj.select_set(True)
    utils.activate(armObj)
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.armature_apply(selected=False)
    utils.set_state(state)
    return True





def apply_map_pose(armature=None, pose=None):
    armObj = armature
    if isinstance(armature, str):
        armObj = bpy.data.objects[armature]

    state = utils.get_state()

    armObj.select_set(True)
    utils.activate(armObj)

    for bone in pose:
        
        if bone not in armObj.data.bones:
            print("no bone:", bone)
            continue
        old_rotation_mode = armObj.pose.bones[bone].rotation_mode
        armObj.pose.bones[bone].rotation_mode = 'QUATERNION'
        armObj.pose.bones[bone].matrix_basis = mathutils.Matrix(pose[bone])
        armObj.pose.bones[bone].rotation_mode = old_rotation_mode

    bpy.context.view_layer.update()

    utils.set_state(state)

    return True
















def match_bone_orientation(inRig=None, outRig=None, apply=False):
    state = utils.get_state()
    outRig.select_set(True)
    utils.activate(outRig)

    
    rename_map = outRig['bb_onemap_rename']

    
    
    matrices = {}
    for boneObj in outRig.pose.bones:
        matrices[boneObj.name] = boneObj.matrix.copy()

    parents = {}
    bpy.ops.object.mode_set(mode='EDIT')
    for boneObj in outRig.data.edit_bones:
        parents[boneObj.name] = boneObj.parent
        boneObj.use_connect = False
    bpy.ops.object.mode_set(mode='OBJECT')

    
    for boneObj in outRig.pose.bones:
        for c in boneObj.constraints:
            boneObj.constraints.remove(c)

    for tbone in rename_map:
        sbone = rename_map[tbone]
        if tbone in outRig.data.bones and sbone in inRig.data.bones:
            
            boneObj = outRig.pose.bones[tbone]
            outRig.data.bones.active = boneObj.bone 
            bc = boneObj.constraints
            conObj = bc.new('COPY_ROTATION')
            cname = conObj.name
            conObj.target = inRig
            conObj.subtarget = sbone
            conObj.target_space = 'WORLD'
            conObj.owner_space = 'WORLD'
            conObj.influence = 1
            conObj.name = "TEMP " + cname
    
    if apply == False:
        
        bpy.ops.object.mode_set(mode='EDIT')
        for boneObj in outRig.data.edit_bones:
            boneObj.parent = None
        bpy.ops.object.mode_set(mode='OBJECT')

        new_matrices = {}
        for boneObj in outRig.pose.bones:
            new_matrices[boneObj.name] = boneObj.matrix.copy()

        
        for boneObj in outRig.pose.bones:
            for c in boneObj.constraints:
                boneObj.constraints.remove(c)

        
        for tbone in rename_map:
            sbone = rename_map[tbone]
            if tbone in outRig.data.bones and sbone in inRig.data.bones:
                outrig.data.bones[tbone].matrix = new_matrices[tbone]

        
        bpy.ops.object.mode_set(mode='EDIT')
        for boneObj in outRig.data.edit_bones:
            boneObj.parent = parents[boneObj.name]
        bpy.ops.object.mode_set(mode='OBJECT')

    
    else:
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.armature_apply(selected=False)
        bpy.ops.object.mode_set(mode='OBJECT')

        
        for boneObj in outRig.pose.bones:
            for c in boneObj.constraints:
                boneObj.constraints.remove(c)

    utils.set_state(state)

    return True










def invert_bone(source=None, target=None, bone=None):
    sarmObj = source
    tarmObj = target
    boneObj = bone
    if isinstance(source, str):
        sarmObj = bpy.data.objects[source]
    if isinstance(target, str):
        tarmObj = bpy.data.objects[target]
    if isinstance(bone, str):
        boneObj = bpy.data.objects[target].pose.bones[bone]
    tmat = tarmObj.matrix_world.copy()
    pmat = sarmObj.matrix_world.copy()
    
    bmat = boneObj.matrix.copy()
    MF = bmat.inverted() @ pmat @ tmat.inverted()
    return MF











def freeze_state(arm, state="start", report=False):
    armObj = arm
    if isinstance(object, str):
        armObj = bpy.data.object[arm]

    frame_current = bpy.context.scene.frame_current
    if state == "start":
        start = True
        end = False
    if state == "end":
        start = False
        end = True
    if state == "current":
        start = False
        end = False
    frame_start, frame_end = animutils.get_frame_range(armObj, start=start, end=end)

    
    utils.make_single(armObj)
    mesh_list = get_associated_mesh(armObj, report=True)
    if mesh_list != False:
        for meshObj in mesh_list:
            utils.make_single(meshObj)
    else:
        mesh_list = [] 

    
    JUNK = utils.get_state() 

    armObj.animation_data_clear()
    armObj.select_set(True)
    utils.activate(armObj)
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.armature_apply()
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    for o in mesh_list:
        o.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


    
    
    
    


    return True








def align_bones(source=None, target=None, bone=None, all=True):
    sarmObj = source
    tarmObj = target
    boneObj = bone
    if isinstance(sarmObj, str):
        sarmObj = bpy.data.objects[source]
    if isinstance(tarmObj, str):
        tarmObj = bpy.data.objects[target]
    if bone != None:
        if isinstance(boneObj, str) == False:
            bone = boneObj.name

    def align_bone_x_axis(edit_bone, new_x_axis):
        
        
        new_x_axis = new_x_axis.cross(edit_bone.y_axis)
        new_x_axis.normalize()
        dot = max(-1.0, min(1.0, edit_bone.z_axis.dot(new_x_axis)))
        angle = math.acos(dot)
        edit_bone.roll += angle
        dot1 = edit_bone.z_axis.dot(new_x_axis)
        edit_bone.roll -= angle * 2.0
        dot2 = edit_bone.z_axis.dot(new_x_axis)
        if dot1 > dot2:
            edit_bone.roll += angle * 2.0

    
    
    
    source_to_world_matrix = sarmObj.matrix_world.to_3x3()
    world_to_target_matrix = tarmObj.matrix_world.inverted().to_3x3()

    source_x_axis = {}
    bpy.ops.object.select_all(action='DESELECT')
    sarmObj.select_set(True)
    bpy.context.view_layer.objects.active = sarmObj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='SELECT')

    for boneObj in sarmObj.data.edit_bones:
        source_x_axis[boneObj.name] = source_to_world_matrix @ boneObj.x_axis

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    tarmObj.select_set(True)
    bpy.context.view_layer.objects.active = tarmObj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='SELECT')

    if all == True:
        for boneObj in tarmObj.data.edit_bones:
            if boneObj.name in source_x_axis:
                align_bone_x_axis(boneObj, world_to_target_matrix @ source_x_axis[boneObj.name])
            else:
                print("rigs::align_bones reports : missing bone", boneObj.name)
    else:
        if bone in source_x_axis:
            align_bone_x_axis(boneObj, world_to_target_matrix @ source_x_axis[bone])
        else:
            print("rigs::align_bones reports : missing bone", bone)

    bpy.ops.object.mode_set(mode='POSE')

    return True







def get_matrix_basis(armature=None, bone=None):
        if isinstance(armature, str) == False:
            armature = armature.name
        if isinstance(bone, str) == False:
            bone = bone.name

        armObj = bpy.data.objects[armature]
        pbmat = armObj.pose.bones[bone].matrix.copy()
        dbmat = armObj.data.bones[bone].matrix.copy()
        dbmatl = armObj.data.bones[bone].matrix_local.copy()
        if armObj.pose.bones[bone].parent:
            pbpmat = armObj.pose.bones[bone].parent.matrix.copy()
            dbpmatl = armObj.data.bones[bone].parent.matrix_local.copy()
        else:
            pbpmat = mathutils.Matrix()
            dbpmatl = mathutils.Matrix()
        if armObj.pose.bones[bone].parent:
            dbpmat = armObj.data.bones[bone].parent.matrix.copy()
        else:
            dbpmat = mathutils.Matrix()
        pbmatI = pbmat.inverted()
        pbpmatI = pbpmat.inverted()
        dbpmatlI = dbpmatl.inverted()
        rp = pbpmat @ dbpmatlI @ dbmatl
        rp_composed = rp.inverted() @ pbmat

        return rp_composed




















def get_matrix_offset(source=None, target=None, bone=None):
        if isinstance(source, str) == False:
            source = source.name
        if isinstance(target, str) == False:
            target = target.name
        if isinstance(bone, str) == False:
            bone = bone.name
        sarmObj = bpy.data.objects[source]
        tarmObj = bpy.data.objects[target]

        pbmat = tarmObj.data.bones[bone].matrix_local.copy()
        dbmat = sarmObj.data.bones[bone].matrix.copy()
        dbmatl = sarmObj.data.bones[bone].matrix_local.copy()
        if sarmObj.pose.bones[bone].parent:
            pbpmat = sarmObj.data.bones[bone].parent.matrix_local.copy()
            dbpmatl = tarmObj.data.bones[bone].parent.matrix_local.copy()
        else:
            pbpmat = mathutils.Matrix()
            dbpmatl = mathutils.Matrix()
        if sarmObj.pose.bones[bone].parent:
            dbpmat = tarmObj.data.bones[bone].parent.matrix.copy()
        else:
            dbpmat = mathutils.Matrix()
        pbmatI = pbmat.inverted()
        pbpmatI = pbpmat.inverted()
        dbpmatlI = dbpmatl.inverted()
        rp = pbpmat @ dbpmatlI @ dbmatl
        rp_composed = rp.inverted() @ pbmat

        MF = rp_composed.inverted() 

        return MF






def set_bone_groups(armObj):
    if isinstance(armObj, str):
        armObj = bpy.data.objects[armObj]

    state = utils.get_state()

    armObj.select_set(True)
    utils.activate(armObj)

    
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.group_add()
    armObj.pose.bone_groups.active.name = mod_data.rig_group_mbones
    armObj.pose.bone_groups.active.color_set = mod_data.rig_group_mtheme
    bpy.ops.pose.group_add()
    armObj.pose.bone_groups.active.name = mod_data.rig_group_vbones
    armObj.pose.bone_groups.active.color_set = mod_data.rig_group_vtheme
    bpy.ops.pose.group_add()
    armObj.pose.bone_groups.active.name = mod_data.rig_group_abones
    armObj.pose.bone_groups.active.color_set = mod_data.rig_group_atheme
    bpy.ops.pose.group_add()
    armObj.pose.bone_groups.active.name = mod_data.rig_group_nbones
    armObj.pose.bone_groups.active.color_set = mod_data.rig_group_ntheme

    for bone in skel.avatar_skeleton:
        if bone not in armObj.data.bones:
            continue
        if skel.avatar_skeleton[bone]['type'] == 'bone':
            group = mod_data.rig_group_mbones
        elif skel.avatar_skeleton[bone]['type'] == 'attachment':
            if " " in bone:
                group = mod_data.rig_group_nbones
            else:
                group = mod_data.rig_group_abones
        else:
            group = mod_data.rig_group_vbones
        armObj.pose.bones[bone].bone_group = armObj.pose.bone_groups[group]

    bpy.ops.object.mode_set(mode='OBJECT')

    utils.set_state(state)

    return True















def make_complete(
    armature=None, connect=False, rotate=False, fix=False,
    strip=True, resize=False, align=False, match=False):

    
    
    
    
    
    
    
    

    armObj = armature
    if isinstance(armObj,str):
        armObj = bpy.data.objects[armObj]

    print("rigs::make_complete : arguments on entry:")
    if armature == None:
        print("armature :", armature)
    else:
        print("armature : ", armObj.name)
    print("fix : ", fix)
    print("strip : ", strip)
    print("match : ", match)
    print("align : ", align)
    print("rotate : ", rotate )
    print("resize : ", resize)
    print("connect : ", connect)

    
    
    
    bad_bones = []
    good_bones = []
    for boneObj in armObj.data.bones:
        bone = boneObj.name
        if bone not in skel.avatar_skeleton:
            bad_bones.append(bone)
        else:
            good_bones.append(bone)

    if len(bad_bones) == len(armObj.data.bones):
        print("rigs::make_complete : None of the bones in the rig matched, there's nothing to do")
        popup("No bones matched, this is not a compatible rig", "Error", "ERROR")
        print(bad_bones)
        return False
    print("Any mismatched bones are listed here")
    print(bad_bones)
    print("Any matching bones are listed here")
    print(good_bones)
    print("Bad bone count:", len(bad_bones))
    print("Rig bone count:", len(armObj.data.bones))

    
    armObj.select_set(True)
    if armObj.select_get() == False:
        print("The associated armature couldn't be selected")
        popup("The associated armature could not be selected", "Error", "ERROR")
        return False

    
    
    


    
    missing_bones = set()
    for bone in skel.avatar_skeleton:
        if bone not in armObj.data.bones:
            missing_bones.add(bone)

    state = utils.get_state()

    bb_import = bpy.context.scene.bb_import

    
    
    
    
    
    
    
    
    

    
    
    
    newObj = build_rig(rig_class="pos", connect=connect, rotate=rotate)

    
    if resize == True:
        
        for o in bpy.context.selected_objects:
            o.select_set(False)
        newObj.select_set(True)
        utils.activate(newObj)
        
        newObj.dimensions.z = armObj.dimensions.z
        
        
        newObj.scale.y = newObj.scale.z
        newObj.scale.x = newObj.scale.z
        
        bpy.ops.object.transform_apply( rotation=False, location=False, scale=True )

    
    for o in bpy.context.selected_objects:
        o.select_set(False)
    armObj.select_set(True)
    utils.activate(armObj)

    
    armObj['bentobuddy'] = globals.version

    
    
    
    
    
    
    
    
    
    bpy.ops.object.mode_set(mode='EDIT')
    
    
    tailed = {}
    M = mathutils.Matrix()  
    
    

    if fix == True:
        print("The option (fix) is enabled, preparing the source first before conversion, this could damage it..")
        for boneObj in armObj.data.edit_bones:
            bone = boneObj.name
            
            if bone in skel.avatar_skeleton:
                if skel.avatar_skeleton[bone]['connected'] == True:
                    if boneObj.parent:
                        pBone = boneObj.parent
                        if pBone.name in skel.avatar_skeleton:
                            roll = pBone.roll
                            pBone.tail = boneObj.head.copy()
                            
                            
                            pBone.roll = roll
                            tailed[pBone.name] = M 
                        else:
                            print("Missing parent from skel, required for moving tail to head", pBone.name)
            else:
                
                
                
                print("Incompatible bone found, visual cleanup only", bone)
                if boneObj.parent:
                    if len(boneObj.parent.children) == 1:
                        pBone = boneObj.parent
                        pBone.tail = boneObj.head.copy()
                        tailed[pBone.name] = M

    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.update()

    
    if align == True:
        print("rigs::make_complete : align requested")
        align_bones(source=newObj, target=armObj, all=True)

    
    
    for boneObj in armObj.data.bones:
        if boneObj.name in tailed:
            tailed[boneObj.name] = boneObj.matrix_local.copy()

    
    for o in bpy.context.selected_objects:
        o.select_set(False)
    armObj.select_set(True)
    utils.activate(armObj)

    
    
    
    
    
    
    if strip == True:
        remove_these = []
        bpy.ops.object.mode_set(mode='EDIT')
        for boneObj in armObj.data.edit_bones:
            if boneObj.name not in skel.avatar_skeleton:
                remove_these.append(boneObj)
        for boneObj in remove_these:
            armObj.data.edit_bones.remove(boneObj)
        bpy.ops.object.mode_set(mode='OBJECT')

    
    
    
    
    
    
    for boneObj in newObj.pose.bones:
        bone = boneObj.name

        
        if bone not in armObj.data.bones:
            continue
        
        if bone in tailed:
            M = tailed[bone]
        
        else:
            l, r, s = armObj.data.bones[bone].matrix_local.decompose()
            L = mathutils.Matrix.Translation(l)
            R = boneObj.matrix.to_quaternion().to_matrix().to_4x4()
            S = mathutils.Matrix()
            for i in range(3):
                S[i][i] = s[i]
            M = L @ R @ S
        newObj.pose.bones[bone].matrix = M
        bpy.context.view_layer.update()

    
    apply_pose(newObj)

    
    
    

    bpy.ops.object.mode_set(mode='EDIT')
    
    for bone in skel.avatar_skeleton:
        if bone not in armObj.data.bones:
            newBone = armObj.data.edit_bones.new(bone)

    
    print("rigs::make_complete : warning - bone matching sequence may damage devkits")
    
    
    for boneObj in armObj.data.edit_bones:
        bone = boneObj.name
        
        if bone not in missing_bones:
            
            
            if match == False:
                continue
        boneObj.head = newObj.data.bones[bone].head_local.copy()
        boneObj.tail = newObj.data.bones[bone].tail_local.copy()
        boneObj.roll = utils.get_bone_roll(newObj.data.bones[bone].matrix_local.copy())

    
    for boneObj in armObj.data.edit_bones:
        if boneObj.name not in skel.avatar_skeleton:
            armObj.data.edit_bones.remove(boneObj)
    
    
    
    
    for boneObj in armObj.data.edit_bones:
        boneObj.use_connect = False
    for boneObj in armObj.data.edit_bones:
        bone = boneObj.name
        parent = skel.avatar_skeleton[bone]['parent']
        if parent != "":
            boneObj.parent = armObj.data.edit_bones[parent]







    
    
    if 1 == 0:
    
        for boneObj in armObj.data.edit_bones:
            if boneObj.parent:
                if len(boneObj.parent.children) == 1:
                    tail = boneObj.parent.tail.copy()
                    roll = boneObj.parent.roll
                    boneObj.parent.tail = boneObj.head.copy()
                    
                    boneObj.parent.roll = roll

                    
                    if boneObj.parent.length < 0.01:
                        
                        print("Parent bone tail to head would result in a bone too small, restoring", boneObj.parent.name)
                        boneObj.parent.tail = tail
                        
                        boneObj.parent.roll = roll


                        

    bpy.ops.object.mode_set(mode='OBJECT')

    
    if len(armObj.data.bones) != len(newObj.data.bones):
        
        armObj.select_set(False)
        newObj.select_set(True)
        utils.activate(newObj)
        bpy.ops.object.delete()
        utils.set_state(state)
        print("The imported armature is not compatible with SL, use the dae importer instead.")
        print("The imported dae file is not SL compatible and was removed from the scene.")
        print("If you are attempting to import and repair a dae file use the Bento Buddy dae importer instead.")
        return False

    
    set_bone_groups(armObj)

    
    for boneObj in newObj.data.bones:
        boneObj.hide = False
    groups = newObj.get('bb_bone_groups')
    if groups != None:
        for g in groups:
            groups[g] = 1
        newObj['bb_bone_groups'] = groups

    armObj.select_set(False)
    newObj.select_set(True)
    utils.activate(newObj)
    bpy.ops.object.delete()

    
    groups = {}
    for l in visible.layers:
        groups[l] = 1
    armObj['bb_bone_groups'] = groups
    for boneObj in armObj.data.bones:
        boneObj.hide = False

    utils.set_state(state)

    return True










