

import os
import bpy
import time
import math
import struct
import tempfile
import mathutils
import traceback
from . import utils
from . import rigutils
from . import mod_data

from .presets import volumes
from .presets import skeleton as skel
from .presets import avastar_to_sl
from .presets import avastar_normalized

U16MAX = 65535
LL_MAX_PELVIS_OFFSET = 5.0




Z90 = mathutils.Matrix ((
    ( 0.0000,  1.0000, 0.0000, 0.0000),
    (-1.0000,  0.0000, 0.0000, 0.0000),
    ( 0.0000,  0.0000, 1.0000, 0.0000),
    ( 0.0000,  0.0000, 0.0000, 1.0000)
    ))

Z90I = Z90.inverted()









pelvis_names = {"mpelvis", "avatar_mPelvis", "hip", "hips", "origin", "COG"}






if 1 == 1:
    props = {}
    
    
    
    props['bake_proxy'] = False
    props['FATAL'] = False

















def export_sl_anim(armature=None, path=None):

    
    
    props['FATAL'] = False

    
    test_proxy = False

    obj = bpy.data.objects
    armObj = obj[armature]
    
    bpy.context.view_layer.update()
    frame_current = bpy.context.scene.frame_current

    
    bb = bpy.context.scene.bentobuddy
    bba = bpy.context.scene.bb_anim_props
    anim = bpy.context.scene.bb_anim
    bb_anim = anim 

    
    
    


    
    
    

    if bb.export_sl_limitations_check_disabled != True:
        if bb.animation_time > 60:
            print("Skipping SL max time check")
            
            
            

    anim.export_sl_anim_label = "Saving: please wait..."
    anim.export_sl_anim_label_short = anim.export_sl_anim_label
    anim.export_sl_anim_alert = True
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

    
    

    

    
    anim_start_frame = bb.animation_start_frame
    anim_end_frame = bb.animation_end_frame
    anim_fps = bb.animation_fps
    disable_location_offsets = bba.disable_location_offsets
    export_volume_motion = bb.export_volume_motion
    mark_tol = anim.mark_tol
    mark_tol_rot = anim.mark_tol_rot
    mark_tol_loc = anim.mark_tol_loc
    fill_missing_keys = bba.fill_missing_keys

    
    
    print("Resample is turned off until a rewrite, this is only useful for reducing file size which is less needed now")
    anim_resample = False
    
    anim_resample_rate_rotation = anim.anim_resample_rate_rotation
    anim_resample_rate_location = anim.anim_resample_rate_location

    anim_deviation_detection = anim.anim_deviation_detection
    
    anim_deviation_rotation = anim.anim_deviation_rotation
    anim_deviation_location = anim.anim_deviation_location
    anim_linear = bb_anim.anim_linear

    high_fidelity = bb_anim.anim_high_fidelity
    anim_use_source_keys = anim.anim_use_source_keys
    anim_use_source_keys_rotation = anim.anim_use_source_keys_rotation
    anim_use_source_keys_location = anim.anim_use_source_keys_location
    anim_use_target_keys = anim.anim_use_target_keys
    anim_use_target_keys_rotation = anim.anim_use_target_keys_rotation
    anim_use_target_keys_location = anim.anim_use_target_keys_location
    anim_use_keys_smooth = anim.anim_use_keys_smooth
    export_avastar_disabled = bb.export_avastar_disabled
    export_avastar_deform_bones = bb.export_avastar_deform_bones

    
    
    ease_in = anim.anim_ease_in_duration
    ease_out = anim.anim_ease_out_duration

    
    
    export_mapped_animation = anim.export_mapped_animation

    export_bentobuddy_disabled = bb.export_bentobuddy_disabled

    
    
    
    bb_split = bpy.context.window_manager.bb_split
    split_enabled = bb_split.split_enabled

    
    
    if anim_start_frame == anim_end_frame:
        print("A frame range of zero was detected, this is non-motion and no content to export")
        popup("Frame range calculates to zero motion, 0 frames, no animation can be exported", "Error", "ERROR")
        return False

    
    print("Checking for animation data")
    has_action = False
    if armObj.animation_data != None:
        if armObj.animation_data.action == None:
            has_action = False
            high_fidelity = True
        else:
            has_action = True
    if armObj.animation_data == None:
        has_action = False
        high_fidelity = True

    
    if has_action == False:
        if anim_deviation_detection == True:
            print("No animation present, reverting to High Fidelity instead")


    
    
    if 1 == 1:
        print("anim_start_frame:", anim_start_frame)
        print("anim_end_frame:", anim_end_frame)
        print("anim_fps:", anim_fps)
        print("ease_in:", ease_in)
        print("ease_out:", ease_out)
        print("disable_location_offsets:", disable_location_offsets)
        print("export_volume_motion:", export_volume_motion)
        print("mark_tol:", mark_tol)
        print("mark_tol_rot:", mark_tol_rot)
        print("mark_tol_loc:", mark_tol_loc)
        print("anim_linear:", anim_linear)
        print("high_fidelity:", high_fidelity)
        print("anim_use_source_keys:", anim.anim_use_source_keys)
        print("anim_use_source_keys_rotation:", anim.anim_use_source_keys_rotation)
        print("anim_use_source_keys_location:", anim.anim_use_source_keys_location)
        print("anim_use_target_keys:", anim.anim_use_target_keys)
        print("anim_use_target_keys_rotation:", anim.anim_use_target_keys_rotation)
        print("anim_use_target_keys_location:", anim.anim_use_target_keys_location)
        print("anim_use_keys_smooth:", anim.anim_use_keys_smooth)
        print("anim_resample:", anim_resample)
        print("anim_resample_rate_rotation:", anim_resample_rate_rotation)
        print("anim_resample_rate_location:", anim_resample_rate_location)
        print("anim_deviation_detection:", anim_deviation_detection)
        print("anim_deviation_rotation:", anim_deviation_rotation)
        print("anim_deviation_location:", anim_deviation_location)
        print("has_action:", has_action)
        print("split_enabled:", split_enabled)
        print("export_avastar_disabled:", export_avastar_disabled)
        print("export_avastar_deform_bones:", export_avastar_deform_bones)
        print("export_mapped_animation:", export_mapped_animation)
        print("export_bentobuddy_disabled:", export_bentobuddy_disabled)

        
        


    
    
    
    
    
    
    
    
    
    if 1 == 0:
        if bba.remove_isolated_keys:
            if has_action == True:
                print("Removing isolated keys")
                print("Isolated keys removed:", remove_isolated_keys(armature=armObj.name))
            else:
                print("remove_isolated_keys is enabled but there's no motion data")
    else:
        print("Skipping check for isolated keys, this would damage an animation that was used for poses only")

    
    
    frame_start = anim_start_frame
    frame_end = anim_end_frame

    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    old_mode = bpy.context.mode
    if test_proxy == True:
        proxyObj = attach_proxy(armature=armObj.name)

    

    
    
    
    
    
    
    
    
    
    time_calc = calculate_time(
        frame_start=frame_start,
        frame_end=frame_end,
        anim_fps=anim_fps,
        )

    total_time = time_calc['total_time']
    loop_in_point = time_calc['loop_in_point']
    loop_out_point = time_calc['loop_out_point']
    time_per_frame = time_calc['time_per_frame']

    
    
    

    
    
    
    is_bentobuddy = False
    is_avastar = False
    if armObj.get('bentobuddy') != None:
        is_bentobuddy = True
    if armObj.get('avastar') != None:
        is_avastar = True

    
    if is_bentobuddy == False:
        print("Not a Bento Buddy rig")

    if export_mapped_animation == True:
        print("Mapped export requested, turning off Bento Buddy rig checking")
        export_bentobuddy_disabled = True

    if export_bentobuddy_disabled == True:
        print("Bento Buddy rig checking is disabled")
    if is_avastar == True and is_bentobuddy == False:
        print("This is an Avastar rig")
        if export_avastar_disabled == True:
            print("Avastar export is disabled, Avastar properties will not be analyzed")
        else:
            print("Avastar checking is enabled, properties will be processed")
    if is_bentobuddy == False and is_avastar == False and export_bentobuddy_disabled == False:
        txt  = "This rig is not flagged as being compatible with Second Life, you can disable \n"
        txt += "the Bento Buddy rig checking in order to attempt to export this if you like, \n"
        txt += "then try again."
        print(txt)
        utils.popup(txt, "Error", "ERROR")
        props['FATAL'] = True
        return False
    if is_bentobuddy == False and is_avastar == True and export_bentobuddy_disabled == False and            export_avastar_disabled == True:
        txt  = "This is not a Bento Buddy rig, it is an Avastar rig, Avastar export feature is disabled \n"
        txt += "and Bento Buddy rig checking is enabled.  This combination of settings prevent the \n"
        txt += "animation from this rig to be exported.  Change at least one of these and try again."
        print(txt)
        utils.popup(txt, "Error", "ERROR")
        props['FATAL'] = True
        return False

    
    
    


    
    
    

    
    time_slices = get_sl_time(total=total_time, tpf=time_per_frame, start=anim_start_frame, stop=anim_end_frame)

    
    is_avastar = False
    if bb.export_avastar_disabled == False:
        if armObj.get('avastar') != None and armObj.get('bentobuddy') == None:
            print("Processing an Avastar rig..")
            print("Frame range - frame_start / frame_end :", frame_start, "/", frame_end)
            print("The following properties will be adjusted:")
            print(" * anim_use_source_keys to True")
            print(" * anim_use_target_keys to False")
            print(" * anim_use_source_rotation_keys to True")
            print(" * anim_use_source_location_keys to True")
            print(" * anim_use_target_rotation_keys to False")
            print(" * anim_use_target_location_keys to False")
            print(" * export_mapped_animation to False")
            print(" * is_avastar = True (internal function flag)")
            anim_use_source_keys = True
            anim_use_target_keys = False
            anim_use_source_rotation_keys = True
            anim_use_source_location_keys = True
            anim_use_target_rotation_keys = False
            anim_use_target_location_keys = False
            export_mapped_animation = False
            is_avastar = True

    
    

    
    
    
    
    
    
    

    
    if anim_linear == True:

        

        print("Linear...")
        if has_action == False:
            print("Linear Animation:")
            print("")
            print("The armature you're attempting to use as an animation source does not have an action associated with it")
            print("There's nothing to export.  The alternative is to bake the influences to the armature or use (High Fidelity)")
            popup("This method of exporting an animation requires that there is one on the rig, but there isn't.", "Error", "ERROR")
            return False
        print("Exporting linear motion...")
        
        
        
        
        
        lerp_data = get_animated_keys(armature=armObj.name, frame_start=frame_start, frame_end=frame_end)
        if lerp_data == False:
            print("Interpolation data returned False from linear process")
            popup("Interpolation data was not valid", "Error", "ERROR")
            return False
        frames = []
        bones = []
        for bone in lerp_data:
            bones.append(bone)
            for trs in lerp_data[bone]:
                frames.extend(lerp_data[bone][trs])
        
        motion = get_motion(armature=armObj.name, frames=frames, bones=bones)
        if motion == False:
            print("Motion data returned False from linear process")
            popup("Motion data was not valid", "Error", "ERROR")
            return False
        bone_data = get_bone_data(armature=armObj.name, motion=motion, lerp_data=lerp_data, time_slices=time_slices, is_avastar=is_avastar)
        if bone_data == False:
            print("Bone data returned False from linear process")
            popup("Bone data was not valid", "Error", "ERROR")
            return False

        
        

    
    
    
    
    
    
    
    

    
    
    
    
    
    elif high_fidelity == True:
        print("High Fidelity...")


        
        
        
        

        
        bones = []
        lerp_source = {}
        lerp_target = {}
        if anim_use_source_keys:

            print("Using source keys")

            if has_action == False:
                print("** Use Source Keys is enabled but there's no animation data to acquire!")
            else:
                print("Use Source Keys enable, gathering keys...")
                
                
                
                
                
                
                lerp_source = get_source_keys(armature=armObj.name, frame_start=frame_start, frame_end=frame_end)
                if lerp_source == False:
                    print("** No key data on the source, does not appear to be animated!")
                else:
                    print("** lerp returned source key data in lerp_source:", lerp_source)
                    bones = [b for b in lerp_source]
        if anim_use_target_keys:

            print("Using target keys")

            
            
            
            lerp_target = get_target_keys(armature=armObj.name, frame_start=frame_start, frame_end=frame_end)
            if len(lerp_target) == 0:
                print("There are no usable target armatures where keys can be gathered.")


        if 1 == 0:
            print("-----------------------------------------------------------")
            print("===========================================================")
            print("-----------------------------------------------------------")
            print("source keys lerp_source:", lerp_source)
            print("target keys lerp_target:", lerp_target)
            print("-----------------------------------------------------------")
            print("===========================================================")
            print("-----------------------------------------------------------")




        
        
        
        
        

        
        
        
        

        
        
        
        
        


        
        
        

        has_keys = False
        if anim_use_source_keys == True or anim_use_target_keys == True:
            has_keys = True
            if len(lerp_source) == 0 and len(lerp_target) == 0:
                print("All attempts to gather keys from the source and/or targets was unsuccessful, continuing to raw bake...")
                anim_use_source_keys = False
                anim_use_target_keys = False
                has_keys = False
            
            
            
            else:
                print("Found keys, processing...")
                lerp_data = {}
                for bone in lerp_source:
                    if bone not in lerp_data:
                        lerp_data[bone] = {}
                    if 'locs' in lerp_source[bone]:
                        if 'locs' not in lerp_data[bone]:
                            lerp_data[bone]['locs'] = []
                        tr = lerp_data[bone]['locs']
                        tr.extend(lerp_source[bone]['locs'])
                        tr = set(tr)
                        lerp_data[bone]['locs'] = list(sorted(tr))
                    if 'rots' in lerp_source[bone]:
                        if 'rots' not in lerp_data[bone]:
                            lerp_data[bone]['rots'] = []
                        tr = lerp_data[bone]['rots']
                        tr.extend(lerp_source[bone]['rots'])
                        tr = set(tr)
                        lerp_data[bone]['rots'] = list(sorted(tr))
                for bone in lerp_target:
                    if bone not in lerp_data:
                        lerp_data[bone] = {}
                    if 'locs' in lerp_target[bone]:
                        if 'locs' not in lerp_data[bone]:
                            lerp_data[bone]['locs'] = []
                        tr = lerp_data[bone]['locs']
                        tr.extend(lerp_target[bone]['locs'])
                        tr = set(tr)
                        lerp_data[bone]['locs'] = list(sorted(tr))
                    if 'rots' in lerp_target[bone]:
                        if 'rots' not in lerp_data[bone]:
                            lerp_data[bone]['rots'] = []
                        tr = lerp_data[bone]['rots']
                        tr.extend(lerp_target[bone]['rots'])
                        tr = set(tr)
                        lerp_data[bone]['rots'] = list(sorted(tr))

                
                

                
                if anim_use_keys_smooth == True:



                    print("------------------------------------------------")
                    print("looks like we're using keys_smooth")
                    print("------------------------------------------------")


                    motion = get_motion(armature=armObj.name, frame_start=frame_start, frame_end=frame_end, bones=[])

                    
                    
                    
                    
                    
                    
                    
                    
                    

                    lerp_smooth = get_baked_animation(
                        armature=armObj.name,
                        motion=motion,
                        frame_start=frame_start,
                        frame_end=frame_end,
                        mark_tol=mark_tol,
                        mark_tol_rot=mark_tol_rot,
                        mark_tol_loc=mark_tol_loc,
                        )
                    
                    
                    
                    if lerp_smooth == False:
                        print("Return from smooth motion resulted nothing")
                        
                        
                    
                    else:
                        for bone in lerp_smooth:
                            if bone not in lerp_data:
                                lerp_data[bone] = {}
                            if 'locs' in lerp_smooth[bone]:
                                if 'locs' not in lerp_data[bone]:
                                    lerp_data[bone]['locs'] = []
                                tr = lerp_data[bone]['locs']
                                tr.extend(lerp_smooth[bone]['locs'])
                                tr = set(tr)
                                lerp_data[bone]['locs'] = list(sorted(tr))
                            if 'rots' in lerp_smooth[bone]:
                                if 'rots' not in lerp_data[bone]:
                                    lerp_data[bone]['rots'] = []
                                tr = lerp_data[bone]['rots']
                                tr.extend(lerp_smooth[bone]['rots'])
                                tr = set(tr)
                                lerp_data[bone]['rots'] = list(sorted(tr))

                
                else:
                    frames = []
                    for bone in lerp_data:
                        frames.extend( lerp_data[bone].get('rots', []) )
                        frames.extend( lerp_data[bone].get('locs', []) )
                    frames = set(frames)
                    frames = list(sorted(frames))
                    motion = get_motion(armature=armObj.name, frame_start=frame_start, frame_end=frame_end, frames=frames)

        

        
        
        if has_keys == False:
        
            print("No key sources, using baked motion...")
            
            
            motion = get_motion(armature=armObj.name, frame_start=frame_start, frame_end=frame_end, bones=[])

            lerp_data = get_baked_animation(
                armature=armObj.name,
                motion=motion,
                frame_start=frame_start,
                frame_end=frame_end,
                mark_tol=mark_tol,
                mark_tol_rot=mark_tol_rot,
                mark_tol_loc=mark_tol_loc,
                )
            if lerp_data == False:
                print("Return from baking resulted in False")
                popup("No detected animation, bake failed", "Error", "ERROR")
                return False

        

        bone_data = get_bone_data(armature=armObj.name, motion=motion, lerp_data=lerp_data, time_slices=time_slices, is_avastar=is_avastar)

        if bone_data == False:
            print("Bone data returned False from baking process")
            popup("Bone data was not valid from baking", "Error", "ERROR")
            return False


        
        if 1 == 0:
            
            
            
            
            

            print("Return from get_bone_data with is_avastar set to", is_avastar, "gives me the following bone_data")
            print("=====================================================")
            print("bone_data:")
            print("-----------------------------------------------------")
            print(bone_data)
            print("bones in bone_data are:", [b for b in bone_data])
            print("=====================================================")

            
            
            
            
            
            




        
        if 1 == 1:
            bone_rots = []
            bone_locs = []
            for bone in bone_data:
                if bone_data[bone].get('rot'):
                    if len(bone_data[bone]['rot']['values']) != 0:
                        bone_rots.append(bone)
                if bone_data[bone].get('loc'):
                    if len(bone_data[bone]['loc']['values']) != 0:
                        bone_locs.append(bone)
            print("----------------------------------------------------------")
            print("Total bones with rotation data:", len(bone_rots))
            print("Total bones with location data:", len(bone_locs))
            print("----------------------------------------------------------")
            print("- Rotations by name -")
            print("rots:", bone_rots)
            print("----------------------------------------------------------")
            print("- Locations by name -")
            print("locs:", bone_locs)
            print("----------------------------------------------------------")



    
    elif anim_deviation_detection == True:

        
        
        
        
        

        
        

        
        

        print("Deviation...")
        print("Exporting interpolated motion...")
        
        lerp_data = get_animated_keys(armature=armObj.name, frame_start=frame_start, frame_end=frame_end)
        if lerp_data == False:
            print("Interpolation data returned False")
            popup("Interpolation data was not valid", "Error", "ERROR")
            return False

        
        
        
        bones = [b for b in lerp_data]

        motion = get_motion(armature=armObj.name, bones=bones, frame_start=frame_start, frame_end=frame_end)
        if motion == False:
            print("Motion data returned False from interpolation process")
            popup("Motion data was not valid", "Error", "ERROR")
            return False

        key_stops = get_key_stops(
            motion=motion, bones=bones,
            frame_start=frame_start, frame_end=frame_end,
            mark_tol_rot=mark_tol_rot, mark_tol_loc=mark_tol_loc)
        if len(key_stops) == 0 or key_stops == False:
            print("Some interpolation data was irretrievable.")
            print("This can happen with static poses or baking an animation so you can ignore it if that's the case.")
            
            

        
        

        
        
        
        
        
        
        
        
        
        
        if 1 == 0:
        
            if 'rots' in lerp_data[bone]:
                rots = lerp_data[bone]['rots']
                changes = get_speed_changes(
                    motion=motion, bone=bone,
                    frame_start=frame_start, frame_end=frame_end,
                    transform='rot', tol=anim_deviation_rotation,
                    )
                frames = rots[:]
                frames.extend(changes)
                lerp_data[bone]['rots'] = sorted(set(frames))
            if 'locs' in lerp_data[bone]:
                locs = lerp_data[bone]['locs']
                changes = get_speed_changes(
                    motion=motion, bone=bone,
                    frame_start=frame_start, frame_end=frame_end,
                    transform='loc', tol=anim_deviation_location,
                    )

        
        
        
        
        
        if 1 == 0:
            rots = lerp_data[bone].get('rots', [])
            locs = lerp_data[bone].get('locs', [])
            if bone in key_stops:
                rots.extend( key_stops[bone].get('rots', []) )
                locs.extend( key_stops[bone].get('locs', []) )
            if len(rots) != 0:
                lerp_data[bone]['rots'] = rots
            if len(locs) != 0:
                lerp_data[bone]['locs'] = locs

        
        
        bone_data = get_bone_data(armature=armObj.name, motion=motion, lerp_data=lerp_data, time_slices=time_slices, is_avastar=is_avastar)
        
        if bone_data == False:
            print("Bone data returned False from interpolation process")
            popup("Bone data was not valid", "Error", "ERROR")
            return False
        if len(bone_data) == 0:
            print("Bone data returned zero length from interpolation process")
            popup("Bone data was not valid", "Error", "ERROR")
            return False


        
        

    
    else:
        print("This is a programming error, but to fix it please chose an export option.")
        print("There are a few, deviations, baking, linear")
        popup("Choose an export option, (Deviation, High Fidelity, Linear)", "No Option Set", "INFO")
        return False

    
    
    
    


    
    
    if props['bake_proxy'] == True:
        print("This is an old bake facility that is obsolete, please report this as a bug")
        popup("You've reach the quiet place, start screaming, or at least report this bug O.o", "Error", "ERROR")
        return False

        proxyObj = attach_proxy(armature=armObj.name)
        print("Baking to proxy:", proxyObj.name)
        key_proxy_rig(armature=proxyObj.name, motion=motion, lerp_data=lerp_data, flatten=False)
        remove_deps(armature=proxyObj.name)
        
        props['bake_proxy'] = False
        
        
        
        
        proxyObj.location.y += 0.4
        print("Your selected rig was copied and the accumulated animation from controllers were applied as keys to this rig.")
        print("This is a new, disposable, rig that contains the entirety of the animation that would have been exported.")
        return True


    if test_proxy == True:
        print("Don't forget to set test_proxy to False !!!")
        remove_deps(armature=proxyObj.name)


    
    if is_avastar == True:
        print("Translating avastar bone names")
        bone_list = []
        
        if bb.export_avastar_deform_bones == True:
            print("export avastar deform bones is True")
            
            for bone in bone_data:
                if bone not in skel.avatar_skeleton:
                    bone_list.append(bone)

            for bone in bone_list:
                bone_data.pop(bone)
        else:
            print("Key detection: deform or control bones for source keys:")
            use_control = False
            pelvis_bones = {'Pelvis', 'COG'}
            
            
            deform_rots = []
            deform_locs = []
            control_rots = []
            control_locs = []
            for bone in bone_data:
                if bone_data[bone].get('rot'):
                    if len(bone_data[bone]['rot']['values']) != 0:

                        
                        if bone in pelvis_bones:
                            control_rots.append(bone)


                        
                        if bone.startswith("m"):
                            deform_rots.append(bone)
                        if bone in skel.avatar_skeleton:
                            if skel.avatar_skeleton[bone]['type'] == "collision":
                                deform_rots.append(bone)
                        else:
                            control_rots.append(bone)

                if bone_data[bone].get('loc'):
                    if len(bone_data[bone]['loc']['values']) != 0:





                        
                        if bone in pelvis_bones:
                            control_locs.append(bone)



                        
                        if bone.startswith("m"):
                            deform_locs.append(bone)
                        if bone in skel.avatar_skeleton:
                            if skel.avatar_skeleton[bone]['type'] == "collision":
                                deform_locs.append(bone)
                        else:
                            control_locs.append(bone)
            print("control_rots:", control_rots)
            print("control_locs:", control_locs)

            if len(control_rots) > 0:
                print("Got control rots")
                use_control = True
            if len(control_locs) > 0:
                print("Got control locs")
                use_control = True

            if use_control == True:
                print("Control bones!  This will override any deform bone animation.")
                
                
                
                
                
                
                
                
                control_temp = control_rots
                control_temp.extend(control_locs)
                control_bones = set(control_temp)
                bone_data_temp = {}
                for bone in control_bones:
                    real_bone = avastar_to_sl.bone_map[bone]

                    
                    
                    
                    
                    if bone in pelvis_bones:
                        print("Found pelvis option:", bone)
                        bone_data_temp[real_bone] = bone_data[real_bone]
                    else:
                        bone_data_temp[real_bone] = bone_data[bone]

                bone_data = bone_data_temp

            else:
                use_deform = False
                if len(deform_rots) > 0:
                    print("Got deform rots")
                    use_deform = True
                if len(deform_locs) > 0:
                    print("Got deform locs")
                    use_deform = True
                if use_deform == True:
                    print("Deform bones!  This will utilise the mBones, Volume bones and any attachment bones.")
                else:
                    txt  = "While attempting to automatically detect animation from control bones\n"
                    txt += "there we no detectable keys or motion.  The process then was to try and\n"
                    txt += "find keys or motion on the deform bones but this failed as well.  There\n"
                    txt += "is nothing to export."
                    print(txt)
                    utils.popup(txt, "Error", "ERROR")
                    return False


    
    print("Generating an ordered bone list with SL bones only")
    bone_list = []

    
    
    if export_mapped_animation == True:
        print("Mapped animation export requested...")



        rename_map = armObj.get('bb_onemap_rename')
        if rename_map == None:
            print("No rename_map on rig, processing normally")
        else:
            print("Found rename_map, translating...")
            bone_data_temp = {}
            for sbone in rename_map.keys():
                tbone = rename_map[sbone]
                print("Processing sbone / tbone:", sbone, "/", tbone)
                if sbone in bone_data:
                    bone_data_temp[tbone] = bone_data[sbone]
            if len(bone_data_temp) == 0:
                print("There was a map but no bones were able to be translated, the resulting dictionary was len 0")
                return False
            bone_data = bone_data_temp
            
            
            print("Generating an ordered bone list from a mapped animation")
            for boneObj in armObj.data.bones:
                bone = boneObj.name

                
                
                if bone in rename_map:
                    tbone = rename_map[bone]
                    
                    if tbone not in bone_data:
                        print("Missing tbone in bone_data, that's fine:", tbone)
                        continue
                    if tbone not in skel.avatar_skeleton:
                        print("missing tbone in skel file, this is NOT ok:", tbone)
                        continue
                    bone_list.append(tbone)
            if len(bone_list) == 0:
                print("Export mapped animation failed with empty list")
                return False

            print("Writing mapped animation...")
            result = write_mapped_animation(
                armature=armObj.name,
                bone_data=bone_data,
                bone_list=bone_list,
                rename_map=rename_map,
                frame_current=frame_current,
                total_time=total_time,
                loop_in_point=loop_in_point,
                loop_out_point=loop_out_point,
                path=path
                )

            
            if result == False:
                txt = "animutils::export_sl_anim: ERROR - write_mapped_animation returned false!"
                return False

           
            if test_proxy == True:
                print("test_proxy is True, generating keys, this could take awhile...")
                key_proxy_rig(armature=proxyObj.name, motion=motion, lerp_data=lerp_data, flatten=False)
                print("finished!")
            return True

    
    
    
    
    if len(bone_list) == 0:
        print("bone_list is empty so we're assuming we'll get an ordered list from the armature...")
        for boneObj in armObj.data.bones:
            if boneObj.name not in skel.avatar_skeleton:
                print("Incompatible bone found [", boneObj.name, "] removing...", sep="")
                bone_data.pop(boneObj.name, '')
                continue
            if boneObj.name in bone_data:
                bone_list.append(boneObj.name)




    if 1 == 0:
        print("KLUDGE: Final cleanup for location data")
        if bba.disable_location_offsets == True:
            print("location offsets is disabled, removing...")
            for bone in bone_data:
                if bone == 'mPelvis':
                    continue
                bone_data[bone].pop("loc", "")
        if bba.disable_pelvis_location_animation == True:
            print("pelvis location animation is disabled, removing...")
            if 'mPelvis' in bone_data:
                bone_data['mPelvis'].pop('loc', '')



    
    if len(bone_data) == 0:
        print("There was no bone data to write, bone_data is empty.  Turn on (Use Source Keys and/or Use Target Keys)")
        print("This can happen if you have an animation associated with your rig but none of the bones qualify for animation")
        popup("Empty bone data, turn on (use keys), see System Console for details", "Empty Bone Data", "ERROR")
        anim.export_sl_anim_label_short = anim.export_sl_anim_label
        anim.export_sl_anim_alert = False
        return False
    if len(bone_list) == 0:
        print("There was no bone list acquired to write, turn on (use keys), bone_list is empty")
        print("This can happen if you have an animation associated with your rig but none of the bones qualify for animation")
        popup("Empty bone list, see System Console for details", "Empty Bone List", "ERROR")
        anim.export_sl_anim_label_short = anim.export_sl_anim_label
        anim.export_sl_anim_alert = False
        return False



    
    if 1 == 0:
        rots = []
        locs = []
        for bone in bone_data:
            if bone_data[bone].get('rot'):
                if len(bone_data[bone]['rot']['values']) != 0:
                    rots.append(bone)
            if bone_data[bone].get('loc'):
                if len(bone_data[bone]['loc']['values']) != 0:
                    locs.append(bone)
        print("Total bones with rotation data:", len(rots))
        print("Total bones with location data:", len(locs))
        print("rots:", rots)
        print("locs:", locs)


    result = write_animation(
        armature=armObj.name,
        bone_data=bone_data,
        bone_list=bone_list,
        frame_current=frame_current,
        total_time=total_time,
        loop_in_point=loop_in_point,
        loop_out_point=loop_out_point,
        path=path,
        )
    
    if result == False:
        txt = "animutils::export_sl_anim: ERROR - write_animation returned false!"
        return False

    
    if test_proxy == True:
        print("test_proxy is True, generating keys, this could take awhile...")
        key_proxy_rig(armature=proxyObj.name, motion=motion, lerp_data=lerp_data, flatten=False)
        print("finished!")

    return True

    
    
    














