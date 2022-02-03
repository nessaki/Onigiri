# This is an example template file, it works, but make your own.
# This will be loaded into the text area for you to change, and save
# as a different file.
#
# --------------------------------------------------------------------------------------------
# This is a python file, you do not need to know how to program.  Just move the names around
# in the order in which you want them to be used.  The "problem_bones" do not get used so
# the order for those do not matter.
# --------------------------------------------------------------------------------------------
#
# This is for the auto mapping to get things done quickly.  From there you can
# test various bone associations using a template.  This file restructures the
# internal data in the order that you prefer.  The way it works is that the first
# bone will go to the root/pelvis of the target skeleton and work its way down
# the chain.  The order is not guaranteed since we'll never know, at first, which
# bones come next if there are more than one child per parent bone.  These are
# in some index order from when your target skeleton was created.
#
# You'll notice this comment, you should notice how it starts.
# Everything after the # is considered a comment and is ignored by Bento Buddy.
# The following are containers for the items that you wish to rearrange.
# The items in the containers are enclosed with single quotes ('), although you
# can use double quotes ("), and the quoted name ends with a comma.
#
# Problem bones are excluded from use.  If you find that your character doesn't work
# properly with some bones you can put their names in here and remove them from mBones
# to quickly prototype your end result.  Note that this problem is mostly associated
# with a combination of bones and not the bones themselves.  For instance, you may find
# that mHead doesn't like to be used in your rig because its parent is still in the
# bone bucket, not being used.  Bento Buddy allows you to quickly prototype, without
# having to redo your animations each time.  The bones below are a suggestion because
# of my experience with problem rigs I know that these usually clear it up if added to
# problem_bones.  You can also put volume bones here (vBones) if they are giving you grief.

# You'll notice that mPelvis is here, it's not a problem bone particularly, but it's
# a bone that you want to have exclusive control over.  You will keyframe this later when
# you need to.

problem_bones = [
]

# This is part of the bone bucket.  This container should not have any of the bones that are listed
# inside of problem_bones.  I do a preliminary check to pull them out of this container but if
# you put them here, or keep them here, you will misunderstand what is happening.  This container
# is a list of names that are allowed to be used for your target rigs, your character.  This does
# not contain the volume bones, which are also usable, and is in the last section.  Volume bones
# should not pose a problem so are not typically listed inside the problem_bones container.

problem_bones = [
# Pelvis is not selectable, but viewable.  It probably should not be translated down to mPelvis, there's
# another bone for that, not sure which.
#
# Possile candidates for exclusion are Pelvis, COG, Origin and PelvisInv, which are in the
# Look into EyeLeft, EyeRight and also mSpine?

'mPelvis',

]

# Mapping from pBones to mBones, the mbones is the Avastar bone wit the "m".

# This new array has all the bones, and after it are the volume bones which I'll test with later on.
# Turns out there's no realy problem with using all of the bones, I think I just needed to key all of
# them and/or make sure they were all moved somewhere.  I tested it on a Character Creator 3 model.
# It worked and so did the test animation.
mBones = [
'mGroin',
'mSpine1',
'mSpine2',
'mSpine3',
'mSpine4',
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

# spines go here

# wings go here
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

# tail goes here
'mTail1',
'mTail2',
'mTail3',
'mTail4',
'mTail5',
'mTail6',

# hinds go here
'mHindLimbsRoot',
'mHindLimb1Left',
'mHindLimb2Left',
'mHindLimb3Left',
'mHindLimb4Left',
'mHindLimb1Right',
'mHindLimb2Right',
'mHindLimb3Right',
'mHindLimb4Right',

# fingers go here, no wrists
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

# Volume bones, of course.
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
