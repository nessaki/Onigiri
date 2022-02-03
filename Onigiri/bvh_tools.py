import re
import os 
import bpy
import math
import mathutils
import traceback
import xml.etree.ElementTree as ET
from xml.dom import minidom

from . import bvh
from . import rigutils
from .presets import volumes
from .presets import skeleton as skel
from . import pill
from . import curves

def read(doc=None, sl_only=True, export_volumes=True, mark_tol=True, rot_tol=0.0001, loc_tol=0.00001):

    bba = bpy.context.scene.bb_anim_props

    if doc == None:
        print("bvh_tools::read reports: no xml, I need an xml object from ElementTree")
        return False

    root = doc.getroot()

    motion = root.find('MOTION')
    frames = int(motion.find('FRAMES').text)
    frame_time = float(motion.find('FRAME_TIME').text)
    motion_data = motion.find('MOTION_DATA').text.split()

    compose = dict()

    for node in root.iter(f'JOINT'):
        bone = node.find('NAME').text
        offsets = node.find('OFFSET').text
        channels = int(node.find('CHANNEL_COUNT').text)
        compose[bone] = {}
        compose[bone]['offsets'] = offsets
        compose[bone]['channels'] = channels

    count = 0

    pointer = 0 

    data = {}
    data['joints'] = {}
    data['frames'] = frames
    data['frame_time'] = frame_time

    for f in range(frames):
        for bone in compose:
            chans = compose[bone]['channels']

            if bone in volumes.vol_joints:
                if export_volumes == False:
                    pointer += chans
                    continue
            if sl_only == True:
                if bone not in skel.avatar_skeleton:
                    pointer += chans
                    continue
 
            try:
                bone_exists = data ['joints'][bone]
            except:
                data['joints'][bone] = {}
                data['joints'][bone]['loc'] = []
                data['joints'][bone]['rot'] = []

            if chans == 3:
                
                rots = [ float(item) for item in motion_data[pointer:pointer+3] ]

                if bone in volumes.vol_joints:
                    rots_new = list(skel.avatar_skeleton[bone]['rot'])
                    rots = rots[0] + rots_new[0], rots[1] + rots_new[1], rots[2] + rots_new[2]

                data['joints'][bone]['rot'].append(tuple(rots))

            elif chans == 6:
                
                locs = [ float(item) for item in motion_data[pointer:pointer+3] ]

                if bone == "mPelvis" or bone == "hip":
                    offset_string = compose[bone]['offsets'].split()
                    offset_floats = [ float(item) for item in offset_string ]
                    locs = offset_floats[0] - locs[0], offset_floats[1] - locs[1], offset_floats[2] - locs[2]
                    
                if bone in volumes.vol_joints:
                    offset_string = compose[bone]['offsets'].split()
                    offset_floats = [ float(item) for item in offset_string ]

                    pos = skel.avatar_skeleton[bone]['pos']
                    end = skel.avatar_skeleton[bone]['end']

                    if 1 == 0:
                        armObj = bpy.context.object
                        matrix_offset = armObj.pose.bones[bone].matrix_channel @ armObj.pose.bones[bone].parent.matrix_channel.inverted()
                        x,y,z = matrix_offset.to_translation()
                        locx = (locs[0] - x)
                        locy = (locs[1] - y)
                        locz = (locs[2] - z)
                        locs = tuple((locx, locy, locz))

                bone_lower = bone.lower()
                if bone_lower == 'mpelvis' or bone == 'hip' or bone == 'hips':
                    if bba.disable_pelvis_location_animation == False:
                        data['joints'][bone]['loc'].append(tuple(locs))
                else:
                    data['joints'][bone]['loc'].append(tuple(locs))

                rots = [ float(item) for item in motion_data[pointer+3:pointer+6] ]

                if bone in volumes.vol_joints:
                    rots_new = list(skel.avatar_skeleton[bone]['rot'])
                    rots = rots[0] + rots_new[0], rots[1] + rots_new[1], rots[2] + rots_new[2]

                data['joints'][bone]['rot'].append(tuple(rots))

            else:
                print("FATAL ERROR!: bvh_tools::read - channels returns wrong amount", str(chans))
                return False
            
            pointer += chans

    bba = bpy.context.scene.onigiri
    armObj = bpy.context.object
    anim_start_frame = bba.animation_start_frame
    anim_end_frame = bba.animation_end_frame

    armrot = pill.rotate_matrix(armObj.matrix_world, [0,0,90])

    rig_class = armObj.get('rig_class')

    test_vbones = False
    if test_vbones == True:
        path = ".presets/posture.py"
        sd = os.path.dirname(os.path.abspath(__file__))
        path = sd + "/presets/posture.py"
        posture = dict()
        try:
            namespace = {}
            exec(open(path, 'r', encoding='UTF8').read(), namespace)
            print("LOADED: posture data")
        except Exception as e:
            print(traceback.format_exc())
            return None
        try:
            posture.update(namespace['pos'])
        except:
            print("no pos dictionary, nothing to do")
            return False

    bpy.context.view_layer.update()

    bpy.context.view_layer.update()
    old_frame = bpy.context.scene.frame_current

    test_time = False
    if test_time == True:
        import time 
        rot_time_total = 0
        loc_time_total = 0
        time_frame_start = time.time()
        print("starting frames iter:", str(time_frame_start))

    use_storage = False
    if use_storage == True:
        matrix_storage = {}
        if test_time == True:
            
            set_frame_time_start = time.time()
        for f in range(anim_start_frame, anim_end_frame+1):
            bpy.context.scene.frame_set(f)
            matrix_storage[f] = {}

            for boneObj in armObj.data.bones:
                bone = boneObj.name
                matrix_storage[f][bone] = {}
                
                pbmat = armObj.pose.bones[bone].matrix.copy()
                dbmat = armObj.data.bones[bone].matrix.copy()
                dbmatl = armObj.data.bones[bone].matrix_local.copy()
                if armObj.pose.bones[bone].parent:
                    pbpmat = armObj.pose.bones[bone].parent.matrix.copy()
                    dbpmatl = armObj.data.bones[bone].parent.matrix_local.copy()
                else:
                    pbpmat = mathutils.Matrix()
                    dbpmatl = mathutils.Matrix()
                if armObj.pose.bones[bone].parent:
                    dbpmat = armObj.data.bones[bone].parent.matrix.copy()
                else:
                    dbpmat = mathutils.Matrix()
                pbmatI = pbmat.inverted()
                pbpmatI = pbpmat.inverted()
                dbpmatlI = dbpmatl.inverted()
                rp = pbpmat @ dbpmatlI @ dbmatl
                rp_composed = rp.inverted() @ pbmat
                
                m3 = dbmatl.to_3x3()
                m4 = m3.to_4x4()
                m4I = m4.inverted()
                mF = m4 @ rp_composed @ m4I
                
                matrix_storage[f][bone]['matrix_real'] = mF

    for f in range(anim_start_frame, anim_end_frame+1):
        bpy.context.scene.frame_set(f)

        for boneObj in armObj.data.bones:
            bone = boneObj.name

            if bone in volumes.vol_joints:
                if export_volumes == False:
                    continue

            if use_storage == True:
                matrix_real = matrix_storage[f][bone]['matrix_real']
            else:
                
                pbmat = armObj.pose.bones[bone].matrix.copy()
                dbmat = armObj.data.bones[bone].matrix.copy()
                dbmatl = armObj.data.bones[bone].matrix_local.copy()
                if armObj.pose.bones[bone].parent:
                    pbpmat = armObj.pose.bones[bone].parent.matrix.copy()
                    dbpmatl = armObj.data.bones[bone].parent.matrix_local.copy()
                else:
                    pbpmat = mathutils.Matrix()
                    dbpmatl = mathutils.Matrix()
                if armObj.pose.bones[bone].parent:
                    dbpmat = armObj.data.bones[bone].parent.matrix.copy()
                else:
                    dbpmat = mathutils.Matrix()
                pbmatI = pbmat.inverted()
                pbpmatI = pbpmat.inverted()
                dbpmatlI = dbpmatl.inverted()
                rp = pbpmat @ dbpmatlI @ dbmatl
                rp_composed = rp.inverted() @ pbmat
                
                m3 = dbmatl.to_3x3()
                m4 = m3.to_4x4()
                m4I = m4.inverted()
                mF = m4 @ rp_composed @ m4I
                
                matrix_real = mF

            try:
                DATA_FILLED = data['joints'][bone]['DATA_FILLED']
            except:
                data['joints'][bone]['DATA_FILLED'] = list() 
                data['joints'][bone]['rot_deg'] = list()
                
                data['joints'][bone]['quats'] = list() 
            
            if test_time == True:
                rot_time_0 = time.time()
                rot_time_1 = rot_time_0

            try:
                ROT_DATA = data['joints'][bone]['rot']
            except:
                ROT_DATA = False

            if ROT_DATA:

                deg = skel.avatar_skeleton[bone]['rot']
                rad = [math.radians(a) for a in deg]
                
                rot_offset = [-rad[1], -rad[0], -rad[2]]

                euler = mathutils.Euler(rot_offset, 'ZXY')
                mat3 = euler.to_matrix()
                ROTATION = mat3.to_4x4()

                quat = ( pill.Z90I @ matrix_real @ ROTATION @ pill.Z90 ).to_quaternion().normalized()

                x = round(quat.x, 6)
                y = round(quat.y, 6)
                z = round(quat.z, 6)

                data['joints'][bone]['quats'].append([x, y, z])

                euler_from_quat = quat.to_euler()

                degrees_from_euler = [math.degrees(a) for a in euler_from_quat]
                data['joints'][bone]['rot_deg'].append(degrees_from_euler)

                if test_time == True:
                    rot_time_1 = time.time()
                    rot_time_total += (rot_time_1-rot_time_0)

            if test_time == True:
                loc_time_0 = time.time()
                loc_time_1 = loc_time_0

            try:
                LOC_DATA = data['joints'][bone]['loc']
            except:
                LOC_DATA = False

            if LOC_DATA:

                if data['joints'][bone].get('loc_pose') == None:
                    data['joints'][bone]['loc_pose'] = list()

                LOCATION = matrix_real.to_translation()
                
                arm_scale = armObj.scale

                deg = skel.avatar_skeleton[bone]['rot']
                rad = [math.radians(a) for a in deg]
                
                rot_offset = [rad[1], rad[0], rad[2]]

                if bone in volumes.vol_joints:
                        vbs_x, vbs_y, vbs_z = [
                        volumes.vol_joints[bone]['scale'][1],
                        volumes.vol_joints[bone]['scale'][0],
                        volumes.vol_joints[bone]['scale'][2]
                        ]
                else:
                    
                    vbs_x, vbs_y, vbs_z = mathutils.Vector((0,0,0))

                bs_x, bs_y, bs_z = armObj.pose.bones[bone].scale

                if armObj.pose.bones[bone].parent:

                    cloc = armObj.data.bones[bone].matrix_local.to_translation()
                    ploc = armObj.data.bones[bone].parent.matrix_local.to_translation()
                    offset = mathutils.Vector((cloc - ploc))

                    if test_vbones == True:
                        
                        if bone in posture:
                            pos = posture[bone][rig_class]
                        else:
                            pos = [0,0,0] 

                        pos_off = mathutils.Vector((
                            pos[0],
                            pos[1],
                            pos[2]
                            ))
                        new_offset = offset + pos_off

                        offset = new_offset.copy()

                    LOCATION += offset 

                if 1 == 1:

                    ROTATION = mathutils.Euler(rot_offset,'ZYX').to_matrix().to_4x4()

                    scale_composed = list()
                    sc = scale_composed
                    sc.append( arm_scale[0]/(vbs_x + bs_x) )
                    sc.append( arm_scale[1]/(vbs_y + bs_y) )
                    sc.append( arm_scale[2]/(vbs_z + bs_z) )
                    SCALE = mathutils.Matrix()
                    SCALE[0][0] = sc[0]
                    SCALE[1][1] = sc[1]
                    SCALE[2][2] = sc[2]

                else:
                    ROTATION = mathutils.Euler(rot_offset,'ZYX').to_matrix().to_4x4()
                    SCALE = mathutils.Matrix()
                    for i in range(3):
                        SCALE[i][i] = 1

                loc = pill.Z90I @ SCALE @ ROTATION @ LOCATION

                data['joints'][bone]['loc_pose'].append( tuple((round(loc[0], 6), round(loc[1], 6), round(loc[2], 6))) )

                if test_time == True:
                    loc_time_1 = time.time()
                    loc_time_total += (loc_time_1-loc_time_0)

    if test_time == True:
        time_frame_end = time.time()
        time_frame_total = time_frame_end - time_frame_start
        print("end frames iter:", str(time_frame_total))
        print("Total rotation processing time:", str(rot_time_total))
        print("Total location processing time:", str(loc_time_total))

    bpy.context.scene.frame_set(old_frame)

    if 1 == 0:
        if armObj.animation_data != None:
            if armObj.animation_data.action != None:
                print("gathering interpolation data...")
                frame_data = curves.get_fcurve_data(armObj.name)

    print("marking unusable keys...")

    ce = close_enough

    for bone in data['joints']:

        data['joints'][bone]['tol'] = {}
        data['joints'][bone]['tol']['rot'] = list()
        data['joints'][bone]['tol']['loc'] = list()

        data['joints'][bone]['tol']['rot_last'] = list()
        data['joints'][bone]['tol']['loc_last'] = list()

        rot_count = 0 
        loc_count = 0

        ref_key = None

        for rots in data['joints'][bone]['rot']:
        
            x, y, z = rots
            if ref_key == None:
                ref_key = (x, y, z)
                
                data['joints'][bone]['tol']['rot'].append(False)
                continue
            else:
                
                if ce(x, ref_key[0], tol=rot_tol):
                    
                    if data['joints'][bone]['tol']['rot'][-1] == False:
                        data['joints'][bone]['tol']['rot'][-1] = True
                        rot_count += 1
                    data['joints'][bone]['tol']['rot'].append(True)
                    ref_key = (x,y,z)
                    rot_count += 1
                    continue
                if ce(y, ref_key[1], tol=rot_tol):
                    if data['joints'][bone]['tol']['rot'][-1] == False:
                        data['joints'][bone]['tol']['rot'][-1] = True
                        rot_count += 1
                    data['joints'][bone]['tol']['rot'].append(True)
                    ref_key = (x,y,z)
                    rot_count += 1
                    continue
                if ce(z, ref_key[2], tol=rot_tol):
                    if data['joints'][bone]['tol']['rot'][-1] == False:
                        data['joints'][bone]['tol']['rot'][-1] = True
                        rot_count += 1
                    data['joints'][bone]['tol']['rot'].append(True)
                    ref_key = (x,y,z)
                    rot_count += 1
                    continue
                data['joints'][bone]['tol']['rot'].append(False)

        data['joints'][bone]['tol']['rot_count'] = rot_count

        ref_key = None
        for locs in data['joints'][bone]['loc']:
            x, y, z = locs
            if ref_key == None:
                ref_key = (x, y, z)
                data['joints'][bone]['tol']['loc'].append(False)

                continue
            else:
                if ce(x, ref_key[0], tol=loc_tol):
                    if data['joints'][bone]['tol']['loc'][-1] == False:
                        data['joints'][bone]['tol']['loc'][-1] = True
                        loc_count += 1
                    data['joints'][bone]['tol']['loc'].append(True)
                    ref_key = (x,y,z)
                    loc_count += 1
                    continue
                if ce(y, ref_key[1], tol=loc_tol):
                    if data['joints'][bone]['tol']['loc'][-1] == False:
                        data['joints'][bone]['tol']['loc'][-1] = True
                        loc_count += 1
                    data['joints'][bone]['tol']['loc'].append(True)
                    ref_key = (x,y,z)
                    loc_count += 1
                    continue
                if ce(z, ref_key[2], tol=loc_tol):
                    if data['joints'][bone]['tol']['loc'][-1] == False:
                        data['joints'][bone]['tol']['loc'][-1] = True
                        loc_count += 1
                    data['joints'][bone]['tol']['loc'].append(True)
                    ref_key = (x,y,z)
                    loc_count += 1
                    continue
                data['joints'][bone]['tol']['loc'].append(False)

        data['joints'][bone]['tol']['loc_count'] = loc_count

        data['joints'][bone]['animated'] = (rot_count > 0 or loc_count > 0)

    if 1 == 0:
        jc = 0
        temp_j = list()
        for j in data['joints']:
            if data['joints'][j]['animated']:
                temp_j.append("\n")
                temp_j.append(j)
                jc += 1
        print("joints that passed tolerance test:", "".join(temp_j))
        print("animated bones:", str(jc))

    return data

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

