import bpy
import os
import json
from bpy_extras.io_utils import ImportHelper, ExportHelper

from . import ico
from . import utils
from .mod_settings import oni_settings

script_dir = os.path.dirname(os.path.abspath(__file__))
presets_path    =   oni_settings['paths']['presets']
data_path       =   oni_settings['paths']['data']














class OnigiriEditTemplateProperties(bpy.types.PropertyGroup):

    
    
    


    load_txt_reversed : bpy.props.BoolProperty(
        name = "",
        description =            "Load the text file with reversed bone order matching"            "\n\n"            "When making a text file to be converted into a CTM you'll usually put the name of the bone from the rig that you want to "            "convert into the first slot and then put the target system into the second slot.  These virtual (slots) are just a line "            "separated by a space.  Unfortunately some bones have spaces in them and the first bone cannot be defined with a space so "            "you may have to use the reverse in order to map your bones, if using a text file.  However, if both the source and the "            "target have spaces in their bones then even the reverse button, right here, won't help you and you'll have to map those "            "bones using this interface instead.  With that in mind, what this switch does is simple reverses the target/source order "            "after reading the file in and is just a convenience in case one of the systems doesn't have spaces in the bones.  Honestly "            "no bone should ever have a space, or white space, in its name but some armatures do this.",
        default = False
        )

    def update_info_onigiri_load_generic_template(self, context):
        
        if oni_settings['terminate'] == True:
            oni_settings['terminate'] = False
            return
        onie = bpy.context.window_manager.oni_edit_template
        
        oni_settings['terminate'] = True
        onie.info_onigiri_load_generic_template = False
        return
    info_onigiri_load_generic_template : bpy.props.BoolProperty(
        name = "Template Converter",
        description =            "\n"            "The button you have hovered over is informative only, read below...\n\n"            "This feature is provided in order to convert a template map from one type to another for use in various areas of Onigiri."            "\n",
        default = False,
        update = update_info_onigiri_load_generic_template,
    )

    disable_map_pose : bpy.props.BoolProperty(
        name = "Push this to disable loading the pose",
        description =            "When you're loading multiple maps you may want to keep a single working pose but not the rest.  Use this disable button "            "to prevent the loader from including the pose into the next loaded map.  When you have a pose in one of them that you're "            "sure about then you can re-enable the loading of the pose to allow the loader to record the included pose data.  In order to "            "check the pose, you can apply it to your skeleton in the Animation rollout and Enable Posing Library.  From there you can "            "load a pose from a CCM file to see what it looks like.  CTM files do not have poses in them so this can only apply to CCM.",
        default = False,
        )

    def update_info_onigiri_combine_generic_template(self, context):
        
        if oni_settings['terminate'] == True:
            oni_settings['terminate'] = False
            return
        onie = bpy.context.window_manager.oni_edit_template
        
        oni_settings['terminate'] = True
        onie.info_onigiri_combine_generic_template = False
        return
    info_onigiri_combine_generic_template : bpy.props.BoolProperty(
        name = "Combine Templates",
        description =            "\n"            "The button you have hovered over is informative only, read below...\n\n"            "This feature will allow you to load multiple modules to combine them for storing into a new map.  This merge "            "feature will allow you to work on different sections of your rig, or have multiple people working on different sections, "            "and then later combine them using this tool.  Each map that is loaded takes precedence over all other previously loaded maps, "            "which is to say, if there are duplicate mapped bones, the newest loaded map will override any existing duplicate maps."            "\n",
        default = False,
        update = update_info_onigiri_combine_generic_template,
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
        onie = bpy.context.window_manager.oni_edit_template
        if onie.terminate == True:
            onie.terminate = False
            return

        print("entered update for source_active")
        return 

    source_active : bpy.props.BoolProperty(
        description =            "Click to disable the active map, your changes will not be harmed but you need to save your work to a file using the save "            "feature because it does not save with the blender file",
        default = False,
        update = update_source_active
    )

    def update_move_name(self,context):
        onie = bpy.context.window_manager.oni_edit_template
        if onie.terminate == True:
            onie.terminate = False
            return
        
        if onie.move_name == onie.move_name_backup:
            print("Property move_name updater running, no name change, returning")
            onie.message = "Same name, nothing changed"
            del onie['name']
            del onie['item']
            return
        
        if onie.move_name.strip() == "":
            print("we're not allowing empty names today, come back tomorrow")
            onie.message = "Empty string"
            del onie['name']
            del onie['item']
            return

        
        
        
        
        
        
        
        tarms = dict()
        for sbone in onie['template_editing']:
            (tarm, tbone), = onie['template_editing'][sbone].items()
            tarms[tarm] = tbone

        
        if onie.move_name in tarms:
            
            
            
            

            
            
            
            template_new = dict()
            target_bones = dict()
            for sbone in onie['template_editing']:
                (tarm, tbone), = onie['template_editing'][sbone].items()
                if tarm == onie.move_name_backup:
                    template_new[sbone] = {onie.move_name : tbone}
                    target_bones[tbone] = ""
            
            for sbone in onie['template_editing']:
                (tarm, tbone), = onie['template_editing'][sbone].items()
                if tarm == onie.move_name_backup:
                    continue
                if tbone in target_bones:
                    continue
                template_new[sbone] = {tarm : tbone}

        
        
        
        
        else:
            template_new = dict()
            for sbone in onie['template_editing']:
                (tarm, tbone), = onie['template_editing'][sbone].items()
                
                if tarm == onie.move_name_backup:
                    template_new[sbone] = {onie.move_name : tbone}
            for sbone in onie['template_editing']:
                (tarm, tbone), = onie['template_editing'][sbone].items()
                
                if tarm == onie.move_name_backup:
                    continue
                template_new[sbone] = {tarm : tbone}

        onie.message = "rig name changed from " + onie.move_name_backup + " to " + onie.move_name
        onie['template_editing'] = template_new

        
        if onie.get('template_editing_undo'):
            del onie['template_editing_undo']

        del onie['name']
        del onie['item']

    def update_sbone_name(self,context):
        onie = bpy.context.window_manager.oni_edit_template
        if onie.terminate == True:
            onie.terminate = False
            return
        
        if onie.sbone_name == onie.sbone_name_backup:
            print("Property sbone_name updater running, no name change, returning")
            onie.message = "Same name, nothing changed"
            del onie['name']
            del onie['item']
            return
        
        if onie.sbone_name.strip() == "":
            print("we're not allowing empty names today, come back tomorrow")
            onie.message = "Empty string"
            del onie['name']
            del onie['item']
            return
        
        if onie.sbone_name in onie['template_editing']:
            print("Name collision, change the name of the other one if you want to move this stream")
            onie.message = "[The name " + '"' + onie.sbone_name + '"' + " would collide with another bone" + "]"
            del onie['name']
            del onie['item']
            return

        print("Property sbone_name updater running to change bone map from", onie.sbone_name_backup, "to", onie.sbone_name)

        
        last_edit = {}
        
        onie['template_editing_undo'] = dict()
        onie['template_editing_undo']['old'] = {}
        onie['template_editing_undo']['new'] = {}
        onie['template_editing_undo']['map'] = {}
        onie['template_editing_undo']['old'][onie.sbone_name_backup] = onie['template_editing'][onie.sbone_name_backup]
        
        onie['template_editing_undo']['new'][onie.sbone_name] = onie['template_editing'][onie.sbone_name_backup]
        
        
        
        onie['template_editing_undo']['map'][onie.sbone_name] = onie.sbone_name_backup

        
        template = onie['template_editing'].to_dict()
        template_new = dict()
        template_new[onie.sbone_name] = template[onie.sbone_name_backup]
        for t in template:
            if t == onie.sbone_name_backup:
                continue
            template_new[t] = template[t]

        onie.sbone_name_backup = onie.sbone_name
        onie['template_editing'] = template_new

        
        del onie['name']
        del onie['item']

        onie.message = "name changed"

        return

    
    
    
    
    
    
    def update_tbone_name(self,context):
        onie = bpy.context.window_manager.oni_edit_template
        if onie.terminate == True:
            onie.terminate = False
            return

        
        sbone = onie['name']

        

        
        
        
        
        
        (tarm, tbone), = onie['template_editing'][sbone].items()

        
        if onie.tbone_name == onie.tbone_name_backup:
            print("Property tbone_name updater running, no name change, returning")
            onie.message = "Same name, nothing changed"
            del onie['name']
            del onie['item']
            return
        
        if onie.tbone_name.strip() == "":
            print("we're not allowing empty names today, come back tomorrow")
            onie.message = "Empty string"
            del onie['name']
            del onie['item']
            return

        
        

        tbone_items = set()
        for k in onie['template_editing']: 
            (rig, tbone), = onie['template_editing'][k].items()
            if rig == tarm:
                tbone_items.add(tbone)

        
        if onie.tbone_name in tbone_items:
            print("Name collision, change the name of the other one if you want to move this stream")
            onie.message = "The name " + '"' + onie.tbone_name + '"' + " would collide with another bone"
            del onie['name']
            del onie['item']
            return

        print("Property tbone_name updater running to change target from", tarm, onie.tbone_name_backup, "to", tarm, onie.tbone_name)

        
        last_edit = {}
        
        onie['template_editing_undo'] = dict()
        onie['template_editing_undo']['old'] = {}
        onie['template_editing_undo']['new'] = {}
        onie['template_editing_undo']['map'] = {}
        onie['template_editing_undo']['old'][sbone] = onie['template_editing'][sbone]
        
        onie['template_editing_undo']['new'][sbone] = {tarm : onie.tbone_name}
        
        onie['template_editing_undo']['map'][onie.tbone_name] = onie.tbone_name_backup

        
        template = onie['template_editing'].to_dict()
        template_new = dict()
        template_new[sbone] = {tarm : onie.tbone_name}

        for t in template:
            if t == sbone:
                continue
            template_new[t] = template[t]

        onie.tbone_name_backup = onie.tbone_name
        onie['template_editing'] = template_new

        del onie['name']
        del onie['item']

        onie.message = "name changed"

        return

    def update_tarm_name(self,context):
        onie = bpy.context.window_manager.oni_edit_template
        if onie.terminate == True:
            onie.terminate = False
            return

        
        sbone = onie['name']

        

        
        (tarm, tbone), = onie['template_editing'][sbone].items()

        
        if onie.tarm_name == onie.tarm_name_backup:
            print("Property tarm_name updater running, no name change, returning")
            onie.message = "Same name, nothing changed"
            del onie['name']
            del onie['item']
            return
        
        if onie.tarm_name.strip() == "":
            print("we're not allowing empty names today, come back tomorrow")
            onie.message = "Empty string"

            del onie['name']
            del onie['item']
            return
        
        
        tarm_items = {}
        for k in onie['template_editing']:
            (arm, bone), = onie['template_editing'][k].items()
            if onie.tarm_name == arm:
                
                print("The target armature rename would have collided:", tarm)
                onie.message = onie.tarm_name + " would have collided, use rig options to merge"
                del onie['name']
                del onie['item']
                return

        
        last_edit = {}
        
        onie['template_editing_undo'] = dict()
        onie['template_editing_undo']['old'] = {}
        onie['template_editing_undo']['new'] = {}
        onie['template_editing_undo']['map'] = {}
        onie['template_editing_undo']['old'][sbone] = onie['template_editing'][sbone]
        
        onie['template_editing_undo']['new'][sbone] = {onie.tarm_name : tbone}
        
        onie['template_editing_undo']['map'][onie.tarm_name] = onie.tarm_name_backup

        
        template = onie['template_editing'].to_dict()
        template_new = dict()
        template_new[sbone] = {onie.tarm_name : tbone}

        for t in template:
            if t == sbone:
                continue
            template_new[t] = template[t]

        onie.tarm_name_backup = onie.tarm_name
        onie['template_editing'] = template_new
        del onie['name']
        del onie['item']

        onie.message = "name changed"

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











class OnigiriLoadGenericTemplate(bpy.types.Operator, ImportHelper):
    """Here you can convert one template type to another
This section contains an info button (!), hover over it for detailed information."""

    
    

    bl_idname = "onigiri.load_generic_template"
    bl_label = "Load *.ccm, *.ctm"

    filter_glob : bpy.props.StringProperty(
        default='*.ccm;*.ctm',
        options={'HIDDEN'}
        )

    
    
    
    
        
        
        

    def execute(self, context):
        obj = bpy.data.objects
        onie = bpy.context.window_manager.oni_edit_template
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
            onie['template_map_convert'] = {}

            
            onie['template_map_convert'] = template




                
                
                
                
                
                


        
        
        if 'template_map' in template:
            onie['map_type_convert'] = "ctm"
        if 'rename' in template:
            onie['map_type_convert'] = "ccm"

        return {'FINISHED'}

    def invoke(self, context, event):
        load_path = script_dir + data_path
        self.filepath = load_path
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}









