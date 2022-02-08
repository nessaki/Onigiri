
import os
import bpy
import sys
from . import rigutils
from . import utils
import mathutils









if 1 == 1:

    props = {}

    
    props['groups'] = {}
    props['groups']['actor'] = "actor"
    props['groups']['director'] = "director"
    props['groups']['reskin'] = "reskin"

    props['themes'] = {}
    props['themes']['actor'] = "THEME01"
    props['themes']['director'] = "THEME04"
    props['themes']['reskin'] = "THEME09"

    
    
    props['actor_bone'] = ""
    props['director_bone'] = ""

    
    
    props['anchor_rotation_x'] = "blank"
    props['anchor_rotation_y'] = "blank"
    props['anchor_rotation_z'] = "blank"
    props['anchor_location_x'] = "blank"
    props['anchor_location_y'] = "blank"
    props['anchor_location_z'] = "blank"

    
    props['target_space'] = "LOCAL"
    props['owner_space'] = "LOCAL"
    props['mix_mode'] = 'AFTER'
    
    props['target_space_anchor'] = "LOCAL"
    props['owner_space_anchor'] = "LOCAL"
    props['mix_mode_anchor'] = 'AFTER'

    
    
    
    
    props['rotation_controller'] = "COPY_ROTATION"

    props_axis_dots = {}
    props_axis_dots[True] = "dot_green"
    props_axis_dots[False] = "dot_red"

    
    
    
    props['hip_start'] = None
    props['hip_end'] = None




def get_anchor_state():
    axis = {
        "rotation": ['blank', 'blank', 'blank'],
        "location": ['blank', 'blank', 'blank']
        }
    if len(bpy.context.selected_objects) == 0:
        return axis
    OBJ = bpy.context.selected_objects[0]
    inRig = get_director(OBJ)
    if inRig == False:
        return axis
    outRig = inRig['oni_motion_actor']
    boneObj = outRig.pose.bones[0]
    for C in boneObj.constraints:
        if C .type == 'COPY_LOCATION':
            axis['location'][0] = props_axis_dots[C.use_x]
            axis['location'][1] = props_axis_dots[C.use_y]
            axis['location'][2] = props_axis_dots[C.use_z]
        elif C .type == 'COPY_ROTATION':
            axis['rotation'][0] = props_axis_dots[C.use_x]
            axis['rotation'][1] = props_axis_dots[C.use_y]
            axis['rotation'][2] = props_axis_dots[C.use_z]
    return axis




def get_director(object, report=False):
    OBJ = object
    if isinstance(object, str):
        OBJ = bpy.data.objects[object]

    
    
    aObj = OBJ.get('oni_motion_actor', None)
    dObj = OBJ.get('oni_motion_director', None)

    if report == True:
        print("motion::get_director examining", OBJ.name, "for the director")

        if aObj == None:
            print("motion::get_director : The actor flag is missing so this is not the director")
        else:
            print("motion::get_director : Found actor, this must be the director:", aObj.name)

        if dObj == None:
            print("motion::get_director : The director flag is missing so this is not the actor")
        else:
            print("motion::get_director : Found director", dObj.name, "this must be the actor")

    
    
    if aObj == None and dObj == None:
        if report == True:
            print("motion::get_director : Could not find a director")
        return False

    
    if aObj != None:
        return OBJ

    
    if dObj.name not in bpy.context.scene.objects:
        if report == True:
            print("motion::get_director : dObj was not found in the scene")
        return False

    
    if report == True:
        print("motion::get_director : returning dObj", dObj.name)
    return dObj






def add_constraints(
    source=None, target=None, bone_map=None,
    constraint="COPY_TRANSFORMS", space='WORLD',
    influence=1, location=False, rotation=True, scale=False):

    obj = bpy.data.objects
    sourceObj = obj[source]
    targetObj = obj[target]

    
    
    sourceObj.select_set(True)
    bpy.context.view_layer.objects.active = sourceObj

    missing_targets = []
    missing_sources= []

    for tbone in bone_map.keys():
        sbone = bone_map[tbone]
        if sbone not in sourceObj.data.bones:
            missing_sources.append(sbone)
        if tbone not in targetObj.data.bones:
            missing_targets.append(tbone)

    if len(missing_targets) > 0:
        print("Missing target bones:")
        print(missing_targets)
    if len(missing_sources) > 0:
        print("Missing source bones:")
        print(missing_sources)

    if len(missing_targets) == len(bone_map):
        print("None of the target bones matched for adding constraints (dynamic.add_constraints)")
        return False
    if len(missing_sources) == len(bone_map):
        print("None of the source bones matched for adding constraints (dynamic.add_constraints)")
        return False

    
    bpy.ops.object.mode_set(mode='POSE')
    for tbone in bone_map.keys():
        
        if tbone not in targetObj.data.bones:
            continue
        sbone = bone_map[tbone]
        if sbone not in sourceObj.data.bones:
            continue
        sourceObj.data.bones.active = sourceObj.data.bones[sbone]
        bc = sourceObj.pose.bones[sbone].constraints
        conObj = bc.new(constraint)
        cname = conObj.name
        conObj.target = targetObj
        conObj.subtarget = tbone
        conObj.influence = influence
        if constraint == 'CHILD_OF':
            conObj.use_location_x = location
            conObj.use_location_y = location
            conObj.use_location_z = location
            conObj.use_scale_x = scale
            conObj.use_scale_y = scale
            conObj.use_scale_z = scale
            conObj.use_rotation_x = rotation
            conObj.use_rotation_y = rotation
            conObj.use_rotation_z = rotation
            
            
            conObj.target_space = "WORLD";
            conObj.owner_space = "POSE"
            context_py = bpy.context.copy()
            context_py["constraint"] = bc.active
            utils.set_inverse(context_py, cname)
            
            
            
        else:
            conObj.target_space = space
            conObj.owner_space = space

        conObj.name = "ONI " + cname

        
        sourceObj.pose.bones[sbone]['oni_motion_cname'] = conObj.name


    bpy.ops.object.mode_set(mode='OBJECT')

    

    return True




