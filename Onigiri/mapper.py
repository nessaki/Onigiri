



import bpy
import mathutils
from mathutils import Vector
import decimal
import importlib
from math import *
import re

from . import mod_data
from .mod_data import *
from . import mod_functions
from .mod_functions import *
from . import utils




def mapper_init():
    obj = bpy.data.objects
    bmp = bpy.context.window_manager.bb_mapper

    


    store_armature_data(bmp.mapper_source_name)
    obj[bmp.mapper_source_name]['location'] = obj[bmp.mapper_source_name].location.copy()

    
    bpy.app.handlers.depsgraph_update_post.append(mapper_handler)




def mapper_handler(context):
    obj = bpy.data.objects
    bmp = bpy.context.window_manager.bb_mapper

    
    
    
    






    
    
    
    
    
    
    

    if bmp.mapper_source_name == "":
        bpy.app.handlers.depsgraph_update_post.remove(mapper_handler)
        bmp.mapper_enabled = False
        print("mapper_handler reports: terminating mapper, source became empty while working:", bmp.mapper_source_name_backup)
        bpy.ops.bentobuddy.mapper_reset()
        return
    if bmp.mapper_source_name not in obj:
        bpy.app.handlers.depsgraph_update_post.remove(mapper_handler)
        bmp.mapper_enabled = False
        print("mapper_handler reports: terminating mapper, source removed:", bmp.mapper_source_name_backup)
        bpy.ops.bentobuddy.mapper_reset()
        return
    
    if bmp.mapper_lock_source == False:
        try:
            bpy.app.handlers.depsgraph_update_post.remove(mapper_handler)
        except:
            print("mapper::mapper_handler reports attempt to disable but doesn't exist")
        bmp.mapper_enabled = False
        print("mapper_handler reports: mapper disengaged by source")
        bpy.ops.bentobuddy.mapper_reset()
        return
    
    
    
    
    
    
    
        
        
        
        
        

    return 





def store_bone_map(source="", sbone="", target="", tbone=""):
    if source =="" or target == "" or sbone == "" or tbone == "":
        print("something is missing, recheck your functions: source/sbone/target/tbone - ", source, sbone, target, tbone)
        return False

    
    
    
    




    obj = bpy.data.objects

    

    
    
    

    
    if 'bone_map' not in obj[source]:
    
        obj[source]['bone_map'] = dict()
        
        obj[source]['bone_map'][sbone] = {target: tbone}
    
    if 'bone_map' not in obj[target]:
        
        obj[target]['bone_map'] = dict()
        obj[target]['bone_map'][tbone] = {source: sbone}
    else:
        
        obj[source]['bone_map'][sbone] = {target: tbone}
        obj[target]['bone_map'][tbone] = {source: sbone}


    return True






def store_armature_data(armature=""):




    
    
    obj = bpy.data.objects
    ani = bpy.context.window_manager.bb_animesh

    armObj = obj[armature]

    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[armature].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[armature]

    source_bone_data = dict()

    
    
    
    
    
    
    target_bone_data = dict()

    
    
        
        
        
        
        
            
            
            

    
    
    rig_data = {}
    armObj["pose_matrix"] = {}
    for boneObj in obj[armature].pose.bones:
        bone = boneObj.name
        head = boneObj.head.copy()
        tail = boneObj.tail.copy()
        source_bone_data[bone] = {}
        source_bone_data[bone] = {
            "pose": {
                "head": head,
                "tail": tail,
                }
            }
        armObj["pose_matrix"][bone] = {}
        armObj["pose_matrix"][bone] = boneObj.matrix.copy()

    
    
    
    
        
        

    
    
    
    
    bpy.context.view_layer.objects.active = obj[armature]
    for o in bpy.context.selected_objects:
        o.select_set(False)
    obj[armature].select_set(True)
    bpy.ops.object.duplicate()
    editObj = bpy.context.selected_objects[0]
    bpy.context.view_layer.objects.active = editObj
    bpy.ops.object.mode_set(mode='EDIT')

    
    for boneObj in editObj.data.edit_bones:
        head = boneObj.head.copy()
        tail = boneObj.tail.copy()
        roll = boneObj.roll 
        connect = boneObj.use_connect
        source_bone_data.setdefault(boneObj.name, {})
        source_bone_data[boneObj.name].setdefault("edit", {})
        source_bone_data[boneObj.name]["edit"].update({
            "head": head,
            "tail": tail,
            "roll": roll,
            "connect": connect,
            })
    obj[armature]['bone_data'] = source_bone_data
    
    
    
    
    obj[armature]['name'] = armature

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.delete()
    obj[armature].select_set(True)
    bpy.context.view_layer.objects.active = obj[armature]

    return






