class OnigiriSaveCCM(bpy.types.Operator, ExportHelper):
    bl_idname = "onigiri.save_ccm"
    bl_label = "Save Converted Template"

    
    filename_ext = ".ccm"

    filter_glob : bpy.props.StringProperty(
        default='*.ccm',
        options={'HIDDEN'}
        )

    
    @classmethod
    def poll(cls, context):
        onie = bpy.context.window_manager.oni_edit_template
        if onie.get('template_map_convert') == None:
            return False
        if onie['template_map_convert'] == "":
            return False
        if onie.get('map_type_convert') == None:
            return False
        if onie['map_type_convert'] == "ccm":
            return False
        return True

    def execute(self, context):
        onie = bpy.context.window_manager.oni_edit_template
        path = self.properties.filepath

        
        if onie['map_type_convert'] == "ccm":
            txt = "Conversion type is the same as the loaded map: " + onie['map_type']
            print(txt)
            utils.popup(txt, "Error", "ERROR")
            return {'FINISHED'}

        
        
        

        
        template = onie['template_map_convert']['template_map'].to_dict()

        
        container = dict()
        for mbone in template:
            (tarm, tbone), = template[mbone].items()
            container[tbone] = mbone

        formatted_maps = "# Auto generated by Onigiri - Character Converter from CTM\n"
        rename_maps = "rename = {\n";

        for tbone in container:
            rename_maps += "    " + '"' + tbone + '": ' + '"' + container[tbone] + '"' + ",\n"
        rename_maps += "    }\n"

        
        formatted_maps += rename_maps

        output = open(path, 'w', encoding='UTF8')
        output.write(formatted_maps)
        output.close()

        
        del onie['template_map_convert']
        del onie['map_type_convert']

        return {'FINISHED'}

    def invoke(self, context, event):
        save_path = script_dir + data_path
        self.filepath = save_path
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}