def clean_xml(doc=None):
    pass

    return data

def compose_bvh_buffers(context=False, return_type="bvh", scale_factor="meters"):

    if scale_factor == "meters":
        scale = 1
    elif scale_factor == "inches":
        scale = 39.3701
    else:
        
        scale = scale_factor

    print("passing context to bvh writer, clean this up")
    if context == False:
            print("goofy did a boo")
            return False

    obj = bpy.data.objects
    bb = bpy.context.scene.onigiri
    bba = bpy.context.scene.bb_anim_props
    armObj = bpy.context.selected_objects[0]

    animation_scale = scale
    animation_fps = bb.animation_fps
    animation_start_frame = bb.animation_start_frame
    animation_end_frame = bb.animation_end_frame

    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    bpy.context.view_layer.objects.active = armObj

    loc, rot, scale = armObj.matrix_world.decompose()
    smat = mathutils.Matrix()
    for i in range(3):
        smat[i][i] = scale[i]

    eu = mathutils.Euler(map(math.radians, (-90, 0, 0)), 'XYZ')
    mat = mathutils.Matrix.Translation(loc) @ eu.to_matrix().to_4x4() @ smat
    armObj.matrix_world = mat

    bpy.ops.object.transform_apply( rotation=True, location=False, scale=False )

    mbones_buf = bvh.save(
        context=context,
        filepath="", 
        global_scale=animation_scale,
        frame_start=animation_start_frame,
        frame_end=animation_end_frame,
        rotate_mode='NATIVE',
        root_transform_only=bba.disable_location_offsets,
        buffer=True,
        )

    armObj.matrix_world = mat.inverted()
    bpy.ops.object.transform_apply( rotation=True, location=False, scale=False )

    eu = mathutils.Euler(map(math.radians, (0, 0, 90)), 'XYZ')
    mat = mathutils.Matrix.Translation(loc) @ eu.to_matrix().to_4x4() @ smat
    armObj.matrix_world = mat
    bpy.ops.object.transform_apply( rotation=True, location=False, scale=False )
    vbones_buf = bvh.save(
        context=context,
        filepath="", 
        global_scale=animation_scale,
        frame_start=animation_start_frame,
        frame_end=animation_end_frame,
        rotate_mode='NATIVE',
        root_transform_only=bba.disable_location_offsets,
        buffer=True,
        )

    eu = mathutils.Euler(map(math.radians, (0, 0, -90)), 'XYZ')
    mat = mathutils.Matrix.Translation(loc) @ eu.to_matrix().to_4x4() @ smat
    armObj.matrix_world = mat
    bpy.ops.object.transform_apply( rotation=True, location=False, scale=False )

    buf = merge(
        vbones=vbones_buf,
        mbones=mbones_buf,
        swap_offsets=False,
        swap_endsites=False,
        swap_motion=True,
        return_type=return_type,
        buffer=True,
    )
    
    return buf

