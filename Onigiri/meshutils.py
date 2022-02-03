

import bpy
import mathutils 
from mathutils import Vector 
import math
from math import *
from . import rigutils
from . import utils
from .presets import bone_sides



import bpy
import uuid








def clean_groups(object=""):
    obj = bpy.data.objects[object]
    def removeEmptyGroups(obj, thres = 0):
        z = []
        for v in obj.data.vertices:
            for g in v.groups:
                if g.weight > thres:
                    if g not in z:
                        z.append(obj.vertex_groups[g.group])
        for r in obj.vertex_groups:
            if r not in z:
                obj.vertex_groups.remove(r)

    def removeZeroVerts(obj, thres = 0):
        for v in obj.data.vertices:
            z = []
            for g in v.groups:
                if not g.weight > thres:
                    z.append(g)
            for r in z:
                obj.vertex_groups[g.group].remove([v.index])

    
    obj = bpy.context.active_object
    if(obj.type == 'MESH'):
        em = None
        if obj.mode == 'EDIT':
            em = obj.mode
            bpy.ops.object.mode_set()
        removeZeroVerts(obj)
        removeEmptyGroups(obj)
        obj.data.update()
        if em:
            bpy.ops.object.mode_set(mode=em)










def remove_empty_groups(mesh):
    print("meshutils::remove_empty_groups : called with", mesh)
    preserve = bpy.context.scene.bb_devkit.preserve_empty_counterparts

    def survey(meshObj):
        maxWeight = {}
        for i in meshObj.vertex_groups:
            maxWeight[i.index] = 0

        for v in meshObj.data.vertices:
            for g in v.groups:
                gn = g.group
                
                try:
                    w = meshObj.vertex_groups[g.group].weight(v.index)
                except:
                    pass
                if (maxWeight.get(gn) is None or w>maxWeight[gn]):
                    maxWeight[gn] = w
        return maxWeight

    meshObj = bpy.data.objects[mesh]
    
    armObj = get_armature(meshObj)
    if armObj == False:
        print("There's no functional armature associated with the mesh", meshObj.name, "so there's no way to prune the weight groups properly.")
        return False

    maxWeight = survey(meshObj)
    ka = []
    ka.extend(maxWeight.keys())
    ka.sort(key=lambda gn: -gn)

    
    
    
    

    non_zero = set() 
    has_zero = set()
    if preserve == True:
        print("Generating a counterpart set for", mesh)
        for gn in ka:
            name = meshObj.vertex_groups[gn].name
            
            if name not in armObj.data.bones:
                continue
            if maxWeight[gn]<=0:
                
                has_zero.add(name)
            else:
                non_zero.add(name)

    count = 0
    for gn in ka:
        if maxWeight[gn]<=0:
            name = meshObj.vertex_groups[gn].name
            if name in bone_sides.both_sides:
                counter_name = bone_sides.both_sides[name]
                if counter_name in non_zero:
                    print("Skipping mirrored vertex group:", name)
            if name not in armObj.data.bones:
                print("Skipping utility group:", name)
                continue
            else:
                count += 1
                meshObj.vertex_groups.remove(meshObj.vertex_groups[gn])

    print("Removed", count, "vertex groups from", mesh)

    
    
    
    















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










def get_one_armature(objects=None):
    obj = bpy.data.objects
    arms = {}

    if objects == None:
        print("meshutils::get_one_armature reports: nothing to do")
        return False, False

    meshes = []
    if isinstance(objects[0], str):
        for m in objects:
            meshes.append(m)
    else:
        for o in objects:
            meshes.append(o.name)
    objects = meshes

    
    for mesh in objects:
        if obj[mesh].type != 'MESH':
            continue
        
        
        mods = []
        for m in obj[mesh].modifiers:
            if m.type == 'ARMATURE':
                mods.append(m.name)
                modObj = m 
        
        
        
        if len(mods)> 1:
            print("The mesh", mesh, "has more than one armature modifiers")
            return False, False
        if len(mods) == 0:
            print("There's no armature modifier available for", mesh)
            return False, False
        if modObj.object != None:
            arm = modObj.object.name
            if arm not in arms:
                arms[arm] = list()
            arms[arm].append(mesh)

    if len(arms) > 1:
        print("The chosen mesh have a combination of", len(arms), "rigs among them, there's no way to determine a target")
        return False, False
    if len(arms) == 0:
        print("There were no armatures associated with any of the given mesh")
        return False, False
    
    
    
    return (arm, arms[arm])









def combine_weights(group_new, groups, target):

    
    
    
    
    
    if isinstance(groups, list):
        group_input = {a for a in groups}
    else:
        print("meshutils::combine_weights reports: this new function requires a list, not a set like the old one")
        return False

    
    
    

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

    
    
    for g in groups:
        grp_del = ob.vertex_groups[g]
        ob.vertex_groups.remove(grp_del)
    grp_del = ob.vertex_groups[target]
    ob.vertex_groups.remove(grp_del)
    ob.vertex_groups[group_new].name = target

    return