def retarget_hard(inRig):
    
    state = utils.get_state()
    oni_motion = bpy.context.window_manager.oni_motion

    outRig = rigutils.build_rig(rig_class="pos", rotate=True)
    outRig.select_set(False)

    
    rename_map = inRig['oni_onemap_rename']

    
    good_bones_out = []
    for sbone in rename_map.keys():
        tbone = rename_map[sbone]
        if tbone in outRig.data.bones:
            good_bones_out.append(sbone)

    if 1 == 0:
        if len(good_bones_out) == 0:
            print("motion::retarget_hard = None of the bones in the available map matched your target.")
            print("The glue option requires a map.")
            popup("No mappable bones, see console", "Error", "ERROR")
            utils.set_state(state)
            return False

    inRig['oni_motion_actor'] = outRig
    outRig['oni_motion_director'] = inRig

    inRig.show_in_front = False
    outRig.show_in_front = True
    outRig.data.display_type = 'STICK'
    inRig['oni_motion_display'] = outRig.display_type

    
    
    inRig.select_set(True)
    utils.activate(inRig)
    bpy.ops.object.duplicate()
    proxyRig = bpy.context.object
    proxyRig.name = "RETARGET_PROXY"

    
    
    frame_start = 1
    if proxyRig.animation_data:
        if proxyRig.animation_data.action:
            frame_start = proxyRig.animation_data.action.frame_range[0]
    bpy.context.scene.frame_set(frame_start)
    
    proxyRig.animation_data_clear()
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.armature_apply()
    bpy.ops.object.mode_set(mode='OBJECT')
    utils.make_single(proxyRig)
    bpy.ops.object.transform_apply(scale=True, rotation=True, location=False)
    
    joint_data = {}
    bpy.ops.object.mode_set(mode='EDIT')
    for boneObj in proxyRig.data.edit_bones:
        bone = boneObj.name
        joint_data[bone] = {}
        joint_data[bone]['head'] = boneObj.head.copy()
        joint_data[bone]['tail'] = boneObj.tail.copy()
        joint_data[bone]['roll'] = boneObj.roll
    bpy.ops.object.mode_set(mode='OBJECT')

    
    outRig.location = proxyRig.location
    offset = proxyRig.location.y + oni_motion.motion_distance
    outRig.location.y = offset

    
    bpy.ops.object.delete()

    
    
    
    outRig.select_set(True)
    utils.activate(outRig)
    outRig.animation_data_clear()
    
    if 1 == 1:
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.armature_apply()
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.transform_apply(scale=True, rotation=True, location=False)

    
    

    
    
    rename_rev = {}
    for sbone in rename_map.keys():
        tbone = rename_map[sbone]
        rename_rev[tbone] = sbone

    bpy.ops.object.mode_set(mode='EDIT')
    
    for boneObj in outRig.data.edit_bones:
        boneObj.use_connect = False

    for tbone in rename_rev:
        if tbone not in outRig.data.bones:
            print("Skipping outRig bone:", tbone)
            continue
        sbone = rename_rev[tbone]
        if sbone not in inRig.data.bones:
            print("skipping inRig bone:", sbone)
            continue
        boneObj = outRig.data.edit_bones[tbone]
        boneObj.head = joint_data[sbone]['head']
        boneObj.tail = joint_data[sbone]['tail']
        boneObj.roll = joint_data[sbone]['roll']


    bpy.ops.object.mode_set(mode='OBJECT')

    outRig.select_set(False)

    
    
    
    
    add_constraints(
        source=outRig.name, target=inRig.name,
        bone_map=rename_map, constraint='COPY_ROTATION', space='WORLD',
        influence=1, location=True, rotation=True, scale=True)
    add_constraints(
        source=outRig.name, target=inRig.name,
        bone_map=rename_map, constraint='COPY_LOCATION', space='WORLD',
        influence=1, location=True, rotation=True, scale=True)

    
    
    
    
    if oni_motion.motion_stabilize == True:
        stickyRig = stabilizer(armObj=outRig, bone_map=rename_map)
        inRig['oni_motion_stabilizer'] = stickyRig
        stickyRig.hide_set(True)

    return True








