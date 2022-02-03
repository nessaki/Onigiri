
import bpy
import traceback
import mathutils
import xml.etree.ElementTree as ET




if 1 == 1:

    props = {}

    
    
    
    
    
    
    
    
    
    
    
    
    
    


    
    
    props['enabled'] = False

    
    
    props['tabs'] = {
        "body": False,
        "head": False,
        "eyes": False,
        "ears": False,
        "nose": False,
        "mouth": False,
        "chin": False,
        "torso": False,
        "legs": False,
        }












def import_shape(file=None):

    obj = bpy.data.objects
    tree = ET.parse(file)
    root = tree.getroot()

    shape = {}
    shape['param'] = {}
    shape['texture'] = {}
    shape['root'] = {}
    shape['bone'] = {}
    shape['collision_volume'] = {}
    shape['attachment_point'] = {}
    shape['joint_rig_info'] = {}

    
    
    
    
    
    tags = root.find(f'archetype')
    for t in tags:
        tag = t.tag
        if tag == 'param':
            id = t.get('id')
            shape['param'][id] = {
                "id"      : id,
                "name"    : t.get('name'),
                "display" : t.get('display'),
                "value"   : t.get('value'),
                "u8"      : t.get('u8'),
                "type"    : t.get('type'),
                "wearable": t.get('wearable'),
                "group"   : t.get('group'),
                }
        if tag == 'texture':
            te = t.get('te')
            shape['texture'][te] = {
                "te": te,
                "uuid": t.get('uuid'),
                }
        if tag == 'root':
            name = t.get('name')
            shape['root'][name] = {
                "name"    : name,
                "position": t.get('position'),
                "scale"   : t.get('scale'),
                }
        if tag == 'bone':
            name = t.get('name')
            shape['bone'][name] = {
                "name": name,
                "position": t.get('position'),
                "scale"   : t.get('scale'),
                }
        if tag == 'collision_volume':
            name = t.get('name')
            shape['collision_volume'][name] = {
                "name": name,
                "position": t.get('position'),
                "scale"   : t.get('scale'),
                }
        if tag == 'attachment_point':
            name = t.get('name')
            shape['attachment_point'][name] = {
                "name": name,
                "position": t.get('position'),
                "scale"   : t.get('scale'),
                }
        if tag == 'joint_rig_info':
            num = t.get('num')
            shape['joint_rig_info'][num] = {
                "num" : num,
                "name": t.get('name'),
                "min" : t.get('min'),
                "max" : t.get('max'),
                "tmin": t.get('tmin'),
                "tmax": t.get('tmax'),
                }

    for tag in shape:
        if len(shape[tag]) == 0:
            print("Something was missing from the xml shape:", tag)
            return False

    return shape


    
    







def apply_shape(armature=None, shape=None):
    obj = bpy.data.objects
    armObj = obj[armature]

    return True





def save_shape(file=None, shape=None):

    content = []
    content.append('<?xml version="1.0" encoding="US-ASCII" standalone="yes"?>')
    content.append('\n')
    content.append('<linden_genepool version="1.0">')
    content.append('\n')
    content.append('\n')
    content.append('\t')
    content.append('<archetype name="???">')
    content.append('\n')

    for node in shape:
        for k in shape[node]:
            content.append('\t')
            content.append('\t')
            content.append('<')
            content.append(node)
            for attrib in shape[node][k]:
                value = shape[node][k][attrib]
                content.append(" ")
                content.append(attrib)
                content.append('="')
                content.append(value)
                content.append('"')
            content.append('/>')
            content.append('\n')
    content.append('\t')
    content.append('</archetype>')
    content.append('\n')
    content.append('\n')
    content.append('</linden_genepool>')
    content.append('\n')

    buf = "".join(content)

    f = open(file, "w", newline='', encoding='UTF8')
    f.write(buf)
    f.close()

    return True





def get_director(object, report=False):
    OBJ = object
    if isinstance(object, str):
        OBJ = bpy.data.objects[object]

    
    
    aObj = OBJ.get('bb_motion_actor', None)
    dObj = OBJ.get('bb_motion_director', None)

    
    
    if aObj == None and dObj == None:
        if report == True:
            print("shape::get_director reports : nothing gotten nothing given")
        return False

    
    if aObj != None:
        if report == True:
            print("shape::get_director reports : given object is the director")
        return OBJ

    
    if utils.is_valid(dObj) == False:
        if report == True:
            print("shape::get_director reports : the determined director is not valid")

        return False

    
    return dObj




