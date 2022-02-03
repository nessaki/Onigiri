

import bpy
import json
import mathutils
import traceback
from . import rigutils
from . import utils









if 1 == 1:

    

    
    
    
    props = {}

    
    
    props['follow'] = True

    
    
    
    
    
    
    props['bb_onemap_state'] = False

    
    
    props['bb_onemap_director'] = ""
    props['bb_onemap_actor'] = ""

    
    
    
    props['input_bone'] = ""
    props['output_bone'] = ""

    
    
    
    
    props['reskin_bone'] = ""
    props['move_bone'] = ""

    
    
    
    props['group_input_name'] = ""
    props['group_input_bone'] = ""
    props['group_reskin_bones'] = [] 
    props['group_reskin_name'] = [] 
    props['group_output_name'] = ""
    props['group_output_bone'] = ""

    
    props['last_input_bone'] = ""
    props['last_output_bone'] = ""

    
    
    
    props['view_reskin_bones'] = ""

    
    props['target'] = ""

    
    props['HALT'] = False

    
    
    
    
    
    
    
    
    
    
    
    
    

    
    input_groups = {
        "Rename": 'THEME04',
        "Reskin": 'THEME09',
        "Anchor": 'THEME10',
        "Branch": 'THEME03',
        "Move": 'THEME02',
        "Selected": 'THEME07',
        }
    output_groups = {
        "Output": 'THEME01',
        "Selected": 'THEME07',
        }








def get_director(armature=None):
    if armature == None:
        return False
    armObj = armature
    if isinstance(armature, str):
        obj = bpy.data.objects
        armObj = obj[armature]
        if armature not in bpy.context.scene.objects:
            return False

    
    
    outRig = armObj.get('bb_onemap_actor', None)
    inRig = armObj.get('bb_onemap_director', None)

    
    
    if outRig == None and inRig == None:
        return False

    

    
    if outRig != None:
        return armObj
    
    if inRig.name not in bpy.context.scene.objects:
        return False
    
    return inRig






def apply_map(input=None, output=None):
    inRig = input
    outRig = output

    
    for boneObj in inRig.pose.bones:
        boneObj.bone_group = None
    for boneObj in outRig.pose.bones:
        boneObj.bone_group = None

    rename = inRig.get('bb_onemap_rename', {})
    reskin = inRig.get('bb_onemap_reskin', {})
    for rename_in_bone in rename:
        if rename_in_bone not in inRig.pose.bones:
            continue
        rename_out_bone = rename[rename_in_bone]
        inRig.pose.bones[rename_in_bone].bone_group = inRig.pose.bone_groups['Rename']
        outRig.pose.bones[rename_out_bone].bone_group = outRig.pose.bone_groups['Output']
        reskin_bones = reskin.get(rename_in_bone, [])
        for bone in reskin_bones:
            
            
            if bone not in inRig.pose.bones:
                continue
            inRig.pose.bones[bone].bone_group = inRig.pose.bone_groups['Reskin']

    return True






