


















import bpy
import math
import mathutils
import traceback

from . import pill
from . import rigutils
from . import utils
from . import devkit
from .presets import volumes

from .presets import skeleton as skel



from .presets import bind_data
from .presets import base_data
from .presets import rig_data as rd
from .presets import real_rig_data

import xml.etree.ElementTree as ET

Z90 = mathutils.Matrix ((
    ( 0.0000,  1.0000, 0.0000, 0.0000),
    (-1.0000,  0.0000, 0.0000, 0.0000),
    ( 0.0000,  0.0000, 1.0000, 0.0000),
    ( 0.0000,  0.0000, 0.0000, 1.0000)
    ))

Z90I = Z90.inverted()


R90x = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'X')
R90y = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Y')
R90 = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Z')
R90I = R90.inverted()
R90z = R90

R180x = mathutils.Matrix.Rotation(math.radians(180.0), 4, 'X')
R180y = mathutils.Matrix.Rotation(math.radians(180.0), 4, 'Y')
R180z = mathutils.Matrix.Rotation(math.radians(180.0), 4, 'Z')














def write_collada(armature="", root="", write=False, file_in="", file_out="", real_armature=None):
    armObj = bpy.data.objects[armature]
    
    realObj = bpy.data.objects[real_armature]

    
    
    
    bb_devkit = bpy.context.scene.bb_devkit

    
    
    
    
    rig_class = rigutils.get_rig_class()
    if rig_class != "":
        rig_data = getattr(rd, rig_class)
    else:
        
        
        
        
        
        
        rig_data = rigutils.get_rig_data(armObj)

    
    
    bb_mesh = bpy.context.scene.bb_devkit

    ccp = bpy.context.window_manager.cc_props

    
    
    
    
    use_rig_data = bb_devkit.use_rig_data
    use_bind_data = bb_devkit.use_bind_data
    
    
    
    
    
    
    
    
    use_app_compatible_data = bb_devkit.use_app_compatible_data
    
    if use_app_compatible_data == True:
        if armObj.get('bb_devkit_transforms') == None:
            use_app_compatible_data = False
            use_rig_data = True
            
    
    if use_bind_data == True:
        has_bind_data = False
        
        for boneObj in armObj.data.bones:
            if boneObj.get('bind_mat') != None:
                has_bind_data = True
                
                break
        if has_bind_data == False:
            
            use_bind_data = False
            use_rig_data = True

    process_volume_bones = bb_devkit.process_volume_bones
    process_attachment_bones = bb_devkit.process_attachment_bones

    if process_attachment_bones == True:
        print("Attachment bones enabled")

    rotate_for_sl = bb_devkit.rotate_for_sl

    use_offset_location = bb_devkit.use_offset_location
    use_offset_rotation = bb_devkit.use_offset_rotation
    use_offset_scale = bb_devkit.use_offset_scale

    
    
    export_path_to_pelvis = bb_devkit.export_path_to_pelvis

    
    
    export_full_rig = bb_devkit.export_full_rig

    
    
    
    
    
    if realObj.get('bb_devkit_transforms') != None or realObj.get('bb_dae_bind') != None:
        export_path_to_pelvis = False
        export_full_rig = False

    if export_path_to_pelvis:
        print("export_path_to_pelvis is designed to give you proper deformations while still being compatible with other applications.")
    if export_full_rig:
        print("export_full_rig Will NOT work in Second Life, it will be most useful when using other applications.")

    if armObj.get('bentobuddy_converted') != None:
        print("collada::write_collada reports: converted mesh detected, adjusting export properties")
        export_path_to_pelvis = True
        export_full_rig = False
        rig_class = ""

    
    
    if use_app_compatible_data == True and armObj.get('bb_devkit_transforms') != None:
        print("Exporting using compatible transforms")

        
        
        

        
        
        
        
        
        bind_pose = {}
        for bone in armObj['bb_devkit_transforms']['bind_pose']:
            bind_pose[bone] = mathutils.Matrix(armObj['bb_devkit_transforms']['bind_pose'][bone])
        joint_pose = {}
        for bone in armObj['bb_devkit_transforms']['joint_pose']:
            joint_pose[bone] = mathutils.Matrix(armObj['bb_devkit_transforms']['joint_pose'][bone])

        edit_dae(
            file_in=file_in,
            file_out=file_out,
            bind_pose=bind_pose,
            joint_pose=joint_pose,
            pretty_mats=True,
            write_nodes=True,
            export_path_to_pelvis=False,
            export_full_rig=False,
            process_attachment_bones=process_attachment_bones,
            process_volume_bones=process_volume_bones,
            )

        bb_devkit.rotate_for_sl = rotate_for_sl

        return True



    if 1 == 0:
        print("Entering write_collada with: armature/root/write/file_in/file_out")
        print("armature:", armature)
        print("root:", root)
        print("write:", write)
        print("file_in:", file_in)
        print("file_out:", file_out)

    
    
    
    
    
    
    
    
    
    
    
    

    print("Note that write_nodes is switched of at some point in collada.py (write_nodes = False)")
    write_nodes = False 

    
    
    

    
    
    

    
    
    
    
    
    
    
    
    

    
    
    
    
    


    
    rig_type = armObj.get('rig_type', 'pivot')

    
    
    if armObj.get('rig_type') == "N/A": 
        rig_type = "pivot"
        print("found N/A, changed to pivot")

    if (
        use_rig_data == False and
        use_bind_data == False
        
        ):
        print("No pose type selected, defaulting to Rig Pose")
        use_rig_data = True









    
    
    
    
    
    
    bind_pose = {}
    joint_pose = {}

    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    sl_rig = None
    if armObj.get('bentobuddy') != None:
        sl_rig = "bentobuddy"
        print("Found SL compatible rig, maybe:", sl_rig)
    if armObj.get('avastar') != None:
        sl_rig = "avastar"
        print("Found SL compatible rig, maybe:", sl_rig)
        


    
    

    
    
    
    
    
    
    if use_rig_data == True:

        
        
        
        









        print("Running rig_pose exporter")

        write_nodes = True

        
        
        
        
        
        

        
        
        
        
        

        
        
        
                
                

        if rig_class != "":
            print("Found rig class:", rig_class)


        
        
        
        
            
            

        
        else:
            print("collada::write_collada reports: no base data was available for custom bind poses, using rig instead")
            
            
            
            if utils.can_select(object=armObj.name) == False:
                print("collada::write_collada reports bad return from utils::can_select")
                print("The rig has to be in view and selectable to generate bind data, did you choose the wrong export option?")
                popup("Export failed, wrong export option?  Where is the rig?", "Error", "ERROR")
                return False
            
            
            
            
            
            

        
        
        
 
        
        use_old_transforms = False
        if use_old_transforms == True:
            print("Using old transform method")
            transforms = rigutils.get_bone_transforms(armature=armature, rig_data=rig_data)

        for pBone in armObj.pose.bones:
            dBone = pBone.bone
            bone = pBone.name

            
            if bone not in skel.avatar_skeleton:
                continue

            
            
            
            
            
            if skel.avatar_skeleton[bone]['type'] == "attachment":
                if process_attachment_bones == False:
                    continue

            
            
            
            
            
            if use_old_transforms == True:
                joint_pose[bone] = transforms[bone]['local']['matrix']
                bind_pose[bone] = transforms[bone]['bind_data']

            
            else:
                jd = rigutils.get_joint_data(armature=armObj.name, bone=bone, rig_data=rig_data)
                joint_pose[bone] = jd[bone]['joint_data']

                bd = rigutils.get_bind_data(armature=armObj.name, bone=bone, rig_data=rig_data)
                bind_pose[bone] = bd[bone]['bind_data']

    
    
    
    
    
    
    
    
    
    
    
    
    
    elif use_bind_data == True:
        
        

        
        
        
        
        
        
        
        print("Running bind_pose exporter")

        write_nodes = False

        has_bind_info = list()
        not_bind_info = list()
        for boneObj in armObj.data.bones:
            if boneObj.use_deform == False:
                continue
            bone = boneObj.name

            
            if bone not in skel.avatar_skeleton:
                continue

            
            
            
            if skel.avatar_skeleton[bone]['type'] == "attachment":
                if process_attachment_bones == False:
                    continue



            
            
            matf = get_bind_matrix(
                armature=armature,
                bone=bone,
                process_volume_bones=process_volume_bones,
                rotate_for_sl=rotate_for_sl
                )
            if bone in realObj.data.bones:
                if realObj.data.bones[bone].get('bind_mat') == None:
                    
                    print("Missing bind data, this is a serious error:", bone)
                    not_bind_info.append(bone)

                else:
                    has_bind_info.append(bone)
                    bind_mat = mathutils.Vector(realObj.data.bones[bone]['bind_mat'])
                    matf = vec2mat(bind_mat)

                bind_pose[bone] = matf


            
                
            
                
                
                

            
            
            

            
            
            
            
            if 1 == 0:
                transforms = rigutils.get_joint_data(armature=armObj.name, bone=bone, rig_data=rig_data)
                if transforms == False:
                    print("Could not retrieve transform data, this is a programming bug")
                    popup("Fatal internal error processing Avastar rig, please report it", "Error", "ERROR")
                    return False
                
                
                joint_pose[bone] = transforms[bone]['joint_data']


        
        if len(not_bind_info) > 0:
            print("The following bones did not have imported bind info so the rig/bone was used instead:")
            print(not_bind_info)
            if len(has_bind_info) > 0:
                print("The following bones had bind info and were processed using that available data:")
                print(has_bind_info)
            else:
                print("There was no imported bind information available for any of the bones")

    
    
    
    
    
    
    













    
    

    
    
    
    

    
    
    elif 1 == 0:

        print("Exporting from Avastar data...")
        print("WARNING: use_offset_location for bind pose defaults to False when using Avastar pose")


        if 1 == 0:
            
            with_appearance = True
            apply_armature_scale = True
            with_sl_rot = True
            use_bind_pose = False
            write_nodes = False

            print("Using alternative avaturd code")
            for boneObj in armObj.data.bones:
                bone = boneObj.name
                if bone not in skel.avatar_skeleton:
                    continue
                if skel.avatar_skeleton[bone]['type'] == 'attachment':
                    continue





                print("Missing line, remove comment and None")
                matf = None
                

                bind_pose[bone] = matf

                bd = rigutils.get_bind_data(armature=armObj.name, bone=bone, rig_data=rig_data)
                bind_pose[bone] = bd[bone]['bind_data']

            edit_dae(
                file_in=file_in,
                file_out=file_out,
                bind_pose=bind_pose,
                joint_pose=joint_pose,
                pretty_mats=True,
                write_nodes=write_nodes,
                export_path_to_pelvis=export_path_to_pelvis,
                export_full_rig=export_full_rig,
                process_attachment_bones=process_attachment_bones,
                process_volume_bones=process_volume_bones,
                )
            return True

        old_ap = False



        if armObj.get('avastar') == None:
            print("Not an Avastar rig, I'll try anyway.")
            
            
        for boneObj in armObj.data.bones:
            bone = boneObj.name

            if bone not in skel.avatar_skeleton:
                continue

            
            
            
            if skel.avatar_skeleton[bone]['type'] == "attachment":
                if process_attachment_bones == False:
                    continue




            


            








            

                

            
            
            
            

            




            if old_ap == True:
                matf = ap.get_rig_data(armObj, boneObj)
            else:
                matf = ava.get_rig_data(armObj, boneObj)

            

            bind_pose[bone] = matf

            
            
            
            
            
            
            
            
            write_nodes = True

            
            
            dBone = boneObj

            
            
            

            
            offsets = {}
            offsets['global'] = dict()
            offsets['local'] = dict()

            dmg = mathutils.Matrix(rig_data[bone]['matrix_local'])
            dmgI = dBone.matrix_local @ dmg.inverted()
            R = mathutils.Matrix.Rotation(math.radians(-90.0), 4, 'Z')
            RI = R.inverted()
            dmgI = dmgI @ R
            dmgI = RI @dmgI
            offsets['global']['matrix'] = dmgI

            if dBone.parent and dBone.parent.use_deform == True:
                pbone = dBone.parent.name
                rml = dBone.parent.matrix_local.inverted() @ dBone.matrix_local
                dml = mathutils.Matrix(rig_data[pbone]['matrix_local']).inverted() @ dmg
                offsets['local']['matrix'] = rml.inverted() @ dml
            else:
                print("Storing global to local with questionable orientation for ROOT bone")
                offsets['local']['matrix'] = offsets['global']['matrix']
            LJ, RJ, SJ = pill.recompose(
                rig_type=rig_type,
                dBone=dBone,
                
                
                offsets=offsets,
                
                
                
                
                
                use_offset_location=use_offset_location,
                use_offset_rotation=use_offset_rotation,
                use_offset_scale=use_offset_scale,
                process_volume_bones=process_volume_bones)

            matj = LJ @ RJ @ SJ
            joint_pose[bone] = matj
            
            
            
            
            transforms = rigutils.get_joint_data(armature=armObj.name, bone=bone, rig_data=rig_data)
            if transforms == False:
                print("Could not retrieve transform data, this is a programming bug")
                popup("Fatal internal error processing Avastar rig, please report it", "Error", "ERROR")
                return False
            
            
            joint_pose[bone] = transforms[bone]['joint_data']

            
            
            
            
            
            
            

            
            
            
            
            

            if 1 == 1:
                
                LB, RB, SB = pill.recompose(
                    rig_type=rig_type,
                    dBone=dBone,
                    
                    
                    
                    
                    
                    bone_space="global",  
                    offsets=offsets,
                    
                    
                    
                    
                    

                    
                    
                    
                    
                    

                    use_offset_location=False,
                    use_offset_rotation=use_offset_rotation,
                    use_offset_scale=use_offset_scale,
                    process_volume_bones=True)

                
                
                
                
                
                l,r,s = matf.decompose()
                L = mathutils.Matrix.Translation(l)
                S = mathutils.Matrix()
                for i in range(3):
                    S[i][i] = s[i]
                matb = L @ RB @ S
                bind_pose[bone] = matb
            
            else:

                bd = rigutils.get_bind_data(armature=armObj.name, bone=bone, rig_data=rig_data)
                bind_pose[bone] = bd[bone]['bind_data']



            
    else:
        print("collada:write_collada reports: no export pose matched")
        return False

    
    
    
    
    
    
    
    edit_dae(
        file_in=file_in,
        file_out=file_out,
        bind_pose=bind_pose,
        joint_pose=joint_pose,
        pretty_mats=True,
        write_nodes=write_nodes,
        export_path_to_pelvis=export_path_to_pelvis,
        export_full_rig=export_full_rig,
        process_attachment_bones=process_attachment_bones,
        process_volume_bones=process_volume_bones,
        )

    return




