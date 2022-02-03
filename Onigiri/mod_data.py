


import mathutils
from mathutils import Matrix






actions = {}


















extra_interpolation_types = {
    "SINE": "IPO_SINE",
    "QUAD": "IPO_QUAD",
    "CUBIC": "IPO_CUBIC",
    "QUART": "IPO_QUART",
    "QUINT": "IPO_QUINT",
    "EXPO": "IPO_EXPO",
    "CIRC": "IPO_CIRC",
    "BACK": "IPO_BACK",
    "BOUNCE": "IPO_BOUNCE",
    "ELASTIC": "IPO_ELASTIC",
    }




X90 = Matrix((
            (1.0000,  0.0000,  0.0000, 0.0000),
            (0.0000, -0.0000, -1.0000, 0.0000),
            (0.0000,  1.0000, -0.0000, 0.0000),
            (0.0000,  0.0000,  0.0000, 1.0000)
        ))
Y90 = Matrix((
            (-0.0000, 0.0000,  1.0000, 0.0000),
            ( 0.0000, 1.0000,  0.0000, 0.0000),
            (-1.0000, 0.0000, -0.0000, 0.0000),
            ( 0.0000, 0.0000,  0.0000, 1.0000)
            ))
Z90 = Matrix ((
            (-0.0000, -1.0000, 0.0000, 0.0000),
            ( 1.0000, -0.0000, 0.0000, 0.0000),
            ( 0.0000,  0.0000, 1.0000, 0.0000),
            ( 0.0000,  0.0000, 0.0000, 1.0000)
            ))

X90I = X90.inverted()
Y90I = Y90.inverted()
Z90I = Z90.inverted()

bb_const = {}
bb_const["RAD"] = 0.01745333
bb_const["meters_to_inches"] = 39.3701













bb_const["bone_roll"] = {
    "mHandThumb1Left": 0.7853981852531433,
    "mHandThumb2Left": 0.7853981852531433,
    "mHandThumb3Left": 0.7853981852531433,
    "mHandThumb1Right": -0.7853981852531433,
    "mHandThumb2Right": -0.7853981852531433,
    "mHandThumb3Right": -0.7853981852531433,
    "mHipRight": -0.13089969754219055,
    "mHipLeft": 0.13089969754219055,
    }




bb_const["constraint_types"] = ["COPY_TRANSFORMS"]


bb_const["constraint_influence"] = 1






temp_dict = {}




g_var = {}










source_skels = []




target_skels = [] 
target_bone = {} 
target_head = {} 
target_tail = {} 
target_roll = {} 





target_bones = []

tbones_heads = []
tbones_tails = []
tbones_rolls = []

mbones_list = [] 
pbones_list = [] 



target_mbones = {} 
target_pbones = {} 



source_mbones = {} 
source_pbones = {} 

source_used = {} 




source_run = {}
source_run["saved"] = 0
source_old = {}





target_links = {}




source_links = {}

source_bones = [] 



connect_state = {}



qualified_armatures = {}





unused_bones = {}




template_map = {}



vbone_anchor = "mHead"






problem_bones = [

'mPelvis',

'mSpine1',
'mSpine2',
'mSpine3',
'mSpine4',

]








safe_bones = [

'mFaceEyeAltRight',
'mFaceEyeAltLeft',
'mFaceForeheadLeft',
'mFaceForeheadRight',
'mFaceEyebrowOuterLeft',
'mFaceEyebrowCenterLeft',
'mFaceEyebrowInnerLeft',
'mFaceEyebrowOuterRight',
'mFaceEyebrowCenterRight',
'mFaceEyebrowInnerRight',
'mFaceEyeLidUpperLeft',
'mFaceEyeLidLowerLeft',
'mFaceEyeLidUpperRight',
'mFaceEyeLidLowerRight',
'mFaceNoseLeft',
'mFaceNoseCenter',
'mFaceNoseRight',
'mFaceCheekLowerLeft',
'mFaceCheekUpperLeft',
'mFaceCheekLowerRight',
'mFaceCheekUpperRight',
'mFaceChin',
'mFaceLipLowerLeft',
'mFaceLipLowerRight',
'mFaceLipLowerCenter',
'mFaceJawShaper',
'mFaceForeheadCenter',
'mFaceNoseBase',
'mFaceLipUpperLeft',
'mFaceLipUpperRight',
'mFaceLipCornerLeft',
'mFaceLipCornerRight',
'mFaceLipUpperCenter',
'mFaceEyecornerInnerLeft',
'mFaceEyecornerInnerRight',
'mFaceNoseBridge',
'mSkull',
'mEyeRight',
'mEyeLeft',
'mToeRight',
'mToeLeft',
'mGroin',
]


almost_safe_bones = [
'mFaceRoot',
'mFaceEar1Left',
'mFaceEar2Left',
'mFaceEar1Right',
'mFaceEar2Right',
'mFaceJaw',
'mFaceTeethLower',
'mFaceTongueBase',
'mFaceTongueTip',
'mFaceTeethUpper',
'mWingsRoot',
'mWing1Left',
'mWing2Left',
'mWing3Left',
'mWing4Left',
'mWing4FanLeft',
'mWing1Right',
'mWing2Right',
'mWing3Right',
'mWing4Right',
'mWing4FanRight',
'mTail1',
'mTail2',
'mTail3',
'mTail4',
'mTail5',
'mTail6',
'mHindLimbsRoot',
'mHindLimb1Left',
'mHindLimb2Left',
'mHindLimb3Left',
'mHindLimb4Left',
'mHindLimb1Right',
'mHindLimb2Right',
'mHindLimb3Right',
'mHindLimb4Right',
'mHandMiddle1Left',
'mHandMiddle2Left',
'mHandMiddle3Left',
'mHandIndex1Left',
'mHandIndex2Left',
'mHandIndex3Left',
'mHandRing1Left',
'mHandRing2Left',
'mHandRing3Left',
'mHandPinky1Left',
'mHandPinky2Left',
'mHandPinky3Left',
'mHandThumb1Left',
'mHandThumb2Left',
'mHandThumb3Left',
'mHandMiddle1Right',
'mHandMiddle2Right',
'mHandMiddle3Right',
'mHandIndex1Right',
'mHandIndex2Right',
'mHandIndex3Right',
'mHandRing1Right',
'mHandRing2Right',
'mHandRing3Right',
'mHandPinky1Right',
'mHandPinky2Right',
'mHandPinky3Right',
'mHandThumb1Right',
'mHandThumb2Right',
'mHandThumb3Right',




'mCollarLeft',
'mShoulderLeft',
'mElbowLeft',
'mWristLeft',
'mCollarRight',
'mShoulderRight',
'mElbowRight',
'mWristRight',
'mHipRight',
'mKneeRight',
'mAnkleRight',
'mFootRight',
'mHipLeft',
'mKneeLeft',
'mAnkleLeft',
'mFootLeft',
]



