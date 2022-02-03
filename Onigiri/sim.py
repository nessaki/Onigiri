
import os
import bpy
import sys
import time
import mathutils
from . import utils




if 1 == 1:

    props = {}

    
    
    
    
    props['controller'] = ""

    
    props['bmesh'] = ""
    
    
    props['last_vertex'] = ""
    
    
    
    props['vertex_head'] = ""
    props['vertex_tail'] = ""

    
    props['marker_head'] = ""
    props['marker_tail'] = ""
    
    
    props['marker_is_head'] = True

    
    
    
    
    
    props['last_marker'] = ""

    
    props['material_head'] = ""
    props['material_tail'] = ""

    
    props['count'] = 0

    
    
    props['group_base'] = "Sim"
    props['theme_base'] = "THEME08"

    
    
    
    
    
    props['custom_bones'] = None
    props['custom_rig'] = None
    props['custom_mesh'] = None







def add_locator():
    temp_name = utils.get_temp_name() 
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.01, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    locObj = bpy.context.object
    
    locObj.dimensions.xyz = 0.2, 0.2, 0.2
    locObj.name = "LOCATOR_" + temp_name

    return locObj





def add_markers(testing=False):

    bb_sim = bpy.context.window_manager.bb_sim

    
    state = utils.get_state()

    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.01, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    headObj = bpy.context.object
    headObj.name = "MARKER_HEAD"
    headObj.dimensions.xyz = bb_sim.sim_marker_size, bb_sim.sim_marker_size, bb_sim.sim_marker_size
    headObj.select_set(False)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.01, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    tailObj = bpy.context.object
    tailObj.dimensions.xyz = bb_sim.sim_marker_size, bb_sim.sim_marker_size, bb_sim.sim_marker_size
    tailObj.name = "MARKER_TAIL"
    tailObj.select_set(False)

    if testing == True:
        headObj.show_name = True
        tailObj.show_name = True

    
    
    
    temp_name = utils.get_temp_name() 
    head_material = props['material_head']
    tail_material = props['material_tail']
    headMatObj = None
    tailMatObj = None
    if head_material != "":
        headMatObj = bpy.data.materials.get(head_material)
    if tail_material != "":
        tailMatObj = bpy.data.materials.get(tail_material)
    if headMatObj == None:
        headObj.select_set(True)
        utils.activate(headObj)
        headMatObj = bpy.data.materials.new( "HEAD_MARKER" + "_" + temp_name )
        headObj.data.materials.append(headMatObj)
        headObj.active_material.use_nodes = False
        headObj.active_material.diffuse_color = (0.769954, 0, 0.00977966, 1)
        headObj.select_set(False)
    else:
        headObj.active_material = headMatObj
    if tailMatObj == None:
        tailObj.select_set(True)
        utils.activate(tailObj)
        tailMatObj = bpy.data.materials.new( "TAIL_MARKER" + "_" + temp_name )
        tailObj.data.materials.append(tailMatObj)
        tailObj.active_material.use_nodes = False
        tailObj.active_material.diffuse_color = (0.00244029, 0.581637, 0.769954, 1)
        tailObj.select_set(False)
    else:
        tailObj.active_material = tailMatObj

    props['marker_head'] = headObj
    props['marker_tail'] = tailObj
    props['material_head'] = headObj.active_material.name
    props['material_tail'] = tailObj.active_material.name

    utils.set_state(state)

    return True









def move_marker(testing=False):

    
    
    if props['bmesh'] == "":
        return False
    bm = props['bmesh']
    for v in bm.verts:
        if v.select == True:
            break
    
    
    if v.select == False:
        return False

    
    if v == props['last_vertex']:
        return False

    props['last_vertex'] = v

    
    
    v.select = False

    print("move marker entry:", v.index)

    
    mw = bpy.context.object.matrix_world.copy()

    
    if props['vertex_head'] == "":
        
        
        
        props['last_marker'] = "head" 

        
        props['vertex_head'] = v
        headObj = props['marker_head']
        headObj.location = mw @ v.co

        if testing == True:
            print("First entry, moved head")

        return True

    
    if props['vertex_tail'] == "":
        
        props['vertex_tail'] = v
        tailObj = props['marker_tail']
        tailObj.location = mw @ v.co
        
        props['last_marker'] = "tail"

        if testing == True:
            print("First entry, moved tail")

        return True

    
    

    
    
    
    
    

    
    
    
    
    
    

    
    headObj = props['marker_head']
    tailObj = props['marker_tail']
    
    if props['last_marker'] == 'tail':
        
        props['vertex_head'] = v

        headObj.location = mw @ props['vertex_head'].co.copy()
        
        props['last_marker'] = "head"
        if testing == True:
            print("fall through stored head from tail")

    else:
        props['vertex_tail'] = v

        
        

        tailObj.location = mw @ props['vertex_tail'].co.copy()

        props['last_marker'] = "tail"

        if testing == True:
            print("fall through stored tail from head")

    

    return True










