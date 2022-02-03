


import re
import os
import bpy
import math
import struct
import decimal
import mathutils


from collections import OrderedDict
from bpy_extras.io_utils import axis_conversion

from  .mod_data import *
from .mod_settings import *
from . import joint_data
from . import mod_flags

script_dir = os.path.dirname(os.path.abspath(__file__))
presets_path    =   bb_settings['paths']['presets']
data_path       =   bb_settings['paths']['data']





if 1 == 1:

    props = {}
    props['anim_data'] = {}
    props['anim_header_types'] = {"<class 'str'>", "<class 'int'>", "<class 'float'>"}
    props['anim_editable_types'] = {
        "base_priority",
        "loop_in_point",
        "loop_out_point",
        "ease_in_duration",
        "ease_out_duration",
        "loop",
        "hand_pose"
        }

    props['file_in_base'] = ""




def load_anim(file=None):

    f = open(file, "rb")
    content = f.read()
    f.close()

    
    if len(content) < 36: 
        print("The header is not a valid SL anim header")
        return False

    
    

    header = {}
    header['version'] = int.from_bytes(content[:2], byteorder='little', signed=False)
    header['sub_version'] = int.from_bytes(content[2:4], byteorder='little', signed=False)
    header['base_priority'] = int.from_bytes(content[4:8], byteorder='little', signed=True)
    header['duration'] = struct.unpack('f', content[8:12])[0]

    if header['version'] != 1 or header['sub_version'] != 0:
        print("The header is corrupt or not a compatible SL file")
        return False

    
    
    start = 12
    stride = 0
    
    
    for c in content[start:-1]:
        stride += 1
        if c == 0:
            break
    
    
    
    emote_bytes = content[start:start+stride-1]
    header['emote_name'] = emote_bytes.decode('utf-8')

    
    start += stride

    header['loop_in_point'] = struct.unpack('f', content[start:start+4])[0]
    header['loop_out_point'] = struct.unpack('f', content[start+4:start+8])[0]
    start += 8
    header['loop'] = int.from_bytes(content[start:start+4], byteorder='little', signed=True)
    start +=4
    header['ease_in_duration'] = struct.unpack('f', content[start:start+4])[0]
    header['ease_out_duration'] = struct.unpack('f', content[start+4:start+8])[0]
    start += 8
    header['hand_pose'] = int.from_bytes(content[start:start+4], byteorder='little', signed=False)
    start += 4
    header['num_joints'] = int.from_bytes(content[start:start+4], byteorder='little', signed=False)
    start += 4

    
    joints = {}
    joint_count = 0
    stride = 0
    while joint_count < header['num_joints']:
        joint_count += 1
        
        character_count = 0
        for c in content[start:-1]:
            character_count += 1 
            if c == 0:
                break

        joint_bytes = content[start:start+character_count-1] 
        start += character_count

        joint_name = joint_bytes.decode('utf-8')
        joints[joint_name] = {}

        joints[joint_name]['joint_priority'] = int.from_bytes(content[start:start+4], byteorder='little', signed=True)
        start += 4

        
        joints[joint_name]['num_rot_keys'] = int.from_bytes(content[start:start+4], byteorder='little', signed=True)
        start += 4
        rot_count = 0
        joints[joint_name]['rot'] = [] 

        while rot_count < joints[joint_name]['num_rot_keys']:
            rot_count += 1
            rots = []
            
            rots.append( int.from_bytes(content[start:start+2], byteorder='little', signed=False) )
            start += 2
            rots.append( int.from_bytes(content[start:start+2], byteorder='little', signed=False) )
            start += 2
            rots.append( int.from_bytes(content[start:start+2], byteorder='little', signed=False) )
            start += 2
            rots.append( int.from_bytes(content[start:start+2], byteorder='little', signed=False) )
            start += 2
            joints[joint_name]['rot'].append(rots) 

        
        joints[joint_name]['num_pos_keys'] = int.from_bytes(content[start:start+4], byteorder='little', signed=True)
        start += 4
        loc_count = 0
        joints[joint_name]['loc'] = [] 

        while loc_count < joints[joint_name]['num_pos_keys']:
            loc_count += 1
            locs = []
            
            locs.append( int.from_bytes(content[start:start+2], byteorder='little', signed=False) )
            start += 2
            locs.append( int.from_bytes(content[start:start+2], byteorder='little', signed=False) )
            start += 2
            locs.append( int.from_bytes(content[start:start+2], byteorder='little', signed=False) )
            start += 2
            locs.append( int.from_bytes(content[start:start+2], byteorder='little', signed=False) )
            start += 2
            joints[joint_name]['loc'].append(locs) 

    constraints = {}
    constraints['num_constraints'] = int.from_bytes(content[start:start+4], byteorder='little', signed=True)
    constraints['binary_end'] = content[start:-1] 

    print("version:", header['version'])
    print("sub version:", header['sub_version'])
    print("base priority:", header['base_priority'])
    print("duration:",  '{:f}'.format(header['duration']) )
    print("emote name:", header['emote_name'])
    print("loop in point:",  '{:f}'.format(header['loop_in_point']) )
    print("loop out point:",  '{:f}'.format(header['loop_out_point']) )
    print("hand pose:", header['hand_pose'])
    print("num joints:", header['num_joints'])

    file_decoded = {}
    file_decoded['header'] = header
    file_decoded['joints'] = joints
    file_decoded['constraints'] = constraints


    print("emote name test:", len(header['emote_name']))



    return file_decoded