safe_bones_DISABLED = [
'mFaceRoot',
'mFaceNoseBridge',
'mFaceEyeAltRight',
'mFaceEyeAltLeft',
'mFaceForeheadLeft',
'mFaceForeheadRight',
'mFaceEyebrowOuterLeft',
'mFaceEyebrowCenterLeft',
'mFaceEyebrowInnerLeft',
'mFaceEyebrowOuterRight',
'mFaceEyebrowCenterRight',
'mFaceEyebrowInnerRight',
'mFaceEyeLidUpperLeft',
'mFaceEyeLidLowerLeft',
'mFaceEyeLidUpperRight',
'mFaceEyeLidLowerRight',
'mFaceEar1Left',
'mFaceEar2Left',
'mFaceEar1Right',
'mFaceEar2Right',
'mFaceNoseLeft',
'mFaceNoseCenter',
'mFaceNoseRight',
'mFaceCheekLowerLeft',
'mFaceCheekUpperLeft',
'mFaceCheekLowerRight',
'mFaceCheekUpperRight',
'mFaceJaw',
'mFaceChin',
'mFaceTeethLower',
'mFaceLipLowerLeft',
'mFaceLipLowerRight',
'mFaceLipLowerCenter',
'mFaceTongueBase',
'mFaceTongueTip',
'mFaceJawShaper',
'mFaceForeheadCenter',
'mFaceNoseBase',
'mFaceTeethUpper',
'mFaceLipUpperLeft',
'mFaceLipUpperRight',
'mFaceLipCornerLeft',
'mFaceLipCornerRight',
'mFaceLipUpperCenter',
'mFaceEyecornerInnerLeft',
'mFaceEyecornerInnerRight',




'mWingsRoot',
'mWing1Left',
'mWing2Left',
'mWing3Left',
'mWing4Left',
'mWing4FanLeft',
'mWing1Right',
'mWing2Right',
'mWing3Right',
'mWing4Right',
'mWing4FanRight',


'mTail1',
'mTail2',
'mTail3',
'mTail4',
'mTail5',
'mTail6',


'mHindLimbsRoot',
'mHindLimb1Left',
'mHindLimb2Left',
'mHindLimb3Left',
'mHindLimb4Left',
'mHindLimb1Right',
'mHindLimb2Right',
'mHindLimb3Right',
'mHindLimb4Right',


'mHandMiddle1Left',
'mHandMiddle2Left',
'mHandMiddle3Left',
'mHandIndex1Left',
'mHandIndex2Left',
'mHandIndex3Left',
'mHandRing1Left',
'mHandRing2Left',
'mHandRing3Left',
'mHandPinky1Left',
'mHandPinky2Left',
'mHandPinky3Left',
'mHandThumb1Left',
'mHandThumb2Left',
'mHandThumb3Left',

'mHandMiddle1Right',
'mHandMiddle2Right',
'mHandMiddle3Right',
'mHandIndex1Right',
'mHandIndex2Right',
'mHandIndex3Right',
'mHandRing1Right',
'mHandRing2Right',
'mHandRing3Right',
'mHandPinky1Right',
'mHandPinky2Right',
'mHandPinky3Right',
'mHandThumb1Right',
'mHandThumb2Right',
'mHandThumb3Right',

'mTorso',
'mChest',
'mNeck',
'mHead',

'mCollarLeft',
'mShoulderLeft',
'mElbowLeft',
'mWristLeft',

'mCollarRight',
'mShoulderRight',
'mElbowRight',
'mWristRight',

'mHipRight',
'mKneeRight',
'mAnkleRight',
'mFootRight',
'mToeRight',
'mHipLeft',
'mKneeLeft',
'mAnkleLeft',
'mFootLeft',
'mToeLeft',

'mSkull',
'mEyeRight',
'mEyeLeft',
]








mBones = [
'mFaceRoot',
'mFaceNoseBridge',
'mFaceEyeAltRight',
'mFaceEyeAltLeft',
'mFaceForeheadLeft',
'mFaceForeheadRight',
'mFaceEyebrowOuterLeft',
'mFaceEyebrowCenterLeft',
'mFaceEyebrowInnerLeft',
'mFaceEyebrowOuterRight',
'mFaceEyebrowCenterRight',
'mFaceEyebrowInnerRight',
'mFaceEyeLidUpperLeft',
'mFaceEyeLidLowerLeft',
'mFaceEyeLidUpperRight',
'mFaceEyeLidLowerRight',
'mFaceEar1Left',
'mFaceEar2Left',
'mFaceEar1Right',
'mFaceEar2Right',
'mFaceNoseLeft',
'mFaceNoseCenter',
'mFaceNoseRight',
'mFaceCheekLowerLeft',
'mFaceCheekUpperLeft',
'mFaceCheekLowerRight',
'mFaceCheekUpperRight',
'mFaceJaw',
'mFaceChin',
'mFaceTeethLower',
'mFaceLipLowerLeft',
'mFaceLipLowerRight',
'mFaceLipLowerCenter',
'mFaceTongueBase',
'mFaceTongueTip',
'mFaceJawShaper',
'mFaceForeheadCenter',
'mFaceNoseBase',
'mFaceTeethUpper',
'mFaceLipUpperLeft',
'mFaceLipUpperRight',
'mFaceLipCornerLeft',
'mFaceLipCornerRight',
'mFaceLipUpperCenter',
'mFaceEyecornerInnerLeft',
'mFaceEyecornerInnerRight',




'mWingsRoot',
'mWing1Left',
'mWing2Left',
'mWing3Left',
'mWing4Left',
'mWing4FanLeft',
'mWing1Right',
'mWing2Right',
'mWing3Right',
'mWing4Right',
'mWing4FanRight',


'mTail1',
'mTail2',
'mTail3',
'mTail4',
'mTail5',
'mTail6',


'mHindLimbsRoot',
'mHindLimb1Left',
'mHindLimb2Left',
'mHindLimb3Left',
'mHindLimb4Left',
'mHindLimb1Right',
'mHindLimb2Right',
'mHindLimb3Right',
'mHindLimb4Right',


'mHandMiddle1Left',
'mHandMiddle2Left',
'mHandMiddle3Left',
'mHandIndex1Left',
'mHandIndex2Left',
'mHandIndex3Left',
'mHandRing1Left',
'mHandRing2Left',
'mHandRing3Left',
'mHandPinky1Left',
'mHandPinky2Left',
'mHandPinky3Left',
'mHandThumb1Left',
'mHandThumb2Left',
'mHandThumb3Left',

'mHandMiddle1Right',
'mHandMiddle2Right',
'mHandMiddle3Right',
'mHandIndex1Right',
'mHandIndex2Right',
'mHandIndex3Right',
'mHandRing1Right',
'mHandRing2Right',
'mHandRing3Right',
'mHandPinky1Right',
'mHandPinky2Right',
'mHandPinky3Right',
'mHandThumb1Right',
'mHandThumb2Right',
'mHandThumb3Right',

'mTorso',
'mChest',
'mNeck',
'mHead',

'mCollarLeft',
'mShoulderLeft',
'mElbowLeft',
'mWristLeft',

'mCollarRight',
'mShoulderRight',
'mElbowRight',
'mWristRight',

'mHipRight',
'mKneeRight',
'mAnkleRight',
'mFootRight',
'mToeRight',
'mHipLeft',
'mKneeLeft',
'mAnkleLeft',
'mFootLeft',
'mToeLeft',

'mSkull',
'mEyeRight',
'mEyeLeft',

]


