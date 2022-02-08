

import os
import bpy
import math
import copy
import tempfile
import traceback
import mathutils
import xml.etree.ElementTree as ET
from . import utils
from . import collada
from . import globals 
from . import rigutils
from . import meshutils
from .presets import rig_data
from .presets import base_data
from .presets import real_rig_data
from .presets import skeleton as skel

if True:

    props = {}

    props['last_source'] = False

    default = {}
    
    defaults = {}
    defaults['defaults'] = {}
    defaults['avastar'] = {}
    defaults['onigiri'] = {}

    defaults_file = "defaults.dkp"
    
    files = {}
    
    files['defaults'] = "defaults.dkp"
    files['avastar'] = "defaults_avastar.dkp"
    files['onigiri'] = "defaults_onigiri.dkp"

    matrices = {}

    props['property'] = ""

    props['preset_name'] = ""

    props['master_text'] = ""
    props['master_icon'] = "dot_black"

def update_preset_source(report=False):
    armObj = utils.has_armature()
    preset = get_properties()
    
    if armObj == False:
        if report == False:
            print("No armature found, updating preset for defaults...")
        for prop in preset:
            
            default[prop] = preset[prop]
    else:
        if armObj.get('oni_devkit_preset') == None:
            if report == False:
                print("Associated armature contains no preset, applying...")
        else:
            if report == False:
                print("Armature preset updating...")
        armObj['oni_devkit_preset'] = {}
        for prop in preset:
            armObj['oni_devkit_preset'][prop] = preset

    return True
    
def get_properties(group=None):
    prop_group = group
    
    if group == None:
        prop_group = bpy.context.scene.oni_devkit
    presets = {}
    for prop in prop_group.__annotations__.keys():
        presets[prop] = getattr(prop_group, prop)

    return presets

