import bpy
import os
import json
from bpy_extras.io_utils import ImportHelper, ExportHelper

from . import ico
from . import utils
from .mod_settings import bb_settings

script_dir = os.path.dirname(os.path.abspath(__file__))
presets_path    =   bb_settings['paths']['presets']
data_path       =   bb_settings['paths']['data']














class BentoBuddyEditTemplateProperties(bpy.types.PropertyGroup):

    
    
    


    load_txt_reversed : bpy.props.BoolProperty(
        name = "",
        description =            "Load the text file with reversed bone order matching"            "\n\n"            "When making a text file to be converted into a CTM you'll usually put the name of the bone from the rig that you want to "            "convert into the first slot and then put the target system into the second slot.  These virtual (slots) are just a line "            "separated by a space.  Unfortunately some bones have spaces in them and the first bone cannot be defined with a space so "            "you may have to use the reverse in order to map your bones, if using a text file.  However, if both the source and the "            "target have spaces in their bones then even the reverse button, right here, won't help you and you'll have to map those "            "bones using this interface instead.  With that in mind, what this switch does is simple reverses the target/source order "            "after reading the file in and is just a convenience in case one of the systems doesn't have spaces in the bones.  Honestly "            "no bone should ever have a space, or white space, in its name but some armatures do this.",
        default = False
        )

    def update_info_bentobuddy_load_generic_template(self, context):
        
        if bb_settings['terminate'] == True:
            bb_settings['terminate'] = False
            return
        bbe = bpy.context.window_manager.bb_edit_template
        
        bb_settings['terminate'] = True
        bbe.info_bentobuddy_load_generic_template = False
        return
    info_bentobuddy_load_generic_template : bpy.props.BoolProperty(
        name = "Template Converter",
        description =            "\n"            "The button you have hovered over is informative only, read below...\n\n"            "This feature is provided in order to convert a template map from one type to another for use in various areas of Bento Buddy."            "\n",
        default = False,
        update = update_info_bentobuddy_load_generic_template,
    )

    disable_map_pose : bpy.props.BoolProperty(
        name = "Push this to disable loading the pose",
        description =            "When you're loading multiple maps you may want to keep a single working pose but not the rest.  Use this disable button "            "to prevent the loader from including the pose into the next loaded map.  When you have a pose in one of them that you're "            "sure about then you can re-enable the loading of the pose to allow the loader to record the included pose data.  In order to "            "check the pose, you can apply it to your skeleton in the Animation rollout and Enable Posing Library.  From there you can "            "load a pose from a CCM file to see what it looks like.  CTM files do not have poses in them so this can only apply to CCM.",
        default = False,
        )

    def update_info_bentobuddy_combine_generic_template(self, context):
        
        if bb_settings['terminate'] == True:
            bb_settings['terminate'] = False
            return
        bbe = bpy.context.window_manager.bb_edit_template
        
        bb_settings['terminate'] = True
        bbe.info_bentobuddy_combine_generic_template = False
        return
    info_bentobuddy_combine_generic_template : bpy.props.BoolProperty(
        name = "Combine Templates",
        description =            "\n"            "The button you have hovered over is informative only, read below...\n\n"            "This feature will allow you to load multiple modules to combine them for storing into a new map.  This merge "            "feature will allow you to work on different sections of your rig, or have multiple people working on different sections, "            "and then later combine them using this tool.  Each map that is loaded takes precedence over all other previously loaded maps, "            "which is to say, if there are duplicate mapped bones, the newest loaded map will override any existing duplicate maps."            "\n",
        default = False,
        update = update_info_bentobuddy_combine_generic_template,
    )

    
    
    

    message : bpy.props.StringProperty(default="look here for messages")

    
    show_map : bpy.props.BoolProperty(
        description =            "Click to expand and show the map"            "\n\n"            "A display of icons will appear for each source bone, target armature and target bone.  The icon is simply a dot with a color "            "legend indicating a bone state.  In standard mode the icons are black and you are simply editing maps without the need for any "            "armatures.  In map mode, as with the other mappers, there are at least 2 armatures required for active mapping.  In this state "            "the icon colors will be red, green or yellow.  "            "\n\n"            "Red - missing item"            "\n"            "Green - item matches"            "\n"            "Yellow - the item would match if not for the prefix"            "\n",
        default = False
    )

    
    show_rigs : bpy.props.BoolProperty(
        description =            "Click to enable and show a list of rigs contained within the template",
        default = False,
        
    )

    def update_source_active(self, context):
        bbe = bpy.context.window_manager.bb_edit_template
        if bbe.terminate == True:
            bbe.terminate = False
            return

        print("entered update for source_active")
        return 

    source_active : bpy.props.BoolProperty(
        description =            "Click to disable the active map, your changes will not be harmed but you need to save your work to a file using the save "            "feature because it does not save with the blender file",
        default = False,
        update = update_source_active
    )

    def update_move_name(self,context):
        bbe = bpy.context.window_manager.bb_edit_template
        if bbe.terminate == True:
            bbe.terminate = False
            return
        
        if bbe.move_name == bbe.move_name_backup:
            print("Property move_name updater running, no name change, returning")
            bbe.message = "Same name, nothing changed"
            del bbe['name']
            del bbe['item']
            return
        
        if bbe.move_name.strip() == "":
            print("we're not allowing empty names today, come back tomorrow")
            bbe.message = "Empty string"
            del bbe['name']
            del bbe['item']
            return

        
        
        
        
        
        
        
        tarms = dict()
        for sbone in bbe['template_editing']:
            (tarm, tbone), = bbe['template_editing'][sbone].items()
            tarms[tarm] = tbone

        
        if bbe.move_name in tarms:
            
            
            
            

            
            
            
            template_new = dict()
            target_bones = dict()
            for sbone in bbe['template_editing']:
                (tarm, tbone), = bbe['template_editing'][sbone].items()
                if tarm == bbe.move_name_backup:
                    template_new[sbone] = {bbe.move_name : tbone}
                    target_bones[tbone] = ""
            
            for sbone in bbe['template_editing']:
                (tarm, tbone), = bbe['template_editing'][sbone].items()
                if tarm == bbe.move_name_backup:
                    continue
                if tbone in target_bones:
                    continue
                template_new[sbone] = {tarm : tbone}

        
        
        
        
        else:
            template_new = dict()
            for sbone in bbe['template_editing']:
                (tarm, tbone), = bbe['template_editing'][sbone].items()
                
                if tarm == bbe.move_name_backup:
                    template_new[sbone] = {bbe.move_name : tbone}
            for sbone in bbe['template_editing']:
                (tarm, tbone), = bbe['template_editing'][sbone].items()
                
                if tarm == bbe.move_name_backup:
                    continue
                template_new[sbone] = {tarm : tbone}

        bbe.message = "rig name changed from " + bbe.move_name_backup + " to " + bbe.move_name
        bbe['template_editing'] = template_new

        
        if bbe.get('template_editing_undo'):
            del bbe['template_editing_undo']

        del bbe['name']
        del bbe['item']

    def update_sbone_name(self,context):
        bbe = bpy.context.window_manager.bb_edit_template
        if bbe.terminate == True:
            bbe.terminate = False
            return
        
        if bbe.sbone_name == bbe.sbone_name_backup:
            print("Property sbone_name updater running, no name change, returning")
            bbe.message = "Same name, nothing changed"
            del bbe['name']
            del bbe['item']
            return
        
        if bbe.sbone_name.strip() == "":
            print("we're not allowing empty names today, come back tomorrow")
            bbe.message = "Empty string"
            del bbe['name']
            del bbe['item']
            return
        
        if bbe.sbone_name in bbe['template_editing']:
            print("Name collision, change the name of the other one if you want to move this stream")
            bbe.message = "[The name " + '"' + bbe.sbone_name + '"' + " would collide with another bone" + "]"
            del bbe['name']
            del bbe['item']
            return

        print("Property sbone_name updater running to change bone map from", bbe.sbone_name_backup, "to", bbe.sbone_name)

        
        last_edit = {}
        
        bbe['template_editing_undo'] = dict()
        bbe['template_editing_undo']['old'] = {}
        bbe['template_editing_undo']['new'] = {}
        bbe['template_editing_undo']['map'] = {}
        bbe['template_editing_undo']['old'][bbe.sbone_name_backup] = bbe['template_editing'][bbe.sbone_name_backup]
        
        bbe['template_editing_undo']['new'][bbe.sbone_name] = bbe['template_editing'][bbe.sbone_name_backup]
        
        
        
        bbe['template_editing_undo']['map'][bbe.sbone_name] = bbe.sbone_name_backup

        
        template = bbe['template_editing'].to_dict()
        template_new = dict()
        template_new[bbe.sbone_name] = template[bbe.sbone_name_backup]
        for t in template:
            if t == bbe.sbone_name_backup:
                continue
            template_new[t] = template[t]

        bbe.sbone_name_backup = bbe.sbone_name
        bbe['template_editing'] = template_new

        
        del bbe['name']
        del bbe['item']

        bbe.message = "name changed"

        return

    
    
    
    
    
    
    def update_tbone_name(self,context):
        bbe = bpy.context.window_manager.bb_edit_template
        if bbe.terminate == True:
            bbe.terminate = False
            return

        
        sbone = bbe['name']

        

        
        
        
        
        
        (tarm, tbone), = bbe['template_editing'][sbone].items()

        
        if bbe.tbone_name == bbe.tbone_name_backup:
            print("Property tbone_name updater running, no name change, returning")
            bbe.message = "Same name, nothing changed"
            del bbe['name']
            del bbe['item']
            return
        
        if bbe.tbone_name.strip() == "":
            print("we're not allowing empty names today, come back tomorrow")
            bbe.message = "Empty string"
            del bbe['name']
            del bbe['item']
            return

        
        

        tbone_items = set()
        for k in bbe['template_editing']: 
            (rig, tbone), = bbe['template_editing'][k].items()
            if rig == tarm:
                tbone_items.add(tbone)

        
        if bbe.tbone_name in tbone_items:
            print("Name collision, change the name of the other one if you want to move this stream")
            bbe.message = "The name " + '"' + bbe.tbone_name + '"' + " would collide with another bone"
            del bbe['name']
            del bbe['item']
            return

        print("Property tbone_name updater running to change target from", tarm, bbe.tbone_name_backup, "to", tarm, bbe.tbone_name)

        
        last_edit = {}
        
        bbe['template_editing_undo'] = dict()
        bbe['template_editing_undo']['old'] = {}
        bbe['template_editing_undo']['new'] = {}
        bbe['template_editing_undo']['map'] = {}
        bbe['template_editing_undo']['old'][sbone] = bbe['template_editing'][sbone]
        
        bbe['template_editing_undo']['new'][sbone] = {tarm : bbe.tbone_name}
        
        bbe['template_editing_undo']['map'][bbe.tbone_name] = bbe.tbone_name_backup

        
        template = bbe['template_editing'].to_dict()
        template_new = dict()
        template_new[sbone] = {tarm : bbe.tbone_name}

        for t in template:
            if t == sbone:
                continue
            template_new[t] = template[t]

        bbe.tbone_name_backup = bbe.tbone_name
        bbe['template_editing'] = template_new

        del bbe['name']
        del bbe['item']

        bbe.message = "name changed"

        return

    def update_tarm_name(self,context):
        bbe = bpy.context.window_manager.bb_edit_template
        if bbe.terminate == True:
            bbe.terminate = False
            return

        
        sbone = bbe['name']

        

        
        (tarm, tbone), = bbe['template_editing'][sbone].items()

        
        if bbe.tarm_name == bbe.tarm_name_backup:
            print("Property tarm_name updater running, no name change, returning")
            bbe.message = "Same name, nothing changed"
            del bbe['name']
            del bbe['item']
            return
        
        if bbe.tarm_name.strip() == "":
            print("we're not allowing empty names today, come back tomorrow")
            bbe.message = "Empty string"

            del bbe['name']
            del bbe['item']
            return
        
        
        tarm_items = {}
        for k in bbe['template_editing']:
            (arm, bone), = bbe['template_editing'][k].items()
            if bbe.tarm_name == arm:
                
                print("The target armature rename would have collided:", tarm)
                bbe.message = bbe.tarm_name + " would have collided, use rig options to merge"
                del bbe['name']
                del bbe['item']
                return

        
        last_edit = {}
        
        bbe['template_editing_undo'] = dict()
        bbe['template_editing_undo']['old'] = {}
        bbe['template_editing_undo']['new'] = {}
        bbe['template_editing_undo']['map'] = {}
        bbe['template_editing_undo']['old'][sbone] = bbe['template_editing'][sbone]
        
        bbe['template_editing_undo']['new'][sbone] = {bbe.tarm_name : tbone}
        
        bbe['template_editing_undo']['map'][bbe.tarm_name] = bbe.tarm_name_backup

        
        template = bbe['template_editing'].to_dict()
        template_new = dict()
        template_new[sbone] = {bbe.tarm_name : tbone}

        for t in template:
            if t == sbone:
                continue
            template_new[t] = template[t]

        bbe.tarm_name_backup = bbe.tarm_name
        bbe['template_editing'] = template_new
        del bbe['name']
        del bbe['item']

        bbe.message = "name changed"

        return

    
    
    
    
    
    move_name : bpy.props.StringProperty(default="", update=update_move_name)
    move_name_backup : bpy.props.StringProperty(default="")
    tarm_name : bpy.props.StringProperty(default="", update=update_tarm_name)
    tarm_name_backup : bpy.props.StringProperty(default="")
    sbone_name : bpy.props.StringProperty(default="", update=update_sbone_name)
    sbone_name_backup : bpy.props.StringProperty(default="")
    tbone_name : bpy.props.StringProperty(default="", update=update_tbone_name)
    tbone_name_backup : bpy.props.StringProperty(default="")

    
    
    
    
    
    terminate : bpy.props.BoolProperty(default=False)











