













import mathutils

def get_diff(vec):
    vr = vec.replace("<", "")
    vr = vr.replace(">", "")
    vs = vr.split()
    vl = list()
    for v in vs:
        vf = v.split(",")
        vl.append([float(fl) for fl in vf])
    v0 = vl[0]
    v1 = vl[1]
    v = list()
    for i in range(len(v0)):
        a = v0[i]
        b = v1[i]
        v.append( abs((a) - (b)) )
    return v
gd = get_diff

vec = """
<-10.1,10.2,-0.3>
<1,2,3>
"""
print(vec)
print("vec dif:", gd(vec))





pos = dict()
pos["BELLY"] = {
    "default": [0.0, 0.0, 0.0],
    
    
    "neutral": [0.0, 0.004, 0.015],
    }

pos["PELVIS"] = {
    "default": [0.0, 0.0, 0.0],
    "neutral": [0.0, 0.0, 0.0],
    }
pos["CHEST"] = {
    "default": [0.0, 0.0, 0.0],
    "neutral": [0.0, 0.0, 0.0],
    }
pos["UPPER_BACK"] = {
    "default": [0.0, 0.0, 0.0],
    "neutral": [0.0, 0.0, 0.0],
    }
pos["LEFT_PEC"] = {
    "default": [0.0, 0.0, 0.0],
    "neutral": [0.0, 0.0, 0.0],
    }
pos["RIGHT_PEC"] = {
    "default": [0.0, 0.0, 0.0],
    "neutral": [0.0, 0.0, 0.0],
    }
pos["HEAD"] = {
    "default": [0.0, 0.0, 0.0],
    "neutral": [0.0, 0.0, 0.0],
    }
pos["NECK"] = {
    "default": [0.0, 0.0, 0.0],
    "neutral": [0.0, 0.0, 0.0],
    }
pos["BUTT"] = {
    "default": [0.0, 0.0, 0.0],
    "neutral": [0.0, 0.0, 0.0],
    }
pos["LOWER_BACK"] = {
    "default": [0.0, 0.0, 0.0],
    "neutral": [0.0, 0.0, 0.0],
    }
pos["L_CLAVICLE"] = {
    "default": [0.0, 0.0, 0.0],
    "neutral": [0.0, 0.0, 0.0],
    }
pos["R_CLAVICLE"] = {
    "default": [0.0, 0.0, 0.0],
    "neutral": [0.0, 0.0, 0.0],
    }
pos["L_UPPER_ARM"] = {
    "default": [0.0063, 0.0, -0.011],
    "neutral": [0.0205, 0.0, -0.012],
    }
pos["R_UPPER_ARM"] = {
    "default": [-0.0063, 0.0, -0.011],
    "neutral": [-0.0205, 0.0, -0.012],
    }

pos["L_LOWER_ARM"] = {
    "default": [0.0, 0.0, 0.0],
    "neutral": [0.0, 0.0, 0.0],
    }
pos["R_LOWER_ARM"] = {
    "default": [0.0, 0.0, 0.0],
    "neutral": [0.0, 0.0, 0.0],
    }
pos["LEFT_HANDLE"] = {
    "default": [0.0, 0.0, 0.0],
    "neutral": [0.0, 0.0, 0.0],
    }
pos["RIGHT_HANDLE"] = {
    "default": [0.0, 0.0, 0.0],
    "neutral": [0.0, 0.0, 0.0],
    }
pos["L_UPPER_LEG"] = {
    "default": [0.0, 0.0, 0.0],
    "neutral": [0.0, 0.0, 0.0],
    }
pos["R_UPPER_LEG"] = {
    "default": [0.0, 0.0, 0.0],
    "neutral": [0.0, 0.0, 0.0],
    }
pos["L_LOWER_LEG"] = {
    "default": [0.0, 0.0, 0.0],
    "neutral": [0.0, 0.0, 0.0],
    }
pos["R_LOWER_LEG"] = {
    "default": [0.0, 0.0, 0.0],
    "neutral": [0.0, 0.0, 0.0],
    }
pos["L_HAND"] = {
    "default": [0.0, 0.0, 0.0],
    "neutral": [0.0, 0.0, 0.0],
    }
pos["R_HAND"] = {
    "default": [0.0, 0.0, 0.0],
    "neutral": [0.0, 0.0, 0.0],
    }
pos["L_FOOT"] = {
    "default": [0.0, 0.0, 0.0],
    "neutral": [0.0, 0.0, 0.0],
    }
pos["R_FOOT"] = {
    "default": [0.0, 0.0, 0.0],
    "neutral": [0.0, 0.0, 0.0],
    }