mBonesHash = set()
for mBone in mBones:
    mBonesHash.add(mBone)







pBones = []
for bone in mBones:
    pBones.append(bone[1:])




vBones = [
'NECK',
'BELLY',
'PELVIS',
'CHEST',
'LEFT_PEC',
'RIGHT_PEC',
'HEAD',
'BUTT',
'UPPER_BACK',
'LOWER_BACK',
'L_CLAVICLE',
'R_CLAVICLE',
'L_UPPER_ARM',
'R_UPPER_ARM',
'L_LOWER_ARM',
'R_LOWER_ARM',
'LEFT_HANDLE',
'RIGHT_HANDLE',
'L_UPPER_LEG',
'R_UPPER_LEG',
'L_LOWER_LEG',
'R_LOWER_LEG',
'L_HAND',
'R_HAND',
'L_FOOT',
'R_FOOT'
]







hidden_bones = ['Spine1','Spine2','Spine3','Spine4', 'FaceRoot']






excluded_bones = ['HandThumb0Right','HandThumb0Left','HandIndex0Right','HandIndex0Left','HandMiddle0Right','HandMiddle0Left',
              'HandRing0Right','HandRing0Left','HandPinky0Right','HandPinky0Left','ThumbControllerRight','ThumbControllerLeft']


misc_bones = ['Origin','COG','PelvisInv']










all_mbones = [
'mPelvis',
'mSpine1',
'mSpine2',
'mSpine3',
'mSpine4',
'mTorso',
'mChest',
'mNeck',
'mHead',
'mSkull',
'mEyeRight',
'mEyeLeft',
'mFaceRoot',
'mFaceEyeAltRight',
'mFaceEyeAltLeft',
'mFaceForeheadLeft',
'mFaceForeheadRight',
'mFaceEyebrowOuterLeft',
'mFaceEyebrowCenterLeft',
'mFaceEyebrowInnerLeft',
'mFaceEyebrowOuterRight',
'mFaceEyebrowCenterRight',
'mFaceEyebrowInnerRight',
'mFaceEyeLidUpperLeft',
'mFaceEyeLidLowerLeft',
'mFaceEyeLidUpperRight',
'mFaceEyeLidLowerRight',
'mFaceEar1Left',
'mFaceEar2Left',
'mFaceEar1Right',
'mFaceEar2Right',
'mFaceNoseLeft',
'mFaceNoseCenter',
'mFaceNoseRight',
'mFaceCheekLowerLeft',
'mFaceCheekUpperLeft',
'mFaceCheekLowerRight',
'mFaceCheekUpperRight',
'mFaceJaw',
'mFaceChin',
'mFaceTeethLower',
'mFaceLipLowerLeft',
'mFaceLipLowerRight',
'mFaceLipLowerCenter',
'mFaceTongueBase',
'mFaceTongueTip',
'mFaceJawShaper',
'mFaceForeheadCenter',
'mFaceNoseBase',
'mFaceTeethUpper',
'mFaceLipUpperLeft',
'mFaceLipUpperRight',
'mFaceLipCornerLeft',
'mFaceLipCornerRight',
'mFaceLipUpperCenter',
'mFaceEyecornerInnerLeft',
'mFaceEyecornerInnerRight',
'mFaceNoseBridge',
'mCollarLeft',
'mShoulderLeft',
'mElbowLeft',
'mWristLeft',
'mHandMiddle1Left',
'mHandMiddle2Left',
'mHandMiddle3Left',
'mHandIndex1Left',
'mHandIndex2Left',
'mHandIndex3Left',
'mHandRing1Left',
'mHandRing2Left',
'mHandRing3Left',
'mHandPinky1Left',
'mHandPinky2Left',
'mHandPinky3Left',
'mHandThumb1Left',
'mHandThumb2Left',
'mHandThumb3Left',
'mCollarRight',
'mShoulderRight',
'mElbowRight',
'mWristRight',
'mHandMiddle1Right',
'mHandMiddle2Right',
'mHandMiddle3Right',
'mHandIndex1Right',
'mHandIndex2Right',
'mHandIndex3Right',
'mHandRing1Right',
'mHandRing2Right',
'mHandRing3Right',
'mHandPinky1Right',
'mHandPinky2Right',
'mHandPinky3Right',
'mHandThumb1Right',
'mHandThumb2Right',
'mHandThumb3Right',
'mWingsRoot',
'mWing1Left',
'mWing2Left',
'mWing3Left',
'mWing4Left',
'mWing4FanLeft',
'mWing1Right',
'mWing2Right',
'mWing3Right',
'mWing4Right',
'mWing4FanRight',
'mHipRight',
'mKneeRight',
'mAnkleRight',
'mFootRight',
'mToeRight',
'mHipLeft',
'mKneeLeft',
'mAnkleLeft',
'mFootLeft',
'mToeLeft',
'mTail1',
'mTail2',
'mTail3',
'mTail4',
'mTail5',
'mTail6',
'mGroin',
'mHindLimbsRoot',
'mHindLimb1Left',
'mHindLimb2Left',
'mHindLimb3Left',
'mHindLimb4Left',
'mHindLimb1Right',
'mHindLimb2Right',
'mHindLimb3Right',
'mHindLimb4Right',
'NECK',
'BELLY',
'PELVIS',
'CHEST',
'LEFT_PEC',
'RIGHT_PEC',
'HEAD',
'BUTT',
'UPPER_BACK',
'LOWER_BACK',
'L_CLAVICLE',
'R_CLAVICLE',
'L_UPPER_ARM',
'R_UPPER_ARM',
'L_LOWER_ARM',
'R_LOWER_ARM',
'LEFT_HANDLE',
'RIGHT_HANDLE',
'L_UPPER_LEG',
'R_UPPER_LEG',
'L_LOWER_LEG',
'R_LOWER_LEG',
'L_HAND',
'R_HAND',
'L_FOOT',
'R_FOOT'
]