class BentoBuddyLoadGenericTemplate(bpy.types.Operator, ImportHelper):
    """Here you can convert one template type to another
This section contains an info button (!), hover over it for detailed information."""

    
    

    bl_idname = "bentobuddy.load_generic_template"
    bl_label = "Load *.ccm, *.ctm"

    filter_glob : bpy.props.StringProperty(
        default='*.ccm;*.ctm',
        options={'HIDDEN'}
        )

    
    
    
    
        
        
        

    def execute(self, context):
        obj = bpy.data.objects
        bbe = bpy.context.window_manager.bb_edit_template
        path = self.properties.filepath

        try:
            namespace = {}
            exec(open(path, 'r', encoding='UTF8').read(), namespace)
        except Exception as e:
            print(traceback.format_exc())
            return {'FINISHED'}

        template = {}
        for container in namespace:
            
            if container.startswith("__"):
                continue
            template[container] = namespace[container]

        


        
        if template != None:
            bbe['template_map_convert'] = {}

            
            bbe['template_map_convert'] = template




                
                
                
                
                
                


        
        
        if 'template_map' in template:
            bbe['map_type_convert'] = "ctm"
        if 'rename' in template:
            bbe['map_type_convert'] = "ccm"

        return {'FINISHED'}

    def invoke(self, context, event):
        load_path = script_dir + data_path
        self.filepath = load_path
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}