def export_dae(matrices=None, joint='bone_data', file=None, real=None):
    
    testing = False
    
    print("Export matrix joint type is:", joint)

    obj = bpy.data.objects

    oni_devkit = bpy.context.scene.oni_devkit

    export_path_to_pelvis = oni_devkit.export_path_to_pelvis
    export_joints = oni_devkit.export_joints
    export_full_rig = oni_devkit.export_full_rig
    apply_location = oni_devkit.apply_location
    apply_rotation = oni_devkit.apply_rotation
    apply_scale = oni_devkit.apply_scale
    export_normalized_weights = oni_devkit.export_normalized_weights
    normalize_bones = oni_devkit.normalize_bones

    rotate_for_sl = oni_devkit.rotate_for_sl

    selected = bpy.context.selected_objects
    active = bpy.context.active_object

    selected_mesh = []
    for o in selected:
        if o.type == 'MESH':
            selected_mesh.append(o)
    
    mods = set()
    mesh = []
    for o in selected_mesh:
        arms = set()
        for m in o.modifiers:
            if m.type == 'ARMATURE':
                arms.add(m)
        if len(arms) > 1:
            print("INIT: A mesh with too many armature modifiers is present, skipping", o.name)
        elif len(arms) == 0:
            print("INIT: A mesh with no armature modifiers is present, skipping", o.name)
        else:
            print("INIT: Found qualified mesh", o.name)
            mesh.append(o)

    if len(mesh) == 0:
        print("There were no exportable mesh in your selection")
        return False
    
    arm_objects = set()
    for o in mesh:
        for m in o.modifiers:
            if m.type == 'ARMATURE':
                target = m.object
                arm_objects.add(target)
    if len(arm_objects) > 1:
        print("There's too many armatures associated with the various selected mesh, there can only be one")
        return False
    if len(arm_objects) == 0:
        print("There's no qualified armatures associated with your selected mesh")
        return False
    
    armObj = list(arm_objects)[0]
    print("Got armature for exportable mesh", armObj.name)

    print("devkit::export_dae - run make_single on armature", armObj.name)
    utils.make_single(armObj)

    state = utils.get_state()

    armObj.select_set(True)

    for o in mesh:
        o.select_set(True)
        utils.activate(o)
        utils.make_single(o)

    utils.activate(o)

    if matrices == None:
        print("No bone definitions were available, this is a bug")
        utils.popup("Missing bone definitions, this is a bug in devkit.export_dae()")
        return

    if export_normalized_weights == True:
        for o in mesh:
            print("Pruning weights for", o.name)
            skin_data = matrices.get('skin_data', None)
            if skin_data != None:
                print("devkit::export_dae : found skin data in matrices")
            
            meshutils.set_normalized_weights(o, skin=skin_data)

    if normalize_bones == True:
        print("devkit::export_dae : Normalizing scale...")
        for bone_type in matrices:
            
            if bone_type == 'skin_data' or bone_type == 'bind_shape':
                continue

            for bone in matrices[bone_type]:

                if isinstance(bone, str):
                    print("getting matrix for bone:", bone)
                else:
                    print("bone is not a string:")
                    for b in bone:
                        print(":", b, ":", sep="")

                if bone not in skel.avatar_skeleton:
                    continue
                if skel.avatar_skeleton[bone]['type'] == 'bone':
                        mat = mathutils.Matrix(matrices[bone_type][bone])
                        if bone_type == "bind_data":
                            mat = mat.inverted()
                        l,r,s = mat.decompose()
                        L = mathutils.Matrix.Translation(l)
                        R = r.to_matrix().to_4x4()
                        S = mathutils.Matrix()
                        for i in range(3):
                            S[i][i] = 1
                        M = L @ R @ S
                        if bone_type == "bind_data":
                            M = M.inverted()
                        matrices[bone_type][bone] = M

    bind_pose = {}
    joint_pose = {}
    for bone in matrices['bind_data'].keys():
        underscored = bone.replace(" ", "_")
        bind_pose[underscored] = matrices['bind_data'][bone]
    for bone in matrices[joint].keys():
        underscored = bone.replace(" ", "_")
        joint_pose[underscored] = matrices[joint][bone]

    print("devkit::export_dae - Applying transforms as indicated.  This is destructive, the items should be origin to rig not all to origin")
    print("The following transforms are set:")
    print(" - Apply scale   :", apply_scale)
    print(" - Apply rotation:", apply_rotation)
    print(" - Apply location:", apply_location)

    bpy.ops.object.transform_apply(scale=apply_scale, rotation=apply_rotation, location=apply_location)
    print("devkit::export_dae - apply transforms finished!")
    if 1 == 0:
        active = bpy.context.active_object
        for o in bpy.context.selected_objects:
            utils.activate(o)
            print("applying transforms to", o.name, "of type", o.type)
            
            bpy.ops.object.transform_apply(scale=apply_scale, rotation=apply_rotation, location=apply_location)
        utils.activate(active)

    if oni_devkit.remove_empty_groups == True:
        print("devkit::export_dae - remove empty groups indicated")
        bpy.ops.onigiri.remove_unused_groups(method="best")

    file_path = tempfile.gettempdir() + "/onigiri_" + utils.get_temp_name() + ".dae"
    
    if testing == True:
        directory = os.path.split(file)[0]
        file_path = directory + "/onigiri_phase_one_export" + ".dae"
        print("Testing mode, file written will be {", file_path, "] and will not be deleted", sep="")

    if rotate_for_sl == True:
        global_forward = '-X'
    else:
        global_forward = 'Y'

    print("bone deform sanity check...")
    use_deform_only = False
    old_deform = {} 
    if use_deform_only == True:
        for boneObj in armObj.data.bones:
            if boneObj.name not in bind_pose or boneObj.name not in joint_pose:
                old_deform[boneObj.name] = boneObj.use_deform
                boneObj.use_deform = False

    for o in bpy.context.selected_objects:
        if "&" in o.name:
            o['name'] = o.name
            o['oni_xml_fix'] = True
            name = o.name.replace("&", "_")
            o.name = name
    if "&" in armObj.name:
        armObj['name'] = armObj.name
        name = armObj.name.replace("&", "_")
        armObj.name = name
        armObj['oni_xml_fix'] = True

    print("devkit::export_dae - Exporting initial collada before processing...")

    sort_by_name = True
    open_sim = True
    triangulate = False
    use_object_instantiation = False
    use_blender_profile = False

    bpy.ops.wm.collada_export(
        filepath = file_path,
        check_existing = False,
        apply_modifiers = oni_devkit.dae_apply_modifiers,
        export_mesh_type_selection='render',
        selected = True,
        include_children = False,
        include_armatures = True,
        include_shapekeys = False,
        include_animations = False,
        deform_bones_only = True,
        triangulate = triangulate,
        use_object_instantiation = use_object_instantiation,
        use_blender_profile = use_blender_profile,
        sort_by_name = sort_by_name,
        open_sim = open_sim,
        export_object_transformation_type_selection = 'matrix',
        export_global_forward_selection=global_forward,
        export_global_up_selection='Z',
        apply_global_orientation=rotate_for_sl,
        )
    print("devkit::export_dae - collada export complete!")

    for o in bpy.context.selected_objects:
        if o.get('oni_xml_fix'):
            name = o['name']
            o.name = name
            o.pop('oni_xml_fix')
            o.pop('name')
    if armObj.get('oni_xml_fix') == True:
        name = armObj['name']
        armObj.name = name
        armObj.pop('oni_xml_fix')
        armObj.pop('name')

    print("devkit::export_dae - Restoring deform bones...")
    for bone in old_deform:
        armObj.data.bones[bone].use_deform = old_deform[bone]
    print("devkit::export_dae - restore complete!")

    file_in = file_path
    file_out = file 

    ET.register_namespace('',globals.collada['URI'])

    tree = ET.parse(file_in)

    root = tree.getroot()
    n = globals.collada['namespace']

    for node in root.iter(f'{n}contributor'):
        creator = node.find(f'{n}author')
        version = node.find(f'{n}authoring_tool')
    print("creator:", creator.text)
    print("version:", version.text)
    creator.text = "Onigiri User"
    version.text = "Onigiri Kit Converter v2.2"

    controller = {}
    skin = {}
    names = list()
    joints = {}
    lc = root.find(f'{n}library_controllers')
    for c in lc:
        cid = c.get('id')
        name = c.get('name')
        controller[cid] = name
        skin = c.find(f'{n}skin')

        for skin_child in skin:
            
            joint_total = 0
            float_total = 0

            for data in skin_child:
                if data.tag == n + "Name_array":

                    Name_array = data

                    if data.text == None:
                        print("devkit::dae_export : the recycled dae file contained no joints, nothing to do")
                        utils.popup("There were no joints available for processing, see console for details", "Error", "ERROR")
                        return False

                    names = data.text.split()

                    print("devkit::dae_export : WARNING...")
                    print("  * Joint reduction will damage vertex order which causes weight data to be incorrect!")
                    print("  * This one has [", len(names), "] in the bind pose matrix before cleaning.", sep="")
                    print("  * Appending joints to the bind data is not problematic, you may wish to leave them out of accessor.")

                    print("----------------------------------------------")
                    print("             SEE HERE BROWN DEER")
                    print("----------------------------------------------")
                    print("names:", names)
                    print("len(names):", len(names))
                    print("----------------------------------------------")
                    print("")
                    print("----------------------------------------------")

                    Name_array_accessor_count = skin_child.find(f'{n}technique_common/{n}accessor')

            for data in skin_child:
                if data.tag == n + "float_array":

                    param = skin_child.find(f'{n}technique_common/{n}accessor/{n}param')

                    if param.get('type') == "float4x4":

                        float_array = data

                        float_array_accessor_count = skin_child.find(f'{n}technique_common/{n}accessor')

                        matrices = list()

                        if export_full_rig == True:
                            
                            export_path_to_pelvis = False
                            
                            name_set = set(names) 

                            all_bones = [b for b in skel.avatar_skeleton]
                            
                            for bone in all_bones:
                                
                                bone_ = bone.replace(" ", "_")

                                if bone_ not in name_set:
                                    joint_type = skel.avatar_skeleton[bone]['type']

                                    names.append(bone_)

                        if export_path_to_pelvis == True:
                            bone_path = set()
                            names_set = set(names)
                            
                            bad_bones = []

                            for bone in names:

                                if 1 == 1:
                                    if bone not in skel.avatar_skeleton:
                                        bad_bones.append(bone)
                                        print("Skipping unknown bone, but this will be processed in joints anyway:", bone)
                                        continue

                                parent = ""
                                next_bone = bone
                                while(True):
                                    parent = skel.avatar_skeleton[next_bone]['parent']
                                    if parent != "":
                                        
                                        if parent not in names_set:
                                            if parent not in bone_path:
                                                bone_path.add(parent)

                                        next_bone = parent

                                    else:
                                        break

                            if len(bad_bones):
                                print("Some bones marked as deformable are suspected of having a party, have a look.")
                                print(bad_bones)
                                
                            for bone in bone_path:
                                if bone not in names_set:
                                    names.append(bone)
                            
                        if export_joints == True:
                            print("devkit::export_dae reports - export_joints is enabled")

                            if real == None:
                                print("devkit::export_dae reports - no real rig, using current for path trace")
                                realRig = armObj
                            else:
                                realRig = real

                            rename_map = realRig.get('oni_onemap_rename')

                            if rename_map:
                                print("devkit::export_dae reports - found a rename_map")

                            names_set = set(names)
                            for boneObj in realRig.data.bones:
                                bone = boneObj.name
                                sl_bone = bone
                                if rename_map:
                                    if bone not in rename_map:
                                        print("devkit::export_dae reports - can't path missing bone from rename map during (export_joints):", bone)
                                        continue
                                    sl_bone = rename_map[bone]
                                if sl_bone in names_set:
                                    print("Skipping name in name_set:", sl_bone)
                                    continue
                                if boneObj.get('oni_joint_export') == None:
                                    continue
                                
                                bone_path = rigutils.get_bone_path(armObj, sl_bone)
                                print("devkit::export_dae reports - bone_path =", bone_path)
                                print("devkit::export_dae reports - trigger bone:", bone, "AKA", sl_bone)
                                names.append(sl_bone)
                                names_set.add(sl_bone)
                                
                                for bone in bone_path:
                                    if bone in names_set:
                                        continue
                                    names.append(bone)
                                    names_set.add(bone) 
                        
                        qualified_joints = []
                        for i in range(len(names)):
                            text_mat = list()
                            bone = names[i]
                            
                            if bone not in bind_pose: 
                                
                                print("==========================================================")
                                print("devkit::dae_export : missing bind_pose bone:", bone)
                                print("  -")
                                print("  * kludging in missing data, this should be done before running this function.")
                                print("  * Try adding this fix to collada:get_matrices() instead or the other matrix")
                                print("  * data filling tools that are called before this function.")
                                print("  -")
                                print("==========================================================")
                                print("-")
                                continue
                            
                            mat = mathutils.Matrix(bind_pose[bone])

                            joint_total += 1
                            
                            qualified_joints.append(bone)

                            for m in mat:
                                
                                float_total += 4
                                shorten = [round(a, 6) for a in m]
                                t = [str(a) for a in shorten]
                                text_mat.append("\n")
                                text_mat.append(" ".join(t))
                            matrices.extend(text_mat)

                            matrices.append("\n")

                        print("--------------------------------------")
                        print("devkit::export_dae : qualified_joints:", qualified_joints)
                        if len(qualified_joints) == 0:
                            print("devkit::export_dae : there were no joints left to process after sanity checks")
                            print("--------------------------------------")
                            return False
                        print("--------------------------------------")

                        Name_array.text = " ".join(qualified_joints)

                        Name_array_accessor_count.set('count', str(len(qualified_joints)))
                        Name_array.set('count', str(len(qualified_joints)))
                        float_array.set('count', str(float_total))
                        float_array_accessor_count.set('count', str(len(qualified_joints)))

                        data.text = "".join(matrices)

                        del matrices
                        del names

    if 1 == 0:
        missing_joints = []
        for node in root.iter(f'{n}node'):
            if node.get('type') == "JOINT":
                matrix = node.find(f'{n}matrix')
                if node.attrib.get('name') != None:
                    bone = node.attrib['name']
                    if bone in joint_pose:
                        tmat = matrix_to_text(joint_pose[bone])
                        matrix.text = " ".join(tmat)
                    else:
                        missing_joints.append(bone)
                        print(":library_visual_scene - missing bone, this should never happen", bone)

        if len(missing_joints) > 0:
            print("write_nodes:",
                "Some joints have no associated data.")
            for bone in missing_joints:
                print("  -", bone)

    else:
        
        lvs = root.find(f'{n}library_visual_scenes')
        
        visual_scene_new = lvs.find(f'{n}visual_scene')
        visual_scene_old = copy.deepcopy(visual_scene_new)

        print("removing old node branch")
        
        lvs = root.find(f'{n}library_visual_scenes')
        scene = lvs.find(f'{n}visual_scene')
        for node in scene.findall(f'{n}node'):
            scene.remove(node)

        if 1 == 0:
            
            mt  = "1 0 0 0 "
            mt += "0 1 0 0 "
            mt += "0 0 1 0 "
            mt += "0 0 0 1"
            for cid in controller:
                
                id = cid.split("-")[0]
                cnode = ET.SubElement(scene, "node")
                cnode.set("id", id)
                cnode.set("name", id)
                cnode.set("type", 'NODE')
                mnode = ET.SubElement(cnode, "matrix")
                mnode.text = mt
                ic = ET.SubElement(cnode, "instance_controller")
                ic.set("url", '#' + cid)
                sk = ET.SubElement(ic, "skeleton")
                sk.text = '#mPelvis'

        ele = {} 
        print("Building joint data...")
        for bone in skel.avatar_skeleton:

            if 1 == 0:
                if " " in bone:
                    print("skipping incompatible attachment bone:", bone)
                    continue

            parent = skel.avatar_skeleton[bone]['parent']

            bone = bone.replace(" ", "_")

            if parent == "":
                node = ET.SubElement(scene, "node")
                ele[bone] = node
            
            else:

                p_node = ele[parent]
                node = ET.SubElement(p_node, "node")
                ele[bone] = node
            node.set("id", bone)
            node.set("name", bone)
            node.set("sid", bone)
            node.set("type", 'JOINT')
            matrix_node = ET.SubElement(node, "matrix")

            mat = mathutils.Matrix(joint_pose[bone])
            mt = matrix_to_string(mat)
            matrix_node.text = mt

            matrix_node.set("sid", 'transform')

        lvs = root.find(f'{n}library_visual_scenes')
        vs = lvs.find(f'{n}visual_scene')
        
        base = visual_scene_old.find(f'{n}node')
        print("============== NODES 1 =============")
        for node in base:
            if node.find(f'{n}instance_controller'):
                print("found instance controller, appending")
                node_type = node.get('TYPE')
                node_name = node.get('name')
                node_id = node.get('id')
                print("node_type:", node_type)
                print("node_name:", node_name)
                print("node_id  :", node_id)
                
                skeleton_node = node.find(f'{n}instance_controller/{n}skeleton')
                if skeleton_node == None:
                    print("No skeleton found under instance_controller, this could be a bug in", node_name)
                else:
                    print("Altering skeleton referencd from", skeleton_node.text, "to", "#mPelvis")
                    skeleton_node.text = '#mPelvis'
                vs.append(node)
        print("====================================")

        if 1 == 0:
            mt  = "1 0 0 0 "
            mt += "0 1 0 0 "
            mt += "0 0 1 0 "
            mt += "0 0 0 1"
            for cid in controller:
                
                id = cid.split("-")[0]
                cnode = ET.SubElement(scene, "node")
                cnode.set("id", id)
                cnode.set("name", id)
                cnode.set("type", 'NODE')
                mnode = ET.SubElement(cnode, "matrix")
                mnode.text = mt
                ic = ET.SubElement(cnode, "instance_controller")
                ic.set("url", '#' + cid)
                sk = ET.SubElement(ic, "skeleton")

                sk.text = '#mPelvis'

    tree.write(file_out,
        xml_declaration = True,
        encoding = 'utf-8',
        method = 'xml'
        )

    try:
        if testing == False:
            os.remove(file_path)
            print("ONI dae cleanup")
        else:
            print("Testing phase, file [", file_path, "] was not removed", sep="")
    except:
        print("ONI Warning: unable to remove temporary file:", file_path)

    pretty_dae(file_in=file_out, file_out=file_out)

    utils.set_state(state)

    return True