class OnigiriSaveCTM(bpy.types.Operator, ExportHelper):
    bl_idname = "onigiri.save_ctm"
    bl_label = "Save Converted Template"

    
    filename_ext = ".ctm"

    filter_glob : bpy.props.StringProperty(
        default='*.ctm',
        options={'HIDDEN'}
        )

    
    @classmethod
    def poll(cls, context):
        onie = bpy.context.window_manager.oni_edit_template
        if onie.get('template_map_convert') == None:
            return False
        if onie['template_map_convert'] == "":
            return False
        if onie.get('map_type_convert') == None:
            return False
        if onie['map_type_convert'] == "ctm":
            return False
        return True

    def execute(self, context):
        onie = bpy.context.window_manager.oni_edit_template
        path = self.properties.filepath

        
        if onie['map_type_convert'] == "ctm":
            txt = "Conversion type is the same as the loaded map: " + onie['map_type']
            print(txt)
            utils.popup(txt, "Error", "ERROR")
            return {'FINISHED'}

        
        template = onie['template_map_convert'].to_dict()

        
        

        
        target = "arm_" + utils.get_unique_name_short()

        container = dict()
        for tbone in template['rename']:
            mbone = template['rename'][tbone]
            container[mbone] = {target: tbone}


        formatted_maps = "# Character Template Map auto-generated by Onigiri from CCM\n"
        formatted_maps += "template_map = {\n"
        for sbone in container:
            (tarm, tbone), = container[sbone].items()
            formatted_maps += "    " + '"' + sbone + '": ' + '{' + "\n"
            formatted_maps += "        " + '"' + tarm +'": ' + '"' + tbone + '",' + "\n" + "        },\n"
        formatted_maps += "    }\n"

        output = open(path, 'w', encoding='UTF8')
        output.write(formatted_maps)
        output.close()

        
        del onie['template_map_convert']

        return {'FINISHED'}

    def invoke(self, context, event):
        save_path = script_dir + data_path
        self.filepath = save_path
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}








class OnigiriCombineGenericTemplate(bpy.types.Operator, ImportHelper):
    """Here you can load multiple templates to create a composition that had
previously been mapped separately, see (!) button"""

    bl_idname = "onigiri.combine_generic_template"
    bl_label = "Load *.ccm, *.ctm"

    filter_glob : bpy.props.StringProperty(
        default='*.ccm;*.ctm',
        options={'HIDDEN'}
        )

    
    
        
        
        

    def execute(self, context):
        obj = bpy.data.objects
        onie = bpy.context.window_manager.oni_edit_template
        path = self.properties.filepath

        low_path = path.lower()
        if low_path.endswith("." + "ccm"):
            my_type = "ccm"
        elif low_path.endswith("." + "ctm"):
            my_type = "ctm"
        else:
            print("OnigiriCombineGenericTemplate reports: Unknown map type in file - ", path)
            utils.popup("Unknown map type in file, check console for details", "Error", "ERROR")
            return {'FINISHED'}

        
        
        if onie.get('map_type_combine') != None:
            if onie['map_type_combine'] == my_type:
                pass
            else:
                print("OnigiriCombineGenericTemplate reports: existing template is", onie['map_type_combine'], "but user wants something else")
                txt = "You can only combine maps of the same type.  To start over use the reset button"
                print(txt)
                utils.popup(txt, "Error", "ERROR")
                return {'FINISHED'}
        
        else:
            onie['map_type_combine'] = my_type

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
            
            if onie.get('template_map_combine') == None:
                onie['template_map_combine'] = {}
                
                onie['map_files_combine'] = [path_tail]
            
            else:

                print("---------------------------------------------------------------")
                print("path_tail")

                print("---------------------------------------------------------------")


                if onie.get('map_files_combine') == None:
                    onie['map_files_combine'] = list()
                if path_tail in onie['map_files_combine']:
                    txt = "OnigiriCombineGenericTemplate reports: already recorded - " + path_tail
                    print(txt)
                    utils.popup(txt, "Error", "ERROR")
                    return {'FINISHED'}

                map_files = onie['map_files_combine']
                map_files.append(path_tail)
                onie['map_files_combine'] = map_files

            
            
            
            
            
            template_map = onie['template_map_combine'].to_dict()
            for root_key in template:
                if template_map.get(root_key) == None:
                    template_map[root_key] = dict()
                for sub_key in template[root_key]:
                    template_map[root_key].update({sub_key : template[root_key][sub_key]})

            for root_key in template_map:
                
                
                
                
                if root_key == "pose":
                    if onie.disable_map_pose == True:
                        continue

            onie['template_map_combine'] = template_map

        return {'FINISHED'}

    def invoke(self, context, event):
        load_path = script_dir + data_path
        self.filepath = load_path
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}




