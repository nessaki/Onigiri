import bpy
import os
import uuid
from math import radians, degrees
import mathutils
import tempfile
import traceback
from . import bvh_tools as bvht
from .presets import skeleton as skel
from . import bvh




















def sl_bvh_export(
    armature="",
    mbones=None,
    mrotate=True,
    vbones=None,
    vrotate=True,
    buffer=True,
    file=None,
    translations=False,
    context=None):

    
    
    

    
    
    
    

    
    
    
    if vbones == None:
        vbones = mbones

    bb = bpy.context.scene.bentobuddy
    bba = bpy.context.scene.bb_anim_props
    obj = bpy.data.objects

    
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    for o in bpy.context.selected_objects:
        o.select_set(False)

    armObj = obj[mbones]
    armObj.select_set(True)
    bpy.context.view_layer.objects.active = armObj

    
    
    
    
    
    
    
    
    

    
    
    
    
    
    bad_bones = list()
    print("Examining deformable joint names...")
    for b in armObj.data.bones:
        if b.use_deform == True:
            if b.name not in skel.avatar_skeleton:
                bad_bones.append(b.name)
    if len(bad_bones) > 0:
        print("There are", str(len(bad_bones)), "joints that cannot be exported to SL.  This function cannot continue.")
        print(bad_bones)
        popup("Incompatible joints found, see console for details.", "Error", "ERROR")
        
        
        bad_bones.clear()
        return False

    print("Exporting animation for", armature)
    animation_scale = 39.3701
    animation_fps = bb.animation_fps
    animation_start_frame = bb.animation_start_frame
    animation_end_frame = bb.animation_end_frame

    
    
    
    
    
    
    
    

    print(
        "\n animation_fps", animation_fps,
        "\n animation_start_frame", animation_start_frame,
        "\n animation_end_frame", animation_end_frame,
        "\n file", file,
        "\n")

    
    
    
    
    
    

    
    

    
    loc, rot, scale = armObj.matrix_world.decompose()
    smat = mathutils.Matrix()
    for i in range(3):
        smat[i][i] = scale[i]

    if mrotate == True:
        eu = mathutils.Euler(map(radians, (-90, 0, 0)), 'XYZ')
        mat = mathutils.Matrix.Translation(loc) @ eu.to_matrix().to_4x4() @ smat
        armObj.matrix_world = mat
        bpy.ops.object.transform_apply( rotation=True, location=False, scale=False )

    mbones_buf = bvh.save(
        context=context,
        filepath=file,
        global_scale=animation_scale,
        frame_start=animation_start_frame,
        frame_end=animation_end_frame,
        rotate_mode='NATIVE',
        root_transform_only=translations,
        buffer=buffer,
        )

    
    if mrotate == True:
        
        
        eu = mathutils.Euler(map(radians, (90, 0, 0)), 'XYZ')
        mat = mathutils.Matrix.Translation(loc) @ eu.to_matrix().to_4x4() @ smat
        armObj.matrix_world = mat
        bpy.ops.object.transform_apply( rotation=True, location=False, scale=False )

    
    
    bvh_temp_name = tempfile.gettempdir() + "/bentobuddy_" + get_unique_name_short() + ".bv_"

    armObj.select_set(False)
    armObj = obj[vbones]
    armObj.select_set(True)
    bpy.context.view_layer.objects.active = armObj

    
    if vrotate == True:
        eu = mathutils.Euler(map(radians, (0, 0, 90)), 'XYZ')
        mat = mathutils.Matrix.Translation(loc) @ eu.to_matrix().to_4x4() @ smat
        armObj.matrix_world = mat
        bpy.ops.object.transform_apply( rotation=True, location=False, scale=False )

    vbones_buf = bvh.save(
        context=context,
        filepath=bvh_temp_name,
        global_scale=animation_scale,
        frame_start=animation_start_frame,
        frame_end=animation_end_frame,
        rotate_mode='NATIVE',
        root_transform_only=translations,
        buffer=buffer,
        )

    
    if vrotate == True:
        eu = mathutils.Euler(map(radians, (0, 0, -90)), 'XYZ')
        mat = mathutils.Matrix.Translation(loc) @ eu.to_matrix().to_4x4() @ smat
        armObj.matrix_world = mat
        bpy.ops.object.transform_apply( rotation=True, location=False, scale=False )

    
    if buffer == True:
        bvh_out = bvht.merge(
            vbones=vbones_buf,
            mbones=mbones_buf,
            swap_offsets=False,
            swap_endsites=False,
            swap_motion=True,
            return_type="bvh",
            buffer=buffer,
        )
    else:
        bvh_out = bvht.merge(
            vbones=bvh_temp_name,
            mbones=file,
            swap_offsets=False,
            swap_endsites=False,
            swap_motion=True,
            return_type="bvh",
            buffer=buffer,
        )
    if bvh_out:
        try:
            bvh_file = open(file, "w", newline="", encoding='UTF8')
            bvh_file.write(bvh_out)
            bvh_file.close()
        except Exception as e:
            txt = traceback.format_exc()
            print("some error occurred trying to write the merged bvh")
            print(txt)
    else:
        print("nothing to alter for now, parser is turned off")

    if buffer != True:
        try:
            os.remove(bvh_temp_name)
            print("BB BVH Cleanup...")
        except:
            print("BB Warning: unable to remove temporary file:", bvh_temp_name)

    return True




def popup(message = "", title = "Message Box", icon =  'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
    return






def get_unique_name_short():
    unique_name = str(uuid.uuid4())
    return unique_name.split('-', 1)[0]



