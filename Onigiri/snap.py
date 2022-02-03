

import bpy
import traceback
import mathutils
from . import utils





if 1 == 1:

    props = {}

    props['actor_group_base'] = "Actor Base"
    props['actor_theme_base'] = "THEME10"
    props['actor_group_mapped'] = "Actor Mapped"
    props['actor_theme_mapped'] = "THEME01"

    props['director_group_base'] = "Director Base"
    props['director_theme_base'] = "THEME09"
    props['director_group_mapped'] = "Director Mapped"
    props['director_theme_mapped'] = "THEME04"

    
    
    props['actor_bone'] = ""
    props['director_bone'] = ""

    
    
    
    
    
    
    
    props['symmetry_running'] = False
    
    
    
    
    
    props['actor_side_difference'] = ""
    props['director_side_difference'] = ""
    
    props['actor_symmetry_display'] = "Choose Side A"
    props['director_symmetry_display'] = "Choose Side A"
    
    props['actor_side_a'] = "" 
    props['actor_side_b'] = ""
    props['director_side_a'] = ""
    props['director_side_b'] = ""
    
    
    
    props['actor_side_a_pre'] = ""
    props['actor_side_a_post'] = ""
    props['actor_side_b_pre'] = ""
    props['actor_side_b_post'] = ""
    props['director_side_a_pre'] = ""
    props['director_side_a_post'] = ""
    props['director_side_b_pre'] = ""
    props['director_side_b_post'] = ""

    
    
    props['last_selected_actor_bone'] = ""
    props['last_selected_director_bone'] = ""

    
    
    
    
    
    

    
    
    props['undo'] = {}








def get_relations(object):
    armObj = object
    if isinstance(object, str):
        armObj = bpy.data.objects[object]

    relations = {}
    for boneObj in armObj.pose.bones:
        bone = boneObj.name
        children = boneObj.children
        parent = ""
        if boneObj.parent:
            parent = boneObj.parent.name
        relations[bone] = {}
        relations[bone]['parent'] = parent
        relations[bone]['children'] = []
        for child in children:
            cname = child.name
            relations[bone]['children'].append(cname)

    return relations






def get_director(armature=None):
    if armature == None:
        return False
    armObj = armature
    if isinstance(armature, str):
        if armature not in bpy.context.scene.objects:
            return False
        obj = bpy.data.objects
        armObj = obj[armature]

    
    
    outRig = armObj.get('bb_snap_actor', None)
    inRig = armObj.get('bb_snap_director', None)

    
    
    if outRig == None and inRig == None:
        return False

    

    
    if outRig != None:
        return armObj
    
    if inRig.name not in bpy.context.scene.objects:
        return False
    
    return inRig


































