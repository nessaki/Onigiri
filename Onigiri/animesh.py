import bpy
import os
from bpy_extras.io_utils import ImportHelper, ExportHelper

from . import mod_settings
from .mod_settings import *
from . import mod_functions
from .mod_functions import *
from . import mapper





script_dir = os.path.dirname(os.path.abspath(__file__))

presets_path    =   bb_settings['paths']['presets']
data_path       =   bb_settings['paths']['data']










    
        
    
        
    
        

    





def animesh_init():
    obj = bpy.data.objects
    ani = bpy.context.window_manager.bb_animesh

    print("animesh_init runs")

    
    
    if ani.animesh_mapper_enabled == True:
        
        print("animesh_init reports: from enabled to disabled -> removing map data")
        ani.animesh_mapper_enabled = False

        
        if ani.animesh_source_name_backup not in obj:
            print("animesh_init reports: animation source missing when attempting to clean up data")
            return
        for arm in ani['targets_backup']:
            if arm not in obj:
                print("animesh_init reports: target missing when attempting to clean up data:", arm)

        ani.animesh_source_name = ""

        
        
        
        
        
        
        
        print("animesh_init reports: cleanup")
        mapper.restore_rig(armature=ani.animesh_source_name_backup, type="edit", roll=True)

        
        
        

        
        for boneObj in obj[ani.animesh_source_name_backup].data.bones:
            boneObj.hide_select = False
        for arm in ani['targets_backup']:
            for boneObj in obj[arm].data.bones:
                boneObj.hide_select = False

        
        remove_bone_groups(ani.animesh_source_name_backup)
        for arm in ani['targets_backup']:
            remove_bone_groups(arm)

        
        del obj[ani.animesh_source_name_backup]['bone_map']
        del obj[ani.animesh_source_name_backup]['bone_data']
 
       
        
        for arm in ani['targets_backup']:
            del obj[arm]['bone_map']
            del obj[arm]['bone_data']

        
        del ani['targets_backup']
        
        ani.animesh_targets = 0

        
        ani.animesh_source_bone = ""

        
        ani.animesh_message = "Select your rigs"

        
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

        return

    
    
    elif ani.animesh_mapper_enabled == False:
        
        
        

        print("animesh_init reports: from disabled to enabled -> adding map data to animesh rigs")

        
        for arm in ani['targets']:
            if arm not in obj:
                txt = "A target was missing when attempting to initialize the mapper, did you delete it?"
                print(txt)
                popup(txt, "Missing Armature", "ERROR")
                return
        
        if ani.animesh_source_name_backup not in obj:
            txt = "The source was missing when attempting to initialize the mapper, did you delete it?"
            print(txt)
            popup(txt, "Missing Armature", "ERROR")
            return

        
        obj[ani.animesh_source_name].show_in_front = True
        for arm in ani['targets']:
            obj[arm].show_in_front = True

        

        
        
        
        apply_transforms(object=ani.animesh_source_name, rotation=True, scale=True, location=True)
        
        apply_rest_pose(armature=ani.animesh_source_name)
        
        
        obj[ani.animesh_source_name]['location'] = obj[ani.animesh_source_name].location

        
        
        bpy.ops.object.select_all(action='DESELECT')

        
        print("animesh_init reports: assuming safe mode", bpy.context.mode)

        
        
        
        
        
        if ani.animesh_bone_map == False:
            
            remove_bone_groups(ani.animesh_source_name)
            for arm in ani['targets']:
                remove_bone_groups(arm)
            
            create_bone_group(ani.animesh_source_name, bb_source_group, bb_source_theme)
            for arm in ani['targets']:
                create_bone_group(arm, bb_target_group, bb_target_theme)
            obj[ani.animesh_source_name]['bone_map'] = dict()
            for arm in ani['targets']:
                obj[arm]['bone_map'] = dict()
        else:
            print("animesh_init reports: bone_map exists, skipping definition")
        
        if ani.animesh_data_map == False:
            
            obj[ani.animesh_source_name_backup]['bone_data'] = dict()
            for arm in ani['targets']:
                obj[arm]['bone_data'] = dict()
        else:
            print("animesh_init reports: data_map exists, skipping definition")

        
        
        for boneObj in obj[ani.animesh_source_name_backup].data.bones:
            boneObj.hide_select = False
        for arm in ani['targets']:
            for boneObj in obj[arm].data.bones:
                boneObj.hide_select = True

        
        
        ani.animesh_rig = "source"

        
        
        
        obj[ani.animesh_source_name].select_set(True)
        bpy.ops.object.mode_set(mode='EDIT')
        for boneObj in obj[ani.animesh_source_name].data.edit_bones:
            boneObj.use_connect = False

        
        print("animesh_init reports: store_armature_data")
        mapper.store_armature_data(armature=ani.animesh_source_name)
        for tarm in ani['targets'].keys():
            mapper.store_armature_data(armature=tarm)


        
        
        rigs = [ani.animesh_source_name]
        
        for arm in ani['targets']:
            rigs.append(arm)
        
        set_obj_mode("pose", rigs)

        
        bpy.ops.pose.select_all(action='DESELECT')

        
        
        
        

        
        ani.animesh_mapper_enabled = True

        return

    print("fall through on animesh_init, not sure what happened")

    return