def combine_groups(groups=None, target=None, mesh=None):
    meshObj = mesh
    if isinstance(mesh, str):
        meshObj = bpy.data.objects[mesh]
    group_input = set(groups)
    ob = meshObj

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
        
        
        
        temp = utils.get_temp_name()
        while temp in meshObj.vertex_groups:
            temp = utils.get_temp_name()

        
        vgroup = ob.vertex_groups.new(name=temp)
        
        
        for key, value in vertex_weights.items():
            vgroup.add([key], value ,'REPLACE') 

        for group in groups:
            grp_del = meshObj.vertex_groups[group]
            meshObj.vertex_groups.remove(grp_del)

        
        
        meshObj.vertex_groups[temp].name = target

    return








def merge_groups(group=None, target=None, mesh=None, report=False):

    meshObj = mesh
    if isinstance(mesh, str):
        meshObj = bpy.data.objects[mesh]

    if group not in meshObj.vertex_groups:
        if report == True:
            print("The reskin bone/group doesn't exist in the mesh:", group)
        return False

    
    if target not in meshObj.vertex_groups:
        meshObj.vertex_groups.new(name=target)

    
    group_input = {}
    group_input[group] = None 
    group_input[target] = None 

    
    temp = utils.get_temp_name()
    while temp in meshObj.vertex_groups:
        temp = utils.get_temp_name()

    if 1 == 0:
        for i in range(10):
            temp = utils.get_temp_name()
            if temp not in meshObj.vertex_groups:
                break
            else:
                if report == True:
                    print("meshutils::merge_groups reports : Name collision when attempting to get a unique name, trying again:", str(i))
        if temp in meshObj.vertex_groups:
            if report == True:
                print("meshutils::merge_groups reports : unique name failed")
            return False

    
    vertex_weights = {}



    for vert in meshObj.data.vertices:
        if len(vert.groups):  
            for item in vert.groups:
                vg = meshObj.vertex_groups[item.group]
                if vg.name in group_input:
                    if vert.index in vertex_weights:    
                        vertex_weights[vert.index] += vg.weight(vert.index)
                    else:
                        vertex_weights[vert.index] = vg.weight(vert.index)

       
    
    for key in vertex_weights.keys():
        if (vertex_weights[key] > 1.0): vertex_weights[key] = 1.0

    
    vgroup = meshObj.vertex_groups.new(name=temp)

    
    for key, value in vertex_weights.items():
        vgroup.add([key], value ,'REPLACE') 

    
    
    
        
        
        
            
        
        
    grp_del = meshObj.vertex_groups[group]
    meshObj.vertex_groups.remove(grp_del)

    grp_del = meshObj.vertex_groups[target]
    meshObj.vertex_groups.remove(grp_del)
    meshObj.vertex_groups[temp].name = target

    return True






def merge_fuzzy(group=None, target=None, mesh=None, report=False):

    meshObj = mesh
    if isinstance(mesh, str):
        meshObj = bpy.data.objects[mesh]

    if group not in meshObj.vertex_groups:
        if report == True:
            print("The reskin bone/group doesn't exist in the mesh:", group)
        return False

    
    if target not in meshObj.vertex_groups:
        meshObj.vertex_groups.new(name=target)

    
    temp = utils.get_temp_name()
    while temp in meshObj.vertex_groups:
        temp = utils.get_temp_name()
    
    vgroup = meshObj.vertex_groups.new(name=temp)

    
    
    
    
    
    
    
    
    
    
    

    if 1 == 0:
        modObj = meshObj.modifiers.new(type='VERTEX_WEIGHT_MIX', name="Vertex Weight Mix")
        modObj.vertex_group_a = temp
        modObj.vertex_group_b = target
        modObj.mix_mode = 'ADD'
        modObj.mix_set = 'B' 
        bpy.ops.object.modifier_apply(modifier=modObj.name)
        
        modObj = meshObj.modifiers.new(type='VERTEX_WEIGHT_MIX', name="Vertex Weight Mix")
        modObj.vertex_group_a = temp
        modObj.vertex_group_b = group
        modObj.mix_mode = 'ADD'
        modObj.mix_set = 'B' 
        bpy.ops.object.modifier_apply(modifier=modObj.name)

        
        groupObj = meshObj.vertex_groups[target]
        meshObj.vertex_groups.remove(groupObj)
        groupObj = meshObj.vertex_groups[group]
        meshObj.vertex_groups.remove(groupObj)
        
        meshObj.vertex_groups[temp].name = target

    
    
    
    
    modObj = meshObj.modifiers.new(type='VERTEX_WEIGHT_MIX', name="Vertex Weight Mix")
    modObj.vertex_group_a = target
    modObj.vertex_group_b = group
    
    modObj.mix_mode = 'ADD'
    modObj.mix_set = 'B' 




    
    

    
    
    
    try:
        
        print("Blender 2.8x")
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modObj.name)
        print("Success for Blender 2.8x")
    except:
        
        print("Blender 2.9x")
        try:
            bpy.ops.object.modifier_apply(modifier=modObj.name)
            print("Success for Blender 2.9x")
        except:
            print("Blender 2.9 failed, nothing left to do")
            return False

    utils.update()
    groupObj = meshObj.vertex_groups[group]
    meshObj.vertex_groups.remove(groupObj)


    return True


    
    group_input = {}
    group_input[group] = None 
    group_input[target] = None 

    
    temp = utils.get_temp_name()
    while temp in meshObj.vertex_groups:
        temp = utils.get_temp_name()


    return True