def get_director(object):
    OBJ = object
    if isinstance(object, str):
        OBJ = bpy.data.objects[object]

    
    aObj = OBJ.get('bb_sim_actor')
    
    if aObj == None:
        print("Entry object may be an actor")
        dObj = OBJ.get('bb_sim_director')
        dObjs = OBJ.get('bb_sim_directors')
        
        if dObj == None and dObjs == None:
            print("A: No directors found on the given object")
            return False
        if dObj != None:
            print("A: Found single director, checking.")
            if utils.is_valid(dObj):
                return dObj
            print("A: This is a fall through for a single director, it failed")
        if dObjs != None:
            print("A: Found multiple directors, checking")
            good = []
            for o in dObjs:
                if utils.is_valid(o):
                    good.append(o)
            if len(good) > 0:
                return good
            print("A: This is a fall through for multiple directors, they all failed")
        return False

    
    print("Entry object may be a director")
    if utils.is_valid(aObj):
        print("D: actor is valid")
        dObj = aObj.get('bb_sim_director')
        dObjs = aObj.get('bb_sim_directors')
        
        if dObj == None and dObjs == None:
            print("D: actor has no directors, this could be a bug")
            return False
        if dObj != None:
            print("D: found single director")
            if utils.is_valid(dObj):
                print("returning object:", dObj.name)
                return dObj
            else:
                print("single director is invalid, falling through to check multiple")
        if dObjs != None:
            good = []
            for o in dObjs:
                if utils.is_valid(o):
                    good.append(o)
            if len(good) > 0:
                return good
        else:
            print("Logic issue when examining director regions, this is an API bug")

        return False

    else:
        print("Entry actor does not appear to be in the scene, the caller probably caused this error")
        return False

    
    print("sim::get_director reports: fall through, check your logic")

    return False








def get_actor(object):
    OBJ = object
    if isinstance(object, str):
        OBJ = bpy.data.objects[object]
    if utils.is_valid(OBJ) == False:
        print("sim::get_actor : object is not viable")
        return False
    
    if OBJ.get('bb_sim_actor') != None:
        return OBJ['bb_sim_actor']
    
    if OBJ.get('bb_sim_director') != None:
        return OBJ
    
    if OBJ.get('bb_sim_directors') != None:
        return OBJ

    
    return False









def build_bone(actor=None, director=None, head=None, tail=None, vertices=[]):

    
    
    
    
    
    
    
    

    state = utils.get_state()

    head_loc = head
    tail_loc = tail
    aObj = bpy.data.objects[actor]
    dObj = bpy.data.objects[director]

    
    aObj.select_set(True)
    utils.activate(aObj)
    bpy.ops.object.mode_set(mode='EDIT')
    
    
    
    
    
    
    
    
    
    
    
    bname = "BB_SIM_BONE_" + utils.get_temp_name()
    while bname in aObj.data.bones:
        print("Bone name collision", bname, "getting new one...")
        bname = "BB_SIM_BONE_" + utils.get_temp_name()
    

    boneObj = aObj.data.edit_bones.new(bname)

    
    bone = boneObj.name

    

    if bone in aObj.vertex_groups:
        print("Bone identified as", bone, "collides with existing skinned mesh, this is a major flaw!")
        print("How to fix it: rename the bone in your mesh to something else or don't use skinned mesh for a simulation")

    
    boneObj.head = head_loc
    boneObj.tail = tail_loc

    
    
    

    bpy.ops.object.mode_set(mode='OBJECT')

    
    if bone in dObj.vertex_groups:
        G = dObj.vertex_groups[bone]
        
        
        dObj.vertex_groups.remove(G)

    G = dObj.vertex_groups.new( name = bone )
    G.add(vertices, 1, 'REPLACE')

    
    
    
    
    
    boneObj = aObj.pose.bones[bone]
    aObj.data.bones.active = boneObj.bone 
    bc = boneObj.constraints

    conObj = bc.new('CHILD_OF')
    cname = conObj.name
    conObj.target = dObj
    conObj.subtarget = bone
    conObj.influence = 1
    
    
    
    conObj.use_scale_x = False
    conObj.use_scale_y = False
    conObj.use_scale_z = False
    context_py = bpy.context.copy()
    context_py["constraint"] = bc.active

    
    

    new_state = utils.get_state()
    aObj.select_set(True)
    utils.activate(aObj)
    bpy.ops.object.mode_set(mode='POSE')



    
    utils.set_inverse(context_py, cname)
    
    
    conObj.name = "BB Sim " + cname

    
    
    
    
    
    
    
    if props['group_base'] not in aObj.pose.bone_groups:
        bpy.ops.pose.group_add()
    aObj.pose.bone_groups.active.name = props['group_base']
    aObj.pose.bone_groups.active.color_set = props['theme_base']
    group_base = props['group_base']
    boneObj.bone_group = aObj.pose.bone_groups[group_base]

    utils.set_state(new_state)

    

    aObj.select_set(False)

    dObj.select_set(True)
    utils.activate(dObj)

    utils.set_state(state)

    
    return boneObj