def save_anim(data=None, file=None):

    header = data['header']
    joints = data['joints']
    constraints = data['constraints']

    file_content = {}
    file_content['header'] = {}
    file_content['header']['version'] = (header['version']).to_bytes(2, byteorder='little')
    file_content['header']['sub_version'] = (header['sub_version']).to_bytes(2, byteorder='little')
    if header['base_priority'] == -1:
        neg_1 = "FFFFFFFF"
        file_content['header']['base_priority'] = bytes.fromhex(neg_1)
    else:
        file_content['header']['base_priority'] = (header['base_priority']).to_bytes(4, byteorder='little')
    file_content['header']['duration'] = struct.pack('f', header['duration'])

    
    
    file_content['header']['emote_name'] = struct.pack("%dsB"%len(header['emote_name']), bytes(header['emote_name'],'utf8') , 0)

    file_content['header']['loop_in_point'] = struct.pack('f', header['loop_in_point'])
    file_content['header']['loop_out_point'] = struct.pack('f', header['loop_out_point'])
    file_content['header']['loop'] = (header['loop']).to_bytes(4, byteorder='little')
    file_content['header']['ease_in_duration'] = struct.pack('f', header['ease_in_duration'])
    file_content['header']['ease_out_duration'] = struct.pack('f', header['ease_out_duration'])

    
    bb_anim_edit = bpy.context.window_manager.bb_anim_edit
    if bb_anim_edit.anim_hand_pose_enabled == True:
        hp = int(bb_edit_anim.anim_hand_pose)
        file_content['header']['hand_pose'] = struct.pack("i", hp)
    else:
        file_content['header']['hand_pose'] = (0).to_bytes(4, byteorder='little')

    file_content['header']['num_joints'] = (header['num_joints']).to_bytes(4, byteorder='little')

    
    
    
    
    
    file_content['joints'] = {}
    for bone in joints:
        file_content['joints'][bone] = {}
        file_content['joints'][bone]['name'] = struct.pack("%dsB"%len(bone), bytes(bone,'utf8') , 0)
        file_content['joints'][bone]['priority'] = struct.pack("i", joints[bone]['joint_priority'])

        file_content['joints'][bone]['num_rot_keys'] = joints[bone]['num_rot_keys'].to_bytes(4, byteorder='little')

        for rot in joints[bone]['rot']:
            
            if file_content['joints'][bone].get('rots') == None:
                file_content['joints'][bone]['rots'] = []
            time_data = struct.pack("H", rot[0])
            x = (rot[1]).to_bytes(2, byteorder='little')
            y = (rot[2]).to_bytes(2, byteorder='little')
            z= (rot[3]).to_bytes(2, byteorder='little')
            file_content['joints'][bone]['rots'].extend(time_data)
            file_content['joints'][bone]['rots'].extend(x)
            file_content['joints'][bone]['rots'].extend(y)
            file_content['joints'][bone]['rots'].extend(z)

        file_content['joints'][bone]['num_pos_keys'] = joints[bone]['num_pos_keys'].to_bytes(4, byteorder='little')

        for loc in joints[bone]['loc']:
            
            if file_content['joints'][bone].get('locs') == None:
                file_content['joints'][bone]['locs'] = []
            time_data = struct.pack("H", loc[0])
            x = (loc[1]).to_bytes(2, byteorder='little')
            y = (loc[2]).to_bytes(2, byteorder='little')
            z= (loc[3]).to_bytes(2, byteorder='little')
            file_content['joints'][bone]['locs'].extend(time_data)
            file_content['joints'][bone]['locs'].extend(x)
            file_content['joints'][bone]['locs'].extend(y)
            file_content['joints'][bone]['locs'].extend(z)
   
    
    
    else:
        file_content['constraints'] = {}
        file_content['constraints']['num_constraints'] = constraints['num_constraints']
        file_content['constraints']['binary_end'] = constraints['binary_end']

    
    file_data = bytearray()
    
    for header in file_content['header']:
        file_data.extend( file_content['header'][header] )
    
    for bone in file_content['joints']:
        file_data.extend( file_content['joints'][bone]['name'] )
        file_data.extend( file_content['joints'][bone]['priority'] )
        file_data.extend( file_content['joints'][bone]['num_rot_keys'] )
        if file_content['joints'][bone].get('rots'):
            file_data.extend( file_content['joints'][bone]['rots'] )
        file_data.extend( file_content['joints'][bone]['num_pos_keys'] )
        if file_content['joints'][bone].get('locs'):
            file_data.extend( file_content['joints'][bone]['locs'] )
    
    file_data.append( file_content['constraints']['num_constraints'] )
    file_data.extend( file_content['constraints']['binary_end'] )

    
    f = open(file, 'wb')
    f.write(file_data)
    f.close()

    return True




