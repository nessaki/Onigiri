
sl_rig = {
    "mPelvis": {
        "parent": "",
        "children": [
            "PELVIS",
            "BUTT",
            "mSpine1",
            "mHipRight",
            "mHipLeft",
            "mTail1",
            "mGroin",
            "mHindLimbsRoot",
        ],
    },
    "PELVIS": {
        "parent": "mPelvis",
        "children": [
        ],
    },
    "BUTT": {
        "parent": "mPelvis",
        "children": [
        ],
    },
    "mSpine1": {
        "parent": "mPelvis",
        "children": [
            "mSpine2",
        ],
    },
    "mSpine2": {
        "parent": "mSpine1",
        "children": [
            "mTorso",
        ],
    },
    "mTorso": {
        "parent": "mSpine2",
        "children": [
            "BELLY",
            "LEFT_HANDLE",
            "RIGHT_HANDLE",
            "LOWER_BACK",
            "mSpine3",
        ],
    },
    "BELLY": {
        "parent": "mTorso",
        "children": [
        ],
    },
    "LEFT_HANDLE": {
        "parent": "mTorso",
        "children": [
        ],
    },
    "RIGHT_HANDLE": {
        "parent": "mTorso",
        "children": [
        ],
    },
    "LOWER_BACK": {
        "parent": "mTorso",
        "children": [
        ],
    },
    "mSpine3": {
        "parent": "mTorso",
        "children": [
            "mSpine4",
        ],
    },
    "mSpine4": {
        "parent": "mSpine3",
        "children": [
            "mChest",
        ],
    },
    "mChest": {
        "parent": "mSpine4",
        "children": [
            "CHEST",
            "LEFT_PEC",
            "RIGHT_PEC",
            "UPPER_BACK",
            "mNeck",
            "mCollarLeft",
            "mCollarRight",
            "mWingsRoot",
        ],
    },
    "CHEST": {
        "parent": "mChest",
        "children": [
        ],
    },
    "LEFT_PEC": {
        "parent": "mChest",
        "children": [
        ],
    },
    "RIGHT_PEC": {
        "parent": "mChest",
        "children": [
        ],
    },
    "UPPER_BACK": {
        "parent": "mChest",
        "children": [
        ],
    },
    "mNeck": {
        "parent": "mChest",
        "children": [
            "NECK",
            "mHead",
        ],
    },
    "NECK": {
        "parent": "mNeck",
        "children": [
        ],
    },
    "mHead": {
        "parent": "mNeck",
        "children": [
            "HEAD",
            "mSkull",
            "mEyeRight",
            "mEyeLeft",
            "mFaceRoot",
        ],
    },
    "HEAD": {
        "parent": "mHead",
        "children": [
        ],
    },
    "mSkull": {
        "parent": "mHead",
        "children": [
        ],
    },
    "mEyeRight": {
        "parent": "mHead",
        "children": [
        ],
    },
    "mEyeLeft": {
        "parent": "mHead",
        "children": [
        ],
    },
    "mFaceRoot": {
        "parent": "mHead",
        "children": [
            "mFaceEyeAltRight",
            "mFaceEyeAltLeft",
            "mFaceForeheadLeft",
            "mFaceForeheadRight",
            "mFaceEyebrowOuterLeft",
            "mFaceEyebrowCenterLeft",
            "mFaceEyebrowInnerLeft",
            "mFaceEyebrowOuterRight",
            "mFaceEyebrowCenterRight",
            "mFaceEyebrowInnerRight",
            "mFaceEyeLidUpperLeft",
            "mFaceEyeLidLowerLeft",
            "mFaceEyeLidUpperRight",
            "mFaceEyeLidLowerRight",
            "mFaceEar1Left",
            "mFaceEar1Right",
            "mFaceNoseLeft",
            "mFaceNoseCenter",
            "mFaceNoseRight",
            "mFaceCheekLowerLeft",
            "mFaceCheekUpperLeft",
            "mFaceCheekLowerRight",
            "mFaceCheekUpperRight",
            "mFaceJaw",
            "mFaceJawShaper",
            "mFaceForeheadCenter",
            "mFaceNoseBase",
            "mFaceTeethUpper",
            "mFaceEyecornerInnerLeft",
            "mFaceEyecornerInnerRight",
            "mFaceNoseBridge",
        ],
    },
    "mFaceEyeAltRight": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceEyeAltLeft": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceForeheadLeft": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceForeheadRight": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceEyebrowOuterLeft": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceEyebrowCenterLeft": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceEyebrowInnerLeft": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceEyebrowOuterRight": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceEyebrowCenterRight": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceEyebrowInnerRight": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceEyeLidUpperLeft": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceEyeLidLowerLeft": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceEyeLidUpperRight": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceEyeLidLowerRight": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceEar1Left": {
        "parent": "mFaceRoot",
        "children": [
            "mFaceEar2Left",
        ],
    },
    "mFaceEar2Left": {
        "parent": "mFaceEar1Left",
        "children": [
        ],
    },
    "mFaceEar1Right": {
        "parent": "mFaceRoot",
        "children": [
            "mFaceEar2Right",
        ],
    },
    "mFaceEar2Right": {
        "parent": "mFaceEar1Right",
        "children": [
        ],
    },
    "mFaceNoseLeft": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceNoseCenter": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceNoseRight": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceCheekLowerLeft": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceCheekUpperLeft": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceCheekLowerRight": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceCheekUpperRight": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceJaw": {
        "parent": "mFaceRoot",
        "children": [
            "mFaceChin",
            "mFaceTeethLower",
        ],
    },
    "mFaceChin": {
        "parent": "mFaceJaw",
        "children": [
        ],
    },
    "mFaceTeethLower": {
        "parent": "mFaceJaw",
        "children": [
            "mFaceLipLowerLeft",
            "mFaceLipLowerRight",
            "mFaceLipLowerCenter",
            "mFaceTongueBase",
        ],
    },
    "mFaceLipLowerLeft": {
        "parent": "mFaceTeethLower",
        "children": [
        ],
    },
    "mFaceLipLowerRight": {
        "parent": "mFaceTeethLower",
        "children": [
        ],
    },
    "mFaceLipLowerCenter": {
        "parent": "mFaceTeethLower",
        "children": [
        ],
    },
    "mFaceTongueBase": {
        "parent": "mFaceTeethLower",
        "children": [
            "mFaceTongueTip",
        ],
    },
    "mFaceTongueTip": {
        "parent": "mFaceTongueBase",
        "children": [
        ],
    },
    "mFaceJawShaper": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceForeheadCenter": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceNoseBase": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceTeethUpper": {
        "parent": "mFaceRoot",
        "children": [
            "mFaceLipUpperLeft",
            "mFaceLipUpperRight",
            "mFaceLipCornerLeft",
            "mFaceLipCornerRight",
            "mFaceLipUpperCenter",
        ],
    },
    "mFaceLipUpperLeft": {
        "parent": "mFaceTeethUpper",
        "children": [
        ],
    },
    "mFaceLipUpperRight": {
        "parent": "mFaceTeethUpper",
        "children": [
        ],
    },
    "mFaceLipCornerLeft": {
        "parent": "mFaceTeethUpper",
        "children": [
        ],
    },
    "mFaceLipCornerRight": {
        "parent": "mFaceTeethUpper",
        "children": [
        ],
    },
    "mFaceLipUpperCenter": {
        "parent": "mFaceTeethUpper",
        "children": [
        ],
    },
    "mFaceEyecornerInnerLeft": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceEyecornerInnerRight": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mFaceNoseBridge": {
        "parent": "mFaceRoot",
        "children": [
        ],
    },
    "mCollarLeft": {
        "parent": "mChest",
        "children": [
            "L_CLAVICLE",
            "mShoulderLeft",
        ],
    },
    "L_CLAVICLE": {
        "parent": "mCollarLeft",
        "children": [
        ],
    },
    "mShoulderLeft": {
        "parent": "mCollarLeft",
        "children": [
            "L_UPPER_ARM",
            "mElbowLeft",
        ],
    },
    "L_UPPER_ARM": {
        "parent": "mShoulderLeft",
        "children": [
        ],
    },
    "mElbowLeft": {
        "parent": "mShoulderLeft",
        "children": [
            "L_LOWER_ARM",
            "mWristLeft",
        ],
    },
    "L_LOWER_ARM": {
        "parent": "mElbowLeft",
        "children": [
        ],
    },
    "mWristLeft": {
        "parent": "mElbowLeft",
        "children": [
            "L_HAND",
            "mHandMiddle1Left",
            "mHandIndex1Left",
            "mHandRing1Left",
            "mHandPinky1Left",
            "mHandThumb1Left",
        ],
    },
    "L_HAND": {
        "parent": "mWristLeft",
        "children": [
        ],
    },
    "mHandMiddle1Left": {
        "parent": "mWristLeft",
        "children": [
            "mHandMiddle2Left",
        ],
    },
    "mHandMiddle2Left": {
        "parent": "mHandMiddle1Left",
        "children": [
            "mHandMiddle3Left",
        ],
    },
    "mHandMiddle3Left": {
        "parent": "mHandMiddle2Left",
        "children": [
        ],
    },
    "mHandIndex1Left": {
        "parent": "mWristLeft",
        "children": [
            "mHandIndex2Left",
        ],
    },
    "mHandIndex2Left": {
        "parent": "mHandIndex1Left",
        "children": [
            "mHandIndex3Left",
        ],
    },
    "mHandIndex3Left": {
        "parent": "mHandIndex2Left",
        "children": [
        ],
    },
    "mHandRing1Left": {
        "parent": "mWristLeft",
        "children": [
            "mHandRing2Left",
        ],
    },
    "mHandRing2Left": {
        "parent": "mHandRing1Left",
        "children": [
            "mHandRing3Left",
        ],
    },
    "mHandRing3Left": {
        "parent": "mHandRing2Left",
        "children": [
        ],
    },
    "mHandPinky1Left": {
        "parent": "mWristLeft",
        "children": [
            "mHandPinky2Left",
        ],
    },
    "mHandPinky2Left": {
        "parent": "mHandPinky1Left",
        "children": [
            "mHandPinky3Left",
        ],
    },
    "mHandPinky3Left": {
        "parent": "mHandPinky2Left",
        "children": [
        ],
    },
    "mHandThumb1Left": {
        "parent": "mWristLeft",
        "children": [
            "mHandThumb2Left",
        ],
    },
    "mHandThumb2Left": {
        "parent": "mHandThumb1Left",
        "children": [
            "mHandThumb3Left",
        ],
    },
    "mHandThumb3Left": {
        "parent": "mHandThumb2Left",
        "children": [
        ],
    },
    "mCollarRight": {
        "parent": "mChest",
        "children": [
            "R_CLAVICLE",
            "mShoulderRight",
        ],
    },
    "R_CLAVICLE": {
        "parent": "mCollarRight",
        "children": [
        ],
    },
    "mShoulderRight": {
        "parent": "mCollarRight",
        "children": [
            "R_UPPER_ARM",
            "mElbowRight",
        ],
    },
    "R_UPPER_ARM": {
        "parent": "mShoulderRight",
        "children": [
        ],
    },
    "mElbowRight": {
        "parent": "mShoulderRight",
        "children": [
            "R_LOWER_ARM",
            "mWristRight",
        ],
    },
    "R_LOWER_ARM": {
        "parent": "mElbowRight",
        "children": [
        ],
    },
    "mWristRight": {
        "parent": "mElbowRight",
        "children": [
            "R_HAND",
            "mHandMiddle1Right",
            "mHandIndex1Right",
            "mHandRing1Right",
            "mHandPinky1Right",
            "mHandThumb1Right",
        ],
    },
    "R_HAND": {
        "parent": "mWristRight",
        "children": [
        ],
    },
    "mHandMiddle1Right": {
        "parent": "mWristRight",
        "children": [
            "mHandMiddle2Right",
        ],
    },
    "mHandMiddle2Right": {
        "parent": "mHandMiddle1Right",
        "children": [
            "mHandMiddle3Right",
        ],
    },
    "mHandMiddle3Right": {
        "parent": "mHandMiddle2Right",
        "children": [
        ],
    },
    "mHandIndex1Right": {
        "parent": "mWristRight",
        "children": [
            "mHandIndex2Right",
        ],
    },
    "mHandIndex2Right": {
        "parent": "mHandIndex1Right",
        "children": [
            "mHandIndex3Right",
        ],
    },
    "mHandIndex3Right": {
        "parent": "mHandIndex2Right",
        "children": [
        ],
    },
    "mHandRing1Right": {
        "parent": "mWristRight",
        "children": [
            "mHandRing2Right",
        ],
    },
    "mHandRing2Right": {
        "parent": "mHandRing1Right",
        "children": [
            "mHandRing3Right",
        ],
    },
    "mHandRing3Right": {
        "parent": "mHandRing2Right",
        "children": [
        ],
    },
    "mHandPinky1Right": {
        "parent": "mWristRight",
        "children": [
            "mHandPinky2Right",
        ],
    },
    "mHandPinky2Right": {
        "parent": "mHandPinky1Right",
        "children": [
            "mHandPinky3Right",
        ],
    },
    "mHandPinky3Right": {
        "parent": "mHandPinky2Right",
        "children": [
        ],
    },
    "mHandThumb1Right": {
        "parent": "mWristRight",
        "children": [
            "mHandThumb2Right",
        ],
    },
    "mHandThumb2Right": {
        "parent": "mHandThumb1Right",
        "children": [
            "mHandThumb3Right",
        ],
    },
    "mHandThumb3Right": {
        "parent": "mHandThumb2Right",
        "children": [
        ],
    },
    "mWingsRoot": {
        "parent": "mChest",
        "children": [
            "mWing1Left",
            "mWing1Right",
        ],
    },
    "mWing1Left": {
        "parent": "mWingsRoot",
        "children": [
            "mWing2Left",
        ],
    },
    "mWing2Left": {
        "parent": "mWing1Left",
        "children": [
            "mWing3Left",
        ],
    },
    "mWing3Left": {
        "parent": "mWing2Left",
        "children": [
            "mWing4Left",
            "mWing4FanLeft",
        ],
    },
    "mWing4Left": {
        "parent": "mWing3Left",
        "children": [
        ],
    },
    "mWing4FanLeft": {
        "parent": "mWing3Left",
        "children": [
        ],
    },
    "mWing1Right": {
        "parent": "mWingsRoot",
        "children": [
            "mWing2Right",
        ],
    },
    "mWing2Right": {
        "parent": "mWing1Right",
        "children": [
            "mWing3Right",
        ],
    },
    "mWing3Right": {
        "parent": "mWing2Right",
        "children": [
            "mWing4Right",
            "mWing4FanRight",
        ],
    },
    "mWing4Right": {
        "parent": "mWing3Right",
        "children": [
        ],
    },
    "mWing4FanRight": {
        "parent": "mWing3Right",
        "children": [
        ],
    },
    "mHipRight": {
        "parent": "mPelvis",
        "children": [
            "R_UPPER_LEG",
            "mKneeRight",
        ],
    },
    "R_UPPER_LEG": {
        "parent": "mHipRight",
        "children": [
        ],
    },
    "mKneeRight": {
        "parent": "mHipRight",
        "children": [
            "R_LOWER_LEG",
            "mAnkleRight",
        ],
    },
    "R_LOWER_LEG": {
        "parent": "mKneeRight",
        "children": [
        ],
    },
    "mAnkleRight": {
        "parent": "mKneeRight",
        "children": [
            "R_FOOT",
            "mFootRight",
        ],
    },
    "R_FOOT": {
        "parent": "mAnkleRight",
        "children": [
        ],
    },
    "mFootRight": {
        "parent": "mAnkleRight",
        "children": [
            "mToeRight",
        ],
    },
    "mToeRight": {
        "parent": "mFootRight",
        "children": [
        ],
    },
    "mHipLeft": {
        "parent": "mPelvis",
        "children": [
            "L_UPPER_LEG",
            "mKneeLeft",
        ],
    },
    "L_UPPER_LEG": {
        "parent": "mHipLeft",
        "children": [
        ],
    },
    "mKneeLeft": {
        "parent": "mHipLeft",
        "children": [
            "L_LOWER_LEG",
            "mAnkleLeft",
        ],
    },
    "L_LOWER_LEG": {
        "parent": "mKneeLeft",
        "children": [
        ],
    },
    "mAnkleLeft": {
        "parent": "mKneeLeft",
        "children": [
            "L_FOOT",
            "mFootLeft",
        ],
    },
    "L_FOOT": {
        "parent": "mAnkleLeft",
        "children": [
        ],
    },
    "mFootLeft": {
        "parent": "mAnkleLeft",
        "children": [
            "mToeLeft",
        ],
    },
    "mToeLeft": {
        "parent": "mFootLeft",
        "children": [
        ],
    },
    "mTail1": {
        "parent": "mPelvis",
        "children": [
            "mTail2",
        ],
    },
    "mTail2": {
        "parent": "mTail1",
        "children": [
            "mTail3",
        ],
    },
    "mTail3": {
        "parent": "mTail2",
        "children": [
            "mTail4",
        ],
    },
    "mTail4": {
        "parent": "mTail3",
        "children": [
            "mTail5",
        ],
    },
    "mTail5": {
        "parent": "mTail4",
        "children": [
            "mTail6",
        ],
    },
    "mTail6": {
        "parent": "mTail5",
        "children": [
        ],
    },
    "mGroin": {
        "parent": "mPelvis",
        "children": [
        ],
    },
    "mHindLimbsRoot": {
        "parent": "mPelvis",
        "children": [
            "mHindLimb1Left",
            "mHindLimb1Right",
        ],
    },
    "mHindLimb1Left": {
        "parent": "mHindLimbsRoot",
        "children": [
            "mHindLimb2Left",
        ],
    },
    "mHindLimb2Left": {
        "parent": "mHindLimb1Left",
        "children": [
            "mHindLimb3Left",
        ],
    },
    "mHindLimb3Left": {
        "parent": "mHindLimb2Left",
        "children": [
            "mHindLimb4Left",
        ],
    },
    "mHindLimb4Left": {
        "parent": "mHindLimb3Left",
        "children": [
        ],
    },
    "mHindLimb1Right": {
        "parent": "mHindLimbsRoot",
        "children": [
            "mHindLimb2Right",
        ],
    },
    "mHindLimb2Right": {
        "parent": "mHindLimb1Right",
        "children": [
            "mHindLimb3Right",
        ],
    },
    "mHindLimb3Right": {
        "parent": "mHindLimb2Right",
        "children": [
            "mHindLimb4Right",
        ],
    },
    "mHindLimb4Right": {
        "parent": "mHindLimb3Right",
        "children": [
        ],
    },
}