def apply_map(director=None, actor=None):

    
    
    
    
    

    inRig = director
    outRig = actor

    bb_snap = bpy.context.window_manager.bb_snap

    follow = bb_snap.snap_follow
    
    

    release = bb_snap.snap_release

    
    
    
    
    
    if follow == True:
        snap = True
    else:
        snap = False

    
    for boneObj in inRig.pose.bones:
        boneObj.bone_group = None
    for boneObj in outRig.pose.bones:
        boneObj.bone_group = None

    
    director_group_base = props['director_group_base']
    actor_group_base = props['actor_group_base']
    for boneObj in inRig.pose.bones:
        boneObj.bone_group = inRig.pose.bone_groups[director_group_base]
    for boneObj in outRig.pose.bones:
        boneObj.bone_group = outRig.pose.bone_groups[actor_group_base]

    
    rename = inRig.get('bb_onemap_rename', {})
    director_group_mapped = props['director_group_mapped']
    actor_group_mapped = props['actor_group_mapped']

    for rename_in_bone in rename.keys():
        if rename_in_bone not in inRig.pose.bones:
            continue
        rename_out_bone = rename[rename_in_bone]
        if rename_out_bone not in outRig.data.bones:
            continue
        inRig.pose.bones[rename_in_bone].bone_group = inRig.pose.bone_groups[director_group_mapped]
        outRig.pose.bones[rename_out_bone].bone_group = outRig.pose.bone_groups[actor_group_mapped]

    
    
    for boneObj in inRig.data.bones:
        boneObj.select = False
    for boneObj in outRig.data.bones:
        boneObj.select = False


    
    
    


    
    
    
    
    
    
    if snap == True:

        
        
        
        mapped = set()
        bpy.context.view_layer.objects.active = outRig
        old_mode = bpy.context.mode
        sloc = inRig.location
        tloc = outRig.matrix_world.inverted().to_translation()
        floc = (sloc + tloc)
        bpy.ops.object.mode_set(mode='EDIT')
        for boneObj in inRig.data.bones:
            sbone = boneObj.name
            if sbone in rename:
                tbone = rename[sbone]
                
                if tbone not in outRig.data.bones:
                    continue
                mapped.add(tbone)
                head = mathutils.Vector(inRig.data.bones[sbone]['head'])
                tail = mathutils.Vector(inRig.data.bones[sbone]['tail'])
                roll = inRig.data.bones[sbone]['roll']
                outRig.data.edit_bones[tbone].head = (head + floc)
                outRig.data.edit_bones[tbone].tail = (tail + floc)
                outRig.data.edit_bones[tbone].roll = roll


        
        if release == False:
            for boneObj in outRig.data.bones:
                tbone = boneObj.name
                if tbone not in mapped:
                    head = outRig.data.bones[tbone]['head'].to_list()
                    tail = outRig.data.bones[tbone]['tail'].to_list()
                    roll = outRig.data.bones[tbone]['roll']
                    outRig.data.edit_bones[tbone].head = head
                    outRig.data.edit_bones[tbone].tail = tail
                    outRig.data.edit_bones[tbone].roll = roll
        bpy.ops.object.mode_set(mode='OBJECT')

    
    
    
    
    
    
    else:
        bpy.ops.object.mode_set(mode='EDIT')
        for boneObj in outRig.data.edit_bones:
            head = boneObj['head'].to_list()
            tail = boneObj['tail'].to_list()
            roll = boneObj['roll']
            boneObj.head = head
            boneObj.tail = tail
            boneObj.roll = roll
        bpy.ops.object.mode_set(mode='OBJECT')

    
    
    
    
    
    rename_rev = {}
    for bone in rename.keys():
        tbone = rename[bone]
        rename_rev[tbone] = bone
    if follow == True:
        for boneObj in outRig.pose.bones:
            abone = boneObj.name
            dbone = ""
            influence = 0
            if abone in rename_rev:
                influence = 1
                dbone = rename_rev[abone]
                if dbone not in inRig.data.bones: 
                    dbone = ""
            for cObj in boneObj.constraints:
                if cObj.type == 'COPY_ROTATION' or cObj.type == 'COPY_LOCATION':
                    cObj.subtarget = dbone
                    cObj.influence = influence

    else:
        
        for boneObj in outRig.pose.bones:
            for cObj in boneObj.constraints:
                if cObj.type == 'COPY_ROTATION' or cObj.type == 'COPY_LOCATION':
                    cObj.influence = 0
    
    outRig.select_set(True)
    bpy.context.view_layer.objects.active = outRig



    
    
    
    if release == False:
        
        bpy.ops.object.mode_set(mode='EDIT')
        for boneObj in outRig.data.edit_bones:
            bone = boneObj.name
            if bone in rename_rev:
                continue
            matrix = mathutils.Matrix(outRig.data.bones[bone]['matrix_local'])
            head = mathutils.Vector(outRig.data.bones[bone]['head'])
            tail = mathutils.Vector(outRig.data.bones[bone]['tail'])
            roll = outRig.data.bones[bone]['roll']
            outRig.data.edit_bones[bone].head = head
            outRig.data.edit_bones[bone].tail = tail
            outRig.data.edit_bones[bone].roll = roll
            outRig.data.edit_bones[bone].matrix = matrix

        bpy.ops.object.mode_set(mode='POSE')
        for boneObj in outRig.pose.bones:
            if boneObj.name in rename_rev:
                continue
            M = mathutils.Matrix(boneObj.bone['matrix'])
            ML = mathutils.Matrix(boneObj.bone['matrix_local'])
            boneObj.matrix = ML
    
    
    



    
    outRig.select_set(True)
    bpy.context.view_layer.objects.active = outRig
    bpy.ops.object.mode_set(mode='POSE')
    

    
    
    for boneObj in inRig.data.bones:
        boneObj.select = False
    for boneObj in outRig.data.bones:
        boneObj.select = False

    
    props['actor_bone'] = ""
    props['director_bone'] = ""

    return True








def update_map(inRig=None, anchor=None, target=None, report=False):
    if inRig == None:
        print("No inRig")
        return False
    if anchor == None and target == None:
        if report == True:
            print("I need at least one bone to deal with, either an anchor or target, you gave me None")
        return False
    if anchor != None:
        if report == True:
            print("Got anchor")
    if target != None:
        if report == True:
            print("Got target")

    if isinstance(inRig, str):
        inRig = bpy.data.objects[inRig]
    if isinstance(anchor, str) == False:
        anchor = anchor.name
    if isinstance(target, str) == False:
        target = tbone.name

    if inRig.get('bb_onemap_rename') == None:
        if report == True:
            print("The inRig doesn't have a rename map")
        return False
    rename_map = inRig['bb_onemap_rename'].to_dict()
    rename_rev = {}
    for bone in rename_map:
        rename_rev[ rename_map[bone] ] = bone

    
    if target in rename_rev:
        old_anchor = rename_rev[target]
        if report == True:
            print("Removing old anchor found from target", anchor)
        rename_map.pop(old_anchor, "")

    rename_map[anchor] = target
    inRig['bb_onemap_rename'] = rename_map

    return True





def save_map(input=None, file=None):
    import json
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
        print("snap::save_map reports: There's nothing to make a map with")
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












def get_difference(a,b):

    
    
    
    al = a.lower()
    bl = b.lower()
    if al == bl:
        print("Matching strings have no difference")
        return False

    
    
    a_list = list(a)
    b_list = list(b)
    if a_list[0] != b_list[0] and a_list[-1] != b_list[-1]:
        print("The book-ends do not have compatible puppy tails")
        return False

    
    
    
    
    
    
    
    
    
    
    
    
    

    
    count_a = len(a)
    count_b = len(b)
    count = count_a
    if count_b < count_a:
        count = count_b
    
    
    a_list = list(a)
    b_list = list(b)
    pre = ""
    for i in range(count):
        if a_list[i] == b_list[i]:
            pre += a_list[i] 
        else:
            break

    a_list = list(a[::-1])
    b_list = list(b[::-1])
    suf_rev = ""
    for i in range(count):
        if a_list[i] == b_list[i]:
            suf_rev += a_list[i] 
        else:
            break
    suf = suf_rev[::-1]
    print("pre:", pre)
    print("suf:", suf)

    
    
    
    a_side = a.strip(pre)
    a_side = a_side.strip(suf)
    b_side = b.strip(pre)
    b_side = b_side.rstrip(suf)

    print("a_side:", a_side)
    print("b_side:", b_side)

    
    
    

    
    return a_fix, b_fix