def get_bone_bind(pose_bone):
    
    rest = pose_bone.bone.matrix_local.copy()
    if pose_bone.parent:
        par_rest = pose_bone.parent.bone.matrix_local.copy()
    else:
        par_rest = mathutils.Matrix()
    final_rest = par_rest.inverted() @ rest
    return final_rest

















def edit_dae(
    file_in=None, file_out=None,
    bind_pose=None, joint_pose=None,
    pretty_mats=True, write_nodes=False,
    export_path_to_pelvis=False,
    export_full_rig=False,
    process_attachment_bones=False,
    process_volume_bones=False,
    ):

    
    ET.register_namespace('',"http://www.collada.org/2005/11/COLLADASchema")
    tree = ET.parse(file_in)
    root = tree.getroot()
    n = '{http://www.collada.org/2005/11/COLLADASchema}'
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

                    
                    
                    
                    
                    
                    
                    
                    
                    

                    
                    
                    names = data.text.split()

                    
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
                            
                            



                            
                            all_bones = []
                            for bone in skel.avatar_skeleton:
                                bone = bone.replace(" ", "_")
                                all_bones.append(bone)



                            all_bones = [b for b in skel.avatar_skeleton if " " not in b]
                            for bone in all_bones:

                                
                                
                                
                                
                                
                                
                                
                                

                                if bone not in name_set:
                                    joint_type = skel.avatar_skeleton[bone]['type']
                                    if joint_type == 'attachment' and process_attachment_bones == True:
                                        names.append(bone)
                                    elif joint_type == 'collision' and process_volume_bones == True:
                                        names.append(bone)
                                    else: 
                                        names.append(bone)

                        if export_path_to_pelvis == True:
                            bone_path = set()
                            names_set = set(names)

                            
                            converted_names = {}
                            for bone in skel.avatar_skeleton:
                                new_bone = bone.replace(" ", "_")
                                converted_names[new_bone] = {}
                                converted_names[new_bone]['parent'] = skel.avatar_skeleton[bone]['parent']

                            for bone in names:
                                
                                parent = ""
                                next_bone = bone
                                while(True):
                                    
                                    
                                    
                                    
                                    parent = converted_names[next_bone]['parent']

                                    if parent != "":
                                        
                                        if parent not in names_set:
                                            if parent not in bone_path:
                                                bone_path.add(parent)

                                        next_bone = parent

                                    else:
                                        break
                            
                            
                            
                            
                            
                            
                            
                            
                            for bone in bone_path:
                                if bone not in names_set:
                                    names.append(bone)
                            

                        

                        for i in range(len(names)):
                            text_mat = list()
                            bone = names[i]
                            if bone not in bind_pose: 
                                continue
                            m = bind_pose[bone]
                            joint_total += 1

                            
                            
                            
                            mat = m.inverted()

                            for m in mat:
                                
                                float_total += 4

                                shorten = [round(a, 6) for a in m]
                                t = [str(a) for a in shorten]

                                
                                if pretty_mats == True:
                                    text_mat.append("\n")
                                else:
                                    text_mat.append(" ")
                                text_mat.append(" ".join(t))
                            matrices.extend(text_mat)
                            
                            
                            
                            if pretty_mats == True:
                                matrices.append("\n")
                            else:
                                matrices.append(" ")

                        
                        
                        Name_array.text = " ".join(names)

                        
                        
                        
                        
                        
                        
                        
                        
                        Name_array.set('count', str(len(names)))

                        float_array.set('count', str(float_total))
                        Name_array_accessor_count.set('count', str(joint_total))
                        float_array_accessor_count.set('count', str(joint_total))

                        data.text = "".join(matrices)

                        del matrices
                        del names


    
    
    if write_nodes == True:
        missing_joints = []
        for node in root.iter(f'{n}node'):
            if node.get('type') == "JOINT":
                matrix = node.find(f'{n}matrix')
                if node.attrib.get('name') != None:
                    bone = node.attrib['name']

                    
                    

                    if 1 == 0:
                        
                        
                        
                        if bone in skel.avatar_skeleton:
                            if skel.avatar_skeleton[bone]['type'] == "attachment":
                                if process_attachment_bones == False:
                                    continue

                    if bone in joint_pose:
                        tmat = pill.matrix_to_text(joint_pose[bone])
                        matrix.text = " ".join(tmat)
                    else:
                        missing_joints.append(bone)
                        print(":library_visual_scene - missing bone, this should never happen", bone)

        if len(missing_joints) > 0:
            print("edit_dae:",
                "Some joints have no associated data.")
            for bone in missing_joints:
                print("  -", bone)
            

    
    
    
    if pretty_mats == True:
        pretty_nodes(root=root)

    tree.write(file_out,
        xml_declaration = True,
        encoding = 'utf-8',
        method = 'xml'
        )

    return True