def animesh_mode(context):
    obj = bpy.data.objects
    ani = bpy.context.window_manager.bb_animesh




    
    
    
    

    
    
    



    if ani.animesh_source_name_backup not in obj:
        print("animesh_mode reports: terminating mapper, source removed:", ani.animesh_source_name_backup)
        ani.animesh_mapper_enabled = False
        return
    for arm in ani['targets_backup']:
        if arm not in obj:
            print("animesh_mode reports: terminating mapper, target was removed:", arm)
            ani.animesh_mapper_enabled = False
            return
    
    if bpy.context.mode != 'POSE':
        bpy.app.handlers.depsgraph_update_post.remove(animesh_mode)
        ani.animesh_message = "WARNING: Suspended!"
        return

    

    
    
    if bpy.context.selected_pose_bones is None:
        return
    if len(bpy.context.selected_pose_bones) != 1:
        return

    
    boneObj = bpy.context.selected_pose_bones[0]

    
    if ani.animesh_rig == "source":
        if bb_flags['debug'] == 1:
            print("source rig activated")
        ani.animesh_message = "Select a target bone"

        
        ani.animesh_source_bone = boneObj.name

        
        
        
        
        
        
        
        if ani.animesh_source_bone in obj[ani.animesh_source_name]['bone_map']:
            print("animesh_mode reports: remapping existing bone", ani.animesh_source_bone)

            
            
            
            
            
            

            
            
            (target_rig, target_bone_value), = obj[ani.animesh_source_name]['bone_map'][ani.animesh_source_bone].items()

            
            del obj[target_rig]['bone_map'][target_bone_value]

            
            bpy.context.view_layer.objects.active = obj[target_rig]
            obj[target_rig].data.bones[target_bone_value].select = True
            bpy.ops.pose.group_unassign()
            bpy.ops.pose.select_all(action = 'DESELECT')

            
            del obj[ani.animesh_source_name]['bone_map'][ani.animesh_source_bone]

        

        

        boneObj.bone_group = bpy.data.objects[ani.animesh_source_name].pose.bone_groups[bb_source_group]

        
        
        for b in obj[ani.animesh_source_name].data.bones:
            b.hide_select = True
        for arm in ani['targets']:
            for b in obj[arm].data.bones:
                b.hide_select = False

        
        obj[ani.animesh_source_name].data.bones[boneObj.name].select = False

        
        ani.animesh_rig = "target"

    elif ani.animesh_rig == "target":
        
        ani.animesh_message = "Select source bone"

        
        ani.animesh_target_bone = boneObj.name

        
        target_rig = bpy.context.selected_pose_bones[0].id_data.name

        
        if ani.animesh_target_bone in obj[target_rig]['bone_map']:
            
            



            (sarm, sbone), = obj[target_rig]['bone_map'][ani.animesh_target_bone].items()
            source_bone_value = sbone


            
            del obj[ani.animesh_source_name]['bone_map'][source_bone_value]

            
            bpy.context.view_layer.objects.active = bpy.data.objects[ani.animesh_source_name]
            obj[ani.animesh_source_name].data.bones[source_bone_value].select = True
            bpy.ops.pose.group_unassign()
            bpy.ops.pose.select_all(action = 'DESELECT')
            
            bpy.context.view_layer.objects.active = bpy.data.objects[ani.animesh_source_name]

        
        

        
        obj[ani.animesh_source_name]['bone_map'][ani.animesh_source_bone] = {}
        obj[ani.animesh_source_name]['bone_map'][ani.animesh_source_bone][target_rig] = ani.animesh_target_bone

        
        

        obj[target_rig]['bone_map'][ani.animesh_target_bone] = dict()
        obj[target_rig]['bone_map'][ani.animesh_target_bone][ani.animesh_source_name] = ani.animesh_source_bone

        
        boneObj.bone_group = bpy.data.objects[target_rig].pose.bone_groups[bb_target_group]

        
        for b in obj[ani.animesh_source_name].data.bones:
            b.hide_select = False
        for arm in ani['targets']:
            for b in obj[arm].data.bones:
                b.hide_select = True

        
        obj[target_rig].data.bones[boneObj.name].select = False

        
        ani.animesh_rig = "source"

    return















class BentoBuddyAnimeshCollectionProps(bpy.types.PropertyGroup):

    
    name : bpy.props.StringProperty(name="container name", default="empty")
    value : bpy.props.BoolProperty(name="container value", default=False)