def merge(
    vbones="",
    mbones="",
    swap_offsets=False,
    swap_endsites=False,
    swap_motion=False,
    use_translations=True,
    return_type="bvh",
    buffer=False
    ):

    if buffer == True:
        print("Buffers instead of files...")

    if buffer == True:
        print("Pulling vbones data from buffer...")
        buf = to_xml(vbones)
    else:
        print("Merging", vbones, "with", mbones)
        try:
            vb = open(vbones, "r", encoding='UTF8')
        except:
            print("Couldn't open file:", vbones)
            return False
        try:
            mb = open(mbones, "r", encoding='UTF8')
        except:
            vb.close()
            print("Couldn't open file:", mbones)
            return False

        buf = vb.read()
        vb.close()
        buf = to_xml(buf)

    tree = ET.ElementTree(ET.fromstring(buf))
    root = tree.getroot()

    vjoints = {}

    for node in root.iter(f'JOINT'):
        name = node.find('NAME').text
        vjoints[name] = {}

        vjoints[name]['offset'] = node.find('OFFSET').text
        vjoints[name]['channel_count'] = int(node.find('CHANNEL_COUNT').text)
        endsite = node.find('END_SITE')
        if endsite:
            
            vjoints[name]['end_site'] = endsite.find('OFFSET').text

    vdata = {}
    motion = root.find(f'MOTION')
    vdata['frames'] = motion.find('FRAMES').text
    vdata['frame_time'] = motion.find('FRAME_TIME').text
    
    vdata['motion_data'] = motion.find('MOTION_DATA').text.split()

    if buffer == True:
        print("Pulling mbones data from buffer...")
        buf = to_xml(mbones)
    else:
        buf = mb.read()
        mb.close()
        buf = to_xml(buf)

    tree = ET.ElementTree(ET.fromstring(buf))
    root = tree.getroot()

    if swap_offsets == True or swap_endsites == True:
        
        for node in root.iter(f'JOINT'):
            name = node.find('NAME').text
            if name in volumes.vol_joints:
                if swap_offsets == True:
                    offset = node.find('OFFSET')
                    offset.text = vjoints[name]['offset']
                if swap_endsites == True:
                    endsite = node.find('END_SITE')
                    if endsite:
                        endsite_offset = endsite.find('OFFSET')
                        endsite_offset.text = vjoints[name]['end_site']

    if swap_motion == True:
        mdata = {}
        motion = root.find(f'MOTION')
        mdata['frames'] = motion.find('FRAMES').text

        frames = int(mdata['frames'])

        mdata['frame_time'] = motion.find('FRAME_TIME').text

        motion_data = motion.find('MOTION_DATA')
        mdata['motion_data'] = motion_data.text.split()

        slot = 0
        for f in range(frames):
            for node in root.iter(f'JOINT'):
                name = node.find('NAME').text
                chans = int(vjoints[name]['channel_count'])
                if name in volumes.vol_joints:
                    for float in range(slot, slot+chans):
                        mdata['motion_data'][float] = vdata['motion_data'][float]
                
                slot += chans

        motion_data.text = " ".join(mdata['motion_data'])

    buf = ET.tostring(root, encoding='unicode')

    if return_type == "object":
        return tree

    elif return_type == "string":
        return buf

    elif return_type == "bvh":
        buf = from_xml(buf)
        return buf

    print("bvh_tools::merge reports no return type, defaulting to bvh")
    return buf