class OnigiriSaveCombinedCCM(bpy.types.Operator, ExportHelper):
    bl_idname = "onigiri.save_combined_ccm"
    bl_label = "Save Combined Template"

    
    filename_ext = ".ccm"

    filter_glob : bpy.props.StringProperty(
        default='*.ccm',
        options={'HIDDEN'}
        )

    def execute(self, context):
        onie = bpy.context.window_manager.oni_edit_template
        path = self.properties.filepath




        
        
        template = onie['template_map_combine'].to_dict()

        formatted_maps = "# Auto generated by Onigiri - Character Converter from Combined CCM\n"
        for k in template:
            formatted_maps += k + " = "
            formatted_maps += json.dumps(template[k], indent=4)
            formatted_maps += "\n"

        output = open(path, 'w', encoding='UTF8')
        output.write(formatted_maps)
        output.close()

        
        del onie['template_map_combine']
        del onie['map_type_combine']

        return {'FINISHED'}

    def invoke(self, context, event):
        save_path = script_dir + data_path
        self.filepath = save_path
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}




class OnigiriSaveCombinedCTM(bpy.types.Operator, ExportHelper):
    bl_idname = "onigiri.save_combined_ctm"
    bl_label = "Save Combined Template"

    
    filename_ext = ".ctm"

    filter_glob : bpy.props.StringProperty(
        default='*.ctm',
        options={'HIDDEN'}
        )

    def execute(self, context):
        onie = bpy.context.window_manager.oni_edit_template
        path = self.properties.filepath

        template = onie['template_map_combine'].to_dict()

        formatted_maps = "# Character Template Map auto-generated by Onigiri from CTM\n"

        for k in template:
            formatted_maps += k + " = "
            formatted_maps += json.dumps(template[k], indent=4)
            formatted_maps += "\n"

        output = open(path, 'w', encoding='UTF8')
        output.write(formatted_maps)
        output.close()

        
        del onie['template_map_combine']
        del onie['map_type_combine']

        return {'FINISHED'}

    def invoke(self, context, event):
        save_path = script_dir + data_path
        self.filepath = save_path
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}




class OnigiriResetCombinedTemplates(bpy.types.Operator):
    """Click to reset the composer so you can have a clean slate"""
    bl_idname = "onigiri.reset_template_composer"
    bl_label = "Reset Composer"

    def execute(self, context):
        onie = bpy.context.window_manager.oni_edit_template
        del onie['template_map_combine']
        del onie['map_type_combine']
        del onie['map_files_combine']
        return {'FINISHED'}









class OnigiriEditTemplateNewCTM(bpy.types.Operator):
    """Start a new map
"""









    bl_idname = "onigiri.edit_template_new_ctm"
    bl_label = "Create a new template"


    def execute(self, context):
        onie = bpy.context.window_manager.oni_edit_template

        if onie.get('template_editing') != None:
            print("Create new CTM runs but there's already a template in the mapper")
            utils.popup("You have an active ctm, reset it to start a new one", "Template Exists", "INFO")
            return {'FINISHED'}



        sbone = utils.get_unique_name_short()
        tarm = utils.get_unique_name_short()
        tbone = utils.get_unique_name_short()
        onie['template_editing'] = {sbone: {tarm: tbone}}

        return {'FINISHED'}




class OnigiriEditTemplateLoadFromTXT(bpy.types.Operator, ImportHelper):
    """Load a text file to create a template from that file.  The format for this file is one bone
map per line.  The SL bone is first and the second part is the target bone on the same line.
SL bones don't have spaces but your target can.
"""

    bl_idname = "onigiri.edit_template_load_txt"
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
        oni_edit_template = bpy.context.window_manager.oni_edit_template
        bpy.ops.onigiri.edit_template_reset()

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
            if oni_edit_template.load_txt_reversed == True:
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

        oni_edit_template['template_editing'] = template_map

        return {'FINISHED'}




class OnigiriEditTemplateLoadFromCTM(bpy.types.Operator, ImportHelper):
    """Load a CTM into the manual editor.
"""

    bl_idname = "onigiri.edit_template_load_ctm"
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
        oni_edit_template = bpy.context.window_manager.oni_edit_template
        bpy.ops.onigiri.edit_template_reset()

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

        
        
        
        oni_edit_template[self.target] = template_map

        return {'FINISHED'}




class OnigiriEditTemplateSaveFromCTM(bpy.types.Operator, ExportHelper):
    """Save your loaded map as a CTM
"""
    bl_idname = "onigiri.edit_template_save_ctm"
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
        oni_edit_template = bpy.context.window_manager.oni_edit_template

        if oni_edit_template.get('template_editing'):

            template_map = oni_edit_template['template_editing'].to_dict()
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




class OnigiriEditTemplatePickSource(bpy.types.Operator):
    """Picking a source rig enables the active mapping process where you can pick bones in
the interface for your source and targets.  Even this mapping process is for data only and
does not actually do anything except build a data set for you"""

    bl_idname = "onigiri.edit_template_pick_source"
    bl_label = "Choose a rig for your source bones and click this button\n"

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) != 1:
            return False
        if bpy.context.selected_objects[0].type == 'ARMATURE':
            return True
        return False

    def execute(self, context):
        onie = bpy.context.window_manager.oni_edit_template
        obj = bpy.data.objects

        armObj = bpy.context.selected_objects[0]
        sarm = armObj.name
        print("source picked", sarm)
        onie.terminate = True
        onie.source_active = True
        return {'FINISHED'}