all_pbones = [
'Pelvis',
'Spine1',
'Spine2',
'Spine3',
'Spine4',
'Torso',
'Chest',
'Neck',
'Head',
'Skull',
'EyeRight',
'EyeLeft',
'FaceRoot',
'FaceEyeAltRight',
'FaceEyeAltLeft',
'FaceForeheadLeft',
'FaceForeheadRight',
'FaceEyebrowOuterLeft',
'FaceEyebrowCenterLeft',
'FaceEyebrowInnerLeft',
'FaceEyebrowOuterRight',
'FaceEyebrowCenterRight',
'FaceEyebrowInnerRight',
'FaceEyeLidUpperLeft',
'FaceEyeLidLowerLeft',
'FaceEyeLidUpperRight',
'FaceEyeLidLowerRight',
'FaceEar1Left',
'FaceEar2Left',
'FaceEar1Right',
'FaceEar2Right',
'FaceNoseLeft',
'FaceNoseCenter',
'FaceNoseRight',
'FaceCheekLowerLeft',
'FaceCheekUpperLeft',
'FaceCheekLowerRight',
'FaceCheekUpperRight',
'FaceJaw',
'FaceChin',
'FaceTeethLower',
'FaceLipLowerLeft',
'FaceLipLowerRight',
'FaceLipLowerCenter',
'FaceTongueBase',
'FaceTongueTip',
'FaceJawShaper',
'FaceForeheadCenter',
'FaceNoseBase',
'FaceTeethUpper',
'FaceLipUpperLeft',
'FaceLipUpperRight',
'FaceLipCornerLeft',
'FaceLipCornerRight',
'FaceLipUpperCenter',
'FaceEyecornerInnerLeft',
'FaceEyecornerInnerRight',
'FaceNoseBridge',
'CollarLeft',
'ShoulderLeft',
'ElbowLeft',
'WristLeft',
'HandMiddle1Left',
'HandMiddle2Left',
'HandMiddle3Left',
'HandIndex1Left',
'HandIndex2Left',
'HandIndex3Left',
'HandRing1Left',
'HandRing2Left',
'HandRing3Left',
'HandPinky1Left',
'HandPinky2Left',
'HandPinky3Left',
'HandThumb1Left',
'HandThumb2Left',
'HandThumb3Left',
'CollarRight',
'ShoulderRight',
'ElbowRight',
'WristRight',
'HandMiddle1Right',
'HandMiddle2Right',
'HandMiddle3Right',
'HandIndex1Right',
'HandIndex2Right',
'HandIndex3Right',
'HandRing1Right',
'HandRing2Right',
'HandRing3Right',
'HandPinky1Right',
'HandPinky2Right',
'HandPinky3Right',
'HandThumb1Right',
'HandThumb2Right',
'HandThumb3Right',
'WingsRoot',
'Wing1Left',
'Wing2Left',
'Wing3Left',
'Wing4Left',
'Wing4FanLeft',
'Wing1Right',
'Wing2Right',
'Wing3Right',
'Wing4Right',
'Wing4FanRight',
'HipRight',
'KneeRight',
'AnkleRight',
'FootRight',
'ToeRight',
'HipLeft',
'KneeLeft',
'AnkleLeft',
'FootLeft',
'ToeLeft',
'Tail1',
'Tail2',
'Tail3',
'Tail4',
'Tail5',
'Tail6',
'Groin',
'HindLimbsRoot',
'HindLimb1Left',
'HindLimb2Left',
'HindLimb3Left',
'HindLimb4Left',
'HindLimb1Right',
'HindLimb2Right',
'HindLimb3Right',
'HindLimb4Right',
'NECK',
'BELLY',
'PELVIS',
'CHEST',
'LEFT_PEC',
'RIGHT_PEC',
'HEAD',
'BUTT',
'UPPER_BACK',
'LOWER_BACK',
'L_CLAVICLE',
'R_CLAVICLE',
'L_UPPER_ARM',
'R_UPPER_ARM',
'L_LOWER_ARM',
'R_LOWER_ARM',
'LEFT_HANDLE',
'RIGHT_HANDLE',
'L_UPPER_LEG',
'R_UPPER_LEG',
'L_LOWER_LEG',
'R_LOWER_LEG',
'L_HAND',
'R_HAND',
'L_FOOT',
'R_FOOT'
]





mbones_only = [
'mPelvis',
'mSpine1',
'mSpine2',
'mSpine3',
'mSpine4',
'mTorso',
'mChest',
'mNeck',
'mHead',
'mSkull',
'mEyeRight',
'mEyeLeft',
'mFaceRoot',
'mFaceEyeAltRight',
'mFaceEyeAltLeft',
'mFaceForeheadLeft',
'mFaceForeheadRight',
'mFaceEyebrowOuterLeft',
'mFaceEyebrowCenterLeft',
'mFaceEyebrowInnerLeft',
'mFaceEyebrowOuterRight',
'mFaceEyebrowCenterRight',
'mFaceEyebrowInnerRight',
'mFaceEyeLidUpperLeft',
'mFaceEyeLidLowerLeft',
'mFaceEyeLidUpperRight',
'mFaceEyeLidLowerRight',
'mFaceEar1Left',
'mFaceEar2Left',
'mFaceEar1Right',
'mFaceEar2Right',
'mFaceNoseLeft',
'mFaceNoseCenter',
'mFaceNoseRight',
'mFaceCheekLowerLeft',
'mFaceCheekUpperLeft',
'mFaceCheekLowerRight',
'mFaceCheekUpperRight',
'mFaceJaw',
'mFaceChin',
'mFaceTeethLower',
'mFaceLipLowerLeft',
'mFaceLipLowerRight',
'mFaceLipLowerCenter',
'mFaceTongueBase',
'mFaceTongueTip',
'mFaceJawShaper',
'mFaceForeheadCenter',
'mFaceNoseBase',
'mFaceTeethUpper',
'mFaceLipUpperLeft',
'mFaceLipUpperRight',
'mFaceLipCornerLeft',
'mFaceLipCornerRight',
'mFaceLipUpperCenter',
'mFaceEyecornerInnerLeft',
'mFaceEyecornerInnerRight',
'mFaceNoseBridge',
'mCollarLeft',
'mShoulderLeft',
'mElbowLeft',
'mWristLeft',
'mHandMiddle1Left',
'mHandMiddle2Left',
'mHandMiddle3Left',
'mHandIndex1Left',
'mHandIndex2Left',
'mHandIndex3Left',
'mHandRing1Left',
'mHandRing2Left',
'mHandRing3Left',
'mHandPinky1Left',
'mHandPinky2Left',
'mHandPinky3Left',
'mHandThumb1Left',
'mHandThumb2Left',
'mHandThumb3Left',
'mCollarRight',
'mShoulderRight',
'mElbowRight',
'mWristRight',
'mHandMiddle1Right',
'mHandMiddle2Right',
'mHandMiddle3Right',
'mHandIndex1Right',
'mHandIndex2Right',
'mHandIndex3Right',
'mHandRing1Right',
'mHandRing2Right',
'mHandRing3Right',
'mHandPinky1Right',
'mHandPinky2Right',
'mHandPinky3Right',
'mHandThumb1Right',
'mHandThumb2Right',
'mHandThumb3Right',
'mWingsRoot',
'mWing1Left',
'mWing2Left',
'mWing3Left',
'mWing4Left',
'mWing4FanLeft',
'mWing1Right',
'mWing2Right',
'mWing3Right',
'mWing4Right',
'mWing4FanRight',
'mHipRight',
'mKneeRight',
'mAnkleRight',
'mFootRight',
'mToeRight',
'mHipLeft',
'mKneeLeft',
'mAnkleLeft',
'mFootLeft',
'mToeLeft',
'mTail1',
'mTail2',
'mTail3',
'mTail4',
'mTail5',
'mTail6',
'mGroin',
'mHindLimbsRoot',
'mHindLimb1Left',
'mHindLimb2Left',
'mHindLimb3Left',
'mHindLimb4Left',
'mHindLimb1Right',
'mHindLimb2Right',
'mHindLimb3Right',
'mHindLimb4Right',
]
vbones_only = [
'NECK',
'BELLY',
'PELVIS',
'CHEST',
'LEFT_PEC',
'RIGHT_PEC',
'HEAD',
'BUTT',
'UPPER_BACK',
'LOWER_BACK',
'L_CLAVICLE',
'R_CLAVICLE',
'L_UPPER_ARM',
'R_UPPER_ARM',
'L_LOWER_ARM',
'R_LOWER_ARM',
'LEFT_HANDLE',
'RIGHT_HANDLE',
'L_UPPER_LEG',
'R_UPPER_LEG',
'L_LOWER_LEG',
'R_LOWER_LEG',
'L_HAND',
'R_HAND',
'L_FOOT',
'R_FOOT'
]


