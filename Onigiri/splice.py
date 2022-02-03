
import bpy
import math
import mathutils




if True:
    props = {}
    
    
    
    props['startup'] = True
    props['camera'] = False















def main(
    source=None, target=None, keys=False, motion=False,
    gap_insert=False, gap_start=1, gap_end=1,
    spread_enabled=False, spread_start=0, spread_end=0,
    ):

    print("------------------------------")
    print("keys:", keys)
    print("motion:", motion)
    print("gap_insert:", gap_insert)
    print("gap_start:", gap_start)
    print("gap_end:", gap_end)
    print("spread_enabled:", spread_enabled)
    print("spread_start:", spread_start)
    print("spread_end:", spread_end)
    print("------------------------------")


    
    
    
    
    
    
        
        

    
    bb_splice = bpy.context.scene.bb_splice
    obj = bpy.data.objects
    sarmObj = obj[source]
    tarmObj = obj[target]

    
    frame_current = int(bpy.context.scene.frame_current)

    
    if tarmObj.animation_data == None:
        tarmObj.animation_data_create()
    if tarmObj.animation_data.action == None:
        AC_OBJ = bpy.data.actions.new("SPLICER")
        tarmObj.animation_data.action = AC_OBJ

    
    
    
    
    

    
    
    keys_removed = remove_isolated_keys(armature=tarmObj.name)
    print("::remove_isolated_keys:: returns count", keys_removed)

    
    t_actionObj = tarmObj.animation_data.action
    t_frame_start, t_frame_end = t_actionObj.frame_range
    t_frame_start = int(t_frame_start)
    t_frame_end = int(t_frame_end)
    
    
    has_keys = False
    if len(t_actionObj.fcurves) != 0:
        for fc in t_actionObj.fcurves:
            if len(fc.keyframe_points) > 0:
                has_keys = True
                break
    if has_keys == False:
        t_frame_end = t_frame_start 





    
    
    bpy.context.scene.frame_set(frame_current)
    tmats = {}
    for boneObj in tarmObj.pose.bones:
        bone = boneObj.name
        tmats[bone] = boneObj.matrix.copy()

    
    
    
    s_has_action = False
    if sarmObj.animation_data != None:
        if sarmObj.animation_data.action != None:
            s_has_action = True
            s_actionObj = sarmObj.animation_data.action
            start, end = sarmObj.animation_data.action.frame_range
            s_frame_start = int(start)
            s_frame_end = int(end)

    
    if spread_enabled == True:
        if spread_start == spread_end:
            print("Preliminary test shows no frame spread to capture but spread is enabled.")
            return False
        s_frame_start, s_frame_end = int(spread_start), int(spread_end)
    
    
    elif spread_enabled == False and s_has_action == False:
        print("There's no sample range to acquire, motion is disabled, spread is disabled and there is no animation on", sarmObj.name)
        return False

    

    
    s_frame_data = {}
    if keys == True:
        if s_has_action == True:
            s_frame_data = get_animated_keys(armature=sarmObj.name)
            
            if len(s_frame_data) == 0:
                print("No keys on the source object")
                if spread_enabled == False:
                    print("No motion keys, set a spread to capture an empty time line if you are using controllers.")
                    return False
                
                else:
                    print("The spread feature will be used for the capture range")
        else:
            print("The feature (keys) is requested but there's no animation, reverting to spread")


    
    
    
    
    
    
    
    frame_gap = int(abs(s_frame_start - s_frame_end))
    
    insertion_range = gap_start + frame_gap + gap_end - 1 

    print("insertion_range =", insertion_range)

    
    if gap_insert == True:
        result = move_keys(armature=tarmObj.name, start=frame_current, spread=insertion_range)

    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    

    s_matrix_data = get_matrices(armature=sarmObj.name, start=s_frame_start, end=s_frame_end, force=True)

    
    
    
    
    
    s_motion_data = {} 
    if motion == True:
        s_motion_data = get_motion(armature=sarmObj.name, start=s_frame_start, end=s_frame_end, matrices=s_matrix_data)





    
    
    
    bone_list = set()
    for bone in s_frame_data:
        bone_list.add(bone)
    for bone in s_motion_data:
        bone_list.add(bone)
    if len(bone_list) == 0:
        print("There was no motion available for use.  If this is a result of motion type then set (Keys) as well")
        print("as (Motion) for the capture, currently your settings are as follows: [Keys: ", keys, "] [Motion: ", motion, "]", sep="")
        return False
    
    

    
    
    
    

    




    
    s_key_data = {}
    for bone in s_frame_data:
        s_key_data[bone] = {}
        for frame in s_frame_data[bone]:
            s_key_data[bone][frame] = {}
            s_key_data[bone][frame]['matrix'] = s_matrix_data[bone][frame]['matrix']
            for trs in s_frame_data[bone][frame]:
                if trs != 'matrix': 
                    
                    s_key_data[bone][frame][trs] = True 
    
    
    for bone in s_motion_data:
        
        if bone not in s_key_data:
            s_key_data[bone] = {}
        for frame in s_motion_data[bone]:
            if frame not in s_key_data[bone]:
                s_key_data[bone][frame] = {}
            
            s_key_data[bone][frame]['matrix'] = s_matrix_data[bone][frame]['matrix']
            for trs in s_motion_data[bone][frame]:
                if trs != 'matrix':
                    
                    s_key_data[bone][frame][trs] = True

    
    
    
    if gap_insert == True:
        
        t_frame = gap_start + frame_current - 1
    else:
        t_frame = gap_start + t_frame_end
    s_map = {}
    for s_frame in range(s_frame_start, s_frame_end+1):
        s_map[s_frame] = t_frame
        t_frame += 1

    
    
    
    

    
    
    
    

    
    
    
    frame_data = {}
    for bone in s_key_data:
        for frame in s_key_data[bone]:
            if frame not in frame_data:
                frame_data[frame] = {}
            if bone not in frame_data[frame]:
                frame_data[frame][bone] = {}
            for trs in s_key_data[bone][frame]:
                frame_data[frame][bone][trs] = s_key_data[bone][frame][trs]






    
    
    
    for s_frame in frame_data:
        t_frame = s_map[s_frame]

        bpy.context.scene.frame_set(t_frame)
        
        for tboneObj in tarmObj.pose.bones:
            bone = tboneObj.name

            bmat = s_matrix_data[bone][s_frame]['matrix_basis']
            tboneObj.matrix_basis = bmat

            
            if bone not in s_key_data:
                continue
            if s_frame not in s_key_data[bone]:
                continue

            
            if 'rot' in s_key_data[bone][s_frame]:
                tboneObj.keyframe_insert(data_path='rotation_quaternion', frame=t_frame)
            if 'loc' in s_key_data[bone][s_frame]:
                tboneObj.keyframe_insert(data_path='location', frame=t_frame)
            if 'scl' in s_key_data[bone][s_frame]:
                tboneObj.keyframe_insert(data_path='scale', frame=t_frame)

    return True





    
        
    
        









