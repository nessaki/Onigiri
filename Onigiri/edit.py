import bpy
from . import mod_data as md

from . import mod_functions
from .mod_functions import *







def auto_weight_on_select(context):

    
    
    
    if bpy.context.selected_pose_bones == None:
        return

    
    

    
    
    
    
    
    

    
    
    
    

    if bpy.context.window_manager.cc_props.edit_mode == False:
        
        return

    ccp = bpy.context.window_manager.cc_props
    last_selected = ccp['map_editor']['last_selected']

    
    if bpy.context.active_object.name != ccp.source_rig_name:
        return

    
    
    if len(bpy.context.selected_pose_bones) > 1:
        return


    
    
    if len(bpy.context.selected_pose_bones) == 0:
        if last_selected == "":
            
            return 

        
        if last_selected in ccp['remap_stored']['rename']:
            print("04: resetting last_selected:", last_selected)
            auto_weight_colors(bone=last_selected, state="reset")

        ccp['map_editor']['last_selected'] = ""
        return

    
    
    
    
    if len(bpy.context.selected_pose_bones) > 1:
        
        if ccp['map_editor']['last_selected'] != "":
            
            auto_weight_colors(bone=last_selected, state="reset")
            
            ccp['map_editor']['last_selected'] = ""
        return

    
    if len(bpy.context.selected_pose_bones) == 1:
        bone = bpy.context.selected_pose_bones[0].name
        
    else:
        print("--- THIS ERROR SHOULD NOT HAPPEN ---")
        return

    
    if ccp['map_editor']['last_selected'] == bone:
        
        return

    
    if bone in ccp['remap_stored']['rename']:
        
        
        if last_selected != "":
            
            if last_selected in ccp['remap_stored']['rename']:
                
                
                auto_weight_colors(bone=last_selected, state="reset")

        
        auto_weight_colors(bone=bone, state="active")

    
    else:
        if last_selected != "":
            if last_selected in ccp['remap_stored']['rename']:
                
                auto_weight_colors(bone=last_selected, state="reset")

    
    
    
    ccp['map_editor']['last_selected'] = bone




    












def auto_weight_colors(bone="", state=""):
    if bone == "":
        print("auto_weight_colors reports: empty bone name")
        return False
    if state == "":
        print("auto_weight_colors reports: empty state name")
        return False

    obj = bpy.data.objects
    ccp = bpy.context.window_manager.cc_props

    
    
    bpy.app.handlers.depsgraph_update_post.remove(auto_weight_on_select)

    arm = bpy.context.active_object.name
    if state == "active":
        if md.cc_rename_selected_name not in obj[arm].pose.bone_groups:
            bpy.ops.pose.group_add()
            obj[arm].pose.bone_groups.active.name = md.cc_rename_selected_name
            obj[arm].pose.bone_groups.active.color_set = md.cc_rename_selected_color
            
            bpy.ops.pose.group_add()
            obj[arm].pose.bone_groups.active.name = md.cc_reskin_selected_name
            obj[arm].pose.bone_groups.active.color_set = md.cc_reskin_selected_color
        bpy.data.objects[arm].pose.bones[bone].bone_group =            bpy.data.objects[arm].pose.bone_groups[md.cc_rename_selected_name]
        
        if bone in ccp['remap_stored']['reskin']:
            for child in ccp['remap_stored']['reskin'][bone]:
                bpy.data.objects[arm].pose.bones[child].bone_group =                    bpy.data.objects[arm].pose.bone_groups[md.cc_reskin_selected_name]
    elif state == "reset":
        bpy.data.objects[arm].pose.bones[bone].bone_group =            bpy.data.objects[arm].pose.bone_groups[md.cc_rename_group]
        if bone in ccp['remap_stored']['reskin']:
            for child in ccp['remap_stored']['reskin'][bone]:
                bpy.data.objects[arm].pose.bones[child].bone_group =                    bpy.data.objects[arm].pose.bone_groups[md.cc_reskin_group]


    print("auto_weight_colors reports: exiting with bone and state:", bone, state)

    
    bpy.app.handlers.depsgraph_update_post.append(auto_weight_on_select)

    return 