def update_map(input=None, output=None, rename=None, reskin=None, controllers=True):
    inRig = input
    outRig = output

    state = utils.get_state()

    if rename == None:
        rename = inRig.get('bb_onemap_rename')
    
    if rename == None:
        print("onemap::update_map : no rename map")
        return False
    if reskin == None:
        reskin = inRig.get('bb_onemap_reskin')
    if reskin == None:
        print("onemap::update_map : no reskin map, adding empty")
        reskin = {}

    bb_onemap = bpy.context.scene.bb_onemap

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    if controllers == True:
        
        if bb_onemap.onemap_follow == True:
            
            
            
            frame_current = bpy.context.scene.frame_current
            has_action = False
            if inRig.animation_data != None:
                if inRig.animation_data.action != None:
                    has_action = True
                    frame_start = inRig.animation_data.action.frame_range[0]
            if has_action == False:
                    frame_start = bpy.context.scene.frame_start
            bpy.context.scene.frame_set(frame_start)

            proxyRig = inRig.get('bb_onemap_proxy')
            if utils.is_valid(proxyRig):
                
                
                
                
                
                

                
                
                
                
                
                for boneObj in proxyRig.pose.bones:
                    for C in boneObj.constraints:
                        C.influence = 0

                
                proxyRig.select_set(True)
                bpy.context.view_layer.objects.active = proxyRig

                
                
                
                
                
                
                
                bpy.ops.object.mode_set(mode='EDIT')
                for boneObj in proxyRig.data.edit_bones:
                    boneObj.head = boneObj['head']
                    boneObj.tail = boneObj['tail']
                    boneObj.roll = boneObj['roll']
                bpy.ops.object.mode_set(mode='OBJECT')

                
                
                for boneObj in proxyRig.pose.bones:
                    dBone = boneObj.bone
                    
                    
                    proxyRig.pose.bones[boneObj.name].matrix = mathutils.Matrix(dBone['matrix_local'])
                
                
                

                
                
                
                
                for boneObj in inRig.pose.bones:
                    
                    
                    
                    
                    
                    cname = boneObj['bb_onemap_cname']
                    if boneObj.constraints.get(cname) != None:
                        conObj = boneObj.constraints[cname]
                        if boneObj.name not in rename:
                            conObj.influence = 0
                        else:
                            
                            
                            
                            
                            tbone = rename[boneObj.name]
                            tMat = boneObj.bone.matrix_local.copy() 
                            matrix_local = mathutils.Matrix(proxyRig.data.bones[tbone]['matrix_local'])
                            M = utils.compose_transforms(matrix_in=tMat, matrix_out=matrix_local, location=False, rotation=True, scale=False)
                            
                            proxyRig.pose.bones[tbone].matrix = M
                            

                            
                            
                            conObj.subtarget = tbone
                            conObj.influence = 1

                
                for bone in rename:
                    tbone = rename[bone]
                    if tbone in proxyRig.pose.bones:
                        boneObj = proxyRig.pose.bones[tbone]
                        cname = boneObj['bb_onemap_cname']
                        if boneObj.constraints.get(cname) != None:
                            proxyRig.data.bones.active = boneObj.bone
                            conObj = boneObj.constraints[cname]
                            conObj.subtarget = tbone
                            conObj.influence = 1
                            
                            
                            

            
            bpy.context.scene.frame_set(frame_current)
 
       
        else:
            for boneObj in inRig.pose.bones:
                cname = boneObj['bb_onemap_cname']
                if boneObj.constraints.get(cname) != None:
                    conObj = boneObj.constraints[cname]
                    conObj.influence = 0

    
    
    

    
    for boneObj in inRig.pose.bones:
        boneObj.bone_group = None
    for boneObj in outRig.pose.bones:
        boneObj.bone_group = None



    
    for rename_in_bone in rename:
        if rename_in_bone not in inRig.pose.bones:
            continue
        rename_out_bone = rename[rename_in_bone]
        inRig.pose.bones[rename_in_bone].bone_group = inRig.pose.bone_groups['Rename']
        outRig.pose.bones[rename_out_bone].bone_group = outRig.pose.bone_groups['Output']
        reskin_bones = reskin.get(rename_in_bone, [])
        for bone in reskin_bones:
            if bone not in inRig.pose.bones:
                continue
            inRig.pose.bones[bone].bone_group = inRig.pose.bone_groups['Reskin']

    
    
    
    if 1 == 0:
        if props['group_input_bone'] != "":
                input_bone = props['group_input_bone']
                input_group = props['group_input_name']
                inRig.pose.bones[input_bone].bone_group = inRig.pose.bone_groups[input_group]

        if props['group_output_bone'] != "":
                output_bone = props['group_output_bone']
                output_group = props['group_output_name']
                outRig.pose.bones[output_bone].bone_group = outRig.pose.bone_groups[output_group]

    
    
    
    
    bpy.context.scene.bb_onemap.onemap_message = "Ready!"

    utils.set_state(state)

    return True






def ready(input=None, output=None):

    for o in bpy.context.selected_objects:
        o.select_set(False)
    inRig = input
    outRig = output
    for g in inRig.pose.bone_groups:
        inRig.pose.bone_groups.remove(g)
    for g in outRig.pose.bone_groups:
        outRig.pose.bone_groups.remove(g)

    
    if 1 == 0:
        inRig.select_set(True)
        bpy.context.view_layer.objects.active = inRig
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action = 'SELECT')
        bpy.ops.pose.group_unassign()
        bpy.ops.pose.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        inRig.select_set(False)
        outRig.select_set(True)
        bpy.context.view_layer.objects.active = outRig
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action = 'SELECT')
        bpy.ops.pose.group_unassign()
        bpy.ops.pose.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')

    

    
    outRig.select_set(True)
    bpy.context.view_layer.objects.active = outRig
    bpy.ops.object.mode_set(mode='POSE')

    for group in output_groups:
        bpy.ops.pose.group_add()
        outRig.pose.bone_groups.active.name = group 
        outRig.pose.bone_groups.active.color_set = output_groups[group] 

    outRig.select_set(False)
    inRig.select_set(True)
    bpy.context.view_layer.objects.active = inRig

    
    bpy.ops.object.mode_set(mode='POSE')
    for group in input_groups:
        bpy.ops.pose.group_add()
        inRig.pose.bone_groups.active.name = group 
        inRig.pose.bone_groups.active.color_set = input_groups[group] 

    bpy.ops.object.mode_set(mode='OBJECT')

    
    
    outRig.select_set(True)
    bpy.context.view_layer.objects.active = inRig
    bpy.ops.object.mode_set(mode='POSE')

    
    apply_map(input=inRig, output=outRig)

    return True