def pretty_dae(file_in=None, file_out=None):
    ET.register_namespace('', globals.collada['URI'])
    n = globals.collada['namespace']
    tree = ET.parse(file_in)
    root = tree.getroot()
    controller = {}
    skin = {}
    names = list()
    joints = {}
    matrices = list()
    lc = root.find(f'{n}library_controllers')
    for c in lc:
        cid = c.get('id')
        name = c.get('name')
        controller[cid] = name
        skin = c.find(f'{n}skin')
        for skin_child in skin:
            for data in skin_child:
                if data.tag == n + "Name_array":
                    names = data.text.split()
                if data.tag == n + "float_array":
                    
                    param = skin_child.find(f'{n}technique_common/{n}accessor/{n}param')
                    
                    if param.get('type') == "float4x4":
                        
                        matrices = data.text.split()
                        mat_out = list()
                        block = 0
                        for i in range(len(names)):
                            mat = matrices[block:block+16]
                            block += 16
                            v = list()
                            for t in range(0, 16, 4):
                                v.append("\n")
                                v.extend(mat[t:t+4])
                            mat_out.extend(v)
                            mat_out.append("\n")
                        data.text = " ".join(mat_out)
    for node in root.iter(f'{n}node'):
        if node.get('type') == "JOINT":
            matrix = node.find(f'{n}matrix')
            if node.attrib.get('name') != None:
                bone = node.attrib['name']
                
                tmat = matrix.text.split()
                t = list()
                for r in range(0, 16, 4):
                    t.append("\n")
                    v = tmat[r:r+4]  
                    
                    for tfl in v:  
                        rfl = round(float(tfl), 6)
                        t.append( f"{rfl:.6f}")
                        t.append(" ")
                t.append("\n")
                matrix.text = " ".join(t)

    tree.write(file_out,
        xml_declaration = True,
        encoding = 'utf-8',
        method = 'xml'
        )
    print("Collada prettified and written:", file_out)
    return

