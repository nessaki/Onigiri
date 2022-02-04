import bpy
import math
import mathutils
import uuid
from bpy.app.handlers import persistent

from . import ico



view_layers = {}
view_layers['avastar'] = {
    "author": "Avastar",
    "index": {
        0 : "Origin",
        1 : "Torso",
        2 : "Arms",
        3 : "Legs",
        4 : "Eye Focus",
        5 : "Alt Focus",
        6 : "Attachment Points",
        7 : "Volume (deform)",
        8 : "Face",
        9 : "Hands",
        10: "Wings",
        11: "Tail",
        12: "Groin",
        13: "Spine (extra)",
        14: "Hinds",
        15: "Extra",
        16: "SL Base (deform)",
        17: "IK Arms",
        18: "IK Legs",
        19: "IK Limbs",
        20: "IK Face (lips)",
        21: "UNKNOWN",
        22: "Structure",
        23: "Bento Bones -All (deform)",
        24: "Bento Bones -Face (deform)",
        25: "Bento Bones -Hands (deform)",
        26: "Bento Bones -Wings (deform)",
        27: "Bento Bones -Tail (deform)",
        28: "Bento Bones -Groin (deform)",
        29: "Bento Bones -Spine (deform)",
        30: "Bento Bones -Hinds (deform)",
        31: "All Bones Deformable Bones",
        },
    }


temp = {}
for r in view_layers:
    temp[r] = {}
    temp[r]['name'] = {}
    for i in view_layers[r]['index']:
        n = view_layers[r]['index'][i]
        temp[r]['name'][n] = i
for r in view_layers:
    view_layers[r]['name'] = temp[r]['name']


view_layers_order = {}
view_layers_order['avastar'] = [
    "Torso", "Origin", "Hands", "Arms", "IK Arms",
    "Legs", "IK Legs", "Hinds", "IK Limbs", "Face",
    "Wings", "Spine (extra)", "Tail", "Groin",
    "SL Base (deform)", "Volume (deform)", "Bento Bones -Hands (deform)",
    "Bento Bones -Hinds (deform)", "Bento Bones -Face (deform)",
    "Bento Bones -Wings (deform)", "Bento Bones -Spine (deform)",
    "Bento Bones -Tail (deform)", "Bento Bones -Groin (deform)"
    ]















@persistent
def viewable_layers(context):



    oni_view = bpy.context.window_manager.oni_view
    so = len(bpy.context.selected_objects)
    if so != 1:
        oni_view.rig_author_name = "Unknown"
        oni_view.rig_author_property = ""
        return
    o = bpy.context.selected_objects[0]
    if o.type != 'ARMATURE':
        oni_view.rig_author_name = "Unknown"
        oni_view.rig_author_property = ""
        return
    
    for rig in view_layers:
        if rig in o:
            oni_view.rig_author_name = view_layers[rig]['author']
            oni_view.rig_author_property = rig
            break
    
    
    oni_view.rig_name = o.data.name
    return 







def cleanup(context):
    if getattr("bpy.context.window_manager", "oni_view", None) != None:
        oniv = bpy.context.window_manager.oni_view
        if oniv.get('states') != None:
            del oniv['states']










@persistent
def clean_before_load(context):
    cleanup(None) 








bpy.app.handlers.load_pre.append(clean_before_load)

bpy.app.handlers.depsgraph_update_post.append(viewable_layers)








def get_unique_name():
    
    import uuid
    import time
    idn = str(uuid.uuid4())
    name = idn.replace("-", "")
    idt = str(time.time())
    time_now = idt.replace(".", "_")
    unique_name = name + "_" + time_now
    return unique_name














def see_all():
    obj = bpy.data.objects
    oniv = bpy.context.window_manager.oni_view
    scene_name = bpy.context.scene.name
    for c in bpy.data.collections:
        c.hide_viewport = False
        c.hide_select = False
    for o in bpy.data.objects:
        o.hide_select = False
        o.hide_viewport = False
    active_view = bpy.context.view_layer.name
    for vlObj in bpy.context.scene.view_layers:
        view_layer = vlObj.name
        bpy.context.window.view_layer = bpy.data.scenes[scene_name].view_layers[view_layer]
        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        for o in bpy.context.selected_objects:
            o.select_set(False)
        for colObj in vlObj.layer_collection.children:
            cname = colObj.name
            vlObj.layer_collection.children[cname].hide_viewport = False
        for o in bpy.data.objects:
            o.hide_set(False)
    bpy.context.window.view_layer = bpy.data.scenes[scene_name].view_layers[active_view]
    return True















