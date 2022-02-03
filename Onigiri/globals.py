
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

    
    
    
    
    bb_mixer = {}
    bb_mixer['source'] = ""
    
    
    bb_mixer['bone_location_set'] = ""
    bb_mixer['bone_rotation_set'] = ""
    bb_mixer['bone_scale_set'] = ""

    
    
    
    
    
    
    
    
    
    bb_mixer['constraints'] = {}
    for bone in skel.avatar_skeleton:
        bone_type = skel.avatar_skeleton[bone]['type']
        
        
        
        

        
        if 1 == 1:
            bb_mixer['constraints'][bone] = {}
            bb_mixer['constraints'][bone]['location'] = None
            bb_mixer['constraints'][bone]['rotation'] = None
            bb_mixer['constraints'][bone]['scale'] = None
            
            bb_mixer['constraints'][bone]['child_of'] = None





    
    
    
    
    
    bb_paint = {}
    bb_paint['use_frontface'] = False
    bb_paint['use_frontface_falloff'] = False
    bb_paint['falloff_shape'] = 'PROJECTED'
    bb_paint['object'] = None 

    
    
    

    












    bb_alib = {}
    
    
    
    bb_alib['actions'] = {}

    bb_alib['active_action'] = None

    bb_alib['frame_start'] = 1

    bb_alib['count'] = 0

