def retarget_soft(inRig, report=False):

    debug = False
    defer = True

    
    state = utils.get_state()
    oni_motion = bpy.context.window_manager.oni_motion

    outRig = rigutils.build_rig(rig_class="pos", rotate=True, connect=False)
    outRig.select_set(False)

    
    
    
    
    
    
    
    if inRig.get('oni_onemap_rename', None) == None:
        print("motion::retarget_soft : No rename map, using blanks")
    rename_map = inRig.get('oni_onemap_rename', {})
    if len(rename_map):
        print("motion::retarget_soft : Rename map contains items")
    else:
        print("motion::retarget_soft : Rename map is empty")

    
    
    
    if 1 == 0:
        good_bones_out = []
        for sbone in rename_map:
            tbone = rename_map[sbone]
            if tbone in outRig.data.bones:
                good_bones_out.append(sbone)
        if len(good_bones_out) == 0:
            print("None of the bones in the available map matched your target")
            popup("No mappable bones, see console", "Error", "ERROR")
            return False

    inRig['oni_motion_actor'] = outRig
    outRig['oni_motion_director'] = inRig

    if 1 == 0:
        inRig.show_in_front = False
        outRig.show_in_front = True
        outRig.data.display_type = 'STICK'
        inRig['oni_motion_display'] = outRig.display_type


    
    
    
    
    
    
    inRig.select_set(True)
    utils.activate(inRig)
    bpy.ops.object.duplicate()
    proxyRig = bpy.context.object
    proxyRig.name = "RETARGET_PROXY"
    print("Storing proxy rig object", proxyRig.name, "onto the Director", inRig.name)
    inRig['oni_motion_proxy'] = proxyRig
    

    
    
    bpy.ops.object.mode_set(mode='EDIT')
    for boneObj in proxyRig.data.edit_bones:
        boneObj.use_connect = False
        boneObj.parent = None
    bpy.ops.object.mode_set(mode='OBJECT')

    
    
    frame_start = 1
    if proxyRig.animation_data:
        if proxyRig.animation_data.action:
            frame_start = proxyRig.animation_data.action.frame_range[0]
    bpy.context.scene.frame_set(frame_start)
    
    proxyRig.animation_data_clear()
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.armature_apply()
    bpy.ops.object.mode_set(mode='OBJECT')
    utils.make_single(proxyRig)
    bpy.ops.object.transform_apply(scale=True, rotation=True, location=False)

    
    
    
    
    
    outRig.location.y = proxyRig.location.y + oni_motion.motion_distance

    
    
    
    
    
    
    
    
    
    if 1 == 0:
        for boneObj in proxyRig.data.bones:
            boneObj['matrix_local'] = boneObj.matrix_local.copy()
            boneObj['head'] = boneObj.head_local.copy()
            boneObj['tail'] = boneObj.tail_local.copy()
            boneObj['roll'] = utils.get_bone_roll(boneObj.matrix_local)

            if debug == False:
                boneObj.hide = True

    
    
    
    rename_rev = {}
    for tbone in rename_map.keys():
        sbone = rename_map[tbone]
        rename_rev[sbone] = tbone



    
    
    
    
    
    
    
    
    
    if len(rename_rev) > 0:
        add_constraints(
            source=proxyRig.name, target=outRig.name,
            bone_map=rename_rev, constraint='COPY_ROTATION',
            space='WORLD', influence=1)

    
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.armature_apply()
    bpy.ops.object.mode_set(mode='OBJECT')
    
    for boneObj in proxyRig.pose.bones:
        for C in boneObj.constraints:
            boneObj.constraints.remove(C)



    for boneObj in proxyRig.data.bones:
        boneObj['matrix_local'] = boneObj.matrix_local.copy()
        boneObj['head'] = boneObj.head_local.copy()
        boneObj['tail'] = boneObj.tail_local.copy()
        boneObj['roll'] = utils.get_bone_roll(boneObj.matrix_local)

        if debug == False:
            boneObj.hide = True



    
    match_map = {}
    for bone in rename_map.keys():
        match_map[bone] = bone

    
    
    
    
    print("motion::retarget_soft reports : Bone relocator turned on")
    if 1 == 1:

        
        
        
        bpy.ops.object.mode_set(mode='POSE')
        good_bones = []
        for boneObj in proxyRig.pose.bones:
            if boneObj.name not in rename_map:
                if report == True:
                    print("skipping bone", boneObj.name, "not in map")
                continue
            good_bones.append(boneObj.name)
            proxyRig.data.bones.active = proxyRig.data.bones[boneObj.name]
            bc = boneObj.constraints
            conObj = bc.new('COPY_LOCATION')
            cname = conObj.name
            conObj.target = outRig

            
            
            
            
            if boneObj.name in rename_rev:
                conObj.subtarget = rename_rev[boneObj.name]
                conObj.influence = 1
            else:
                conObj.influence = 0
            conObj.target_space = "WORLD";
            conObj.owner_space = "WORLD"
            conObj.name = "ONI " + cname
            boneObj['oni_motion_constraints'] = [conObj.name]
        bpy.ops.object.mode_set(mode='OBJECT')
        if len(good_bones) == 0:
            print("None of the bones in the map matched your set")

        
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.armature_apply()
        bpy.ops.object.mode_set(mode='OBJECT')
        
        for boneObj in proxyRig.pose.bones:
            for C in boneObj.constraints:
                boneObj.constraints.remove(C)

    
    
    
    

    
    
    
    
    bpy.ops.object.mode_set(mode='POSE')
    for boneObj in proxyRig.pose.bones:
        
        
        proxyRig.data.bones.active = proxyRig.data.bones[boneObj.name]
        bc = boneObj.constraints
        conObj = bc.new('CHILD_OF')
        cname = conObj.name
        conObj.target = inRig
        conObj.subtarget = boneObj.name
        conObj.influence = 1
        
        
        conObj.target_space = "WORLD";
        conObj.owner_space = "POSE"

        if defer == True:
            
            
            tbone = boneObj.name 
            tmat = inRig.matrix_world.copy()
            pmat = proxyRig.matrix_world.copy()
            bmat = inRig.pose.bones[tbone].matrix.copy()
            
            
            MF = bmat.inverted() @ pmat @ tmat.inverted()
            
            conObj.inverse_matrix = MF
        else:
            context_py = bpy.context.copy()
            context_py["constraint"] = bc.active
            bpy.ops.constraint.childof_set_inverse(context_py, constraint=cname, owner="BONE")
 
        conObj.name = "ONI " + cname
        boneObj['oni_motion_constraints'] = [conObj.name]

    bpy.ops.object.mode_set(mode='OBJECT')

    
    proxyRig.select_set(False)
    outRig.select_set(True)
    utils.activate(outRig)

    
    if oni_motion.motion_prepare_actor == True:
        frame_start = 1
        if outRig.animation_data:
            if outRig.animation_data.action:
                frame_start = outRig.animation_data.action.frame_range[0]
        bpy.context.scene.frame_set(frame_start)
        
        outRig.animation_data_clear()
        mode = bpy.context.mode
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.armature_apply()
        bpy.ops.object.mode_set(mode=mode)
        bpy.ops.object.transform_apply(scale=True, rotation=True, location=False)

    
    
    
    
    
    
    
    
    bpy.ops.object.mode_set(mode='POSE')
    for boneObj in outRig.pose.bones:
        tbone = boneObj.name
        outRig.data.bones.active = outRig.data.bones[boneObj.name]
        bc = boneObj.constraints
        conObj = bc.new('COPY_ROTATION')
        cname = conObj.name
        conObj.target = proxyRig
        
        if boneObj.name in rename_rev:
            sbone = rename_rev[tbone]
            if sbone in inRig.data.bones:
                conObj.subtarget = rename_rev[boneObj.name]
                conObj.influence = 1
        else:
            conObj.influence = 0
        conObj.target_space = "POSE";
        conObj.owner_space = "POSE"
        conObj.name = "ONI " + cname
        boneObj['oni_motion_constraints'] = [conObj.name]
    
    
    

    
    
    
    
    
    
    for boneObj in outRig.pose.bones:
        tbone = boneObj.name
        outRig.data.bones.active = outRig.data.bones[boneObj.name]
        bc = boneObj.constraints
        conObj = bc.new('COPY_LOCATION')
        cname = conObj.name
        conObj.target = proxyRig
        
        if boneObj.name in rename_rev:
            sbone = rename_rev[tbone]
            if sbone in inRig.data.bones:
                conObj.subtarget = rename_rev[boneObj.name]
                conObj.influence = 0
        else:
            conObj.influence = 0
        
        
        
        
        conObj.target_space = "LOCAL";
        conObj.owner_space = "LOCAL"
        conObj.name = "ONI " + cname

        
        
        
        
        
        
        if boneObj.parent:
            
            
            conObj.target_space = "LOCAL_WITH_PARENT";
            conObj.owner_space = "LOCAL_WITH_PARENT"

            c_list = boneObj['oni_motion_constraints']
            c_list.append(conObj.name)
            boneObj['oni_motion_constraints'] = c_list

    
    
    
    
    
    if 1 == 0:
        boneObj = outRig.pose.bones[0]
        c_list = boneObj['oni_motion_constraints']
        new_list = []
        for cname in c_list:
            conObj = boneObj.constraints[cname]
            if conObj.type == 'COPY_LOCATION':
                print("Replacing COPY_LOCATION wit custom")
                boneObj.constraints.remove(conObj)
            else:
                new_list.append(cname)
        boneObj['oni_motion_constraints'] = new_list
    
    
    

    bpy.ops.object.mode_set(mode='OBJECT')

    
    
    
    
    
    
    
    

    
    
    if 1 == 1:
        boneObj = outRig.pose.bones[0]
        new_list = boneObj['oni_motion_constraints']
        for conObj in boneObj.constraints:
            if conObj.type == 'COPY_LOCATION':
                conObj.influence = 1
                new_list.append(conObj.name)
            
            
            
                
                
                
        boneObj['oni_motion_constraints'] = new_list

    
    
    
    
    
    

    
    
    
    
    if 1 == 0:
        boneObj = outRig.pose.bones[0]
        proxy_anchor = proxyRig.pose.bones[0].name
        outRig.data.bones.active = boneObj.bone 
        bc = boneObj.constraints
        conObj = bc.new('COPY_LOCATION')
        conObj.target = proxyRig
        conObj.subtarget = proxy_anchor
        conObj.owner_space = 'POSE'
        conObj.influence = 1

        
        
        
        for C in boneObj.constraints:
            if C.type == 'COPY_ROTATION':
                C.use_x = False
                C.use_y = False
                C.use_z = False
    
    
    


    if oni_motion.motion_stabilize == True:
        print("Stabilizer used with humanoid non-joint position uploads are likely to be unusable!")
        stickyRig = stabilizer(armObj=outRig, bone_map=rename_map)
        inRig['oni_motion_stabilizer'] = stickyRig
        stickyRig.hide_set(True)

    return True












