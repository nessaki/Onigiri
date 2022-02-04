
import traceback

oni_settings = {}

oni_settings["layers"] = {}
oni_settings["layers"]["mbones"] = 1
oni_settings["layers"]["vbones"] = 2
oni_settings["layers"]["abones"] = 3
oni_settings["layers"]["nbones"] = 4
oni_settings["layers"]["extended"] = 5
oni_settings["layers"]["face"] = 6
oni_settings["layers"]["hand"] = 7

oni_settings['debug'] = False

oni_settings['proxy_type'] = "empty"

oni_settings['mh_vcount'] = 13380

oni_settings['mh_edges'] = [
    11556,
    24851,
    11788,
    25037,
    12203,
    25465]

oni_settings["arg"] = ""

oni_settings["save_state"] = True

oni_settings["fly_paper"] = True

oni_settings["set_rotation"] = True

oni_settings["keep_rotation"] = False

oni_settings["source"] = "" 

oni_settings["terminate"] = False
oni_settings["terminate_handler"] = False

oni_settings["sl_joint_total"] = 110
oni_settings["sl_joint_influences"] = 4 

oni_settings["count"] = 0 

oni_settings["paths"] = {}
oni_settings["paths"]["presets"] = "/presets/"   
oni_settings["paths"]["data"] = "/data/"         
oni_settings["paths"]["devkit"] = "/devkit/"         
oni_settings["paths"]["code"] = "/code/"         
oni_settings["paths"]["icons"] = "/icons"        
oni_settings["paths"]["characters"] = "/characters/"        

oni_settings["files"] = {}
oni_settings["files"]["reset"] = "/reset.pkl"
oni_settings["files"]["bvh_template"] = "/bvh_template.txt"
oni_settings["files"]["anim_data"] = "/anim_data.py"
oni_settings["files"]["joint_data"] = "/joint_data.py"

oni_settings["files"]["lsl_animation"] = "/bulk_export_fill_avatar.txt"
oni_settings["files"]["lsl_animmesh"] = "/bulk_export_fill_animesh.txt"

oni_settings["files"]["lsl_split_animation"] = "/bulk_export_split_avatar.txt"
oni_settings["files"]["lsl_split_animmesh"] = "/bulk_export_split_animesh.txt"

oni_settings["files"]["bone_orientation"] = "/bone_orientation.mtx"

oni_settings["files"]["rigs"] = {}
oni_settings["files"]["rigs"]["lib"] = "oni_rig_lib.blend" 
oni_settings["files"]["rigs"]["types"] = {}
oni_settings["files"]["rigs"]["types"]["base"] = "OnigiriBase"
oni_settings["files"]["rigs"]["types"]["animation"] = "Onigiri"

oni_settings["map_to_mbones"] = {}
oni_settings["map_to_mbones"]["flags_new"] = {}
oni_settings["map_to_mbones"]["flags_new"]["rename_to"] = 0
oni_settings["map_to_mbones"]["flags_new"]["unlink_bones"] = 0
oni_settings["map_to_mbones"]["flags_new"]["create_links"] = 0
oni_settings["map_to_mbones"]["flags_new"]["use_connect_state"] = 1
oni_settings["map_to_mbones"]["flags_new"]["pretty_places"] = 0
oni_settings["map_to_mbones"]["flags_old"] = {}

oni_settings["map_to_template"] = {}
oni_settings["map_to_template"]["path"] = ""

oni_settings["map_to_template"]["flags_new"] = {}
oni_settings["map_to_template"]["flags_new"]["rename_to"] = 0
oni_settings["map_to_template"]["flags_new"]["unlink_bones"] = 0
oni_settings["map_to_template"]["flags_new"]["create_links"] = 0
oni_settings["map_to_template"]["flags_new"]["use_connect_state"] = 1
oni_settings["map_to_template"]["flags_new"]["pretty_places"] = 0
oni_settings["map_to_template"]["flags_old"] = {}

oni_settings['dae_export_options'] = {
    "dae_apply_modifiers": "Apply Modifiers",
    "dae_selected": "Selection Only",
    "dae_include_children": "Include Children",
    "dae_include_armatures": "Include Armatures",
    "dae_include_shapekeys": "Include Shapekeys",
    "dae_include_animations": "Include Animations",
    "dae_deform_bones_only": "Deformable Bones Only",
    "dae_triangulate": "Triangulate",
    "dae_use_object_instantiation": "Use Object Instantiation",
    "dae_use_blender_profile": "Use Blender Profile",
    "dae_sort_by_name": "Sort By Name",
    "dae_open_sim": "For SL / OpenSim",
    }

pelvis_names = {"mpelvis", "avatar_mPelvis", "hip", "hips"}