class BentoBuddyAnimeshProps(bpy.types.PropertyGroup):

    def update_animesh_menu_enabled(self, context):
        

        
        
        ani = bpy.context.window_manager.bb_animesh
        obj = bpy.data.objects
        if ani.animesh_menu_enabled == True:
            print("animesh menu enabled")
        else:
            print("animesh menu disabled")
        return

    def update_animesh_mapper_enabled(self, context):
        
        if bb_settings['terminate'] == True:
            bb_settings['terminate'] = False
            return
        
        
        
        ani = bpy.context.window_manager.bb_animesh
        obj = bpy.data.objects
        if ani.animesh_mapper_enabled == True:
            print("update_animesh_mapper_enabled reports: animesh mapper enabled")
            ani.animesh_message = "Select a source bone"
            
            ani.animesh_rig = "source"
            bpy.app.handlers.depsgraph_update_post.append(animesh_mode)
        else:
            print("update_animesh_mapper_enabled reports: removing animesh_mode handler")
            bpy.app.handlers.depsgraph_update_post.remove(animesh_mode)
            ani.animesh_text = "[Select rigs]"
        return

    def update_animesh_lock_source(self, context):
        if bb_settings['terminate'] == True:
            bb_settings['terminate'] = False
            return
        ani = bpy.context.window_manager.bb_animesh
        obj = bpy.data.objects
        if ani.animesh_lock_source == True:
            if len(bpy.context.selected_objects) == 0:
                ani.animesh_message = "[Select at least 1 armature]"
                bb_settings['terminate'] = True
                ani.animesh_lock_source = False
                return
            if len(bpy.context.selected_objects) > 1:
                ani.animesh_message = "[Select only 1 armature for this]"
                bb_settings['terminate'] = True
                ani.animesh_lock_source = False
                return
            armObj = bpy.context.selected_objects[0]
            if armObj.type != 'ARMATURE':
                ani.animesh_message = "[Must be an armature]"
                bb_settings['terminate'] = True
                ani.animesh_lock_source = False
                return
            
            
            if 'targets' in ani.keys() and armObj.name in ani['targets']:
                print("source rig in target")
                ani.animesh_message = "ERROR: Source is in targets"
                bb_settings['terminate'] = True
                ani.animesh_lock_source = False
                return
            ani.animesh_source_name = armObj.name
            ani.animesh_source_name_backup = armObj.name
            return
        
        ani.animesh_message = "[Select your rigs]"
        
        bb_settings['terminate'] = True
        ani.animesh_lock_target = False
        
        
        ani.animesh_source_name = ""
        
        
        bb_settings['terminate'] = True
        ani.animesh_target_name = ""
        return

    def update_animesh_lock_target(self, context):
        
        
        if bb_settings['terminate'] == True:
            bb_settings['terminate'] = False
            return
        ani = bpy.context.window_manager.bb_animesh
        obj = bpy.data.objects
        if ani.animesh_lock_target == True:
            
            ani['targets'] = dict()
            if len(bpy.context.selected_objects) == 0:
                ani.animesh_message = "[Select at least 1 armature]"
                bb_settings['terminate'] = True
                ani.animesh_lock_target = False
                return
            
            
            
            if ani.animesh_source_name != "" and obj[ani.animesh_source_name] in bpy.context.selected_objects:
                print("can't have source as target")
                ani.animesh_message = "ERROR: Target in source"
                bb_settings['terminate'] = True
                ani.animesh_lock_target = False
                return
            
            for arm in bpy.context.selected_objects:
                print("update_animesh_lock_target reports: recording armatures", arm.name)
                if arm.type == 'ARMATURE':
                    ani['targets'].update({arm.name: {}})
            
            if len(ani['targets']) == 0:
                ani.animesh_message = "[Select armatures]"
                bb_settings['terminate'] = True
                ani.animesh_lock_target = False
                return
            
            ani['targets_backup'] = ani['targets']
            ani.animesh_targets = len(ani['targets'])
            ani.animesh_target_name = "ACTIVE"

            return
        
        
        
        
        
        ani.animesh_message = "[Select your rigs]"
        
        bb_settings['terminate'] = True
        ani.animesh_lock_source = False

        
        ani.animesh_target_name = "" 
        
        bb_settings['terminate'] = True
        ani.animesh_source_name = ""
        
        
        
        ani.animesh_targets = 0
        ani['targets'] = dict()
        return

    def update_animesh_check(self, context):
        if bb_settings['terminate'] == True:
            bb_settings['terminate'] = False
            return
        ani = bpy.context.window_manager.bb_animesh
        obj = bpy.data.objects
        
        
        
        
        
        
        if (ani.animesh_source_name == "" or ani.animesh_target_name == "") and ani.animesh_mapper_enabled == False:
            if ani.get('targets_waiting') != None:
                if len(ani['targets_waiting']) > 0:
                    print("Template targets still waiting to be processed")
                    return
            
            print("update_animesh_check reports: still waiting for data")
            return

        elif (ani.animesh_source_name == "" or ani.animesh_target_name == "") and ani.animesh_mapper_enabled == True:
            
            
            print("update_animesh_check reports: disabled animesh mapper")
            animesh_init()
            return
        else:
            if ani.get('targets_waiting') != None:
                if len(ani['targets_waiting']) > 0:
                    print("Ready to enable template workshop but targets are not completely processed")
                    return

            
            
            
            
            print("update_animesh_check reports: enabled animesh mapper")

            
            source_bone_count = len(obj[ani.animesh_source_name].data.bones)
            if obj[ani.animesh_source_name].get('bentobuddy_control_rig') == True:
                
                print("has control rig", ani.animesh_source_name)
                source_bone_count = int(source_bone_count / 2)
            target_bone_count = 0
            for arm in ani['targets']:
                target_bone_count += len(obj[arm].data.bones)
            if source_bone_count < target_bone_count:
                txt = "Target(s) bone count exceeds the source bone count, you will have problems."
                popup(txt, "Error", "ERROR")
                print("Not enough bones in source rig - source/target:", source_bone_count, target_bone_count)
                
                
            animesh_init()
        return

    def update_animesh_suspend(self, context):
        if bb_settings['terminate'] == True:
            bb_settings['terminate'] = False
            return
        ani = bpy.context.window_manager.bb_animesh
        obj = bpy.data.objects
        if ani.animesh_mapper_enabled == False:
            
            bb_settings['terminate'] = True
            ani.animesh_suspend = False
            return
        
        if ani.animesh_suspend == True:
            bpy.app.handlers.depsgraph_update_post.remove(animesh_mode)
            ani.animesh_message = "[SUSPENDED] Move rigs / bones"
            
            arms = ani['targets'].keys() 
            arms.append(ani.animesh_source_name)
            
            set_select_enabled(select="enabled", armatures=arms)
            
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            obj[ani.animesh_source_name].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects[ani.animesh_source_name]
            print("mapper suspended")
            return
        elif ani.animesh_suspend == False:
            print("mapper resumed")
            arms = ani['targets'].keys() 
            set_select_enabled(select="disabled", armatures=arms)

            
            
            activate(ani.animesh_source_name)
            arms.append(ani.animesh_source_name)
            
            set_obj_mode_multi(mode="pose", objects=arms)
            
            bpy.ops.pose.select_all(action = 'DESELECT')
            ani.animesh_message = "Choose a source bone"
            
            
            ani.animesh_rig = "source"
            bpy.app.handlers.depsgraph_update_post.append(animesh_mode)
            return

        return

    def update_animesh_reset(self, context):
        if bb_settings['terminate'] == True:
            bb_settings['terminate'] = False
            return
        ani = bpy.context.window_manager.bb_animesh
        obj = bpy.data.objects
        
        if ani.animesh_suspend == True:
            ani.animesh_message = "ERROR: come out of suspend"
            bb_settings['terminate'] = True
            ani.animesh_reset = False
            return
        
        bpy.app.handlers.depsgraph_update_post.remove(animesh_mode)

        
        error = mapper.restore_rig(armature=ani.animesh_source_name_backup, type="edit", roll=True)
        if error == False:
            
            print("update_animesh_reset reports: restore_rig returned False, that's not good")

        
        arms = ani['targets'].keys()
        
        set_select_enabled(select="enabled", armatures=arms)
        set_select_enabled(select="enabled", armatures=[ani.animesh_source_name])
        clean_bone_groups(armatures=arms)
        clean_bone_groups(armatures=[ani.animesh_source_name])


        obj[ani.animesh_source_name]['bone_map'] = dict()
        for arm in arms:
            obj[arm]['bone_map'] = dict()

        activate(ani.animesh_source_name)

        bb_settings['terminate'] = True
        ani.animesh_reset = False
        
        
        

        
        
        

        return

    
    animesh_menu_enabled : bpy.props.BoolProperty(
        name = "bbr enable animesh mapper",
        description =            "Enable the character map creator which allows you to point and click bones to be placed for mapping your custom "            "wearable characters or for Animesh.  You can map a number of target characters at one time or just one if you like.",
        default = False,
        update = update_animesh_menu_enabled
        )
    
    
    animesh_mapper_enabled : bpy.props.BoolProperty(
        name = "bbr enable animesh mapper",
        description =            "-- internal",
        default = False,
        update = update_animesh_mapper_enabled
        )
    animesh_lock_source : bpy.props.BoolProperty(
        name = "anim add source",
        description =            "Select your bone source rig, this might, for instance, be a Bento Buddy rig designed for Second Life or Opensim.",
        default = False,
        update = update_animesh_lock_source
        )
    animesh_lock_target : bpy.props.BoolProperty(
        name = "animesh set targets",
        description =            "Select 1 or more target armatures.  These armatures are associated with the characters that you want to "            "bring into Second Life, Opensim or remap to another platform.  For Second Life the bone total cannot be more than 110 "            "per mesh.  The mapper will do the math for you, when source and target are enabled, and let you know if there's a problem.",
        default = False,
        update = update_animesh_lock_target
        )

    animesh_source_name : bpy.props.StringProperty(
        name = "animesh source name",
        description = "",
        default = "",
        update = update_animesh_check
        )
    
    
    
    
    animesh_target_name : bpy.props.StringProperty(
        name = "animesh target names",
        description = "",
        default = "",
        update = update_animesh_check
        )

    
    
    
    animesh_rig : bpy.props.StringProperty(
        default = "",
        )
    
    
    
    animesh_source_bone : bpy.props.StringProperty(
        default = "",
        )
    animesh_target_bone : bpy.props.StringProperty(
        default = "",
        )

    
    
    
    
    
    animesh_targets : bpy.props.IntProperty(
        default = 0,
        
        )
    


    
    animesh_source_name_backup : bpy.props.StringProperty(
        default = "",
        )
    
    animesh_target_name_backup : bpy.props.StringProperty(
        default = "",
        )

    
    animesh_message : bpy.props.StringProperty(
        default = "[look here for messages]",
        )

    animesh_suspend : bpy.props.BoolProperty(
        name = "bbr animesh suspend",
        description =            "This is useful if you need to adjust the position of bones or move rigs in order to get a better view of your work.  "            "This button, or getting out of pose mode, when enabled, will allow you to move your rigs without losing your data.  "            "When you've finished click this button so that it's disabled (out) and you will be returned to your mapping stage.",
        default = False,
        update = update_animesh_suspend
        )
    
    
    
    
    
    animesh_reset : bpy.props.BoolProperty(
        name = "bbr animesh reset",
        description =            "This will reset the mapper as if you never did anything, save your work first.  You might want to do this after you've "            "finished mapping and you've saved your work and now you want to test things out.  Another option is to just save your "            "map file, open a new Blender without closing this one, and test it over there loading the map to see if things worked. ",
        default = False,
        update = update_animesh_reset
        )

    
    
    animesh_template_path : bpy.props.StringProperty(
        default = "",
        )
    
    

    
    animesh_template_ready : bpy.props.BoolProperty(
        name = "animesh template ready",
        description = "-- internal",
        default = False
        )
    
    
    
    
    animesh_bone_map : bpy.props.BoolProperty(
        name = "animesh usable bone map exists",
        description = "-- internal",
        default = False
        )
    animesh_data_map : bpy.props.BoolProperty(
        name = "animesh usable data map exists",
        description = "-- internal",
        default = False
        )

    
    
    
    
    
    
    
    
    animesh_remove_bones_label : bpy.props.StringProperty(
        default = "Remove Active Bone",
        )

    
    
    
    
    
    
    animesh_action : bpy.props.StringProperty(default="")