def save_map(input=None, file=None):
    inRig = input

    rename = {}
    reskin = {}
    pose = {}
    code = {}
    lock = {}

    if len(inRig.get('bb_onemap_rename', {})) != 0:
        rename = inRig['bb_onemap_rename'].to_dict()
    if len(inRig.get('bb_onemap_reskin', {})) != 0:
        reskin = inRig['bb_onemap_reskin'].to_dict()
    if len(inRig.get('bb_onemap_pose', {})) != 0:
        pose = inRig['bb_onemap_pose'].to_dict()
    if len(inRig.get('bb_onemap_code', {})) != 0:
        code = inRig['bb_onemap_code'].to_dict()
    if len(inRig.get('bb_onemap_lock', {})) != 0:
        lock = inRig['bb_onemap_lock'].to_dict()



    formatted_text = "# Auto Generated by Bento Buddy : Hybrid Map"
    if len(rename) == 0:
        print("onemap::save_map reports: There's nothing to make a map with")
        return False

    if len(code) != 0:
        formatted_text += "\n"
        formatted_text += "code = "
        formatted_text += json.dumps(code, indent=4)

    
    formatted_text += "\n"
    formatted_text += "rename = "
    formatted_text += json.dumps(rename, indent=4)

    if len(reskin) != 0:
        formatted_text += "\n"
        formatted_text += "reskin = "
        formatted_text += json.dumps(reskin, indent=4)

    
    formatted_text += "\n"
    formatted_text += "template_map = "

    
    
    template = {}
    for tbone in rename:
        mbone = rename[tbone]
        template[mbone] = {"Avatar": tbone}
    formatted_text += json.dumps(template, indent=4)

    if len(pose) != 0:
        formatted_text += "\n"
        formatted_text += "pose = "
        formatted_text += json.dumps(pose, indent=4)

    if len(lock) != 0:
        formatted_text += "\n"
        formatted_text += "lock = "
        formatted_text += json.dumps(lock, indent=4)

    try:
        f = open(file, "w", encoding='UTF8')
        f.write(formatted_text)
        f.close()
        print("Saved:", file)
    except Exception as e:
        print("There was a problem opening the file", file, "the following trace might give a clue what happened")
        print(traceback.format_exc())
        return False

    return True






def save_template(template=None, file=None):
    rename = {}





    formatted_text = "# Auto Generated by Bento Buddy : Hybrid Map from template_map"

    for mbone in template:
        (arm, tbone), = template[mbone].items()
        rename[tbone] = mbone

    
    formatted_text += "\n"
    formatted_text += "rename = "
    formatted_text += json.dumps(rename, indent=4)

    
    formatted_text += "\n"
    formatted_text += "template_map = "

    
    
    template = {}
    for tbone in rename:
        mbone = rename[tbone]
        template[mbone] = {"Avatar": tbone}
    formatted_text += json.dumps(template, indent=4)

    try:
        f = open(file, "w", encoding='UTF8')
        f.write(formatted_text)
        f.close()
        print("Saved:", file)
    except Exception as e:
        print("There was a problem opening the file", file, "the following trace might give a clue what happened")
        print(traceback.format_exc())
        return False

    return True









def save_hybrid_template(template=None, file=None):
 
    formatted_text = "# Auto Generated by Bento Buddy : Hybrid Composer"





    
    
    rename = {}
    reskin = {}
    template_map = {}
    code = {}
    pose = {}
    unknown = {}

    
    for map_base in template:
        if map_base == "rename":
            rename = template[map_base]
        elif map_base == "reskin":
            reskin = template[map_base]
        elif map_base == "code":
            code = template[map_base]
        elif map_base == "pose":
            pose = template[map_base]
        elif map_base == "template_map":
            template_map = template[map_base]
        else:
            unknown[map_base] = template[map_base]

    
    
    if len(rename) == 0:
        print("Nothing to write for rename so nothing to write for template_map")

    
    if len(rename) != 0:
        formatted_text += "\n"
        formatted_text += "rename = "
        formatted_text += json.dumps(rename, indent=4)

    
    if len(reskin) != 0:
        formatted_text += "\n"
        formatted_text += "reskin = "
        formatted_text += json.dumps(reskin, indent=4)

    
    
    if len(template_map) == 0:
        if len(rename) != 0:
            formatted_text += "\n"
            formatted_text += "template_map = "
            for tbone in rename:
                mbone = rename[tbone]
                template_map[mbone] = {"Avatar": tbone}
            formatted_text += json.dumps(template_map, indent=4)
    
    else:
        formatted_text += "\n"
        formatted_text += "template_map = "
        for tbone in rename:
            mbone = rename[tbone]
            template_map[mbone] = {"Avatar": tbone}
        formatted_text += json.dumps(template_map, indent=4)

    
    if len(code) != 0:
        formatted_text += "\n"
        formatted_text += "code = "
        formatted_text += json.dumps(code, indent=4)

    
    if len(pose) != 0:
        formatted_text += "\n"
        formatted_text += "pose = "
        formatted_text += json.dumps(pose, indent=4)

    
    for map_type in unknown:
        formatted_text += "\n"
        formatted_text += map_type + " = "
        formatted_text += json.dumps(unknown[map_type], indent=4)

    try:
        f = open(file, "w", encoding='UTF8')
        f.write(formatted_text)
        f.close()
        print("Saved:", file)
    except Exception as e:
        print("There was a problem opening the file", file, "the following trace might give a clue what happened")
        print(traceback.format_exc())
        return False

    return True