def compare_nodes(file1,file2, node=None):
    if node == None:
        print("collada::compare_nodes reports: nothing to do")
        return False

    
    
    node1 = {}
    node2 = {}
    ET.register_namespace('',"http://www.collada.org/2005/11/COLLADASchema")
    tree = ET.parse(file1)
    root1 = tree.getroot()
    n = '{http://www.collada.org/2005/11/COLLADASchema}'

    lc = root1.find(f'{n}library_controllers')
    for c in lc:
        cid = c.get('id')
        name = c.get('name')
        controller[cid] = name
        skin = c.find(f'{n}skin')
        for skin_child in skin:
            for data in skin_child:
                if data.tag == n + "Name_array":
                    print("Found Name_array")
                    names = data.text.split()
                if data.tag == n + "float_array":
                    print("found float array")

    return True





def replace_scale(bone=None, mat=None, scale=None):
    loc,rot,s = mat.decompose() 
    L = mathutils.Matrix.Translation(loc)
    if scale == None:
        scale = skel.avatar_skeleton[bone]['scale']
    S = mathutils.Matrix()
    S[0][0] = scale[0]
    S[1][1] = scale[1]
    S[2][2] = scale[2]
    eu = mat.to_euler()
    
    R = mathutils.Euler(eu,eu.order).to_matrix().to_4x4()
    return L @ R @ S