def write_animation(
    armature=None,
    bone_data=None,
    bone_list=None,
    frame_current=None,
    total_time=None,
    loop_in_point=None,
    loop_out_point=None,
    path=None,
    ):

    
    bb = bpy.context.scene.bentobuddy
    bba = bpy.context.scene.bb_anim_props
    anim = bpy.context.scene.bb_anim
    bb_anim = anim 





    obj = bpy.data.objects
    armObj = obj[armature]

    

    
    file_content = {}

    
    file_content['header'] = {}

    file_content['header']['version'] = (1).to_bytes(2, byteorder='little')
    file_content['header']['sub_version'] = (0).to_bytes(2, byteorder='little')

    
    
    
    if anim.anim_base_priority == -1:
        neg_1 = "FFFFFFFF"
        file_content['header']['base_priority'] = bytes.fromhex(neg_1)
    else:
        file_content['header']['base_priority'] = (anim.anim_base_priority).to_bytes(4, byteorder='little')


    file_content['header']['anim_length'] = struct.pack('f', total_time)
    
    file_content['header']['emote_name'] = struct.pack("%dsB"%len(anim.anim_emote_name), bytes(anim.anim_emote_name,'utf8') , 0)
    
    file_content['header']['loop_in'] = struct.pack('f', loop_in_point)
    file_content['header']['loop_out'] = struct.pack('f', loop_out_point)
    
    file_content['header']['loop'] = (anim.anim_loop).to_bytes(4, byteorder='little')
    
    file_content['header']['ease_in'] = struct.pack('f', anim.anim_ease_in_duration)
    file_content['header']['ease_out'] = struct.pack('f', anim.anim_ease_out_duration)
    
    if anim.anim_hand_pose_enabled == True:
        hp = int(anim.anim_hand_pose)
        file_content['header']['hand_pose'] = struct.pack("i", hp)
    else:
        file_content['header']['hand_pose'] = (0).to_bytes(4, byteorder='little')

    
    file_content['header']['joint_count'] = (int(len(bone_list))).to_bytes(4, byteorder='little')

    
    file_content['joints'] = {}

    for bone in bone_list:
        file_content['joints'][bone] = {}

        
        file_content['joints'][bone]['name'] = struct.pack("%dsB"%len(bone), bytes(bone,'utf8') , 0)
        
        
        priority = anim.anim_base_priority
        if armObj.pose.bones[bone].get('priority_enabled') == 1:
            if armObj.pose.bones[bone].get('priority') != None:
                priority = armObj.pose.bones[bone]['priority']
        if priority == -1:
            neg_1 = "FFFFFFFF"
            file_content['joints'][bone]['priority'] = bytes.fromhex(neg_1)
        else:
            file_content['joints'][bone]['priority'] = struct.pack("i", priority)

        
        
        

        
        

        
        
        

        
        if bone_data[bone].get('rot'):
            rots_ = bone_data[bone]['rot']['values']
            time_ = bone_data[bone]['rot']['times']
            rot_count = len(rots_)
            file_content['joints'][bone]['rot_count'] = rot_count.to_bytes(4, byteorder='little')
            file_content['joints'][bone]['rot_data'] = []

            for i in range(rot_count):
                x,y,z = rots_[i]
                t = time_[i]
                time_data = struct.pack("H", t)
                file_content['joints'][bone]['rot_data'].extend(time_data)
                file_content['joints'][bone]['rot_data'].extend((x).to_bytes(2, byteorder='little'))
                file_content['joints'][bone]['rot_data'].extend((y).to_bytes(2, byteorder='little'))
                file_content['joints'][bone]['rot_data'].extend((z).to_bytes(2, byteorder='little'))
        else:
            rot_count = 0
            file_content['joints'][bone]['rot_count'] = rot_count.to_bytes(4, byteorder='little')

        
        if bone_data[bone].get('loc'):
            locs_ = bone_data[bone]['loc']['values']
            time_ = bone_data[bone]['loc']['times']
            loc_count = len(locs_)
            file_content['joints'][bone]['loc_count'] = loc_count.to_bytes(4, byteorder='little')
            file_content['joints'][bone]['loc_data'] = []

            for i in range(loc_count):
                x,y,z = locs_[i]
                t = time_[i]
                time_data = struct.pack("H", t)
                file_content['joints'][bone]['loc_data'].extend(time_data)
                file_content['joints'][bone]['loc_data'].extend((x).to_bytes(2, byteorder='little'))
                file_content['joints'][bone]['loc_data'].extend((y).to_bytes(2, byteorder='little'))
                file_content['joints'][bone]['loc_data'].extend((z).to_bytes(2, byteorder='little'))
        else:
            loc_count = 0
            file_content['joints'][bone]['loc_count'] = loc_count.to_bytes(4, byteorder='little')

        
        
        file_content['constraints'] = {}
        file_content['constraints']['count'] = (0).to_bytes(4, byteorder='little')

        
        file_data = bytearray()

        for header in file_content['header']:
            file_data.extend( file_content['header'][header] )

        for bone in file_content['joints']:
            file_data.extend( file_content['joints'][bone]['name'] )
            file_data.extend( file_content['joints'][bone]['priority'] )
            file_data.extend( file_content['joints'][bone]['rot_count'] )
            if file_content['joints'][bone].get('rot_data') != None:
                file_data.extend( file_content['joints'][bone]['rot_data'] )
            file_data.extend( file_content['joints'][bone]['loc_count'] )
            if file_content['joints'][bone].get('loc_data') != None:
                file_data.extend( file_content['joints'][bone]['loc_data'] )

        file_data.extend( file_content['constraints']['count'] )


    
    
    bb_anim = bpy.context.scene.bb_anim
    bb = bpy.context.scene.bentobuddy
    
    
    
    
    
    
    
    
    
    
    if bb_anim.anim_details == True:
        T = str( round(total_time, 2) )
        F = str( round(bb.animation_fps, 2) )
        L = str( int(bb_anim.anim_loop) )
        I = str( round(loop_in_point, 2) )
        O = str( round(loop_out_point, 2) )
        E = str( round(bb_anim.anim_ease_in_duration, 2) )
        Z = str( round(bb_anim.anim_ease_out_duration, 2) )
        P = str( bb_anim.anim_base_priority )

        dets_enabled = {
            "T": bb_anim.anim_details_time,
            "F": bb_anim.anim_details_fps,
            "L": bb_anim.anim_details_loop_enabled,
            "I": bb_anim.anim_details_loop_in,
            "O": bb_anim.anim_details_loop_out,
            "E": bb_anim.anim_details_ease_in,
            "Z": bb_anim.anim_details_ease_out,
            "P": bb_anim.anim_details_priority,
            }

        details = {
            "T": T,
            "F": F,
            "L": L,
            "I": I,
            "O": O,
            "E": E,
            "Z": Z,
            "P": P,
            }

        cr = "\n"
        print_string = (
            "Total animation time (T): " + T + cr +
            "Frames per second (F): " + F + cr +
            "Loop enabled (L - 0 or 1): " + L + cr +
            "Loop in point, fractional seconds (I): " + I + cr +
            "Loop out point, fractional seconds (O): " + O + cr +
            "Ease in duration, fractional seconds (E): " + E + cr +
            "Ease out duration, fraction seconds (Z): " + Z + cr +
            "Base Priority, integer from 0 to 6 (P): " + P + cr
            )
        print(print_string)

        file_name = path.split(".")[0]
        anim_dets = "#"
        space = ""
        for det in details:
            if dets_enabled[det] == True:
                print(" - detail enabled:", det)
                anim_dets += space 
                anim_dets += det + details[det]
                space = " "
        anim_dets += "#"
        path = file_name + anim_dets + ".anim"
        print("- Appended details -")
        print(anim_dets)
        print(" -------------------")
    

    

    animF = open(path, 'wb')
    animF.write(file_data)
    animF.close()

    

    bpy.context.scene.bb_anim.property_unset("export_sl_anim_label")
    bpy.context.scene.bb_anim.property_unset("export_sl_anim_label_short")
    anim.export_sl_anim_alert = False

    bpy.context.scene.frame_set(frame_current)

    print("path:", path)
    print("len file_data:", len(file_data))

    
    
    file_length = len(file_data)
    if file_length > 250000:
        txt = "animutils::write_animation: Your file size is rather large, it may not upload.  The file was written but the \n"
        txt += "operation may have been canceled in order to save  you time and allow you to examine the problem before proceeding."
        print(txt)
        utils.popup("File is too large for Second Life, exported anyway but see console for instructions.", "Info", "INFO")
        return False

    return True