class BentoBuddySaveCCM(bpy.types.Operator, ExportHelper):
    bl_idname = "bentobuddy.save_ccm"
    bl_label = "Save Converted Template"

    
    filename_ext = ".ccm"

    filter_glob : bpy.props.StringProperty(
        default='*.ccm',
        options={'HIDDEN'}
        )

    
    @classmethod
    def poll(cls, context):
        bbe = bpy.context.window_manager.bb_edit_template
        if bbe.get('template_map_convert') == None:
            return False
        if bbe['template_map_convert'] == "":
            return False
        if bbe.get('map_type_convert') == None:
            return False
        if bbe['map_type_convert'] == "ccm":
            return False
        return True

    def execute(self, context):
        bbe = bpy.context.window_manager.bb_edit_template
        path = self.properties.filepath

        
        if bbe['map_type_convert'] == "ccm":
            txt = "Conversion type is the same as the loaded map: " + bbe['map_type']
            print(txt)
            utils.popup(txt, "Error", "ERROR")
            return {'FINISHED'}

        
        
        

        
        template = bbe['template_map_convert']['template_map'].to_dict()

        
        container = dict()
        for mbone in template:
            (tarm, tbone), = template[mbone].items()
            container[tbone] = mbone

        formatted_maps = "# Auto generated by Bento Buddy - Character Converter from CTM\n"
        rename_maps = "rename = {\n";

        for tbone in container:
            rename_maps += "    " + '"' + tbone + '": ' + '"' + container[tbone] + '"' + ",\n"
        rename_maps += "    }\n"

        
        formatted_maps += rename_maps

        output = open(path, 'w', encoding='UTF8')
        output.write(formatted_maps)
        output.close()

        
        del bbe['template_map_convert']
        del bbe['map_type_convert']

        return {'FINISHED'}

    def invoke(self, context, event):
        save_path = script_dir + data_path
        self.filepath = save_path
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}




class BentoBuddySaveCTM(bpy.types.Operator, ExportHelper):
    bl_idname = "bentobuddy.save_ctm"
    bl_label = "Save Converted Template"

    
    filename_ext = ".ctm"

    filter_glob : bpy.props.StringProperty(
        default='*.ctm',
        options={'HIDDEN'}
        )

    
    @classmethod
    def poll(cls, context):
        bbe = bpy.context.window_manager.bb_edit_template
        if bbe.get('template_map_convert') == None:
            return False
        if bbe['template_map_convert'] == "":
            return False
        if bbe.get('map_type_convert') == None:
            return False
        if bbe['map_type_convert'] == "ctm":
            return False
        return True

    def execute(self, context):
        bbe = bpy.context.window_manager.bb_edit_template
        path = self.properties.filepath

        
        if bbe['map_type_convert'] == "ctm":
            txt = "Conversion type is the same as the loaded map: " + bbe['map_type']
            print(txt)
            utils.popup(txt, "Error", "ERROR")
            return {'FINISHED'}

        
        template = bbe['template_map_convert'].to_dict()

        
        

        
        target = "arm_" + utils.get_unique_name_short()

        container = dict()
        for tbone in template['rename']:
            mbone = template['rename'][tbone]
            container[mbone] = {target: tbone}


        formatted_maps = "# Character Template Map auto-generated by Bento Buddy from CCM\n"
        formatted_maps += "template_map = {\n"
        for sbone in container:
            (tarm, tbone), = container[sbone].items()
            formatted_maps += "    " + '"' + sbone + '": ' + '{' + "\n"
            formatted_maps += "        " + '"' + tarm +'": ' + '"' + tbone + '",' + "\n" + "        },\n"
        formatted_maps += "    }\n"

        output = open(path, 'w', encoding='UTF8')
        output.write(formatted_maps)
        output.close()

        
        del bbe['template_map_convert']

        return {'FINISHED'}

    def invoke(self, context, event):
        save_path = script_dir + data_path
        self.filepath = save_path
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}








class BentoBuddyCombineGenericTemplate(bpy.types.Operator, ImportHelper):
    """Here you can load multiple templates to create a composition that had
previously been mapped separately, see (!) button"""

    bl_idname = "bentobuddy.combine_generic_template"
    bl_label = "Load *.ccm, *.ctm"

    filter_glob : bpy.props.StringProperty(
        default='*.ccm;*.ctm',
        options={'HIDDEN'}
        )

    
    
        
        
        

    def execute(self, context):
        obj = bpy.data.objects
        bbe = bpy.context.window_manager.bb_edit_template
        path = self.properties.filepath

        low_path = path.lower()
        if low_path.endswith("." + "ccm"):
            my_type = "ccm"
        elif low_path.endswith("." + "ctm"):
            my_type = "ctm"
        else:
            print("BentoBuddyCombineGenericTemplate reports: Unknown map type in file - ", path)
            utils.popup("Unknown map type in file, check console for details", "Error", "ERROR")
            return {'FINISHED'}

        
        
        if bbe.get('map_type_combine') != None:
            if bbe['map_type_combine'] == my_type:
                pass
            else:
                print("BentoBuddyCombineGenericTemplate reports: existing template is", bbe['map_type_combine'], "but user wants something else")
                txt = "You can only combine maps of the same type.  To start over use the reset button"
                print(txt)
                utils.popup(txt, "Error", "ERROR")
                return {'FINISHED'}
        
        else:
            bbe['map_type_combine'] = my_type

        path_head, path_tail = os.path.split(path)

        print("Adding module: filename:", path_tail)

        try:
            namespace = {}
            exec(open(path, 'r', encoding='UTF8').read(), namespace)
        except Exception as e:
            print(traceback.format_exc())
            return {'FINISHED'}

        template = {}
        for container in namespace:
            
            if container.startswith("__"):
                continue
            template[container] = namespace[container]

        
        
        if template != "":
            
            if bbe.get('template_map_combine') == None:
                bbe['template_map_combine'] = {}
                
                bbe['map_files_combine'] = [path_tail]
            
            else:

                print("---------------------------------------------------------------")
                print("path_tail")

                print("---------------------------------------------------------------")


                if bbe.get('map_files_combine') == None:
                    bbe['map_files_combine'] = list()
                if path_tail in bbe['map_files_combine']:
                    txt = "BentoBuddyCombineGenericTemplate reports: already recorded - " + path_tail
                    print(txt)
                    utils.popup(txt, "Error", "ERROR")
                    return {'FINISHED'}

                map_files = bbe['map_files_combine']
                map_files.append(path_tail)
                bbe['map_files_combine'] = map_files

            
            
            
            
            
            template_map = bbe['template_map_combine'].to_dict()
            for root_key in template:
                if template_map.get(root_key) == None:
                    template_map[root_key] = dict()
                for sub_key in template[root_key]:
                    template_map[root_key].update({sub_key : template[root_key][sub_key]})

            for root_key in template_map:
                
                
                
                
                if root_key == "pose":
                    if bbe.disable_map_pose == True:
                        continue

            bbe['template_map_combine'] = template_map

        return {'FINISHED'}

    def invoke(self, context, event):
        load_path = script_dir + data_path
        self.filepath = load_path
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}




class BentoBuddySaveCombinedCCM(bpy.types.Operator, ExportHelper):
    bl_idname = "bentobuddy.save_combined_ccm"
    bl_label = "Save Combined Template"

    
    filename_ext = ".ccm"

    filter_glob : bpy.props.StringProperty(
        default='*.ccm',
        options={'HIDDEN'}
        )

    def execute(self, context):
        bbe = bpy.context.window_manager.bb_edit_template
        path = self.properties.filepath




        
        
        template = bbe['template_map_combine'].to_dict()

        formatted_maps = "# Auto generated by Bento Buddy - Character Converter from Combined CCM\n"
        for k in template:
            formatted_maps += k + " = "
            formatted_maps += json.dumps(template[k], indent=4)
            formatted_maps += "\n"

        output = open(path, 'w', encoding='UTF8')
        output.write(formatted_maps)
        output.close()

        
        del bbe['template_map_combine']
        del bbe['map_type_combine']

        return {'FINISHED'}

    def invoke(self, context, event):
        save_path = script_dir + data_path
        self.filepath = save_path
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}