def anim_sanity_check(c):
    print("anim_sanity_check reports: handler running")
    return



def get_compatible_bone_list(armature=""):

    obj = bpy.data.objects
    armObj = obj[armature]
    actionObj = armObj.animation_data.action

    
    fcurves = actionObj.fcurves

    
    
    
    

    
    
    
    
    
    
    
    fcurve_paths = {}
    for boneObj in armObj.data.bones:
        path_key = 'pose.bones["' + boneObj.name + '"]'
        fcurve_paths[path_key] = boneObj.name

    
    

    
    frame_data = {}

    
    
    
    
    for fc in fcurves:
        
        
        dp, i = fc.data_path, fc.array_index

        
        
        bone_path, delimiter, transform_type = dp.rpartition('.')

        
        
        if bone_path not in fcurve_paths:
            continue

        
        
        
        real_bone = fcurve_paths[bone_path]

        
        rot_mode = armObj.pose.bones[real_bone].rotation_mode

        
        
        
        

        
        

        if transform_type == 'rotation_quaternion' and rot_mode == 'QUATERNION':
            loc_rot = 'rot'
        elif transform_type == 'rotation_euler' and rot_mode != 'QUATERNION':
            loc_rot = 'rot'
        elif transform_type == 'location':
            loc_rot = 'loc'
        else:
            if bb_settings['debug'] == True:
                print("anim::get_compatible_bone_list reports : wrong transform type, skipping...", transform_type, rot_mode)
            continue


        
        
        
        if real_bone not in frame_data:
            frame_data[real_bone] = {}


        
        
        
        if 'rot' not in frame_data[real_bone]: frame_data[real_bone]['rot'] = {}
        if 'loc' not in frame_data[real_bone]: frame_data[real_bone]['loc'] = {}
        
        


        
        
        if loc_rot not in frame_data[real_bone]:
            frame_data[real_bone][loc_rot] = {}

        
        
        
        
        if 1 == 0:
            for kfp in fc.keyframe_points:

                kfp_interpolation = kfp.interpolation
                kfp_easing = kfp.easing
                kfp_frame = int(kfp.co[0])
                kfp_value = kfp.co[1]

                frame_data[real_bone][loc_rot][kfp_frame] = {
                    "value": kfp_value,
                    "easing": kfp_easing,
                    "interpolation": kfp_interpolation,
                }

    bone_names = list()
    for bone in frame_data:
        bone_names.append(bone)
    
    

    return bone_names