def save_state():
    obj = bpy.data.objects
    oniv = bpy.context.window_manager.oni_view

    
    
    
    
    
    
    scene_name = bpy.context.scene.name
    ID = get_unique_name()

    
    
    if oniv.get('states') == None:
        
        oniv['states'] = dict()
        oniv['states']['names'] = dict()
        oniv['states']['data'] = dict()

    
    if scene_name in oniv['states']['names']:
        print("save_states reports: you did a dum, fix your program")
        return False

    print("Saving state for scene", scene_name, "with ID", ID)

    
    
    
    oniv['states']['names'][scene_name] = ID
    oniv['states']['data'] = dict()
    oniv['states']['data'][ID] = dict()
    oniv['states']['data'][ID]['collections'] = dict()
    oniv['states']['data'][ID]['armatures'] = dict() 
    oniv['states']['data'][ID]['objects'] = dict()
    oniv['states']['data'][ID]['layers'] = dict()

    
    
    
    
    for c in bpy.data.collections:
        oniv['states']['data'][ID]['collections'][c.name] = dict()
        oniv['states']['data'][ID]['collections'][c.name]['hide_viewport'] = c.hide_viewport
        oniv['states']['data'][ID]['collections'][c.name]['hide_select'] = c.hide_select
        c.hide_viewport = False
        c.hide_select = False

    
    
    for o in bpy.data.objects:
        oniv['states']['data'][ID]['objects'][o.name] = dict()
        oniv['states']['data'][ID]['objects'][o.name]['hide_select'] = o.hide_select
        oniv['states']['data'][ID]['objects'][o.name]['hide_viewport'] = o.hide_viewport
        o.hide_select = False
        o.hide_viewport = False

    
    
    
    
    
    
    

    
    
    
    

    
    active_view = bpy.context.view_layer.name

    for vlObj in bpy.context.scene.view_layers:
        view_layer = vlObj.name
        
        
        bpy.context.window.view_layer = bpy.data.scenes[scene_name].view_layers[view_layer] 
        oniv['states']['data'][ID]['layers'][view_layer] = dict()
        oniv['states']['data'][ID]['layers'][view_layer]['objects'] = dict()
        oniv['states']['data'][ID]['layers'][view_layer]['collections'] = dict()
        oniv['states']['data'][ID]['layers'][view_layer]['selections'] = [a.name for a in bpy.context.selected_objects]

        
        if bpy.context.view_layer.objects.active == None:
            oniv['states']['data'][ID]['layers'][view_layer]['active_object'] = None
        else:
            oniv['states']['data'][ID]['layers'][view_layer]['active_object'] = bpy.context.view_layer.objects.active.name

        oniv['states']['data'][ID]['layers'][view_layer]['mode'] = bpy.context.mode

        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        for o in bpy.context.selected_objects:
            o.select_set(False)

        
        for colObj in vlObj.layer_collection.children:
            cname = colObj.name
            oniv['states']['data'][ID]['layers'][view_layer]['collections'][cname] = dict()
            oniv['states']['data'][ID]['layers'][view_layer]['collections'][cname]['hide_viewport'] =                vlObj.layer_collection.children[cname].hide_viewport
            vlObj.layer_collection.children[cname].hide_viewport = False

        
        
        for o in bpy.data.objects:
            oniv['states']['data'][ID]['layers'][view_layer]['objects'][o.name] = o.hide_get()
            o.hide_set(False)

    
    
    
    
    for o in bpy.data.objects:
        if o.type != 'ARMATURE':
            continue
        oniv['states']['data'][ID]['armatures'][o.name] = dict()
        oniv['states']['data'][ID]['armatures'][o.name]['edit_hide'] = dict()
        oniv['states']['data'][ID]['armatures'][o.name]['pose_hide'] = dict()
        oniv['states']['data'][ID]['armatures'][o.name]['hide_select'] = dict()
        o.select_set(True)
        bpy.context.view_layer.objects.active = o

        
        bpy.ops.object.mode_set(mode='POSE')
        for boneObj in o.data.bones:
            bname = boneObj.name
            oniv['states']['data'][ID]['armatures'][o.name]['pose_hide'][bname] = boneObj.hide
            oniv['states']['data'][ID]['armatures'][o.name]['hide_select'][bname] = boneObj.hide_select
            boneObj.hide = False
            boneObj.hide_select = False
        
        bpy.ops.object.mode_set(mode='EDIT')
        for boneObj in o.data.edit_bones:
            bname = boneObj.name
            oniv['states']['data'][ID]['armatures'][o.name]['edit_hide'][bname] = boneObj.hide
            boneObj.hide = False
        bpy.ops.object.mode_set(mode='OBJECT')
        o.select_set(False)

        
        for name in oniv['states']['data'][ID]['layers'][view_layer]['selections']:
            obj[name].select_set(True)
        this_mode = oniv['states']['data'][ID]['layers'][view_layer]['mode']
        if this_mode != 'OBJECT':
            if this_mode == 'EDIT_ARMATURE':
                bpy.ops.object.mode_set(mode='EDIT')
            else:
                bpy.ops.object.mode_set(mode=this_mode)
        active_object = oniv['states']['data'][ID]['layers'][view_layer]['active_object']
        if active_object == None:
            bpy.context.view_layer.objects.active = None
        else:
            bpy.context.view_layer.objects.active = obj[active_object]

    bpy.context.window.view_layer = bpy.data.scenes[scene_name].view_layers[active_view]

    return True