class BentoBuddySaveCombinedCTM(bpy.types.Operator, ExportHelper):
    bl_idname = "bentobuddy.save_combined_ctm"
    bl_label = "Save Combined Template"

    
    filename_ext = ".ctm"

    filter_glob : bpy.props.StringProperty(
        default='*.ctm',
        options={'HIDDEN'}
        )

    def execute(self, context):
        bbe = bpy.context.window_manager.bb_edit_template
        path = self.properties.filepath

        template = bbe['template_map_combine'].to_dict()

        formatted_maps = "# Character Template Map auto-generated by Bento Buddy from CTM\n"

        for k in template:
            formatted_maps += k + " = "
            formatted_maps += json.dumps(template[k], indent=4)
            formatted_maps += "\n"

        output = open(path, 'w', encoding='UTF8')
        output.write(formatted_maps)
        output.close()

        
        del bbe['template_map_combine']
        del bbe['map_type_combine']

        return {'FINISHED'}

    def invoke(self, context, event):
        save_path = script_dir + data_path
        self.filepath = save_path
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}




class BentoBuddyResetCombinedTemplates(bpy.types.Operator):
    """Click to reset the composer so you can have a clean slate"""
    bl_idname = "bentobuddy.reset_template_composer"
    bl_label = "Reset Composer"

    def execute(self, context):
        bbe = bpy.context.window_manager.bb_edit_template
        del bbe['template_map_combine']
        del bbe['map_type_combine']
        del bbe['map_files_combine']
        return {'FINISHED'}









class BentoBuddyEditTemplateNewCTM(bpy.types.Operator):
    """Start a new map
"""









    bl_idname = "bentobuddy.edit_template_new_ctm"
    bl_label = "Create a new template"


    def execute(self, context):
        bbe = bpy.context.window_manager.bb_edit_template

        if bbe.get('template_editing') != None:
            print("Create new CTM runs but there's already a template in the mapper")
            utils.popup("You have an active ctm, reset it to start a new one", "Template Exists", "INFO")
            return {'FINISHED'}



        sbone = utils.get_unique_name_short()
        tarm = utils.get_unique_name_short()
        tbone = utils.get_unique_name_short()
        bbe['template_editing'] = {sbone: {tarm: tbone}}

        return {'FINISHED'}




class BentoBuddyEditTemplateLoadFromTXT(bpy.types.Operator, ImportHelper):
    """Load a text file to create a template from that file.  The format for this file is one bone
map per line.  The SL bone is first and the second part is the target bone on the same line.
SL bones don't have spaces but your target can.
"""

    bl_idname = "bentobuddy.edit_template_load_txt"
    bl_label = "Open TXT"

    filename_ext = ".txt"

    filter_glob : bpy.props.StringProperty(
        default='*.txt',
        options={'HIDDEN'}
        )

    def invoke(self, context, event):
        save_path = script_dir + data_path
        self.filepath = save_path
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        bb_edit_template = bpy.context.window_manager.bb_edit_template
        bpy.ops.bentobuddy.edit_template_reset()

        template = {}

        try:
            with open(self.filepath, encoding='UTF8') as fh:
                for line in fh:
                    test_list = line.split()
                    if len(test_list) < 2:
                        continue
                    sbone, tbone = line.strip().split(' ', 1)
                    template[sbone] = tbone.strip()
        except Exception as e:
            print("Couldn't read:", self.filepath)
            print(traceback.format_exc())
            utils.popup("Couldn't read file", "Error reading", "ERROR")
            return {'FINISHED'}

        
        

        
        
        
        
        
        used_targets = {}
        duplicates = {}
        template_map = {}
        for sbone in template:
            tbone = template[sbone]
            if tbone in used_targets:
                duplicates[tbone] = ""
                continue
            if bb_edit_template.load_txt_reversed == True:
                used_targets[sbone] = "" 
                template_map[tbone] = {}
                template_map[tbone]["Target"] = sbone

            else:
                used_targets[tbone] = "" 
                template_map[sbone] = {}
                template_map[sbone]["Target"] = tbone

        if len(duplicates) > 0:
            print("There were duplicate targets in your map, they were removed:", duplicates)
            utils.popup("Duplicates were found and removed, see console.", "Info", "INFO")

        bb_edit_template['template_editing'] = template_map

        return {'FINISHED'}




class BentoBuddyEditTemplateLoadFromCTM(bpy.types.Operator, ImportHelper):
    """Load a CTM into the manual editor.
"""

    bl_idname = "bentobuddy.edit_template_load_ctm"
    bl_label = "Edit Template"

    filename_ext = ".ctm"

    
    
    target : bpy.props.StringProperty(default="template_editing")

    filter_glob : bpy.props.StringProperty(
        default='*.ctm',
        options={'HIDDEN'}
        )

    def invoke(self, context, event):
        save_path = script_dir + data_path
        self.filepath = save_path
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        bb_edit_template = bpy.context.window_manager.bb_edit_template
        bpy.ops.bentobuddy.edit_template_reset()

        try:
            namespace = {}
            exec(open(self.filepath, 'r', encoding='UTF8').read(), namespace)
        except Exception as e:
            print("error loading ctm")
            print(traceback.format_exc())
            return {'FINISHED'}

        template_map = {}
        try:
            template_map.update(namespace['template_map'])
        except:
            txt = "No template_map found in the ctm"
            print(txt)
            utils.popup(txt, "Error", "ERROR")
            return {'FINISHED'}

        
        
        
        bb_edit_template[self.target] = template_map

        return {'FINISHED'}




class BentoBuddyEditTemplateSaveFromCTM(bpy.types.Operator, ExportHelper):
    """Save your loaded map as a CTM
"""
    bl_idname = "bentobuddy.edit_template_save_ctm"
    bl_label = "Save Template"

    filename_ext = ".ctm"
    filter_glob : bpy.props.StringProperty(
        default='*.ctm',
        options={'HIDDEN'}
        )

    def invoke(self, context, event):
        save_path = script_dir + data_path
        self.filepath = save_path
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        bb_edit_template = bpy.context.window_manager.bb_edit_template

        if bb_edit_template.get('template_editing'):

            template_map = bb_edit_template['template_editing'].to_dict()
            formatted_text = utils.format_ctm(template_map)

            try:
                f = open(self.filepath, "w", encoding='UTF8')
                f.write(formatted_text)
                f.close()
                
                print("Template saved as:", self.filepath)
            except Exception as e:
                
                print("Couldn't write file:", self.filepath)
                print(traceback.format_exc())
        else:
            print("Property (template_editing) was missing when attempting to access it, we got ghosts!")

        return {'FINISHED'}




class BentoBuddyEditTemplatePickSource(bpy.types.Operator):
    """Picking a source rig enables the active mapping process where you can pick bones in
the interface for your source and targets.  Even this mapping process is for data only and
does not actually do anything except build a data set for you"""

    bl_idname = "bentobuddy.edit_template_pick_source"
    bl_label = "Choose a rig for your source bones and click this button\n"

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) != 1:
            return False
        if bpy.context.selected_objects[0].type == 'ARMATURE':
            return True
        return False

    def execute(self, context):
        bbe = bpy.context.window_manager.bb_edit_template
        obj = bpy.data.objects

        armObj = bpy.context.selected_objects[0]
        sarm = armObj.name
        print("source picked", sarm)
        bbe.terminate = True
        bbe.source_active = True
        return {'FINISHED'}