def pretty_nodes(root=None):
    print("Generating pretty nodes")
    n = globals.collada['namespace']
    for node in root.iter(f'{n}node'):
        if node.get('type') == "JOINT":
            matrix = node.find(f'{n}matrix')
            if node.attrib.get('name') != None:
                bone = node.attrib['name']
                
                tmat = matrix.text.split()
                t = list()
                for r in range(0, 16, 4):
                    t.append("\n")
                    v = tmat[r:r+4]  
                    for tfl in v:  
                        rfl = round(float(tfl), 6)
                        t.append( f"{rfl:.6f}")
                        t.append(" ")
                t.append("\n")
                matrix.text = " ".join(t)

    return root 

def matrix_to_text(mat):
    tmat = list()
    for v in mat:
        for n in v:
            tmat.append(f"{n:.6f}")
    return tmat

def matrix_to_string(mat):
    tmat = list()
    for v in mat:
        for n in v:
            tmat.append(f"{n:.6f}")
    txt = " ".join(tmat)
    return txt

def matrix_from_list(l):
    M = mathutils.Matrix()
    for c in range(4):
        for r in range(4):
            M[c][r] = l[ r + (c*4) ]
    return M

def has_devkit_armature(object=None):
    obj = bpy.data.objects
    
    if object != None:
        if isinstance(object, str):
            OBJ = obj[object]
        else:
            OBJ = object
        if OBJ.type == 'ARMATURE':
            if OBJ.get('oni_devkit_presets') != None:
                print("found devkit armature", OBJ.name)
                return OBJ 
            else:
                return False
        match = []
        for M in OBJ.modifiers:
            if M.type == 'ARMATURE':
                match.append(M)
        if len(match) == 1:
            armObj = M.object
            if utils.is_valid(armObj):
                if armObj.get('oni_devkit_presets') != None:
                    print("found armature:", armObj.name)
                    return armObj
                else:
                    return False
            else:
                print("devkit::get_devkit_armature reports : The armature that the single armature modifier points to is invalid")
                return False
        
        txt = ""
        if len(match) > 1:
            txt = "too many armature modifiers"
        if len(match) == 0:
            txt = "no armature modifiers"
        print("devkit::get_devkit_armature reports :", txt)
        return False

    selected = bpy.context.selected_objects
    if len(selected) == 0:
        print("devkit::get_devkit_armature reports: no argument and no selection, nothing to do")
        return False

    mesh = []
    arms = []
    for o in selected:
        if o.type == 'MESH':
            mesh.append(o)
        elif o.type == 'ARMATURE':
            arms.append(o)

    if len(mesh) == 0 and len(arms) > 1:
        print("devkit::get_devkit_armature reports : no mesh selected and too many armatures, expected 1 armature or 1 or more mesh and/or armature with it")
        return False

    if len(mesh) == 0 and len(arms) == 1:
        
        armObj = arms[0]
        if armObj.get('oni_devkit_presets') != None:
            print("devkit::get_devkit_armature reports : Found devkit armature on the single selected armature:", armObj.name)
            return armObj
        else:
            return False

    if len(mesh) == 0:
        print("devkit::get_devkit_armature reports : after running excessive tests on the selected objects no qualified mesh or armatures were found")
        return False

    mods = set() 
    objs = set() 
    for o in mesh:
        mesh_mods = []
        for m in o.modifiers:
            if m.type == 'ARMATURE':
                mesh_mods.append(m)
        if len(mesh_mods) == 0:
            print("No qualified modifiers on", o.name)
        else:
            print("Found qualified modifiers on", o.name)
            if len(mesh_mods) > 1:
                print("Too many armature modifiers on", o.name)
            else:
                if mesh_mods[0].object == None:
                    print("Modifier points to nothing", o.name)
                else:
                    if utils.is_valid(mesh_mods[0].object):
                        print("found valid armature modifier on", o.name)
                        objs.add(mesh_mods[0].object)

    if len(objs) > 1:
        print("devkit::get_devkit_armature reports : too many directions, the target objects for qualified mesh with qualified armatures is greater than 1")
        return False
    if len(objs) == 0:
       print("devkit::get_devkit_armature reports : no qualified armatures armatures were found on the selected mesh")
       return False

    return list(objs)[0]

