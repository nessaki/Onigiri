import bpy
import math
import mathutils





if 1 == 1:

    props = {}
    props['frozen_rig'] = ""
    props['frozen_bones'] = []
































def snap(sarm=None, tarms=[], type="rig", source=[]):
    bbm = bpy.context.window_manager.bb_mapper
    obj = bpy.data.objects
    sarmObj = obj[sarm]

    
    old_mode = bpy.context.mode
    if old_mode == 'EDIT_ARMATURE':
        old_mode = 'EDIT'
    if old_mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    
    for o in bpy.context.selected_objects:
        o.select_set(False)

    
    
    
    for tarm in tarms:
        if tarm not in obj:
            print("shifter::snap: an armature sent to this function does not exist:", tarm)
            popup("Missing rig", "Error", "ERROR")
            return False

    
    
    if type == "map":
        bm = obj[sarm]['bone_map'].to_dict()
        good_targets = list()
        
        for sbone in bm:
            (tarm, tbone), = bm[sbone].items()
            if tarm not in obj:
                print("shift::snap reports : target armature missing from scene:", tarm)
                continue
            if tarm not in good_targets:
                
                
                good_targets.append(tarm)
        if len(good_targets) == 0:
            print("shift::snap reports : no target armatures to process")
            return False
        
        bone_map = {}
        for sbone in bm:
            (tarm, tbone), = bm[sbone].items()
            if tarm not in good_targets or tbone not in obj[tarm].data.bones:
                print("Skipping missing items", sbone, tarm, tbone)
                continue
            if sbone not in bone_map:
                bone_map[sbone] = {}
            bone_map[sbone] = {tarm : tbone}

    
    
    
    
    
    elif type == "rig":
        bone_source = list()
        
        if len(source) == 0:
            for boneObj in obj[sarm].data.bones:
                bone_source.append(boneObj.name)
        else:
            bone_source = source
        
        sbone_count = len(bone_source)
        tbone_count = 0
        bone_map = {}
        good_targets = list()
        for tarm in tarms:
            
            good_targets.append(tarm)
            for boneObj in obj[tarm].data.bones:
                bone_map[sbone] = {tarm : tbone}
                tbone_count += 1
                if tbone_count == sbone_count:
                    break

    else:
        print("shifter::snap: got unrecognized map type:", type)
        return False

    

    
    
    
    

    
    bpy.context.view_layer.update()
    current_frame = bpy.context.scene.frame_current

    
    sarmObj.select_set(True)
    bpy.context.view_layer.objects.active = sarmObj
    bpy.ops.object.mode_set(mode='EDIT')
    for boneObj in sarmObj.data.edit_bones:
        boneObj.use_connect = False
        
        boneObj.use_inherit_rotation = False
    bpy.ops.object.mode_set(mode='OBJECT')

    
    bpy.context.view_layer.objects.active = sarmObj
    bpy.ops.object.duplicate()
    glueObj = bpy.context.object
    glueObj.name = "_SNAP_RIG"
    glue = glueObj.name

    
    bpy.ops.object.mode_set(mode='POSE')
    bpy.context.view_layer.objects.active = glueObj
    
    obj = bpy.data.objects
    for g in obj[glue].pose.bone_groups:
        obj[glue].pose.bone_groups.remove(g)
    
    bpy.ops.pose.group_add()
    glueObj.pose.bone_groups.active.name = "Glue"
    glueObj.pose.bone_groups.active.color_set = 'THEME07'
    
    for boneObj in glueObj.pose.bones:
        boneObj.bone_group = glueObj.pose.bone_groups["Glue"]

    
    
    
    
    bpy.ops.object.mode_set(mode='EDIT')
    for boneObj in glueObj.data.edit_bones:
        boneObj.parent = None
    bpy.ops.object.mode_set(mode='OBJECT')

    
    
    
    for b in obj[tarm].pose.bones:
        for c in b.constraints:
            b.constraints.remove(c)
    for b in obj[glue].pose.bones:
        for c in b.constraints:
            b.constraints.remove(c)

    
    

    lname = "BB Copy Loc"
    rname = "BB Copy Rot"

    obj[glue].select_set(False)
    obj[sarm].select_set(True)
    bpy.context.view_layer.objects.active = obj[sarm]
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

    obj[sarm].select_set(False)

    
    
    
    
    
    

    
    
    
    for sbone in bone_map:
        (tarm, tbone), = bone_map[sbone].items()
        tBone = obj[tarm].pose.bones[tbone]
        gBone = glueObj.pose.bones[sbone]
        tmat = obj[tarm].matrix_world.copy()
        gmat = obj[glue].matrix_world.copy()
        tm = tmat @ tBone.matrix
        l = tm.to_translation()
        Lt = mathutils.Matrix.Translation(l)
        R = tm.to_quaternion().to_matrix().to_4x4()
        S = mathutils.Matrix()
        l = glueObj.matrix_world.inverted().to_translation()
        Lg = mathutils.Matrix.Translation(l)
        M = Lg @ Lt @ R @ S
        gBone.matrix = M

    bpy.context.view_layer.update()

    obj[glue].select_set(True)
    bpy.context.view_layer.objects.active = obj[glue]

    
    
    
    
    
    bpy.ops.object.mode_set(mode='EDIT')
    edit_mats = {}
    for sbone in bone_map:
        (tarm, tbone), = bone_map[sbone].items()
        head = obj[tarm].matrix_world @ obj[tarm].pose.bones[tbone].head.copy()
        tail = obj[tarm].matrix_world @ obj[tarm].pose.bones[tbone].tail.copy()
        glueObj.data.edit_bones[sbone].head = head - glueObj.location
        glueObj.data.edit_bones[sbone].tail = tail - glueObj.location

    bpy.ops.object.mode_set(mode='OBJECT')

    
    
    obj[sarm].select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    for boneObj in obj[sarm].data.edit_bones:
        bone = boneObj.name
        head = obj[glue].pose.bones[bone].head.copy()
        tail = obj[glue].pose.bones[bone].tail.copy()
        boneObj.head = head
        boneObj.tail = tail

    bpy.ops.object.mode_set(mode='OBJECT')
    sarmObj.select_set(False)
    glueObj.select_set(True)
    bpy.context.view_layer.objects.active = glueObj

    
    for gbone in bone_map:
        (tarm, tbone), = bone_map[gbone].items() 
        glueObj.data.bones[gbone].select = True
        glueObj.data.bones.active = glueObj.data.bones[gbone]
        bc = glueObj.pose.bones[gbone].constraints
        bc.new('COPY_LOCATION')
        bc['Copy Location'].target = obj[tarm]
        bc['Copy Location'].subtarget = tbone
        bc['Copy Location'].target_space = 'WORLD'
        bc['Copy Location'].owner_space = 'WORLD'
        bc['Copy Location'].influence = 1
        bc['Copy Location'].name = lname
        glueObj.data.bones[gbone].select = False
    for gbone in bone_map:
        (tarm, tbone), = bone_map[gbone].items() 
        glueObj.data.bones[gbone].select = True
        glueObj.data.bones.active = glueObj.data.bones[gbone]
        bc = glueObj.pose.bones[gbone].constraints
        bc.new('COPY_ROTATION')
        bc['Copy Rotation'].target = obj[tarm]
        bc['Copy Rotation'].subtarget = tbone
        bc['Copy Rotation'].target_space = 'WORLD'
        bc['Copy Rotation'].owner_space = 'WORLD'
        bc['Copy Rotation'].influence = 1
        bc['Copy Rotation'].name = rname
        glueObj.data.bones[gbone].select = False

    
    
    if bbm.get('clean') == None:
        bbm['clean'] = {}
    if bbm['clean'].get('objects') == None:
        bbm['clean']['objects'] = list()
    if bbm['clean'].get('constraints') == None:
        bbm['clean']['constraints'] = list()

    if glue not in bbm['clean']['objects']:
        
        temp_list = list(bbm['clean']['objects'])
        temp_list.append(glue)
        bbm['clean']['objects'] = temp_list
    if tarm not in bbm['clean']['constraints']:
        
        temp_list = list(bbm['clean']['constraints'])
        temp_list.append(glue)
        bbm['clean']['constraints'] = temp_list





    
    
    
    

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.frame_set(current_frame)
    for o in bpy.context.selected_objects:
        o.select_set(False)
    glueObj.select_set(True)
    bpy.context.view_layer.objects.active = glueObj
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.armature_apply(selected=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    glueObj.select_set(False)
    sarmObj.select_set(True)
    bpy.context.view_layer.objects.active = sarmObj
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.armature_apply(selected=False)
    bpy.ops.object.mode_set(mode='OBJECT')

    
    
    
    
    
    
    
            
    morph_reset(good_targets)
    shaper = True
    if shaper == True:
        
        bpy.context.view_layer.update()
        
        for o in bpy.context.selected_objects:
            o.select_set(False)

        
        glueObj.select_set(True)
        bpy.context.view_layer.objects.active = glueObj

        
        
        bpy.ops.object.mode_set(mode='POSE')

        
        
        pose_mats = {}
        for boneObj in obj[glue].pose.bones:
            pose_mats[boneObj.name] = boneObj.matrix.copy()

        
        
        
        

        
        
        
        
        
        st_start = 1
        st_range = 2
        for tarm in good_targets:
            move_keys(arm=tarm, start=st_start, range=st_range, marker=True)

        
        
        print("Setting glue frame to:", st_start)
        bpy.context.scene.frame_set(st_start)
        
        
        
        for bone in bone_map:
            
            glueObj.data.bones[bone].select = True
            glueObj.pose.bones[bone].constraints[lname].influence = 0
            glueObj.pose.bones[bone].constraints[rname].influence = 0
            glueObj.pose.bones[bone].constraints[lname].keyframe_insert(data_path='influence')
            glueObj.pose.bones[bone].constraints[rname].keyframe_insert(data_path='influence')
        for boneObj in glueObj.pose.bones:
            bone = boneObj.name
            
            glueObj.pose.bones[bone].keyframe_insert(data_path="location", frame=st_start)
            glueObj.pose.bones[bone].keyframe_insert(data_path="rotation_quaternion", frame=st_start)
            glueObj.pose.bones[bone].keyframe_insert(data_path="rotation_euler", frame=st_start)

        

        
        R = mathutils.Matrix.Rotation(math.radians(1), 4, 'X')
        
        L = mathutils.Matrix.Translation((0.1, 0.0, 0.0))
        
        S = mathutils.Matrix()
        
        M = L @ R @ S

        
        bpy.context.scene.frame_set(st_start+1)

        
        for bone in bone_map:
            glueObj.pose.bones[bone].constraints[lname].influence = 0
            glueObj.pose.bones[bone].constraints[rname].influence = 0
            glueObj.pose.bones[bone].constraints[lname].keyframe_insert(data_path='influence')
            glueObj.pose.bones[bone].constraints[rname].keyframe_insert(data_path='influence')

        
        for boneObj in glueObj.pose.bones:
            mat = boneObj.matrix.copy()
            boneObj.matrix = mat @ M

        bpy.context.view_layer.update()
        for boneObj in glueObj.pose.bones:
            bone = boneObj.name
            glueObj.data.bones[bone].select = True
            glueObj.pose.bones[bone].keyframe_insert(data_path="location", frame=st_start+1)
            glueObj.pose.bones[bone].keyframe_insert(data_path="rotation_quaternion", frame=st_start+1)
            glueObj.pose.bones[bone].keyframe_insert(data_path="rotation_euler", frame=st_start+1)

        bpy.context.scene.frame_set(st_start+2)

        
        for bone in pose_mats:
            glueObj.pose.bones[bone].matrix = pose_mats[bone]
        bpy.context.view_layer.update()

        for boneObj in glueObj.pose.bones:
            bone = boneObj.name
            glueObj.data.bones[bone].select = True
            glueObj.pose.bones[bone].keyframe_insert(data_path="location", frame=st_start+2)
            glueObj.pose.bones[bone].keyframe_insert(data_path="rotation_quaternion", frame=st_start+2)
            glueObj.pose.bones[bone].keyframe_insert(data_path="rotation_euler", frame=st_start+2)

        
        for bone in bone_map: 
            glueObj.pose.bones[bone].constraints[lname].influence = 1
            glueObj.pose.bones[bone].constraints[rname].influence = 1
            glueObj.pose.bones[bone].constraints[lname].keyframe_insert(data_path='influence')
            glueObj.pose.bones[bone].constraints[rname].keyframe_insert(data_path='influence')


    
    if bbm.get('clean') == None:
        bbm['clean'] = {}
    if bbm['clean'].get('objects') == None:
        bbm['clean']['objects'] = list()
    if bbm['clean'].get('constraints') == None:
        bbm['clean']['constraints'] = list()

    if glue not in bbm['clean']['objects']:
        
        temp_list = list(bbm['clean']['objects'])
        temp_list.append(glue)
        bbm['clean']['objects'] = temp_list
    if tarm not in bbm['clean']['constraints']:
        
        temp_list = list(bbm['clean']['constraints'])
        temp_list.append(glue)
        bbm['clean']['constraints'] = temp_list

    bpy.context.scene.frame_set(current_frame)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    glueObj.hide_set(True)
    return True

























def morph(
    sarm=None, bone_map={},
    frame_start=1, frame_range=3, reverse=False, peak=2,
    location=True, rotation=True, scale=False):

    ss = bpy.context.scene.bb_shifter
    obj = bpy.data.objects
    sarmObj = obj[sarm]

    print("shifter::morph Sanity check")
    bpy.context.view_layer.update()
    frame_current = bpy.context.scene.frame_current

    bpy.context.scene.frame_set(frame_start)


    
    
    

    
    if frame_range < 3:
        reverse = False
        print("reverse requires at least 3 frames,", frame_range, "was given so reverse is disabled")
    else:
        
        
        morph_end_frame = frame_start + frame_range - 1
        if peak > morph_end_frame - 1:
            reverse = False
            print("peak too high, reverse has been disabled")
        if peak < frame_start + 1:
            reverse = False
            print("peak too low, reverse has been disabled")


    

    
    frame_end = frame_start + frame_range - 1

    

    
    old_mode = bpy.context.mode
    if old_mode == 'EDIT_ARMATURE':
        old_mode = 'EDIT'
    if old_mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    
    for o in bpy.context.selected_objects:
        o.select_set(False)

    

    
    
    
    sarmObj.select_set(True)
    bpy.context.view_layer.objects.active = sarmObj
    bpy.ops.object.mode_set(mode='EDIT')
    for boneObj in sarmObj.data.edit_bones:
        boneObj.use_connect = False
        
        boneObj.use_inherit_rotation = False
    bpy.ops.object.mode_set(mode='OBJECT')

    
    
    
    bpy.context.view_layer.objects.active = sarmObj
    bpy.ops.object.duplicate()
    glueObj = bpy.context.object
    glueObj.name = "_MORPH_RIG"
    glue = glueObj.name

    
    bpy.ops.object.mode_set(mode='POSE')
    bpy.context.view_layer.objects.active = glueObj
    
    obj = bpy.data.objects
    for g in obj[glue].pose.bone_groups:
        obj[glue].pose.bone_groups.remove(g)
    
    bpy.ops.pose.group_add()
    glueObj.pose.bone_groups.active.name = "Glue"
    glueObj.pose.bone_groups.active.color_set = 'THEME07'
    
    for boneObj in glueObj.pose.bones:
        boneObj.bone_group = glueObj.pose.bone_groups["Glue"]

    
    
    
    
    bpy.ops.object.mode_set(mode='EDIT')
    for boneObj in glueObj.data.edit_bones:
        boneObj.parent = None
    bpy.ops.object.mode_set(mode='OBJECT')

    
    
    
    
    
    
    for b in obj[glue].pose.bones:
        for c in b.constraints:
            b.constraints.remove(c)
    for b in obj[sarm].pose.bones:
        for c in b.constraints:
            b.constraints.remove(c)

    
    

    lname = "BB Copy Location"
    rname = "BB Copy Rotation"
    sname = "BB Copy Scale"

    obj[glue].select_set(False)
    obj[sarm].select_set(True)
    bpy.context.view_layer.objects.active = obj[sarm]
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
    sarmObj.select_set(False)
    glueObj.select_set(True)
    bpy.context.view_layer.objects.active = glueObj
    bpy.ops.object.mode_set(mode='POSE')

    
    
    
    for gbone in bone_map:
        (tarm, tbone), = bone_map[gbone].items() 
        glueObj.data.bones[gbone].select = True
        glueObj.data.bones.active = glueObj.data.bones[gbone]
        bc = glueObj.pose.bones[gbone].constraints
        bc.new('COPY_LOCATION')
        bc['Copy Location'].target = obj[tarm]
        bc['Copy Location'].subtarget = tbone
        bc['Copy Location'].target_space = 'WORLD'
        bc['Copy Location'].owner_space = 'WORLD'
        bc['Copy Location'].influence = 0
        bc['Copy Location'].keyframe_insert(data_path='influence')
        bc['Copy Location'].name = lname
        glueObj.data.bones[gbone].select = False
    for gbone in bone_map:
        (tarm, tbone), = bone_map[gbone].items() 
        glueObj.data.bones[gbone].select = True
        glueObj.data.bones.active = glueObj.data.bones[gbone]
        bc = glueObj.pose.bones[gbone].constraints
        bc.new('COPY_ROTATION')
        bc['Copy Rotation'].target = obj[tarm]
        bc['Copy Rotation'].subtarget = tbone
        bc['Copy Rotation'].target_space = 'WORLD'
        bc['Copy Rotation'].owner_space = 'WORLD'
        bc['Copy Rotation'].influence = 0
        bc['Copy Rotation'].keyframe_insert(data_path='influence')
        bc['Copy Rotation'].name = rname
        glueObj.data.bones[gbone].select = False
    for gbone in bone_map:
        (tarm, tbone), = bone_map[gbone].items() 
        glueObj.data.bones[gbone].select = True
        glueObj.data.bones.active = glueObj.data.bones[gbone]
        bc = glueObj.pose.bones[gbone].constraints
        bc.new('COPY_SCALE')
        bc['Copy Scale'].target = obj[tarm]
        bc['Copy Scale'].subtarget = tbone
        bc['Copy Scale'].target_space = 'WORLD'
        bc['Copy Scale'].owner_space = 'WORLD'
        bc['Copy Scale'].influence = 0
        bc['Copy Scale'].keyframe_insert(data_path='influence')
        bc['Copy Scale'].name = sname
        glueObj.data.bones[gbone].select = False




    
    if reverse == True:
        bpy.context.scene.frame_set(peak)
        for gbone in bone_map:
            glueObj.pose.bones[gbone].constraints[lname].influence = 1
            glueObj.pose.bones[gbone].constraints[lname].keyframe_insert(data_path='influence')
            glueObj.pose.bones[gbone].constraints[rname].influence = 1
            glueObj.pose.bones[gbone].constraints[rname].keyframe_insert(data_path='influence')
            glueObj.pose.bones[gbone].constraints[sname].influence = 1
            glueObj.pose.bones[gbone].constraints[sname].keyframe_insert(data_path='influence')
        
        bpy.context.scene.frame_set(frame_end)
        for gbone in bone_map:
            glueObj.pose.bones[gbone].constraints[lname].influence = 0
            glueObj.pose.bones[gbone].constraints[lname].keyframe_insert(data_path='influence')
            glueObj.pose.bones[gbone].constraints[rname].influence = 0
            glueObj.pose.bones[gbone].constraints[rname].keyframe_insert(data_path='influence')
            glueObj.pose.bones[gbone].constraints[sname].influence = 0
            glueObj.pose.bones[gbone].constraints[sname].keyframe_insert(data_path='influence')
    
    
    else:
        bpy.context.scene.frame_set(frame_end)
        for gbone in bone_map:
            glueObj.pose.bones[gbone].constraints[lname].influence = 1
            glueObj.pose.bones[gbone].constraints[lname].keyframe_insert(data_path='influence')
            glueObj.pose.bones[gbone].constraints[rname].influence = 1
            glueObj.pose.bones[gbone].constraints[rname].keyframe_insert(data_path='influence')
            glueObj.pose.bones[gbone].constraints[sname].influence = 1
            glueObj.pose.bones[gbone].constraints[sname].keyframe_insert(data_path='influence')

    bpy.ops.object.mode_set(mode='OBJECT')

    
    
    
    
    
    
    for boneObj in obj[glue].pose.bones:
        if len(boneObj.constraints) == 0:
            continue
        if location == False:
            boneObj.constraints[lname].mute = True
        if rotation == False:
            boneObj.constraints[rname].mute = True
        if scale == False:
            boneObj.constraints[sname].mute = True

    
    bpy.context.scene.frame_set(frame_current)

    
    obj[sarm]['morph'] = {}
    obj[sarm]['morph']['name'] = glue
    
    
    
    obj[sarm]['morph']['transforms'] = {}
    obj[sarm]['morph']['transforms']['location'] = lname
    obj[sarm]['morph']['transforms']['rotation'] = rname
    obj[sarm]['morph']['transforms']['scale'] = sname

    
    
    glueObj.select_set(False)
    sarmObj.select_set(True)
    bpy.context.view_layer.objects.active = sarmObj

    return True








def nothing_to_do_here(): 

    
    
    
    
    
    if 1 == 0:
        for sbone in bone_map:
            (tarm, tbone), = bone_map[sbone].items()
            tBone = obj[tarm].pose.bones[tbone]
            gBone = glueObj.pose.bones[sbone]
            tmat = obj[tarm].matrix_world.copy()
            gmat = obj[glue].matrix_world.copy()
            tm = tmat @ tBone.matrix
            l = tm.to_translation()
            Lt = mathutils.Matrix.Translation(l)
            R = tm.to_quaternion().to_matrix().to_4x4()
            S = mathutils.Matrix()
            l = glueObj.matrix_world.inverted().to_translation()
            Lg = mathutils.Matrix.Translation(l)
            M = Lg @ Lt @ R @ S
            gBone.matrix = M
            
            
        bpy.context.view_layer.update()

    
    
    
    if 1 == 0:
        obj[glue].select_set(True)
        bpy.ops.object.mode_set(mode='EDIT')
        edit_mats = {}
        for sbone in bone_map:
            edit_mats[sbone] = obj[glue].data.edit_bones[sbone].matrix.copy()
            (tarm, tbone), = bone_map[sbone].items()
            head = obj[tarm].matrix_world @ obj[tarm].pose.bones[tbone].head.copy()
            tail = obj[tarm].matrix_world @ obj[tarm].pose.bones[tbone].tail.copy()
            glueObj.data.edit_bones[sbone].head = head - glueObj.location
            glueObj.data.edit_bones[sbone].tail = tail - glueObj.location
        bpy.ops.object.mode_set(mode='OBJECT')
    if 1 == 0:
        obj[sarm].select_set(True)
        bpy.ops.object.mode_set(mode='EDIT')
        edit_mats = {}
        for boneObj in obj[sarm].data.edit_bones:
            bone = boneObj.name
            head = obj[glue].pose.bones[bone].head.copy()
            tail = obj[glue].pose.bones[bone].tail.copy()
            boneObj.head = head
            boneObj.tail = tail

        bpy.ops.object.mode_set(mode='POSE')

        
        for dBone in glueObj.data.bones:
            dBone.select = True
        bpy.ops.pose.transforms_clear()
        bpy.ops.pose.armature_apply()
        bpy.ops.object.mode_set(mode='OBJECT')
        glueObj.select_set(False)
        sarmObj.select_set(True)
        bpy.context.view_layer.objects.active = sarmObj
        bpy.ops.object.mode_set(mode='POSE')

        for dBone in sarmObj.data.bones:
            dBone.select = True
        bpy.ops.pose.transforms_clear()
        bpy.ops.pose.armature_apply()





def morph_reset(arms=[]):
    if len(arms) == 0:
        return
    obj = bpy.data.objects
    for arm in arms:
        if arm not in obj:
            continue
        if obj[arm].type != 'ARMATURE':
            continue
        if obj[arm].animation_data != None:
            if obj[arm].animation_data.action.get('morph') != None:
                frame_start = obj[arm].animation_data.action['morph']['frame_start']
                frame_range = obj[arm].animation_data.action['morph']['frame_range']
                print("morph restore to frame", frame_start)
                for fcurve in obj[arm].animation_data.action.fcurves:
                    for point in fcurve.keyframe_points:
                        if point.co.x >= frame_start: 
                            point.co.x -= frame_range
                del obj[arm].animation_data.action['morph']
    return







def move_keys(arm=None, start=1, range=2, marker=False):
    obj = bpy.data.objects
    if arm in obj:
        armObj = obj[arm]
        if armObj.animation_data != None:
            animObj = armObj.animation_data
            frame_start, frame_end = armObj.animation_data.action.frame_range
            for fcurve in animObj.action.fcurves:
                for point in fcurve.keyframe_points:
                    
                    if point.co.x >= start:
                        point.co.x += range
            if marker == True:
                animObj.action['morph'] = {'frame_start' : start, 'frame_range' : range } 

        else:
            print("no animation data to alter")
            return False
    return True





def freeze(sarm):

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
    glueObj.pose.bone_groups.active.color_set = 'THEME01'
    
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
        conObj = bc.new('COPY_TRANSFORMS')
        conObj.target = glueObj
        conObj.subtarget = sbone
        conObj.target_space = 'WORLD'
        conObj.owner_space = 'WORLD'
        conObj.influence = 1
        conObj.name = "BB Copy TRS"

    
    if 1 == 0:
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




def stabilize(sarm=None, tarm=None, type="map"):
    
    pass










def pose_to(sarm=None, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1], start=1, frame_range=4, current=False, pingpong=False):
    if sarm == None:
        print("morph_to reports: nothing to do")
        return False

    obj = bpy.data.objects
    if sarm not in obj:
        print("morph_to reports: object missing -", sarm)
        return False

    
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    
    bpy.context.view_layer.update()
    current_frame = bpy.context.scene.frame_current

    
    
    if current == True:
        frame_start = current_frame
        frame_stop = frame_start + frame_range
    else:
        frame_start = start
        frame_stop = frame_start + frame_range

    glue = freeze(sarm)
    if glue == False:
        print("morph_to reports: freeze returned False")
        return False

    
    for o in bpy.context.selected_objects:
        o.select_set(False)

    glueObj = obj[glue]
    glueObj.select_set(True)
    bpy.context.view_layer.objects.active = glueObj

    
    R90 = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'X')

    L = mathutils.Matrix.Translation(location)
    eu = mathutils.Euler(map(math.radians, rotation), 'XYZ')
    R = eu.to_matrix().to_4x4()
    
    S = mathutils.Matrix()
    for i in range(3):
        S[i][i] = scale[i]
    M = L @ R @ S


    
    

    glueObj.animation_data_clear()

    bpy.context.scene.frame_set(frame_start)

    
    pose_mats = {}
    for boneObj in glueObj.pose.bones:
        bone = boneObj.name
        pose_mats[bone] = boneObj.matrix.copy()

    
    for boneObj in glueObj.pose.bones:
        bone = boneObj.name
        glueObj.pose.bones[bone].keyframe_insert(data_path="location", frame=frame_start)
        glueObj.pose.bones[bone].keyframe_insert(data_path="rotation_quaternion", frame=frame_start)
        glueObj.pose.bones[bone].keyframe_insert(data_path="rotation_euler", frame=frame_start)
        glueObj.pose.bones[bone].keyframe_insert(data_path="scale", frame=frame_start)

    


    bpy.context.scene.frame_set(frame_start+frame_range-1)

    
    for boneObj in glueObj.pose.bones:
        bone = boneObj.name
        boneObj.matrix = M @ pose_mats[bone]

    bpy.context.view_layer.update()

    
    
        
        
        
        
        

    
    for boneObj in glueObj.pose.bones:
        bone = boneObj.name
        glueObj.pose.bones[bone].keyframe_insert(data_path="location", frame=frame_start+frame_range-1)
        glueObj.pose.bones[bone].keyframe_insert(data_path="rotation_quaternion", frame=frame_start+frame_range-1)
        glueObj.pose.bones[bone].keyframe_insert(data_path="rotation_euler", frame=frame_start+frame_range-1)
        glueObj.pose.bones[bone].keyframe_insert(data_path="scale", frame=frame_start+frame_range-1)

    bpy.context.view_layer.update()

    

    
    bpy.context.scene.frame_set(current_frame)



    return True




def popup(message = "", title = "Message Box", icon =  'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
    return