class BentoBuddyEditTemplatePickTarget(bpy.types.Operator):
    """Choose a target rig and click this button to add it to your map.
"""

    bl_idname = "bentobuddy.edit_template_pick_target"
    bl_label = "Choose a target rig\n"

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) != 1:
            return False
        if bpy.context.selected_objects[0].type != 'ARMATURE':
            return False

        
        
        
        bbe = bpy.context.window_manager.bb_edit_template
        return bbe.source_active

    def execute(self, context):
        bbe = bpy.context.window_manager.bb_edit_template
        obj = bpy.data.objects

        armObj = bpy.context.selected_objects[0]
        tarm = armObj.name
        print("target picked", tarm)
        bbe.terminate = True

        if bbe.get('template_editor_targets') == None:
            bbe['template_editor_targets'] = dict()

        if tarm in bbe['template_editor_targets']:
            print("target exists already:", tarm)
            utils.popup("Target already chosen", "Info", "INFO")
        else:
            bbe['template_editor_targets'][tarm] = {}

        return {'FINISHED'}







class BentoBuddyEditTemplateMoveTarget(bpy.types.Operator):
    """WARNING: This will merge or rename a rig stream.  Any target bones that match
within a merger will be overwritten by the renamed stream.  There is no recovery from this.
Any stored undo will be removed
"""

    bl_idname = "bentobuddy.edit_template_move_target"
    bl_label = "Click to globally change the rig name or merge\n"

    
    
    
    name : bpy.props.StringProperty(default="")

    def execute(self, context):
        bbe = bpy.context.window_manager.bb_edit_template
        obj = bpy.data.objects

        
        if self.name == bbe.get('name'):
            
            
            del bbe['name']
            del bbe['item']
            return {'FINISHED'}

        
        
        

        
        
        bbe['item'] = "move"
        bbe['name'] = self.name

        
        
        

        
        
        bbe.terminate = True
        bbe.move_name = self.name
        bbe.move_name_backup = self.name

        return {'FINISHED'}






    

    
    

    

    
        
        







class BentoBuddyEditTemplateRemoveTarget(bpy.types.Operator):
    """WARNING:  This will remove a target rig from your map completely.  This
is not usually what you need but it's here for convenience.
"""

    bl_idname = "bentobuddy.edit_template_remove_target"
    bl_label = "Click to globally remove a target from your map\n"

    
    
    
    name : bpy.props.StringProperty(default="")

    def execute(self, context):
        bbe = bpy.context.window_manager.bb_edit_template
        obj = bpy.data.objects

        
        if self.name == bbe.get('name'):
            
            
            del bbe['name']
            del bbe['item']
            return {'FINISHED'}

        print("Removing target armature stream for:", self.name)

        
        template_new = {}
        template = bbe['template_editing'].to_dict()
        for sbone in template:
            (tarm, tbone), = template[sbone].items()
            if tarm == self.name:
                continue
            template_new[sbone] = {tarm : tbone}

        bbe['template_editing'] = template_new
        bbe.terminate = True
        bbe.move_name = ""
        bbe.move_name_backup = ""

        
        if bbe.get('name'):
            del bbe['name']
        if bbe.get('item'):
            del bbe['item']

        
        if len(bbe['template_editing']) == 0:
            
            
            
            print("All target rigs were removed, resetting")
            bpy.ops.bentobuddy.edit_template_reset()

        
        if bbe.get('template_editing_undo'):
            undo_stream = bbe['template_editing_undo']['new'].to_dict()
            (sbone, tarm_tbone), = undo_stream.items()
            (tarm, tbone), = tarm_tbone.items()
            if tarm == self.name:
                print("removed undo for target armature:", self.name)
                del bbe['template_editing_undo']

        return {'FINISHED'}



class BentoBuddyEditTemplateReset(bpy.types.Operator):
    """This will clear out the editor, make sure you saved your work if you want to keep it"""

    bl_idname = "bentobuddy.edit_template_reset"
    bl_label = "Edit Template Reset"

    def execute(self, context):
        
        
        bbe = bpy.context.window_manager.bb_edit_template
        if bbe.get('template_editing') != None:
            del bbe['template_editing']
        if bbe.get('template_editing_undo') != None:
            del bbe['template_editing_undo']
        if bbe.get('item') != None:
            del bbe['item']
        if bbe.get('name') != None:
            del bbe['name']

        bbe.show_rigs = False
        bbe.terminate = True
        bbe.move_name = ""
        bbe.move_name_backup = ""
        bbe.terminate = True
        bbe.source_active = False

        bbe.item_name = ""
        bbe.item_name_backup = ""

        return {'FINISHED'}



class BentoBuddyEditTemplateRemoveBone(bpy.types.Operator):
    """The X indicates a state:

red, source is a root bone but target is not
white/black, target is a root bone but source is not
white, root to root
black, not in map mode"""

    bl_idname = "bentobuddy.edit_template_remove_bone"
    bl_label = "Click to remove this bone from the map\n"

    bone : bpy.props.StringProperty(default="")

    def execute(self, context):
        bbe = bpy.context.window_manager.bb_edit_template
        try:
            del bbe['template_editing'][self.bone]
            if len(bbe['template_editing']) == 0:
                del bbe['template_editing']
            print("Removed", self.bone)
        except:
            print("Couldn't remove bone, this is weird:", self.bone)

        
        if bbe.get('template_editing_undo') != None:
            undo_stream = bbe['template_editing_undo']['new'].to_dict()
            (sbone, tarm_tbone), = undo_stream.items()
            if self.bone == sbone:
                print("removed undo for bone:", self.bone)
                del bbe['template_editing_undo']

        return {'FINISHED'}



class BentoBuddyEditTemplateAddBone(bpy.types.Operator):
    """Add a bone to the map.  Unique names will be given to each element.  Obviously
you'll want to rename them to bones and rigs you'll expect to be working with.  If you
get an error about a collision just try again
"""
    bl_idname = "bentobuddy.edit_template_add_bone"
    bl_label = "Click to manually add a bone to the mapper\n"

    def execute(self, context):
        bbe = bpy.context.window_manager.bb_edit_template

        
        sbone = utils.get_unique_name_short()
        tarm = utils.get_unique_name_short()
        tbone = utils.get_unique_name_short()

        tarm = sbone
        tbone = sbone

        if sbone in bbe['template_editing']:
            print("uuid was present in the map as a source bone, maybe try again?")
            utils.popup("the uniquly created name for the source bone existed in the map, see console", "Collision", "ERROR")
            return {'FINISHED'}

        
        
        template = bbe['template_editing'].to_dict()
        template_new = dict()
        template_new[sbone] = {}
        template_new[sbone][tarm] = tbone

        print("BentoBuddyEditTemplateAddBone : Generated bone defs:", sbone, tarm, tbone)

        for sbone in template:
            (tarm, tbone), = template[sbone].items()
            template_new[sbone] = {}
            template_new[sbone][tarm] = tbone

        bbe['template_editing'] = template_new

        return {'FINISHED'}








class BentoBuddyEditTemplateChangeRigName(bpy.types.Operator):
    """This changes a single bone branch and will split into a different stream.
This is usually not what you want, if you want to rename a rig globally use the
Rig Tools options
"""

    bl_idname = "bentobuddy.edit_template_change_rig_name"
    bl_label = "Click to change the name of the target rig\n"

    
    
    name : bpy.props.StringProperty(default="")

    def execute(self, context):
        bb_edit_template = bpy.context.window_manager.bb_edit_template
        obj = bpy.data.objects

        
        if self.name == bb_edit_template.get('name'):
            
            
            del bb_edit_template['name']
            del bb_edit_template['item']
            return {'FINISHED'}

        
        
        

        
        
        bb_edit_template['item'] = "tarm"
        bb_edit_template['name'] = self.name

        
        
        

        
        (tarm, tbone), = bb_edit_template['template_editing'][self.name].items()
        bb_edit_template.terminate = True
        bb_edit_template.tarm_name = tarm
        bb_edit_template.tarm_name_backup = tarm

        return {'FINISHED'}