def save_default_presets(path):

    import pprint

    oni_devkit = bpy.context.scene.oni_devkit
    presets_backup = {}
    for prop in oni_devkit.keys():
        presets_backup[prop] = getattr(oni_devkit, prop)
        oni_splice.property_unset(prop)
    presets = {}
    for prop in oni_devkit.keys():
        presets[prop] = oni_devkit[prop]
    for prop in presets_backup:
        oni_devkit[prop] = presets_backup[prop]

    f = open(path, "w", encoding='UTF8')
    f.write(formatted)
    f.close()
    return True

def set_defaults(all=True, area="devkit"):

    oni_devkit = bpy.context.scene.oni_devkit

    presets = {}
    properties = set()
    for prop in oni_devkit.__annotations__.keys():
        properties.add(prop)

    if all == True:
        for prop in properties:
            oni_devkit.property_unset(prop)
    else:
        
        reset_props = set()
        if area == "devkit":
            for prop in properties:
                
                if prop.startswith("dae_"):
                    continue
                reset_props.add(prop)
        elif area == "dae":
            for prop in properties:
                if prop.startswith("dae_"):
                    oni_devkit.property_unset(prop)
        else:
            print("all is False but the area doesn't match anything")
            return False

        for prop in reset_props:
            try:
                oni_devkit.property_unset(prop)
            except:
                print("Couldn't reset", prop)

    return True

