import bpy




if True:
    props = {}
    
    
    










def get_director(armature=None):
    if armature == None:
        return False
    if armature not in bpy.context.scene.objects:
        return False
    obj = bpy.data.objects
    armObj = obj[armature]

    
    
    actor_check = armObj.get('bb_dynamic_actor', None)
    director_check = armObj.get('bb_dynamic_director', None)

    
    
    if actor_check == None:
        if director_check == None:
            return False
        inRig = director_check
    elif director_check == None:
        if actor_check == None:
            return False
        director = actor_check.get('bb_dynamic_director', None)
        if director == None:
            return False
        inRig = director
    
    
    
    else:
        inRig = director_check

    if inRig.name not in bpy.context.scene.objects:
       return False

    

    return inRig











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

    for tbone in bone_map:
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

    for tbone in bone_map:
        
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
        conObj.target_space = space
        conObj.owner_space = space
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
            context_py = bpy.context.copy()
            context_py["constraint"] = bc.active
            utils.set_inverse(context_py, cname)
            
            
        conObj.name = "BB " + cname

    

    return True