def write_mapped_animation(
    armature=None,
    bone_data=None,
    bone_list=None,
    rename_map=None,
    frame_current=None,
    total_time=None,
    loop_in_point=None,
    loop_out_point=None,
    path=None
    ):

    
    bb = bpy.context.scene.bentobuddy
    bba = bpy.context.scene.bb_anim_props
    anim = bpy.context.scene.bb_anim
    bb_anim = anim 

    obj = bpy.data.objects
    armObj = obj[armature]

    

    
    file_content = {}

    
    file_content['header'] = {}

    file_content['header']['version'] = (1).to_bytes(2, byteorder='little')
    file_content['header']['sub_version'] = (0).to_bytes(2, byteorder='little')

    
    
    
    if anim.anim_base_priority == -1:
        neg_1 = "FFFFFFFF"
        file_content['header']['base_priority'] = bytes.fromhex(neg_1)
    else:
        file_content['header']['base_priority'] = (anim.anim_base_priority).to_bytes(4, byteorder='little')


    file_content['header']['anim_length'] = struct.pack('f', total_time)
    
    file_content['header']['emote_name'] = struct.pack("%dsB"%len(anim.anim_emote_name), bytes(anim.anim_emote_name,'utf8') , 0)
    
    file_content['header']['loop_in'] = struct.pack('f', loop_in_point)
    file_content['header']['loop_out'] = struct.pack('f', loop_out_point)
    
    file_content['header']['loop'] = (anim.anim_loop).to_bytes(4, byteorder='little')
    
    file_content['header']['ease_in'] = struct.pack('f', anim.anim_ease_in_duration)
    file_content['header']['ease_out'] = struct.pack('f', anim.anim_ease_out_duration)
    
    if anim.anim_hand_pose_enabled == True:
        hp = int(anim.anim_hand_pose)
        file_content['header']['hand_pose'] = struct.pack("i", hp)
    else:
        file_content['header']['hand_pose'] = (0).to_bytes(4, byteorder='little')

    
    file_content['header']['joint_count'] = (int(len(bone_list))).to_bytes(4, byteorder='little')

    
    file_content['joints'] = {}

    
    rename_rev = {}
    for sbone in rename_map.keys():
        tbone = rename_map[sbone]
        rename_rev[tbone] = sbone
    for bone in bone_list:
        sbone = rename_rev[bone]

        file_content['joints'][bone] = {}

        
        file_content['joints'][bone]['name'] = struct.pack("%dsB"%len(bone), bytes(bone,'utf8') , 0)
        
        
        priority = anim.anim_base_priority
        if armObj.pose.bones[sbone].get('priority_enabled') == 1:
            if armObj.pose.bones[sbone].get('priority') != None:
                priority = armObj.pose.bones[sbone]['priority']
        if priority == -1:
            neg_1 = "FFFFFFFF"
            file_content['joints'][bone]['priority'] = bytes.fromhex(neg_1)
        else:
            file_content['joints'][bone]['priority'] = struct.pack("i", priority)

        
        
        

        
        

        
        
        

        
        if bone_data[bone].get('rot'):
            rots_ = bone_data[bone]['rot']['values']
            time_ = bone_data[bone]['rot']['times']
            rot_count = len(rots_)
            file_content['joints'][bone]['rot_count'] = rot_count.to_bytes(4, byteorder='little')
            file_content['joints'][bone]['rot_data'] = []

            for i in range(rot_count):
                x,y,z = rots_[i]
                t = time_[i]
                time_data = struct.pack("H", t)
                file_content['joints'][bone]['rot_data'].extend(time_data)
                file_content['joints'][bone]['rot_data'].extend((x).to_bytes(2, byteorder='little'))
                file_content['joints'][bone]['rot_data'].extend((y).to_bytes(2, byteorder='little'))
                file_content['joints'][bone]['rot_data'].extend((z).to_bytes(2, byteorder='little'))
        else:
            rot_count = 0
            file_content['joints'][bone]['rot_count'] = rot_count.to_bytes(4, byteorder='little')

        
        if bone_data[bone].get('loc'):
            locs_ = bone_data[bone]['loc']['values']
            time_ = bone_data[bone]['loc']['times']
            loc_count = len(locs_)
            file_content['joints'][bone]['loc_count'] = loc_count.to_bytes(4, byteorder='little')
            file_content['joints'][bone]['loc_data'] = []

            for i in range(loc_count):
                x,y,z = locs_[i]
                t = time_[i]
                time_data = struct.pack("H", t)
                file_content['joints'][bone]['loc_data'].extend(time_data)
                file_content['joints'][bone]['loc_data'].extend((x).to_bytes(2, byteorder='little'))
                file_content['joints'][bone]['loc_data'].extend((y).to_bytes(2, byteorder='little'))
                file_content['joints'][bone]['loc_data'].extend((z).to_bytes(2, byteorder='little'))
        else:
            loc_count = 0
            file_content['joints'][bone]['loc_count'] = loc_count.to_bytes(4, byteorder='little')

        
        
        file_content['constraints'] = {}
        file_content['constraints']['count'] = (0).to_bytes(4, byteorder='little')

        
        file_data = bytearray()

        for header in file_content['header']:
            file_data.extend( file_content['header'][header] )

        for bone in file_content['joints']:
            file_data.extend( file_content['joints'][bone]['name'] )
            file_data.extend( file_content['joints'][bone]['priority'] )
            file_data.extend( file_content['joints'][bone]['rot_count'] )
            if file_content['joints'][bone].get('rot_data') != None:
                file_data.extend( file_content['joints'][bone]['rot_data'] )
            file_data.extend( file_content['joints'][bone]['loc_count'] )
            if file_content['joints'][bone].get('loc_data') != None:
                file_data.extend( file_content['joints'][bone]['loc_data'] )

        file_data.extend( file_content['constraints']['count'] )


    
    
    bb_anim = bpy.context.scene.bb_anim
    bb = bpy.context.scene.bentobuddy
    
    
    
    
    
    
    
    
    
    
    if bb_anim.anim_details == True:
        T = str( round(total_time, 2) )
        F = str( round(bb.animation_fps, 2) )
        L = str( int(bb_anim.anim_loop) )
        I = str( round(loop_in_point, 2) )
        O = str( round(loop_out_point, 2) )
        E = str( round(bb_anim.anim_ease_in_duration, 2) )
        Z = str( round(bb_anim.anim_ease_out_duration, 2) )
        P = str( bb_anim.anim_base_priority )

        dets_enabled = {
            "T": bb_anim.anim_details_time,
            "F": bb_anim.anim_details_fps,
            "L": bb_anim.anim_details_loop_enabled,
            "I": bb_anim.anim_details_loop_in,
            "O": bb_anim.anim_details_loop_out,
            "E": bb_anim.anim_details_ease_in,
            "Z": bb_anim.anim_details_ease_out,
            "P": bb_anim.anim_details_priority,
            }

        details = {
            "T": T,
            "F": F,
            "L": L,
            "I": I,
            "O": O,
            "E": E,
            "Z": Z,
            "P": P,
            }

        cr = "\n"
        print_string = (
            "Total animation time (T): " + T + cr +
            "Frames per second (F): " + F + cr +
            "Loop enabled (L - 0 or 1): " + L + cr +
            "Loop in point, fractional seconds (I): " + I + cr +
            "Loop out point, fractional seconds (O): " + O + cr +
            "Ease in duration, fractional seconds (E): " + E + cr +
            "Ease out duration, fraction seconds (Z): " + Z + cr +
            "Base Priority, integer from 0 to 6 (P): " + P + cr
            )
        print(print_string)

        file_name = path.split(".")[0]
        anim_dets = "#"
        space = ""
        for det in details:
            if dets_enabled[det] == True:
                print(" - detail enabled:", det)
                anim_dets += space 
                anim_dets += det + details[det]
                space = " "
        anim_dets += "#"
        path = file_name + anim_dets + ".anim"
        print("- Appended details -")
        print(anim_dets)
        print(" -------------------")
    

    

    animF = open(path, 'wb')
    animF.write(file_data)
    animF.close()


    

    bpy.context.scene.bb_anim.property_unset("export_sl_anim_label")
    bpy.context.scene.bb_anim.property_unset("export_sl_anim_label_short")
    anim.export_sl_anim_alert = False

    bpy.context.scene.frame_set(frame_current)

    print("path:", path)
    print("len file_data:", len(file_data))

    
    
    file_length = len(file_data)
    if file_length > 250000:
        txt = "animutils::write_mapped_animation: Your file size is rather large, it may not upload.  The file was written but the \n"
        txt += "operation may have been canceled in order to save  you time and allow you to examine the problem before proceeding."
        print(txt)
        utils.popup("File is too large for Second Life, exported anyway but see console for instructions.", "Info", "INFO")
        return False

    return True







def get_baked_animation(
    armature=None,
    frame_start=0,
    frame_end=0,
    motion=None,
    mark_tol=False,
    mark_tol_rot=0.001,
    mark_tol_loc=0.001,
    ):

    if abs(frame_start - frame_end) == 0:
        print("get_baked_animation reports: no frames to examine")
        return False

    
    
    
    
    
    mrot = mark_tol_rot
    mloc = mark_tol_loc

    bb = bpy.context.scene.bentobuddy
    bba = bpy.context.scene.bb_anim_props
    bb_anim = bpy.context.scene.bb_anim

    obj = bpy.data.objects
    armObj = obj[armature]

    
    _abs = abs
    _ce = close_enough
    _round = round

    
    
    
    animated = set()
    if mark_tol == True:
        print("  tolerance marking enabled, checking for motion...")
        for bone in motion:
            
            
            frames = [ f for f in motion[bone] ]
            f0 = frames[0]
            rot_start = motion[bone][f0]['rot']
            loc_start = motion[bone][f0]['loc']

            
            
            
            
            
            
            
            

            
            
            for frame in frames:
                rot = motion[bone][frame]['rot']
                loc = motion[bone][frame]['loc']
                
                rot_mark = False
                loc_mark = False
                for i in range(3):
                    if _ce(rot_start[i], rot[i], tol=mrot) == True:
                        rot_mark = True
                        animated.add(bone)
                        break
                    if _ce(loc_start[i], loc[i], tol=mloc) == True:
                        loc_mark = True
                        animated.add(bone)
                        break
                if rot_mark == True or loc_mark == True:
                    break
        print("Bones that exceeded motion tolerance:", animated)
    else:
        print("  no tolerance marking, adding all bones as animated")
        for bone in motion:
            animated.add(bone)

    if len(animated) == 0:
        print("No animated bones were detected when attempting to bake high fidelity motion")
        return False

    
    
    
    
    
    
    
    

    key_stops = get_key_stops(
        motion=motion, bones=animated,
        frame_start=frame_start, frame_end=frame_end,
        mark_tol_rot=mrot, mark_tol_loc=mloc)


    if 1 == 0:
        print("---------------------------------------------")
        print("Going into get_key_stops:")
        
        print("animated:", animated)
        print("frame_start:", frame_start)
        print("frame_end:", frame_end)
        print("mrot:", mrot)
        print("mloc:", mloc)
        print("---------------------------------------------")

        print("---------------------------------------------")
        print("Returned from key_stops:")
        print(key_stops)
        print("---------------------------------------------")


    
    

    
    keep_rots = set() 
    keep_locs = set() 
    if bb_anim.anim_resample == True:
        print("resampling baked animation")
        r = [i for i in range(frame_start, frame_end+1, bb_anim.anim_resample_rate_rotation)]
        l = [i for i in range(frame_start, frame_end+1, bb_anim.anim_resample_rate_location)]
        keep_rots = set(r)
        keep_locs = set(l)

    
    stage_one = key_stops

    
    
    if len(key_stops) > 0:
        for bone in animated:
            if bone not in stage_one:
                stage_one[bone] = {}
            for frame in motion[bone]:
                if frame not in keep_rots:
                    if 'rots' not in stage_one[bone]:
                        stage_one[bone]['rots'] = []
                    stage_one[bone]['rots'].append(frame)
                if frame not in keep_locs:
                    if 'locs' not in stage_one[bone]:
                        stage_one[bone]['locs'] = []
                    stage_one[bone]['locs'].append(frame)
    
    if bb.export_volume_motion == False:
        bones_del = []
        for bone in stage_one:
            if bone in volumes.vol_joints:
                bones_del.append(bone)
        for bone in bones_del:
            stage_one.pop(bone, "")
        print("Removed the following volume bones from animation:")
        print(bones_del)

    
    pelvis_bones = {'mpelvis', 'hip', 'hips'}
    if bba.disable_pelvis_location_animation == True:
        
        bones_del = []
        for bone in stage_one:
            bone_lower = bone.lower()
            if bone_lower in pelvis_bones:
                bones_del.append(bone)
        for bone in bones_del:
            print("disable_pelvis_location_animation is True, removing root from location data:", bone)
            stage_one.pop(bone, "")
 
    
    if bba.disable_location_offsets == True:
        
        bones_del = []
        for bone in stage_one:
            bone_lower = bone.lower()
            if bone_lower not in pelvis_bones:
                stage_one[bone].pop('locs', [])
            
            if len(stage_one[bone]) == 0:
                bones_del.append(bone)
        for bone in bones_del:
            print("disable_location_offsets is True, removing location data from bone:", bone)
            stage_one.pop(bone, "")

    
    
    
    if mark_tol == True:
        lerp_data = {}
        for bone in stage_one:
            
            
            
            lerp_data[bone] = {}
            if 'rots' in stage_one[bone]:
                
                rots = stage_one[bone]['rots']
                frames = clean_frames(bone=bone, motion=motion, frames=rots, tol=mrot, transform="rot")
                lerp_data[bone]['rots'] = frames
            if 'locs' in stage_one[bone]:
                
                locs = stage_one[bone]['locs']
                frames = clean_frames(bone=bone, motion=motion, frames=locs, tol=mloc, transform="loc")
                lerp_data[bone]['locs'] = frames
    else:
        lerp_data = stage_one

    return lerp_data