def to_xml(buf="", return_type="string"):
    if buf == "":
        print("nothing to do")
        return False

    mocap = Bvh(buf)

    m = re.search(r'ROOT (.*?)\n{\s*OFFSET\s(.*?)\n.*?CHANNELS\s(\d)\s(.*?)\n', buf, re.DOTALL)

    if not m:
        print("this is probably not a bvh formatted text, nothing I can do")
        return False

    root_name = m.group(1)
    root_offset = m.group(2)
    root_channel_count = m.group(3)
    root_channels = m.group(4)

    joints = {}

    joints[root_name] = [root_offset, root_channel_count, root_channels]

    matches = re.findall(r'JOINT (.*?)\n\s+{\s+OFFSET\s(.*?)\s+CHANNELS\s(\d)\s(.*?)\n', buf, re.DOTALL)

    for m in matches:
        j = m[0]
        joints[j] = list()
        joints[j].append(m[1])
        joints[j].append(m[2])
        joints[j].append(m[3])

    joint_junk = mocap.joint_direct_children(root_name)
    joint_children = {}
    joint_children[root_name] = list()
    for c in joint_junk:
        joint_children[root_name].append(c.name)

    for j in joints:
        joint_children[j] = []
        joint_junk = mocap.joint_direct_children(j)
        for c in joint_junk:
            
            joint_children[j].append(c.name)
    del joint_junk

    endsites = {}
    for j in joint_children:
        children = joint_children[j]
        if len(children) == 0:
            m = re.search(rf'JOINT {j}\n.+?End Site\n.+?OFFSET (.+?)\n', buf, re.DOTALL)
            if m:
                endsites[j] = m[1]
            else:
                print("expected an End Site from joint", j, "but got nothing")

    matches = re.search(r'}\nMOTION\nFrames: (.*?)\nFrame Time: (.*?)\n(.*?)$', buf, re.DOTALL)

    if matches:
        pass
    else:
        print("something went wrong when parsing motions")
        return False

    frames = matches.group(1)
    frame_time = matches.group(2)
    frame_data = matches.group(3).split()
    motion_data = [' '.join(frame_data[i:i+3]) for i in range(0,len(frame_data),3)]

    del frame_data
    
    def walk_tree(bone=None, node=None):
        name_tag = ET.SubElement(node, 'NAME')
        name_tag.text = bone
        offset_tag = ET.SubElement(node, 'OFFSET')
        offset_tag.text = joints[bone][0]
        channel_count_tag = ET.SubElement(node, 'CHANNEL_COUNT')
        channel_count_tag.text = joints[bone][1]
        channels_tag = ET.SubElement(node, 'CHANNELS')
        channels_tag.text = joints[bone][2]

        children = joint_children[bone]

        if len(children) == 0:
            end_tag = ET.SubElement(node, 'END_SITE')
            end_offset_tag = ET.SubElement(end_tag, 'OFFSET')
            end_offset_tag.text = endsites[bone]
        else:
            for c in children:
                child_tag = ET.SubElement(node, 'JOINT')
                walk_tree(bone=c, node=child_tag)

        return True

    root_tag = ET.Element('ROOT')
    joint_tag = ET.SubElement(root_tag, 'JOINT')
    walk_tree(bone=root_name, node=joint_tag)

    motion_tag = ET.SubElement(root_tag, 'MOTION')
    frames_tag = ET.SubElement(motion_tag, 'FRAMES')
    frames_tag.text = frames
    frame_time_tag = ET.SubElement(motion_tag, 'FRAME_TIME')
    frame_time_tag.text = frame_time

    frame_data = " ".join(motion_data)

    motion_data_tag = ET.SubElement(motion_tag, 'MOTION_DATA')
    motion_data_tag.text = frame_data

    if return_type == "object":
        tree=ET.ElementTree(root_tag)
        return tree

    elif return_type == "string":
        
        buf = minidom.parseString(ET.tostring(root_tag)).toprettyxml(indent="\t")

    return buf