def get_animated_bone_names(armature=""):
    if armature == "":
        print("get_animated_bone_names reports: needs an armature")
        return False

    obj = bpy.data.objects
    armObj = obj[armature]
    actionObj = armObj.animation_data.action

    
    pose_bones = set()
    for fcurve in actionObj.fcurves:
        pose_bone_path = fcurve.data_path.rpartition('.')[0]
        boneObj = armObj.path_resolve(pose_bone_path)
        
        if boneObj.name not in pose_bones:
            
            if boneObj.name in armObj.data.bones:
                coord = None
            for fp in fcurve.keyframe_points:
                if coord == None:
                    
                    coord = fp.co
                
                elif coord == fp.co:
                    continue
                
                else:
                    pose_bones.add(boneObj.name)

    return pose_bones











def is_keyframe(ob, frame, data_path, array_index=-1):
    if ob is not None and ob.animation_data is not None and ob.animation_data.action is not None:
        for fcu in ob.animation_data.action.fcurves:
            if fcu.data_path == data_path:
                if array_index == -1 or fcu.array_index == array_index:
                    return frame in (p.co.x for p in fcu.keyframe_points)
    return False













    
        
            
            
            
                
            
                






def get_keys(transform="", type=""):
    if transform =="":
        print("get_keys reports: need transform")
        return False
    if type == "":
        print("get_keys reports: need type")
        return False

    count = 0 
    return count







def get_frames(armature="", type="active"):
    arm = ""
    if type == "action":
        print("not implemented yet")
        return False
    if type == "active":
        if armature == "":
            print("get_frames reports: needs an armature or action")
            return False
        arm = armature

    if arm == "":
        print("get_frames reports: nothing to work with")
        return False

    
    return True






















def get_rotation_data(armature="", bone="", frame="", frame_data="", matrix_type="pose_matrix_basis"):

    
    
    
    
    

 
    obj = bpy.data.objects
    arm = armature
    jd = joint_data

    
    ac = bpy.context.scene.bb_anim_advanced



    
    
    
    
    

    
    
    
    
    
    
    
    


    
    
    

    
    
    

    
    
    


    matrix_basis = frame_data[bone][frame][matrix_type]




    quat_base = frame_data[bone][frame][matrix_type].to_quaternion()
    
    rot_base = list()
    rot_base.append(quat_base.x)
    rot_base.append(quat_base.y)
    rot_base.append(quat_base.z)

    
    
    
    
    if mod_flags.bb_flags['debug'] == 1:
        res = quat_base.x ** 2 + quat_base.y ** 2 + quat_base.z ** 2 + quat_base.w ** 2
        print("quat result:", res)
























    if mod_flags.bb_flags['debug'] == 1:
        print("== Quats ==========================================================")
        print(rot_base)
        print("===================================================================")




    if ac.disable_axis_conversion == False:
        
        if ac.matrix_converter_enabled == True:
            if mod_flags.bb_flags['debug'] == 1:
                print("========================================================")
                print("debug axis conversion enabled:", bone)
            m = axis_conversion(
                from_forward=ac.ac_from_forward_axis,
                from_up=ac.ac_from_up_axis,
                to_forward=ac.ac_to_forward_axis,
                to_up=ac.ac_to_up_axis).to_4x4()
            rot_mat = m @ matrix_basis

            Q = rot_mat.to_quaternion()
            rot = list()
            rot.append(Q.x)
            rot.append(Q.y)
            rot.append(Q.z)

        
        else:

            if bone in jd.joint_data:

                
                
                if jd.joint_data[bone].get('copy') != "":
                    old_bone = bone
                    bone = jd.joint_data[bone]['copy']

            
            

                A0, A1, A2 = jd.joint_data[bone]['rot_axis_angle']
                C0 = round(rot_base[A0], 4)
                C1 = round(rot_base[A1], 4)
                C2 = round(rot_base[A2], 4)

                
                
                
                
                
                


                
                I0 = C0
                I1 = C1
                I2 = C2
                if jd.joint_data[bone]['rot_axis_inverted'][0] == "-":
                    I0 = -I0
                if jd.joint_data[bone]['rot_axis_inverted'][1] == "-":
                    I1 = -I1
                if jd.joint_data[bone]['rot_axis_inverted'][2] == "-":
                    I2 = -I2


                
                rot = mathutils.Vector((I0, I1, I2))

                if mod_flags.bb_flags['debug'] == 1:
                    print("Bone reorienting:", bone)
                    print("A0, A1, A2:", A0, A1, A2)
                    print("C0, C1, C2:", C0, C1, C2)
                    print("I0, I1, I2:", I0, I1, I2)
                    print("rot:", rot)
            
            
            else:
                rot = rot_base

    
    
    else:
        rot = rot_base

    
    
    
        


    
    
    
    


















    
    

    
    
    
    


    
    
    
    
    
    
    
    


    if mod_flags.bb_flags['debug'] == 1:
        print("final rot:", rot)



    
    
    rot_x, rot_y, rot_z = rot

    x = F32_to_U16(rot_x, -1, 1)
    y = F32_to_U16(rot_y, -1, 1)
    z = F32_to_U16(rot_z, -1, 1)

    
    
    

    if mod_flags.bb_flags['debug'] == 1:
        print("final: x,y,z:", x,y,z)

    return [x, y, z]






    
    
    
    






    
    
        
        
        
    
        
        


    
    
    

    
    
    
    