class OnigiriEditTemplatePickTarget(bpy.types.Operator):
    """Choose a target rig and click this button to add it to your map.
"""

    bl_idname = "onigiri.edit_template_pick_target"
    bl_label = "Choose a target rig\n"

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) != 1:
            return False
        if bpy.context.selected_objects[0].type != 'ARMATURE':
            return False

        
        
        
        onie = bpy.context.window_manager.oni_edit_template
        return onie.source_active

    def execute(self, context):
        onie = bpy.context.window_manager.oni_edit_template
        obj = bpy.data.objects

        armObj = bpy.context.selected_objects[0]
        tarm = armObj.name
        print("target picked", tarm)
        onie.terminate = True

        if onie.get('template_editor_targets') == None:
            onie['template_editor_targets'] = dict()

        if tarm in onie['template_editor_targets']:
            print("target exists already:", tarm)
            utils.popup("Target already chosen", "Info", "INFO")
        else:
            onie['template_editor_targets'][tarm] = {}

        return {'FINISHED'}







class OnigiriEditTemplateMoveTarget(bpy.types.Operator):
    """WARNING: This will merge or rename a rig stream.  Any target bones that match
within a merger will be overwritten by the renamed stream.  There is no recovery from this.
Any stored undo will be removed
"""

    bl_idname = "onigiri.edit_template_move_target"
    bl_label = "Click to globally change the rig name or merge\n"

    
    
    
    name : bpy.props.StringProperty(default="")

    def execute(self, context):
        onie = bpy.context.window_manager.oni_edit_template
        obj = bpy.data.objects

        
        if self.name == onie.get('name'):
            
            
            del onie['name']
            del onie['item']
            return {'FINISHED'}

        
        
        

        
        
        onie['item'] = "move"
        onie['name'] = self.name

        
        
        

        
        
        onie.terminate = True
        onie.move_name = self.name
        onie.move_name_backup = self.name

        return {'FINISHED'}






    

    
    

    

    
        
        







class OnigiriEditTemplateRemoveTarget(bpy.types.Operator):
    """WARNING:  This will remove a target rig from your map completely.  This
is not usually what you need but it's here for convenience.
"""

    bl_idname = "onigiri.edit_template_remove_target"
    bl_label = "Click to globally remove a target from your map\n"

    
    
    
    name : bpy.props.StringProperty(default="")

    def execute(self, context):
        onie = bpy.context.window_manager.oni_edit_template
        obj = bpy.data.objects

        
        if self.name == onie.get('name'):
            
            
            del onie['name']
            del onie['item']
            return {'FINISHED'}

        print("Removing target armature stream for:", self.name)

        
        template_new = {}
        template = onie['template_editing'].to_dict()
        for sbone in template:
            (tarm, tbone), = template[sbone].items()
            if tarm == self.name:
                continue
            template_new[sbone] = {tarm : tbone}

        onie['template_editing'] = template_new
        onie.terminate = True
        onie.move_name = ""
        onie.move_name_backup = ""

        
        if onie.get('name'):
            del onie['name']
        if onie.get('item'):
            del onie['item']

        
        if len(onie['template_editing']) == 0:
            
            
            
            print("All target rigs were removed, resetting")
            bpy.ops.onigiri.edit_template_reset()

        
        if onie.get('template_editing_undo'):
            undo_stream = onie['template_editing_undo']['new'].to_dict()
            (sbone, tarm_tbone), = undo_stream.items()
            (tarm, tbone), = tarm_tbone.items()
            if tarm == self.name:
                print("removed undo for target armature:", self.name)
                del onie['template_editing_undo']

        return {'FINISHED'}



class OnigiriEditTemplateReset(bpy.types.Operator):
    """This will clear out the editor, make sure you saved your work if you want to keep it"""

    bl_idname = "onigiri.edit_template_reset"
    bl_label = "Edit Template Reset"

    def execute(self, context):
        
        
        onie = bpy.context.window_manager.oni_edit_template
        if onie.get('template_editing') != None:
            del onie['template_editing']
        if onie.get('template_editing_undo') != None:
            del onie['template_editing_undo']
        if onie.get('item') != None:
            del onie['item']
        if onie.get('name') != None:
            del onie['name']

        onie.show_rigs = False
        onie.terminate = True
        onie.move_name = ""
        onie.move_name_backup = ""
        onie.terminate = True
        onie.source_active = False

        onie.item_name = ""
        onie.item_name_backup = ""

        return {'FINISHED'}



class OnigiriEditTemplateRemoveBone(bpy.types.Operator):
    """The X indicates a state:

red, source is a root bone but target is not
white/black, target is a root bone but source is not
white, root to root
black, not in map mode"""

    bl_idname = "onigiri.edit_template_remove_bone"
    bl_label = "Click to remove this bone from the map\n"

    bone : bpy.props.StringProperty(default="")

    def execute(self, context):
        onie = bpy.context.window_manager.oni_edit_template
        try:
            del onie['template_editing'][self.bone]
            if len(onie['template_editing']) == 0:
                del onie['template_editing']
            print("Removed", self.bone)
        except:
            print("Couldn't remove bone, this is weird:", self.bone)

        
        if onie.get('template_editing_undo') != None:
            undo_stream = onie['template_editing_undo']['new'].to_dict()
            (sbone, tarm_tbone), = undo_stream.items()
            if self.bone == sbone:
                print("removed undo for bone:", self.bone)
                del onie['template_editing_undo']

        return {'FINISHED'}



class OnigiriEditTemplateAddBone(bpy.types.Operator):
    """Add a bone to the map.  Unique names will be given to each element.  Obviously
you'll want to rename them to bones and rigs you'll expect to be working with.  If you
get an error about a collision just try again
"""
    bl_idname = "onigiri.edit_template_add_bone"
    bl_label = "Click to manually add a bone to the mapper\n"

    def execute(self, context):
        onie = bpy.context.window_manager.oni_edit_template

        
        sbone = utils.get_unique_name_short()
        tarm = utils.get_unique_name_short()
        tbone = utils.get_unique_name_short()

        tarm = sbone
        tbone = sbone

        if sbone in onie['template_editing']:
            print("uuid was present in the map as a source bone, maybe try again?")
            utils.popup("the uniquly created name for the source bone existed in the map, see console", "Collision", "ERROR")
            return {'FINISHED'}

        
        
        template = onie['template_editing'].to_dict()
        template_new = dict()
        template_new[sbone] = {}
        template_new[sbone][tarm] = tbone

        print("OnigiriEditTemplateAddBone : Generated bone defs:", sbone, tarm, tbone)

        for sbone in template:
            (tarm, tbone), = template[sbone].items()
            template_new[sbone] = {}
            template_new[sbone][tarm] = tbone

        onie['template_editing'] = template_new

        return {'FINISHED'}