def load_defaults(file=None, extend=False, report=False):
    print("devkit::load_defaults runs")
    from . import oni_settings
    script_dir = os.path.dirname(os.path.abspath(__file__))
    devkit_path = oni_settings['paths']['devkit']

    if file != None:
        file_name = files[file]
    else:
        file_name = defaults_file

    print("loading devkit presets from", file_name)

    file_path = script_dir + "/" + devkit_path + "/" + file_name
    presets = {}
    try:
        namespace = {}
        exec(open(file_path, 'r', encoding='UTF8').read(), namespace)
        if "devkit_presets" in namespace:
            if report == True:
                print("Found devkit_presets")
            name = "devkit_presets"
        elif "presets" in namespace:
            if report == True:
                print("Found presets")
            name = "presets"
        else:
            if report == True:
                print("No presest")
            return {}

        presets = namespace[name]

    except Exception as e:
        print(traceback.format_exc())
        if report == True:
            print("Error loading default presets, your installation is damaged!")

        if extend == True:
            if report == True:
                print("Error loading default presets, generating from current...")
            oni_devkit = bpy.context.scene.oni_devkit
            properties = set()
            for prop in oni_devkit.__annotations__.keys():
                properties.add(prop)
            for prop in properties:
                presets[prop] = getattr(oni_devkit, prop)

    if report == True:
        print("devkit::load_defaults : defaults loaded")

    return presets

if True:

    pass

def get_matrices(armature=None, use_bind_pose=False, rotate=True, base=None, report=False):

    print("rotate =", rotate)
    R90 = mathutils.Matrix.Rotation(math.radians(0.0), 4, 'Z')
    if rotate == True:
        R90 = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Z')
    R90I = R90.inverted()
    
    dae = {}
    dae['bind_data'] = {}
    dae['bone_data'] = {}
    
    dae['real_data'] = {}

    base_rig = base_data.female_neutral
    for bone in base_rig:
        dmg = mathutils.Matrix(base_rig[bone]['matrix_local'])
        matI = dmg.inverted()
        matI = matI @ dmg.inverted()
        l = matI.to_translation()
        L = mathutils.Matrix.Translation(l)
        dmg = dmg @ L
        dmgI = mathutils.Matrix(base_rig[bone]['matrix_local']) @ dmg.inverted()
        dmgI = dmgI @ R90I
        dmgI = R90 @ dmgI
        l_ofs, r_ofs, s_ofs = dmgI.decompose()
        l = mathutils.Matrix(base_rig[bone]['matrix_local']).to_translation()
        L = mathutils.Matrix.Translation(l)
        R = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Z')
        RI = R.inverted()
        L = R @ L
        l = L.to_translation()
        L = mathutils.Matrix.Translation(l)
        r = skel.avatar_skeleton[bone]['rot']
        rot = [math.radians(a) for a in r]
        R_mat = mathutils.Euler(rot,'XYZ').to_matrix().to_4x4()
        R_ofs = r_ofs.to_matrix().to_4x4()
        R = R_mat
        R = R_mat @ R_ofs
        s = [ a for a in skel.avatar_skeleton[bone]['scale'] ]
        S = mathutils.Matrix()
        for i in range(3):
            S[i][i] = s[i]
        M = L @ R @ S
        dae['bind_data'][bone] = M.inverted()
    for bone in dae['bind_data']:
        matbcI = dae['bind_data'][bone]
        matbc = matbcI.inverted()
        parent = skel.avatar_skeleton[bone]['parent']
        if bone == "mPelvis":
            dae['bone_data'][bone] = matbc
            dae['real_data'][bone] = matbc
        else:
            matbpI = dae['bind_data'][parent]
            matjc = matbpI @ matbc
            dae['bone_data'][bone] = matjc
            dae['real_data'][bone] = matjc

    armObj = armature
    if armObj == None:
        
        print("devkit::get_matrices : no armature, returning bind and joint data for base only")
        return dae

    if isinstance(armature, str):
        armObj = bpy.data.objects[armature]

    is_avaclown = False
    if armObj.get('avastar') != None:
        is_avaclown = True

    if armObj.get('avastar_converted') != None:
        is_avaclown = False

    bone_names = {}
    if is_avaclown:
        bone_names = rigutils.normalize(armObj)
    
    else:
        for boneObj in armObj.data.bones:
            bone = boneObj.name
            bone_names[bone] = bone

    bone_rev = {}
    for sbone in bone_names:
        tbone = bone_names[sbone]
        
        if tbone in bone_rev:
            print("bone_rev name collision:", tbone)
        bone_rev[tbone] = sbone

    print("devkit::get_matrices : base =", base)
    if base == None:
        base_rig = getattr(base_data, "female_neutral")
    else:
        base_rig = getattr(base_data, base)

    base_matrices = {}
    for bone in base_rig:
        mb = mathutils.Matrix(base_rig[bone]['matrix_local'])
        base_matrices[bone] = mb

    if base == None:
        for bone in skel.avatar_skeleton:
            if bone not in bone_rev:
                continue
            tbone = bone_rev[bone]
            mb = armObj.data.bones[tbone].matrix_local.copy()
            base_matrices[bone] = mb

    matrices = {}
    for bone in skel.avatar_skeleton:
        if bone not in bone_rev:
            ml = base_matrices[bone]
        else:
            sbone = bone_rev[bone]
            ml = armObj.data.bones[sbone].matrix_local.copy()
        matrices[bone] = ml

    if 1 == 0:
        for bone in skel.avatar_skeleton:
            
            if bone.startswith("mSpine"):
                if report == True:
                    print("Found spine:", bone)
                bone_dup = globals.spine_chain[bone]
                if bone_dup not in bone_rev:
                    ml = base_matrices[bone_dup]
                    matrices[bone] = ml
                    if report == True:
                        print("Not in bone_rev, replacing", bone, "with", bone_dup, "matrix")
                        print(ml)
                else:
                    ml = matrices[bone_dup]
                    matrices[bone] = ml
                    if report == True:
                        print("Bone appears to be recorded already, replacing", bone, "with", bone_dup, "matrix")
                        print(ml)
    
    for bone in matrices:
        
        if bone not in bone_rev:
            continue
        
        sbone = bone_rev[bone]
        boneObj = armObj.data.bones[sbone]

        dmg = base_matrices[bone]

        matI = dmg.inverted()
        matI = matI @ dmg.inverted()

        l = matI.to_translation()
        L = mathutils.Matrix.Translation(l)
        dmg = dmg @ L

        dmgI = matrices[bone] @ dmg.inverted()

        dmgI = dmgI @ R90I
        dmgI = R90 @ dmgI

        l_ofs, r_ofs, s_ofs = dmgI.decompose()

        use_offset_location = True
        if use_offset_location == True:
            l = matrices[bone].to_translation()
        else:
            l = base_matrices[bone].to_translation()

        L = mathutils.Matrix.Translation(l)

        R = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Z')
        RI = R.inverted()
        L = R @ L

        l = L.to_translation()
        L = mathutils.Matrix.Translation(l)

        r = skel.avatar_skeleton[bone]['rot']
        rot = [math.radians(a) for a in r] 
        R_mat = mathutils.Euler(rot,'XYZ').to_matrix().to_4x4()

        R_ofs = r_ofs.to_matrix().to_4x4()
        R = R_mat 
        
        if use_bind_pose:
            R = R_mat @ R_ofs 
        
        if is_avaclown:
            S = utils.get_stored_scale(boneObj)
            
            if skel.avatar_skeleton[bone]['type'] == 'collision':

                S = utils.get_stored_scale(boneObj.parent, S)
        else:
            
            s = [ a for a in skel.avatar_skeleton[bone]['scale'] ]
            S = mathutils.Matrix()
            for i in range(3):
                S[i][i] = s[i]

        M = L @ R @ S

        dae['bind_data'][bone] = M.inverted()

    for bone in dae['bind_data']:
        matbcI = dae['bind_data'][bone]
        matbc = matbcI.inverted()
        parent = skel.avatar_skeleton[bone]['parent']
        
        if bone == "mPelvis":
            dae['bone_data'][bone] = matbc
            
            dae['real_data'][bone] = matbc
        else:
            matbpI = dae['bind_data'][parent]
            matjc = matbpI @ matbc
            dae['bone_data'][bone] = matjc
            
            dae['real_data'][bone] = matjc

    return dae

    for bone in skel.avatar_skeleton:
        
        if bone.startswith("mSpine"):
            bone_dup = globals.spine_chain[bone]
            if bone_dup not in dae['bone_data']:
                if report == True:
                    print("Spine bone", bone_dup, "not in dae joints, skipping")
                continue
            ml = dae['bone_data'][bone_dup]
            dae['bone_data'][bone] = ml
            dae['real_data'][bone] = ml

    return dae