def move_keys(armature=None, start=1, spread=2):
    obj = bpy.data.objects
    armObj = obj[armature]
    for fcurve in armObj.animation_data.action.fcurves:
        for point in fcurve.keyframe_points:
            
            if point.co.x >= start:
                point.co.x += spread
    return True



def remove_isolated_keys(armature=None):
    armObj = bpy.data.objects[armature]
    count = 0
    action = armObj.animation_data.action
    for fcurve in action.fcurves:
        if len(fcurve.keyframe_points) < 2:
            action.fcurves.remove(fcurve)
            count +=1
    return count













def get_animated_keys(armature=None):

    obj = bpy.data.objects
    armObj = obj[armature]

    if armObj.animation_data == None:
        return []
    if armObj.animation_data.action == None:
        return []

    
    actionObj = armObj.animation_data.action

    
    
    if len(actionObj.fcurves) == 0:
        return []

    
    
    fcurves = actionObj.fcurves

    
    
    
    
    
    
    
    fcurve_paths = {}
    for boneObj in armObj.data.bones:

        path_key = 'pose.bones["' + boneObj.name + '"]'
        fcurve_paths[path_key] = boneObj.name

    
    frame_data = {}
    
    point_data = {}

    
    
    
    
    
    
    for fc in fcurves:

        
        
        dp, idx = fc.data_path, fc.array_index

        
        bone_path, delimiter, transform_type = dp.rpartition('.')

        
        
        if bone_path not in fcurve_paths:
            continue

        
        
        
        real_bone = fcurve_paths[bone_path]

        
        rot_mode = armObj.pose.bones[real_bone].rotation_mode

        
        

        
        

        if transform_type == 'rotation_quaternion' and rot_mode == 'QUATERNION':
            trs = 'rot'

            
            if idx == 0:
                
                continue

        elif transform_type == 'rotation_euler' and rot_mode != 'QUATERNION':
            trs = 'rot'

        
        
        
        
        
        elif transform_type == 'rotation_euler' and rot_mode == 'QUATERNION':
            trs = 'rot'

        elif transform_type == 'location':
            trs = 'loc'

        
        
        
        
        elif transform_type == 'scale':
            
            
            continue

        else:
            
            
            continue

        
        if real_bone not in frame_data:
            frame_data[real_bone] = {}
            
            point_data[real_bone] = {}

        if trs not in frame_data[real_bone]:
            frame_data[real_bone][trs] = {}
            
            point_data[real_bone][trs] = {}

        
        frames = [int(k.co.x) for k in fc.keyframe_points]
        
        frames_set = set(frames)
        
        frame_numbers = list(sorted(frames_set))

        if len(frame_numbers) == 0:
            print("No frames to process, not sure why this happened")
            return []
        frame_data[real_bone][trs] = frame_numbers

        
        
        
        points = [k.co.y for k in fc.keyframe_points]
        point_data[real_bone][trs][idx] = points

    
    
    
    new_data = {}
    for bone in frame_data:
        new_data[bone] = {}
        
        for trs in frame_data[bone]:
            
            frames = frame_data[bone][trs]
            for frame in frames:
                if frame not in new_data[bone]:
                    new_data[bone][frame] = {}
                if trs not in new_data[bone][frame]:
                    new_data[bone][frame][trs] = {}

                
                
                
                
                for p in point_data[bone][trs]:
                    new_data[bone][frame][trs][p] = point_data[bone][trs][p]

    return new_data









