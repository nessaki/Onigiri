
import math
import mathutils
from .presets import skeleton as skel

if True:
    collada = {}
    collada['URI'] ='http://www.collada.org/2005/11/COLLADASchema'
    collada['namespace'] = '{http://www.collada.org/2005/11/COLLADASchema}'

    version = (0, 0, 0)

    bone_roll = {
    "mHandThumb1Left": 0.7853981852531433,
    "mHandThumb2Left": 0.7853981852531433,
    "mHandThumb3Left": 0.7853981852531433,
    "mHandThumb1Right": -0.7853981852531433,
    "mHandThumb2Right": -0.7853981852531433,
    "mHandThumb3Right": -0.7853981852531433,
    "mHipRight": -0.13089969754219055,
    "mHipLeft": 0.13089969754219055,
    }

    Z90 = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Z')
    Z90I = Z90.inverted()
    Z180 = mathutils.Matrix.Rotation(math.radians(180.0), 4, 'Z')
    Z180I = Z180.inverted()

    align_bones = {}
    align_bones['first'] = None
    align_bones['last'] = None

if True:
    
    legacy_parents = {}
    legacy_parents['mTorso'] = 'mPelvis'
    legacy_parents['mChest'] = 'mTorso'

    goofy_bones = ('PelvisInv', 'COG', 'Origin', 'Tinker')

    spine_chain = {
        "mSpine1": "mTorso",
        "mSpine2": "mPelvis",
        "mSpine3": "mChest",
        "mSpine4": "mTorso",
        "mPelvis": "mSpine2",
        "mTorso" : "mSpine1",
        "mChest" : "mSpine3",
        }

if True:

    oni_mixer = {}
    oni_mixer['source'] = ""
    
    oni_mixer['bone_location_set'] = ""
    oni_mixer['bone_rotation_set'] = ""
    oni_mixer['bone_scale_set'] = ""

    oni_mixer['constraints'] = {}
    for bone in skel.avatar_skeleton:
        bone_type = skel.avatar_skeleton[bone]['type']
        
        if 1 == 1:
            oni_mixer['constraints'][bone] = {}
            oni_mixer['constraints'][bone]['location'] = None
            oni_mixer['constraints'][bone]['rotation'] = None
            oni_mixer['constraints'][bone]['scale'] = None
            
            oni_mixer['constraints'][bone]['child_of'] = None

    oni_paint = {}
    oni_paint['use_frontface'] = False
    oni_paint['use_frontface_falloff'] = False
    oni_paint['falloff_shape'] = 'PROJECTED'
    oni_paint['object'] = None 

    oni_alib = {}
    
    oni_alib['actions'] = {}

    oni_alib['active_action'] = None

    oni_alib['frame_start'] = 1

    oni_alib['count'] = 0
