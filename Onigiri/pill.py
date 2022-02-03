







import bpy
import math
import mathutils
from .presets import skeleton as skel
from .presets import avatar_skeleton as skel_old
from .presets import volumes



YZZYX = mathutils.Matrix.Rotation(math.pi/2, 4, 'Y')
XYZZY = mathutils.Matrix.Rotation(math.pi/2, 4, 'X')





Z90 = mathutils.Matrix ((
    ( 0.0000,  1.0000, 0.0000, 0.0000),
    (-1.0000,  0.0000, 0.0000, 0.0000),
    ( 0.0000,  0.0000, 1.0000, 0.0000),
    ( 0.0000,  0.0000, 0.0000, 1.0000)
    ))

Z90I = Z90.inverted()







zeros = {
    0 : "000",
    1 : "00",
    2 : "0",
    3 : "",
    }
to_asc = {}
to_chr = {}
for i in range(256):
    c = chr(i)
    z = len(str(i))
    fbx = 'FBXASC' + zeros[z] + str(i)
    to_asc[c] = fbx
    to_chr[fbx] = c




def matrix_help():

    print("pill::matrix_help - I'm pill")
    help_text = """I are gone doop"""

    
    
    
    
    
    
    
    
    
    
    
    
    
    print(help_text)
    return False

def get_transform():
    return matrix_help()
def get_location():
    return matrix_help()
def get_rotation():
    return matrix_help()
def get_scale():
    return matrix_help()
def set_matrix():
    return matrix_help()
def set_transform():
    return matrix_help()
def set_location():
    return matrix_help()
def set_rotation():
    return matrix_help()
def set_scale():
    return matrix_help()







def quat_short(a,b):
    if a.dot(b) < 0:
        return b.negate()
    return a

def quat_long(a,b):
    if a.dot(b) > 0:
        return b.negate()
    return a


def rotate_matrix(mat, angle=[]):
    loc, rot, scale = mat.decompose()
    smat = mathutils.Matrix()
    for i in range(3):
        smat[i][i] = scale[i]
    eu = mathutils.Euler(map(math.radians, angle), 'XYZ')
    new_mat = mathutils.Matrix.Translation(loc) @ eu.to_matrix().to_4x4() @ smat
    return new_mat




def get_local_matrix(armature="", bone=""):
    armObj = bpy.data.objects[armature]
    poseBone = armObj.pose.bones[bone]
    if poseBone.parent:
        parentRefPoseMtx = poseBone.parent.bone.matrix_local
        boneRefPoseMtx = poseBone.bone.matrix_local
        parentPoseMtx = poseBone.parent.matrix
        bonePoseMtx = poseBone.matrix
        boneLocMtx = ( parentRefPoseMtx.inverted() @ boneRefPoseMtx ).inverted() @ ( parentPoseMtx.inverted() @ bonePoseMtx )
    else:
        boneRefPoseMtx = poseBone.bone.matrix_local
        bonePoseMtx = poseBone.matrix
        boneLocMtx = boneRefPoseMtx.inverted() @ bonePoseMtx
    return boneLocMtx




def add_vectors(a, b):
    if len(a) < len(b):
        print("length mismatch, last vector must be equal or larger")
        return False
    v = []
    for i in range(len(a)):
        v.append(a[i] + b[i])
    return v
def subtract_vectors(a, b):
    if len(a) < len(b):
        print("length mismatch, last vector must be equal or larger")
        return False
    v = []
    for i in range(len(a)):
        v.append(a[i] - b[i])
    return v
def round_to_tuple(a, f=6):
    b = list()
    for t in a:
        b.append(round(t), f)
    return tuple(b)
def round_to_list(a, f=6):
    b = list()
    for t in a:
        b.append(round(t), f)
    return b
def float_to_string(a, f=6):
    b = list()
    for c in a:
        b.append( f"{c:.ff}".rstrip('0') )
    return b

def quat_to_degrees(a):
    eu = a.to_euler()
    b = [math.degrees(eu.x), math.degrees(eu.y), math.degrees(eu.z)]
    return b










def eulerRotate(x,y,z, rot_order): 
    
    MATRIX_IDENTITY_3x3 = mathutils.Matrix([1,0,0],[0,1,0],[0,0,1])
    MATRIX_IDENTITY_4x4 = mathutils.Matrix([1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1])
    
    mats=[mathutils.RotationMatrix(x%360,3,'x'), mathutils.RotationMatrix(y%360,3,'y'), mathutils.RotationMatrix(z%360,3,'z')]
    
    
    return (mats[rot_order[2]] @ (mats[rot_order[1]] @ (mats[rot_order[0]] @ MATRIX_IDENTITY_3x3))).toEuler()






    
    
        
            
    

def matrix_from_list(l):
    M = mathutils.Matrix()
    for c in range(4):
        for r in range(4):
            M[c][r] = l[ r + (c*4) ]
    return M