def restore_state():
    

    obj = bpy.context.scene.objects
    oniv = bpy.context.window_manager.oni_view

    if oniv.get('states') == None:
        print("Nothing to restore")
        return False
    if oniv['states'].get('names') == None:
        print("got base but names missing")
        return False

    scene_name = bpy.context.scene.name
    if scene_name not in oniv['states']['names']:
        print("scene not saved, nothing to restore")
        return False

    
    
    
    
    
    selected = [a.name for a in bpy.context.selected_objects]
    if bpy.context.active_object == None:
        active_object = None
    else:
        active_object = bpy.context.active_object.name
    old_mode = bpy.context.mode
    if old_mode == 'EDIT_ARMATURE':
        old_mode = 'EDIT'
    if old_mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    
    see_all()

    
    for o in bpy.context.selected_objects:
        o.select_set(False)
    

    ID = oniv['states']['names'][scene_name]

    print("Restoring state for scene", scene_name, "with ID", ID)

    
    for oname in oniv['states']['data'][ID]['armatures']:
        if oname not in obj:
            print("Missing armature:", oname)
            continue
        obj[oname].select_set(True)
        bpy.context.view_layer.objects.active = obj[oname]
        bpy.ops.object.mode_set(mode='POSE')

        
        for bname in oniv['states']['data'][ID]['armatures'][oname]['pose_hide']:
            if bname in obj[oname].data.bones:
                obj[oname].data.bones[bname].hide = oniv['states']['data'][ID]['armatures'][oname]['pose_hide'][bname]
                obj[oname].data.bones[bname].hide_select = oniv['states']['data'][ID]['armatures'][oname]['hide_select'][bname]
        
        bpy.ops.object.mode_set(mode='EDIT')
        for bname in oniv['states']['data'][ID]['armatures'][oname]['edit_hide']:
            if bname in obj[oname].data.edit_bones:
                obj[oname].data.edit_bones[bname].hide = oniv['states']['data'][ID]['armatures'][oname]['edit_hide'][bname]
        bpy.ops.object.mode_set(mode='OBJECT')
        obj[oname].select_set(False)

    
    for cname in oniv['states']['data'][ID]['collections']:
        if cname in bpy.data.collections:
            bpy.data.collections[cname].hide_viewport = oniv['states']['data'][ID]['collections'][cname]['hide_viewport']
            bpy.data.collections[cname].hide_select = oniv['states']['data'][ID]['collections'][cname]['hide_select']
        else:
            print("collection missing:", c)
    
    for oname in oniv['states']['data'][ID]['objects']:
        if oname in obj:
            obj[oname].hide_select = oniv['states']['data'][ID]['objects'][oname]['hide_select']
            obj[oname].hide_viewport = oniv['states']['data'][ID]['objects'][oname]['hide_viewport']
        else:
            print("object missing from scene:", oname)
    
    active_view = bpy.context.view_layer.name
    for view_layer in oniv['states']['data'][ID]['layers']:
        if view_layer not in  bpy.context.scene.view_layers:
            print("View layer missing:", view_layer)
            continue
        
        vlObj = bpy.context.scene.view_layers[view_layer]
        
        bpy.context.window.view_layer = bpy.data.scenes[scene_name].view_layers[view_layer]
        
        for cname in oniv['states']['data'][ID]['layers'][view_layer]['collections']:
            vlObj.layer_collection.children[cname].hide_viewport =                oniv['states']['data'][ID]['layers'][view_layer]['collections'][cname]['hide_viewport']

        
        for oname in oniv['states']['data'][ID]['layers'][view_layer]['objects']:
            if oname not in obj:
                print("object missing in scene:", oname)
                continue
            hide_state = oniv['states']['data'][ID]['layers'][view_layer]['objects'][oname]
            obj[oname].hide_set(hide_state)


    bpy.context.window.view_layer = bpy.data.scenes[scene_name].view_layers[active_view]
    for o in bpy.context.selected_objects:
        o.select_set(False)
    for oname in selected:
        obj[oname].select_set(True)
    if active_object != None:
        bpy.context.view_layer.objects.active = obj[active_object]
    del oniv['states']['data'][ID]
    del oniv['states']['names'][scene_name]

    return True