def from_xml(buf=""):
    if buf == "":
        print("Nothing to do ")
        return False
    
    buf = re.sub('\s+(?=<)', '', buf)
    tree = ET.ElementTree(ET.fromstring(buf))
    root = tree.getroot()

    data = {}
    data['joints'] = {}

    joint = root.find('JOINT')
    name = joint.find('NAME')

    offset = joint.find('OFFSET')
    channel_count = joint.find('CHANNEL_COUNT')
    channels = joint.find('CHANNELS')

    data['joints'][name.text] = {}
    data['joints'][name.text]['offset'] = offset.text
    data['joints'][name.text]['channel_count'] = channel_count.text
    data['joints'][name.text]['channels'] = channels.text

    end_site = joint.find('END_SITE')
    if end_site:
        end_site_float = end_site.find('OFFSET')
        data['joints'][name.text]['end_site'] = end_site_float.text
    else:
        data['joints'][name.text]['end_site'] = None

    root.remove(joint)
    root.extend(joint)

    buf = minidom.parseString(ET.tostring(root)).toprettyxml(indent="\t")

    buffer = [
        "HIERARCHY\n", "ROOT ", name.text, "\n{\n", "\tOFFSET ",
        offset.text, "\n\tCHANNELS ", channel_count.text, " ", channels.text, "\n"]

    for node in joint.iter('JOINT'):
        name = node.find('NAME')

        offset = node.find('OFFSET')
        channel_count = node.find('CHANNEL_COUNT')
        channels = node.find('CHANNELS')
        data['joints'][name.text] = {}
        data['joints'][name.text]['offset'] = offset.text
        data['joints'][name.text]['channel_count'] = channel_count.text
        data['joints'][name.text]['channels'] = channels.text

        end_site = node.find('END_SITE')
        if end_site:
            end_site_float = end_site.find('OFFSET')
            data['joints'][name.text]['end_site'] = end_site_float.text
        else:
            data['joints'][name.text]['end_site'] = None

    segments = list() 

    name_segs = re.findall(r'(\t+<JOINT>\s+<NAME>.*?</NAME>)', buf, re.DOTALL)
    for seg in name_segs:
        tup = re.search(r'(\t+)<JOINT>\s+<NAME>(.*?)</NAME>', seg, re.DOTALL)
        tabs = tup.group(1) 
        name = tup.group(2) 

        if data['joints'][name]['end_site'] != None:
            endsite =                tabs + "\t" + "End Site\n" + tabs + "\t" + "{\n" + tabs + "\t\t" + "OFFSET " +                data['joints'][name]['end_site'] + "\n" + tabs + "\t" + "}\n"
        else:
            endsite = ""
        segments.append("".join([
            tabs, 'JOINT ', name, "\n", tabs, "{\n",
            tabs, "\t", "OFFSET ", data['joints'][name]['offset'], "\n",
            tabs, "\t", "CHANNELS ", data['joints'][name]['channel_count'],
            " ", data['joints'][name]['channels'], "\n", endsite
            ]))

    joint_tags = re.findall(r'(</?JOINT>)', buf, re.DOTALL)
    joint_tabs = re.findall(r'(\t+)</?JOINT>', buf, re.DOTALL)

    seg_count = 0 
    for i in range(len(joint_tags)):
        if joint_tags[i] == "<JOINT>":
            buffer.append(segments[seg_count])
            seg_count += 1
        elif joint_tags[i] == "</JOINT>":
            buffer.extend([joint_tabs[i], "}\n"])
        else:
            print("tag out of range:", joint_tags[i])
    
    buffer.append("}\n")

    motion = list()
    frames = root.find(f'./MOTION/FRAMES')
    frame_time = root.find(f'./MOTION/FRAME_TIME')
    motion_data = root.find(f'./MOTION/MOTION_DATA')

    motion_list = motion_data.text.split()

    frame_count = int(frames.text) 
    float_count = len(motion_list)
    per_frame = int( float_count / frame_count ) 

    buffer.extend(["MOTION\n", "Frames: ", frames.text, "\n", "Frame Time: ", frame_time.text, "\n"])

    frames = list()
    for i in range(0, float_count, per_frame):
        buffer.append(" ".join(motion_list[i:i+per_frame]))
        
        buffer.append(" \n")

    bvh_buf = "".join(buffer)

    return bvh_buf

