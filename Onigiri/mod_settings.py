
import traceback





bb_settings = {}


bb_settings["layers"] = {}
bb_settings["layers"]["mbones"] = 1
bb_settings["layers"]["vbones"] = 2
bb_settings["layers"]["abones"] = 3
bb_settings["layers"]["nbones"] = 4
bb_settings["layers"]["extended"] = 5
bb_settings["layers"]["face"] = 6
bb_settings["layers"]["hand"] = 7




bb_settings['debug'] = False





bb_settings['proxy_type'] = "empty"













bb_settings['mh_vcount'] = 13380




bb_settings['mh_edges'] = [
    11556,
    24851,
    11788,
    25037,
    12203,
    25465]









bb_settings["arg"] = ""







bb_settings["save_state"] = True

































bb_settings["fly_paper"] = True





bb_settings["set_rotation"] = True




bb_settings["keep_rotation"] = False





bb_settings["source"] = "" 


bb_settings["terminate"] = False
bb_settings["terminate_handler"] = False


bb_settings["sl_joint_total"] = 110
bb_settings["sl_joint_influences"] = 4 

















bb_settings["count"] = 0 


bb_settings["paths"] = {}
bb_settings["paths"]["presets"] = "/presets/"   
bb_settings["paths"]["data"] = "/data/"         
bb_settings["paths"]["devkit"] = "/devkit/"         
bb_settings["paths"]["code"] = "/code/"         
bb_settings["paths"]["icons"] = "/icons"        
bb_settings["paths"]["characters"] = "/characters/"        

bb_settings["files"] = {}
bb_settings["files"]["reset"] = "/reset.pkl"
bb_settings["files"]["bvh_template"] = "/bvh_template.txt"
bb_settings["files"]["anim_data"] = "/anim_data.py"
bb_settings["files"]["joint_data"] = "/joint_data.py"


bb_settings["files"]["lsl_animation"] = "/bulk_export_fill_avatar.txt"
bb_settings["files"]["lsl_animmesh"] = "/bulk_export_fill_animesh.txt"

bb_settings["files"]["lsl_split_animation"] = "/bulk_export_split_avatar.txt"
bb_settings["files"]["lsl_split_animmesh"] = "/bulk_export_split_animesh.txt"



bb_settings["files"]["bone_orientation"] = "/bone_orientation.mtx"








bb_settings["files"]["rigs"] = {}
bb_settings["files"]["rigs"]["lib"] = "bb_rig_lib.blend" 
bb_settings["files"]["rigs"]["types"] = {}
bb_settings["files"]["rigs"]["types"]["base"] = "BentoBuddyBase"
bb_settings["files"]["rigs"]["types"]["animation"] = "BentoBuddy"














bb_settings["map_to_mbones"] = {}
bb_settings["map_to_mbones"]["flags_new"] = {}
bb_settings["map_to_mbones"]["flags_new"]["rename_to"] = 0
bb_settings["map_to_mbones"]["flags_new"]["unlink_bones"] = 0
bb_settings["map_to_mbones"]["flags_new"]["create_links"] = 0
bb_settings["map_to_mbones"]["flags_new"]["use_connect_state"] = 1
bb_settings["map_to_mbones"]["flags_new"]["pretty_places"] = 0
bb_settings["map_to_mbones"]["flags_old"] = {}





bb_settings["map_to_template"] = {}
bb_settings["map_to_template"]["path"] = ""



bb_settings["map_to_template"]["flags_new"] = {}
bb_settings["map_to_template"]["flags_new"]["rename_to"] = 0
bb_settings["map_to_template"]["flags_new"]["unlink_bones"] = 0
bb_settings["map_to_template"]["flags_new"]["create_links"] = 0
bb_settings["map_to_template"]["flags_new"]["use_connect_state"] = 1
bb_settings["map_to_template"]["flags_new"]["pretty_places"] = 0
bb_settings["map_to_template"]["flags_old"] = {}



bb_settings['dae_export_options'] = {
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