def retarget_custom(inRig=None, outRig=None):

    debug = True
    defer = True

    
    state = utils.get_state()
    oni_motion = bpy.context.window_manager.oni_motion

    
    
    

    
    
    
    
    
    
    
    rename_map = inRig.get('oni_onemap_rename', {})

    inRig['oni_motion_actor'] = outRig
    outRig['oni_motion_director'] = inRig

    
    
    
    
    
    
    inRig.select_set(True)
    utils.activate(inRig)
    bpy.ops.object.duplicate()
    proxyRig = bpy.context.object
    proxyRig.name = "RETARGET_PROXY"
    inRig['oni_motion_proxy'] = proxyRig

    
    
    bpy.ops.object.mode_set(mode='EDIT')
    for boneObj in proxyRig.data.edit_bones:
        boneObj.use_connect = False
        boneObj.parent = None
    bpy.ops.object.mode_set(mode='OBJECT')

    
    
    frame_start = 1
    if proxyRig.animation_data:
        if proxyRig.animation_data.action:
            frame_start = proxyRig.animation_data.action.frame_range[0]
    bpy.context.scene.frame_set(frame_start)
    
    proxyRig.animation_data_clear()
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.armature_apply()
    bpy.ops.object.mode_set(mode='OBJECT')
    utils.make_single(proxyRig)
    bpy.ops.object.transform_apply(scale=True, rotation=True, location=False)

    
    
    
    
    
    outRig.location.y = proxyRig.location.y + oni_motion.motion_distance

    
    
    
    rename_rev = {}
    for tbone in rename_map:
        sbone = rename_map[tbone]
        rename_rev[sbone] = tbone

    
    
    
    
    
    
    
    
    
    if len(rename_rev) > 0:
        add_constraints(
            source=proxyRig.name, target=outRig.name,
            bone_map=rename_rev, constraint='COPY_ROTATION',
            space='WORLD', influence=1)

    
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.armature_apply()
    bpy.ops.object.mode_set(mode='OBJECT')
    
    for boneObj in proxyRig.pose.bones:
        for C in boneObj.constraints:
            boneObj.constraints.remove(C)

    for boneObj in proxyRig.data.bones:
        boneObj['matrix_local'] = boneObj.matrix_local.copy()
        boneObj['head'] = boneObj.head_local.copy()
        boneObj['tail'] = boneObj.tail_local.copy()
        boneObj['roll'] = utils.get_bone_roll(boneObj.matrix_local)

        if debug == False:
            boneObj.hide = True

    
    match_map = {}
    for bone in rename_map:
        match_map[bone] = bone

    
    
    
    
    print("motion::retarget_soft reports : Bone relocator turned on")
    if 1 == 1:

        
        
        
        bpy.ops.object.mode_set(mode='POSE')
        good_bones = []
        for boneObj in proxyRig.pose.bones:
            if boneObj.name not in rename_map:
                print("skipping bone", boneObj.name, "not in map")
                continue
            good_bones.append(boneObj.name)
            proxyRig.data.bones.active = proxyRig.data.bones[boneObj.name]
            bc = boneObj.constraints
            conObj = bc.new('COPY_LOCATION')
            cname = conObj.name
            conObj.target = outRig

            
            
            
            
            if boneObj.name in rename_rev:
                conObj.subtarget = rename_rev[boneObj.name]
                conObj.influence = 1
            else:
                conObj.influence = 0
            conObj.target_space = "WORLD";
            conObj.owner_space = "WORLD"
            conObj.name = "ONI " + cname
            boneObj['oni_motion_constraints'] = [conObj.name]
        bpy.ops.object.mode_set(mode='OBJECT')
        if len(good_bones) == 0:
            print("None of the bones in the map matched your set")

        
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.armature_apply()
        bpy.ops.object.mode_set(mode='OBJECT')
        
        for boneObj in proxyRig.pose.bones:
            for C in boneObj.constraints:
                boneObj.constraints.remove(C)

    
    
    
    

    
    
    
    
    bpy.ops.object.mode_set(mode='POSE')
    for boneObj in proxyRig.pose.bones:
        
        
        proxyRig.data.bones.active = proxyRig.data.bones[boneObj.name]
        bc = boneObj.constraints
        conObj = bc.new('CHILD_OF')
        cname = conObj.name
        conObj.target = inRig
        conObj.subtarget = boneObj.name
        conObj.influence = 1
        
        
        conObj.target_space = "WORLD";
        conObj.owner_space = "POSE"

        if defer == True:
            
            
            tbone = boneObj.name 
            tmat = inRig.matrix_world.copy()
            pmat = proxyRig.matrix_world.copy()
            bmat = inRig.pose.bones[tbone].matrix.copy()
            
            
            MF = bmat.inverted() @ pmat @ tmat.inverted()
            
            conObj.inverse_matrix = MF
        else:
            context_py = bpy.context.copy()
            context_py["constraint"] = bc.active
            bpy.ops.constraint.childof_set_inverse(context_py, constraint=cname, owner="BONE")
 
        conObj.name = "ONI " + cname
        boneObj['oni_motion_constraints'] = [conObj.name]

    bpy.ops.object.mode_set(mode='OBJECT')

    
    proxyRig.select_set(False)
    outRig.select_set(True)
    utils.activate(outRig)

    
    if oni_motion.motion_prepare_actor == True:
        frame_start = 1
        if outRig.animation_data:
            if outRig.animation_data.action:
                frame_start = outRig.animation_data.action.frame_range[0]
        bpy.context.scene.frame_set(frame_start)
        
        outRig.animation_data_clear()
        mode = bpy.context.mode
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.armature_apply()
        bpy.ops.object.mode_set(mode=mode)
        bpy.ops.object.transform_apply(scale=True, rotation=True, location=False)

    
    
    
    
    
    
    
    
    bpy.ops.object.mode_set(mode='POSE')
    for boneObj in outRig.pose.bones:
        tbone = boneObj.name
        outRig.data.bones.active = outRig.data.bones[boneObj.name]
        bc = boneObj.constraints
        conObj = bc.new('COPY_ROTATION')
        cname = conObj.name
        conObj.target = proxyRig
        
        if boneObj.name in rename_rev:
            sbone = rename_rev[tbone]
            if sbone in inRig.data.bones:
                conObj.subtarget = rename_rev[boneObj.name]
                conObj.influence = 1
        else:
            conObj.influence = 0
        conObj.target_space = "POSE";
        conObj.owner_space = "POSE"
        conObj.name = "ONI " + cname
        boneObj['oni_motion_constraints'] = [conObj.name]
    
    
    

    
    
    
    
    
    
    for boneObj in outRig.pose.bones:
        tbone = boneObj.name
        outRig.data.bones.active = outRig.data.bones[boneObj.name]
        bc = boneObj.constraints
        conObj = bc.new('COPY_LOCATION')
        cname = conObj.name
        conObj.target = proxyRig
        
        if boneObj.name in rename_rev:
            sbone = rename_rev[tbone]
            if sbone in inRig.data.bones:
                conObj.subtarget = rename_rev[boneObj.name]
                conObj.influence = 0
        else:
            conObj.influence = 0
        
        
        conObj.target_space = "LOCAL";
        conObj.owner_space = "LOCAL"
        conObj.name = "ONI " + cname

        
        
        
        
        
        
        if boneObj.parent:
            conObj.target_space = "LOCAL";
            conObj.owner_space = "LOCAL"
            c_list = boneObj['oni_motion_constraints']
            c_list.append(conObj.name)
            boneObj['oni_motion_constraints'] = c_list

    
    
    

    bpy.ops.object.mode_set(mode='OBJECT')

    
    
    
    
    
    
    
    

    
    
    if 1 == 1:
        boneObj = outRig.pose.bones[0]
        new_list = boneObj['oni_motion_constraints']
        for conObj in boneObj.constraints:
            if conObj.type == 'COPY_LOCATION':
                conObj.influence = 1
                new_list.append(conObj.name)
            
            
            
                
                
                
        boneObj['oni_motion_constraints'] = new_list

    
    
    

    if oni_motion.motion_stabilize == True:
        print("Stabilizer used with humanoid non-joint position uploads are likely to be unusable!")
        stickyRig = stabilizer(armObj=outRig, bone_map=rename_map)
        inRig['oni_motion_stabilizer'] = stickyRig
        stickyRig.hide_set(True)

    return True