def replace_rotation(bone=None, mat=None, rot=None):
    loc,r,scale = mat.decompose()
    L = mathutils.Matrix.Translation(loc)
    S = mathutils.Matrix()
    S[0][0] = scale[0]
    S[1][1] = scale[1]
    S[2][2] = scale[2]
    
    eu = mat.to_euler()
    if rot == None:
        rot = skel.avatar_skeleton[bone]['rot']
        eu = [math.radians(a) for a in rot]
        
        R = mathutils.Euler(eu,'XYZ').to_matrix().to_4x4()
    else:
        R = mathutils.Euler(rot,eu.order).to_matrix().to_4x4()
    return L @ R @ S



def replace_location(bone=None, mat=None, loc=None):
    l,rot,scale = mat.decompose()
    L = mathutils.Matrix()
    if loc == None:
        loc = skel.avatar_skeleton[bone]['pivot']
    L[0][3] = loc[0]
    L[1][3] = loc[1]
    L[2][3] = loc[2]
    S = mathutils.Matrix()
    S[0][0] = scale[0]
    S[1][1] = scale[1]
    S[2][2] = scale[2]
    eu = mat.to_euler()
    R = mathutils.Euler(eu,eu.order).to_matrix().to_4x4()
    return L @ R @ S





def matrix_from_list(l):
    M = mathutils.Matrix()
    for c in range(4):
        for r in range(4):
            M[c][r] = l[4*r + c]
    return M