class BentoBuddyEditTemplateChangeSourceBone(bpy.types.Operator):
    """Changing a source bone name to another takes the stream with it, which is to say the
target rig and target bone stay the same.  The only change you'll see is the source bone name.
"""
    bl_idname = "bentobuddy.edit_template_change_source_bone"
    bl_label = "Click to change the name of the source bone\n"

    
    
    
    name : bpy.props.StringProperty(default="")

    def execute(self, context):
        bb_edit_template = bpy.context.window_manager.bb_edit_template
        obj = bpy.data.objects

        
        if self.name == bb_edit_template.get('name'):
            
            
            del bb_edit_template['name']
            del bb_edit_template['item']
            return {'FINISHED'}

        
        
        

        
        
        bb_edit_template['item'] = "sbone"
        bb_edit_template['name'] = self.name

        
        
        

        
        
        
        
        bb_edit_template.terminate = True
        bb_edit_template.sbone_name = self.name
        bb_edit_template.sbone_name_backup = self.name

        return {'FINISHED'}

class BentoBuddyEditTemplateChangeTargetBone(bpy.types.Operator):
    """Change the target bone name, presumably to make it match an existing bone in the
target rig.  The entire stream goes with it, source bone and target rig.
"""

    bl_idname = "bentobuddy.edit_template_change_target_bone"
    bl_label = "Click to change the name of the target bone\n"

    
    
    name : bpy.props.StringProperty(default="")

    def execute(self, context):
        bb_edit_template = bpy.context.window_manager.bb_edit_template
        obj = bpy.data.objects

        
        if self.name == bb_edit_template.get('name'):
            
            
            del bb_edit_template['name']
            del bb_edit_template['item']
            return {'FINISHED'}

        
        
        

        
        
        bb_edit_template['item'] = "tbone"
        bb_edit_template['name'] = self.name

        
        
        

        
        (tarm, tbone), = bb_edit_template['template_editing'][self.name].items()
        bb_edit_template.terminate = True
        bb_edit_template.tbone_name = tbone
        bb_edit_template.tbone_name_backup = tbone

        return {'FINISHED'}







class BentoBuddyEditTemplateUndo(bpy.types.Operator):
    """This will undo the last change you made, the display with the red recycle
icon will show what is in storage.  You only get one of these so if you made a
mistake take advantage of this right away!"""

    bl_idname = "bentobuddy.edit_template_undo"
    bl_label = "Click this to recover from a mistake\n"

    @classmethod
    def poll(cls, context):
        bbe = bpy.context.window_manager.bb_edit_template
        if bbe.get('template_editing_undo') == None:
            return False
        return True

    def execute(self, context):
        bbe = bpy.context.window_manager.bb_edit_template

        old_stream = bbe['template_editing_undo']['old'].to_dict()
        new_stream = bbe['template_editing_undo']['new'].to_dict()

        (old_bone, tarm_tbone), = old_stream.items()
        (new_bone, junk), = new_stream.items()

        
        template = bbe['template_editing'].to_dict()
        template_new = dict()
        template_new[old_bone] = tarm_tbone
        for t in template:
            if t == new_bone:
                continue
            template_new[t] = template[t]

        bbe['template_editing'] = template_new

        bbe.terminate = True
        bbe.sbone_name = old_bone
        bbe.sbone_name_backup = old_bone

        (new, old), = bbe['template_editing_undo']['map'].items()
        bbe.message = new + " restored to " + old

        del bbe['template_editing_undo']


        return {'FINISHED'}