def stabilizer(armObj=None, bone_map=None):

    if bone_map == None:
        bone_map = armObj['oni_onemap_rename']

    
    rename_rev = set()
    for sbone in bone_map.keys():
        tbone = bone_map[sbone]
        rename_rev.add(tbone)
    bones = []
    for boneObj in armObj.data.bones:
        if boneObj.name not in rename_rev:
            bones.append(boneObj.name)

    for o in bpy.context.selected_objects:
        o.select_set(False)
    armObj.select_set(True)
    utils.activate(armObj)
    bpy.ops.object.duplicate()
    stickyRig = bpy.context.object
    stickyRig.name = 'STICKY_RIG'
    
    for boneObj in stickyRig.pose.bones:
        for C in boneObj.constraints:
            boneObj.constraints.remove(C)
    stickyRig.select_set(False)
    armObj.select_set(True)
    utils.activate(armObj)

    constraints = ['COPY_LOCATION', 'COPY_ROTATION']
    for constraint in constraints:
        for bone in bones:
            boneObj = armObj.pose.bones[bone]
            armObj.data.bones.active = boneObj.bone
            bc = boneObj.constraints
            conObj = bc.new(constraint)
            cname = conObj.name
            conObj.target = stickyRig
            conObj.subtarget = bone
            conObj.target_space = 'WORLD'
            conObj.owner_space = 'WORLD'
            conObj.influence = 1
            conObj.name = "ONI " + cname + " STK"


    return stickyRig




