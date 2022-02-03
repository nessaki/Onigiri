

import bpy
import traceback
import mathutils




if 1 == 1:

    props = {}

    props["help"] = "https://critters.xyz/help/bentobuddy/puppeteer.html"

    props["master"] = None 




def get_master(armature, report=False):
    OBJ = armature
    if isinstance(armature, str):
        OBJ = bpy.data.objects[armature]

    
    masRig = OBJ.get('bb_puppet_master')
    minions = OBJ.get('bb_puppet_minions')
    if masRig == None and minions == None:
        if report == True:
            print("puppet::get_master reports : not in the set")
        return False
    if masRig != None and minions != None:
        if report == True:
            print("puppet::get_master reports : provided object contains both data sets for master and puppet, this is invalid.")
        return False
    if masRig != None:
        return masRig
    
    if minions != None:
        return OBJ

    if report == True:
        print("puppet::get_master reports : fall-through, this shouldn't happen.")

    return False