def vec2mat(v):
    M = mathutils.Matrix()
    for i in range(4):
        for j in range(4):
            M[i][j] = v[4*j + i]
    return M




def pretty_matrices(file_in=None, file_out=None):

    ET.register_namespace('',"http://www.collada.org/2005/11/COLLADASchema")
    tree = ET.parse(file_in)
    root = tree.getroot()
    n = '{http://www.collada.org/2005/11/COLLADASchema}'
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
                        
    tree.write(file_out,
        xml_declaration = True,
        encoding = 'utf-8',
        method = 'xml'
        )




def pretty_nodes(root=None):
    

    print("Generating pretty nodes")

    n = '{http://www.collada.org/2005/11/COLLADASchema}'

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









def save_nodes(file="", root=None):
    if file == "":
        print("save_nodes: no mat_file")
        return False

    try:
        mf = open(file, "w", encoding='UTF8')
    except:
        print("Couldn't open file to write nodes")
        return False

    print("saving nodes...")

    n = '{http://www.collada.org/2005/11/COLLADASchema}'

    node_matrix = {}

    
    pretty_it = True

    for node in root.iter(f'{n}node'):
        if node.get('type') == "JOINT":
            matrix = node.find(f'{n}matrix')
            if node.attrib.get('name') != None:
                bone = node.attrib['name']
                
                matrix = node.find(f'{n}matrix')
                tfloats = matrix.text.split()
                if pretty_it == True:
                
                    t = list()
                    for tfl in tfloats:
                        rfl = round(float(tfl), 6)
                        
                        strip = f"{rfl:.6f}".rstrip('0')
                        
                        if strip.endswith("."):
                            strip = strip.replace(".", ".0")
                        t.append(strip)
                    node_matrix[bone] = " ".join(t)
                else:
                    node_matrix[bone] = " ".join(tfloats)

    
    text_out = "# library_visual_scene nodes / matrices\n"
    text_out += "node_matrices = {\n"
    for k,v in node_matrix.items():
        text_out += '    "' + k + '": ' + '"' + v + '"' + ",\n"
    text_out += "    }\n"

    mf.write(text_out)
    mf.close()
    return True









def replace_nodes(file="", root=None):

    if file == "":
        print("replace_nodes: no mat_file")
        return False

    print("replacing nodes...")

    node_matrices = {}
    try:
        namespace = {}
        exec(open(file, 'r', encoding='UTF8').read(), namespace)
        node_matrices.update(namespace['node_matrices'])
    except Exception as e:
        print(traceback.format_exc())

    

    n = '{http://www.collada.org/2005/11/COLLADASchema}'

    for node in root.iter(f'{n}node'):
        if node.get('type') == "JOINT":
            matrix = node.find(f'{n}matrix')
            if node.attrib.get('name') != None:
                bone = node.attrib['name']

                matrix = node.find(f'{n}matrix')
                if bone in node_matrices:
                    matrix.text = node_matrices[bone]
                else:
                    print(bone + ":missing")

    return root 






def fix_nodes(root=None):
    

    print("WARNING: collada::fix_nodes reports: does not provide rotation data, fix later")

    n = '{http://www.collada.org/2005/11/COLLADASchema}'

    
    
    
    
    
    for node in root.iter(f'{n}node'):
        if node.get('type') == "JOINT":
            matrix = node.find(f'{n}matrix')
            if node.attrib.get('name') != None:
                bone = node.attrib['name']
                
                
                if bone in skel.avatar_skeleton:
                    tmat = matrix.text.split()
                    
                    
                    tMatrix = pill.tMatrix
                    tMatrix[3] = tmat[3]
                    tMatrix[7] = tmat[7]
                    tMatrix[11] = tmat[11]
                    t = list()
                    for r in range(0, 16, 4):
                        t.append("\n")
                        t.extend(tMatrix[r:r+4])
                    matrix.text = " ".join(t)
    return root 