def matrix_from_vectors(v):
    matL = list()
    for fl in v:
        matL.extend( [float(a) for a in fl] )
    print("PROBABLY NOT FUNCTIONAL: matrix_from_vectors")
    return matrix_from_list(matL)










def matrix_from_list(l):
    M = mathutils.Matrix()
    for c in range(4):
        for r in range(4):
            M[c][r] = l[4*r + c]
    return M



    
    
    
        






def inverse_bind(arm, bone):
    boneObj = bpy.data.objects[arm].data.bones[bone]
    
    if boneObj.get('bind_mat') != None:
        
        
        M = list_to_matrix(boneObj['bind_mat'])
        if 1 == 0: 
            M = YZZYX @ M
        
        return M.inverted()

    

    else: 
        loc - boneObj.head_local
        R = mathutils.Matrix()
        L = mathutils.Matrix.Translation((loc))

    if bone in vol.vol_joints:
        rot = skel_old.avatar_skeleton[bone]['rot'] 
        scale = volumes.vol_joints[bone]['scale']
        matf = L @ R @ rot @ scale
        
        
            
        
        
        matf = Z90I @ matf @ Z90

    return matf












    
    
        
        
        

        

        
              
    
    
    
    
    
    
    
    
    
    
    


    
    
    
    
    
    
    
    



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






def get_sl_vector_difference(vec):
    vr = vec.replace("<", "")
    vr = vr.replace(">", "")
    vs = vr.split()
    vl = list()
    vfinal = list()
    for v in vs:
        vf = v.split(",")
        vl.append([float(fl) for fl in vf])
        print("vl:", vl)
        vfinal.append(vl)
    v0 = vl[0]
    v1 = vl[1]
    v = list()
    for i in range(len(v0)):
        a = v0[i]
        b = v1[i]
        v.append( abs((a) - (b)) )
    return v









def update_matrices(obj):
    if obj.parent is None:
        obj.matrix_world = obj.matrix_basis
    else:
        obj.matrix_world = obj.parent.matrix_world @                           obj.matrix_parent_inverse @                           obj.matrix_basis








def BuildScaleMatrix(s):
    return Matrix.Scale(s[0],4,(1,0,0)) @ Matrix.Scale(s[1],4,(0,1,0)) @ Matrix.Scale(s[2],4,(0,0,1))

def BuildRotationMatrixXYZ(r):
    return  Matrix.Rotation(r[2],4,'Z') @ Matrix.Rotation(r[1],4,'Y') @ Matrix.Rotation(r[0],4,'X')

def BuildMatrix(t,r,s):
    return   Matrix.Translation(t) @ BuildRotationMatrixXYZ(r) @ BuildScaleMatrix(s)

def UpdateObjectTransform(ob):
    ob.matrix_world = BuildMatrix(ob.location, ob.rotation_euler, ob.scale)





def ident(tmat):
    if type(tmat[0]) == type(str()):
        one = "1"
    else:
        one = 1.0
    c = 0
    for i in range(0, 16, 4):
        tmat[i+c] = one
        c +=1
    return tmat






def matrix_to_text(mat):
    tmat = list()
    for v in mat:
        for n in v:
            tmat.append(f"{n:.6f}")

    return tmat


tMatrix = matrix_to_text(mathutils.Matrix())




def print_matrix(mat):
    for r in range(0, 16, 4):
        print(mat[r:r+4])
