def get_unique_name_short():
    
    found = "yes" 
    break_point = 0 
    while found == "yes":
        unique_name = str(uuid.uuid4())
        break_point += 1
        if unique_name not in bpy.data.objects:
            name_search = "not found"
            break
        if break_point == 100:
            print("get_unique_name_short reports: 100 names were searched and found, this probably can't happen")
            popup("Houston we have a problem!  Name collision, check console", "Name Collision 100", "ERROR")
            break
    
    
    return unique_name.split('-', 1)[0]









def get_mesh_armature(mesh=""):
        print("get_mesh_armature one runs")
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



def mesh_from_rig(armature=None):
    
    def boneGeometry( l1, l2, x, z, baseSize, l1Size, l2Size, base ):
        x1 = x * baseSize * l1Size 
        z1 = z * baseSize * l1Size

    
    
        
        x2 = Vector( (0, 0, 0) )
        z2 = Vector( (0, 0, 0) )

        verts = [
            l1 - x1 + z1,
            l1 + x1 + z1,
            l1 - x1 - z1,
            l1 + x1 - z1,
            l2 - x2 + z2,
            l2 + x2 + z2,
            l2 - x2 - z2,
            l2 + x2 - z2
            ] 

        faces = [
            (base+3, base+1, base+0, base+2),
            (base+6, base+4, base+5, base+7),
            (base+4, base+0, base+1, base+5),
            (base+7, base+3, base+2, base+6),
            (base+5, base+1, base+3, base+7),
            (base+6, base+2, base+0, base+4)
            ]

        return verts, faces

    print("Generating mesh from rig:", armature)

    obj = bpy.data.objects
    armObj = obj[armature]

    name = armObj.name + "_mesh"
    meshData = bpy.data.meshes.new( name + "Data" )
    meshObj = bpy.data.objects.new( name, meshData )
    

    
    
    
    
    bpy.context.scene.collection.objects.link(meshObj)
    bpy.context.view_layer.update()

    
    

    
    for o in bpy.context.selected_objects:
        o.select_set(False)
    armObj.select_set(True)
    bpy.context.view_layer.objects.active = armObj

    verts = []
    edges = []
    faces = []
    vertexGroups = {}

    bpy.ops.object.mode_set(mode='EDIT')

    try:
        
        for editBone in [b for b in armObj.data.edit_bones if b.use_deform]:
            boneName = editBone.name
            
            poseBone = armObj.pose.bones[boneName]

            
            editBoneHead = editBone.head
            editBoneTail = editBone.tail
            editBoneVector = editBoneTail - editBoneHead
            editBoneSize = editBoneVector.dot( editBoneVector )
            editBoneRoll = editBone.roll
            editBoneX = editBone.x_axis
            editBoneZ = editBone.z_axis
            editBoneHeadRadius = editBone.head_radius
            editBoneTailRadius = editBone.tail_radius

            
            baseIndex = len(verts)
            baseSize = sqrt( editBoneSize )
            newVerts, newFaces = boneGeometry( editBoneHead, editBoneTail, editBoneX, editBoneZ, baseSize, editBoneHeadRadius, editBoneTailRadius, baseIndex )

            verts.extend( newVerts )
            faces.extend( newFaces )

            
            vertexGroups[boneName] = [(x, 1.0) for x in range(baseIndex, len(verts))]

        
        meshObj.data.from_pydata(verts, edges, faces)

    except:
        bpy.ops.object.mode_set(mode='OBJECT')
    else:
        bpy.ops.object.mode_set(mode='OBJECT')

    for name, vertexGroup in vertexGroups.items():
        groupObject = meshObj.vertex_groups.new(name=name)
        for (index, weight) in vertexGroup:
            groupObject.add([index], weight, 'REPLACE')

    
    modifier = meshObj.modifiers.new('ArmatureMod', 'ARMATURE')
    modifier.object = armObj
    modifier.use_bone_envelopes = False
    modifier.use_vertex_groups = True

    meshObj.data.update()

    meshObj.parent = armObj
    armObj.select_set(False)
    meshObj.select_set(True)
    bpy.context.view_layer.objects.active = meshObj

    meshObj.matrix_world = armObj.matrix_world.copy()

    
    

    return meshObj.name










    
    
        
        
        
        
        

    
    
        
        

    
    
        
        
        

        
            
            
            
            
            
            
            
            
            

        
            
            
            
            
            
            
            

        

    
    
        

        
        
        
        

        
        
        

        
        
        
        

        

        
            
            
                
                
                

                
                
                
                
                
                
                
                
                
                

                
                
                
                

                
                

                
                

            
            

        
            
        
            

        
        
            
                
                
                    

        
        
        
        
        

        

        
        
        
        

        

    

    

    

    
        
    
        
    
        





