def get_bind_matrix(armature=None, bone=None, process_volume_bones=False, rotate_for_sl=False):
    if bone == None or armature == None:
        return mathutils.Matrix()

    armObj = bpy.data.objects[armature]
    boneObj = armObj.data.bones[bone]

    loc = boneObj.head_local
    L = mathutils.Matrix.Translation((loc))

    R = mathutils.Matrix()
    ROT = mathutils.Matrix() 
    S = mathutils.Matrix()

    if process_volume_bones == True:
        if bone in volumes.vol_joints:
            rot = skel.avatar_skeleton[bone]['rot'] 
            rot_rad = [math.radians(r) for r in rot] 
            ROT = mathutils.Euler(rot_rad,'XYZ').to_matrix().to_4x4()
            scale = volumes.vol_joints[bone]['scale']
            S[0][0] = scale[0]
            S[1][1] = scale[1]
            S[2][2] = scale[2]
    else:
        rot_rad = armObj.data.bones[bone].matrix_local.to_euler()
        ROT = mathutils.Euler(rot_rad,'XYZ').to_matrix().to_4x4()
        scale = armObj.pose.bones[bone].scale
        S[0][0] = scale[0]
        S[1][1] = scale[1]
        S[2][2] = scale[2]

    
    
    
    
    
    

    if rotate_for_sl == True:
        matf = R90 @ L @ R90I @ ROT @ S
    else:
        matf = L @ ROT @ S
    return matf







def get_bind_pose(file=None, bone=None):

    bone_name = bone

    import mathutils
    import xml.etree.ElementTree as ET

    ET.register_namespace('',"http://www.collada.org/2005/11/COLLADASchema")
    tree = ET.parse(file)
    root = tree.getroot()
    n = '{http://www.collada.org/2005/11/COLLADASchema}'
    controller = {}
    skin = {}
    names = list()
    joints = {}
    matrices = list()

    
    
    bind_pose = dict()

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
                        
                        
                        matrices = [round(float(i), 6) for i in data.text.split()]
                        
                        block = 0
                        for i in range(len(names)):
                            bone = names[i]
                            mat = matrices[block:block+16]
                            block+= 16
                            
                            M = mathutils.Matrix()
                            for c in range(4):
                                for r in range(4):
                                    M[c][r] = mat[ r + (c*4) ]
                            
                            
                            bind_pose[bone] = mat
    print("returning matrix for bone:", bone_name)
    return bind_pose[bone_name]

def get_joint_pose(file=None, bone=None):
    bone_name = bone

    import mathutils
    import xml.etree.ElementTree as ET

    ET.register_namespace('',"http://www.collada.org/2005/11/COLLADASchema")
    tree = ET.parse(file)
    root = tree.getroot()
    n = '{http://www.collada.org/2005/11/COLLADASchema}'

    joint_pose = {}

    for node in root.iter(f'{n}node'):
        if node.get('type') == "JOINT":
            matrix = node.find(f'{n}matrix')
            if node.attrib.get('name') != None:
                bone = node.attrib['name']
                matrix = node.find(f'{n}matrix')
                joint_pose[bone] = matrix.text

    return joint_pose[bone_name]