def get_sim_armature(objects):
    mesh = []
    for o in objects:
        if o.type == 'MESH':
            mesh.append(o)
    if len(mesh) == 0:
        print("sim::get_sim_armature reports: no mesh was provided")
        return False, False
    actors = set()
    for o in mesh:
        a = o.get('bb_sim_actor')
        if a == None:
            print("The object mesh", o.name, "has no actor")
            return False, False
        try:
            if a.name not in bpy.context.scene.objects:
                print("The object mesh", o.name, "has a simulator actor but the object is not available")
                return False, False
        except:
            print("The property bb_sim_actor on mesh object", o.name, "is damaged")
            return False, False
        actors.add(a)
    if len(actors) == 0:
        print("The actors amount to 0, this really shouldn't happen")
        return False, False
    if len(actors) > 1:
        print("Too many actors, limit your selection to objects that share the same")
        print("simulator set.")
        return False, False

    armObj = list(actors)[0]
    arm = armObj.name
    mesh_names = [m.name for m in mesh]

    return (arm, mesh_names)

            
            
            
            
            
                
                    













def export_fix(selected):
    mesh = []
    
    
    
    for o in selected:
        if o.type == 'MESH':
            for m in o.modifiers:
                if m.type == 'ARMATURE':
                    continue
                
            mesh.append(o)
    if len(mesh) == 0:
        print("sim::export_fix reports: does not appear to be a simulator set")
        return False
    
    
    qualified = {}
    for o in mesh:
        a = o.get('bb_sim_actor')
        if a == None:
            continue
        try:
            if a.name not in bpy.context.scene.objects:
                print("The object", o.name, "has a simulator actor but the object is not available")
                continue
            qualified[o] = a
        except:
            print("The object", o.name, "has a simulator actor but the object never existed in this scene")
    
    if len(qualified) == 0:
        print("sim::export_fix reports: no qualified mesh were present")
        return False

    
    

    
    
    
    
    for o in qualified:
        aObj = o.get('bb_sim_actor')
        if aObj != None:
            if aObj.get('bb_sim_director') != None:
                dObj = aObj.get('bb_sim_director')
                if dObj == None:
                    print("Something weird happened attempting to get the dynamic sim director")
                else:
                    print("Found dynamic sim", o.name)
                    for o in bpy.context.selected_objects:
                        o.select_set(False)
                    dObj.select_set(True)
                    aObj.select_set(True)
                    utils.activate(aObj)
                    
                    for boneObj in aObj.pose.bones:
                        for C in boneObj.constraints:
                            C.influence = 0
                    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
                    return True

    print("Found object sim")

    
    for o in qualified:
        o.parent = qualified[o]
    
    for o in qualified:
        m = o.modifiers.new(name='Armature', type='ARMATURE')
        m.object = qualified[o]
        m.use_vertex_groups = True

    
    

    return True