def mesh_integrity_check(mesh=None, armature=None):

    if not mesh:
        print("meshutils:mesh_integrity_check reports: No mesh to process")
        return False
    if not armature:
        print("meshutils:mesh_integrity_check reports: No armature to process")
        return False

    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
        
            
                
                
                
        

    

    
    

    obj = bpy.data.objects
    arm = armature
    bbm = bpy.context.window_manager.bb_misc
    group_limit = bbm.group_count_limit
    error_count = 0
    error_notes = {}
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    
    if len(obj[mesh].vertex_groups) > group_limit:
        error_count += 1
        
        
        
        
        
        print("Mesh", mesh, "vertex groups total", len(obj[mesh].vertex_groups), "exceeds group limit of", group_limit)

    
    status = get_mesh_armature(mesh=mesh)
    if status == False:
        print("meshutils::mesh_intergrity_check reports: Mesh did not pass armature validation test -", mesh)
        error_count += 1
        error_notes['armature'] = "Mesh did not pass armature validation"
        return error_notes

    bad_verts = [] 
    bad_groups = {} 
    bad_amount = [] 
    for v in obj[mesh].data.vertices:
        if len(v.groups) == 0:
            bad_verts.append(v.index)
        elif len(v.groups) > 4:
            bad_amount.append(v.index)
        for ig in v.groups:
            vertex_index = v.index
            vertex_loc = v.co.copy()
            group_index = ig.group
            group_name = obj[mesh].vertex_groups[ig.group].name
            
            if group_name not in obj[arm].data.bones:
                bad_groups[group_name] = ""
            weight = ig.weight

    
    
    if len(bad_amount) > 0:
        error_count += 1
        error_notes['influences'] = "Too many bone influences"
        print("meshutils::mesh_intergrity_check reports:")
        print("There were", len(bad_amount), "vertices weighted to more than 4 bones, use the (Limit bone influences) tool to correct it")
    if len(bad_verts) > 0:
        error_count += 1
        error_notes['unweighted'] = "There were unweighted vertices"
        uv = len(bad_verts)
        print("meshutils::mesh_intergrity_check reports:")
        print("Unweighted vertices:", uv)
    if len(bad_groups) > 0:
        error_count += 1
        error_notes['missing_bones'] = "Unmatched bones for groups"
        print("meshutils::mesh_intergrity_check reports:")
        print("Unmatched group names, no bone association:", [ a for a in bad_groups ])

    if error_count > 0:
        print("meshutils::mesh_intergrity_check reports:")
        txt = "There were " + str(error_count) + " errors that would prevent your mesh from working properly in Second Life, check console."
    else:
        print("meshutils::mesh_intergrity_check reports:")
        txt = "The integrity check found no errors preventing your mesh from working in Second Life, check console."

    
    return error_notes
    








def split_mesh(mesh=None, group_limit=110):
    print("running split_mesh on", mesh)

    obj = bpy.data.objects

    
    if mesh == None:
        if bpy.context.active_object == None:
            print("meshutils::split_mesh reports: No mesh and no active object, can't do anything")
            return []
        mesh = bpy.context.active_object.name

    
    for o in bpy.context.selected_objects:
        o.select_set(False)
    obj[mesh].select_set(True)
    bpy.context.view_layer.objects.active = obj[mesh]

    
    
    
    

    group_count = len(obj[mesh].vertex_groups)

    
    portions = list()
    count = 0
    for gc in range(group_count):
        count += 1
        if count == group_limit:
            portions.append(count)
            count = 0
    
    if count < group_limit:
        portions.append(count)




    print("The mesh", mesh, "will be split into", len(portions), "parts")

    
    
    
    
    
    
    
    

    
    
    
    
    
    
    

    
    
    
    

    
    
    
    
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_mode(type="VERT")
    
    
    
    bpy.ops.mesh.select_all(action = 'SELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')


    
    
    
    
    
    
    
    
    results = []
    for d in portions:
        obj[mesh].select_set(True)
        bpy.context.view_layer.objects.active = obj[mesh]
        bpy.ops.object.duplicate()
        o = bpy.context.object
        results.append(o.name)
        o.select_set(False)

    bpy.context.view_layer.update()

    

    
    
    
    split_list = []
    count = 0

    
    
    
    
    
    
    
    

    
    
    for i in range(len(portions)):
        mesh = results[i] 
        p = portions[i] 
        obj[mesh].select_set(True)
        bpy.context.view_layer.objects.active = obj[mesh]
        bpy.ops.object.mode_set(mode = 'EDIT')

        
        
        for g in range(p):
            obj[mesh].vertex_groups.active_index = count+g
            bpy.ops.object.vertex_group_deselect()

        
        
        
        
        bpy.ops.mesh.delete(type='VERT')

        bpy.ops.object.mode_set(mode = 'OBJECT') 
        count += p 
        obj[mesh].select_set(False)


    return results








def restore_shape(mesh=None, shape=[]):
    obj = bpy.data.objects

    return True