class BentoBuddyAnimeshGetCurrent(bpy.types.Operator):
    """Load the currently mapped rig setup into the Template Workshop"""
    bl_idname = "bentobuddy.animesh_get_current"
    bl_label = "Get map from Mapper"

    @classmethod
    def poll(cls, context):
        obj = bpy.data.objects
        ani = bpy.context.window_manager.bb_animesh
        bmp = bpy.context.window_manager.bb_mapper
        
        if bmp.mapper_enabled == True:
            return True
        return False

    def execute(self, context):
        obj = bpy.data.objects
        ani = bpy.context.window_manager.bb_animesh
        bmp = bpy.context.window_manager.bb_mapper

        source = bmp.mapper_source_name

        
        if obj[source].get('mapped') != 1:
            print("Not mapped yet, nothing to do")
            popup("Not mapped yet, nothing to do", "Map Missing", "INFO")
            return {'FINISHED'}

        
        
        

        
        
        
        
        
        
        
        

        
        
        arms = list()
        arms.append(source)
        for arm in bmp['targets']:
            arms.append(arm)
        arm_props = {}
        for arm in arms:
            arm_props.setdefault(arm, {})
            if obj[arm].get('bentobuddy_control_rig') != None:
                arm_props[arm]['bentobuddy_control_rig'] = obj[source]['bentobuddy_control_rig']
            if obj[arm].get('bone_map') != None:
                arm_props[arm]['bone_map'] = obj[source]['bone_map'].to_dict()
            if obj[arm].get('bone_data') != None:
                arm_props[arm]['bone_data'] = obj[source]['bone_data'].to_dict()
            if obj[arm].get('name') != None:
                arm_props[arm]['name'] = obj[source]['name']
            if obj[arm].get('mapped') != None:
                arm_props[arm]['mapped'] = obj[source]['mapped'] 
            if obj[arm].get('rig_type') != None:
                arm_props[arm]['rig_type'] = obj[source]['rig_type']

            
            if obj[arm].get('location') != None:
                arm_props[arm]['location'] = obj[source]['location']

            if obj[arm].get('role') != None:
                arm_props[arm]['role'] = obj[source]['role']

        
        
        targets = bmp['targets'].to_dict()

        
        bpy.ops.bentobuddy.mapper_reset()

        
        if len(bpy.context.selected_objects) > 0:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')

        
        obj[source].data.display_type = 'OCTAHEDRAL'
        obj[source].show_in_front = True

        
        
        

        
        bpy.ops.bentobuddy.animesh_reset()

        
        
        ani['template'] = arm_props[source]['bone_map']
        ani['targets_waiting'] = targets
        ani['targets'] = dict()

        

        obj[source].select_set(True)
        ani.animesh_lock_source = True
        obj[source].select_set(False)

        
        
        for tarm in targets:
            obj[tarm].select_set(True)
            bpy.context.view_layer.objects.active = obj[tarm]
            bpy.ops.bentobuddy.animesh_set_target(target=tarm)
            
            
            
            
            
            
            
            if len(ani['targets_waiting']) > 0:
                obj[tarm].select_set(False)

        return {'FINISHED'}