def remove_isolated_keys(armature=None):
    armObj = bpy.data.objects[armature]
    count = 0
    action = armObj.animation_data.action
    for fcurve in action.fcurves:
        if len(fcurve.keyframe_points) < 2:
            action.fcurves.remove(fcurve)
            count +=1
    return count







def key_proxy_rig(armature=None, motion=None, lerp_data=None, flatten=False):
    armObj = bpy.data.objects[armature]

    for bone in lerp_data:
        rots = lerp_data[bone].get('rots', [])
        locs = lerp_data[bone].get('locs', [])

        
        frames = rots[:]
        frames.extend(locs)
        frames = set(frames)

        for frame in frames:
            bpy.context.scene.frame_set(frame)
            pmat = motion[bone][frame]['pmat']
            boneObj = armObj.pose.bones[bone]
            boneObj.matrix = pmat
            rotation_mode = boneObj.rotation_mode
            if rotation_mode == 'QUATERNION':
                rmode = 'rotation_quaternion'
            else:
                rmode = 'rotation_euler'
            if frame in rots:
                boneObj.keyframe_insert(data_path=rmode, frame=frame)
            if frame in locs:
                boneObj.keyframe_insert(data_path='location', frame=frame)

    
    
    
    if flatten == True:
        for fc in armObj.animation_data.action.fcurves:
            for k in fc.keyframe_points:
                k.interpolation = 'LINEAR'

    return True









def get_animated_frames(
    armature=None,
    frame_start=0,
    frame_end=0,
    action=False,
    ):

    bb = bpy.context.scene.bentobuddy
    bba = bpy.context.scene.bb_anim_props
    bb_anim = bpy.context.scene.bb_anim

    export_volume_motion - bb.export_volume_motion

    obj = bpy.data.objects
    armObj = obj[armature]

    
    
    rot_frames = []
    loc_frames = []
    if bb_anim.anim_resample == True:
        rots = [i for i in range(frame_start, frame_end+1, bb_anim.anim_resample_rate_rotation)]
        rot_frames.append(frame_start)
        rot_frames.extend(rots)
        rot_frames.append(frame_end)
        locs = [i for i in range(frame_start, frame_end+1, bb_anim.anim_resample_rate_location)]
        loc_frames.append(frame_start)
        loc_frames.extend(locs)
        loc_frames.append(frame_end)
    else:
        rot_frames = [i for i in range(frame_start, frame_end+1)]
        loc_frames = [i for i in range(frame_start, frame_end+1)]

    
    if action == False:
        frame_data = {}
        for boneObj in armObj.data.bones:
            bone = boneObj.name

            
            if bb.export_volume_motion == False:
                if bone in volumes.vol_joints:
                    continue

            frame_data[bone] = {}
            frame_data[bone]['rot'] = {}
            frame_data[bone]['rot']['frames'] = rot_frames
            bone_lower = bone.lower()
            if bone_lower == 'mpelvis' or bone_lower == 'hip' or bone_lower == 'hips':
                if bba.disable_pelvis_location_animation == True:
                    continue
            if bba.disable_location_offsets == True:
                continue
            frame_data[bone]['loc'] = {}
            frame_data[bone]['loc']['frames'] = loc_frames
        return frame_data

    actionObj = armObj.animation_data.action
    fcurves = actionObj.fcurves
    fcurve_paths = {}
    for boneObj in armObj.data.bones:

        path_key = 'pose.bones["' + boneObj.name + '"]'
        fcurve_paths[path_key] = boneObj.name

    frame_data = {}
    for fc in fcurves:
        dp, idx = fc.data_path, fc.array_index
        bone_path, delimiter, transform_type = dp.rpartition('.')
        if bone_path not in fcurve_paths:
            continue
        real_bone = fcurve_paths[bone_path]
        rot_mode = armObj.pose.bones[real_bone].rotation_mode
        if transform_type == 'rotation_quaternion' and rot_mode == 'QUATERNION':
            loc_rot = 'rot'
            if idx == 0:
                continue
        elif transform_type == 'rotation_euler' and rot_mode != 'QUATERNION':
            loc_rot = 'rot'
        elif transform_type == 'location':
            bone_lower = real_bone.lower()
            if bone_lower == 'mpelvis' or bone_lower == 'hip' or bone_lower == 'hips':
                if bba.disable_pelvis_location_animation == True:
                    continue
            if bba.disable_location_offsets == True:
                continue
            loc_rot = 'loc'
        elif transform_type == 'scale':
            continue

        
        
        elif transform_type == 'rotation_euler' and rot_mode == 'QUATERNION':
            print("The rotation type of this particular key frame is incompatible with the bone rotation mode.")
            print("There is no logical way to proceed, you have to change the affected rig bones rotation mode")
            print("manually or retarget the offending animation to a new rig, make sure the new rig has only")
            print("quaternion rotation modes on the bones.")
            print("--")
            print("Potentially you can convert the animation using one of Bento Buddy's tools, from Euler to")
            print("quaternion, but you will still need to make sure that the bones are compliant.  It's expected")
            print("that this is a Bento Buddy rig so just generate a new rig to test the results.")
            loc_rot = 'rot'

        else:
            continue
        if real_bone not in frame_data:
            frame_data[real_bone] = {}
        if loc_rot not in frame_data[real_bone]:
            frame_data[real_bone][loc_rot] = {}

        
        frames = [int(k.co.x) for k in fc.keyframe_points]

        
        
        
        if bb_anim.anim_resample == True:
            frames.append(frame_start)
            frames.append(frame_end)
        
        
        frames_set = set(frames)
        frame_numbers = list(sorted(frames_set))

        
        
        new_frames = []
        if bb_anim.anim_resample == True:
            if loc_rot == 'rot':
                stride = bb_anim.anim_resample_rate_rotation
            else:
                stride = bb_anim.anim_resample_rate_location

            new_frames.append(frame_numbers[0])

            for f in range( 1, len(frame_numbers), stride):
                new_frames.append(f)
            new_frames.append(frame_numbers[-1])

            frame_numbers = new_frames

        frame_data[real_bone][loc_rot]['frames'] = frame_numbers

    return frame_data









def get_animated_keys(
    armature=None,
    frame_start=0,
    frame_end=0
    ):
    bb = bpy.context.scene.bentobuddy
    bba = bpy.context.scene.bb_anim_props
    bb_anim = bpy.context.scene.bb_anim

    obj = bpy.data.objects
    armObj = obj[armature]

    
    frame_error = False

    
    
    actionObj = armObj.animation_data.action

    
    fcurves = actionObj.fcurves

    
    
    
    
    
    
    
    fcurve_paths = {}
    for boneObj in armObj.data.bones:

        path_key = 'pose.bones["' + boneObj.name + '"]'
        fcurve_paths[path_key] = boneObj.name

    
    frame_data = {}

    
    
    
    
    
    
    for fc in fcurves:

        
        

        
        
        
        
        

        
        
        dp, idx = fc.data_path, fc.array_index

        
        
        bone_path, delimiter, transform_type = dp.rpartition('.')

        
        
        if bone_path not in fcurve_paths:
            continue

        
        
        
        real_bone = fcurve_paths[bone_path]

        
        if bb.export_volume_motion == False:
            if real_bone in volumes.vol_joints:
                continue

        
        rot_mode = armObj.pose.bones[real_bone].rotation_mode

        
        

        
        

        if transform_type == 'rotation_quaternion' and rot_mode == 'QUATERNION':
            loc_rot = 'rots'

            
            if idx == 0:
                
                continue

        elif transform_type == 'rotation_euler' and rot_mode != 'QUATERNION':
            loc_rot = 'rots'

        elif transform_type == 'location':
            
            

            
            bone_lower = real_bone.lower()
            if bone_lower == 'mpelvis' or bone_lower == 'hip' or bone_lower == 'hips':
                if bba.disable_pelvis_location_animation == True:
                    continue
            
            elif bba.disable_location_offsets == True:
                continue

            loc_rot = 'locs'

        
        
        
        
        
        elif transform_type == 'scale':
            continue

        
        
        elif transform_type == 'rotation_euler' and rot_mode == 'QUATERNION':
            print("The rotation type of this particular key frame is incompatible with the bone rotation mode.")
            print("There is no logical way to proceed, you have to change the affected rig bones rotation mode")
            print("manually or retarget the offending animation to a new rig, make sure the new rig has only")
            print("quaternion rotation modes on the bones.")
            print("--")
            print("Potentially you can convert the animation using one of Bento Buddy's tools, from Euler to")
            print("quaternion, but you will still need to make sure that the bones are compliant.  It's expected")
            print("that this is a Bento Buddy rig so just generate a new rig to test the results.")
            loc_rot = 'rots'

        else:
            
            
            continue

        
        if real_bone not in frame_data:
            frame_data[real_bone] = {}

        if loc_rot not in frame_data[real_bone]:
            frame_data[real_bone][loc_rot] = {}

        
        frames = [int(k.co.x) for k in fc.keyframe_points]

        
        
        
        
        
        
        
        
        frames.append(frame_start)
        frames.append(frame_end)

        
        
        
        
        frames_cleaned = []
        for f in frames:
            if f < frame_start or f > frame_end:
                continue
            frames_cleaned.append(f)

        
        frames_set = set(frames_cleaned)

        
        frame_numbers = list(sorted(frames_set))

        if len(frame_numbers) == 0:
            frame_error = True

        
        
        
        
        
        frame_data[real_bone][loc_rot] = frame_numbers

    if frame_error == True:
        print("An unexpected condition occurred!")
        print("Either your frame range is wrong or the action associated with this armature,", armObj.name)
        print("have different rotation modes, eg: quaternion vs Euler, please correct the issue on your rig.")

    return frame_data








def get_source_keys(
    armature=None,
    frame_start=0,
    frame_end=0
    ):
    bb = bpy.context.scene.bentobuddy
    bba = bpy.context.scene.bb_anim_props
    anim = bpy.context.scene.bb_anim
    bb_anim = bpy.context.scene.bb_anim

    
    use_rotation = anim.anim_use_source_keys_rotation
    use_location = anim.anim_use_source_keys_location

    obj = bpy.data.objects
    armObj = obj[armature]

    
    
    actionObj = armObj.animation_data.action

    
    fcurves = actionObj.fcurves

    
    
    
    
    
    
    
    fcurve_paths = {}
    for boneObj in armObj.data.bones:

        path_key = 'pose.bones["' + boneObj.name + '"]'
        fcurve_paths[path_key] = boneObj.name

    
    frame_data = {}

    
    
    
    
    
    
    for fc in fcurves:

        
        

        
        
        
        
        

        
        
        dp, idx = fc.data_path, fc.array_index

        
        
        bone_path, delimiter, transform_type = dp.rpartition('.')

        
        
        if bone_path not in fcurve_paths:
            continue

        
        
        
        real_bone = fcurve_paths[bone_path]

        
        if bb.export_volume_motion == False:
            if real_bone in volumes.vol_joints:
                continue

        
        
        loc_rot = ''

        if transform_type == 'rotation_quaternion' or transform_type == 'rotation_euler':
            if use_rotation == True:
                loc_rot = 'rots'
        elif transform_type == 'location':
            if use_location == True:
                loc_rot = 'locs'
        else:
            
            continue
        if loc_rot == '':
            continue

        
        if real_bone not in frame_data:
            frame_data[real_bone] = {}

        if loc_rot not in frame_data[real_bone]:
            frame_data[real_bone][loc_rot] = {}

        
        frames = [int(k.co.x) for k in fc.keyframe_points]

        
        frames.append(frame_start)
        frames.append(frame_end)

        
        
        
        
        frames_cleaned = []
        for f in frames:
            if f < frame_start or f > frame_end:
                continue
            frames_cleaned.append(f)

        
        frames_set = set(frames_cleaned)

        
        frame_numbers = list(sorted(frames_set))

        if len(frame_numbers) == 0:
            frame_error = True

        
        
        
        
        
        frame_data[real_bone][loc_rot] = frame_numbers

    return frame_data










def get_target_keys(
    armature=None,
    frame_start=0,
    frame_end=0,
    ):

    bb = bpy.context.scene.bentobuddy
    bba = bpy.context.scene.bb_anim_props
    anim = bpy.context.scene.bb_anim
    bb_anim = bpy.context.scene.bb_anim

    
    use_rotation = anim.anim_use_target_keys_rotation
    use_location = anim.anim_use_target_keys_location

    obj = bpy.data.objects
    armObj = obj[armature]

    
    
    tarms = {}
    tbones = []

    
    
    bone_targets = {}
    constraint_types = {'COPY_ROTATION', 'COPY_LOCATION', 'COPY_TRANSFORMS', 'CHILD_OF'}
    for boneObj in armObj.pose.bones:
        sbone = boneObj.name
        for cObj in boneObj.constraints:
            if cObj.type in constraint_types:
                if cObj.target == None:
                    continue
                
                
                
                
                tarmObj = cObj.target

                
                
                
                tarmReal = armObj.get('bb_motion_director')
                if tarmReal != None:
                    if utils.is_valid(tarmReal):
                        tarmObj = tarmReal
                if tarmObj.type != 'ARMATURE':
                    continue
                if cObj.subtarget == "":
                    continue
                if sbone not in bone_targets:
                    bone_targets[sbone] = {}
                tarm = tarmObj.name
                if tarm not in bone_targets[sbone]:
                    bone_targets[sbone][tarm] = {}
                tbone = cObj.subtarget

                
                
                

                
                
                bone_path = 'pose.bones["' + tbone + '"]'
                bone_targets[sbone][tarm][bone_path] = tbone

    
    frame_data = {}
    for sbone in bone_targets:
        for tarm in bone_targets[sbone]:

            if obj[tarm].animation_data == None:
                continue

            if obj[tarm].animation_data.action == None:
                continue
            fcurves = obj[tarm].animation_data.action.fcurves
            for fc in fcurves:
                
                dp, idx = fc.data_path, fc.array_index

                
                
                bone_path, delimiter, transform_type = dp.rpartition('.')

                
                
                if bone_path not in bone_targets[sbone][tarm]:
                    continue

                
                real_bone = bone_targets[sbone][tarm][bone_path]

                
                
                
                if bb.export_volume_motion == False:
                    if sbone in volumes.vol_joints:
                        continue

                
                
                loc_rot = ''

                if transform_type == 'rotation_quaternion' or transform_type == 'rotation_euler':
                    if use_rotation == True:
                        loc_rot = 'rots'

                elif transform_type == 'location':
                    if use_location == True:
                        loc_rot = 'locs'
                else:
                    
                    continue
                if loc_rot == '':
                    continue

                
                
                
                
                if sbone not in frame_data:
                    frame_data[sbone] = {}

                if loc_rot not in frame_data[sbone]:
                    frame_data[sbone][loc_rot] = {}

                
                
                
                
                
                
                

                
                frames = [int(k.co.x) for k in fc.keyframe_points]

                
                frames.append(frame_start)
                frames.append(frame_end)

                
                
                
                
                frames_cleaned = []
                for f in frames:
                    if f < frame_start or f > frame_end:
                        continue
                    frames_cleaned.append(f)

                
                frames_set = set(frames_cleaned)

                
                frame_numbers = list(sorted(frames_set))

                if len(frame_numbers) == 0:
                    frame_error = True

                
                
                
                
                
                frame_data[sbone][loc_rot] = frame_numbers

    return frame_data












def get_action_keys(armature=None, action=None):
    obj = bpy.data.objects
    armObj = obj[armature]
    actionObj = bpy.data.actions[action]
    been_here = False 
    fcurves = actionObj.fcurves
    frame_data = {}

    
    fcurve_paths = {}
    for boneObj in armObj.data.bones:
        path_key = 'pose.bones["' + boneObj.name + '"]'
        fcurve_paths[path_key] = boneObj.name

    for fc in fcurves:
        dp, idx = fc.data_path, fc.array_index
        bone_path, delimiter, transform_type = dp.rpartition('.')
        if bone_path not in fcurve_paths:
            continue
        real_bone = fcurve_paths[bone_path]
        rot_mode = armObj.pose.bones[real_bone].rotation_mode
        if transform_type == 'rotation_quaternion' and rot_mode == 'QUATERNION':
            lrs = 'rotation'
            
            if idx == 0:
                continue
        elif transform_type == 'rotation_euler' and rot_mode != 'QUATERNION':
            lrs = 'rotation'
        elif transform_type == 'location':
            lrs = 'location'
        elif transform_type == 'scale':
            lrs = 'scale'

        
        
        elif transform_type == 'rotation_euler' and rot_mode == 'QUATERNION':
            if been_here == False:
                print("The rotation type of this particular key frame is incompatible with the bone rotation mode.")
                print("There is no logical way to proceed, you have to change the affected rig bones rotation mode")
                print("manually or retarget the offending animation to a new rig, make sure the new rig has only")
                print("quaternion rotation modes on the bones.")
                print("--")
                print("Potentially you can convert the animation using one of Bento Buddy's tools, from Euler to")
                print("quaternion, but you will still need to make sure that the bones are compliant.  It's expected")
                print("that this is a Bento Buddy rig so just generate a new rig to test the results.")
                print("The attempt to generate the keys requested will continue but will probably have animation anomalies.")
                been_here = True
            lrs = 'rot'

        else:
            continue


        
        frames = [int(k.co.x) for k in fc.keyframe_points]
        
        
        
        
        
        for f in frames:
            if f not in frame_data:
                frame_data[f] = {}
            if real_bone not in frame_data[f]:
                frame_data[f][real_bone] = {}
            if lrs not in frame_data[f][real_bone]:
                frame_data[f][real_bone][lrs] = True

    return frame_data