def select_half(mesh):
    import bpy
    import bmesh
    from mathutils.geometry import distance_point_to_plane
    from mathutils import Vector

    partition = "y" 

    context = bpy.context

    def bbox(ob):
        return (Vector(b) for b in ob.bound_box)

    def bbox_center(ob):
        return sum(bbox(ob), Vector()) / 8

    def bbox_axes(ob):
        bb = list(bbox(ob))
        return tuple(bb[i] - bb[0] for i in (4, 3, 1))

    ob = context.edit_object
    o = bbox_center(ob)
    x, y, z = bbox_axes(ob) 

    print(o, x, y, z)
    

    me = ob.data
    bm = bmesh.from_edit_mesh(me)
    for v in bm.verts:
        v.select = distance_point_to_plane(v.co, o, partition) >= 0

    bmesh.update_edit_mesh(me) 





def build_mesh(shape="diamond"):
    if shape=="diamond":
        bpy.ops.mesh.primitive_uv_sphere_add(segments=3, ring_count=3, radius=0.03, enter_editmode=False, location=(0, 0, 0))
        meshObj = bpy.context.object
        meshObj.name = "DIAMOND_MESH"
        
        vert_pairs = {
            0:1, 2:3, 5:6, }
        
        vhead = 2
        vtail = 4
        
        skin_verts = [0,1,2,3,4]
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        for i1 in vert_pairs:
            bpy.ops.object.mode_set(mode = 'OBJECT')
            i2 = vert_pairs[i1]
            v1 = meshObj.data.vertices[i1]
            v2 = meshObj.data.vertices[i2]
            v1.select = True
            v2.select = True
            c1 = v1.co
            c2 = v2.co
            
            cm = c1.lerp(c2, 0.5)
            
            v1.co = cm
            v2.co = cm
            
            
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.remove_doubles()
        bpy.ops.object.mode_set(mode = 'OBJECT')

    else:
        print("unknown shape:", shape)
        return False

    return meshObj














def bones_to_mesh(armature=None, bones=[], target=None, separate=False, middle=False):

    if target == None:
        target = armature
        print("No target, setting to armature:", armature)

    obj = bpy.data.objects
    armObj = obj[armature]

    
    R90 = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'X')
    
    R90I = R90.inverted()

    mesh_list = []
    mw = armObj.matrix_world.copy()

    new_origin = mw.to_translation()
    cursor_location = bpy.context.scene.cursor.location
    cursor_now = mw.to_translation()

    
    
    
    
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=3, ring_count=3, radius=0.03, enter_editmode=False, location=(0, 0, 0))
    meshObj = bpy.context.object
    meshObj.name = "BONE_MESH"
    
    vert_pairs = {
        0:1, 2:3, 5:6, }
    
    vhead = 2
    vtail = 4
    
    skin_verts = [0,1,2,3,4]
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    for i1 in vert_pairs:
        bpy.ops.object.mode_set(mode = 'OBJECT')
        i2 = vert_pairs[i1]
        v1 = meshObj.data.vertices[i1]
        v2 = meshObj.data.vertices[i2]
        v1.select = True
        v2.select = True
        c1 = v1.co
        c2 = v2.co
        
        cm = c1.lerp(c2, 0.5)
        
        v1.co = cm
        v2.co = cm
        
        
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.mode_set(mode = 'OBJECT')




    
    if len(bones) == 0:
        for boneObj in armObj.data.bones:
            bones.append(bone.name)
    for bone in bones:
        boneObj = obj[armature].data.bones[bone]

        bpy.ops.object.duplicate()
        newObj = bpy.context.object

        mesh_list.append(newObj)
        
        newObj.select_set(False)
        meshObj.select_set(True)
        bpy.context.view_layer.objects.active = meshObj

        
        
        

        l, r, s = boneObj.matrix_local.decompose()
        S = mathutils.Matrix()
        for i in range(3):
            S[i][i] = s[i]
        R = r.to_matrix().to_4x4()
        
        head = boneObj.head_local
        tail = boneObj.tail_local
        center = head
        if middle == True:
            center = head.lerp(tail, 0.5)
        C = mathutils.Matrix.Translation(center)

        L = mathutils.Matrix.Translation(l)
        bmat = C @ R @ S
        bmat = bmat @ R90

        newObj.matrix_world = mw @ bmat




        if 1 == 0:
            ci = newObj.matrix_world.inverted()
            vchead = (ci @ mw).to_translation()

            newObj.data.vertices[vhead].co = vchead
            newObj.data.vertices[vtail].co = vctail


        
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        newObj.data.transform(mathutils.Matrix.Translation(-new_origin))
        newObj.matrix_world.translation += new_origin

        
        
        new_vertex_group = newObj.vertex_groups.new(name=boneObj.name)
        new_vertex_group.add(skin_verts, 1.0, 'ADD')


    
    newObj.select_set(False)
    meshObj.select_set(True)
    bpy.context.view_layer.objects.active = meshObj
    bpy.ops.object.delete()

    
    
    bpy.context.view_layer.objects.active = newObj
    for newObj in mesh_list:
        newObj.select_set(True)

    if separate == False:
        bpy.ops.object.join()
        
        
        newObj = bpy.context.object

        
        
        
        
        newObj['bentobuddy_mesh_rig'] = 1

        
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        newObj.data.transform(mathutils.Matrix.Translation(-new_origin))
        newObj.matrix_world.translation += new_origin

        
        modObj = newObj.modifiers.new('Armature', 'ARMATURE')
        modObj.object = obj[target]
        newObj.parent = obj[target]
    else:
        
        for meshObj in mesh_list:
            modObj = meshObj.modifiers.new('Armature', 'ARMATURE')
            modObj.object = obj[target]
            meshObj.parent = obj[target]
    
    return [o.name for o in bpy.context.selected_objects]