def recompose(
    rig_type=None,
    bone_space="local",
    offsets=None,
    dBone=None,


    use_offset_volume=False,
    use_offset_location=False,
    use_offset_rotation=False,
    use_offset_scale=False,
    process_volume_bones=True):

    print("Processing from pill, using old skeleton file (avatar_skeleton)")

    bone = dBone.name

    if bone_space == "global":
        rig_type = "absolute_" + rig_type

    l = skel_old.avatar_skeleton[bone][rig_type]
    r = skel_old.avatar_skeleton[bone]['rot']  
    s = skel_old.avatar_skeleton[bone]['scale'] 

    
    
    
    
    








    
    
    if bone in volumes.vol_joints:
        if process_volume_bones == True:
            l = skel_old.avatar_skeleton[bone]['pos']

    
    
    
    
    
    
    
    
    
    
    
    
    if bone_space == "global":
        
        
        
        
        l = skel_old.avatar_skeleton[bone][rig_type]

        
        
        
        
        if use_offset_location == True:
            L_SKEL = mathutils.Matrix.Translation(l)
            L = mathutils.Matrix.Translation(l)
            M_OFF = offsets['global']['matrix']
            L = M_OFF @ L_SKEL
            
            
            l = L.to_translation()

        
        
        else:
            l = dBone.head_local.copy()
            
            
            L = mathutils.Matrix.Translation(l)
            R = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Z')
            RI = R.inverted()
            L = R @ L
            
            
            l = L.to_translation()


    
    
    
    l_ofs, r_ofs, s_ofs = offsets[bone_space]['matrix'].decompose()

    
    L_mat = mathutils.Matrix.Translation(l)
    L_ofs = mathutils.Matrix.Translation(l_ofs)

    
    
    
    rot = [math.radians(a) for a in r] 

    R_mat = mathutils.Euler(rot,'XYZ').to_matrix().to_4x4()

    
    
    
    
    
    
    
    if use_offset_rotation == True:
        R_ofs = r_ofs.to_matrix().to_4x4()
    else:
        R_ofs = mathutils.Euler((0,0,0),'XYZ').to_matrix().to_4x4()


    
    
    
    
    
    
    
    
    
    S_mat = mathutils.Matrix()
    S_ofs = mathutils.Matrix()
    for i in range(3):
        S_mat[i][i] = s[i]
    if use_offset_scale == True:
        for i in range(3):
            S_ofs[i][i] = s_ofs[i]

    
    
    R90y = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Y')
    R90yI = R90y.inverted()
    R_ofs_f = R_ofs  

    
    L = L_mat @ L_ofs
    R = R_mat @ R_ofs_f
    S = S_mat @ S_ofs

    
    
    
    
    
    if bone_space == 'global':
        L = L_mat









    
    
    if 1 == 0:
        if bone == 'R_UPPER_ARM':
            print("=====================================")
            print("pill:")
            print("-------------------------------------")
            print("Bone:", bone)
            print("Bone Space:", bone_space)
            print(bone + ":R_mat:", to_deg(R_mat))
            print(R_mat)
            print(bone + ":R_ofs:", to_deg(R_ofs))
            print(R_ofs)
            print(bone + ":L_ofs:", L_ofs.to_translation())
            print(bone + ":l from skel:", l)
            print(L_ofs)
            print(bone + ":L_mat:", L_mat.to_translation())
            print(L_mat)

            print(bone + ":R_ofs_f:", to_deg(R_ofs_f))
            print(R_ofs_f)
            print(bone + ":R:", to_deg(R))
            print(R)
            print("offset matrix:")
            print(offsets[bone_space]['matrix'])
            print("=====================================")



    return L, R, S






def matrify(l,r,s):
    L = mathutils.Matrix.Translation(l)
    
    
    R = r.to_matrix().to_4x4()
    S = mathutils.Matrix()
    for i in range(3):
        S[i][i] = s[i]
    return L, R, S




def to_deg(mat):
    eu = mat.to_euler()
    return [math.degrees(round(a, 4)) for a in eu]




def get_pose_matrix_in_other_space(mat, pose_bone):
    """ Returns the transform matrix relative to pose_bone's current
        transform space.  In other words, presuming that mat is in
        armature space, slapping the returned matrix onto pose_bone
        should give it the armature-space transforms of mat.
        TODO: try to handle cases with axis-scaled parents better.
    """
    rest = pose_bone.bone.matrix_local.copy()
    rest_inv = rest.inverted()
    if pose_bone.parent:
        par_mat = pose_bone.parent.matrix.copy()
        par_inv = par_mat.inverted()
        par_rest = pose_bone.parent.bone.matrix_local.copy()
    else:
        par_mat = Matrix()
        par_inv = Matrix()
        par_rest = Matrix()

    
    smat = rest_inv @ (par_rest @ (par_inv @ mat))

    
    
    
    

    return smat







def get_rest_pose(pose_bone):
    rest = pose_bone.bone.matrix_local.copy()
    if pose_bone.parent:
        par_rest = pose_bone.parent.bone.matrix_local.copy()
    else:
        par_rest = Matrix()
    return par_rest.inverted() @ rest



def safe_object_mode():
    mode = bpy.context.mode
    
    
    if bpy.context.active_object == None:
        if len(bpy.context.selected_objects) > 0:
            bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
        return None
    bpy.ops.object.mode_set(mode='OBJECT')
    
    if mode == 'EDIT_ARMATURE':
        return 'EDIT'
    return mode





def close_enough(a, b, tol=0.000001):
    if a > b:
        n = round((a - b), 6)
    elif a < b:
        n = round((b - a), 6)
    elif a == b:
        return False
    if n > tol:
        return True
    return False











def vec_equal(vec1,vec2, tol=0.001):
    mat = mathutils.Matrix(([vec1[0],vec2[0]],[vec1[1],vec2[1]]))
    D = mat.determinant()
    if (abs(D) <= tol):
        mat = mathutils.Matrix(([vec1[0],vec2[0]],[vec1[2],vec2[2]]))
        D = mat.determinant()
        if (abs(D) <= tol):
            mat = mathutils.Matrix(([vec1[1],vec2[1]],[vec1[2],vec2[2]]))
            D = mat.determinant()
            if (abs(D) <= tol):
                return True
    return False