class BentoBuddyAnimeshLoad(bpy.types.Operator, ImportHelper):
    """Load a previously saved character template map into the set to continue work on it or to apply it to your rigs to test"""
    bl_idname = "bentobuddy.animesh_load"
    bl_label = "Load template"

    filename_ext = ".ctm"
    filter_glob : bpy.props.StringProperty(
        default='*.ctm;*.bbm',
        options={'HIDDEN'}
        )

    def execute(self, context):
        obj = bpy.data.objects
        ani = bpy.context.window_manager.bb_animesh

        filename = self.properties.filepath
        template_map = {}
        try:
            namespace = {}
            exec(open(filename, 'r', encoding='UTF8').read(), namespace)
            template_map.update(namespace['template_map'])
        except Exception as e:
            print(traceback.format_exc())
            return {'FINISHED'}

        
        bpy.ops.bentobuddy.animesh_reset()

        ani['template'] = template_map
        arms = {}
        for sbone in template_map:
            (tarm, tbone), = template_map[sbone].items()
            arms[tarm] = {}

        if len(arms) != 0:
            ani['targets_waiting'] = arms
            ani.animesh_message = "Select a target in scene, click armature button"

            
            
            ani.animesh_template_path = self.filepath
            
            ani['targets'] = dict()
            
            
            
            

        return {'FINISHED'}

    def invoke(self, context, event):
        load_path = script_dir + data_path
        self.filepath = load_path
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}













class BentoBuddyAnimeshRemoveTarget(bpy.types.Operator):
    """Remove this target from your list.  All targets must be processed before the workshop is enabled."""
    bl_idname = "bentobuddy.animesh_remove_target"
    bl_label = "Remove target map"

    target : bpy.props.StringProperty(default="")

    def execute(self, context):
        obj = bpy.data.objects
        ani = bpy.context.window_manager.bb_animesh

        
        
        
        del ani['targets_waiting'][self.target]
        if len(ani['targets_waiting']) == 0:
            ani.animesh_message = "Ready! Start picking."
            ani.animesh_template_path = ""

            
            
            
            source = ani.animesh_source_name

            
            for tarm in ani['targets']:
                obj[tarm]['bone_map'] = dict()
            
            bone_map = obj[source]['bone_map'].to_dict()
            for sbone in bone_map:
                (tarm, tbone), = bone_map[sbone].items()
                obj[tarm]['bone_map'][tbone] = {source : sbone}

            
            ani.animesh_bone_map = True

            
            

            
            remove_bone_groups(source)
            for tarm in ani['targets']:
                remove_bone_groups(tarm)

            create_bone_group(source, bb_source_group, bb_source_theme)
            for tarm in ani['targets']:
                create_bone_group(tarm, bb_target_group, bb_target_theme)
            
            
            
            bad_bones = {}
            for sbone in bone_map:
                (tarm, tbone), = bone_map[sbone].items()
                if tbone not in obj[tarm].data.bones:
                    bad_bones.setdefault(tarm, [])
                    bad_bones[tarm].append(tbone)
                    continue
                add_bone_to_group(armature=source, bone=sbone, group=bb_source_group)
                add_bone_to_group(armature=tarm, bone=tbone, group=bb_target_group)
            if len(bad_bones) > 0:
                txt = "There were some missing bones in your targets, they were skipped, check console for details."
                print("Missing bones in targets:", bad_bones)
                popup(txt, "Missing bones", "INFO")

            
            
            bpy.ops.object.select_all(action='DESELECT')
            
            bpy.context.view_layer.objects.active = bpy.data.objects[ani.animesh_source_name]
            
            for arm in ani['targets']:
                obj[arm].select_set(True)

            
            ani.animesh_lock_target = True

        else:
            ani.animesh_message = "Choose another target if needed"

        return {'FINISHED'}