def get_exportable_mesh(objects=None, report=False):
    if len(objects) == 0:
        if report == True:
            print("There are no objects selected to export")
            popup("There's nothing selected", "Error", "ERROR")
        return False
    
    new_objects = []
    for o in objects:
        if o.type == 'MESH':
            new_objects.append(o)
    if len(new_objects) == 0:
        if report == True:
            print("There are no qualified mesh selected to export")
            popup("There's no mesh selected to export", "Error", "ERROR")
        return False
    
    new_arms = set()
    for o in new_objects:
        arm = get_mesh_armature(mesh=o.name)
        
        if arm != False:
            new_arms.add(arm)
    if len(new_arms) == 0:
        if report == True:
            print("There were no armatures associated with any of the qualified mesh")
            popup("No armatures supplied", "Error", "ERROR")
        return False
    if len(new_arms) > 1:
        if report == True:
            print("There were multiple armatures associated with your mesh, we can't export this just yet.")
            popup("Too many armatures supplied", "Error", "ERROR")
        return False
    
    a = list(new_arms)
    arm = a[0]
    result = {
        "mesh": new_objects,
        "armature": arm,
        
        "armObj": bpy.data.objects[arm],
        }
    return result









def clone_mesh(mesh=None):
    
    
    
    
    
    
    state = utils.get_state()

    qualified_mesh = []
    for o in mesh:
        if o.type == 'MESH':
            qualified_mesh.append(o)
    if len(qualified_mesh) == 0:
        print("meshutils::clone_mesh reports: no mesh found")
        return False
    
    
    meshObj = qualified_mesh[0]
    for modObj in meshObj.modifiers:
        if modObj.type == 'ARMATURE':
            armObj = modObj.object
            break 

    
    for o in bpy.context.selected_objects:
        o.select_set(False)

    
    for o in qualified_mesh:
        o.select_set(True)
    bpy.context.view_layer.objects.active = o

    
    bpy.ops.object.duplicate()

    
    cloned_mesh = [o for o in bpy.context.selected_objects]

    
    sourceObj = rigutils.build_sl_rig(rig_class="pos", rotate=True)

    
    modObj.object = sourceObj
    for meshObj in cloned_mesh:
        meshObj.parent = sourceObj

    
    rigutils.snap_to(source=sourceObj.name, target=armObj.name)

    
    for o in bpy.context.selected_objects:
        o.select_set(False)

    
    clones = {
        "armature": sourceObj,
        "mesh": cloned_mesh,
        }

    
    utils.set_state(state)

    
    return clones









def get_mesh_armature(mesh=""):
        print("get_mesh_armature two runs")
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









def clean(object=None, copy=False, rotation=True, location=False, scale=True, pose=True):


    if isinstance(object, str):
        OBJ = bpy.data.objects[object]
    else:
        OBJ = object
    try:
        if OBJ.name not in bpy.context.scene.objects:
            print("Object was removed")
            return False
    except:
        print("The object is just plain missing from the scene")
        return False




    print("meshutils::clean is not functional")
    return False



    if len(objects) == 0 and len(selected) == 0:
        print("No objects to process")
        return False

    
    
    mark = False
    for o in selected:
        if o.type == 'MESH':
            mark = True
            break
    if mark == False:
        print("No mesh to process")
        return False

    state = utils.get_state()

    if copy == True:
        for o in selected:
            o.select_set(True)
        utils.activate(o)
        bpy.ops.object.duplicate()
        selected = bpy.context.selected_objects
        for o in selected:
            o.select_set(False)

    mesh = []
    for m in selected:
        if m.type == 'MESH':
            mesh.append(m)

    frame_current = bpy.context.scene.frame_current
    for meshObj in mesh:
        meshObj.select_set(True)
        utils.activate(meshObj)

        
        if pose == True:
            armObj = None
            if meshObj.parent:
                if meshObj.parent.type == 'ARMATURE':
                    armObj = meshObj.parent
            
            if armObj == None:
                
                
                for modObj in meshObj.modifiers:
                    if modObj.type == 'ARMATURE':
                        if modObj.object != None:
                            armObj = modObj.object
            
            if armObj != None:
                frame_start = 1
                if armObj.animation_data:
                    if armObj.animation_data.action:
                        frame_start = armObj.animation_data.action.frame_range[0]
                bpy.context.scene.frame_set(frame_start)

        print("Attempting to apply modifiers...")
        for modObj in meshObj.modifiers:
            try:
                
                print("Blender 2.8x")
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modObj.name)
                print("Success for Blender 2.8x")
            except:
                
                try:
                    print("Blender 2.9x")
                    bpy.ops.object.modifier_apply(modifier=modObj.name)
                    print("Success for Blender 2.9x")
                except:
                    print("Internal Error 507 - Blender 2.9 alternative didn't work, this should not happen")
                    popup("Internal Error 507, contact support with the contents of the console window", "Fatal Error", "ERROR")
                    print("modifier error, removing:", modObj.name)
                    meshObj.modifiers.remove(modObj)
        
        freeze(meshObj)

        
        
        bpy.ops.object.transform_apply(scale=scale, rotation=rotation, location=location)

    bpy.context.scene.frame_set(frame_current)
    return selected