def get_bind_info(arm):
    armObj = arm
    if isinstance(arm, str):
        armObj = bpy.data.objects[arm]

    dae_mats = get_matrices(armObj)

    matrices = {}
    matrices['bind_data'] = {}
    matrices['bone_data'] = {}
    matrices['real_data'] = {}

    for boneObj in armObj.data.bones:
        bone = boneObj.name
        bm = boneObj.get('bind_mat')
        jm = boneObj.get('rest_mat')
        if bm:
            mf = utils.bind_to_matrix(bm)
            matrices['bind_data'][bone] = mf.inverted()
        if jm:
            mf = utils.bind_to_matrix(jm)
            matrices['bone_data'][bone] = mf
            matrices['real_data'][bone] = mf

    if len(matrices['bind_data']) == 0:
        print("devkit::get_bind_info : No stored bind info available")
        return False

    print("Sanity check for bind/bone data, if there are errors you may have unusable bind info on the rig.")
    for bone in matrices['bone_data']:
        if bone not in matrices['bind_data']:
            print("A bone identified in bone_data is missing from bind_data:", bone)
    for bone in matrices['bind_data']:
        if bone not in matrices['bone_data']:
            print("A bone identified in bind_data is missing from bone_data:", bone)

    print("Depositing empty matrices for bone_data...")
    bone_data_count = 0
    for bone in dae_mats['bone_data']:
        if bone not in matrices['bone_data']:
            bone_data_count += 1
            matrices['bone_data'][bone] = dae_mats['bone_data'][bone]
            matrices['real_data'][bone] = dae_mats['real_data'][bone]
    print("Depositing empty matrices for bind_data...")
    bind_data_count = 0
    for bone in dae_mats['bind_data']:
        if bone not in matrices['bind_data']:
            bind_data_count += 1
            matrices['bind_data'][bone] = dae_mats['bind_data'][bone]

    print("Filled missing bone data for", bone_data_count, "joints")
    print("Filled missing bind data for", bind_data_count, "joints")

    for cbone in matrices['bind_data']:
        cmatb = matrices['bind_data'][cbone]
        
        if cbone not in armObj.data.bones:
            continue
        boneObj = armObj.data.bones[cbone]
        
        if cbone != "mPelvis":
            if boneObj.parent:
                pbone = boneObj.parent.name
                if pbone not in matrices['bind_data']:
                    print("Skipping unknown parent", pbone, "for bone", cbone, "in armature", armObj.name)
                    continue
                pmatb = matrices['bind_data'][pbone]
        else:
            pmatb = mathutils.Matrix()
        jmat = pmatb @ cmatb
        matrices['real_data'][bone] = jmat

    return matrices