extended_bones = [
'Tail1',
'Tail2',
'Tail3',
'Tail4',
'Tail5',
'Tail6',
'Groin',
'HindLimbsRoot',
'HindLimb1Left',
'HindLimb2Left',
'HindLimb3Left',
'HindLimb4Left',
'HindLimb1Right',
'HindLimb2Right',
'HindLimb3Right',
'HindLimb4Right',
'WingsRoot',
'Wing1Left',
'Wing2Left',
'Wing3Left',
'Wing4Left',
'Wing4FanLeft',
'Wing1Right',
'Wing2Right',
'Wing3Right',
'Wing4Right',
'Wing4FanRight',
'Spine1',
'Spine2',
'Spine3',
'Spine4',
]

face_bones = [
'FaceRoot',
'FaceEyeAltRight',
'FaceEyeAltLeft',
'FaceForeheadLeft',
'FaceForeheadRight',
'FaceEyebrowOuterLeft',
'FaceEyebrowCenterLeft',
'FaceEyebrowInnerLeft',
'FaceEyebrowOuterRight',
'FaceEyebrowCenterRight',
'FaceEyebrowInnerRight',
'FaceEyeLidUpperLeft',
'FaceEyeLidLowerLeft',
'FaceEyeLidUpperRight',
'FaceEyeLidLowerRight',
'FaceEar1Left',
'FaceEar2Left',
'FaceEar1Right',
'FaceEar2Right',
'FaceNoseLeft',
'FaceNoseCenter',
'FaceNoseRight',
'FaceCheekLowerLeft',
'FaceCheekUpperLeft',
'FaceCheekLowerRight',
'FaceCheekUpperRight',
'FaceJaw',
'FaceChin',
'FaceTeethLower',
'FaceLipLowerLeft',
'FaceLipLowerRight',
'FaceLipLowerCenter',
'FaceTongueBase',
'FaceTongueTip',
'FaceJawShaper',
'FaceForeheadCenter',
'FaceNoseBase',
'FaceTeethUpper',
'FaceLipUpperLeft',
'FaceLipUpperRight',
'FaceLipCornerLeft',
'FaceLipCornerRight',
'FaceLipUpperCenter',
'FaceEyecornerInnerLeft',
'FaceEyecornerInnerRight',
'FaceNoseBridge',
]
hand_bones = [
'HandMiddle1Left',
'HandMiddle2Left',
'HandMiddle3Left',
'HandIndex1Left',
'HandIndex2Left',
'HandIndex3Left',
'HandRing1Left',
'HandRing2Left',
'HandRing3Left',
'HandPinky1Left',
'HandPinky2Left',
'HandPinky3Left',
'HandThumb1Left',
'HandThumb2Left',
'HandThumb3Left',
'HandMiddle1Right',
'HandMiddle2Right',
'HandMiddle3Right',
'HandIndex1Right',
'HandIndex2Right',
'HandIndex3Right',
'HandRing1Right',
'HandRing2Right',
'HandRing3Right',
'HandPinky1Right',
'HandPinky2Right',
'HandPinky3Right',
'HandThumb1Right',
'HandThumb2Right',
'HandThumb3Right',
]

face_mbones = [
'mFaceRoot',
'mFaceEyeAltRight',
'mFaceEyeAltLeft',
'mFaceForeheadLeft',
'mFaceForeheadRight',
'mFaceEyebrowOuterLeft',
'mFaceEyebrowCenterLeft',
'mFaceEyebrowInnerLeft',
'mFaceEyebrowOuterRight',
'mFaceEyebrowCenterRight',
'mFaceEyebrowInnerRight',
'mFaceEyeLidUpperLeft',
'mFaceEyeLidLowerLeft',
'mFaceEyeLidUpperRight',
'mFaceEyeLidLowerRight',
'mFaceEar1Left',
'mFaceEar1Right',
'mFaceNoseLeft',
'mFaceNoseCenter',
'mFaceNoseRight',
'mFaceCheekLowerLeft',
'mFaceCheekUpperLeft',
'mFaceCheekLowerRight',
'mFaceCheekUpperRight',
'mFaceJaw',
'mFaceJawShaper',
'mFaceForeheadCenter',
'mFaceNoseBase',
'mFaceTeethUpper',
'mFaceEyecornerInnerLeft',
'mFaceEyecornerInnerRight',
'mFaceNoseBridge',
'mFaceEar2Left',
'mFaceEar2Right',
'mFaceChin',
'mFaceTeethLower',
'mFaceLipUpperLeft',
'mFaceLipUpperRight',
'mFaceLipCornerLeft',
'mFaceLipCornerRight',
'mFaceLipUpperCenter',
'mFaceLipLowerLeft',
'mFaceLipLowerRight',
'mFaceLipLowerCenter',
'mFaceTongueBase',
'mFaceTongueTip',
]

