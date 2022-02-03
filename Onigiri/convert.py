
import os
import sys
import mathutils
import xml.etree.ElementTree as ET
from .presets import avatar_skeleton as skel
from .presets import matrices as dae_data






































def import_dae_kit(file_in=None, file_out=None, rebuild=False):

    
    
    






























    
    
    
    
    
    

    ET.register_namespace('',"http://www.collada.org/2005/11/COLLADASchema")
    tree = ET.parse(file_in)
    root = tree.getroot()
    n = '{http://www.collada.org/2005/11/COLLADASchema}'

    controller = {}
    skin = {}
    names = list()
    matrices = list()

    
    
    
    
    
    
    
    
    

    if 1 == 0:
        joints = set()
        lcon = root.find(f'{n}library_controllers')
        for c in lcon:
            skin = c.find(f'{n}skin')
            for skin_child in skin:
                for data in skin_child:
                    if data.tag == n + "Name_array":
                        names = data.text.split()
                        for n in names:
                            joints.add(n)
        
        for node in root.iter(f'{n}node'):
            if node.get('type') == "JOINT":
                if node.attrib.get('name') != None:
                    bone = node.attrib['name']
                joints.add(bone)
    

    
    
    bind_matrix = dict()

    
    
    
    
    
    
    transforms = {}
    transforms['bind_pose'] = {}
    transforms['joint_pose'] = {}

    lc = root.find(f'{n}library_controllers')
    for c in lc:
        cid = c.get('id')
        name = c.get('name')

        
        cname = name

        
        controller[cid] = {}
        controller[cid]['name'] = name

        skin = c.find(f'{n}skin')

        
        
        
        
        
        
        
        for skin_child in skin:
            for data in skin_child:
                if data.tag == n + "Name_array":
                    names = data.text.split()
                if data.tag == n + "float_array":
                    
                    param = skin_child.find(f'{n}technique_common/{n}accessor/{n}param')
                    
                    if param.get('type') == "float4x4":
                        

                        
                        
                        matrices = [float(i) for i in data.text.split()]
                        
                        
                        
                        controller[cid]['bones'] = names
                        controller[cid]['matrices'] = matrices

                        
                        block = 0
                        for i in range(len(names)):
                            bone = names[i]
                            mat = matrices[block:block+16]
                            block+= 16
                            
                            M = mathutils.Matrix()
                            for c in range(4):
                                for r in range(4):
                                    M[c][r] = mat[ r + (c*4) ]
                            
                            
                            
                            
                            
                            
                            
                            
                            M = matrix_from_list(mat)
                            MI = M.inverted()
                            
                            
                            
                            
                            
                            bind_matrix[bone] = MI 

    
    transforms['bind_pose'] = bind_matrix

    
    
    
    
    

    for node in root.iter(f'{n}contributor'):
        creator = node.find(f'{n}author')
        version = node.find(f'{n}authoring_tool')
    print("creator:", creator.text)
    print("version:", version.text)
    creator.text = "Bento Buddy Associate"
    version.text = "Bento Buddy Kit Converter v2.1"

    
    

    
    
    
    
    

    
    
    old_matrix = {}

    
    for node in root.iter(f'{n}node'):
        if node.get('type') == "JOINT":
            if node.attrib.get('name') != None:
                bone = node.attrib['name']
                matrix = node.find(f'{n}matrix')
                LT = matrix.text.split()
                MF = [float(f) for f in LT]
                M = matrix_from_list(MF)
                
                old_matrix[bone] = M

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    old_joints = {}
    for node in root.iter(f'{n}node'):
        if node.get('type') == "JOINT":
            matrix = node.find(f'{n}matrix')
            if node.attrib.get('name') != None:
                bone = node.attrib['name']
                mat_text_list = matrix.text.split()
                mat_float_list = [float(m) for m in mat_text_list]
                old_joints[bone] = matrix_from_list(mat_float_list)

    if 1 == 0:
        print("----------------------------------------------")
        print("old_joints:", old_joints)
        print("----------------------------------------------")

    
    
    

    
    for scene in root.iter(f'{n}visual_scene'):
        print("Removing old nodes -> visual_scene:", scene.tag)
        for node in scene.findall(f'{n}node'):
            scene.remove(node)


    
    
    
    

    

    
    
    
    skel_ = skel.avatar_skeleton
    node_p = scene
    first_in = True
    second = False
    third = False

    
    
    
    
    
    
    
    

    
    mt  = "1 0 0 0 "
    mt += "0 1 0 0 "
    mt += "0 0 1 0 "
    mt += "0 0 0 1"

    
    base_root = cname 
    if 1 == 0:
        node = ET.SubElement(scene, "node")
        
        
        node.set("id", cname)
        node.set("name", cname)
        node.set("type", 'NODE')
        mat = ET.SubElement(node, "matrix")
        mat.text = mt


    
    
    
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

    
    
    
    
    rig_class = "pos"

    if rig_class == "pos":
        class_data = dae_data.pos
    if rig_class == "default":
        class_data = dae_data.default
    if rig_class == "neutral":
        class_data = dae_data.neutral
    if rig_class == "default_male":
        class_data = dae_data.default_male
    if rig_class == "neutral_male":
        class_data = dae_data.neutral_male

    ele = {} 

    
    
    

    
    
    
    
    if 1 == 0:
        for bone in joints:
            if bone not in skel_:
                print("Missing bone, this doesn't appear to be compatible with SL:", bone)
                continue
    for bone in skel_:
        parent = skel_[bone]['parent']
        
        if parent == "":
            node = ET.SubElement(scene, "node")
            ele[bone] = node
        
        else:
            parent = skel_[bone]['parent']
            p_node = ele[parent]
            node = ET.SubElement(p_node, "node")
            ele[bone] = node

        node.set("id", bone)
        node.set("name", bone)
        node.set("sid", bone)
        node.set("type", 'JOINT')
        matrix_node = ET.SubElement(node, "matrix")

        
            
            


        
        
        
        
        if bone not in bind_matrix:
            if bone in old_joints:
                MF = old_joints[bone]
            else:
                MF = matrix_from_list(class_data['joint'][bone])
            
            mt = matrix_to_string(MF)
            matrix_node.text = mt
            matrix_node.set("sid", 'transform')
            
            transforms['joint_pose'][bone] = MF
            continue

        
        
        
        
        
        


        
        
        
        
        
        
        
        if parent == "":
            if bone in old_joints:
                MF = old_joints[bone]
            else:
                MF = matrix_from_list(class_data['joint'][bone])

            mt = matrix_to_string(MF)
            matrix_node.text = mt
            matrix_node.set("sid", 'transform')
            
            transforms['joint_pose'][bone] = MF
            continue

        
        
        
        
        
        
        
        
        

        cmat = matrix_from_list(class_data['bind'][bone]) 
        if bone in bind_matrix:
            cmat = bind_matrix[bone]
        if bone in old_joints:
            cmat = old_joints[bone]

        mat = matrix_from_list(class_data['bind'][parent]) 

        
        
        
        

        
        has_bind = False
        has_old = False

        if parent in bind_matrix:
            has_bind = True
            bmat = bind_matrix[parent] 
            pmat = bmat
        if parent in old_joints:
            has_old = True
            omat = old_joints[parent] 
            pmat = omat

        
        
        
        if has_bind == True:
            MF = bmat.inverted() @ cmat
        elif has_old == True:
            MF = omat.inverted() @ cmat
        else:
            MF = mat.inverted() @ cmat

        
        
        
        
        

        
        
        


        
        
        
        
        
        
        



        
        
        

        mt = matrix_to_string(MF)
        matrix_node.text = mt
        matrix_node.set("sid", 'transform')

        
        transforms['joint_pose'][bone] = MF

        if bone == 'mShoulderRight':
            print("Matrix result from convert.py:")
            print(MF)


    tree.write(file_out,
        xml_declaration = True,
        encoding = 'utf-8',
        method = 'xml'
        )

    print("file saved:", file_out)
    print("Converting to pretty")
    from . import collada
    collada.pretty_dae(file_in=file_out, file_out=file_out)
    return transforms

    
    
    



def matrix_from_list(l):
    M = mathutils.Matrix()
    for c in range(4):
        for r in range(4):
            M[c][r] = l[ r + (c*4) ]
    return M
def matrix_to_list(m):
    l = list(m)
    lt = list()
    for v in l:
        
        t = tuple([a for a in v])
        lt.append(t)
    
    return lt
def matrix_to_string(mat):
    tmat = list()
    for v in mat:
        for n in v:
            tmat.append(f"{n:.6f}")
    txt = " ".join(tmat)
    return txt
def vector_to_list(v):
    l = [a for a in v]
    return l