'''
# MIT License
#
# Copyright (c) 2017 20tab srl
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# This program has been altered from its original form, it has been formatted to fit your spleen.
'''
class BvhNode:

    def __init__(self, value=[], parent=None):
        self.value = value
        self.children = []
        self.parent = parent
        if self.parent:
            self.parent.add_child(self)

    def add_child(self, item):
        item.parent = self
        self.children.append(item)

    def filter(self, key):
        for child in self.children:
            if child.value[0] == key:
                yield child

    def __iter__(self):
        for child in self.children:
            yield child

    def __getitem__(self, key):
        for child in self.children:
            for index, item in enumerate(child.value):
                if item == key:
                    if index + 1 >= len(child.value):
                        return None
                    else:
                        return child.value[index + 1:]
        raise IndexError('key {} not found'.format(key))

    def __repr__(self):
        return str(' '.join(self.value))

    @property
    def name(self):
        return self.value[1]

class Bvh:

    def __init__(self, data):
        self.data = data
        self.root = BvhNode()
        self.frames = []
        self.tokenize()

    def tokenize(self):
        first_round = []
        accumulator = ''
        for char in self.data:
            if char not in ('\n', '\r'):
                accumulator += char
            elif accumulator:
                    first_round.append(re.split('\\s+', accumulator.strip()))
                    accumulator = ''
        node_stack = [self.root]
        frame_time_found = False
        node = None
        for item in first_round:
            if frame_time_found:
                self.frames.append(item)
                continue
            key = item[0]
            if key == '{':
                node_stack.append(node)
            elif key == '}':
                node_stack.pop()
            else:
                node = BvhNode(item)
                node_stack[-1].add_child(node)
            if item[0] == 'Frame' and item[1] == 'Time:':
                frame_time_found = True

    def search(self, *items):
        found_nodes = []

        def check_children(node):
            if len(node.value) >= len(items):
                failed = False
                for index, item in enumerate(items):
                    if node.value[index] != item:
                        failed = True
                        break
                if not failed:
                    found_nodes.append(node)
            for child in node:
                check_children(child)
        check_children(self.root)
        return found_nodes

    def get_joints(self):
        joints = []

        def iterate_joints(joint):
            joints.append(joint)
            for child in joint.filter('JOINT'):
                iterate_joints(child)
        iterate_joints(next(self.root.filter('ROOT')))
        return joints

    def get_joints_names(self):
        joints = []

        def iterate_joints(joint):
            joints.append(joint.value[1])
            for child in joint.filter('JOINT'):
                iterate_joints(child)
        iterate_joints(next(self.root.filter('ROOT')))
        return joints

    def joint_direct_children(self, name):
        joint = self.get_joint(name)
        return [child for child in joint.filter('JOINT')]

    def get_joint_index(self, name):
        return self.get_joints().index(self.get_joint(name))

    def get_joint(self, name):
        found = self.search('ROOT', name)
        if not found:
            found = self.search('JOINT', name)
        if found:
            return found[0]
        raise LookupError('joint not found')

    def joint_offset(self, name):
        joint = self.get_joint(name)
        offset = joint['OFFSET']
        return (float(offset[0]), float(offset[1]), float(offset[2]))

    def joint_channels(self, name):
        joint = self.get_joint(name)
        return joint['CHANNELS'][1:]

    def get_joint_channels_index(self, joint_name):
        index = 0
        for joint in self.get_joints():
            if joint.value[1] == joint_name:
                return index
            index += int(joint['CHANNELS'][0])
        raise LookupError('joint not found')

    def get_joint_channel_index(self, joint, channel):
        channels = self.joint_channels(joint)
        if channel in channels:
            channel_index = channels.index(channel)
        else:
            channel_index = -1
        return channel_index
        
    def frame_joint_channel(self, frame_index, joint, channel, value=None):
        joint_index = self.get_joint_channels_index(joint)
        channel_index = self.get_joint_channel_index(joint, channel)
        if channel_index == -1 and value is not None:
            return value
        return float(self.frames[frame_index][joint_index + channel_index])

    def frame_joint_channels(self, frame_index, joint, channels, value=None):
        values = []
        joint_index = self.get_joint_channels_index(joint)
        for channel in channels:
            channel_index = self.get_joint_channel_index(joint, channel)
            if channel_index == -1 and value is not None:
                values.append(value)
            else:
                values.append(
                    float(
                        self.frames[frame_index][joint_index + channel_index]
                    )
                )
        return values

    def frames_joint_channels(self, joint, channels, value=None):
        all_frames = []
        joint_index = self.get_joint_channels_index(joint)
        for frame in self.frames:
            values = []
            for channel in channels:
                channel_index = self.get_joint_channel_index(joint, channel)
                if channel_index == -1 and value is not None:
                    values.append(value)
                else:
                    values.append(
                        float(frame[joint_index + channel_index]))
            all_frames.append(values)
        return all_frames

    def joint_parent(self, name):
        joint = self.get_joint(name)
        if joint.parent == self.root:
            return None
        return joint.parent

    def joint_parent_index(self, name):
        joint = self.get_joint(name)
        if joint.parent == self.root:
            return -1
        return self.get_joints().index(joint.parent)

    @property
    def nframes(self):
        try:
            return int(next(self.root.filter('Frames:')).value[1])
        except StopIteration:
            raise LookupError('number of frames not found')

    @property
    def frame_time(self):
        try:
            return float(next(self.root.filter('Frame')).value[2])
        except StopIteration:
            raise LookupError('frame time not found')