def sync(aObj):

    bb_sim = bpy.context.window_manager.bb_sim

    try:
        if aObj.name not in bpy.context.scene.objects:
            print("sim::sync reports: the object is missing")
            return False
    except:
        print("sim::sync reports: invalid objecdt")
        return False
    
    dObj = aObj.get('bb_sim_director')
    if dObj == None:
        print("Can't sync, no director")
        return False
    if utils.is_valid(dObj) == False:
        print("Cant' sync, director is unavailable")
        return False

    
    groups = set([g.name for g in dObj.vertex_groups])
    for boneObj in aObj.data.bones:
        bone = boneObj.name
        if bone in groups:
            G = dObj.vertex_groups[bone]
            dObj.vertex_groups.remove(G)

    
    state = utils.get_state()

    
    aObj.select_set(True)
    utils.activate(aObj)
    bpy.ops.object.mode_set(mode='EDIT')
    heads = {}
    for boneObj in aObj.data.edit_bones:
        heads[boneObj.name] = boneObj.head.copy()
    bpy.ops.object.mode_set(mode='OBJECT')

    
    dmw = dObj.matrix_world.copy()
    size = len(dObj.data.vertices)
    kd = mathutils.kdtree.KDTree(size)
    for v in dObj.data.vertices:
        v_co = dmw @ v.co
        kd.insert(v_co, v.index)
    kd.balance()

    
    
    for bone in heads:
        hloc = heads[bone]
        vertices = []
        if bb_sim.sim_path_radius == 0:
            loc, index, dist = kd.find(hloc)  
            vertices.append(index)
        else:
            for loc, index, dist in kd.find_range(hloc, bb_sim.sim_path_radius):
                vertices.append(index)
        
        G = dObj.vertex_groups.new( name = bone )
        G.add(vertices, 1, 'REPLACE')
        for C in aObj.pose.bones[bone].constraints:
            C.influence = 1
            C.target = dObj
            C.subtarget = bone

    utils.set_state(state)

    return True






def ik_length(set=False, count=1):
    
    
    
    
    selected = bpy.context.selected_objects
    if len(selected) != 1:
        return False
    o = selected[0]
    if o.type != 'ARMATURE':
        return False
    if o.data.bones.active == None:
        return False
    boneObj = o.data.bones.active
    bone = boneObj.name
    if bone not in o.data.bones:
        return False
    
    if o.pose.bones[bone].id_data != o:
        return False
    
    for boneObj in o.pose.bones:
        for C in boneObj.constraints:
            if C.type == 'IK':
                old_count = C.chain_count
                if set == True:
                    C.chain_count = count
                
                if old_count == 0:
                    print("ik_length: 0 converted to True to prevent a bug, this should be fixed!")
                    return True
                return old_count
    return False





def vertex_constraint(arm=None, bone=None, mesh=None, vertices=[], influence=1, location=True, rotation=True, scale=False):
    armObj = arm
    boneObj = bone
    meshObj = mesh
    if isinstance(arm, str):
        armObj = bpy.data.objects[arm]
    if isinstance(bone, str):
        boneObj = armObj.pose.bones[bone]
    if isinstance(mesh, str):
        meshObj = bpy.data.objects[mesh]
    if len(vertices) == 0:
        print("utils::vertex_constraint : No vertices were delivered, nothing to do ")
        return False

    
    G = meshObj.vertex_groups.new( name = boneObj.name )
    G.add(vertices, 1, 'REPLACE')

    
    armObj.data.bones.active = boneObj.bone 
    bc = boneObj.constraints

    conObj = bc.new('CHILD_OF')
    cname = conObj.name
    conObj.target = meshObj
    conObj.subtarget = boneObj.name
    conObj.influence = influence
    conObj.use_location_x = location
    conObj.use_location_y = location
    conObj.use_location_z = location
    conObj.use_rotation_x = rotation
    conObj.use_rotation_y = rotation
    conObj.use_rotation_z = rotation
    conObj.use_scale_x = scale
    conObj.use_scale_y = scale
    conObj.use_scale_z = scale

    
    
    
    context_py = bpy.context.copy()
    context_py["constraint"] = bc.active

    
    
    if 1 == 0:
        new_state = utils.get_state()
        aObj.select_set(True)
        utils.activate(aObj)
        bpy.ops.object.mode_set(mode='POSE')

    
    set_inverse(context_py, cname)
    
    
    conObj.name = "BB Sim " + cname

    
    
    
    
    
    
    
    if props['group_base'] not in armObj.pose.bone_groups:
        bpy.ops.pose.group_add()
    armObj.pose.bone_groups.active.name = props['group_base']
    armObj.pose.bone_groups.active.color_set = props['theme_base']
    group_base = sim.props['group_base']
    boneObj.bone_group = armObj.pose.bone_groups[group_base]

    return True