def get_matrices(armature=None, bones=[], frames=None):
    obj = bpy.data.objects
    armObj = obj[armature]
    matrices = {}

    for f in frames:
        bpy.context.scene.frame_set(f)
        for bone in bones:
            bone_lower = bone.lower()

            
            if bone not in matrices:
                matrices[bone] = {}
            pbmat = armObj.pose.bones[bone].matrix.copy()
            dbmat = armObj.data.bones[bone].matrix.copy()
            dbmatl = armObj.data.bones[bone].matrix_local.copy()


            
            if 1 == 1:
                if bone_lower not in pelvis_names:
                    pbpmat = armObj.pose.bones[bone].parent.matrix.copy()
                    dbpmatl = armObj.data.bones[bone].parent.matrix_local.copy()
                else:
                    pbpmat = mathutils.Matrix()
                    dbpmatl = mathutils.Matrix()
                if bone_lower not in pelvis_names:
                    dbpmat = armObj.data.bones[bone].parent.matrix.copy()
                else:
                    dbpmat = mathutils.Matrix()


            if 1 == 0:
                if armObj.pose.bones[bone].parent:
                    pbpmat = armObj.pose.bones[bone].parent.matrix.copy()
                    dbpmatl = armObj.data.bones[bone].parent.matrix_local.copy()
                else:
                    pbpmat = mathutils.Matrix()
                    dbpmatl = mathutils.Matrix()
                if armObj.pose.bones[bone].parent:
                    dbpmat = armObj.data.bones[bone].parent.matrix.copy()
                else:
                    dbpmat = mathutils.Matrix()


            pbmatI = pbmat.inverted()
            pbpmatI = pbpmat.inverted()
            dbpmatlI = dbpmatl.inverted()
            rp = pbpmat @ dbpmatlI @ dbmatl
            rp_composed = rp.inverted() @ pbmat
            m3 = dbmatl.to_3x3()
            m4 = m3.to_4x4()
            m4I = m4.inverted()
            mF = m4 @ rp_composed @ m4I
            
            matrices[bone][f] = {}
            matrices[bone][f]['matrix'] = mF

    return matrices














def clean_motion(matrices=None, rot_tol=1.0, loc_tol=0.01):

    eu_tol = math.radians(rot_tol)

    if 1 == 0:
        print("matrices in:")
        for b in matrices:
            print("bone:", b)
            for f in matrices[b]:
                print("  f:", f)
                print("  m:")
                print(matrices[b][f])
        

    
    
    
    cleaned_mats = {}
    for bone in matrices:
        cleaned_mats[bone] = {}
        
        
        last_rot = []
        last_loc = []
        first = True
        for frame in matrices[bone]:
            cleaned_mats[bone][frame] = {}
            cleaned_mats[bone][frame]['animated'] = False
            mat = matrices[bone][frame]['matrix'].copy()
            rot = mat.to_euler()
            loc = mat.to_translation()
            
            if first:
                first = False
                last_rot = rot
                last_loc = loc
                last_frame = frame
                continue

            
            for r in range(3):
                mark = False
                if close_enough(rot[r], last_rot[r], tol=eu_tol) == True:
                    
                    mark = True
                    
                    
                    cleaned_mats[bone][last_frame]['rot'] = True
                    cleaned_mats[bone][frame]['rot'] = True
                    break

            
            
            

            
            if mark:
                last_rot = rot
                
                last_frame = frame
                mark = False

            for l in range(3):
                mark = False
                if close_enough(loc[l], last_loc[l], tol=loc_tol) == True:
                    mark = True
                    
                    
                    cleaned_mats[bone][last_frame]['loc'] = True
                    cleaned_mats[bone][frame]['loc'] = True
                    break

            
            if mark:
                
                last_loc = loc
                last_frame = frame
                mark = False

    
    
    
    
    
    new_matrices = {}
    for bone in cleaned_mats:
        for frame in cleaned_mats[bone]:
            rot = cleaned_mats[bone][frame].get('rot', False)
            loc = cleaned_mats[bone][frame].get('loc', False)
            if rot == False and loc == False:
                continue
            if new_matrices.get(bone) == None:
                new_matrices[bone] = {}
            new_matrices[bone][frame] = {}
            new_matrices[bone][frame]['rot'] = rot
            new_matrices[bone][frame]['loc'] = loc
            new_matrices[bone][frame]['matrix'] = matrices[bone][frame]['matrix']


    if 1 == 0:
        print("matrices out:")
        for bone in new_matrices:
            print("bone:", bone)
            for frame in new_matrices[bone]:
                print("  frame:", frame)
                print("  matrix:")
                print(new_matrices[bone][frame])

        print("len bone frame matrices    :", len(matrices[test_bone]))
        print("len bone frame cleaned_mats:", len(cleaned_mats[test_bone]))
        print("len bone frame new_matrices:", len(new_matrices[test_bone]))

    return new_matrices



def to_deg(mat, limit=8):
    eu = mat.to_euler()
    deg = [math.degrees(round(a, limit)) for a in eu]
    return deg
















def get_deviations(
    armature=None,
    bones=None,
    frame_start=None,
    frame_end=None,
    time_slices=None,
    rotation=0.001,
    location=0.001,
    mark_tol=False,
    mark_tol_rot=0.01,
    mark_tol_loc=0.001,
    ):

    bb = bpy.context.scene.bentobuddy
    bba = bpy.context.scene.bb_anim_props
    anim = bpy.context.scene.bb_anim
    bb_anim = anim

    
    
    drot = rotation
    dloc = location

    
    
    
    
    mrot = mark_tol_rot
    mloc = mark_tol_loc

    print("Deviation factors rot/loc:", drot, "/", dloc)
    print("Armature Proxy:", armature)
    print("Motion rotation tolerance:", mrot)
    print("Motion location tolerance:", mloc)

    
    
    
    

    obj = bpy.data.objects
    armObj = obj[armature]

    matrices = {}

    st = time.time()
    print("composing matrices for deviation checks")

    
    
    
    

    print("Range taken from frame_start and frame_end, this may not be what you want.")
    for frame in range(frame_start, frame_end + 1):
        bpy.context.scene.frame_set(frame)
        
        
        
        
        for boneObj in armObj.pose.bones:
            bone = boneObj.name

            if bone not in matrices:
                matrices[bone] = {}
            matrices[bone][frame] = {}
            rmat = get_real_matrix(armature, bone)
            pmat = armObj.pose.bones[bone].matrix.copy()
            matrices[bone][frame]['rmat'] = rmat 
            matrices[bone][frame]['pmat'] = pmat 
            matrices[bone][frame]['rquat'] = rmat.to_quaternion()
            matrices[bone][frame]['pquat'] = pmat.to_quaternion()  
            matrices[bone][frame]['rot'] = to_deg(rmat)
            matrices[bone][frame]['loc'] = rmat.to_translation()

    et = time.time() - st
    print("time:", et)

    
    
    
    
    
    
    
    st = time.time()
    print("getting animated bones")

    animated = set()

    
    
    
    if mark_tol == True:
        print("  tolerance marking enabled, checking for motion...")
        for bone in matrices:
            
            
            frames = [ f for f in matrices[bone] ]
            f0 = frames[0]
            rot_start = matrices[bone][f0]['rot']
            loc_start = matrices[bone][f0]['loc']
            for frame in range(1, len(frames)):
                rot = matrices[bone][frame]['rot']
                loc = matrices[bone][frame]['loc']
                
                rot_mark = False
                loc_mark = False
                for i in range(3):
                    if close_enough(rot_start[i], rot[i], tol=mrot) == True:
                        rot_mark = True
                        animated.add(bone)
                        break
                    if close_enough(loc_start[i], loc[i], tol=mloc) == True:
                        loc_mark = True
                        animated.add(bone)
                        break
                if rot_mark == True or loc_mark == True:
                    break
        print("Bones that exceeded motion tolerance:", animated)
    else:
        print("  no tolerance marking, adding all bones as animated")
        for bone in matrices:
            animated.add(bone)

    et = time.time() - st
    print("time:", et)

    
    
    
    
    
    
    

    print("composing linear interpolation matrices for deviations")
    st = time.time()

    

    
    
    
    
    
    
    
    
    
    
    
    
    print("Gathering stops")
    
    key_stops = get_key_stops(
        motion=matrices, bones=animated,
        frame_start=frame_start, frame_end=frame_end,
        mark_tol_rot=mrot, mark_tol_loc=mloc)

    

    
    _abs = abs
    _ce = close_enough
    _round = round
    lerp_data = {}
    
    
    print("Gathering rate changes...")
    for bone in animated:
        
        
        lerp_data[bone] = {}
        
        
        rots = get_speed_changes(bone=bone, motion=matrices, transform='rot', frame_start=frame_start, frame_end=frame_end, tol=drot)
        if len(rots) != 0:
            
            rots = set(rots)
            rots = sorted(rots)
            lerp_data[bone]['rots'] = rots



        
        locs=[]

        if len(locs) != 0:
            
            locs = set(locs)
            locs = sorted(locs)
            lerp_data[bone]['locs'] = locs

    et = time.time() - st
    print("time:", et)





    print("Removing unused data...")
    st = time.time()

    
    
    pelvis_bones = {'mpelvis', 'hip', 'hips'}
    if bba.disable_pelvis_location_animation == True:
        for bone in lerp_data:
            bone_lower = bone.lower()
            if bone_lower in pelvis_bones:
                del lerp_data[bone]
    
    if bba.disable_location_offsets == True:
        for bone in lerp_data:
            bone_lower = bone.lower()
            if bone_lower not in pelvis_bones:
                lerp_data[bone].pop('locs', [])

    et = time.time() - st
    print("time:", et)


    print("composing binary data...")
    st = time.time()
    
    bone_data = {}
    for bone in lerp_data:
        
        bone_data[bone] = {}
        if lerp_data[bone].get('rots') != None:
            
            
            frames = lerp_data[bone]['rots']




            for frame in frames:
                
                mat = matrices[bone][frame]['rmat']
                sl_rot = get_sl_rotation(bone=bone, matrix=mat)
                if bone_data[bone].get('rot') == None:
                    bone_data[bone]['rot'] = {}
                
                    bone_data[bone]['rot']['values'] = []
                    bone_data[bone]['rot']['times'] = []
                bone_data[bone]['rot']['values'].append(sl_rot)
                bone_data[bone]['rot']['times'].append(time_slices[frame])

        if lerp_data[bone].get('locs') != None:
            
            frames = lerp_data[bone]['locs']
            for frame in frames:
                
                mat = matrices[bone][frame]['rmat']
                sl_loc = get_sl_location(armature=armature, bone=bone, matrix=mat)
                if bone_data[bone].get('loc') == None:
                    bone_data[bone]['loc'] = {}
                
                    bone_data[bone]['loc']['values'] = []
                    bone_data[bone]['loc']['times'] = []
                bone_data[bone]['loc']['values'].append(sl_loc)
                bone_data[bone]['loc']['times'].append(time_slices[frame])

    et = time.time() - st
    print("time:", et)


    
    
    
    
    
    if 1 == 0:
        key_proxy_rig(armature=armObj.name, matrices=matrices, lerp_data=lerp_data, flatten=False)

    
    

    return bone_data








def get_motion(armature=None, frame_start=0, frame_end=0, frames=[], bones=[]):

    print("animutils::get_motion : frame_start / frame end:", frame_start, "/", frame_end)

    obj = bpy.data.objects
    armObj = obj[armature]
    motion = {}

    
    bb_anim = bpy.context.scene.bb_anim

    if abs(frame_start - frame_end) == 0 and len(frames) == 0:
        print("get_motion reports: no frames to examine, this is an internal error probably, call the doctor!")
        return False

    if len(frames) == 0:
        print("No frames delivered, using range instead")
        frames = list( range(frame_start, frame_end + 1) )
    if len(bones) == 0:
        print("animutils::get_motion : reports - no bones delivered, using armature instead:", armObj.name)
        for boneObj in armObj.data.bones:
            bones.append(boneObj.name)
    for frame in frames:
        bpy.context.scene.frame_set(frame)
        for bone in bones:
            if bone not in motion:
                motion[bone] = {}
            motion[bone][frame] = {}
            rmat = get_real_matrix(armature, bone)
            pmat = armObj.pose.bones[bone].matrix.copy()
            motion[bone][frame]['rmat'] = rmat 
            motion[bone][frame]['pmat'] = pmat 
            motion[bone][frame]['rquat'] = rmat.to_quaternion()
            motion[bone][frame]['pquat'] = pmat.to_quaternion()  
            motion[bone][frame]['rot'] = to_deg(rmat)
            motion[bone][frame]['loc'] = rmat.to_translation()

    return motion








def get_animated_bones(
    armature=None, motion=None,
    mark_tol_rot=0.01,
    mark_tol_loc=0.001,
    ):
    mrot = mark_tol_rot
    mloc = mark_tol_loc

    animated = set()
    
    
    print("motion_data was used as a container but doesn't exist, using (motion) as passed instead")
    
    for bone in motion:
        
        
        frames = [ f for f in motion[bone] ]
        f0 = frames[0]
        rot_start = motion[bone][f0]['rot']
        loc_start = motion[bone][f0]['loc']
        for frame in range(1, len(frames)):
            rot = motion[bone][frame]['rot']
            loc = motion[bone][frame]['loc']
            
            rot_mark = False
            loc_mark = False
            for i in range(3):
                if close_enough(rot_start[i], rot[i], tol=mrot) == True:
                    rot_mark = True
                    animated.add(bone)
                    break
                if close_enough(loc_start[i], loc[i], tol=mloc) == True:
                    loc_mark = True
                    animated.add(bone)
                    break
            if rot_mark == True or loc_mark == True:
                break
    return animated











def get_bone_data(armature=None, lerp_data=None, motion=None, time_slices=None, is_avastar=False):







    

    if is_avastar == True:
        print("-----------------------------------------------------------------------")
        print("animutils::get_bone_data reports : accumulating data for an Avastar rig")
        print("-----------------------------------------------------------------------")
        bone_data = {}
        for bone in lerp_data:
            
            if bone not in avastar_to_sl.bone_map:
                print("Skipping missing bone in map:", bone)
                continue
            real_bone = avastar_to_sl.bone_map[bone]

            
            
            
                
                

            
            bone_data[bone] = {}
            if lerp_data[bone].get('rots') != None:
                
                frames = lerp_data[bone]['rots']
                for frame in frames:
                    
                    mat = motion[bone][frame]['rmat']
                    
                    
                    sl_rot = get_sl_rotation(bone=real_bone, matrix=mat)
                    if bone_data[bone].get('rot') == None:
                        bone_data[bone]['rot'] = {}
                        bone_data[bone]['rot']['values'] = []
                        bone_data[bone]['rot']['times'] = []
                    bone_data[bone]['rot']['values'].append(sl_rot)
                    bone_data[bone]['rot']['times'].append(time_slices[frame])

            if lerp_data[bone].get('locs') != None:
                frames = lerp_data[bone]['locs']
                for frame in frames:
                    
                    mat = motion[bone][frame]['rmat']
                    sl_loc = get_sl_location(armature=armature, bone=bone, matrix=mat)
                    if bone_data[bone].get('loc') == None:
                        bone_data[bone]['loc'] = {}
                        bone_data[bone]['loc']['values'] = []
                        bone_data[bone]['loc']['times'] = []
                    bone_data[bone]['loc']['values'].append(sl_loc)
                    bone_data[bone]['loc']['times'].append(time_slices[frame])


    else:
        bone_data = {}
        for bone in lerp_data:
            
            bone_data[bone] = {}
            if lerp_data[bone].get('rots') != None:
                
                frames = lerp_data[bone]['rots']
                for frame in frames:
                    
                    mat = motion[bone][frame]['rmat']
                    sl_rot = get_sl_rotation(bone=bone, matrix=mat)
                    if bone_data[bone].get('rot') == None:
                        bone_data[bone]['rot'] = {}
                        bone_data[bone]['rot']['values'] = []
                        bone_data[bone]['rot']['times'] = []
                    bone_data[bone]['rot']['values'].append(sl_rot)
                    bone_data[bone]['rot']['times'].append(time_slices[frame])

            if lerp_data[bone].get('locs') != None:
                frames = lerp_data[bone]['locs']
                for frame in frames:
                    
                    mat = motion[bone][frame]['rmat']
                    sl_loc = get_sl_location(armature=armature, bone=bone, matrix=mat)
                    if bone_data[bone].get('loc') == None:
                        bone_data[bone]['loc'] = {}
                        bone_data[bone]['loc']['values'] = []
                        bone_data[bone]['loc']['times'] = []
                    bone_data[bone]['loc']['values'].append(sl_loc)
                    bone_data[bone]['loc']['times'].append(time_slices[frame])

    return bone_data