class BentoBuddyPanelTemplateEditor(bpy.types.Panel):
    """This is CTM Editor"""
    bl_idname = "OBJECT_PT_bento_buddy_template_tools"
    bl_label = "Template Creator / Editor"
    bl_space_type = "VIEW_3D"
    bl_category = "Bento Buddy"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        obj = bpy.data.objects
        selected = bpy.context.selected_objects
        
        
        bbe = bpy.context.window_manager.bb_edit_template
        bb_edit_template = bpy.context.window_manager.bb_edit_template

        
        scale_factor = 21
        
        icon_repeat = int(round(bpy.context.region.width / scale_factor))

        
        
        
        
        
        
        
        

        layout = self.layout
        box = layout.box()
        box.label(
            text = "Template Converter:",
            )
        col = box.column(align = True)
        row = col.row(align=True)
        row.operator(
            "bentobuddy.load_generic_template",
            text="Load ctm or ccm",
            icon_value = ico.custom_icons["load"].icon_id
            )
        row.prop(
            bbe,
            "info_bentobuddy_load_generic_template",
            toggle=True,
            text = "",
            icon_value = ico.custom_icons["alert"].icon_id
            )
        row = col.row(align=True)

        row.operator(
            "bentobuddy.save_ccm",
            text="Save as Character Converter",
            icon_value = ico.custom_icons["save"].icon_id
            )
        row = col.row(align=True)
        row.operator(
            "bentobuddy.save_ctm",
            text="Save as Template Map",
            icon_value = ico.custom_icons["save"].icon_id
            )
        
        
        
        layout = self.layout
        box = layout.box()
        box.label(
            text = "Template Composer:",
            )
        col = box.column(align = True)
        row = col.row(align=True)
        if bbe.get('map_type_combine') == "ctm":
            label_text = "Load ctm"
        elif bbe.get('map_type_combine') == "ccm":
            label_text = "Load ccm"
        else:
            label_text = "Load ctm or ccm"
        row.operator(
            "bentobuddy.combine_generic_template",
            text = label_text,
            icon_value = ico.custom_icons["load"].icon_id
            )
        
        row.prop(
            bbe,
            "disable_map_pose",
            text = "",
            toggle = True,
            icon_value = ico.custom_icons["disable_map_pose"].icon_id
            )
        row.prop(
            bbe,
            "info_bentobuddy_combine_generic_template",
            toggle=True,
            text = "",
            icon_value = ico.custom_icons["alert"].icon_id
            )
        if bbe.get('template_map_combine') != None and bbe.get('map_files_combine') != None:

            row = col.row(align=True)
            row.operator(
                "bentobuddy.reset_template_composer",
                text = "Reset Composer",
                icon_value = ico.custom_icons["reset"].icon_id
                )
            if len(bbe['map_files_combine']) > 1:
                layout = self.layout
                row = col.row(align=True)
                if bbe['map_type_combine'] == "ccm":
                    row.operator(
                        "bentobuddy.save_combined_ccm",
                        text = "Save Combined CCM",
                        icon_value = ico.custom_icons["save"].icon_id
                        )
                elif bbe['map_type_combine'] == "ctm":
                    row.operator(
                        "bentobuddy.save_combined_ctm",
                        text = "Save Combined CTM",
                        icon_value = ico.custom_icons["save"].icon_id
                        )
                else:
                    row.label(
                        text = "** UNKNOWN MAP TYPE DETECTED, THIS IS A FATAL ERROR **",
                        )
            layout = self.layout
            row = col.row(align=True)
            row.label(
                text = "- maps loaded -",
                )
            for m in bbe['map_files_combine']:
                row = col.row(align=True)
                row.label(
                    text = "[" + m + "]",
                    )
        
        
        




        
        
        
        
        
        
        
        
        
        
        

        
        
        
        
        
        

        
        

        layout = self.layout

        box = layout.box()
        box.label(
            text = "Manual Template Creator / Editor:",
            )
        col = box.column(align = True)
        row = col.row(align=True)
        row.operator(
            "bentobuddy.edit_template_new_ctm",
            text = "New ctm",
            icon_value = ico.custom_icons["magic"].icon_id
            )
        row.operator(
            "bentobuddy.edit_template_load_ctm",
            text = "Load ctm",
            icon_value = ico.custom_icons["load"].icon_id
            )

        test_ccm = False
        if test_ccm == True:
            row.operator(
                "bentobuddy.edit_template_load_ccm",
                text = "Load ccm",
                icon_value = ico.custom_icons["load"].icon_id
                )

        row.operator(
            "bentobuddy.edit_template_load_txt",
            text = "Load txt",
            icon_value = ico.custom_icons["load"].icon_id
            )

        row.prop(
            bb_edit_template,
            "load_txt_reversed",
            toggle=True,
            text = "",
            icon_value = ico.custom_icons["loop"].icon_id
            )

        if test_ccm == True:
            row = col.row(align=True)
            row.operator(
                "bentobuddy.edit_template_save_ccm",
                text = "Save ccm",
                icon_value = ico.custom_icons["save"].icon_id
                )


        if bb_edit_template.get('template_editing'):
            row = col.row(align=True)
            row.operator(
                "bentobuddy.edit_template_save_ctm",
                text = "Save ctm",
                icon_value = ico.custom_icons["save"].icon_id
                )

            if bb_edit_template.show_map == True:
                edit_template_show_map_icon = "menu_opened"
            else:
                edit_template_show_map_icon = "menu_closed"
            if bb_edit_template.show_rigs == True:
                edit_template_show_rigs_icon = "menu_opened"
            else:
                edit_template_show_rigs_icon = "menu_closed"

            col = box.column(align = True)
            row = col.row(align=True)
            row.prop(
                bb_edit_template,
                "show_map",
                toggle=True,
                text = "Expand Map",
                icon_value = ico.custom_icons[edit_template_show_map_icon].icon_id
                )

            row.prop(
                bb_edit_template,
                "show_rigs",
                toggle=True,
                text = "Rig Options",
                icon_value = ico.custom_icons[edit_template_show_rigs_icon].icon_id
                )


            if bb_edit_template.show_map == True or bb_edit_template.show_rigs == True:

                    
                    row = col.row(align=True)
                    for i in range(icon_repeat):
                        row.label(
                            text = "",
                            icon_value = ico.custom_icons["line_thin_white"].icon_id
                            )

                    row = col.row(align=True)
                    
                    row.label(
                        text = "[" +bbe.message + "]",
                        )
                    
                    if bbe.get('template_editing_undo') != None:
                        edit_template_undo_icon = "reset_warning"
                        row_state = True
                    else:
                        edit_template_undo_icon = "reset"
                        row_state = False

                    row.operator(
                        "bentobuddy.edit_template_undo",
                        text = "",
                        icon_value = ico.custom_icons[edit_template_undo_icon].icon_id
                        )

            if bb_edit_template.show_rigs == True:
                row = col.row(align=True)


                
                for i in range(icon_repeat):
                    row.label(
                        text = "",
                        icon_value = ico.custom_icons["line_thin_white"].icon_id
                        )











                if 1 == 0:
                    row = col.row(align=True)
                    if bbe.source_active == True:
                        row.prop(
                            bbe,
                            "source_active",
                            toggle = True,
                            text = "Source Active",
                            icon_value = ico.custom_icons["walking_black"].icon_id
                            )
                    else:
                        row.operator(
                            "bentobuddy.edit_template_pick_source",
                            text = "Pick the source rig",
                            icon_value = ico.custom_icons["walking_blue"].icon_id
                            )
                    row.operator(
                        "bentobuddy.edit_template_pick_target",
                        text = "Pick a target rig",
                        icon_value = ico.custom_icons["walking_red"].icon_id
                        )

                    col = box.column(align = True)
                    row = col.row(align=True)
                    row.label(
                        text = "This is the manual mapper, automated features are on the way",
                        )
                    row = col.row(align=True)




                
                targets = dict()
                for sbone in bbe.get('template_editing', []):
                    (tarm, tbone), = bbe['template_editing'][sbone].items()
                    targets[tarm] = "" 
                for target in targets:
                    row = col.row(align=True)
                    row.operator(
                        "bentobuddy.edit_template_move_target",
                        text = "",
                        icon_value = ico.custom_icons["edit_red"].icon_id
                        ).name = target
                    if bb_edit_template.get('item') == "move" and bb_edit_template.get('name') == target:
                        row.prop(
                            bb_edit_template,
                            "move_name",
                            text = "",
                            )
                    else:
                        row.label(
                            text = target,
                            )

                    row.operator(
                        "bentobuddy.edit_template_remove_prefix",
                        text = "",
                        icon_value = ico.custom_icons["prefix_remove"].icon_id
                        )

                    row.operator(
                        "bentobuddy.edit_template_remove_target",
                        text = "",
                        icon_value = ico.custom_icons["x_red"].icon_id
                        ).name = target

            if bb_edit_template.show_map == True:
                edit_template_change_source_bone_icon = "edit"
                edit_template_change_target_bone_icon = "edit"
                edit_template_change_rig_name_icon = "edit"

                row = col.row(align=True)

                if bb_edit_template.get('template_editing'):
                    row = col.row(align=True)
                    for i in range(icon_repeat):
                        row.label(
                            text = "",
                            icon_value = ico.custom_icons["line_thin_white"].icon_id
                            )

                    row = col.row(align=True)
                    row.label(
                        text = "Source Bone",
                        icon_value = ico.custom_icons["blank"].icon_id
                        )
                    row.label(
                        text = "Target Rig",
                        icon_value = ico.custom_icons["blank"].icon_id
                        )
                    row.label(
                        text = "Target Bone",
                        icon_value = ico.custom_icons["blank"].icon_id
                        )
                    row.operator(
                        "bentobuddy.edit_template_reset",
                        text = "",
                        icon_value = ico.custom_icons["reset"].icon_id
                        )
                    scale_factor = 21
                    icon_repeat = int(round(bpy.context.region.width / scale_factor))
                    row = col.row(align=True)
                    
                    for i in range(icon_repeat):
                        row.label(
                            text = "",
                            icon_value = ico.custom_icons["line_thin_white"].icon_id
                            )

                    row = col.row(align=True)
                    row.operator(
                        "bentobuddy.edit_template_add_bone",
                        text = "",
                        icon_value = ico.custom_icons["magic"].icon_id
                        )
                    row.label(
                        text = "Manually add a custom bone to the map",
                        )

                
                
                for sbone in bb_edit_template['template_editing']:

                    row = col.row(align=True)
                    (tarm, tbone), = bb_edit_template['template_editing'][sbone].items()

                    
                    row.operator(
                        "bentobuddy.edit_template_change_source_bone",
                        text = "",
                        icon_value = ico.custom_icons[edit_template_change_source_bone_icon].icon_id
                        ).name = sbone

                    
                    
                    
                    

                    
                    if bb_edit_template.get('item') == "sbone" and bb_edit_template.get('name') == sbone:
                        row.prop(
                            bb_edit_template,
                            "sbone_name",
                            text = "",
                            )
                    else:
                        row.label(
                            text = sbone
                            )
                    row.operator(
                        "bentobuddy.edit_template_change_rig_name",
                        text = "",
                        icon_value = ico.custom_icons[edit_template_change_rig_name_icon].icon_id
                        ).name = sbone

                    
                    if bb_edit_template.get('item') == "tarm" and bb_edit_template.get('name') == sbone:
                        row.prop(
                            bb_edit_template,
                            "tarm_name",
                            text = "",
                            )
                    else:
                        row.label(
                            text = tarm
                            )
                    row.operator(
                        "bentobuddy.edit_template_change_target_bone",
                        text = "",
                        icon_value = ico.custom_icons[edit_template_change_target_bone_icon].icon_id
                        ).name = sbone

                    
                    if bb_edit_template.get('item') == "tbone" and bb_edit_template.get('name') == sbone:
                        row.prop(
                            bb_edit_template,
                            "tbone_name",
                            text = "",
                            )
                    else:
                        row.label(
                            text = tbone
                            )
                    row.operator(
                        "bentobuddy.edit_template_remove_bone",
                        text = "",
                        icon_value = ico.custom_icons["x_black"].icon_id
                        ).bone = sbone

        
        
        

            
                
                
                

        
        
        

        
        
        
        
        
        
        
        
        
        
        bb_onemap = bpy.context.window_manager.bb_onemap

        layout = self.layout
        box = layout.box()
        box.label(
            text = "Hybrid Map:",
            )
        col = box.column(align = True)

        row = col.row(align=True)
        row.operator(
            "bentobuddy.template_load_onemap",
            text = "Load Hybrid",
            icon_value = ico.custom_icons["load"].icon_id
            )
        row.operator(
            "bentobuddy.template_save_onemap",
            text = "Save Hybrid",
            icon_value = ico.custom_icons["save"].icon_id
            )
        row = col.row(align=True)
        row.prop(
            bb_onemap,
            "blank",
            text = "something",
            )




