def get_matrices(armature=None, start=0, end=0, force=False):

    obj = bpy.data.objects
    armObj = obj[armature]

    if abs(start - end) == 0:
        print("get_matrices reports: no range delivered")
        return False

    matrices = {}
    for frame in range(start, end+1):
        bpy.context.scene.frame_set(frame)
        for boneObj in armObj.pose.bones:
            bone = boneObj.name
            if bone not in matrices:
                matrices[bone] = {}
            matrices[bone][frame] = {}
            mat = boneObj.matrix.copy()
            matrices[bone][frame]['matrix'] = mat
            if force == True:
                
                
                boneObj.matrix = mat
            pmat = boneObj.matrix_basis.copy()
            matrices[bone][frame]['matrix_basis'] = pmat
            
            rmat = get_real_matrix(armObj.name, bone)
            
            matrices[bone][frame]['rot'] = to_deg(rmat)
            matrices[bone][frame]['loc'] = rmat.to_translation()

    return matrices







def get_motion(armature=None, start=0, end=0, matrices={}):
    if abs(start - end) == 0:
        print("get_motion reports: no range delivered")
        return False

    if len(matrices) == 0:
        print("I need some composed matrices from (get_matrices) in order to work")
        return False

    

    
    
    
    
    motion = {}

    
    

    
    
    if 1 == 1:
        for bone in matrices:
            
            rot_last = matrices[bone][start]['rot']
            loc_last = matrices[bone][start]['loc']
            for frame in matrices[bone]:
                rot_now = matrices[bone][frame]['rot']
                loc_now = matrices[bone][frame]['loc']
                
                if close_enough(rot_now, rot_last, tol=0.01) == True:
                    if bone not in motion:
                        motion[bone] = {}
                    if frame not in motion[bone]:
                        motion[bone][frame] = {}
                    motion[bone][frame]['rot'] = True 
                    motion[bone][frame]['matrix'] = matrices[bone][frame]['matrix']  
                    
                    if frame-1 not in motion[bone]:
                        motion[bone][frame-1] = {}
                    motion[bone][frame-1]['rot'] = True
                    motion[bone][frame-1]['matrix'] = matrices[bone][frame-1]['matrix']
                    rot_last = rot_now
                if close_enough(loc_now, loc_last, tol=0.01) == True:
                    if bone not in motion:
                        motion[bone] = {}
                    if frame not in motion[bone]:
                            motion[bone][frame] = {}
                    motion[bone][frame]['loc'] = True
                    motion[bone][frame]['matrix'] = matrices[bone][frame]['matrix']
                    
                    if frame-1 not in motion[bone]:
                        motion[bone][frame-1] = {}
                    motion[bone][frame-1]['loc'] = True
                    motion[bone][frame-1]['matrix'] = matrices[bone][frame-1]['matrix']  
                    loc_last = loc_now
    return motion 






def get_real_matrix(armature, bone):
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
    
    m3 = dbmatl.to_3x3()
    m4 = m3.to_4x4()
    m4I = m4.inverted()
    real_mat = m4 @ rp_composed @ m4I
    return real_mat



def to_deg(mat, limit=8):
    eu = mat.to_euler()
    deg = [math.degrees(round(a, limit)) for a in eu]
    return deg





def close_enough(a,b, tol=0.001):
    for (x,y) in zip(a,b):
        if abs(x-y) > tol:
            return True
    return False