class BentoBuddyAnimeshSetTarget(bpy.types.Operator):
    """Choose a target armature that is associated with the name displayed on this button.  When
you have processed them all the workshop will be enabled."""

    bl_idname = "bentobuddy.animesh_set_target"
    bl_label = "Set target"

    target : bpy.props.StringProperty(default="")

    @classmethod
    def poll(cls, context):
        ani = bpy.context.window_manager.bb_animesh
        if len(bpy.context.selected_objects) == 0:
            return False
        if ani.animesh_source_name == "":
            ani.animesh_message = "Choose your source first"
            return False
        else:
            ani.animesh_message = "Select a target then a button"
        if len(ani['targets']) > 0 and len(ani['targets_waiting']) != 0:
            ani.animesh_message = "Choose another target if you want"
        return True

    def execute(self, context):
        obj = bpy.data.objects
        ani = bpy.context.window_manager.bb_animesh

        
        

        if ani.animesh_action == "remove":
            print("BentoBuddyAnimeshSetTarget reports: removing target from list -", self.target)
            ani.animesh_action = ""
            del ani['targets'][self.target]
            return {'FINISHED'}

        for o in bpy.context.selected_objects:
            if o.type != 'ARMATURE':
                o.select_set(False)

        if len(bpy.context.selected_objects) == 0:
            txt = "No armatures were selected, this can only work with skeletons"
            print(txt)
            popup(txt, "Rigs Only", "ERROR")
            return {'FINISHED'}

        
        if len(bpy.context.selected_objects) > 1:
            txt = "Can only target one armature at a time with this method"
            print(txt)
            popup(txt, "Too many targets", "ERROR")
            return {'FINISHED'}

        
        armObj = bpy.context.selected_objects[0]

        
        
        if armObj.name == ani.animesh_source_name:
            txt = "Error: target cannot be the same as source"
            print(txt)
            popup(txt, "Circular dependency", "ERROR")
            return {'FINISHED'}

        
        if ani.get('targets') != None:
            if armObj.name in ani['targets'].keys():
                txt = "Error: already chosen as target"
                popup(txt, "Duplicate Target", "ERROR")
                return {'FINISHED'}
            ani['targets'].update({armObj.name : {}})
        else:
            ani['targets'] = dict()
            ani['targets'].update({armObj.name : {}})

        
        mapper.store_armature_data(armObj.name)

        

        
        
        
        
        
        
        
        
            

        obj[ani.animesh_source_name]['bone_map'] = dict()
        for sbone in ani['template']:
            (tarm, tbone), = ani['template'][sbone].items()
            
            
            
            if tarm == self.target:
                obj[ani.animesh_source_name]['bone_map'].update({sbone: {armObj.name: tbone}})

        
        ani.animesh_bone_map = True

        
        
        

        
        del ani['targets_waiting'][self.target]
        if len(ani['targets_waiting']) == 0:
            ani.animesh_message = "Ready! Start picking."
            ani.animesh_template_path = ""

            
            
            
            source = ani.animesh_source_name

            
            for tarm in ani['targets']:
                obj[tarm]['bone_map'] = dict()
            
            bone_map = obj[source]['bone_map'].to_dict()
            for sbone in bone_map:
                (tarm, tbone), = bone_map[sbone].items()
                obj[tarm]['bone_map'][tbone] = {source : sbone}

            
            
            
                
                
                
            

            
            

            
            remove_bone_groups(source)
            for tarm in ani['targets']:
                remove_bone_groups(tarm)

            create_bone_group(source, bb_source_group, bb_source_theme)
            for tarm in ani['targets']:
                create_bone_group(tarm, bb_target_group, bb_target_theme)

            
            
            sbone_error = False
            for sbone in bone_map:
                if sbone not in obj[source].data.bones:
                    print("Missing bone in source armature:", sbone)
                    sbone_error = True
                    continue

                (tarm, tbone), = bone_map[sbone].items()
                if tbone in obj[tarm].data.bones:
                    add_bone_to_group(armature=source, bone=sbone, group=bb_source_group)
                    add_bone_to_group(armature=tarm, bone=tbone, group=bb_target_group)
            if sbone_error == True:
                popup("There were source bones missing, this is probably not good, check console", "Error", "ERROR")

            
            
            bpy.ops.object.select_all(action='DESELECT')
            
            bpy.context.view_layer.objects.active = bpy.data.objects[ani.animesh_source_name]
            
            for arm in ani['targets']:
                obj[arm].select_set(True)

            
            ani.animesh_lock_target = True

        else:
            ani.animesh_message = "Choose another target if needed"

        return {'FINISHED'}




class BentoBuddyAnimeshSave(bpy.types.Operator, ExportHelper):
    """Save your character template map to a file"""
    bl_idname = "bentobuddy.animesh_save"
    bl_label = "Save template map"

    filename_ext = ".ctm"
    filter_glob : bpy.props.StringProperty(
        default='*.ctm',
        options={'HIDDEN'}
        )

    @classmethod
    def poll(cls, context):
        obj = bpy.data.objects
        ani = bpy.context.window_manager.bb_animesh

        
        if ani.animesh_mapper_enabled == False:
            return False
        
        if len(obj[ani.animesh_source_name]['bone_map']) == 0:
            return False

        return True

    def execute(self, context):
        obj = bpy.data.objects
        ani = bpy.context.window_manager.bb_animesh

        
        bpy.app.handlers.depsgraph_update_post.remove(animesh_mode)

        
        bone_map = obj[ani.animesh_source_name]['bone_map'].to_dict()

        
        template_map = "# Character Template Map auto-generated by Bento Buddy\n";
        template_map += "template_map = {\n"
        for sbone in bone_map:
            (tarm, tbone), = bone_map[sbone].items()
            template_map += "    " + '"' + sbone + '": ' + '{' + "\n"
            template_map += "        " + '"' + tarm +'": ' + '"' + tbone + '",' + "\n" + "        },\n"
        template_map += "    }\n"

        output = open(self.properties.filepath, 'w', encoding='UTF8')
        output.write(template_map)
        output.close()

        
        bpy.app.handlers.depsgraph_update_post.append(animesh_mode)

        return {'FINISHED'}

    def invoke(self, context, event):
        save_path = script_dir + data_path
        self.filepath = save_path
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}