'''
# bvh-python
Python module for parsing BVH (Biovision hierarchical data) mocap files

#### Instance Bvh object from .bvh file
```python
>>> from bvh import Bvh
>>> with open('tests/test_freebvh.bvh') as f:
>>>    mocap = Bvh(f.read())
```
 #### Get mocap tree
```python
>>> [str(item) for item in mocap.root]
['HIERARCHY', 'ROOT mixamorig:Hips', 'MOTION', 'Frames: 69', 'Frame Time: 0.0333333']
```
 #### Get ROOT OFFSET
```python
>>> next(mocap.root.filter('ROOT'))['OFFSET']
['0.0000', '0.0000', '0.0000']
```
 #### Get JOINT OFFSET
```python
>>> mocap.joint_offset('mixamorig:Head')
(-0.0, 10.3218, 3.1424)
```
 #### Get Frames
```python
>>> mocap.nframes
69
```
 #### Get Frame Time
```python
>>> mocap.frame_time
0.0333333
```
 #### Get JOINT CHANNELS
```python
>>> mocap.joint_channels('mixamorig:Neck')
['Zrotation', 'Yrotation', 'Xrotation']
```
 #### Get Frame CHANNEL
```python
>>> mocap.frame_joint_channel(22, 'mixamorig:Spine', 'Xrotation')
11.8096
```
 #### Get all JOINT names
```python
>>> mocap.get_joints_names()
['mixamorig:Hips', 'mixamorig:Spine', 'mixamorig:Spine1', 'mixamorig:Spine2', 'mixamorig:Neck', 'mixamorig:Head', 'mixamorig:HeadTop_End', 'mixamorig:LeftEye', 'mixamorig:RightEye', 'mixamorig:LeftShoulder', 'mixamorig:LeftArm', 'mixamorig:LeftForeArm', 'mixamorig:LeftHand', 'mixamorig:LeftHandMiddle1', 'mixamorig:LeftHandMiddle2', 'mixamorig:LeftHandMiddle3', 'mixamorig:LeftHandThumb1', 'mixamorig:LeftHandThumb2', 'mixamorig:LeftHandThumb3', 'mixamorig:LeftHandIndex1', 'mixamorig:LeftHandIndex2', 'mixamorig:LeftHandIndex3', 'mixamorig:LeftHandRing1', 'mixamorig:LeftHandRing2', 'mixamorig:LeftHandRing3', 'mixamorig:LeftHandPinky1', 'mixamorig:LeftHandPinky2', 'mixamorig:LeftHandPinky3', 'mixamorig:RightShoulder', 'mixamorig:RightArm', 'mixamorig:RightForeArm', 'mixamorig:RightHand', 'mixamorig:RightHandMiddle1', 'mixamorig:RightHandMiddle2', 'mixamorig:RightHandMiddle3', 'mixamorig:RightHandThumb1', 'mixamorig:RightHandThumb2', 'mixamorig:RightHandThumb3', 'mixamorig:RightHandIndex1', 'mixamorig:RightHandIndex2', 'mixamorig:RightHandIndex3', 'mixamorig:RightHandRing1', 'mixamorig:RightHandRing2', 'mixamorig:RightHandRing3', 'mixamorig:RightHandPinky1', 'mixamorig:RightHandPinky2', 'mixamorig:RightHandPinky3', 'mixamorig:RightUpLeg', 'mixamorig:RightLeg', 'mixamorig:RightFoot', 'mixamorig:RightToeBase', 'mixamorig:LeftUpLeg', 'mixamorig:LeftLeg', 'mixamorig:LeftFoot', 'mixamorig:LeftToeBase']
```
 #### Get single JOINT name
```python
>>> mocap.get_joints_names()[17]
'mixamorig:LeftHandThumb2'
```
 #### Get JOINT parent index
```python
>>> mocap.joint_parent_index('mixamorig:Neck')
3
```
 #### Get JOINT parent name
```python
>>> mocap.joint_parent('mixamorig:Head').name
'mixamorig:Neck'
```
 #### Search single item
```python
>>> [str(node) for node in mocap.search('JOINT', 'LeftShoulder')]
['JOINT LeftShoulder']
```
 #### Search all items
```python
>>> [str(node) for node in mocap.search('JOINT')]
['JOINT mixamorig:Spine', 'JOINT mixamorig:Spine1', 'JOINT mixamorig:Spine2', 'JOINT mixamorig:Neck', 'JOINT mixamorig:Head', 'JOINT mixamorig:HeadTop_End', 'JOINT mixamorig:LeftEye', 'JOINT mixamorig:RightEye', 'JOINT mixamorig:LeftShoulder', 'JOINT mixamorig:LeftArm', 'JOINT mixamorig:LeftForeArm', 'JOINT mixamorig:LeftHand', 'JOINT mixamorig:LeftHandMiddle1', 'JOINT mixamorig:LeftHandMiddle2', 'JOINT mixamorig:LeftHandMiddle3', 'JOINT mixamorig:LeftHandThumb1', 'JOINT mixamorig:LeftHandThumb2', 'JOINT mixamorig:LeftHandThumb3', 'JOINT mixamorig:LeftHandIndex1', 'JOINT mixamorig:LeftHandIndex2', 'JOINT mixamorig:LeftHandIndex3', 'JOINT mixamorig:LeftHandRing1', 'JOINT mixamorig:LeftHandRing2', 'JOINT mixamorig:LeftHandRing3', 'JOINT mixamorig:LeftHandPinky1', 'JOINT mixamorig:LeftHandPinky2', 'JOINT mixamorig:LeftHandPinky3', 'JOINT mixamorig:RightShoulder', 'JOINT mixamorig:RightArm', 'JOINT mixamorig:RightForeArm', 'JOINT mixamorig:RightHand', 'JOINT mixamorig:RightHandMiddle1', 'JOINT mixamorig:RightHandMiddle2', 'JOINT mixamorig:RightHandMiddle3', 'JOINT mixamorig:RightHandThumb1', 'JOINT mixamorig:RightHandThumb2', 'JOINT mixamorig:RightHandThumb3', 'JOINT mixamorig:RightHandIndex1', 'JOINT mixamorig:RightHandIndex2', 'JOINT mixamorig:RightHandIndex3', 'JOINT mixamorig:RightHandRing1', 'JOINT mixamorig:RightHandRing2', 'JOINT mixamorig:RightHandRing3', 'JOINT mixamorig:RightHandPinky1', 'JOINT mixamorig:RightHandPinky2', 'JOINT mixamorig:RightHandPinky3', 'JOINT mixamorig:RightUpLeg', 'JOINT mixamorig:RightLeg', 'JOINT mixamorig:RightFoot', 'JOINT mixamorig:RightToeBase', 'JOINT mixamorig:LeftUpLeg', 'JOINT mixamorig:LeftLeg', 'JOINT mixamorig:LeftFoot', 'JOINT mixamorig:LeftToeBase']
```
#### Get joint's direct children
```python
>>> mocap.joint_direct_children('mixamorig:Hips')
[JOINT mixamorig:Spine, JOINT mixamorig:RightUpLeg, JOINT mixamorig:LeftUpLeg]
```
'''
