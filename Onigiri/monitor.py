

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
    onie = bpy.context.window_manager.oni_expire
    
    
    
    if onie.get('suspend') == True:
        return

    if onie.get('triggers') == None:
        
        return
    
    for trigger in onie['triggers']:
        if trigger not in bpy.data.objects:
            print("expire_data reports: trigger object is missing", "[" + trigger + "],", "expiring links")
            expire_purge(trigger)
    return









































def expire_create(trigger="", partners=[], objects=[], tasks={}):
    print("expire_create reports: adding expire trigger for", trigger)
    onie = bpy.context.window_manager.oni_expire
    expires = {}
    expires[trigger] = {}
    expires[trigger]['objects'] = objects
    expires[trigger]['partners'] = partners
    expires[trigger]['tasks'] = tasks

    print("tasks are:", tasks)

    if onie.get('triggers') == None:
        print("expire_create reports: no triggers property, creating...")
        onie['triggers'] = {}

    
    
    
    
    onie['triggers'][trigger] = expires[trigger].copy()

    
    for partner in partners:
        print("expire_create reports: adding partner -", partner)
        expires[partner] = expires[trigger].copy()
        
        expires[partner]['partners'].remove(partner)
        
        expires[partner]['partners'].append(trigger)
        
        onie['triggers'][partner] = expires[partner].copy()

    return True



def expire_remove(trigger=""):
    onie = bpy.context.window_manager.oni_expire
    if onie.get(triggers) == None:
        print("expire_remove reports: oni_expire base item (triggers) is missing")
        return False
    if onie['triggers'].get(trigger) == None:
        print("expire_remove reports: Trigger doesn't exist -", trigger)
        return False
    
    if onie['triggers'][trigger].get(partners) != None:
        partners = onie['triggers'][trigger]['partners']
        if partners != "":
            for p in partners:
                del onie['triggers'][p]
    del onie['triggers'][trigger]
    return True



def expire_purge(trigger=""):
    print("expire_purge reports: trigger executed -", trigger)
    onie = bpy.context.window_manager.oni_expire
    obj = bpy.data.objects
    if onie.get('triggers') == None:
        print("expire_purge reports: oni_expire base item (triggers) is missing")
        return False
    if onie['triggers'].get(trigger) == None:
        print("expire_purge reports: Trigger doesn't exist -", trigger)
        return False

    o_to_delete = []

    
    
    
    
    
    
    
    

    for o in onie['triggers'][trigger]['objects']:
        if o in bpy.data.objects:
            
            
            o_to_delete.append(bpy.data.objects[o])

    
    
    
    
    
    
    
    onie['suspend'] = True
    bpy.ops.object.delete({"selected_objects": o_to_delete})
    
    


    
    for p in onie['triggers'][trigger]['partners']:
        print("removing partner trigger:", p)
        try:
            del onie['triggers'][p]
        except:
            print("missing partner:", p)

    
    
    
    
    tasks = onie['triggers'][trigger]['tasks'].to_dict()
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

    
    del onie['triggers'][trigger]

    onie['suspend'] = False
    return True