def freeze(object=None, copy=False):
    OBJ = object
    if isinstance(object, str):
        OBJ = bpy.data.object[object]

    state = utils.get_state()

    if copy == True:
        OBJ.select_set(True)
        utils.activate(OBJ)
        bpy.ops.object.duplicate()
        meshObj = bpy.context.object
    else:
        meshObj = OBJ

    
    
    bpy.ops.object.convert(target='MESH')
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return meshObj








    mat = meshObj.matrix_world

    loc, rot, sca = mat.decompose()

    mat_loc = mathutils.Matrix.Translation(loc)
    mat_rot = rot.to_matrix().to_4x4()
    mat_sca = mathutils.Matrix.Identity(4)
    mat_sca[0][0], mat_sca[1][1], mat_sca[2][2] = sca

    mat_out = mat_loc @ mat_rot @ mat_sca
    mat_h = mat_out.inverted() @ mat

    
    if meshObj.parent:
        meshObj.select_set(True)
        utils.activate(meshObj)
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

    for modObj in meshObj.modifiers:
        try:
            
            print("Blender 2.8x")
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modObj.name)
            print("Success for Blender 2.8x")
        except:
            
            try:
                print("Blender 2.9x")
                bpy.ops.object.modifier_apply(modifier=modObj.name)
                print("Success for Blender 2.9x")
            except:
                print("Internal Error 507 - Blender 2.9 alternative didn't work, this should not happen")
                popup("Internal Error 507, contact support with the contents of the console window", "Fatal Error", "ERROR")
                print("modifier error, removing:", modObj.name)
                meshObj.modifiers.remove(modObj)
        

    
    
    for v in meshObj.data.vertices:
        v.co = mat_h @ v.co

    if copy == False:
        utils.set_state(state)

    else:
        bpy.ops.object.transform_apply(scale=True, rotation=True, location=True)

    return meshObj






def normalize_weights(meshObj):

    if meshObj.type != 'MESH':
        print("Not a mesh")
        return False

    state = utils.get_state()

    
    
    obj = meshObj
    mesh_name = meshObj.name
    mesh = meshObj.data
    

    obj = bpy.context.active_object
    mesh = bpy.data.objects[obj.name].data
    mesh_name = bpy.data.objects[obj.name].data.name
    listbones = {}
    b=0

    
    for modifiers in bpy.data.objects[obj.name].modifiers:
        if modifiers.type == 'ARMATURE':
            data = bpy.data.objects[modifiers.object.name].data.name
            for bones in bpy.data.armatures[data].bones:
                listbones[bones.name] = b
                b+=1

    
    DictGroup = {} 

    i=0
    for group in bpy.context.active_object.vertex_groups:
        DictGroup[i]=group.name
        i+=1
                
    if bpy.context.mode == 'OBJECT':
        for vertex in bpy.data.meshes[mesh_name].vertices: 
            total_weight=0 
            space_left=1 
                    
            for group in vertex.groups: 
                if DictGroup[group.group] in listbones: 
                    if obj.vertex_groups[DictGroup[group.group]].lock_weight:
                        space_left-=group.weight
                    else:
                        total_weight+=group.weight
                else:
                    print("this is not a bone group " + str(DictGroup[group.group])) 
      
            for group in vertex.groups: 
                if DictGroup[group.group] in listbones: 
                    if not obj.vertex_groups[DictGroup[group.group]].lock_weight: 
                        this_weight = group.weight
                        if space_left > 0 and total_weight!=0:
                            new_weight = this_weight * (space_left/total_weight)
                        else:
                            new_weight = 0
                            
                        obj.vertex_groups[DictGroup[group.group]].add([vertex.index],new_weight,'REPLACE')
                        
    if bpy.context.mode == 'EDIT_MESH':
        print("")
        print("start")
        myVertex = {}
        v=0
        bpy.ops.object.mode_set(mode='OBJECT')
        for vertex in bpy.data.meshes[mesh_name].vertices:
            if vertex.select==True:
                myVertex[v]=vertex.index
                v+=1
        
        for each in myVertex:
            print(myVertex[each])
            total_weight=0 
            space_left=1 
            

            for group in mesh.vertices[myVertex[each]].groups: 
                print(group.weight)              
                if DictGroup[group.group] in listbones: 
                    print("this is a bone " + str(DictGroup[group.group]))

                    if obj.vertex_groups[DictGroup[group.group]].lock_weight:
                        space_left-=group.weight
                    else:
                        total_weight+=group.weight
                else:
                    print("this is not a bone group " + str(DictGroup[group.group])) 
       
            for group in mesh.vertices[myVertex[each]].groups: 
                if DictGroup[group.group] in listbones: 
                    if not obj.vertex_groups[DictGroup[group.group]].lock_weight: 
                        this_weight = group.weight
                        if space_left > 0 and total_weight!=0:
                            new_weight = this_weight * (space_left/total_weight)
                        else:
                            new_weight = 0
                            
                        obj.vertex_groups[DictGroup[group.group]].add([myVertex[each]],new_weight,'REPLACE')

    utils.set_state(state)

    return True