class BentoBuddyEditTemplateLoadFromCCM(bpy.types.Operator, ImportHelper):
    """Load a CCM into the manual editor.
"""

    bl_idname = "bentobuddy.edit_template_load_ccm"
    bl_label = "Edit Template"

    filename_ext = ".ccm"

    
    
    target : bpy.props.StringProperty(default="template_editing")

    filter_glob : bpy.props.StringProperty(
        default='*.ccm',
        options={'HIDDEN'}
        )

    def invoke(self, context, event):
        save_path = script_dir + data_path
        self.filepath = save_path
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


    def execute(self, context):
        bbe = bpy.context.window_manager.bb_edit_template
        bpy.ops.bentobuddy.edit_template_reset()

        try:
            namespace = {}
            exec(open(self.filepath, 'r', encoding='UTF8').read(), namespace)
        except Exception as e:
            print("error loading ccm")
            print(traceback.format_exc())
            return {'FINISHED'}

        rename = {}
        reskin = {}
        pose = {}
        try:
            rename.update(namespace['rename'])
        except:
            txt = "No bone map was found in the ccm"
            print(txt)
            utils.popup(txt, "Error", "ERROR")
            return {'FINISHED'}
        try:
            reskin.update(namespace['reskin'])
        except:
            
            reskin = dict()
            print("No reskin data, that's not a fatal error but the definition should exist at least")
        try:
            pose.update(namespace['pose'])
        except:
            pose = dict()
            print("No pose data, that's not a fatal error but the definition should exist at least")

        bbe['template_ccm'] = dict()
        bbe['template_ccm']['rename'] = rename
        bbe['template_ccm']['reskin'] = reskin
        bbe['template_ccm']['pose'] = pose

        return {'FINISHED'}





class BentoBuddyEditTemplateSaveFromCCM(bpy.types.Operator, ExportHelper):
    """Save your loaded map as a CCM
"""
    bl_idname = "bentobuddy.edit_template_save_ccm"
    bl_label = "Save Template"

    filename_ext = ".ccm"
    filter_glob : bpy.props.StringProperty(
        default='*.ccm',
        options={'HIDDEN'}
        )

    def invoke(self, context, event):
        save_path = script_dir + data_path
        self.filepath = save_path
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        bbe = bpy.context.window_manager.bb_edit_template

        if bbe.get('template_ccm'):

            template_map = bbe['template_ccm'].to_dict()
            formatted_text = utils.format_ccm(template_map)

            try:
                f = open(self.filepath, "w", encoding='UTF8')
                f.write(formatted_text)
                f.close()
                
                print("Template saved as:", self.filepath)
            except Exception as e:
                
                print("Couldn't write file:", self.filepath)
                print(traceback.format_exc())
        else:
            print("Property (template_ccm) was missing when attempting to access it, we got ghosts!")

        return {'FINISHED'}





class BentoBuddyTemplateOneMapProperties(bpy.types.PropertyGroup):

    
    def update_blank(self, context):
        bpy.context.window_manager_bb_onemap.property_unset("blank")
    blank : bpy.props.BoolProperty(default=False, update=update_blank)

    def update_onemap_reskin(self, context):
        print("reskin triggered to off")

    onemap_reskin : bpy.props.BoolProperty(
        name = "",
        description =            "Reskin Mode"            "\n\n"            "While this is enabled you choose a number of bones that you would like to remove and have their mesh weights assigned to the "            "bone that you chose when you enabled this mode.  This allows you to smoothly merge vertex weights from a bone that can't be "            "used in the target system to a bone that can be used.",
        default=False,
        update = update_onemap_reskin
        )




class BentoBuddyTemplateLoadOneMap(bpy.types.Operator, ImportHelper):
    """Load a CTM or CCM"""

    bl_idname = "bentobuddy.template_load_onemap"
    bl_label = "Load Map"

    filter_glob : bpy.props.StringProperty(
        default='*.ctm;*.ccm',
        options={'HIDDEN'}
        )

    def invoke(self, context, event):
        load_path = script_dir + data_path
        self.filepath = load_path
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        bb_onemap = bpy.context.window_manager.bb_onemap

        file_path = self.properties.filepath
        path, name = os.path.split(self.properties.filepath)
        ext = name.split(".")[-1]

        try:
            namespace = {}
            exec(open(file_path, 'r', encoding='UTF8').read(), namespace)
        except Exception as e:
            print(traceback.format_exc())
            return {'FINISHED'}

        template = {}
        for container in namespace:
            
            if container.startswith("__"):
                continue
            template[container] = namespace[container]

        
        

        if ext.lower() == "ccm":
            bone_map = {}
            for tbone in template['rename']:
                sbone = template['rename'][tbone]
                bone_map[tbone] = {"Armature": sbone} 

        elif ext.lower() == "ctm":
            bone_map = {}
            for sbone in template['template_map']:
                (tarm, tbone), = template['template_map'][sbone].items()
                bone_map[tbone] = {"Armature": sbone} 

        else:
            print("Programmers dum, invalid extension:", ext)
            return {'FINISHED'}

        bb_onemap.onemap_template_name = name

        return {'FINISHED'}







class BentoBuddyTemplateSaveOneMap(bpy.types.Operator, ExportHelper):
    bl_idname = "bentobuddy.template_save_onemap"
    bl_label = "Save Hybrid"

    
    filename_ext = ".ccm"

    filter_glob : bpy.props.StringProperty(
        default='*.ccm',
        options={'HIDDEN'}
        )
    def invoke(self, context, event):
        save_path = script_dir + data_path
        self.filepath = save_path
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    @classmethod
    def poll(cls, context):
        bb_onemap = bpy.context.window_manager.bb_onemap
        if bb_onemap.get('template_map') == None:
            return False
        return True

    def execute(self, context):
        bb_onemap = bpy.context.window_manager.bb_onemap
        path = self.properties.filepath

        template_map = bb_onemap['template_map'].to_dict()
        rename = bb_onemap['rename'].to_dict()
        reskin = bb_onemap['reskin'].to_dict()
        target = "Armature"

        container = dict()
        for tbone in template['rename']:
            mbone = template['rename'][tbone]
            container[mbone] = {target: tbone}


        formatted_maps = "# Character Hybrid Map auto-generated by Bento Buddy\n"
        formatted_maps += "template_map = {\n"
        for sbone in template_map:
            (tarm, tbone), = template_map[sbone].items()
            formatted_maps += "    " + '"' + sbone + '": ' + '{' + "\n"
            formatted_maps += "        " + '"' + tarm +'": ' + '"' + tbone + '",' + "\n" + "        },\n"
        formatted_maps += "    }\n"

        


        output = open(path, 'w', encoding='UTF8')
        output.write(formatted_maps)
        output.close()

        
        del bb_onemap['template_map'] 
        bb_onemap.pop('rename', "")
        bb_onemap.pop('reskin', "")

        return {'FINISHED'}













