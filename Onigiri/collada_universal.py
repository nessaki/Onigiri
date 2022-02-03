



import bpy
import math
import mathutils
import traceback

from . import pill
from . import rigutils

from .presets import volumes
from .presets import skeleton as skel

from .presets import bind_data





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























def write_collada(armature="", root="", write=False, file_in="", file_out=""):
    print("Entering write_collada with: armature/root/write/file_in/file_out")
    print("armature:", armature)
    print("root:", root)
    print("write:", write)
    print("file_in:", file_in)
    print("file_out:", file_out)

    
    
    
    
    
    
    
    
    
    

    
    
    write_nodes = True

    armObj = bpy.data.objects[armature]

    
    
    
    
    
    

    
    rig_type = armObj.get('rig_type', 'pivot')
    
    
    print("Checking for old unusable rig type...")
    if armObj.get('rig_type') == "N/A": 
        rig_type = "pivot"
        print("found N/A, changed to pivot")

    
    
    if armObj.get('rig_data') == None:
        print("collada_universal::write_collada reports: Armature has no base rig data, using saved data.")
        
        rig_data = bind_data.rig_data
    else:
        print("collada_universal::write_collada reports: rig_data pulled from armature")
        rig_data = armObj['rig_data'].to_dict()

    
    
    
    
    
    
    transforms = rigutils.get_bone_transforms(armature=armature, rig_data=rig_data)

    ccp = bpy.context.window_manager.cc_props
    bb_mesh = bpy.context.scene.bb_mesh

    
    if 1 == 0:
        use_rig_data = bb_mesh.use_rig_data
        use_bind_data = bb_mesh.use_bind_data
        process_volume_bones = bb_mesh.process_volume_bones
        rotate_for_sl = bb_mesh.rotate_for_sl

        

        
        
        
        
        
        
        
        
        

        
        
        use_offset_volume = bb_mesh.use_offset_volume
        
        
        use_offset_location = bb_mesh.use_offset_location
        
        use_offset_rotation = bb_mesh.use_offset_rotation
        
        
        
        
        use_offset_scale = bb_mesh.use_offset_scale



    
    
    
    
    
    
    bind_pose = {}
    joint_pose = {}

    
    

    
    
    
    

    print("Running universal exporter")

    for pBone in armObj.pose.bones:
        dBone = pBone.bone
        bone = pBone.name

        
        
        if bone not in skel.avatar_skeleton:
            print("Found incompatible bone for SL, skipping", bone)
            continue

        joint_pose[bone] = transforms[bone]['local']['matrix']
        bind_pose[bone] = transforms[bone]['bind_data']

    

    
    
    pretty_mats = True

    
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

                        for i in range(len(names)):
                            joint_total += 1
                            text_mat = list()
                            bone = names[i]
                            m = bind_pose[bone]

                            
                            
                            
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

                        
                        
                        Name_array.set('count', str(joint_total))
                        float_array.set('count', str(float_total))
                        Name_array_accessor_count.set('count', str(joint_total))
                        float_array_accessor_count.set('count', str(joint_total))

                        data.text = "".join(matrices)
                        del matrices


    
    
    if write_nodes == True:
        for node in root.iter(f'{n}node'):
            if node.get('type') == "JOINT":
                matrix = node.find(f'{n}matrix')
                if node.attrib.get('name') != None:
                    bone = node.attrib['name']

                    
                    

                    if bone in joint_pose:
                        tmat = pill.matrix_to_text(joint_pose[bone])
                        matrix.text = " ".join(tmat)
                    else:
                        print(":library_visual_scene - missing bone, this should never happen", bone)

    
    
    
    if pretty_mats == True:
        pretty_nodes(root=root)

    tree.write(file_out,
        xml_declaration = True,
        encoding = 'utf-8',
        method = 'xml'
        )

    return True





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





def to_deg(mat):
    eu = mat.to_euler()
    return [math.degrees(round(a, 4)) for a in eu]