def get_location_data(armature="", bone="", frame="", frame_data="", matrix_type="pose_matrix_basis"):

    
    
    
    
    
    
    
    

    if bone=="":
        print("get_location_data reports: no bone name to process")
        return False
    if frame=="":
        print("get_location_data reports: no frames to process")
        return False
    if armature=="":
        print("get_location_data reports: no armature to process")
        return False

    obj = bpy.data.objects
    arm = armature
    jd = joint_data




    
    ac = bpy.context.scene.bb_anim_advanced

    
    
    



    
    
    
    
    


    
    
    
    
    


    
    
    
    
    
    
    

    
    
    
    
    
    
    

    
    
    if ac.disable_axis_conversion == False:

        
        if ac.matrix_converter_enabled == True:
            if mod_flags.bb_flags['debug'] == 1:
                print("========================================================")
                print("debug axis conversion enabled:", bone)
            m = axis_conversion(
                from_forward=ac.ac_from_forward_axis,
                from_up=ac.ac_from_up_axis,
                to_forward=ac.ac_to_forward_axis,
                to_up=ac.ac_to_up_axis).to_4x4()
            
            
            l = frame_data[bone][frame][matrix_type]
            loc_mat = m @ l
            loc = loc_mat.to_translation()

        else:
            
            
            
            

            
            
            
            

            
            
            





            
            
                
                
                
                












            

            
            
            
            

            
            
            
            
            



            

            
            
                
            
                
                
                
                
                

            loc_base = frame_data[bone][frame][matrix_type].to_translation()

            print("get_location_data reports: loc_base from matrix_type -", loc_base)












            
            if bone in jd.joint_data:

                
                
                if jd.joint_data[bone].get('copy') != "":
                    old_bone = bone
                    bone = jd.joint_data[bone]['copy']

                
                
                
                A0, A1, A2 = jd.joint_data[bone]['loc_axis_angle']

                
                

                
                
                
                C0 = round(loc_base[A0], 4)
                C1 = round(loc_base[A1], 4)
                C2 = round(loc_base[A2], 4)

                
                
                
                
                


                
                I0 = C0
                I1 = C1
                I2 = C2
                if jd.joint_data[bone]['loc_axis_inverted'][0] == "-":
                    I0 = -I0
                if jd.joint_data[bone]['loc_axis_inverted'][1] == "-":
                    I1 = -I1
                if jd.joint_data[bone]['loc_axis_inverted'][2] == "-":
                    I2 = -I2




                
                loc = mathutils.Vector((I0, I1, I2))

                if 1 == 1:

                    print("Bone reorienting:", bone)
                    print("A0, A1, A2:", A0, A1, A2)
                    print("C0, C1, C2:", C0, C1, C2)
                    print("I0, I1, I2:", I0, I1, I2)
                    print("loc:", loc)

            
            
            
            
            else:
                
                
                loc = frame_data[bone][frame][matrix_type].to_translation()


    else:
        
        
        
        
        loc = frame_data[bone][frame][matrix_type].to_translation()

    
    
    if ac.disable_joint_offsets == False:

        
        
        
        
        
        loc_offset = obj[arm]['delta_loc_parent'][bone].to_list()

        print("delta_loc_parent / bone:" ,loc_offset, bone)

        
        if bone in jd.joint_data:

            
            
            if jd.joint_data[bone].get('copy') != "":
                old_bone = bone
                bone = jd.joint_data[bone]['copy']

            
            P0 = jd.joint_data[bone]['loc_offset_angle'][0]
            P1 = jd.joint_data[bone]['loc_offset_angle'][1]
            P2 = jd.joint_data[bone]['loc_offset_angle'][2]

            
            L0 = loc_offset[P0]
            L1 = loc_offset[P1]
            L2 = loc_offset[P2]

            if mod_flags.bb_flags['debug'] == 1:
                print("offset loc after Vector:", loc)

            
            
            
            
            
            

            if jd.joint_data[bone]['loc_offset_inverted'][0] == "-":
                I0 = -L0
            else:
                I0 = L0
            if jd.joint_data[bone]['loc_offset_inverted'][1] == "-":
                I1 = -L1
            else:
                I1 = L1
            if jd.joint_data[bone]['loc_offset_inverted'][2] == "-":
                I2 = -L2
            else:
                I2 = L2

            
            loc += mathutils.Vector((I0, I1, I2))


            print("inverted loc after Vector:", loc)
            print("------------------------------------------------")


        
        
        
        
        
        





    
    
    
    
    
    
    
    
    
    loc_x, loc_y, loc_z = loc

    

    x = F32_to_U16(loc_x/LL_MAX_PELVIS_OFFSET, -1, 1)
    y = F32_to_U16(loc_y/LL_MAX_PELVIS_OFFSET, -1, 1)
    z = F32_to_U16(loc_z/LL_MAX_PELVIS_OFFSET, -1, 1)


    if 1 == 1:
        print("|||||||||||||||||||||||||||||||||||||||||||||||||")
        print("after everything - bone: loc_x, loc_y, loc_z")
        print(bone, loc_x, loc_y, loc_z)
        print("rounded:", round(loc_x, 4), round(loc_y, 4), round(loc_z, 4))
        print("bytes x,y,z:", x, y, z)
        print("|||||||||||||||||||||||||||||||||||||||||||||||||")

    
    
    
    
















    
    

    return [x, y, z]