class OnigiriEditTemplateChangeRigName(bpy.types.Operator):
    """This changes a single bone branch and will split into a different stream.
This is usually not what you want, if you want to rename a rig globally use the
Rig Tools options
"""

    bl_idname = "onigiri.edit_template_change_rig_name"
    bl_label = "Click to change the name of the target rig\n"

    
    
    name : bpy.props.StringProperty(default="")

    def execute(self, context):
        oni_edit_template = bpy.context.window_manager.oni_edit_template
        obj = bpy.data.objects

        
        if self.name == oni_edit_template.get('name'):
            
            
            del oni_edit_template['name']
            del oni_edit_template['item']
            return {'FINISHED'}

        
        
        

        
        
        oni_edit_template['item'] = "tarm"
        oni_edit_template['name'] = self.name

        
        
        

        
        (tarm, tbone), = oni_edit_template['template_editing'][self.name].items()
        oni_edit_template.terminate = True
        oni_edit_template.tarm_name = tarm
        oni_edit_template.tarm_name_backup = tarm

        return {'FINISHED'}

class OnigiriEditTemplateChangeSourceBone(bpy.types.Operator):
    """Changing a source bone name to another takes the stream with it, which is to say the
target rig and target bone stay the same.  The only change you'll see is the source bone name.
"""
    bl_idname = "onigiri.edit_template_change_source_bone"
    bl_label = "Click to change the name of the source bone\n"

    
    
    
    name : bpy.props.StringProperty(default="")

    def execute(self, context):
        oni_edit_template = bpy.context.window_manager.oni_edit_template
        obj = bpy.data.objects

        
        if self.name == oni_edit_template.get('name'):
            
            
            del oni_edit_template['name']
            del oni_edit_template['item']
            return {'FINISHED'}

        
        
        

        
        
        oni_edit_template['item'] = "sbone"
        oni_edit_template['name'] = self.name

        
        
        

        
        
        
        
        oni_edit_template.terminate = True
        oni_edit_template.sbone_name = self.name
        oni_edit_template.sbone_name_backup = self.name

        return {'FINISHED'}

class OnigiriEditTemplateChangeTargetBone(bpy.types.Operator):
    """Change the target bone name, presumably to make it match an existing bone in the
target rig.  The entire stream goes with it, source bone and target rig.
"""

    bl_idname = "onigiri.edit_template_change_target_bone"
    bl_label = "Click to change the name of the target bone\n"

    
    
    name : bpy.props.StringProperty(default="")

    def execute(self, context):
        oni_edit_template = bpy.context.window_manager.oni_edit_template
        obj = bpy.data.objects

        
        if self.name == oni_edit_template.get('name'):
            
            
            del oni_edit_template['name']
            del oni_edit_template['item']
            return {'FINISHED'}

        
        
        

        
        
        oni_edit_template['item'] = "tbone"
        oni_edit_template['name'] = self.name

        
        
        

        
        (tarm, tbone), = oni_edit_template['template_editing'][self.name].items()
        oni_edit_template.terminate = True
        oni_edit_template.tbone_name = tbone
        oni_edit_template.tbone_name_backup = tbone

        return {'FINISHED'}







class OnigiriEditTemplateUndo(bpy.types.Operator):
    """This will undo the last change you made, the display with the red recycle
icon will show what is in storage.  You only get one of these so if you made a
mistake take advantage of this right away!"""

    bl_idname = "onigiri.edit_template_undo"
    bl_label = "Click this to recover from a mistake\n"

    @classmethod
    def poll(cls, context):
        onie = bpy.context.window_manager.oni_edit_template
        if onie.get('template_editing_undo') == None:
            return False
        return True

    def execute(self, context):
        onie = bpy.context.window_manager.oni_edit_template

        old_stream = onie['template_editing_undo']['old'].to_dict()
        new_stream = onie['template_editing_undo']['new'].to_dict()

        (old_bone, tarm_tbone), = old_stream.items()
        (new_bone, junk), = new_stream.items()

        
        template = onie['template_editing'].to_dict()
        template_new = dict()
        template_new[old_bone] = tarm_tbone
        for t in template:
            if t == new_bone:
                continue
            template_new[t] = template[t]

        onie['template_editing'] = template_new

        onie.terminate = True
        onie.sbone_name = old_bone
        onie.sbone_name_backup = old_bone

        (new, old), = onie['template_editing_undo']['map'].items()
        onie.message = new + " restored to " + old

        del onie['template_editing_undo']


        return {'FINISHED'}








