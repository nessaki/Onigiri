




















    
        
        
    


import bpy
import re



    
        
        
    

def write_armature(
        context,
        filepath,
        frame_start,
        frame_end,
        global_scale=1.0,
        rotate_mode='NATIVE',
        root_transform_only=False,
    
    buffer=False,
):

    def ensure_rot_order(rot_order_str):
        if set(rot_order_str) != {'X', 'Y', 'Z'}:
            rot_order_str = "XYZ"
        return rot_order_str

    from mathutils import Matrix, Euler
    from math import degrees

    
    if buffer == True:
        buf = []
    else:
        file = open(filepath, "w", encoding="utf8", newline="\n")

    obj = context.object
    arm = obj.data

    
    
    children = {None: []}




    
    for bone in arm.bones:






        children[bone.name] = []

    
    
    for bone in arm.bones:
        children[getattr(bone.parent, "name", None)].append(bone.name)

    
    serialized_names = []

    node_locations = {}

    if buffer == True:
        buf.append("HIERARCHY\n")
    else:
        file.write("HIERARCHY\n")

    def write_recursive_nodes(bone_name, indent):
        my_children = children[bone_name]

        indent_str = "\t" * indent

        bone = arm.bones[bone_name]
        pose_bone = obj.pose.bones[bone_name]
        loc = bone.head_local
        node_locations[bone_name] = loc

        if rotate_mode == "NATIVE":
            rot_order_str = ensure_rot_order(pose_bone.rotation_mode)
        else:
            rot_order_str = rotate_mode

        
        if bone.parent:
            loc = loc - node_locations[bone.parent.name]

        if indent:
            if buffer == True:
                buf.append("%sJOINT %s\n" % (indent_str, bone_name))
            else:
                file.write("%sJOINT %s\n" % (indent_str, bone_name))

        else:
            if buffer == True:
                buf.append("%sROOT %s\n" % (indent_str, bone_name))
            else:
                file.write("%sROOT %s\n" % (indent_str, bone_name))

        if buffer == True:
            buf.append("%s{\n" % indent_str)
            buf.append("%s\tOFFSET %.6f %.6f %.6f\n" % (indent_str, *(loc * global_scale)))
        else:
            file.write("%s{\n" % indent_str)
            file.write("%s\tOFFSET %.6f %.6f %.6f\n" % (indent_str, *(loc * global_scale)))

        if (bone.use_connect or root_transform_only) and bone.parent:
            if buffer == True:
                buf.append("%s\tCHANNELS 3 %srotation %srotation %srotation\n" % (indent_str, *rot_order_str))
            else:
                file.write("%s\tCHANNELS 3 %srotation %srotation %srotation\n" % (indent_str, *rot_order_str))

        else:
            if buffer == True:
                buf.append("%s\tCHANNELS 6 Xposition Yposition Zposition %srotation %srotation %srotation\n" % (indent_str, *rot_order_str))
            else:
                file.write("%s\tCHANNELS 6 Xposition Yposition Zposition %srotation %srotation %srotation\n" % (indent_str, *rot_order_str))

        if my_children:
            
            

            
            for child_bone in my_children:
                serialized_names.append(child_bone)
                write_recursive_nodes(child_bone, indent + 1)

        else:
            
            if buffer == True:
                buf.append("%s\tEnd Site\n" % indent_str)
                buf.append("%s\t{\n" % indent_str)
                loc = bone.tail_local - node_locations[bone_name]
                buf.append("%s\t\tOFFSET %.6f %.6f %.6f\n" % (indent_str, *(loc * global_scale)))
                buf.append("%s\t}\n" % indent_str)
            else:
                file.write("%s\tEnd Site\n" % indent_str)
                file.write("%s\t{\n" % indent_str)
                loc = bone.tail_local - node_locations[bone_name]
                file.write("%s\t\tOFFSET %.6f %.6f %.6f\n" % (indent_str, *(loc * global_scale)))
                file.write("%s\t}\n" % indent_str)

        if buffer == True:
            buf.append("%s}\n" % indent_str)
        else:
            file.write("%s}\n" % indent_str)

    if len(children[None]) == 1:
        key = children[None][0]
        serialized_names.append(key)
        indent = 0

        write_recursive_nodes(key, indent)

    else:
        
        
        i = 0
        key = "__%d" % i
        while key in children:
            i += 1
            key = "__%d" % i

        if buffer == True:
            buf.append("ROOT %s\n" % key)
            buf.append("{\n")
            buf.append("\tOFFSET 0.0 0.0 0.0\n")
            buf.append("\tCHANNELS 0\n")  
        else:
            file.write("ROOT %s\n" % key)
            file.write("{\n")
            file.write("\tOFFSET 0.0 0.0 0.0\n")
            file.write("\tCHANNELS 0\n")  

        indent = 1

        
        for child_bone in children[None]:
            serialized_names.append(child_bone)
            write_recursive_nodes(child_bone, indent)

        if buffer == True:
            buff.append("}\n")
        else:
            file.write("}\n")

    
    

    class DecoratedBone:
        __slots__ = (
            
            "name",
            "parent",  
            
            "rest_bone",
            
            "pose_bone",
            
            "pose_mat",
            
            "rest_arm_mat",
            
            "rest_local_mat",
            
            "pose_imat",
            
            "rest_arm_imat",
            
            "rest_local_imat",
            
            "prev_euler",
            
            "skip_position",
            "rot_order",
            "rot_order_str",
            
            "rot_order_str_reverse",
        )

        _eul_order_lookup = {
            'XYZ': (0, 1, 2),
            'XZY': (0, 2, 1),
            'YXZ': (1, 0, 2),
            'YZX': (1, 2, 0),
            'ZXY': (2, 0, 1),
            'ZYX': (2, 1, 0),
        }

        def __init__(self, bone_name):
            self.name = bone_name
            self.rest_bone = arm.bones[bone_name]
            self.pose_bone = obj.pose.bones[bone_name]

            if rotate_mode == "NATIVE":
                self.rot_order_str = ensure_rot_order(self.pose_bone.rotation_mode)
            else:
                self.rot_order_str = rotate_mode
            self.rot_order_str_reverse = self.rot_order_str[::-1]

            self.rot_order = DecoratedBone._eul_order_lookup[self.rot_order_str]

            self.pose_mat = self.pose_bone.matrix

            
            self.rest_arm_mat = self.rest_bone.matrix_local
            self.rest_local_mat = self.rest_bone.matrix

            
            self.pose_imat = self.pose_mat.inverted()
            self.rest_arm_imat = self.rest_arm_mat.inverted()
            self.rest_local_imat = self.rest_local_mat.inverted()

            self.parent = None
            self.prev_euler = Euler((0.0, 0.0, 0.0), self.rot_order_str_reverse)
            self.skip_position = ((self.rest_bone.use_connect or root_transform_only) and self.rest_bone.parent)

        def update_posedata(self):
            self.pose_mat = self.pose_bone.matrix
            self.pose_imat = self.pose_mat.inverted()

        def __repr__(self):
            if self.parent:
                return "[\"%s\" child on \"%s\"]\n" % (self.name, self.parent.name)
            else:
                return "[\"%s\" root bone]\n" % (self.name)

    bones_decorated = [DecoratedBone(bone_name) for bone_name in serialized_names]

    
    bones_decorated_dict = {dbone.name: dbone for dbone in bones_decorated}
    for dbone in bones_decorated:
        parent = dbone.rest_bone.parent
        if parent:
            dbone.parent = bones_decorated_dict[parent.name]
    del bones_decorated_dict
    

    scene = context.scene
    bpy.context.view_layer.update()
    frame_current = scene.frame_current

    if buffer == True:
        buf.append("MOTION\n")
        buf.append("Frames: %d\n" % (frame_end - frame_start + 1))
        buf.append("Frame Time: %.6f\n" % (1.0 / (scene.render.fps / scene.render.fps_base)))
    else:
        file.write("MOTION\n")
        file.write("Frames: %d\n" % (frame_end - frame_start + 1))
        file.write("Frame Time: %.6f\n" % (1.0 / (scene.render.fps / scene.render.fps_base)))

    for frame in range(frame_start, frame_end + 1):
        scene.frame_set(frame)

        for dbone in bones_decorated:
            dbone.update_posedata()

        for dbone in bones_decorated:
            trans = Matrix.Translation(dbone.rest_bone.head_local)
            itrans = Matrix.Translation(-dbone.rest_bone.head_local)

            if dbone.parent:
                mat_final = dbone.parent.rest_arm_mat @ dbone.parent.pose_imat @ dbone.pose_mat @ dbone.rest_arm_imat
                mat_final = itrans @ mat_final @ trans
                loc = mat_final.to_translation() + (dbone.rest_bone.head_local - dbone.parent.rest_bone.head_local)
            else:
                mat_final = dbone.pose_mat @ dbone.rest_arm_imat
                mat_final = itrans @ mat_final @ trans
                loc = mat_final.to_translation() + dbone.rest_bone.head

            
            rot = mat_final.to_euler(dbone.rot_order_str_reverse, dbone.prev_euler)

            if not dbone.skip_position:
                if buffer == True:
                    buf.append("%.6f %.6f %.6f " % (loc * global_scale)[:])
                else:
                    file.write("%.6f %.6f %.6f " % (loc * global_scale)[:])
            if buffer == True:
                buf.append("%.6f %.6f %.6f " % (degrees(rot[dbone.rot_order[0]]), degrees(rot[dbone.rot_order[1]]), degrees(rot[dbone.rot_order[2]])))
            else:
                file.write("%.6f %.6f %.6f " % (degrees(rot[dbone.rot_order[0]]), degrees(rot[dbone.rot_order[1]]), degrees(rot[dbone.rot_order[2]])))

            dbone.prev_euler = rot

        if buffer == True:
            buf.append("\n")
        else:
            file.write("\n")
    if buffer == True:
        bufstr = "".join(buf)
    else:
        file.close()

    scene.frame_set(frame_current)

    

    if buffer == True:
        return bufstr

def save(
        context, filepath="",
        frame_start=-1,
        frame_end=-1,
        global_scale=1.0,
        rotate_mode="NATIVE",
        root_transform_only=False,
    
    
    buffer=False,
):
    buf = write_armature(
        context, filepath,
        frame_start=frame_start,
        frame_end=frame_end,
        global_scale=global_scale,
        rotate_mode=rotate_mode,
        root_transform_only=root_transform_only,
    
    buffer=buffer,
    )

    return buf
    