class OnigiriViewProperties(bpy.types.PropertyGroup):

    def update_viewable_layers(self, context):
        if oni_settings['terminate'] == True:
            oni_settings['terminate'] = False
            return

    dummy : bpy.props.BoolProperty(default=False)

    
    rig_author_name : bpy.props.StringProperty(default="Unknown")
    rig_author_property : bpy.props.StringProperty(default="")
    
    rig_name : bpy.props.StringProperty(default="")

    
    
"""
    def draw(self, context):
        layout = self.layout

        arm = context.armature

        layout.row().prop(arm, "pose_position", expand=True)

        col = layout.column()
        col.label(text="Layers:")
        col.prop(arm, "layers", text="")
        col.label(text="Protected Layers:")
        col.prop(arm, "layers_protected", text="")

        if context.scene.render.engine == 'BLENDER_GAME':
            col = layout.column()
            col.label(text="Deform:")
            col.prop(arm, "deform_method", expand=True)
"""



class OnigiriViewOperator(bpy.types.Operator):
    """This may unhide everything and make it all selectable.  The toggle can be used to
reverse the process.  It's buggy.  Use it only as a brute force way to examine items but make
sure that you DON'T save your file after.  Save BEFORE using"""

    bl_idname = "onigiri.access_everything"
    bl_label = "See All"

    state : bpy.props.StringProperty(default="")

    
    
        

    def execute(self, context):
        
        
        
        if self.state == "open":
            save_state()
        if self.state == "close":
            restore_state()
        return {'FINISHED'}




class OnigiriPanelView(bpy.types.Panel):
    """Viewable Options"""
    bl_idname = "OBJECT_PT_onigiri_view"
    bl_label = "Viewable"
    bl_space_type = "VIEW_3D"
    bl_category = "Onigiri"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        obj = bpy.data.objects
        oni_view = bpy.context.window_manager.oni_view

        layout = self.layout
        
        
            
            

        
        row = self.layout.row(align=True)
        
        if oni_view.get('states') == None:
            
            oni_view['states'] = dict()
            oni_view['states']['names'] = dict()

        
        scene_name = bpy.context.scene.name
        if scene_name not in oni_view['states'].get('names'):
            
            row.operator(
                "onigiri.access_everything",
                text= "Open Your Eyes",
                icon_value = ico.custom_icons["eye"].icon_id
                ).state = "open"
        else:
            
            row.operator(
                "onigiri.access_everything",
                text= "Close Your Eyes",
                ).state = "close"

        
        

        layout = self.layout
        box = layout.box()
        box.label(
            text = "Rig View Options: " + oni_view.rig_author_name
            )
        
        
        if oni_view.rig_author_property != "": 
            prop_name = oni_view.rig_author_property
            col = box.column(align = True)
            for i in range(0, len(view_layers_order[prop_name]), 2):
                buttons = view_layers_order[prop_name][i:i+2]
                
                row = col.row(align=True)
                for b in buttons:
                    row.prop(
                        bpy.data.armatures[oni_view.rig_name],
                        "layers",
                        index = view_layers[prop_name]['name'][b],
                        toggle=True,
                        text = b
                        )

        if 1 == 0:
            row.prop(
                oni_view,
                "dummy",
                toggle=True,
                text = "Volume Bones"
                )
            row.prop(
                oni_view,
                "dummy",
                toggle=True,
                text = "Non-Human Bones"
                )
            row = col.row(align=True)
            row.prop(
                oni_view,
                "dummy",
                toggle=True,
                text = "Face Bones"
                )
            row.prop(
                oni_view,
                "dummy",
                toggle=True,
                text = "Hand Bones"
                )

        return 







    
    
    

    
    
    
        
    
    


    
    
        






 