def attach_proxy(inRig=None, outRig=None):

    
    
    frame_current = bpy.context.scene.frame_current
    has_action = False
    if inRig.animation_data != None:
        if inRig.animation_data.action != None:
            has_action = True
            frame_start = inRig.animation_data.action.frame_range[0]
    if has_action == False:
            frame_start = bpy.context.scene.frame_start
    bpy.context.scene.frame_set(frame_start)

    
    
    
    for boneObj in inRig.pose.bones:
        for C in boneObj.constraints:
            
            
            cname = boneObj.get('bb_onemap_cname')
            if cname != None:
                if C.name == cname:
                    boneObj.constraints.remove(C)

    duplicate = utils.duplicate(objects=outRig)
    if duplicate == False:
        print("Something went wrong when attempting to copy the rig")
        return False
    proxyRig = duplicate[0]
    proxyRig.name = "BB_Constraint_Proxy"

    
    
    
    rigutils.remove_pose_groups(proxyRig)
    for k in proxyRig.keys():
        del proxyRig[k]

    
    
    
    
    
    
    
    
    for boneObj in proxyRig.data.bones:
        boneObj['matrix_local'] = boneObj.matrix_local.copy()
        boneObj['head'] = boneObj.head_local.copy()
        boneObj['tail'] = boneObj.tail_local.copy()
        boneObj['roll'] = utils.get_bone_roll(boneObj.matrix_local)
    
    
    

    
    
    
    proxyRig.select_set(True)
    bpy.context.view_layer.objects.active = proxyRig
    bpy.ops.object.mode_set(mode='EDIT')
    for boneObj in proxyRig.data.edit_bones:
        boneObj.use_connect = False
        boneObj.parent = None 
        
        

    
    
    bpy.ops.object.mode_set(mode='POSE')
    for boneObj in proxyRig.pose.bones:
        sbone = boneObj.name

        proxyRig.data.bones.active = boneObj.bone 
        bc = boneObj.constraints
        conObj = bc.new('CHILD_OF')
        conObj.target = outRig
        conObj.subtarget = sbone 
        conObj.influence = 1
        
        
        
        
        conObj.target_space = "WORLD";
        conObj.owner_space = "POSE"

        cname = conObj.name

        M = rigutils.invert_bone(source=proxyRig, target=outRig, bone=outRig.pose.bones[sbone])
        conObj.inverse_matrix = M

        
        if 1 == 0:
            context_py = bpy.context.copy()
            context_py["constraint"] = bc.active
            bpy.ops.constraint.childof_clear_inverse(context_py, constraint=cname, owner="BONE")
            bpy.ops.constraint.childof_set_inverse(context_py, constraint=cname, owner="BONE")

        conObj.name = "BB " + cname
        
        
        
        boneObj['bb_onemap_cname'] = conObj.name

        boneObj.bone.hide = True

    bpy.ops.object.mode_set(mode='OBJECT')
    proxyRig.select_set(False)
    inRig['bb_onemap_proxy'] = proxyRig

    
    
    
    inRig.select_set(True)
    bpy.context.view_layer.objects.active = inRig
    bpy.ops.object.mode_set(mode='POSE')
    for boneObj in inRig.pose.bones:
        sbone = boneObj.name
        inRig.data.bones.active = boneObj.bone 
        bc = boneObj.constraints
        conObj = bc.new('COPY_ROTATION')
        conObj.target = proxyRig
        conObj.target_space = 'POSE'
        conObj.owner_space = 'POSE'
        conObj.influence = 0
        cname = conObj.name
        conObj.name = "BB " + cname
        boneObj['bb_onemap_cname'] = conObj.name 
        
        
        
        
        
        
        
        
    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.context.scene.frame_set(frame_current)

    return True