def calculate_time(
    frame_start=None,
    frame_end=None,
    anim_fps=None,
    ):

    bb = bpy.context.scene.bentobuddy
    bba = bpy.context.scene.bb_anim_props
    anim = bpy.context.scene.bb_anim
    bb_anim = anim 

    time_calc = {}

    
    
    anim_start_frame = frame_start
    anim_end_frame = frame_end

    time_calc['anim_start_frame'] = anim_start_frame
    time_calc['anim_start_frame'] = anim_end_frame

    
    


    total_frames = abs(anim_start_frame - anim_end_frame - 1)

    print("total_frames:", total_frames)


    total_steps = abs(anim_start_frame - anim_end_frame)

    print("total_steps:", total_steps)


    total_time = round(total_steps / anim_fps, 6)

    print("total_time:", total_time)

    time_per_frame = round(total_time / total_steps, 6)

    print("time_per_frame:", time_per_frame)


    time_calc['total_frames'] = total_frames
    time_calc['total_steps'] = total_steps
    time_calc['total_time'] = total_time
    time_calc['time_per_frame'] = time_per_frame

    
    if anim.anim_loop_advanced == True:
        
        
        
        
        
        
        
        
        loop_in_point = round(anim.anim_loop_in_time, 6)
        loop_out_point = round(anim.anim_loop_out_time, 6)
    
    else:
        
        
        loop_in = abs(anim_start_frame - anim.anim_loop_in_frame)
        loop_range = abs(anim.anim_loop_in_frame - anim.anim_loop_out_frame)
        loop_out = loop_in + loop_range
        
        loop_in_point   = round( ( loop_in  * time_per_frame), 6)
        loop_out_point  = round( ( loop_out * time_per_frame), 6)

    time_calc['loop_in_point'] = loop_in_point
    time_calc['loop_out_point'] = loop_out_point

    
    
    
    if 1 == 0:
        if anim.anim_loop == True:
            txt = ""
            if bb_anim.anim_loop_advanced == True:
                print("Advanced loop enabled")
                if loop_in_point < 0:
                    txt = "Loop failure: loop start must be 0 or greater, not less"
                if loop_in_point >= total_time:
                    txt = "Loop failure: loop start must be less than total time"
                if loop_out_point > total_time:
                    txt = "Loop failure: loop end point must be equal or less than animation time"
                if loop_out_point <= 0:
                    txt = "Loop failure: loop end point must be within frame time"
            else:
                if loop_in < anim_start_frame:
                    txt = "Loop failure: in < start"
                if loop_in >= anim_end_frame:
                    txt = "Loop failure: in >= end"
                if loop_out > anim_end_frame:
                    txt = "Loop failure: out > end"
                if loop_out <= anim_start_frame:
                    txt = "Loop failure: out <= start"

            if txt != "":
                print(txt)
                print("The loop failure described above must be corrected or your animation will not loop and may not even play")
                print("There could be other loop issues that will present themselves after you correct the one above")
                popup(txt, "Error", "ERROR")

    
    if 1 == 0:
        print("==============================================")
        print("anim_file_name:", anim.anim_base_name)
        print("base_priority:", anim.anim_base_priority)
        print("anim_start_frame:", anim_start_frame)
        print("anim_end_frame:", anim_end_frame)
        print("anim_fps:", anim_fps)
        print("total_time:", total_time)
        print("total_frames:", total_frames)
        print("total_steps:", total_steps)
        print("loop enabled:", anim.anim_loop)
        print("loop_in_frame:", anim.anim_loop_in_frame)
        print("loop_out_frame:", anim.anim_loop_out_frame)
        print("loop_in_point:", loop_in_point)
        print("loop_out_point:", loop_out_point)
        print("ease_in:", anim.anim_ease_in_duration)
        print("ease_out:", anim.anim_ease_out_duration)
        print("hand_pose", anim.anim_hand_pose)
        print("time_per_frame:", time_per_frame)
        if bba.disable_location_offsets == True:
            print("locations: disabled")
        else:
            print("locations: enabled")
        if bb.export_volume_motion == True:
            print("export_volume_motion: enabled")
        else:
            print("export_volume_motion: disabled")
        print("==============================================")

    return time_calc




def get_real_matrix(armature, bone):
    bone_lower = bone.lower() 

    armObj = bpy.data.objects[armature]
    pbmat = armObj.pose.bones[bone].matrix.copy()
    dbmat = armObj.data.bones[bone].matrix.copy()
    dbmatl = armObj.data.bones[bone].matrix_local.copy()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    if 1 == 0:
        if bone_lower not in pelvis_names:
            pbpmat = armObj.pose.bones[bone].parent.matrix.copy()
            dbpmatl = armObj.data.bones[bone].parent.matrix_local.copy()
        else:
            pbpmat = mathutils.Matrix()
            dbpmatl = mathutils.Matrix()
        if bone_lower not in pelvis_names:
            dbpmat = armObj.data.bones[bone].parent.matrix.copy()
        else:
            dbpmat = mathutils.Matrix()


    
    
    if 1 == 1:
        if armObj.pose.bones[bone].parent:
            pbpmat = armObj.pose.bones[bone].parent.matrix.copy()
            dbpmatl = armObj.data.bones[bone].parent.matrix_local.copy()
        else:
            pbpmat = mathutils.Matrix()
            dbpmatl = mathutils.Matrix()
        if armObj.pose.bones[bone].parent:
            dbpmat = armObj.data.bones[bone].parent.matrix.copy()
        else:
            dbpmat = mathutils.Matrix()

    
    if 1 == 0:
        boneObj = armObj.pose.bones[bone]
        if bone_lower in pelvis_names:
            if boneObj.parent:
                pbpmat = boneObj.matrix @ boneObj.parent.matrix
                dbpmatl = boneObj.bone.matrix_local @ boneObj.bone.parent.matrix_local



    pbmatI = pbmat.inverted()
    pbpmatI = pbpmat.inverted()
    dbpmatlI = dbpmatl.inverted()
    rp = pbpmat @ dbpmatlI @ dbmatl
    rp_composed = rp.inverted() @ pbmat
    m3 = dbmatl.to_3x3()
    m4 = m3.to_4x4()
    m4I = m4.inverted()
    real_mat = m4 @ rp_composed @ m4I

    
    
    
    

    return real_mat






def get_matrix_pair(armature, bone):
    
    bone_lower = bone.lower()

    armObj = bpy.data.objects[armature]
    pbmat = armObj.pose.bones[bone].matrix.copy()
    dbmat = armObj.data.bones[bone].matrix.copy()
    dbmatl = armObj.data.bones[bone].matrix_local.copy()


    
    if 1 == 1:
        if bone_lower not in pelvic_bones:
            pbpmat = armObj.pose.bones[bone].parent.matrix.copy()
            dbpmatl = armObj.data.bones[bone].parent.matrix_local.copy()
        else:
            pbpmat = mathutils.Matrix()
            dbpmatl = mathutils.Matrix()
        if bone_lower not in pelvic_bones:
            dbpmat = armObj.data.bones[bone].parent.matrix.copy()
        else:
            dbpmat = mathutils.Matrix()


    if 1 == 0:
        if armObj.pose.bones[bone].parent:
            pbpmat = armObj.pose.bones[bone].parent.matrix.copy()
            dbpmatl = armObj.data.bones[bone].parent.matrix_local.copy()
        else:
            pbpmat = mathutils.Matrix()
            dbpmatl = mathutils.Matrix()
        if armObj.pose.bones[bone].parent:
            dbpmat = armObj.data.bones[bone].parent.matrix.copy()
        else:
            dbpmat = mathutils.Matrix()


    pbmatI = pbmat.inverted()
    pbpmatI = pbpmat.inverted()
    dbpmatlI = dbpmatl.inverted()
    rp = pbpmat @ dbpmatlI @ dbmatl
    rp_composed = rp.inverted() @ pbmat
    m3 = dbmatl.to_3x3()
    m4 = m3.to_4x4()
    m4I = m4.inverted()
    real_mat = m4 @ rp_composed @ m4I

    return real_mat, pbmat




def close_enough(a, b, tol=0.000001):
    if a > b:
        n = round((a - b), 10)
    elif a < b:
        n = round((b - a), 10)
    elif a == b:
        return False
    if n > tol:
        return True
    return False






def get_sl_rotation(bone=None, matrix=None):

    old = False

    if old == True:
        deg = skel.avatar_skeleton[bone]['rot']
        

    else:
        
        
        
        
        if bone not in avastar_normalized.bone_map:
            
            
            eu = matrix.to_euler()
            deg = [math.degrees(a) for a in eu]
        else:
            bone = avastar_normalized.bone_map[bone]
            deg = skel.avatar_skeleton[bone]['rot']

    rad = [math.radians(a) for a in deg]


    

    
    rot_offset = [-rad[1], -rad[0], -rad[2]]
    euler = mathutils.Euler(rot_offset, 'ZXY')
    mat3 = euler.to_matrix()
    ROTATION = mat3.to_4x4()
    quat = ( Z90I @ matrix @ ROTATION @ Z90 ).to_quaternion().normalized()
    rot_x = round(quat.x, 6)
    rot_y = round(quat.y, 6)
    rot_z = round(quat.z, 6)
    x = F32_to_U16(rot_x, -1, 1)
    y = F32_to_U16(rot_y, -1, 1)
    z = F32_to_U16(rot_z, -1, 1)

    return tuple((x,y,z))



def get_sl_location(armature=None, bone=None, matrix=None):
    obj = bpy.data.objects
    armObj = obj[armature]
    LOCATION = matrix.to_translation()

    arm_scale = armObj.scale

    deg = (0,0,0)

    
    
    
    
    
    
        

    rad = [math.radians(a) for a in deg]

    
    
    
    
    
    rot_offset = [rad[1], rad[0], rad[2]]

    
    
    
    
    if bone in volumes.vol_joints:
            vbs_x, vbs_y, vbs_z = [
            volumes.vol_joints[bone]['scale'][1],
            volumes.vol_joints[bone]['scale'][0],
            volumes.vol_joints[bone]['scale'][2]
            ]
    else:
        vbs_x, vbs_y, vbs_z = mathutils.Vector((0,0,0))

    bs_x, bs_y, bs_z = armObj.pose.bones[bone].scale


    
    
    
    
    
    
    
    if 1 == 1:
    
        
        vbx_x, vbx_y, vbs_z = 0.0,0.0,0.0
        bs_x, bs_y, bs_z = 1.0,1.0,1.0
        
        
        





    if armObj.pose.bones[bone].parent:
        cloc = armObj.data.bones[bone].matrix_local.to_translation()
        ploc = armObj.data.bones[bone].parent.matrix_local.to_translation()
        offset = mathutils.Vector((cloc - ploc))
        LOCATION += offset 

    ROTATION = mathutils.Euler(rot_offset,'ZYX').to_matrix().to_4x4()

    
    scale_composed = list()
    sc = scale_composed
    sc.append( arm_scale[0]/(vbs_x + bs_x) )
    sc.append( arm_scale[1]/(vbs_y + bs_y) )
    sc.append( arm_scale[2]/(vbs_z + bs_z) )
    SCALE = mathutils.Matrix()

    SCALE[0][0] = sc[0]
    SCALE[1][1] = sc[1]
    SCALE[2][2] = sc[2]






    SCALE = mathutils.Matrix()
    
    
    
    
        


    loc = Z90I @ SCALE @ ROTATION @ LOCATION
    loc_x, loc_y, loc_z = loc

    x = F32_to_U16(loc_x/LL_MAX_PELVIS_OFFSET, -1, 1)
    y = F32_to_U16(loc_y/LL_MAX_PELVIS_OFFSET, -1, 1)
    z = F32_to_U16(loc_z/LL_MAX_PELVIS_OFFSET, -1, 1)

    if bone == 'LEFT_HANDLE disabled':
        print("LOCATION:", LOCATION)
        
        pass
    return tuple((x,y,z))



def get_sl_time(total=0, tpf=0, start=0, stop=0):
    
    
    
    

    
    
    

    slices = {}

    frame = start 
    count = stop - start
    for c in range(count+1):
        t = tpf * (c)
        s = F32_to_U16(float(t), 0, total)
        slices[frame] = s
        frame += 1

    return slices 



def F32_to_U16(val, lower, upper):
    val = llclamp(val, lower, upper);
    
    val -= lower;
    val /= (upper - lower);
    
    
    return int(math.floor(val*U16MAX))



def llclamp(a, minval, maxval):
    if a<minval:
        return minval
    if a>maxval:
        return maxval
    return a