def popup(message = "", title = "Message Box", icon =  'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
    return





def to_deg(mat):
    eu = mat.to_euler()
    return [math.degrees(round(a, 4)) for a in eu]



def close_enough(a, b, tol=0.000001):
    if a > b:
        n = round((a - b), 6)
    elif a < b:
        n = round((b - a), 6)
    elif a == b:
        return False
    if n > tol:
        return True
    return False











def export_custom(
    armature=None,
    file_in=None, file_out=None,
    pretty_mats=True, write_nodes=False,
    export_path_to_pelvis=False,
    export_full_rig=False,
    ):

    print("Running export_custom...")

    obj = bpy.data.objects
    armObj = obj[armature]

    
    if utils.can_select(object=armObj.name) == False:
        print("collada::write_collada reports bad return from utils::can_select")
        print("The rig has to be in view and selectable to generate bind data, did you choose the wrong export option?")
        popup("Export failed, wrong export option?  Where is the rig?", "Error", "ERROR")
        return False

    
    

    rig_data = rigutils.get_rig_data(armObj)

    joint_pose = {}
    bind_pose = {}
    for pBone in armObj.pose.bones:
        dBone = pBone.bone
        bone = pBone.name
        
        if bone not in skel.avatar_skeleton:
            continue
        jd = rigutils.get_joint_data(armature=armObj.name, bone=bone, rig_data=rig_data)
        joint_pose[bone] = jd[bone]['joint_data']
        bd = rigutils.get_bind_data(armature=armObj.name, bone=bone, rig_data=rig_data)
        bind_pose[bone] = bd[bone]['bind_data']

    
    ET.register_namespace('',"http://www.collada.org/2005/11/COLLADASchema")
    tree = ET.parse(file_in)
    root = tree.getroot()
    n = '{http://www.collada.org/2005/11/COLLADASchema}'
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

                    
                    
                    names = data.text.split()

                    
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
                                
                                joint_type = skel.avatar_skeleton[bone]['type']
                                if joint_type == 'collision' or joint_type == 'bone':
                                    if bone not in name_set:
                                        names.append(bone)
                        
                        if export_path_to_pelvis == True:
                            bone_path = set()
                            names_set = set(names)

                            for bone in names:
                                
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
                            
                            
                            
                            
                            
                            
                            
                            
                            for bone in bone_path:
                                if bone not in names_set:
                                    names.append(bone)
                            

                        
                        qualified_joints = []
                        for i in range(len(names)):
                            joint_total += 1
                            text_mat = list()
                            bone = names[i]
                            
                            if bone not in bind_pose:
                                continue
                            m = bind_pose[bone]

                            
                            
                            qualified_joints.append(bone)

                            
                            
                            
                            mat = m.inverted()

                            for m in mat:
                                
                                float_total += 4

                                shorten = [round(a, 6) for a in m]
                                t = [str(a) for a in shorten]

                                
                                if pretty_mats == True:
                                    text_mat.append("\n")
                                else:
                                    text_mat.append(" ")
                                text_mat.append(" ".join(t))
                            matrices.extend(text_mat)
                            
                            
                            
                            if pretty_mats == True:
                                matrices.append("\n")
                            else:
                                matrices.append(" ")

                        
                        
                        
                        
                        
                        Name_array.text = " ".join(qualified_joints)

                        
                        
                        
                        
                        
                        

                        Name_array_accessor_count.set('count', str(len(qualified_joints)))
                        Name_array.set('count', str( len(qualified_joints)))
                        float_array.set('count', str(float_total))
                        float_array_accessor_count.set('count', str(len(qualified_joints)))

                        data.text = "".join(matrices)

                        del matrices
                        del names


    
    
    if write_nodes == True:
        missing_joints = []
        for node in root.iter(f'{n}node'):
            if node.get('type') == "JOINT":
                matrix = node.find(f'{n}matrix')
                if node.attrib.get('name') != None:
                    bone = node.attrib['name']

                    
                    

                    if bone in joint_pose:
                        tmat = pill.matrix_to_text(joint_pose[bone])
                        matrix.text = " ".join(tmat)
                    else:
                        missing_joints.append(bone)
                        print(":library_visual_scene - missing bone, this should never happen", bone)

        if len(missing_joints) > 0:
            print("write_nodes:",
                "Some joints have no associated data.")
            for bone in missing_joints:
                print("  -", bone)
            

    
    
    
    if pretty_mats == True:
        pretty_nodes(root=root)

    tree.write(file_out,
        xml_declaration = True,
        encoding = 'utf-8',
        method = 'xml'
        )







def pretty_dae(file_in=None, file_out=None):
    ET.register_namespace('',"http://www.collada.org/2005/11/COLLADASchema")
    tree = ET.parse(file_in)
    root = tree.getroot()
    n = '{http://www.collada.org/2005/11/COLLADASchema}'
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
                sid = node.attrrib.get('sid')
                if sid != None:
                    bone == sid
                
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













































def get_matrices(file=None, base="female_neutral", armature=None, report=False):
    print("collada::get_matrices processing unified matrix")

    armObj = armature
    if isinstance(armature, str):
        armObj = bpy.data.objects[armature]

    
    if file == None:
        print("collada::get_matrices : no file, nothing to do")
        return False

    ET.register_namespace('',"http://www.collada.org/2005/11/COLLADASchema")
    tree = ET.parse(file)
    root = tree.getroot()
    n = '{http://www.collada.org/2005/11/COLLADASchema}'
    controller = {}
    skin = {}
    names = list()
    joints = {}
    matrices = list()

    
    
    transforms = {}

    
    
    bind_pose = {}

    lc = root.find(f'{n}library_controllers')
    for c in lc:
        cid = c.get('id')
        name = c.get('name')
        controller[cid] = name
        skin = c.find(f'{n}skin')
        for skin_child in skin:

            
            
            
            
            if skin_child.tag == n + "bind_shape_matrix":
                mat = [round(float(i), 6) for i in skin_child.text.split()]
                M = mathutils.Matrix()
                for c in range(4):
                    for r in range(4):
                        M[c][r] = mat[ r + (c*4) ]
                transforms['bind_shape'] = M

            for data in skin_child:
                if data.tag == n + "Name_array":
                    names = data.text.split()
                if data.tag == n + "float_array":
                    
                    param = skin_child.find(f'{n}technique_common/{n}accessor/{n}param')
                    
                    if param.get('type') == "float4x4":
                        
                        
                        matrices = [round(float(i), 6) for i in data.text.split()]
                        
                        block = 0
                        for i in range(len(names)):
                            bone = names[i]



                            mat = matrices[block:block+16]
                            block+= 16
                            
                            M = mathutils.Matrix()
                            for c in range(4):
                                for r in range(4):
                                    M[c][r] = mat[ r + (c*4) ]
                            bind_pose[bone] = M

    transforms['bind_data'] = bind_pose

    
    
    
    
    joint_pose = {}
    for node in root.iter(f'{n}node'):
        if node.get('type') == "JOINT":
            matrix = node.find(f'{n}matrix')
            if matrix == None:
                continue
            if node.attrib.get('name') != None:
                bone = node.attrib['name']
                sid = node.attrib.get('sid')
                if sid != None:
                    bone = sid
                mat = [round(float(i), 6) for i in matrix.text.split()]
                M = mathutils.Matrix()
                for c in range(4):
                    for r in range(4):
                        M[c][r] = mat[ r + (c*4) ]
                joint_pose[bone] = M
    transforms['bone_data'] = joint_pose

    
    
    
    
    
    
    real_data = {}
    for cbone in transforms['bind_data']:
        
        
        
        cmatb = transforms['bind_data'][cbone]
        cmati = cmatb.inverted() 

        pbone = ""
        
        
        
        
        
        if cbone not in skel.avatar_skeleton:
            if report == True:
                print(cbone, "is an unknown bind data bone in SL")
            
        else:
            
            
            pbone = skel.avatar_skeleton[cbone]['parent']

        
        if pbone == "":
            if report == True:
                print("collada::get_matrices : found root:", cbone)
            pmat = mathutils.Matrix()
            pmati = pmat.inverted()
            real_data[cbone] = pmati.inverted() @ cmati
            continue
        else:
            
            
            
            
            if pbone not in transforms['bind_data']:
                if report == True:
                    print("collada::get_matrices : from file", file)
                    print(" - No bind data for parent", pbone)
                if armature != None:
                    if report == True:
                        print(" - Skipping extrapolation, armature provided:", armObj.name)
                    continue

                if 1 == 0:
                    
                    if pbone not in transforms['bone_data']:
                        if report == True:
                            print(pbone, "is a parent of", cbone, "and requires a joint matrix but doesn't exist.")
                            print("This is probably a dae error, skipping.")
                        continue
                else:
                    
                    
                    if report == True:
                        print("parent", pbone, "for", cbone, "is missing, using broken data instead")
                    if pbone not in transforms['bone_data']:
                        if report == True:
                            print("Fallback broken parent data is missing as well, using identity instead")
                    else:
                        real_data[cbone] = transforms['bone_data'][pbone]
                continue
            
            pmatb = transforms['bind_data'][pbone]
            pmati = pmatb.inverted()
            MJF = pmati.inverted() @ cmati
            real_data[cbone] = MJF
            continue

    transforms['real_data'] = real_data

    
    
    
    
    base_mats = devkit.get_matrices(base=base) 
    for bone in base_mats['bone_data']:
        if bone not in transforms['bone_data']:
            print("collada::get_matrices filling missing bone_data", bone)
            transforms['bone_data'][bone] = base_mats['bone_data'][bone]
        if bone not in transforms['real_data']:
            print("collada::get_matrices filling missing real_data", bone)
            transforms['real_data'][bone] = base_mats['real_data'][bone]

    return transforms
























def build_dae_matrices(armature=None, base="female_neutral", report=False):
    armObj = armature

    
    
    
    
    
    

    
    base_rig = getattr(base_data, base)
    R90 = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Z')
    R90I = R90.inverted()
    
    
    
    dae = {}
    dae['bind_data'] = {}
    dae['bone_data'] = {}
    
    dae['real_data'] = {}
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

    if armObj == None:
        
        
        
        txt = "collada::build_dae_matrices : no armature, will use " + base + " entirely"

        return dae

    else:
        txt = "collada::build_dae_matrices : armature provided, will fill missing with " + base
    print(txt)

    
    if isinstance(armature, str):
        armObj = bpy.data.objects[armature]

    R90 = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Z')
    R90I = R90.inverted()

    

    
    
    
    

    
    
    
    

    
    
    
    
    

    
    
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

    
    
    
    base_rig = getattr(base_data, base)

    
    

    
    
    base_matrices = {}
    for bone in base_rig:
        mb = mathutils.Matrix(base_rig[bone]['matrix_local'])
        base_matrices[bone] = mb

    
    
    
    
    
    
    
    
    
    matrices = {}
    for bone in skel.avatar_skeleton:
        if bone not in bone_rev:
            ml = base_matrices[bone]
        else:
            sbone = bone_rev[bone]
            ml = armObj.data.bones[sbone].matrix_local.copy()
        matrices[bone] = ml

    
    
    for bone in base_matrices:
        if bone not in matrices:
            base_matrices[bone] = base_matrices[bone]

    
    
    
    
    
    
    
    
    
    

    
    
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
        l = matrices[bone].to_translation()
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

    
    
    for bone in skel.avatar_skeleton:
        
        if bone.startswith("mSpine"):
            print("Found spine:", bone)
            bone_dup = globals.spine_chain[bone]
            if bone_dup not in dae['bone_data']:
                print("Spine bone", bone_dup, "not in dae joints, skipping")
                continue
            ml = dae[bone_dup]
            print(ml)
            dae['bone_data'][bone] = ml
            dae['real_data'][bone] = ml

    return dae


























def fill_matrices(armature=None, base=None, matrices=None):
    armObj = armature
    if armObj != None:
        if isinstance(armature, str):
            armObj = bpy.data.objects[armature]
    
    if base == None:
        base_rig = getattr(real_rig_data, "female_neutra") 
    else:
        base_rig = getattr(base_data, base)






