face_mbone_connections = {
    "mFaceEar2Left": "mFaceEar1Left",
    "mFaceEar2Right": "mFaceEar1Right",
    "mFaceTongueTip": "mFaceTongueBase",
    }




bvh_names = {
    'mPelvis': 'hip',
    'mTorso': 'abdomen',
    'mChest': 'chest',
    'mNeck': 'neck',
    'mHead': 'head',
    'mSkull': 'figureHair',
    'mCollarLeft': 'lCollar',
    'mShoulderLeft': 'lShldr',
    'mElbowLeft': 'lForeArm',
    'mWristLeft': 'lHand',
    'mCollarRight': 'rCollar',
    'mShoulderRight': 'rShldr',
    'mElbowRight': 'rForeArm',
    'mWristRight': 'rHand',
    'mHipRight': 'rThigh',
    'mKneeRight': 'rShin',
    'mAnkleRight': 'rFoot',
    'mHipLeft': 'lThigh',
    'mKneeLeft': 'lShin',
    'mAnkleLeft': 'lFoot'
    }

bvh_names_rev = {}
for m in bvh_names:
    a = bvh_names[m]
    bvh_names_rev[a] = m
















mbones_map = {}

pbones_map = {}

cr_bones_map = {}
cr_bones_hash = {}
for mBone, pBone in zip(all_mbones, all_pbones):
    mbones_map[mBone] = pBone
    pbones_map[pBone] = mBone
    cr_bones_map[mBone] = "bb_" + pBone
    cr_bones_hash["bb_" + pBone] = mBone













layers_visible = [0,1,2,3,8,9,10,11,12,13,14,15]
layers_extra = [6,7,16,22,24,25,27,26,28,29,30]



layers_ik = [17,18,19]

























bento_buddy_group_name = 'Bento Buddy Proxy'    
pose_bones_group_name = 'BB Base Bones'  
mbones_group_name = 'New mBone Group'           
unused_bones_group_name = 'Bone Bucket'         
excluded_bones_group_name = 'Excluded Bones'    
problem_bones_group_name = 'Problem Bones'      
misc_bones_group_name = 'Misc Bones'            
vbones_group_name = 'BB Volume Bones'              
ref_mbones_group_name = 'BB Ref mBones'
ref_vbones_group_name = 'BB Ref vBones'
cr_mbones_group_name = 'BB Control mBones'       
cr_vbones_group_name = 'BB Control vBones'



cc_rename_group = "Rename Bones"
cc_reskin_group = "Reskin Bones"



bb_target_group = "Retarget Bones"
bb_source_group = "Source Bones"




rig_group_mbones = "mBones"
rig_group_vbones = "vBones"
rig_group_abones = "aBones"
rig_group_mtheme = 'THEME04'
rig_group_vtheme = 'THEME10'
rig_group_atheme = 'THEME09'


rig_group_nbones = "nBones"
rig_group_ntheme = 'THEME01'







bb_all_bones_layer = 0


bb_base_layer = 0



bb_vbones_layer = 1

bb_mbones_layer = 2


cr_mbones_theme = 'THEME08'
cr_vbones_theme = 'THEME05'
bento_buddy_theme = 'THEME04'
pose_bone_theme = 'THEME02'
mbone_theme = 'THEME03'
unused_bone_theme = 'THEME09'
excluded_bone_theme = 'THEME20'
problem_bone_theme = 'THEME01'
misc_bone_theme = 'THEME13'
vbone_theme = 'THEME10'
ref_mbones_theme = 'THEME12'
ref_vbones_theme = 'THEME14'


cc_rename_theme = 'THEME01'
cc_reskin_theme = 'THEME09'




cc_rename_selected_name = "Rename Anchor"
cc_reskin_selected_name = "Reskin Children"

cc_rename_selected_color = 'THEME10'
cc_reskin_selected_color = 'THEME03'


bb_source_theme = 'THEME09'
bb_target_theme = 'THEME03'


fly_paper_group_name = "Fly Paper"
fly_paper_theme = 'THEME09'


glue_group_name = "Deformer"
glue_theme = 'THEME07'

slave_group_name = "slave"
slave_group_theme = 'THEME07'


mixer_group_target_active_name = "active"
mixer_group_target_active_theme = 'THEME08'
mixer_group_target_inactive_name = "Inactive"
mixer_group_target_inactive_theme = 'THEME09'

mixer_group_source_active_name = "active"
mixer_group_source_active_theme = 'THEME03'
mixer_group_source_inactive_name = "Inactive"
mixer_group_source_inactive_theme = 'THEME01'



onemap_group_rename_name = "Rename"
onemap_group_rename_color = 'THEME01'
onemap_group_reskin_name = "Reskin"
onemap_group_reskin_color = 'THEME09'
onemap_group_anchor_name = "Anchor"
onemap_group_anchor_color = 'THEME10'
onemap_group_branch_name = "Branch"
onemap_group_branch_color = 'THEME03'


priority_groups = {
    "0": {
        "normal": (1, 0, 0),
        "select": (0.509804, 0.901961, 0.145098),
        "active": (0.109804, 0.627451, 0.878431),
    },
    "1": {
        "normal": (1, 0.478431, 0),
        "select": (0.509804, 0.901961, 0.145098),
        "active": (0.109804, 0.627451, 0.878431),
    },
    "2": {
        "normal": (0.984314, 1, 0),
        "select": (0.509804, 0.901961, 0.145098),
        "active": (0.109804, 0.627451, 0.878431),
    },
    "3": {
        "normal": (0.290196, 1, 0),
        "select": (0.509804, 0.901961, 0.145098),
        "active": (0.109804, 0.627451, 0.878431),
    },
    "4": {
        "normal": (0, 1, 0.909804),
        "select": (0.509804, 0.901961, 0.145098),
        "active": (0.109804, 0.627451, 0.878431),
    },
    "5": {
        "normal": (0.976471, 0.584314, 1),
        "select": (0.509804, 0.901961, 0.145098),
        "active": (0.109804, 0.627451, 0.878431),
    },
    "6": {
        "normal": (0.737255, 0, 1),
        "select": (0.509804, 0.901961, 0.145098),
        "active": (0.109804, 0.627451, 0.878431),
    },
}













dynamic_properties = {"trigger_start": True}







    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    