def restore_rig(armature="", type="", roll=False, data="all"):
    obj = bpy.data.objects

    print("restoring rig:", armature)

    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')



    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[armature].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[armature]
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action = 'DESELECT')

    
    
    
    
    
    

    if obj[armature].get('bone_map') == None:
        print("This armature has no bone map to restore, did you detach previously?")
        popup("No saved data, did you detach this set?", "Error", "ERROR")
        return False

    bone_map = obj[armature]['bone_map'].to_dict()

    
    
    
    for boneObj in obj[armature].pose.bones:
        sbone = boneObj.name
        for con in obj[armature].pose.bones[sbone].constraints:
            obj[armature].pose.bones[sbone].constraints.remove(con)

    bpy.ops.object.mode_set(mode='EDIT')

    error = 0
    if armature == "":
        print("restore_rig reports: missing armature")
        error = 1
    if type == "":
        print("restore_rig reports: missing type, use pose or edit")
        error = 1
    if error == 1:
        print('usage: restore_rig(armature="someArmatureName", type="[pose/edit]", [roll=True (default = False)]')
        return
    if armature not in obj:
        print("restore_rig reports: the armature does not exist:", armature)
        return False
    if obj[armature].type != 'ARMATURE':
        print("restore_rig reports: the object sent as an armature is NOT an armature", armature)
        return False

    
    if data == "all":
        bone_data = obj[armature]['bone_data'].to_dict()
    elif data == "used":
        bone_data = obj[armature]['bone_map'].to_dict()
    elif data == "unused":
        bone_data = list()
        for b in obj[armature].data.bones:
            if b.name not in obj[armature]['bone_map']:
                bone_data.append(b.name)
    else:
        print("restore_rig reports: data source unknown:", data)
        return False

    
    for sbone in bone_data:
        error = restore_bone(armature=armature, bone=sbone, type=type, roll=True)
        if error == False:
            print("restore_rig reports: restore_bone returned False")
            return False

    
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action = 'DESELECT')

    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    if obj[armature].get('location') != None:
        print("restoring object location for:", armature)
        obj[armature].location = obj[armature]['location']

    
    obj[armature]['mapped'] = 0
    obj[armature]['locked'] = 0

    
    
    
    
    
    
    
    
    
    
    
    
    
        
    

    
    
    clear_transforms(object=armature, rotation=True)

    return True




def restore_bone(armature="", bone="", type="", roll=False):

    obj = bpy.data.objects

    
    
    
    
    
        
        
    error = 0
    if armature == "":
        print("restore_bone reports: missing armature parameter")
        error = 1
    if bone == "":
        print("restore_bone reports: missing bone parameter")
        error = 1
    if type == "":
        print("restore_bone reports: missing type, use pose or edit")
        error = 1
    if error == 1:
        print('usage: restore_bone(armature="someArmatureName", bone="someBoneName, type="[pose/edit]", [roll=True (default = False)]')
        return False
    if armature not in obj:
        print("restore_bone reports: the armature does not exist:", armature)
        return False
    if obj[armature].type != 'ARMATURE':
        print("restore_bone reports: the object sent as an armature is NOT an armature", armature)
        return False

    
    
    if type == "pose":
        obj[armature].data.edit_bones[bone].head =            obj[armature]['bone_data'][bone]['pose']['head']
        obj[armature].data.edit_bones[bone].tail =            obj[armature]['bone_data'][bone]['pose']['tail']
        if roll == True:
            obj[armature].data.edit_bones[bone].roll =                obj[armature]['bone_data'][bone]['edit']['roll']

    elif type == "edit":
        obj[armature].data.edit_bones[bone].head =            obj[armature]['bone_data'][bone]['edit']['head']
        obj[armature].data.edit_bones[bone].tail =            obj[armature]['bone_data'][bone]['edit']['tail']
        if roll == True:
            obj[armature].data.edit_bones[bone].roll =                obj[armature]['bone_data'][bone]['edit']['roll']

    return True