U16MAX = 65535
OOU16MAX = 1.0/(float)(U16MAX)
LL_MAX_PELVIS_OFFSET = 5.0







    

    
    
    
    
    
        
    

    
    
    
        
    
    




def llclamp(a, minval, maxval):
    if a<minval:
        return minval
    if a>maxval:
        return maxval
    return a


def F32_to_U16(val, lower, upper):
    val = llclamp(val, lower, upper);
    
    val -= lower;
    val /= (upper - lower);
    
    
    return int(math.floor(val*U16MAX))


def U16_to_F32(ival, lower, upper):
    if ival < 0 or ival > U16MAX:
        raise Exception("U16 out of range: "+ival)
    val = ival*OOU16MAX
    delta = (upper - lower)
    val *= delta
    val += lower

    max_error = delta*OOU16MAX;

    
    if abs(val) < max_error:
        val = 0.0
    return val




    
    
    
    
    
    
    
    





    
    
    
    
    
    
    
    
    




def alter_keys(transform="", bone=""):
    

    transform_start_int = transform + "_start_int"
    transform_end_int = transform + "_end_int"
    altered_keys = {}
    altered_keys[bone] = {transform: list()}

    return altered_keys



















def set_frame(frame=0):
    bpy.context.scene.frame_set(frame)
    return