class BentoBuddyAnimeshApply(bpy.types.Operator):
    """Apply retargeting map to selected rig"""
    bl_idname = "bentobuddy.animesh_apply"
    bl_label = "apply animesh map"

    @classmethod
    def poll(cls, context):
        obj = bpy.data.objects
        ani = bpy.context.window_manager.bb_animesh

        
        if ani.animesh_suspend == True:
            return False
        
        
        if ani.animesh_mapper_enabled == False:
            return False
        
        if 'targets' not in ani:
            return False
        
        if len(ani['targets']) == 0:
            return False
        
        if len(obj[ani.animesh_source_name]['bone_map']) == 0:
            return False

        return True

    def execute(self, context):
        obj = bpy.data.objects
        ani = bpy.context.window_manager.bb_animesh

        
        
        bpy.app.handlers.depsgraph_update_post.remove(animesh_mode)

        
        
        
        
        
        
        apply_transforms(object=ani.animesh_source_name, rotation=True, scale=True, location=True)
        
        apply_rest_pose(armature=ani.animesh_source_name)

        targets = list()
        for tarm in ani['targets']:
            targets.append(tarm)

        
        
        
        error = snap_to(source=ani.animesh_source_name)

        if error == False:
            print("snap_to reports: returned False, not good")

        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action = 'DESELECT')

        
        bpy.app.handlers.depsgraph_update_post.append(animesh_mode)

        return {'FINISHED'}








class BentoBuddyAnimeshAddTarget(bpy.types.Operator):
    """This only works in suspend mode.  Suspend your mapping, choose a rig and click (Add Rig) to include it into your set."""

    bl_idname = "bentobuddy.animesh_add_target"
    bl_label = "add a rig to set"

    @classmethod
    def poll(cls, context):
        obj = bpy.data.objects
        ani = bpy.context.window_manager.bb_animesh
        if ani.animesh_suspend != True:
            return False
        if ani.get('targets') == None:
            return False
        if len(bpy.context.selected_objects) == 0:
            return False
        
        for o in bpy.context.selected_objects:
            if o.type == 'ARMATURE':
                
                if o.name == ani.animesh_source_name:
                    return False
                if o.name in ani['targets']:
                    return False
                
                return True

        return False

    def execute(self, context):
        obj = bpy.data.objects
        ani = bpy.context.window_manager.bb_animesh

        
        o = bpy.context.selected_objects[0]
        ani['targets'][o.name] = {}
        o['bone_map'] = dict()
        o['name'] = o.name
        remove_bone_groups(o.name)
        create_bone_group(o.name, bb_target_group, bb_target_theme)
        mapper.store_armature_data(o.name)
        ani.animesh_targets += 1
        ani.animesh_message = "[SUSPENDED] " + o.name + " added"

        return {'FINISHED'}



class BentoBuddyAnimeshStore(bpy.types.Operator):
    """Store all of the bones' current position/rotation into the (Restore) buffer.  If you do this while (Apply) is still in effect,
    you will freeze those bones where they are, you may not want that."""

    bl_idname = "bentobuddy.animesh_store"
    bl_label = "store character map"

    @classmethod
    def poll(cls, context):
        obj = bpy.data.objects
        ani = bpy.context.window_manager.bb_animesh

        
        if ani.animesh_suspend == True:
            return False
        
        
        if ani.animesh_mapper_enabled == False:
            return False
        
        if 'targets' not in ani:
            return False
        
        if len(ani['targets']) == 0:
            return False

        return True

    def execute(self, context):
        obj = bpy.data.objects
        ani = bpy.context.window_manager.bb_animesh

        
        
        bpy.app.handlers.depsgraph_update_post.remove(animesh_mode)

        
        
        active = bpy.context.active_object.name

        
        apply_transforms(object=ani.animesh_source_name, rotation=True, scale=True, location=True)
        
        apply_rest_pose(armature=ani.animesh_source_name)
        
        obj[ani.animesh_source_name].select_set(True)
        for sel in ani['targets']:
            obj[sel].select_set(True)

        
        
        
        mapper.store_armature_data(armature=ani.animesh_source_name)

        
        ani.animesh_message = "Bone origins stored!"

        
        arms = list()
        arms.append(ani.animesh_source_name)
        for arm in ani['targets']:
            arms.append(arm)
        set_obj_mode_multi(mode="pose", objects=arms)
        
        bpy.context.view_layer.objects.active = bpy.data.objects[ani.animesh_source_name]

        
        bpy.app.handlers.depsgraph_update_post.append(animesh_mode)

        return {'FINISHED'}










class BentoBuddyAnimeshRestore(bpy.types.Operator):
    """Restore the bones to their original locations, this will not delete your work."""
    bl_idname = "bentobuddy.animesh_restore"
    bl_label = "restore rig"

    @classmethod
    def poll(cls, context):
        obj = bpy.data.objects
        ani = bpy.context.window_manager.bb_animesh

        
        if ani.animesh_suspend == True:
            return False
        
        
        if ani.animesh_mapper_enabled == False:
            return False
        
        if 'targets' not in ani:
            return False
        
        if len(ani['targets']) == 0:
            return False
        
        
        if len(obj[ani.animesh_source_name]['bone_map']) == 0:
            return False
        
        if len(obj[ani.animesh_source_name]['bone_data']) == 0:
            return False

        return True

    def execute(self, context):
        
        
        

        obj = bpy.data.objects
        ani = bpy.context.window_manager.bb_animesh

        
        
        bpy.app.handlers.depsgraph_update_post.remove(animesh_mode)

        
        
        
        
        return_value = mapper.restore_rig(armature=ani.animesh_source_name_backup, type="edit", data="all", roll=True)
        if return_value == False:
            print("BentoBuddyAnimeshRestore reports: restore_rig returned False")

        arms = ani['targets'].keys()
        arms.append(ani.animesh_source_name)
        set_obj_mode_multi(mode="pose", objects=arms)
        bpy.context.view_layer.objects.active = bpy.data.objects[ani.animesh_source_name]


        
        bpy.app.handlers.depsgraph_update_post.append(animesh_mode)

        return {'FINISHED'}