def reshape(armObj, matrices=None, bone_type="bind_data", rotate=False, copy=False, delete=False, report=True):
    if isinstance(armObj, str):
        armObj = bpy.data.objects[armObj]

    if armObj.type != 'ARMATURE':
        print("devkit::reshape reports : not an armature")
        return False
    
    if matrices == None:
        print("devkit::reshape reports : no matrices offered")
        transforms = armObj.get('oni_collada_matrices')
        if transforms == None:
            print("devkit::reshape reports : no matrices on the armature object")
            return False
        matrices = {}
        for bone in transforms[bone_type]:
            mat = mathutils.Matrix(transforms[bone_type][bone]).inverted()
            matrices[bone] = mat

    mesh = rigutils.get_associated_mesh(armObj, report=True)
    if mesh == False:
        print("devkit::reshape reports : the function rigutils::get_associated_mesh returned False")
        return False

    state = utils.get_state()

    qualified = []
    if copy == True:
        for meshObj in mesh:
            meshObj.select_set(True)
        armObj.select_set(True)
        utils.activate(armObj)
        bpy.ops.object.duplicate()
        qualified = [o for o in bpy.context.selected_objects]
        if delete == True:
            
            utils.get_state()
            for o in mesh:
                o.select_set(True)
            armObj.select_set(True)
            utils.activate(armObj)
            bpy.ops.object.delete()
        
        for o in qualified:
            if o.type == 'ARMATURE':
                
                if o == armObj:
                    print("devkit::reshape reports : attempt to duplicate reports the same armature")
                    return False
                armObj = o
    
    else:
        qualified = [o for o in mesh]
        qualified.append(armObj)
    
    for o in bpy.context.selected_objects:
        o.select_set(False)

    armObj.select_set(True)
    utils.activate(armObj)

    S = mathutils.Matrix()
    for i in range(3):
        S[i][i] = 1

    if 1 == 0:

        R90i = mathutils.Matrix.Rotation(math.radians(-90.0), 4, 'Z')
        matrices_rotated = {}
        for boneObj in armObj.pose.bones:
            bone = boneObj.name
            if bone not in matrices:
                continue
            mat = matrices[bone]
            l = mat.to_translation()
            L = mathutils.Matrix.Translation(l)
            L = R90i @ L
            r = boneObj.bone.matrix_local.copy().to_quaternion()
            R = r.to_matrix().to_4x4()
            M = L @ R @ S
            matrices_rotated[bone] = M

        for boneObj in armObj.pose.bones:
            bone = boneObj.name
            if bone not in matrices:
                continue
            boneObj.matrix = matrices_rotated[bone]
        utils.update()

    if rotate == True:
        mw = armObj.matrix_world.copy()
        l = mw.to_translation()
        s = mw.to_scale()
        L = mathutils.Matrix.Translation(l)
        S = mathutils.Matrix()
        for i in range(3):
            S[i][i] = s[i]
        R = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Z')
        M = L @ R @ S
        armObj.matrix_world = M
        bpy.ops.object.transform_apply( rotation=True, location=False, scale=False )

    if 1 == 1:

        MS = mathutils.Matrix()
        S = mathutils.Matrix()
        for i in range(3):
            MS[i][i] = 1

        for boneObj in armObj.pose.bones:
            bone = boneObj.name
            if bone not in matrices:
                continue

            mat = matrices[bone]

            so = mat.to_scale()
            for i in range(3):
                S[i][i] = s[i]

            S = MS

            if 1 == 1:
                if bone in skel.avatar_skeleton:
                    if skel.avatar_skeleton[bone]['type'] == 'collision':
                        sb = [ a for a in skel.avatar_skeleton[bone]['scale'] ]
                        
                        s = [0,0,0]
                        for i in range(3):
                            offset = utils.base_to_sign(base=s[i], offset=so[i])
                            s[i] = 1 + offset
                        S = mathutils.Matrix()
                        for i in range(3):
                            S[i][i] = s[i]

            l = mat.to_translation()
            
            r = boneObj.bone.matrix_local.copy().to_quaternion()
            L = mathutils.Matrix.Translation(l)
            R = r.to_matrix().to_4x4()
            M = L @ R @ S
            boneObj.matrix = M
            utils.update()

    if rotate == True:
        mw = armObj.matrix_world.copy()
        l = mw.to_translation()
        s = mw.to_scale()
        L = mathutils.Matrix.Translation(l)
        S = mathutils.Matrix()
        for i in range(3):
            S[i][i] = s[i]
        R = mathutils.Matrix.Rotation(math.radians(-90.0), 4, 'Z')
        M = L @ R @ S
        armObj.matrix_world = M
        bpy.ops.object.transform_apply( rotation=True, location=False, scale=False )

    rigutils.rebind(armObj)

    utils.set_state(state)

    return qualified