def snap_to(source=""):

    
    bmp = bpy.context.window_manager.bb_mapper

    if source == "":
        print("snap_to reports: no source")
        return False
    
        
        

    obj = bpy.data.objects

    if source not in obj:
        print("snap_to reports: source doesn't exist:", source)
        return False

    if obj[source].get('mapped') == 1:
        print("object already mapped, this should be caught before snap_to")
        popup("Already mapped, Restore or Reset to start over", "ERROR")
        return False

    print("snap_to reports: source is -", source)

    
    
    
    
    
    if bmp.mapper_retarget_only == True:
        
        

        print("snap_to reports: retarget_only is enabled, setting map flag only")

        
        if obj[source].get('bone_map') == None:
            print("snap_to reports: no bone_map")
            return False

        
        if len(obj[source]['bone_map']) == 0:
            print("snap_to reports: bone_map exists but it's empty")
            return False

        
        
        

        
        obj[source]['mapped'] = 1
        return True

    
    
    if bmp.mapper_morph_pose == True:
        print("snap_to reports: morph_pose enabled, setting map flag only")
        print("snap_to reports: adjusting to visual snap, use (Attach) to complete")
        
        

    
    
    
    state = save_state()

    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[source].select_set(True)
    
    bpy.context.view_layer.objects.active = bpy.data.objects[source]


    
        
            
            
        

    
    if obj[source].get('bone_map') == None:
        print("snap_to reports: no bone_map")
        return False

    
    if len(obj[source]['bone_map']) == 0:
        print("snap_to reports: bone_map exists but it's empty")
        return False

    
    
    
    
    
        
            
            
            
                

    
    bone_map = obj[source]['bone_map'].to_dict()

    
    source_location = obj[source].location

    
    
    
    target_states = list()
    for t in bmp['targets']:
        s = save_armature_state(t)
        target_states.append(s)


    
    
    
    
    
    
    
    
    
    
    
    if 1 == 0:
        
        
        
        sarm = source

        
        bpy.ops.object.mode_set(mode='EDIT')
        for boneObj in obj[source].data.edit_bones:
            boneObj.use_connect = False
            boneObj.use_inherit_rotation = False
        bpy.ops.object.mode_set(mode='OBJECT')

        
        
        
        last_frame = 1000000 
        print("will check earliest frame with", last_frame)
        for tarm in bmp['targets']:
            if obj[tarm].animation_data != None:
                best_frame, nothing = obj[tarm].animation_data.action.frame_range
                if best_frame < last_frame:
                    last_frame = best_frame
            else:
                best_frame = 1

        
        bpy.context.scene.frame_set(best_frame)
        bpy.context.view_layer.update()
        current_frame = bpy.context.scene.frame_current

        
        for sbone in bone_map:
            if sbone not in obj[source].data.bones:
                print("Missing source bone in target armature, this is not necessarily bad, you might have a control rig:", sbone)
                bmp.mapper_message = "Missing bones in target: see console"
                continue
            (tarm, tbone), = bone_map[sbone].items()
            
            
            
            obj[sarm].pose.bones[sbone].matrix = obj[tarm].pose.bones[tbone].matrix.copy() @ obj[tarm].matrix_world.inverted()
            bpy.context.view_layer.update()

        bpy.context.scene.frame_set(current_frame)

    

    
    
    if 1 == 1:
        
        bpy.ops.object.mode_set(mode='EDIT')
        for boneObj in obj[source].data.edit_bones:
            boneObj.use_connect = False

        
        
        
        
        
        for sbone in bone_map:
            if sbone not in obj[source].data.bones:
                print("Missing source bone in target armature, this is not necessarily bad, you might have a control rig:", sbone)
                bmp.mapper_message = "Missing bones in target: see console"
                continue
            (tarm, tbone), = bone_map[sbone].items()

            
            head = obj[tarm].pose.bones[tbone].head.copy()
            tail = obj[tarm].pose.bones[tbone].tail.copy()

            tarm_matrix_head = obj[tarm].matrix_world @ obj[tarm].pose.bones[tbone].head.copy()
            tarm_matrix_tail = obj[tarm].matrix_world @ obj[tarm].pose.bones[tbone].tail.copy()

            obj[source].data.edit_bones[sbone].head = tarm_matrix_head - source_location
            obj[source].data.edit_bones[sbone].tail = tarm_matrix_tail - source_location
            obj[source].data.edit_bones[sbone].roll = obj[tarm]['bone_data'][tbone]['edit']['roll']

    
    
    
    bpy.context.view_layer.update()

    
    for s in target_states:
        restore_armature_state(s)




   
   
   
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[source].select_set(True)
    
    bpy.context.view_layer.objects.active = bpy.data.objects[source]

    
    print("snap_to reports: transforms_clear is disabled")
    if 1 == 0:
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action = 'SELECT')
        bpy.ops.pose.transforms_clear()
        bpy.ops.pose.select_all(action = 'DESELECT')

    
    
    



    
    obj[source]['mapped'] = 1

    try:
        bpy.context.window_manager.bb_mapper.mapper_message = mapper_message = "Use (Attach) if you are animating"
    except:
        print("snap_to reports: Called by unknown method.  No problem, continuing...")


    
    
    
    
        

    
    
    
    
        
    




    
    
        
            
            
            
                


    restore_state(state)

    return True