class BentoBuddyAnimeshReset(bpy.types.Operator):
    """This resets the template workshop as if you didn't do anything."""

    bl_idname = "bentobuddy.animesh_reset"
    bl_label = "Reset template workshop"

    def execute(self, context):
        print("got reset signal")

        obj = bpy.data.objects
        ani = bpy.context.window_manager.bb_animesh

        
        
        
        
        
        ani.animesh_bone_map = False
        ani.animesh_data_map = False

        
        
        
        ani.animesh_lock_source = False

        bb_settings['terminate'] = True
        ani.animesh_suspend = False

        return {'FINISHED'}







class BentoBuddyAnimeshRemoveSelectedBones(bpy.types.Operator):
    """This will remove all of the currently selected bones from the mapper or the sole active pose bone depending what stage you're in."""

    bl_idname = "bentobuddy.animesh_remove_selected_bones"
    bl_label = "remove animesh remove bones"

    @classmethod
    def poll(cls, context):
        obj = bpy.data.objects
        ani = bpy.context.window_manager.bb_animesh

        
        if ani.animesh_suspend == True:
            return
        if bpy.context.mode != 'POSE':
            return False

        if len(bpy.context.selected_pose_bones) == 0:
            if ani.animesh_source_bone != "":
                if ani.animesh_source_bone in obj[ani.animesh_source_name]['bone_map']:
                    ani.animesh_remove_bones_label = "Remove Current"
                    return True
                else:
                    ani.animesh_remove_bones_label = "Cancel [" + ani.animesh_source_bone + "]"
                    return True
            else:
                ani.animesh_remove_bones_label = "Select a bone"
                return False
        else:
            ani.animesh_remove_bones_label = "Remove selected bones"
            return True

        return True

    def execute(self, context):
        obj = bpy.data.objects
        ani = bpy.context.window_manager.bb_animesh

        
        
        
        




        
        
        
        if len(bpy.context.selected_pose_bones) == 0:

            
            
            
            if ani.animesh_source_bone in obj[ani.animesh_source_name]['bone_map']:
                bpy.ops.bentobuddy.animesh_remove_bone(bone=ani.animesh_source_bone)
                ani.animesh_source_bone = ""
                return {'FINISHED'}

            
            bpy.app.handlers.depsgraph_update_post.remove(animesh_mode)

            
            bpy.ops.pose.select_all(action = 'DESELECT')
            bpy.context.view_layer.objects.active = obj[ani.animesh_source_name]
            obj[ani.animesh_source_name].data.bones[ani.animesh_source_bone].select = True
            bpy.ops.pose.group_unassign()
            obj[ani.animesh_source_name].data.bones[ani.animesh_source_bone].select = False

            
            ani.animesh_source_bone = ""
            ani.animesh_rig = "source"

            
            for b in obj[ani.animesh_source_name].data.bones:
                b.hide_select = False
            for arm in ani['targets']:
                for b in obj[arm].data.bones:
                    b.hide_select = True

            
            bpy.app.handlers.depsgraph_update_post.append(animesh_mode)
            return {'FINISHED'}

        else:
            
            bone_list = list()
            for boneObj in bpy.context.selected_pose_bones:
                if boneObj.name not in obj[ani.animesh_source_name].pose.bones:
                    continue
                if boneObj.name not in obj[ani.animesh_source_name]['bone_map']:
                    continue
                bone_list.append(boneObj.name)

            for b in bone_list:
                
                
                bpy.ops.bentobuddy.animesh_remove_bone(bone=b)

            return {'FINISHED'}

        return {'FINISHED'}





class BentoBuddyAnimeshRemoveBone(bpy.types.Operator):
    """Remove this specific bone map from your set, this will NOT delete all of your work, only the associated bone map."""
    bl_idname = "bentobuddy.animesh_remove_bone"
    bl_label = "remove animesh remove bone"

    bone : bpy.props.StringProperty(default="")

    @classmethod
    def poll(cls, context):
        obj = bpy.data.objects
        ani = bpy.context.window_manager.bb_animesh

        
        if ani.animesh_suspend == True:
            return
        if bpy.context.mode != 'POSE':
            return False
        
        
        
            

        return True

    def execute(self, context):
        obj = bpy.data.objects
        ani = bpy.context.window_manager.bb_animesh

        
        
        bpy.app.handlers.depsgraph_update_post.remove(animesh_mode)

        
        (target, tbone), = obj[ani.animesh_source_name]['bone_map'][self.bone].items()

        
        active_obj = bpy.context.active_object.name

        activate(ani.animesh_source_name)

        
        bpy.ops.object.mode_set(mode='EDIT')
        error = restore_bone(armature=ani.animesh_source_name, bone=self.bone, type="edit", roll=True)
        if error == False:
            print("BentoBuddyRemoveBone reports: restore_bone returned False")
        bpy.ops.object.mode_set(mode='POSE')

        
        bpy.ops.pose.select_all(action = 'DESELECT')
        obj[ani.animesh_source_name].data.bones[self.bone].select = True
        bpy.ops.pose.group_unassign()
        obj[ani.animesh_source_name].data.bones[self.bone].select = False

        
        activate(target)

        bpy.ops.pose.select_all(action = 'DESELECT')
        obj[target].data.bones[tbone].select = True
        bpy.ops.pose.group_unassign()
        obj[target].data.bones[tbone].select = False

        del obj[ani.animesh_source_name]['bone_map'][self.bone]
        del obj[target]['bone_map'][tbone]

        
        activate(active_obj)

        
        bpy.app.handlers.depsgraph_update_post.append(animesh_mode)

        return {'FINISHED'}