vol_joints = dict()
vol_joints['BELLY'] = {}
vol_joints['BELLY']['scale'] = [0.09, 0.13, 0.15]
vol_joints['PELVIS'] = {}
vol_joints['PELVIS']['scale'] = [0.12, 0.16, 0.17]
vol_joints['CHEST'] = {}
vol_joints['CHEST']['scale'] = [0.11, 0.15, 0.2]
vol_joints['UPPER_BACK'] = {}
vol_joints['UPPER_BACK']['scale'] = [0.09, 0.13, 0.15]
vol_joints['LEFT_PEC'] = {}
vol_joints['LEFT_PEC']['scale'] = [0.05, 0.05, 0.05]
vol_joints['RIGHT_PEC'] = {}
vol_joints['RIGHT_PEC']['scale'] = [0.05, 0.05, 0.05]
vol_joints['HEAD'] = {}
vol_joints['HEAD']['scale'] = [0.11, 0.09, 0.12]
vol_joints['NECK'] = {}
vol_joints['NECK']['scale'] = [0.05, 0.06, 0.08]
vol_joints['BUTT'] = {}
vol_joints['BUTT']['scale'] = [0.1, 0.1, 0.1]
vol_joints['LOWER_BACK'] = {}
vol_joints['LOWER_BACK']['scale'] = [0.09, 0.13, 0.15]
vol_joints['L_CLAVICLE'] = {}
vol_joints['L_CLAVICLE']['scale'] = [0.07, 0.14, 0.05]
vol_joints['R_CLAVICLE'] = {}
vol_joints['R_CLAVICLE']['scale'] = [0.07, 0.14, 0.05]
vol_joints['L_UPPER_ARM'] = {}
vol_joints['L_UPPER_ARM']['scale'] = [0.05, 0.17, 0.05]
vol_joints['R_UPPER_ARM'] = {}
vol_joints['R_UPPER_ARM']['scale'] = [0.05, 0.17, 0.05]
vol_joints['L_LOWER_ARM'] = {}
vol_joints['L_LOWER_ARM']['scale'] = [0.04, 0.14, 0.04]
vol_joints['R_LOWER_ARM'] = {}
vol_joints['R_LOWER_ARM']['scale'] = [0.04, 0.14, 0.04]
vol_joints['LEFT_HANDLE'] = {}
vol_joints['LEFT_HANDLE']['scale'] = [0.05, 0.05, 0.05]
vol_joints['RIGHT_HANDLE'] = {}
vol_joints['RIGHT_HANDLE']['scale'] = [0.05, 0.05, 0.05]
vol_joints['L_UPPER_LEG'] = {}
vol_joints['L_UPPER_LEG']['scale'] = [0.09, 0.09, 0.32]
vol_joints['R_UPPER_LEG'] = {}
vol_joints['R_UPPER_LEG']['scale'] = [0.09, 0.09, 0.32]
vol_joints['L_LOWER_LEG'] = {}
vol_joints['L_LOWER_LEG']['scale'] = [0.06, 0.06, 0.25]
vol_joints['R_LOWER_LEG'] = {}
vol_joints['R_LOWER_LEG']['scale'] = [0.06, 0.06, 0.25]
vol_joints['L_HAND'] = {}
vol_joints['L_HAND']['scale'] = [0.05, 0.08, 0.03]
vol_joints['R_HAND'] = {}
vol_joints['R_HAND']['scale'] = [0.05, 0.08, 0.03]
vol_joints['L_FOOT'] = {}
vol_joints['L_FOOT']['scale'] = [0.13, 0.05, 0.05]
vol_joints['R_FOOT'] = {}
vol_joints['R_FOOT']['scale'] = [0.13, 0.05, 0.05]






mbones_to_fitmesh = {
    "mHead": "HEAD",
    "mNeck": "NECK",
    "mCollarLeft": "L_CLAVICLE",
    "mCollarRight": "R_CLAVICLE",
    "mShoulderLeft": "L_UPPER_ARM",
    "mShoulderRight": "R_UPPER_ARM",
    "mElbowLeft": "L_LOWER_ARM",
    "mElbowRight": "R_LOWER_ARM",
    "mHipLeft": "L_UPPER_LEG",
    "mHipRight": "R_UPPER_LEG",
    "mKneeLeft": "L_LOWER_LEG",
    "mKneeRight": "R_LOWER_LEG",
    "mWristLeft": "L_HAND",
    "mWristRight": "R_HAND",
    "mAnkleLeft": "L_FOOT",
    "mAnkleRight": "R_FOOT",
    }

mbones_to_fitmesh_rev = {}
for m in mbones_to_fitmesh:
    f = mbones_to_fitmesh[m]
    mbones_to_fitmesh_rev[f] = m