def refresh_weights(meshObj):

    if meshObj.type != 'MESH':
        print("Not a mesh")
        return False

    state = utils.get_state()

    groups = meshObj.vertex_groups
    
    names = {}
    indices = {}
    for g in groups:
        name = g.name
        index = g.index
        names[name] = index
        indices[index] = name

    
    vertices = meshObj.data.vertices
    weights = {}
    for v in vertices:
        weights[v.index] = {}
        for g in v.groups:
            
            
            
            
            index = g.group 
            weight = g.weight 
            group = groups[index] 
            name = group.name 
            
            weights[v.index][name] = weight

    
    del vertices
    del groups
    for g in meshObj.vertex_groups:
        meshObj.vertex_groups.remove(g)

    
    groups = [g for g in names]
    groups.reverse()
    for g in groups:
        meshObj.vertex_groups.new( name = g )

    
    groups_map = {}
    count = 0
    for g in meshObj.vertex_groups:
        groups_map[g.name] = count
        count += 1
    
    
    for v in weights:
        
        for name in weights[v]:
            
            g = meshObj.vertex_groups[name]
            
            weight = weights[v][name]
            
            g.add( [v], weight, 'REPLACE' )

    utils.set_state(state)

    return True






def get_armature(meshObj):
    armObj = False
    for modObj in meshObj.modifiers:
        if modObj.type == 'ARMATURE':
            armObj = modObj.object
            if utils.is_valid(armObj):
                return armObj
    return armObj




















def set_normalized_weights(meshObj, armature=None, skin=None, max_groups=4, precision=6):
        armObj = armature
        if meshObj.type != 'MESH':
            print("meshutils::restrict_weights : not a mesh", meshObj.name)
            return False

        if skin != None:
            skin_data = skin
        elif armature == None:
            armObj = get_armature(meshObj)
            if armObj == False:
                print("meshutils::restrict_weights : armature not provided or found for", meshObj.name)
                return False
            else:
                print("meshutils::restrict_weights : found armature", armObj.name, "for", meshObj.name)

        
        if skin == None:
            if armObj != None:
                if armObj.get('bb_collada_matrices') == None:
                    print("meshutils::restrict_weights : no collada data")
                    return False
                if armObj['bb_collada_matrices'].get('skin_data') == None:
                    print("meshutils::restrict_weights : no collada skin data")
                    return False
                skin_data = armObj['bb_collada_matrices']['skin_data']

        
        
        
        if armObj == None:
            print("meshutils::restrict_weights : none of the provided data returned an armature object, trying mesh as last resort.")
            armObj = get_armature(meshObj)
            if armObj == False:
                print("meshutils::restrict_weights : a last effort attempt to find an armature failed.")
                return False

        qualified_joints = set(skin_data)

        state = utils.get_state()

        for v in meshObj.data.vertices:
            weights = []
            for g in v.groups:
                bonename = meshObj.vertex_groups[g.group].name
                if bonename in qualified_joints:
                    if bonename not in armObj.data.bones:
                        print("Skipping group that is not a bone:", bonename)
                        continue
                    if armObj.data.bones[bonename].use_deform == False:
                        print("Skipping bone that is non deformable:", bonename)
                        continue
                    weights.append([g.weight, g.group])

            
            
            weights.sort(key=lambda x: x[0], reverse=True)

            
            weights = weights[:max_groups]

            
            tot = 0
            for w,g in weights:
                tot+=w
            if tot > 0:
                for wg in weights:
                    wg[0]=wg[0]/float(tot)

            final_groups = {}
            count = 0
            for g in v.groups:
                final_groups[g.group] = count
                count += 1

            
            for weight,group in weights:
                
                w = utils.normalize_float(weight, precision)
                
                i = final_groups[group]
                v.groups[i].weight = w

            
            good_weights = set()
            for w,g in weights:
                good_weights.add(g)

            
            delete = []
            for g in v.groups:
                if g.group not in good_weights:
                    delete.append(g.group)

            
            for i in delete:
                meshObj.vertex_groups[i].remove([v.index])

        utils.set_state(state)

        return








def popup(message = "", title = "Message Box", icon =  'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
    return