def popup(message = "", title = "Message Box", icon =  'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
    return



def remove_deps(armature=None):
    obj = bpy.data.objects
    armObj = obj[armature]
    for pBone in armObj.pose.bones:
        for pbC in pBone.constraints:
            pBone.constraints.remove(pbC)
    try:
        fcurves = armObj.animation_data.drivers
        for fc in fcurves:
            fcurves.remove(fc)
    except:
        print("No drivers, moving on")
    return True





def recycle_actions():
    actions = {a.name for a in bpy.data.actions}
    bb_alib = bpy.context.scene.bb_alib
    if bb_alib.get('actions') == None:
        bb_alib['actions'] = {}
    

    
    
    del_actions = []
    for a in bb_alib['actions'].keys():
        if a not in actions:
            del_actions.append(a)
    
    for a in del_actions:
        del bb_alib['actions'][a]

    
    
    

    
    for a in actions:
        if bb_alib['actions'].get(a) == None:
            bb_alib['actions'][a] = {}
            bb_alib['actions'][a]['flagged'] = False

    return True






def attach_proxy(armature=None, proxy="ANIM_PROXY_RIG"):

    bpy.ops.object.mode_set(mode='OBJECT')
    obj = bpy.data.objects

    sarm = armature
    sarmObj = obj[sarm]

    for o in bpy.context.selected_objects:
        o.select_set(False)

    sarmObj.select_set(True)
    bpy.context.view_layer.objects.active = sarmObj
    bpy.ops.object.duplicate()

    tarmObj = bpy.context.selected_objects[0]
    tarmObj.name = proxy
    tarm = tarmObj.name

    
    
    if tarmObj.animation_data != None:
        if tarmObj.animation_data.action != None:
            tarmObj.animation_data.action = None

    
    
    bpy.context.view_layer.objects.active = tarmObj

    
    
    
    print("Creating animation proxy...")
    bpy.ops.object.mode_set(mode='POSE')
    for boneObj in tarmObj.pose.bones:
        tbone = boneObj.name
        sbone = tbone 
        bpy.data.objects[tarm].data.bones.active = bpy.data.objects[tarm].data.bones[sbone]
        bc = bpy.data.objects[tarm].pose.bones[tbone].constraints
        bc.new('COPY_LOCATION')
        bc['Copy Location'].target = bpy.data.objects[sarm]
        bc['Copy Location'].subtarget = sbone 
        bc['Copy Location'].target_space = 'WORLD'
        bc['Copy Location'].owner_space = 'WORLD'
        bc['Copy Location'].influence = 1
        bc['Copy Location'].name = "BB Copy Loc"
        bc = bpy.data.objects[tarm].pose.bones[tbone].constraints
        bc.new('COPY_ROTATION')
        bc['Copy Rotation'].target = bpy.data.objects[sarm]
        bc['Copy Rotation'].subtarget = sbone
        bc['Copy Rotation'].target_space = 'WORLD'
        bc['Copy Rotation'].owner_space = 'WORLD'
        bc['Copy Rotation'].influence = 1
        bc['Copy Rotation'].name = "BB Copy Rot"
 
    bpy.ops.object.mode_set(mode='OBJECT')

    return tarmObj


















def get_key_stops(motion=None, bones=None, frame_start=0, frame_end=0, mark_tol_rot=0.01, mark_tol_loc=0.0001):

    
    
    
    

    lerp_data = {}

    
    
    
    

    _abs = abs 
    _ce = close_enough
    _round = round

    for bone in bones:
        point_start = frame_start
        point_mid = frame_start
        point_now = frame_start
        rot_start = motion[bone][frame_start]['pquat']
        loc_start = motion[bone][frame_start]['loc']
        rot_now_state = "stopped"
        rot_start_state = "stopped"
        loc_now_state = "stopped"
        loc_start_state = "stopped"

        for frame in range(frame_start, frame_end + 1):
            
            rot_now = motion[bone][frame]['pquat']
            loc_now = motion[bone][frame]['loc']
            
            

            
            
            
            
            
            
            
            
            


            
            
            rot_mark = False
            loc_mark = False

            
            
            
            
            
            
            
            
            
            
            
            

            
            
            for i in range(3):
                rot_start_axis, rot_now_axis = _round(rot_start[i], 4), _round(rot_now[i], 4)

                
                if _ce(rot_start_axis, rot_now_axis, tol=mark_tol_rot) == True:
                    rot_mark = True



                    if rot_now_axis > rot_start_axis:
                        rot_now_state = "ascending"
                    elif rot_now_axis < rot_start_axis:
                        rot_now_state = "descending"
                    
                    else:
                        print("rot tolerance triggers non motion in a motion sequence")
                    break
                
                
                else:
                    
                    rot_now_state = "stopped"

            
            
            
            for i in range(3):
                loc_start_axis, loc_now_axis = _round(loc_start[i], 4), _round(loc_now[i], 4)
                if _ce(loc_start_axis, loc_now_axis, tol=mark_tol_loc) == True:
                    loc_mark = True
                    if loc_now_axis > loc_start_axis:
                        loc_now_state = "ascending"
                    elif loc_now_axis < loc_start_axis:
                        loc_now_state = "descending"
                    
                    else:
                        print("loc tolerance triggers non motion in a motion sequence")
                    break
                else:
                    loc_now_state = "stopped"

            if rot_now_state != rot_start_state:
                rot_start_state = rot_now_state
                if bone not in lerp_data:
                    lerp_data[bone] = {}
                if 'rots' not in lerp_data[bone]:
                    lerp_data[bone]['rots'] = []
                    
                    lerp_data[bone]['rots'].append(frame_start)

                lerp_data[bone]['rots'].append(frame-1)
            
            
            if loc_now_state != loc_start_state:
                loc_start_state = loc_now_state
                if bone not in lerp_data:
                    lerp_data[bone] = {}
                if 'locs' not in lerp_data[bone]:
                    lerp_data[bone]['locs'] = []
                    
                    lerp_data[bone]['locs'].append(frame_start)
                lerp_data[bone]['locs'].append(frame-1)

            
            if frame == frame_end:
                
                
                
                
                if bone in lerp_data:
                    if 'rots' not in lerp_data[bone] and 'locs' not in lerp_data[bone]:
                        lerp_data[bone]['rots'] = [frame]
                    else:
                        if 'rots' in lerp_data[bone]:
                            lerp_data[bone]['rots'].append(frame)
                        if 'locs' in lerp_data[bone]:
                            lerp_data[bone]['locs'].append(frame)



            
            
            
            
            
            
            



            
            
            
            
            rot_start = rot_now[:]
            loc_start = loc_now[:]

    if len(lerp_data) == 0:
        return []

    return lerp_data

















def clean_frames(
    bone=None,
    motion=None,
    frames=None,
    transform=None,
    tol=0.001,
    ):
    
    frames_set = set(frames)
    
    frames_list = sorted(frames_set)

    
    start = frames_list[0]
    end = frames_list[-1]

    
    
    
    
    
    
    frames_cleaned = []
    tr_animated = []

    tr_start = motion[bone][start][transform]

    
    _ce = close_enough

    
    
    
    
    
    

    
    
    
    
    
    

    
    hit_now = False
    hits = {}
    hits[1] = False
    hits[2] = False
    hits[3] = False

    
    
    
    
    
    
    frame_entry = 0
    for frame in frames_list:
        frame_entry += 1
        tr_now = motion[bone][frame][transform]
        
        
        
        
        
        
        
        
        for i in range(3):
            if _ce(tr_start[i], tr_now[i], tol=tol) == True:
                tr_animated.append(frame)
                tr_start = tr_now[:]
                hit_now = True
                
                
                
                break

        
        
        
        
        
        

            
            hit_now = False

        
        hits[1] = hits[2]
        hits[2] = hits[3]
        hits[3] = hit_now

        
        if frame_entry > 2:
            if hit_now == True:
                
                if hits[1] == False and hits[2] == False:
                    tr_animated.append(frame-1)

        

    if len(tr_animated) > 0:
        frames_cleaned = [start]
        frames_cleaned.extend( sorted(tr_animated) )
        frames_cleaned.append(end)

    return frames_cleaned





def get_speed_changes(
    bone=None,
    motion=None,
    frame_start=0,
    frame_end=0,
    transform=None,
    tol=0.001,
    ):

    bb = bpy.context.scene.bentobuddy
    bba = bpy.context.scene.bb_anim_props
    anim = bpy.context.scene.bb_anim
    bb_anim = anim 

    
    
    anim_fps = bb.animation_fps
    anim_start_frame = frame_start
    anim_end_frame = frame_end
    total_frames = abs(anim_start_frame - anim_end_frame - 1)
    total_steps = abs(anim_start_frame - anim_end_frame)
    total_time = round(total_steps / anim_fps, 6)
    time_per_frame = round(total_time / total_steps, 6)
    tpf = time_per_frame
    

    if abs(frame_start - frame_end) == 0:
        print("get_speed_changes reports: no frames to process")
        return False

    lerp_data = {}

    _abs = abs 

    
    
    has_keys = False

    def _rnd(a):
        b = [round(c, 4) for c in a]
        return b
    def _deg(a):
        str_type = str(type(a))
        if 'Quaternion' in str_type:
            eu = a.to_euler()
            d = [round(math.degrees(e), 4) for e in eu]
        elif 'Euler' in str_type:
            d = [round(math.degrees(e), 4) for e in a]
        elif 'float' in str_type:
            d = round(math.degrees(a), 4)
        else:
            print("Type not supported:", type(a))
            return
        return d

    
    
    
    
    
    
    
    
    
    if transform == 'loc':
        key_set = []
        loc_start = motion[bone][frame_start]['loc']
        speed_start = 0

        for frame in range(frame_start, frame_end + 1):
            loc_now = motion[bone][frame]['loc']
            speed_now = (loc_start - loc_now).length
            speed_dif = abs(speed_start - speed_now)

            if speed_dif < tol:
                
                
                continue
            else:
                
                speed_start = speed_dif
                loc_start = loc_now.copy()
                
                
                
                key_set.append(frame)
                has_keys = True
                continue
            

        return []

    else:

        
        
        
        
        
        
        
        
        

        
        key_set = []

        
        
        rot_start = motion[bone][frame_start]['rquat']

        
        
        
        speed_start = mathutils.Quaternion().angle 

        for frame in range(frame_start, frame_end + 1):
            rot_now = motion[bone][frame]['rquat']
            speed_now = rot_now.rotation_difference(rot_start).angle

            speed_dif = _abs(speed_start - speed_now)

            
            
            

            
            
            
            
            
            
            
            
            

            if speed_dif < tol:
                speed_start = speed_dif
                
                continue
            else:
                
                speed_start = speed_dif
                rot_start = rot_now.copy()
                
                
                
                key_set.append(frame-1)
                has_keys = True
                continue
            

    
    
    

    
    if has_keys == False:
        return []

    key_set.append(frame_end)
    keys_finished = [frame_start]
    keys_finished.extend(key_set)
    return keys_finished





def get_rate_changes(
    bone=None,
    matrices=None,
    frame_start=0,
    frame_end=0,
    transform=None,
    tol=0.001,
    ):

    
    
    
    
    
    
    
    
    

    lerp_data = {}

    _abs = abs 


    
    
    has_keys = False

    def _rnd(a):
        b = [round(c, 4) for c in a]
        return b



    
    
    
    
    
    key_set = []

    
    
    trs_start = matrices[bone][frame_start][transform] 

    
    
    
    speed_start = {}
    for i in range(3):
        speed_start[i] = 0.0

    for frame in range(frame_start, frame_end + 1):
        trs_now = matrices[bone][frame][transform]

        
        
        
        speed_now = []
        for i in range(3):
            speed_now.append( _abs(trs_start[i] - trs_now[i]) )

        for i in range(3):




            speed_now = _abs(trs_start[i] - trs_now[i])

            
            
            
            
            
            
            
            
            
            
            
            
            
            
            if speed_now != speed_start[i]:
                if speed_now < tol:
                    
                    continue
                
                speed_start[i] = speed_now
                trs_start = trs_now[:]

                
                
                key_set.append(frame-1)
                has_keys = True
                break
            




    
    if has_keys == False:
        return []

    key_set.append(frame_end)

    return key_set








def convert_animated_controllers(source=None, target=None):

    obj = bpy.data.objects
    avaRig = obj[source]
    bbRig = obj[target]

    if avaRig.animation_data == None:
        print("convert_animated_controllers reports: no animation_data")
        return False
    if avaRig.animation_data.action == None:
        print("convert_animated_controllers reports: no action")
        return False

    for o in bpy.context.selected_objects:
        o.select_set(False)

    avaRig.select_set(True)

    
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action = 'DESELECT')
    for boneObj in avaRig.data.bones:
        
        bone = boneObj.name
        if bone in mod_data.all_pbones:
            continue
        boneObj.select = True
        avaRig.data.bones.active = boneObj
        bpy.ops.anim.keyframe_clear_v3d()
        boneObj.select = False

    bpy.ops.object.mode_set(mode='EDIT')
    
    for boneObj in avaRig.data.edit_bones:
        bone = boneObj.name
        if bone not in mod_data.all_pbones:
            avaRig.data.edit_bones.remove(boneObj)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    for bone in mod_data.pbones_map:
        if bone not in avaRig.data.bones:
            continue
        avaRig.data.bones[bone].name = mod_data.pbones_map[bone]
    bpy.context.view_layer.update()

    
    animObj = avaRig.animation_data.action.copy()
    bbRig.animation_data_create()
    bbRig.animation_data.action = animObj

    return animObj 



















def morph_to(source=None, target=None, morph=False):

    
    if morph == False:
        shifter.morpher_reset(arms=[source])
        return True

    bb = bpy.context.scene.bentobuddy
    obj = bpy.data.objects
    sourceObj = obj[source]
    targetObj = obj[target]

    frame_start = bb.animation_start_frame
    frame_end = bb.animation_end_frame
    frame_current = bpy.context.scene.frame_current



    print("would have morphed", source)
    return True


    
    
    
    
    if sourceObj.animation_data == None:
        sourceObj.animation_data_create()
    if sourceObj.animation_data.action == None:
        actionObj = bpy.data.actions.new("MORPH_TO")
    
    
    shifter.move_keys(arm=source, start=start, range=2, marker=True)


    
    
    

    return True






def get_keyframes(arm, report=False):
    armObj = arm
    if isinstance(arm, str):
        armObj = bpy.data.objects[arm]
    if armObj.animation_data == None:
        if report == True:
            print("animutils::get_keyframes reports no animation data")
        return False
    if armObj.animation_data.action == None:
        if report == True:
            print("animutils::get_keyframes reports no action")
        return False

    animObj = armObj.animation_data.action
    fcurves = animObj.fcurves
    frames = set()
    for fc in fcurves:
        for kfp in fc.keyframe_points:
            frames.add(int(kfp.co.x))
    frames_sorted = list(sorted(frames))

    return frames_sorted











def transfer_motion(sarm=None, tarm=None):
    
    frame_current = bpy.context.scene.frame_current

    obj = bpy.data.objects
    sarmObj = sarm
    tarmObj = tarm
    if isinstance(sarm, str):
        sarmObj = obj[sarm]
    if isinstance(tarm, str):
        tarmObj = obj[tarm]

    state = utils.get_state()

    
    
    
    
    
    
    
    tarmObj.select_set(True)
    utils.activate(tarmObj)
    cnames = []
    for boneObj in tarmObj.pose.bones:
        bone = boneObj.name
        tarmObj.data.bones.active = boneObj.bone 
        
        bc = boneObj.constraints
        conObj = bc.new('COPY_LOCATION')
        cname = conObj.name
        conObj.target = sarmObj
        conObj.subtarget = bone
        conObj.target_space = 'WORLD'
        conObj.owner_space = 'WORLD'
        conObj.influence = 1
        conObj.name = "BB " + cname
        cnames.append(conObj.name)
        
        bc = boneObj.constraints
        conObj = bc.new('COPY_ROTATION')
        cname = conObj.name
        conObj.target = sarmObj
        conObj.subtarget = bone
        conObj.target_space = 'WORLD'
        conObj.owner_space = 'WORLD'
        conObj.influence = 1
        conObj.name = "BB " + cname
        cnames.append(conObj.name)

        boneObj['cname'] = cnames

    
    
    tarmObj.animation_data_clear()

    
    animObj = tarmObj.animation_data_create()

    
    action = "BB_action_transfer"
    actionObj = bpy.data.actions.new(action)

    
    tarmObj.animation_data.action = actionObj

    

    
    
    
    groups = {}
    for boneObj in tarmObj.pose.bones:
        bone = boneObj.name
        g = actionObj.groups.new(bone)
        groups[bone] = g

    
    frames = get_keyframes(sarmObj)

    
    matrices = {}
    for frame in frames:
        bpy.context.scene.frame_set(frame)
        for boneObj in tarmObj.pose.bones:
            bone = boneObj.name
            if bone not in matrices:
                matrices[bone] = {}
            if frame not in matrices[bone]:
                matrices[bone][frame] = {}
            mat = get_matrix_basis(armature=tarmObj.name, bone=boneObj.name)
            matrices[bone][frame] = mat

    
    fcurve_paths = {}
    for boneObj in tarmObj.pose.bones:
        path_key = 'pose.bones["' + boneObj.name + '"]'
        fcurve_paths[path_key] = boneObj.name

    
    transform_types = [".rotation_euler", ".location", ".scale"]
    for bone_path in fcurve_paths:
        bone = fcurve_paths[bone_path]
        
        dp = bone_path + ".rotation_quaternion"
        fc = actionObj.fcurves.new(data_path=dp, index=0)
        fc.group = groups[bone]
        fc = actionObj.fcurves.new(data_path=dp, index=1)
        fc.group = groups[bone]
        fc = actionObj.fcurves.new(data_path=dp, index=2)
        fc.group = groups[bone]
        fc = actionObj.fcurves.new(data_path=dp, index=3)
        fc.group = groups[bone]
        for transform in transform_types:
            dp = bone_path + transform
            fc = actionObj.fcurves.new(data_path=dp, index=0)
            fc.group = groups[bone]
            fc = actionObj.fcurves.new(data_path=dp, index=1)
            fc.group = groups[bone]
            fc = actionObj.fcurves.new(data_path=dp, index=2)
            fc.group = groups[bone]

    
    

    
    tfcurves = actionObj.fcurves
    for fc in tfcurves:
        dp, idx = fc.data_path, fc.array_index
        bone_path, delimiter, transform = dp.rpartition('.')
        
        bone = fcurve_paths[bone_path]
        if bone not in tarmObj.data.bones:
            
            
            continue

        
        
        fc.keyframe_points.add(count=len(frames))

        
        
        
        
        
        samples = []
        for frame in matrices[bone]:
            if transform == 'rotation_quaternion':
                samples.append(matrices[bone][frame].to_quaternion()[idx])
            elif transform == 'rotation_euler':
                samples.append(matrices[bone][frame].to_euler()[idx])
            elif transform == 'location':
                samples.append(matrices[bone][frame].to_translation()[idx])
            elif transform == 'scale':
                
                samples.append(1)

        
        kfp_data = []
        for i in range(len(frames)):
            kfp_data.append(frames[i])
            kfp_data.append(samples[i])

        fc.keyframe_points.foreach_set("co", kfp_data)
        fc.update()

    bpy.context.scene.frame_set(frame_current)

    
    
    matrices = {}
    for boneObj in tarmObj.pose.bones:
        bone = boneObj.name
        matrices[bone] = {}
        matrices[bone]['matrix'] = boneObj.matrix.copy()
        matrices[bone]['tail'] = boneObj.bone.tail_local.copy()

    for boneObj in tarmObj.pose.bones:
        for cname in boneObj['cname']:
            if cname in boneObj.constraints:
                conObj = boneObj.constraints[cname]
                boneObj.constraints.remove(conObj)
        boneObj.pop('cname', "")

    utils.set_state(state)

    return True









def bake_motion(sarm=None, tarm=None, frame_start=0, frame_end=0):

    bb = bpy.context.scene.bentobuddy

    if sarm == None or tarm == None:
        print("bake_motion - nothing to do")
        return False

    if abs(frame_start - frame_end) == 0:
        print("No frames to record, using animation range instead")
        
        
        
        
        frame_start = int(bpy.context.scene.frame_start)
        frame_end = int(bpy.context.scene.frame_end)
        
        
        

    
    frame_current = bpy.context.scene.frame_current

    obj = bpy.data.objects
    sarmObj = sarm
    tarmObj = tarm
    if isinstance(sarm, str):
        sarmObj = obj[sarm]
    if isinstance(tarm, str):
        tarmObj = obj[tarm]

    
    
    state = utils.get_state()
    tarmObj.select_set(True)
    utils.activate(tarmObj)
    bpy.ops.object.mode_set(mode='EDIT')
    for boneObj in tarmObj.data.edit_bones:
        boneObj.use_connect = False
    bpy.ops.object.mode_set(mode='OBJECT')
    utils.set_state(state)

    
    
    tarmObj.animation_data_clear()

    
    animObj = tarmObj.animation_data_create()

    
    action = "BB_Baked"
    actionObj = bpy.data.actions.new(action)
    print("Created new action:", actionObj.name)

    
    tarmObj.animation_data.action = actionObj

    

    
    
    

    groups = {}
    for boneObj in tarmObj.pose.bones:
        bone = boneObj.name
        g = actionObj.groups.new(bone)
        groups[bone] = g

    
    matrices = {}
    for frame in range(frame_start, frame_end + 1):
        bpy.context.scene.frame_set(frame)
        for boneObj in sarmObj.pose.bones:
            bone = boneObj.name
            if bone not in matrices:
                matrices[bone] = {}
            if frame not in matrices[bone]:
                matrices[bone][frame] = {}
            mat = get_matrix_basis(armature=sarmObj.name, bone=boneObj.name)
            matrices[bone][frame] = mat

    
    fcurve_paths = {}
    for boneObj in tarmObj.pose.bones:
        bone = boneObj.name
        
        if bone not in tarmObj.pose.bones:
            continue
        path_key = 'pose.bones["' + boneObj.name + '"]'
        fcurve_paths[path_key] = boneObj.name

    
    transform_types = [".rotation_euler", ".location", ".scale"]
    for bone_path in fcurve_paths:
        bone = fcurve_paths[bone_path]
        
        dp = bone_path + ".rotation_quaternion"
        fc = actionObj.fcurves.new(data_path=dp, index=0)
        fc.group = groups[bone]
        fc = actionObj.fcurves.new(data_path=dp, index=1)
        fc.group = groups[bone]
        fc = actionObj.fcurves.new(data_path=dp, index=2)
        fc.group = groups[bone]
        fc = actionObj.fcurves.new(data_path=dp, index=3)
        fc.group = groups[bone]
        for transform in transform_types:
            dp = bone_path + transform
            fc = actionObj.fcurves.new(data_path=dp, index=0)
            fc.group = groups[bone]
            fc = actionObj.fcurves.new(data_path=dp, index=1)
            fc.group = groups[bone]
            fc = actionObj.fcurves.new(data_path=dp, index=2)
            fc.group = groups[bone]

    
    

    
    tfcurves = actionObj.fcurves
    for fc in tfcurves:
        dp, idx = fc.data_path, fc.array_index
        bone_path, delimiter, transform = dp.rpartition('.')
        
        bone = fcurve_paths[bone_path]
        if bone not in tarmObj.data.bones:
            
            
            continue
        
        
        
        if bone not in matrices:
            continue

        
        frames = list(range(frame_start, frame_end +1))
        fc.keyframe_points.add(count=len(frames))

        
        samples = []
        for frame in matrices[bone]:
            if transform == 'rotation_quaternion':
                samples.append(matrices[bone][frame].to_quaternion()[idx])
            elif transform == 'rotation_euler':
                samples.append(matrices[bone][frame].to_euler()[idx])
            elif transform == 'location':
                samples.append(matrices[bone][frame].to_translation()[idx])
            elif transform == 'scale':
                samples.append(matrices[bone][frame].to_scale()[idx])

        
        kfp_data = []
        for i in range(len(frames)):
            kfp_data.append(frames[i])
            kfp_data.append(samples[i])

        fc.keyframe_points.foreach_set("co", kfp_data)
        fc.update()

    bpy.context.scene.frame_set(frame_current)

    return True