def fly_paper(armature=""):

    obj = bpy.data.objects
    bmp = bpy.context.window_manager.bb_mapper

    
    
    if bmp.mapper_retarget_only == True:
        print("fly_paper reports: mapper_retarget_only is enabled, nothing to do")
        return True

    if armature == "":
        print("fly_paper reports: nothing to do")
        return False

    if obj[armature].type != 'ARMATURE':
        print("fly_paper reports: not an armature", armature)

    
    
    
    
    
    
    
    
    
    
    

    armObj = obj[armature]

    
    if armObj.get('fly_paper') != None:
        fly = armObj['fly_paper']
        del armObj['fly_paper']
        if fly in obj:
            armObj.select_set(False)
            obj[fly].hide_set(False)
            obj[fly].hide_select = False
            obj[fly].select_set(True)
            bpy.context.view_layer.objects.active = obj[fly]
            try:
                bpy.ops.object.delete()
            except:
                print("Couldn't delete stale fly paper:", fly)

    
    
    
    
    
    if bpy.context.active_object != None:
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    armObj.select_set(True)
    bpy.context.view_layer.objects.active = armObj
    bpy.ops.object.duplicate()

    
    armFly = bpy.context.selected_objects[0]
    
    armFly.name = "Fly_Paper"

    
    
    fly = armFly.name

    
    
    armFly['name'] = fly

    
    armObj['fly_paper'] = fly



    
    
    




    
    
        

    
        

    
    
    
    
    remove_armature_groups(fly)
    
    create_bone_group(fly, fly_paper_group_name, fly_paper_theme)

    bpy.ops.object.select_all(action='DESELECT')
    obj[fly].select_set(True)
    bpy.context.view_layer.objects.active = obj[fly]

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.update()
    bpy.ops.object.mode_set(mode='EDIT')

    
    for boneObj in obj[fly].data.edit_bones:
        boneObj.use_deform = False
        boneObj.parent = None

    
    bpy.ops.object.mode_set(mode='POSE')
    for boneObj in obj[fly].pose.bones:
        add_bone_to_group(armature=fly, bone=boneObj.name, group=fly_paper_group_name)

    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    armObj.select_set(True)
    bpy.context.view_layer.objects.active = armObj
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='DESELECT')
    for boneObj in armFly.pose.bones:
        add_bone_to_group(armature=fly, bone=boneObj.name, group=fly_paper_group_name)

    
    
    
    sarm = armObj.name
    bone_map = armObj['bone_map'].to_dict()
    tarm = armFly.name

    
    
    
    
    
    if bmp.mapper_stabilize == True:
        bpy.context.view_layer.objects.active = obj[fly]
        for tboneObj in armFly.pose.bones:
            tbone = tboneObj.name
            sbone = tbone 

            if tbone not in bone_map:
                
                
                bpy.data.objects[sarm].data.bones.active = bpy.data.objects[sarm].data.bones[sbone]
                utils.add_constraint(source=sarm, sbone=sbone, target=tarm, tbone=tbone, type="COPY_LOCATION", influence=1)
                utils.add_constraint(source=sarm, sbone=sbone, target=tarm, tbone=tbone, type="COPY_ROTATION", influence=1)
                
                
                
                if 1 == 0:
                    bc = bpy.data.objects[sarm].pose.bones[sbone].constraints
                    bc.new('COPY_LOCATION')
                    bc['Copy Location'].target = bpy.data.objects[tarm]
                    bc['Copy Location'].subtarget = tbone 
                    bc['Copy Location'].target_space = 'WORLD'
                    bc['Copy Location'].owner_space = 'WORLD'
                    bc['Copy Location'].influence = 1
                    bc['Copy Location'].name = "BB Copy Loc"

                    bc = bpy.data.objects[sarm].pose.bones[sbone].constraints
                    bc.new('COPY_ROTATION')
                    bc['Copy Rotation'].target = bpy.data.objects[tarm]
                    bc['Copy Rotation'].subtarget = tbone 
                    bc['Copy Rotation'].target_space = 'WORLD'
                    bc['Copy Rotation'].owner_space = 'WORLD'
                    bc['Copy Rotation'].influence = 1
                    bc['Copy Rotation'].name = "BB Copy Rot"

        
        bpy.context.view_layer.update()

    
    armFly.hide_set(True)

    
    bpy.ops.object.select_all(action='DESELECT')
    armObj.select_set(True)
    bpy.context.view_layer.objects.active = armObj

    return True
    














def auto_weight_colors(bone="", state=""):
    if bone == "":
        print("auto_weight_colors reports: empty bone name")
        return False
    if state == "":
        print("auto_weight_colors reports: empty state name")
        return False

    
    
    bpy.app.handlers.depsgraph_update_post.remove(auto_weight_on_select)
    
    print("auto_weight_colors reports: would have colorized -", bone, state)

    
    bpy.app.handlers.depsgraph_update_post.append(auto_weight_on_select)

    return 










