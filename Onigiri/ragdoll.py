


import bpy
from . import utils
import traceback
import mathutils




if 1 == 1:

    props = {}
    
    props["mesh"] = None
    
    props["pool"] = None

    
    








def get_actor():

    selected = bpy.context.selected_objects
    if len(selected) == 0:
        print("ragdog::get_actor : nothing selected")
        return False

    armObj = None
    for o in selected:
        if o.get('bb_ragdoll_directors') != None:
            print("Found actor rig directly:", o.name)
            return o
    for o in selected:
       if o.get('bb_ragdoll_actor') != None:
            print("Found actor rig on a director object:", o.name)
            return o['bb_ragdoll_actor']

    print("ragdoll::get_actor : I couldn't find the actor")

    return False













def create_directors(armObj, source=None, move=True):
    if source == "existing":
        print("Using mesh objects associated with the rig")
    elif source == "pool":
        print("Using a pre-selected pool")
    elif source == None:
        print("ragdoll::create_directors : reports None, will generate cubes instead")
 
    state = utils.get_state()

    
    
    
    if source == "pool":
        print("ragdoll::create_directors: source is pool")
        pool = []
        for name in props['pool']:
            if name in bpy.data.objects:
                o = bpy.data.objects[name]
                o.select_set(True)
                utils.activate(o)
                bpy.ops.object.duplicate()
                activeObj = bpy.context.active_object
                pool.append(activeObj)
                activeObj.select_set(False)

            else:
                print("Can't find", name, "in scene, skipping")

        print("Recorded", len(pool), "pool objects")

        
        if len(pool) != 0:
            for o in bpy.context.selected_objects:
                o.select_set(False)
            for o in pool:
                o.select_set(True)
            utils.activate(o)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            for o in bpy.context.selected_objects:
                o.select_set(False)

    
    elif source == None:
        print("ragdoll::create_directors: source is None")
        pool = []
        
        size = 0.2
        for boneObj in armObj.pose.bones:
            dBone = boneObj.bone
            bpy.ops.mesh.primitive_cube_add( size=size, enter_editmode=False, align='WORLD', location=(0.0, 0.0, 0.0) )
            pool.append(bpy.context.active_object)
    elif source == "mesh":
        print("ragdoll::create_directors: source is mesh")
        mesh = props['mesh']
        meshObj = mesh
        if isinstance(mesh, str):
            meshObj = bpy.data.objects[mesh]
        meshObj.select_set(True)
        utils.activate(meshObj)
        pool = []
        for boneObj in armObj.pose.bones:
            dBone = boneObj.bone
            bpy.ops.object.duplicate()
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
            pool.append(bpy.context.active_object)
    elif source == "existing":
        print("ragdoll::create_directors: source is existing")
        
        pool = []
        
        
        existing_mesh = {}
        for o in bpy.data.objects:
            for modObj in o.modifiers:
                if modObj.type == 'ARMATURE':
                    if modObj.object == armObj:
                        
                        vglen = len(o.vertex_groups)
                        if vglen == 0:
                            print("Skipping almost qualified mesh", o.name, "no vertex groups")
                            break
                        if vglen > 1:
                            print("Skipping almost qualified mesh", o.name, "too many vertex groups:", str(vglen))
                            break
                        pool.append(o)
                        gname = o.vertex_groups[0].name
                        existing_mesh[gname] = o
                        break 
                    break 
        
        
        for o in pool:
            for modObj in o.modifiers:
                if modObj.type == 'ARMATURE':
                    modObj.show_viewport = False
    
    if len(pool) == 0:
        print("ragdoll::create_directors : no pool remaining")
        return False

    
    if source != "existing":
        
        
        
        bone_count = len(armObj.data.bones)
        qualified_mesh = []
        count = 0
        for director in pool:
            if count > bone_count:
                break
            qualified_mesh.append(director)
            count += 1

        print("qualified mesh:", len(qualified_mesh))
    else:
        print("qualified mesh is not required for (existing)")

    
    world_mat = armObj.matrix_world.copy()

    
    

    
    ragdoll_directors = {}
    count = 0
    for boneObj in armObj.pose.bones:

        
        if source != "existing":
            
            
            if count == len(qualified_mesh):
                break
            
            OBJ = qualified_mesh[count]
            count += 1
        else:
            bone = boneObj.name
            OBJ = existing_mesh[bone] 

        OBJ.select_set(True)
        utils.activate(OBJ)
        dBone = boneObj.bone

        
        head = dBone.head_local
        tail = dBone.tail_local
        middle = head.lerp(tail, 0.5)
        bone_mat = dBone.matrix_local
        OBJ.matrix_world = bone_mat @ world_mat

        
        OBJ.location = middle

        length = dBone.length

        
        if source == "mesh" or source == None:

            
            
            OBJ.dimensions = ( (length / 4), length, (length / 4) )

        if source != "existing":
            
            OBJ.name = boneObj.name + "_DIR"

        
        group = OBJ.vertex_groups.new( name = boneObj.name )
        vertices = [v.index for v in OBJ.data.vertices]
        group.add( vertices, 1, 'REPLACE' )

        
        
        modObj = OBJ.modifiers.new('Armature', 'ARMATURE')
        modObj.object = armObj
        modObj.show_viewport = False 

        OBJ['bb_ragdoll_bone'] = boneObj.name
        OBJ['bb_ragdoll_bone_info'] = "I contain the bone name that is that target bone on the actor"
        OBJ['bb_ragdoll_actor'] = armObj
        OBJ['bb_ragdoll_actor_info'] = "I contain the rig object that is the actor containing the target pose bone"

        
        
        
        ragdoll_directors[boneObj.name] = OBJ.name

        OBJ.select_set(False)

    armObj['bb_ragdoll_directors'] = ragdoll_directors

    armObj.select_set(True)
    utils.activate(armObj)

    return True











def add_constraints(armObj):

    state = utils.get_state()
    armObj.select_set(True)
    utils.activate(armObj)

    
    for boneObj in armObj.pose.bones:
        cname = boneObj.bone.get('bb_ragdoll_constraint')
        if cname == None:
            continue
        for cObj in boneObj.constraints:
            if cObj.name == cname:
                boneObj.constraints.remove(cObj)

    
    directors = armObj['bb_ragdoll_directors']

    
    bpy.ops.object.mode_set(mode = 'POSE')
    for boneObj in armObj.pose.bones:
        
        bone = boneObj.name
        if bone not in directors:
            print("missing bone in directors [", bone, "]", "limit probably reached for pool or existing", sep="")
            continue
        dname = directors[bone]

        dBone = boneObj.bone
        armObj.data.bones.active = dBone
        bc = boneObj.constraints
        conObj = bc.new('CHILD_OF')
        cname = conObj.name
        conObj.target = bpy.data.objects[dname]
        
        
        
        conObj.target_space = 'WORLD'
        conObj.owner_space = 'POSE'
        context_py = bpy.context.copy()
        context_py["constraint"] = bc.active
        utils.set_inverse(context_py, cname)
        conObj.name = "BB " + cname
        dBone['bb_ragdoll_constraint'] = conObj.name
    bpy.ops.object.mode_set(mode = 'OBJECT')

    utils.set_state(state)

    return True