pbone_map = {
    "Wing3Left": "mWing3Left",
    "FaceEyeLidUpperLeft": "mFaceEyeLidUpperLeft",
    "Wing1Left": "mWing1Left",
    "WristLeft": "mWristLeft",
    "FaceNoseBridge": "mFaceNoseBridge",
    "R_HAND": "R_HAND",
    "FaceLipUpperLeft": "mFaceLipUpperLeft",
    "HandRing1Left": "mHandRing1Left",
    "Wing1Right": "mWing1Right",
    "HandRing2Right": "mHandRing2Right",
    "AnkleRight": "mAnkleRight",
    "FaceRoot": "mFaceRoot",
    "RIGHT_HANDLE": "RIGHT_HANDLE",
    "FaceEar2Right": "mFaceEar2Right",
    "HandRing3Left": "mHandRing3Left",
    "L_HAND": "L_HAND",
    "KneeRight": "mKneeRight",
    "Tail5": "mTail5",
    "L_UPPER_ARM": "L_UPPER_ARM",
    "FaceForeheadCenter": "mFaceForeheadCenter",
    "HindLimb1Right": "mHindLimb1Right",
    "AnkleLeft": "mAnkleLeft",
    "FaceEyeAltRight": "mFaceEyeAltRight",
    "FaceNoseBase": "mFaceNoseBase",
    "LOWER_BACK": "LOWER_BACK",
    "FaceCheekLowerRight": "mFaceCheekLowerRight",
    "ShoulderLeft": "mShoulderLeft",
    "HandRing2Left": "mHandRing2Left",
    "Wing4Right": "mWing4Right",
    "HandMiddle1Right": "mHandMiddle1Right",
    "BUTT": "BUTT",
    "FaceJawShaper": "mFaceJawShaper",
    "HandPinky3Right": "mHandPinky3Right",
    "LEFT_PEC": "LEFT_PEC",
    "CHEST": "CHEST",
    "HandIndex1Left": "mHandIndex1Left",
    "HindLimb4Left": "mHindLimb4Left",
    "FaceLipCornerRight": "mFaceLipCornerRight",
    "R_UPPER_LEG": "R_UPPER_LEG",
    "HindLimb3Right": "mHindLimb3Right",
    "HandPinky3Left": "mHandPinky3Left",
    "NECK": "NECK",
    "ShoulderRight": "mShoulderRight",
    "HEAD": "HEAD",
    "Skull": "mSkull",
    "Tail4": "mTail4",
    "R_FOOT": "R_FOOT",
    "Groin": "mGroin",
    "FaceCheekUpperLeft": "mFaceCheekUpperLeft",
    "FaceTongueTip": "mFaceTongueTip",
    "FaceEyeLidUpperRight": "mFaceEyeLidUpperRight",
    "HandRing3Right": "mHandRing3Right",
    "FaceEyeLidLowerRight": "mFaceEyeLidLowerRight",
    "Wing4FanLeft": "mWing4FanLeft",
    "HindLimb3Left": "mHindLimb3Left",
    "R_CLAVICLE": "R_CLAVICLE",
    "HandIndex2Right": "mHandIndex2Right",
    "FootLeft": "mFootLeft",
    "Wing3Right": "mWing3Right",
    "EyeLeft": "mEyeLeft",
    "HandMiddle3Right": "mHandMiddle3Right",
    "Pelvis": "mPelvis",
    "FaceLipLowerCenter": "mFaceLipLowerCenter",
    "HandThumb3Left": "mHandThumb3Left",
    "FaceEyecornerInnerLeft": "mFaceEyecornerInnerLeft",
    "HandPinky2Left": "mHandPinky2Left",
    "Wing2Left": "mWing2Left",
    "HindLimb4Right": "mHindLimb4Right",
    "FaceNoseRight": "mFaceNoseRight",
    "UPPER_BACK": "UPPER_BACK",
    "HandPinky1Right": "mHandPinky1Right",
    "HandThumb1Right": "mHandThumb1Right",
    "EyeRight": "mEyeRight",
    "FaceEar2Left": "mFaceEar2Left",
    "Tail3": "mTail3",
    "LEFT_HANDLE": "LEFT_HANDLE",
    "CollarLeft": "mCollarLeft",
    "Torso": "mTorso",
    "FaceLipLowerLeft": "mFaceLipLowerLeft",
    "HandIndex2Left": "mHandIndex2Left",
    "FaceEyebrowInnerRight": "mFaceEyebrowInnerRight",
    "Wing2Right": "mWing2Right",
    "FaceNoseLeft": "mFaceNoseLeft",
    "FaceEyebrowOuterRight": "mFaceEyebrowOuterRight",
    "KneeLeft": "mKneeLeft",
    "FaceLipLowerRight": "mFaceLipLowerRight",
    "FaceEyeLidLowerLeft": "mFaceEyeLidLowerLeft",
    "FaceEar1Right": "mFaceEar1Right",
    "HandPinky1Left": "mHandPinky1Left",
    "HipLeft": "mHipLeft",
    "HindLimb2Right": "mHindLimb2Right",
    "Tail6": "mTail6",
    "FaceEar1Left": "mFaceEar1Left",
    "HandThumb2Right": "mHandThumb2Right",
    "Spine2": "mSpine2",
    "Spine4": "mSpine4",
    "FaceCheekUpperRight": "mFaceCheekUpperRight",
    "WingsRoot": "mWingsRoot",
    "FaceNoseCenter": "mFaceNoseCenter",
    "FaceJaw": "mFaceJaw",
    "FaceLipUpperRight": "mFaceLipUpperRight",
    "HandMiddle3Left": "mHandMiddle3Left",
    "HandMiddle2Right": "mHandMiddle2Right",
    "ElbowRight": "mElbowRight",
    "L_FOOT": "L_FOOT",
    "R_UPPER_ARM": "R_UPPER_ARM",
    "FaceEyebrowOuterLeft": "mFaceEyebrowOuterLeft",
    "HindLimb2Left": "mHindLimb2Left",
    "HandMiddle2Left": "mHandMiddle2Left",
    "Tail1": "mTail1",
    "R_LOWER_ARM": "R_LOWER_ARM",
    "HandIndex3Right": "mHandIndex3Right",
    "FaceCheekLowerLeft": "mFaceCheekLowerLeft",
    "HandThumb2Left": "mHandThumb2Left",
    "FootRight": "mFootRight",
    "ToeRight": "mToeRight",
    "Tail2": "mTail2",
    "L_CLAVICLE": "L_CLAVICLE",
    "FaceForeheadRight": "mFaceForeheadRight",
    "HandRing1Right": "mHandRing1Right",
    "Spine3": "mSpine3",
    "HandThumb3Right": "mHandThumb3Right",
    "FaceTeethUpper": "mFaceTeethUpper",
    "PELVIS": "PELVIS",
    "RIGHT_PEC": "RIGHT_PEC",
    "FaceEyebrowCenterRight": "mFaceEyebrowCenterRight",
    "FaceLipUpperCenter": "mFaceLipUpperCenter",
    "ElbowLeft": "mElbowLeft",
    "L_LOWER_ARM": "L_LOWER_ARM",
    "HandIndex3Left": "mHandIndex3Left",
    "FaceEyeAltLeft": "mFaceEyeAltLeft",
    "WristRight": "mWristRight",
    "HandPinky2Right": "mHandPinky2Right",
    "HandMiddle1Left": "mHandMiddle1Left",
    "CollarRight": "mCollarRight",
    "ToeLeft": "mToeLeft",
    "Wing4Left": "mWing4Left",
    "HandThumb1Left": "mHandThumb1Left",
    "Chest": "mChest",
    "L_LOWER_LEG": "L_LOWER_LEG",
    "R_LOWER_LEG": "R_LOWER_LEG",
    "FaceEyebrowInnerLeft": "mFaceEyebrowInnerLeft",
    "Head": "mHead",
    "FaceTeethLower": "mFaceTeethLower",
    "BELLY": "BELLY",
    "L_UPPER_LEG": "L_UPPER_LEG",
    "FaceForeheadLeft": "mFaceForeheadLeft",
    "HandIndex1Right": "mHandIndex1Right",
    "HindLimb1Left": "mHindLimb1Left",
    "FaceChin": "mFaceChin",
    "HipRight": "mHipRight",
    "FaceTongueBase": "mFaceTongueBase",
    "Neck": "mNeck",
    "FaceLipCornerLeft": "mFaceLipCornerLeft",
    "FaceEyebrowCenterLeft": "mFaceEyebrowCenterLeft",
    "Spine1": "mSpine1",
    "HindLimbsRoot": "mHindLimbsRoot",
    "Wing4FanRight": "mWing4FanRight",
    "FaceEyecornerInnerRight": "mFaceEyecornerInnerRight",
    "COG": "mPelvis",
    "PelvisInv": "mPelvis",
    }










pelvis_names = {"mpelvis", "avatar_mPelvis", "hip", "hips"}