def popup(message = "", title = "Message Box", icon =  'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
    return









def add_groups(inRig=None, outRig=None):
    state = utils.get_state()

    inRig.select_set(True)
    utils.activate(inRig)
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.group_add()
    inRig.pose.bone_groups.active.name = props['groups']['director']
    inRig.pose.bone_groups.active.color_set = props['themes']['director']
    bpy.ops.pose.group_add()
    inRig.pose.bone_groups.active.name = props['groups']['reskin']
    inRig.pose.bone_groups.active.color_set = props['themes']['reskin']
    bpy.ops.object.mode_set(mode='OBJECT')
    inRig.select_set(False)

    outRig.select_set(True)
    utils.activate(outRig)
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.group_add()
    outRig.pose.bone_groups.active.name = props['groups']['actor']
    outRig.pose.bone_groups.active.color_set = props['themes']['actor']
    bpy.ops.pose.group_add()
    outRig.pose.bone_groups.active.name = props['groups']['reskin']
    outRig.pose.bone_groups.active.color_set = props['themes']['reskin']

    bpy.ops.object.mode_set(mode='OBJECT')

    utils.set_state(state)

    return True









def update_map(inRig=None):

    oni_motion = bpy.context.window_manager.oni_motion

    state = utils.get_state()

    rename = inRig.get('oni_onemap_rename')
    if rename == None:
        print("motion::update_map : no rename map")
        return False
    reskin = inRig.get('oni_onemap_reskin')
    if reskin == None:
        print("motion::update_map : no reskin map, adding empty")
        reskin = {}

    oni_onemap = bpy.context.scene.oni_onemap

    outRig = inRig['oni_motion_actor']
    proxyRig = inRig.get('oni_motion_proxy')

    
    
    
    if 1 == 1:
        print("Entering update")
        
        if utils.is_valid(proxyRig):
            
            
            
            frame_current = bpy.context.scene.frame_current
            has_action = False
            if inRig.animation_data != None:
                if inRig.animation_data.action != None:
                    has_action = True
                    frame_start = inRig.animation_data.action.frame_range[0]
            if has_action == False:
                    frame_start = bpy.context.scene.frame_start
            bpy.context.scene.frame_set(frame_start)

            
            
            
            
            

            
            
            
            for boneObj in proxyRig.pose.bones:
                for cname in boneObj['oni_motion_constraints']:
                    boneObj.constraints[cname].influence = 0

            
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
            
            
            

            
            
            for boneObj in outRig.pose.bones:
                for cname in boneObj['oni_motion_constraints']:
                    boneObj.constraints[cname].influence = 0

            
            
            
            
            
            


            
            
            
            

            
            
            

            for sbone in rename.keys():
                tbone = rename[sbone]
                if sbone not in proxyRig.data.bones:
                    print("sbone missing in rig:", sbone)
                    continue
                pBone = proxyRig.pose.bones[sbone]
                if tbone not in outRig.data.bones:
                    print("tbone missing in rig:", tbone)
                    continue

                
                

                oBone = outRig.data.bones[tbone]

                
                
                tMat = oBone.matrix_local.copy()
                matrix_local = mathutils.Matrix(pBone.bone['matrix_local'])
                M = utils.compose_transforms(matrix_in=tMat, matrix_out=matrix_local, location=False, rotation=True, scale=False)
                pBone.matrix = M

                
                for cname in pBone['oni_motion_constraints']:
                    conObj = pBone.constraints[cname]
                    conObj.subtarget = sbone
                    if conObj.type == 'COPY_ROTATION' or conObj.type == 'CHILD_OF':
                        conObj.influence = 1
                    if conObj.type == 'COPY_LOCATION':
                        if oni_motion.motion_constrain_location == True:
                            conObj.influence = 1

            
            
            if 1 == 0:
                if bone_match == 0:
                    print("No matching bones, see above")
                    popup("No matchig bones", "Error", "ERROR")
                    return False

            
            bpy.ops.object.mode_set(mode='POSE')
            for bone in rename.keys():
                
                if bone in proxyRig.pose.bones:
                    boneObj = proxyRig.pose.bones[bone]
                    proxyRig.data.bones.active = boneObj.bone
                    for cname in boneObj['oni_motion_constraints']:
                        conObj = boneObj.constraints[cname]
                        if conObj.type == 'CHILD_OF':
                            
                            
                            
                            
                            defer = True
                            if defer == True:
                                
                                
                                

                                tmat = inRig.matrix_world.copy()
                                pmat = proxyRig.matrix_world.copy()
                                
                                bmat = inRig.pose.bones[boneObj.name].matrix.copy()
                                MF = bmat.inverted() @ pmat @ tmat.inverted()
                                conObj.inverse_matrix = MF

                            else:
                                context_py = bpy.context.copy()
                                context_py["constraint"] = conObj 
                                bpy.ops.constraint.childof_set_inverse(context_py, constraint=cname, owner="BONE")

                        
                        
                        
                        tbone = rename[bone]
                        if tbone in outRig.pose.bones:
                            for cname in outRig.pose.bones[tbone]['oni_motion_constraints']:
                                conObj = outRig.pose.bones[tbone].constraints[cname]
                                conObj.subtarget = bone
                                if conObj.type == 'COPY_ROTATION':
                                    conObj.influence = 1
                                if oni_motion.motion_constrain_location == True:
                                    if conObj.type == 'COPY_LOCATION':
                                        conObj.influence = 1
                                
                                if tbone == outRig.pose.bones[0].name:
                                    conObj.influence = 1






            bpy.ops.object.mode_set(mode='OBJECT')

            
            bpy.context.scene.frame_set(frame_current)

    
    
    

    
    for boneObj in inRig.pose.bones:
        boneObj.bone_group = None
    for boneObj in outRig.pose.bones:
        boneObj.bone_group = None

    

    
    
    bad_group = False
    for rename_in_bone in rename.keys():
        if rename_in_bone not in inRig.pose.bones:
            continue
        rename_out_bone = rename[rename_in_bone]
        director_group = props['groups']['director']
        actor_group = props['groups']['actor']
        
        
        try:
            inRig.pose.bones[rename_in_bone].bone_group = inRig.pose.bone_groups[director_group]
            outRig.pose.bones[rename_out_bone].bone_group = outRig.pose.bone_groups[actor_group]
        except:
            bad_group = True
            pass

        
        reskin_group = props['groups']['reskin']
        reskin_bones = reskin.get(rename_in_bone, [])
        for bone in reskin_bones:
            if bone not in inRig.pose.bones:
                continue
            inRig.pose.bones[bone].bone_group = inRig.pose.bone_groups[reskin_group]

    utils.set_state(state)

    if bad_group == True:
        print("There was a problem assigning bone group to your rig, if this is a match map please use the (custom) feature")
        
        

    return True






def apply_map(inRig=None, outRig=None):

    
    for boneObj in inRig.pose.bones:
        boneObj.bone_group = None
    for boneObj in outRig.pose.bones:
        boneObj.bone_group = None

    rename = inRig.get('oni_onemap_rename', {})
    reskin = inRig.get('oni_onemap_reskin', {})
    for rename_in_bone in rename:
        if rename_in_bone not in inRig.pose.bones:
            continue
        rename_out_bone = rename[rename_in_bone]

        director_group = props['groups']['director']
        actor_group = props['groups']['actor']

        inRig.pose.bones[rename_in_bone].bone_group = inRig.pose.bone_groups[director_group]
        outRig.pose.bones[rename_out_bone].bone_group = outRig.pose.bone_groups[actor_group]
        reskin_bones = reskin.get(rename_in_bone, [])

        
        reskin_group = props['groups']['reskin']

        for bone in reskin_bones:
            
            
            if bone not in inRig.pose.bones:
                continue
            inRig.pose.bones[bone].bone_group = inRig.pose.bone_groups[reskin_group]

    return True


















