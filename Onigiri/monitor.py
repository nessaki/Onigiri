

import bpy
import mathutils
from mathutils import Vector
import decimal
import importlib
from math import *
import re
import os
import traceback
from bpy.app.handlers import persistent

from . import mod_functions
from .mod_functions import *










@persistent
def expire_data(context):
    bbe = bpy.context.window_manager.bb_expire
    
    
    
    if bbe.get('suspend') == True:
        return

    if bbe.get('triggers') == None:
        
        return
    
    for trigger in bbe['triggers']:
        if trigger not in bpy.data.objects:
            print("expire_data reports: trigger object is missing", "[" + trigger + "],", "expiring links")
            expire_purge(trigger)
    return









































def expire_create(trigger="", partners=[], objects=[], tasks={}):
    print("expire_create reports: adding expire trigger for", trigger)
    bbe = bpy.context.window_manager.bb_expire
    expires = {}
    expires[trigger] = {}
    expires[trigger]['objects'] = objects
    expires[trigger]['partners'] = partners
    expires[trigger]['tasks'] = tasks

    print("tasks are:", tasks)

    if bbe.get('triggers') == None:
        print("expire_create reports: no triggers property, creating...")
        bbe['triggers'] = {}

    
    
    
    
    bbe['triggers'][trigger] = expires[trigger].copy()

    
    for partner in partners:
        print("expire_create reports: adding partner -", partner)
        expires[partner] = expires[trigger].copy()
        
        expires[partner]['partners'].remove(partner)
        
        expires[partner]['partners'].append(trigger)
        
        bbe['triggers'][partner] = expires[partner].copy()

    return True



def expire_remove(trigger=""):
    bbe = bpy.context.window_manager.bb_expire
    if bbe.get(triggers) == None:
        print("expire_remove reports: bb_expire base item (triggers) is missing")
        return False
    if bbe['triggers'].get(trigger) == None:
        print("expire_remove reports: Trigger doesn't exist -", trigger)
        return False
    
    if bbe['triggers'][trigger].get(partners) != None:
        partners = bbe['triggers'][trigger]['partners']
        if partners != "":
            for p in partners:
                del bbe['triggers'][p]
    del bbe['triggers'][trigger]
    return True



def expire_purge(trigger=""):
    print("expire_purge reports: trigger executed -", trigger)
    bbe = bpy.context.window_manager.bb_expire
    obj = bpy.data.objects
    if bbe.get('triggers') == None:
        print("expire_purge reports: bb_expire base item (triggers) is missing")
        return False
    if bbe['triggers'].get(trigger) == None:
        print("expire_purge reports: Trigger doesn't exist -", trigger)
        return False

    o_to_delete = []

    
    
    
    
    
    
    
    

    for o in bbe['triggers'][trigger]['objects']:
        if o in bpy.data.objects:
            
            
            o_to_delete.append(bpy.data.objects[o])

    
    
    
    
    
    
    
    bbe['suspend'] = True
    bpy.ops.object.delete({"selected_objects": o_to_delete})
    
    


    
    for p in bbe['triggers'][trigger]['partners']:
        print("removing partner trigger:", p)
        try:
            del bbe['triggers'][p]
        except:
            print("missing partner:", p)

    
    
    
    
    tasks = bbe['triggers'][trigger]['tasks'].to_dict()
    print("eval_purge reports: tasks type is", type(tasks))
    if tasks != "":
        for task_list in tasks:
            print("task_list:", task_list)
            for task in tasks:
                print("task:", task)
                jobs = tasks[task_list]
                print("jobs:", jobs)
                for job in jobs:
                    print("running job:", job)
                    eval(job)

    
    del bbe['triggers'][trigger]

    bbe['suspend'] = False
    return True