class OnigiriPanelTemplateEditor(bpy.types.Panel):
    """This is CTM Editor"""
    bl_idname = "OBJECT_PT_onigiri_template_tools"
    bl_label = "Template Creator / Editor"
    bl_space_type = "VIEW_3D"
    bl_category = "Onigiri"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        obj = bpy.data.objects
        selected = bpy.context.selected_objects
        
        
        onie = bpy.context.window_manager.oni_edit_template
        oni_edit_template = bpy.context.window_manager.oni_edit_template

        
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
            "onigiri.load_generic_template",
            text="Load ctm or ccm",
            icon_value = ico.custom_icons["load"].icon_id
            )
        row.prop(
            onie,
            "info_onigiri_load_generic_template",
            toggle=True,
            text = "",
            icon_value = ico.custom_icons["alert"].icon_id
            )
        row = col.row(align=True)

        row.operator(
            "onigiri.save_ccm",
            text="Save as Character Converter",
            icon_value = ico.custom_icons["save"].icon_id
            )
        row = col.row(align=True)
        row.operator(
            "onigiri.save_ctm",
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
        if onie.get('map_type_combine') == "ctm":
            label_text = "Load ctm"
        elif onie.get('map_type_combine') == "ccm":
            label_text = "Load ccm"
        else:
            label_text = "Load ctm or ccm"
        row.operator(
            "onigiri.combine_generic_template",
            text = label_text,
            icon_value = ico.custom_icons["load"].icon_id
            )
        
        row.prop(
            onie,
            "disable_map_pose",
            text = "",
            toggle = True,
            icon_value = ico.custom_icons["disable_map_pose"].icon_id
            )
        row.prop(
            onie,
            "info_onigiri_combine_generic_template",
            toggle=True,
            text = "",
            icon_value = ico.custom_icons["alert"].icon_id
            )
        if onie.get('template_map_combine') != None and onie.get('map_files_combine') != None:

            row = col.row(align=True)
            row.operator(
                "onigiri.reset_template_composer",
                text = "Reset Composer",
                icon_value = ico.custom_icons["reset"].icon_id
                )
            if len(onie['map_files_combine']) > 1:
                layout = self.layout
                row = col.row(align=True)
                if onie['map_type_combine'] == "ccm":
                    row.operator(
                        "onigiri.save_combined_ccm",
                        text = "Save Combined CCM",
                        icon_value = ico.custom_icons["save"].icon_id
                        )
                elif onie['map_type_combine'] == "ctm":
                    row.operator(
                        "onigiri.save_combined_ctm",
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
            for m in onie['map_files_combine']:
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
            "onigiri.edit_template_new_ctm",
            text = "New ctm",
            icon_value = ico.custom_icons["magic"].icon_id
            )
        row.operator(
            "onigiri.edit_template_load_ctm",
            text = "Load ctm",
            icon_value = ico.custom_icons["load"].icon_id
            )

        test_ccm = False
        if test_ccm == True:
            row.operator(
                "onigiri.edit_template_load_ccm",
                text = "Load ccm",
                icon_value = ico.custom_icons["load"].icon_id
                )

        row.operator(
            "onigiri.edit_template_load_txt",
            text = "Load txt",
            icon_value = ico.custom_icons["load"].icon_id
            )

        row.prop(
            oni_edit_template,
            "load_txt_reversed",
            toggle=True,
            text = "",
            icon_value = ico.custom_icons["loop"].icon_id
            )

        if test_ccm == True:
            row = col.row(align=True)
            row.operator(
                "onigiri.edit_template_save_ccm",
                text = "Save ccm",
                icon_value = ico.custom_icons["save"].icon_id
                )


        if oni_edit_template.get('template_editing'):
            row = col.row(align=True)
            row.operator(
                "onigiri.edit_template_save_ctm",
                text = "Save ctm",
                icon_value = ico.custom_icons["save"].icon_id
                )

            if oni_edit_template.show_map == True:
                edit_template_show_map_icon = "menu_opened"
            else:
                edit_template_show_map_icon = "menu_closed"
            if oni_edit_template.show_rigs == True:
                edit_template_show_rigs_icon = "menu_opened"
            else:
                edit_template_show_rigs_icon = "menu_closed"

            col = box.column(align = True)
            row = col.row(align=True)
            row.prop(
                oni_edit_template,
                "show_map",
                toggle=True,
                text = "Expand Map",
                icon_value = ico.custom_icons[edit_template_show_map_icon].icon_id
                )

            row.prop(
                oni_edit_template,
                "show_rigs",
                toggle=True,
                text = "Rig Options",
                icon_value = ico.custom_icons[edit_template_show_rigs_icon].icon_id
                )


            if oni_edit_template.show_map == True or oni_edit_template.show_rigs == True:

                    
                    row = col.row(align=True)
                    for i in range(icon_repeat):
                        row.label(
                            text = "",
                            icon_value = ico.custom_icons["line_thin_white"].icon_id
                            )

                    row = col.row(align=True)
                    
                    row.label(
                        text = "[" +onie.message + "]",
                        )
                    
                    if onie.get('template_editing_undo') != None:
                        edit_template_undo_icon = "reset_warning"
                        row_state = True
                    else:
                        edit_template_undo_icon = "reset"
                        row_state = False

                    row.operator(
                        "onigiri.edit_template_undo",
                        text = "",
                        icon_value = ico.custom_icons[edit_template_undo_icon].icon_id
                        )

            if oni_edit_template.show_rigs == True:
                row = col.row(align=True)


                
                for i in range(icon_repeat):
                    row.label(
                        text = "",
                        icon_value = ico.custom_icons["line_thin_white"].icon_id
                        )











                if 1 == 0:
                    row = col.row(align=True)
                    if onie.source_active == True:
                        row.prop(
                            onie,
                            "source_active",
                            toggle = True,
                            text = "Source Active",
                            icon_value = ico.custom_icons["walking_black"].icon_id
                            )
                    else:
                        row.operator(
                            "onigiri.edit_template_pick_source",
                            text = "Pick the source rig",
                            icon_value = ico.custom_icons["walking_blue"].icon_id
                            )
                    row.operator(
                        "onigiri.edit_template_pick_target",
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
                for sbone in onie.get('template_editing', []):
                    (tarm, tbone), = onie['template_editing'][sbone].items()
                    targets[tarm] = "" 
                for target in targets:
                    row = col.row(align=True)
                    row.operator(
                        "onigiri.edit_template_move_target",
                        text = "",
                        icon_value = ico.custom_icons["edit_red"].icon_id
                        ).name = target
                    if oni_edit_template.get('item') == "move" and oni_edit_template.get('name') == target:
                        row.prop(
                            oni_edit_template,
                            "move_name",
                            text = "",
                            )
                    else:
                        row.label(
                            text = target,
                            )

                    row.operator(
                        "onigiri.edit_template_remove_prefix",
                        text = "",
                        icon_value = ico.custom_icons["prefix_remove"].icon_id
                        )

                    row.operator(
                        "onigiri.edit_template_remove_target",
                        text = "",
                        icon_value = ico.custom_icons["x_red"].icon_id
                        ).name = target

            if oni_edit_template.show_map == True:
                edit_template_change_source_bone_icon = "edit"
                edit_template_change_target_bone_icon = "edit"
                edit_template_change_rig_name_icon = "edit"

                row = col.row(align=True)

                if oni_edit_template.get('template_editing'):
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
                        "onigiri.edit_template_reset",
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
                        "onigiri.edit_template_add_bone",
                        text = "",
                        icon_value = ico.custom_icons["magic"].icon_id
                        )
                    row.label(
                        text = "Manually add a custom bone to the map",
                        )

                
                
                for sbone in oni_edit_template['template_editing']:

                    row = col.row(align=True)
                    (tarm, tbone), = oni_edit_template['template_editing'][sbone].items()

                    
                    row.operator(
                        "onigiri.edit_template_change_source_bone",
                        text = "",
                        icon_value = ico.custom_icons[edit_template_change_source_bone_icon].icon_id
                        ).name = sbone

                    
                    
                    
                    

                    
                    if oni_edit_template.get('item') == "sbone" and oni_edit_template.get('name') == sbone:
                        row.prop(
                            oni_edit_template,
                            "sbone_name",
                            text = "",
                            )
                    else:
                        row.label(
                            text = sbone
                            )
                    row.operator(
                        "onigiri.edit_template_change_rig_name",
                        text = "",
                        icon_value = ico.custom_icons[edit_template_change_rig_name_icon].icon_id
                        ).name = sbone

                    
                    if oni_edit_template.get('item') == "tarm" and oni_edit_template.get('name') == sbone:
                        row.prop(
                            oni_edit_template,
                            "tarm_name",
                            text = "",
                            )
                    else:
                        row.label(
                            text = tarm
                            )
                    row.operator(
                        "onigiri.edit_template_change_target_bone",
                        text = "",
                        icon_value = ico.custom_icons[edit_template_change_target_bone_icon].icon_id
                        ).name = sbone

                    
                    if oni_edit_template.get('item') == "tbone" and oni_edit_template.get('name') == sbone:
                        row.prop(
                            oni_edit_template,
                            "tbone_name",
                            text = "",
                            )
                    else:
                        row.label(
                            text = tbone
                            )
                    row.operator(
                        "onigiri.edit_template_remove_bone",
                        text = "",
                        icon_value = ico.custom_icons["x_black"].icon_id
                        ).bone = sbone

        
        
        

            
                
                
                

        
        
        

        
        
        
        
        
        
        
        
        
        
        oni_onemap = bpy.context.window_manager.oni_onemap

        layout = self.layout
        box = layout.box()
        box.label(
            text = "Hybrid Map:",
            )
        col = box.column(align = True)

        row = col.row(align=True)
        row.operator(
            "onigiri.template_load_onemap",
            text = "Load Hybrid",
            icon_value = ico.custom_icons["load"].icon_id
            )
        row.operator(
            "onigiri.template_save_onemap",
            text = "Save Hybrid",
            icon_value = ico.custom_icons["save"].icon_id
            )
        row = col.row(align=True)
        row.prop(
            oni_onemap,
            "blank",
            text = "something",
            )




































class OnigiriEditTemplateLoadFromCCM(bpy.types.Operator, ImportHelper):
    """Load a CCM into the manual editor.
"""

    bl_idname = "onigiri.edit_template_load_ccm"
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
        onie = bpy.context.window_manager.oni_edit_template
        bpy.ops.onigiri.edit_template_reset()

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

        onie['template_ccm'] = dict()
        onie['template_ccm']['rename'] = rename
        onie['template_ccm']['reskin'] = reskin
        onie['template_ccm']['pose'] = pose

        return {'FINISHED'}





class OnigiriEditTemplateSaveFromCCM(bpy.types.Operator, ExportHelper):
    """Save your loaded map as a CCM
"""
    bl_idname = "onigiri.edit_template_save_ccm"
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
        onie = bpy.context.window_manager.oni_edit_template

        if onie.get('template_ccm'):

            template_map = onie['template_ccm'].to_dict()
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





class OnigiriTemplateOneMapProperties(bpy.types.PropertyGroup):

    
    def update_blank(self, context):
        bpy.context.window_manager_oni_onemap.property_unset("blank")
    blank : bpy.props.BoolProperty(default=False, update=update_blank)

    def update_onemap_reskin(self, context):
        print("reskin triggered to off")

    onemap_reskin : bpy.props.BoolProperty(
        name = "",
        description =            "Reskin Mode"            "\n\n"            "While this is enabled you choose a number of bones that you would like to remove and have their mesh weights assigned to the "            "bone that you chose when you enabled this mode.  This allows you to smoothly merge vertex weights from a bone that can't be "            "used in the target system to a bone that can be used.",
        default=False,
        update = update_onemap_reskin
        )




class OnigiriTemplateLoadOneMap(bpy.types.Operator, ImportHelper):
    """Load a CTM or CCM"""

    bl_idname = "onigiri.template_load_onemap"
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
        oni_onemap = bpy.context.window_manager.oni_onemap

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

        oni_onemap.onemap_template_name = name

        return {'FINISHED'}







class OnigiriTemplateSaveOneMap(bpy.types.Operator, ExportHelper):
    bl_idname = "onigiri.template_save_onemap"
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
        oni_onemap = bpy.context.window_manager.oni_onemap
        if oni_onemap.get('template_map') == None:
            return False
        return True

    def execute(self, context):
        oni_onemap = bpy.context.window_manager.oni_onemap
        path = self.properties.filepath

        template_map = oni_onemap['template_map'].to_dict()
        rename = oni_onemap['rename'].to_dict()
        reskin = oni_onemap['reskin'].to_dict()
        target = "Armature"

        container = dict()
        for tbone in template['rename']:
            mbone = template['rename'][tbone]
            container[mbone] = {target: tbone}


        formatted_maps = "# Character Hybrid Map auto-generated by Onigiri\n"
        formatted_maps += "template_map = {\n"
        for sbone in template_map:
            (tarm, tbone), = template_map[sbone].items()
            formatted_maps += "    " + '"' + sbone + '": ' + '{' + "\n"
            formatted_maps += "        " + '"' + tarm +'": ' + '"' + tbone + '",' + "\n" + "        },\n"
        formatted_maps += "    }\n"

        


        output = open(path, 'w', encoding='UTF8')
        output.write(formatted_maps)
        output.close()

        
        del oni_onemap['template_map'] 
        oni_onemap.pop('rename', "")
        oni_onemap.pop('reskin', "")

        return {'FINISHED'}