def get_matrix_basis(armature=None, bone=None):
        if isinstance(armature, str) == False:
            armature = armature.name
        if isinstance(bone, str) == False:
            bone = bone.name

        armObj = bpy.data.objects[armature]
        pbmat = armObj.pose.bones[bone].matrix.copy()
        dbmat = armObj.data.bones[bone].matrix.copy()
        dbmatl = armObj.data.bones[bone].matrix_local.copy()
        if armObj.pose.bones[bone].parent:
            pbpmat = armObj.pose.bones[bone].parent.matrix.copy()
            dbpmatl = armObj.data.bones[bone].parent.matrix_local.copy()
        else:
            pbpmat = mathutils.Matrix()
            dbpmatl = mathutils.Matrix()
        if armObj.pose.bones[bone].parent:
            dbpmat = armObj.data.bones[bone].parent.matrix.copy()
        else:
            dbpmat = mathutils.Matrix()
        pbmatI = pbmat.inverted()
        pbpmatI = pbpmat.inverted()
        dbpmatlI = dbpmatl.inverted()
        rp = pbpmat @ dbpmatlI @ dbmatl
        rp_composed = rp.inverted() @ pbmat

        return rp_composed








def get_frame_range(armature, start=True, end=False):
    armObj = armature
    frame_start = 1
    frame_end = 1
    if isinstance(armature, str):
        armObj = bpy.data.objects[armature]
    if armObj.animation_data != None:
        if armObj.animation_data.action != None:
            frame_start, frame_end = armObj.animation_data.action.frame_range
    else:
        frame_start = bpy.context.scene.frame_start
        frame_end = bpy.context.scene.frame_end

    if start == True:
        bpy.context.scene.frame_set(frame_start)
    if end == True:
        bpy.context.scene.frame_set(frame_end)

    return int(frame_start), int(frame_end)




def apply_transforms(arm, report=False):

    
    
    
    
    tarmObj = bpy.context.selected_objects[0]

    state = utils.get_state()

    tarmObj.select_set(True)
    utils.activate(tarmObj)
    bpy.ops.object.duplicate()
    sarmObj = bpy.context.object

    frame_current = bpy.context.scene.frame_current
    
    
    start_frame, end_frame = get_frame_range(sarmObj, start=True)

    
    
    
    
    

    
    sarmObj.select_set(False)
    tarmObj.select_set(True)
    utils.activate(tarmObj)
    tarmObj.animation_data_clear()
    
    rigutils.rebind(tarmObj, report=True)
    bpy.ops.object.transform_apply(
        location=True,
        rotation=True,
        scale=True)

    for o in bpy.context.selected_objects:
        o.select_set(False)
    mesh = rigutils.get_associated_mesh(tarmObj)
    if mesh != False:
        for o in mesh:
            o.select_set(True)
        utils.activate(o)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    for o in bpy.context.selected_objects:
        o.select_set(False)

    result = transfer_motion(sarm=sarmObj, tarm=tarmObj)

    for o in bpy.context.selected_objects:
        o.select_set(False)

    if result == False:
        print("The call to transfer motion seems to have failed")
        popup("Motion transfer failed", "Error", "ERROR")
        sarmObj.select_set(True)
        utils.activate(sarmObj)
        bpy.ops.object.delete()
        utils.set_state(state)
        return {'FINISHED'}

    sarmObj.select_set(True)
    utils.activate(sarmObj)

    bpy.ops.object.delete()

    tarmObj.select_set(True)
    utils.activate(tarmObj)

    utils.set_state(state)

    bpy.context.scene.frame_set(frame_current)

    return True












def merge_actions(actions=None, armature=None):
    armObj = armature
    if isinstance(armature, str):
        armObj = bpy.data.objects[armature]

    
    action = "BB_Merged"
    animObj = bpy.data.actions.new(action)
    print("Created new action:", animObj.name)

    
    fcurve_paths = {}
    for boneObj in armObj.pose.bones:
        bone = boneObj.name
        path_key = 'pose.bones["' + bone + '"]'
        fcurve_paths[path_key] = bone



    if 1 == 0:
        print("----------------------------------")
        print(" WARNING WARNING WARNING WARNING")
        print(" Look below this warning and change")
        print(" the code to enable mutliple action")
        print(" merge.")
        print("----------------------------------")
        a = actions[0]
        actions = [a]

    
    



    
    actionable = []
    for action in actions:
        print("storing action:", action)
        if action in bpy.data.actions:
            actionable.append(action)

    
    
    
    groups = {}
    for action in actionable:
        srcAnim = bpy.data.actions[action]
        for fc in srcAnim.fcurves:
            bone_path, delimiter, transform = fc.data_path.rpartition('.')
            if bone_path in fcurve_paths:
                bone = fcurve_paths[bone_path]
                if bone in groups:
                    continue
                g = animObj.groups.new(bone)
                groups[bone] = g

    
    
    

    kfp_data = {}
    for action in actionable:
        print("iterating action:", action)
        srcAnim = bpy.data.actions[action]
        for fc in srcAnim.fcurves:

            
            
            
            
            bone_path, delimiter, transform = fc.data_path.rpartition('.')

            
            if 1 == 1: 
                
                array_index = fc.array_index









                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                

                if fc.data_path not in kfp_data:
                    
                    kfp_data[fc.data_path] = {}
                if fc.array_index not in kfp_data[fc.data_path]:
                    kfp_data[fc.data_path][fc.array_index] = {}
                    kfp_data[fc.data_path][fc.array_index]['easing'] = []
                    kfp_data[fc.data_path][fc.array_index]['back'] = []
                    kfp_data[fc.data_path][fc.array_index]['handle_left'] = []
                    kfp_data[fc.data_path][fc.array_index]['handle_left_type'] = []
                    kfp_data[fc.data_path][fc.array_index]['handle_right'] = []
                    kfp_data[fc.data_path][fc.array_index]['handle_right_type'] = []
                    kfp_data[fc.data_path][fc.array_index]['interpolation'] = []
                    kfp_data[fc.data_path][fc.array_index]['period'] = []
                    
                    kfp_data[fc.data_path][fc.array_index]['co'] = []
                    kfp_data[fc.data_path][fc.array_index]['co.x'] = []
                    kfp_data[fc.data_path][fc.array_index]['co.y'] = []
                for kfp in fc.keyframe_points:
                    kfp_data[fc.data_path][fc.array_index]['easing'].append(kfp.easing)
                    kfp_data[fc.data_path][fc.array_index]['back'].append(kfp.back)
                    kfp_data[fc.data_path][fc.array_index]['handle_left'].append(kfp.handle_left.copy())
                    kfp_data[fc.data_path][fc.array_index]['handle_left_type'].append(kfp.handle_left_type)
                    kfp_data[fc.data_path][fc.array_index]['handle_right'].append(kfp.handle_right.copy())
                    kfp_data[fc.data_path][fc.array_index]['handle_right_type'].append(kfp.handle_right_type)
                    kfp_data[fc.data_path][fc.array_index]['interpolation'].append(kfp.interpolation)
                    kfp_data[fc.data_path][fc.array_index]['period'].append(kfp.period)
                    
                    kfp_data[fc.data_path][fc.array_index]['co'].extend(list(kfp.co.copy()))
                    kfp_data[fc.data_path][fc.array_index]['co.x'].append(kfp.co.x)
                    kfp_data[fc.data_path][fc.array_index]['co.y'].append(kfp.co.y)

    print("done iterating actions")



    if 1 == 0:
        for dp in kfp_data:
            if "mShoulderRight" in dp:
                print(" ", dp)
                for index in kfp_data[dp]:
                    print("  -kfp.co  :", kfp_data[dp][index]['co'])
                    print("  -kfp.co.x:", kfp_data[dp][index]['co.x'])
                    print("  -kfp.co.y:", kfp_data[dp][index]['co.y'])






    
    
    print("creating new fcurves")
    for action in actionable:

        srcAnim = bpy.data.actions[action]

        
        
        



        
        
        for fc in srcAnim.fcurves:
            

            bone_path, delimiter, transform = fc.data_path.rpartition('.')
            bone = fcurve_paths[bone_path]
            
            if fc.data_path in kfp_data:
                dp = bone_path + "." + transform
                fc = animObj.fcurves.new(data_path=dp, index=fc.array_index)
                fc.group = groups[bone]

    print("done creating new fcurves")

    print("applying data...")
    print(" - foreach_set (skipped) ...")
    
    
    print("   adding keyframes only...")
    for fc in animObj.fcurves:
        
        
        count = len(kfp_data[fc.data_path][fc.array_index]['co.x'])
        fc.keyframe_points.add(count=count)
        
        
            
            
            
            
            

    

    print(" - foreach_set finished!")

    print(" - additional data, contains x and y now...")
    
    for fc in animObj.fcurves:
        
        if fc.data_path in kfp_data:
            index = 0
            for kfp in fc.keyframe_points:

                kfp.co.x = kfp_data[fc.data_path][fc.array_index]['co.x'][index]
                kfp.co.y = kfp_data[fc.data_path][fc.array_index]['co.y'][index]

                kfp.easing = kfp_data[fc.data_path][fc.array_index]['easing'][index]
                kfp.back = kfp_data[fc.data_path][fc.array_index]['back'][index]
                kfp.handle_left = kfp_data[fc.data_path][fc.array_index]['handle_left'][index]
                kfp.handle_left_type = kfp_data[fc.data_path][fc.array_index]['handle_left_type'][index]
                kfp.handle_right = kfp_data[fc.data_path][fc.array_index]['handle_right'][index]
                kfp.handle_right_type = kfp_data[fc.data_path][fc.array_index]['handle_right_type'][index]
                kfp.interpolation = kfp_data[fc.data_path][fc.array_index]['interpolation'][index]
                kfp.period = kfp_data[fc.data_path][fc.array_index]['period'][index]

                
                

                



                if 1 == 0:
                    if "mShoulderLeft" in fc.data_path:
                        print("dp:", fc.data_path)
                        print(" -real x/y:", kfp.co.x, "/", kfp.co.y)
                        print(" -save x/y:", kfp_data[fc.data_path][fc.array_index]['co.x'][index], "/", kfp_data[fc.data_path][fc.array_index]['co.y'][index])

                index += 1
    print(" - additional data done!")

    if 1 == 0:
        print(" -saved ALL:", kfp_data[fc.data_path])
        print("len fcuves:", len(animObj.fcurves))
        print("len data  :", len(kfp_data))



    return animObj

    print("kfp_data:", kfp_data)
    actionable.append(animObj.name)
    for action in actionable:
        srcAction = bpy.data.actions[action]
        for fc in srcAction.fcurves:
            if "mHipLeft" in fc.data_path:
                for kfp in fc.keyframe_points:
                    print("action / path / kfp.co:", action, "/", fc.data_path, "/", kfp.co)




    return animObj






def split_time(frame_start=0, frame_end=0, fill_fps=24, fill_time=60):

    
    frame_start = int(frame_start)
    frame_end = int(frame_end)

    
    frame_range = frame_start + frame_end - 1
    
    total_time = (frame_range / fill_fps)

    print("- Split Time Stats -")
    print("frame_range:", frame_range)
    print("fill_time:", fill_time)
    print("total_time:", total_time)

    
    if total_time <= fill_time:
        print("The custom fill time accommodates the entire animation, splitting is not required.")
        print("In order to split your animation reduce your custom time to below", round(total_time, 2))
        popup("Warning: split not required, see console", "Error", "ERROR")
        return False

    
    
    base_float = total_time / fill_time
    base_int = int(base_float)
    if base_int == base_float:
        clones = base_int
    else:
        clones = base_int + 1

    print("clones:", clones)
    print("base_float:", base_float)
    print("base_int:", base_int)

    
    
    
    
    tpf = 1 / fill_fps
    frames = 0
    while (tpf * frames) < fill_time:
        frames += 1
    print("frames per full segment:", frames)

    
    
    
    
    
    if 1 == 0:
        actions = {}
        for count in range(clones):
            print("count:", count)
            newAction = actionObj.copy()
            newAction.use_fake_user = True
            name = newAction.name
            
            actions[name] = "" 
            bb_alib['actions'][name] = {}
            bb_alib['actions'][name]['flagged'] = True

    actions = {}
    for count in range(clones):
        print("count:", count)
        actions[count] = {}


    


    


    

    


    
    if 1 == 0:
        count = 1
        frame_now = frame_start
        for action in actions:
            actionObj = bpy.data.actions[action]
            actionObj['frame_start'] = frame_now
            
            if count == clones:
                actionObj['frame_end'] = frame_end
            else:
                actionObj['frame_end'] = frame_now + frames
            
            frame_now = (frame_now + frames + 1)
            actionObj['frame_range'] =  True 
            print("next pass for frame_now:", frame_now)
            count += 1

    
    
    count = 1
    frame_now = frame_start
    for action in actions:
        actions[action]['frame_start'] = frame_now
        
        if count == clones:
            actions[action]['frame_end'] = frame_end
        else:
            actions[action]['frame_end'] = frame_now + frames
        
        frame_now = (frame_now + frames + 1)
        print("next pass for frame_now:", frame_now)
        count += 1

    return actions













def write_lsl(source=None, target=None, actions=None, prefix="Anim", fps=24):
    bb_split = bpy.context.window_manager.bb_split

    split_overlap = bb_split.split_overlap
    split_delay = bb_split.split_delay

    
    n = 0
    anim_list = []
    for a in actions:
        
        n += 1
        ns = str(n)
        zf = ns.zfill(3)
        anim_name = prefix + "_" + zf 
        anim_list.append(anim_name)

    time_list = []
    
    
    
    action_list = [a for a in actions]
    for action in actions:
        frame_start = actions[action]['frame_start']
        frame_end = actions[action]['frame_end']
        frame_fps = fps
        total_time = abs(frame_start - frame_end) / frame_fps

        
        
        final_time = round(total_time, 2) + split_delay - split_overlap
        if final_time < 0:
            print("final_time is less than 0, skipping calculation [action/time]:", action, "/", final_time)
            
            
            
            
            if action == action_list[-1]:
                print("Last action has a zero issue, dividing the original by 2 to get a sane result")
                new_time = total_time / 2
            else:
                new_time = total_time
            total_time_text = str(round(new_time, 2))
        else:
            total_time_text = str(final_time)
        time_list.append(total_time_text)

    
    
    anim_string = ""
    last = ", "
    count = 0
    for anim in anim_list:
        count += 1
        if count == len(anim_list):
            last = ""
        anim_string += '"' + anim + '"' + last
    time_string = ""
    last = ", "
    count = 0
    for time in time_list:
        count += 1
        if count == len(time_list):
            last = ""
        time_string += '"' + time + '"' + last

    
    print("anim_string:", anim_string)
    print("time_list:", time_string)

    f = open(source)
    code = f.read()
    f.close()

    split_debug = str(bb_split.split_debug).upper()
    split_kill = str(bb_split.split_kill).upper()
    split_owner = str(bb_split.split_owner).upper()
    split_loop = str(bb_split.split_loop).upper()
    split_touch = str(bb_split.split_touch).upper()
    split_listen = str(bb_split.split_listen).upper()
    split_channel = str(bb_split.split_channel).upper()
    split_start = bb_split.split_start
    split_stop = bb_split.split_stop
    split_on_start = str(bb_split.split_on_start).upper()

    code = code.replace( "%ANIM_LIST", anim_string, 1 )
    code = code.replace( "%TIME_LIST", time_string, 1 )
    code = code.replace( "%DEBUG", split_debug, 1 )
    code = code.replace( "%KILL", split_kill, 1 )
    code = code.replace( "%OWNER_ONLY", split_owner, 1 )
    code = code.replace( "%ANIM_LOOP", split_loop, 1 )
    code = code.replace( "%ON_TOUCH", split_touch, 1 )
    code = code.replace( "%ON_LISTEN", split_listen, 1 )
    code = code.replace( "%ON_START", split_on_start, 1 )
    code = code.replace( "%CHANNEL", split_channel, 1 )
    code = code.replace( "%START", split_start, 1 )
    code = code.replace( "%STOP", split_stop, 1 )

    f = open(target, "w")
    f.write(code)
    f.close()

    print("Saved to:", target)

    return True























