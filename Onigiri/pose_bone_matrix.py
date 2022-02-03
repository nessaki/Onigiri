



import bpy
from mathutils import Matrix, Vector





def get_mat_offs(pose_bone):
    bone = pose_bone.bone        
    mat_offs = bone.matrix.to_4x4()
    mat_offs.translation = bone.head
    mat_offs.translation.y += bone.parent.length
    
    return mat_offs

def get_mat_rest(pose_bone, mat_pose_parent):
    bone = pose_bone.bone
    
    if pose_bone.parent:
        mat_offs = get_mat_offs(bone)
        
        
        if (not bone.use_inherit_rotation and 
            not bone.use_inherit_scale):                
            mat_rotscale = bone.parent.matrix_local @ mat_offs
            
        elif not bone.use_inherit_rotation:                        
            mat_size = Matrix.Identity(4)
            for i in range(3):
                mat_size[i][i] = mat_pose_parent.col[i].magnitude
            mat_rotscale = mat_size @ bone.parent.matrix_local @ mat_offs
            
        elif not bone.use_inherit_scale:
            mat_rotscale = mat_pose_parent.normalized() @ mat_offs
            
        else:
            mat_rotscale = mat_pose_parent @ mat_offs
            
        
        if not bone.use_local_location:
            mat_a = Matrix.Translation(
                mat_pose_parent @ mat_offs.translation)
            
            mat_b = mat_pose_parent.copy()
            mat_b.translation = Vector()
                        
            mat_loc = mat_a @ mat_b
        
        elif (not bone.use_inherit_rotation or 
              not bone.use_inherit_scale):                  
            mat_loc = mat_pose_parent @ mat_offs
            
        else:
            mat_loc = mat_rotscale.copy()
                  
    else:    
        mat_rotscale = bone.matrix_local
        if not bone.use_local_location:
            mat_loc = Matrix.Translation(bone.matrix_local.translation)
        else:
            mat_loc = mat_rotscale.copy()      
            
    return mat_rotscale, mat_loc

@default_to_existing_values
def get_mat_pose(pose_bone, mat_pose_parent, mat_basis):    
    mat_rotscale, mat_loc = get_mat_rest(pose_bone, mat_pose_parent)    
    mat_pose = mat_rotscale @ mat_basis
    mat_pose.translation = mat_loc @ mat_basis.translation
    
    return mat_pose

def default_to_existing_values(func):
    def func_new(pose_bone, mat_pose_parent=None, mat_basis=None):
        if pose_bone.parent and not mat_pose_parent:
            mat_pose_parent = pose_bone.parent.matrix
        if not mat_basis:
            mat_basis = pose_bone.matrix_basis

        func(pose_bone, mat_pose_parent, mat_basis)
    return func_new
