
















oni_flags = {} 
oni_notes = {} 
oni_labels = {} 
oni_data = {} 
oni_options = {} 




oni_groups = {}
oni_groups["general"] = []
oni_groups["advanced"] = []
























oni_flags.update({"rename_to": 1})
oni_groups["general"].append("rename_to")
oni_labels["rename_to"] = "Rename custom rig bones"
oni_notes["rename_to"] = "Rename the target bones to SL bone names, is the default.  This allows you to "    "rebind your meshes to the Avastar rig in order to use its mesh exporter for Second Life.  "    "See advanced settings for other features."











    
    
    
    
    
    
    






oni_flags.update({"unhide_animation_bones": 1})
oni_groups["general"].append("unhide_animation_bones")
oni_labels["unhide_animation_bones"] = "Unhide all of the animation bones"
oni_notes["unhide_animation_bones"] =    "I have a lot of useless flags that I'll be removing over time, this is not one of them.  This will uhide "    "all of the animation bones on the Avastar rig.  Combine this with (Hide unused bones) and you might have the "    "only pair of visibility flags you need."





oni_options["rename_to"] = {}
oni_options["rename_to"].update({"rename_to_source": 0})
oni_options["rename_to"].update({"rename_to_mbones": 1})

oni_flags.update({"rename_to_source": 0}) 
oni_groups["advanced"].append("rename_to_source")
oni_labels["rename_to_source"] = "Rename custom bones to source"
oni_notes["rename_to_source"] = "Rename the bones in your custom rig to the same as the bones used "    "in your source rig.  This is probably not a common setting but it's here if you need it.  "    "This is not the same as (SL compatibility).  The pose bones in the Avastar rig are not named for SL.  "    "If you want Second Life compatibility then use the flag (Rename custom bones for SL compatibility)."
oni_flags.update({"rename_to_mbones": 1}) 
oni_groups["advanced"].append("rename_to_mbones")
oni_labels["rename_to_mbones"] = "Rename custom bones for SL compatibility"
oni_notes["rename_to_mbones"] = "Rename your custom rig bones to the proper Second Life mBone names.  "    "This is valuable when you want to transfer weights (rebind) from your mesh to the source rig, to "    "make it compatible with Second Life and exportable by Avastar.  The base flag must be checked for "    "this to work (Rename custom rig bones)."





oni_flags.update({"unlink_bones": 1})
oni_groups["advanced"].append("unlink_bones")
oni_labels["unlink_bones"] = "Unlink the source bones"
oni_notes["unlink_bones"] = "Unlink source bones, default is pose bones.  See advanced options for other features."



oni_flags.update({"unlink_all": 0})
oni_groups["advanced"].append("unlink_all")
oni_labels["unlink_all"] = "Unlink all bones in the source rig"
oni_notes["unlink_all"] = "Using this flag will break animations, if you have no use for this then leave it unchecked."


oni_flags.update({"unlink_pbones": 1})
oni_groups["advanced"].append("unlink_pbones")
oni_labels["unlink_pbones"] = "Unlink all the pose bones"
oni_notes["unlink_pbones"] = "Unlinking all of the pose bones usually doesn't cause any problems.  Doing this might fix some strange deformations."


oni_flags.update({"unlink_vbones": 1})
oni_groups["advanced"].append("unlink_vbones")
oni_labels["unlink_vbones"] = "Unlink the volume bones"
oni_notes["unlink_vbones"] = "This doesn't usually cause problems but enabling it could fix some deformation issues."


oni_flags.update({"anchor_vbones": 1})
oni_groups["general"].append("anchor_vbones")
oni_labels["anchor_vbones"] = "Anchor the volume bones"
oni_notes["anchor_vbones"] =    "If you're unlinking the volume bones and you are sure that's what you want, "    "and you are experiencing problems because of it, try enabling this switch.  "    "It will anchor all of the volume bones to a common location, defined in your "    "custom template or in your custom bone lists.  This might clear up animation  "    "export errors."


oni_flags.update({"unlink_mbones": 0})
oni_groups["advanced"].append("unlink_mbones")
oni_labels["unlink_mbones"] = "Unlink the base mBones - (breaks animations)"
oni_notes["unlink_mbones"] =    "There might be a reason for you to do this, I don't know, I used it for debugging, it will break animation exports."




oni_flags.update({"unlink_used_pbones": 0})
oni_groups["advanced"].append("unlink_used_pbones")
oni_labels["unlink_used_pbones"] = "Unlink only the used pose bones"
oni_notes["unlink_used_pbones"] =    "If unlinking all of the pose bones causes issues, you might be able to get away with this one.  "    "It will unlink only the bones that were used for your target rigs."


oni_flags.update({"unlink_used_mbones": 0})
oni_groups["advanced"].append("unlink_used_mbones")
oni_labels["unlink_used_mbones"] = "Unlink the used base bones (mBones) (breaks animations)"
oni_notes["unlink_used_mbones"] = "This will unlink the base mBones that were matched with the pose bones, it will break animations export."


oni_flags.update({"unlink_problem_bones": 0})
oni_groups["advanced"].append("unlink_problem_bones")
oni_labels["unlink_problem_bones"] = "Unlink bones that have caused problems"
oni_notes["unlink_problem_bones"] = "Unlink the bones listed in the problem_bones section, again this might free up deform issues."




oni_flags.update({"unlink_excluded_bones": 0})
oni_groups["advanced"].append("unlink_excluded_bones")
oni_labels["unlink_excluded_bones"] = "Unlink structure bones"
oni_notes["unlink_excluded_bones"] =    "These excluded bones are not real SL bones, mostly they can be ignored, "    "but sometimes they cause problems if they are linked.  Sometimes they cause problems when they are unlinked.  Try either."







oni_flags.update({"create_links": 0})
oni_groups["general"].append("create_links")
oni_labels["create_links"] = "Re-link the pose bone hierarchy"
oni_notes["create_links"] =    "Despite what you may have heard, yes you can do this, link the pose bone hierarchy into a different structure "    "that makes more sense for your animations.  This will take on the structure of the target rigs.  "    "You only need this if you are going to animate the pose bones directly, without your proxy rigs doing it for you."





oni_flags.update({"constrain_bones": 1})
oni_groups["general"].append("constrain_bones")
oni_labels["constrain_bones"] = "Constrain used bones to your rigs"
oni_notes["constrain_bones"] =    "This constraint allows you to transfer your animations from your target rigs to the source bones.  "    "This is part of the magic you probably want as it will effectively glue the pose bones to the rigs, allowing "    "the source bones and target bones to move together.  This is just the base flag, enable this and choose one of "    "the constraint options."


oni_flags.update({"constraint_child_of": 0})
oni_groups["advanced"].append("constraint_child_of")
oni_labels["constraint_child_of"] = "Constrain Child OF"
oni_notes["constraint_child_of"] = "This has been effective in many situations.  The default is to use separate constraints."

oni_flags.update({"constraint_copy_location": 1})
oni_groups["advanced"].append("constraint_copy_location")
oni_labels["constraint_copy_location"] = "Constrain Location"
oni_notes["constraint_copy_location"] = "Constrain the pose bones to the target bones locations."

oni_flags.update({"constraint_copy_rotation": 1})
oni_groups["advanced"].append("constraint_copy_rotation")
oni_labels["constraint_copy_rotation"] = "Constrain Rotation"
oni_notes["constraint_copy_rotation"] = "Constrain the pose bones to the target bones rotation."

oni_flags.update({"constraint_copy_scale": 0})
oni_groups["advanced"].append("constraint_copy_scale")
oni_labels["constraint_copy_scale"] = "Constrain Scale"
oni_notes["constraint_copy_scale"] = "Constrain the pose bones to the target bones scale."

oni_flags.update({"constraint_copy_transforms": 0})
oni_groups["advanced"].append("constraint_copy_transforms")
oni_labels["constraint_copy_transforms"] = "Constrain All Transforms"
oni_notes["constraint_copy_transforms"] =    "Constrain to all transforms of the targets.  Not always what you need but but sometimes an alternative to (Child Of) "    "and you might want to try a combination of things if you have a difficult rig."





oni_flags.update({"target_non_deformable": 0})
oni_groups["advanced"].append("target_non_deformable")
oni_labels["target_non_deformable"] = "Target non deformable bones"
oni_notes["target_non_deformable"] =    "Usually you don't want to waste a bone mapping on a target bone that is not flagged as deformable.  "    "An example of this would be shape bones, that alter the mesh depending on where the rotation is.  "    "Second Life doesn't support this.  Control bones and controllers for IK also are non deformable and you "    "don't want to waste bones on those either.  However, I'm giving you the option here in case you need it.  "    "Enabling this will tell Onigiri to put a bone anywhere where this is a bone, regardless if it's deformable."







oni_flags.update({"use_vbones": 0})
oni_groups["general"].append("use_vbones")
oni_labels["use_vbones"] = "Include volume bones as possible source"
oni_notes["use_vbones"] =    "Enabling this allows them to be counted as possible sources for animation, you'll need this if the tool "    "reports that you don't have enough source bones for your target rigs."









    
    






oni_flags.update({"preserve_animation": 0})
oni_groups["general"].append("preserve_animation")
oni_labels["preserve_animation"] = "Fix scaled Rig to preserve animation"
oni_notes["preserve_animation"] =    "Check the scale on your target rig, the one on the character you want to convert.  Open up the N panel and check "    "the scale.  If it is not a 1 then you need this flag if you want to preserve the animation.  This is typical of characters "    "exported from Mixamo."






oni_flags.update({"debug": 0})
oni_labels["debug"] = "Show extensive messages in console"
oni_notes["debug"] = "Turn on debug messages in order to find a problem.  Use the output in the console to report an issue."
oni_groups["advanced"].append("debug")


oni_flags["used_source"] = 0
oni_labels["used_source"] = "Flag mapped source as used (debug setting)"
oni_notes["used_source"] = "Flag the source rig as used after its mapped to the targets."
oni_groups["general"].append("used_source")







oni_flags.update({"hide_excluded_bones": 1})
oni_groups["advanced"].append("hide_excluded_bones")
oni_labels["hide_excluded_bones"] = "Hide the excluded bones"
oni_notes["hide_excluded_bones"] =    "Hide these bones that can't be animated, probably a good idea after conversion since attempting "    "to animate them can cause an export problem."


oni_flags.update({"hide_unused_bones": 0})
oni_groups["general"].append("hide_unused_bones")
oni_labels["hide_unused_bones"] = "Hide unused bones"
oni_notes["hide_unused_bones"] =    "Hide the bones that were not used in your target rigs, it just makes things look better if you're not adding more bones after."





oni_flags.update({"hide_problem_bones": 0})
oni_groups["advanced"].append("hide_problem_bones")
oni_labels["hide_problem_bones"] = "Hide the bones known to cause problems"
oni_notes["hide_problem_bones"] =    "These problem bones that have been identified as causing problems can safely be hidden.  However, if you need to "    "debug a problem then you can uncheck this box to see what's going on in the backgroud with these bones."



oni_flags.update({"hide_misc": 0})
oni_groups["advanced"].append("hide_misc")
oni_labels["hide_misc"] = "Hide misc items"
oni_notes["hide_misc"] =    "These include COG, Origin and PevlisInv.  They should not cause problems either way.  It's usually safe to keep them hidden."










oni_flags.update({"show_used_bones": 1})
oni_groups["advanced"].append("show_used_bones")
oni_labels["show_used_bones"] = "Unhide the used pose bones"
oni_notes["show_used_bones"] = "Force the used pose bones to be unhidden, sometimes they have a tendency to vanish."


oni_flags.update({"unhide_vbones": 1})
oni_groups["general"].append("unhide_vbones")
oni_labels["unhide_vbones"] = "Unhide the volume bones"
oni_notes["unhide_vbones"] =    "Unhide the volume bones, allowing you to see what's used and not used.  You may have decided to include the "    "volume bones for your animations and you should force these to be unhidden so you can see what's going on."








oni_flags.update({"view_extras": 1})
oni_groups["general"].append("view_extras")
oni_labels["view_extras"] = "View normally unused bones"
oni_notes["view_extras"] =    "We really want these available if we're doing Animesh, to get the most out of the skeleton.  These bones "    "are not typically used, and do not affect the classic avatar in world, but are available to animate and "    "to skin the mesh to, so use them as you please."




oni_flags.update({"force_unhide": 1})
oni_groups["general"].append("force_unhide")
oni_labels["force_unhide"] = "Force view of extra spine bones"
oni_notes["force_unhide"] =    "The Avastar rig default setting is to hide these bones to reduce complexity and problems.  "    "We're doing Animesh or custom avastars so we want all the bones we can get.  Feel free to tinker "    "with these."


oni_flags.update({"unhide_ik_bones": 0})
oni_groups["advanced"].append("unhide_ik_bones")
oni_labels["unhide_ik_bones"] = "Unhide Avastar's IK bones"
oni_notes["unhide_ik_bones"] =    "This will show the IK bones after the conversion.  There's probably never a need to do this, unless you want "    "to just delete them.  Keeping them hidden is usually save since it prevents you from accidentally adding a keyframe "    "to any of them, which would prevent you from exporting your animation."


































oni_flags.update({"disable_use_connect": 1})
oni_groups["general"].append("disable_use_connect")
oni_labels["disable_use_connect"] = "Disable source use_connect"
oni_notes["disable_use_connect"] =    "This will set the use_connect property of the bones in the source rig before mapping.  "    "This was initially a debug setting but I found it useful for some rigs so I put it into the "    "general settings.  This is not the same as (Enable use_connect).  The (Enable use_connect) happens "    "after the bones have been mapped and is used to orient the bone ends of the finished mapping in alignment "    "with the new positions.  This is probably safe to use (enabled) unless you're using standard Mixamo rigs."



oni_flags.update({"use_connect_state": 0})
oni_groups["general"].append("use_connect_state")
oni_labels["use_connect_state"] = "Enable use_connect"
oni_notes["use_connect_state"] =    "This setting requires that you enable (Re-Link the pose bone hierarchy).  While this is the same property as "    "(Disable use_connect) it "    "is used differently.  This particular connection will be enabled after the bones have been mapped (moved).  "    "In this way the bones are aiming at each other.  This is not what you will always want.  For instance, with Mixamo "    "characters you probably want to disable this feature, since the rigs exported from Mixamo tend to be broken "    "(disconnected) and you want to mimic that apparent breakage in order to capture the animations exported from "    "that platform."









oni_flags.update({"change_inherit": 0})
oni_groups["advanced"].append("change_inherit")
oni_labels["change_inherit"] = "Base flag for transform inheritance"
oni_notes["change_inherit"] = "This flag is required if you want any of the other 3 inherit flags to have meaning."

oni_flags.update({"inherit_rotation": 1})
oni_groups["advanced"].append("inherit_rotation")
oni_labels["inherit_rotation"] = "Inherit parent rotation"
oni_notes["inherit_rotation"] = "Inherit the rotation of the parent bone, you probably always want this enabled."

oni_flags.update({"inherit_location": 1})
oni_groups["advanced"].append("inherit_location")
oni_labels["inherit_location"] = "Inherit parent location"
oni_notes["inherit_location"] = "Inherit the location of the parent bone, you probably always want this enabled."

oni_flags.update({"inherit_scale": 0})
oni_groups["advanced"].append("inherit_scale")
oni_labels["inherit_scale"] = "Inherit parent scale"
oni_notes["inherit_scale"] =    "Inherit the scale of the parent bone.  Typically this is disabled since the scale is derived from the armature anyway.  "    "Enabling this might have unexpected results."






    
    





oni_flags.update({"remove_constraints": 1})
oni_groups["advanced"].append("remove_constraints")
oni_labels["remove_constraints"] = "Base flag to remove source constraints"
oni_notes["remove_constraints"] =    "You need to enable this in order to remove all locks and constraints from the source armature.  "    "You probably always want to enable this but leave the mBones alone or you'll break animations."

oni_flags.update({"remove_constraints_pbones": 1})
oni_groups["advanced"].append("remove_constraints_pbones")
oni_labels["remove_constraints_pbones"] = "Remove pose bone constraints"
oni_notes["remove_constraints_pbones"] =    "Pose bones are the ones we really need but the other constraints get in the way so make sure you remove those "    "for an effective conversion."

oni_flags.update({"remove_constraints_mbones": 0}) 
oni_groups["advanced"].append("remove_constraints_mbones")
oni_labels["remove_constraints_mbones"] = "Remove base bone constraints (mBones)"
oni_notes["remove_constraints_mbones"] = "You don't need to do this, it might even break something if you do.  These are the base bones."

oni_flags.update({"remove_constraints_vbones": 1})
oni_groups["advanced"].append("remove_constraints_vbones")
oni_labels["remove_constraints_vbones"] = "Remove volume bone constraints"
oni_notes["remove_constraints_vbones"] = "These volume bones can be used like any other bones, we want them unlocked and available."

oni_flags.update({"remove_constraints_ik": 1})
oni_groups["advanced"].append("remove_constraints_ik")
oni_labels["remove_constraints_ik"] = "Remove ik bone constraints"
oni_notes["remove_constraints_ik"] =    "These constraints, if enabled, might cause some strange malformations in your animations, particularly in those that are "    "transfered from another rig.  Enable this in order to disable those constraints.  It's probably alway safe to do that."



oni_flags.update({"remove_constraints_misc": 1})
oni_groups["advanced"].append("remove_constraints_misc")
oni_labels["remove_constraints_misc"] = "Remove misc bone constraints"
oni_notes["remove_constraints_misc"] =    "These misc bones include COG, Origin and PelvisInv.  If you have deform or location issues in SL try toggling this."

oni_flags.update({"remove_constraints_problem": 1})
oni_groups["advanced"].append("remove_constraints_problem")
oni_labels["remove_constraints_problem"] = "Remove problem bone constraints"
oni_notes["remove_constraints_problem"] =    "These bones that I, or you, have identified as being problems should still be free to move around.  Keeping this "    "checked is probably safe."

oni_flags.update({"remove_constraints_excluded": 1})
oni_groups["advanced"].append("remove_constraints_excluded")
oni_labels["remove_constraints_excluded"] = "Remove constraints from excluded bones"
oni_notes["remove_constraints_excluded"] =    "These excluded bones are not able to be animated.  They can, however, cause problems if they are not free to roam.  "    "It's probably safe to remove their constraints."


oni_flags.update({"remove_shapes": 1})
oni_groups["advanced"].append("remove_shapes")
oni_labels["remove_shapes"] = "Remove custom shapes"
oni_notes["remove_shapes"] =    "The source rig uses a variety of custom shapes, which we don't need.  Use it, don't use it, makes no difference.  "    "They are just annoying to see when they have no effect on the resulting rig."




























oni_flags.update({"pretty_bones": 1})
oni_groups["advanced"].append("pretty_bones")
oni_labels["pretty_bones"] = "Pretty bone colors"
oni_notes["pretty_bones"] =    "This is really just for show, but it does allow you to group things for selection.  This has no major effect either way."











oni_flags.update({"pretty_places":               0 }) 
oni_groups["general"].append("pretty_places")
oni_labels["pretty_places"] = "Pretty places for the left over bones"
oni_notes["pretty_places"] = "This is the base flag.  Any bones remaining after conversion can be place in a grid in a specified location."

oni_flags.update({"pretty_places_set_pbones":    1 }) 
oni_groups["advanced"].append("pretty_places_set_pbones")
oni_labels["pretty_places_set_pbones"] = "Relocate the left over pose bones"
oni_notes["pretty_places_set_pbones"] = "Move the remaining pose bones to a specified location."



oni_flags.update({"pretty_places_set_vbones":    1 }) 
oni_groups["advanced"].append("pretty_places_set_vbones")
oni_labels["pretty_places_set_vbones"] = "Relocation left over volume bones"
oni_notes["pretty_places_set_vbones"] = "Move the left over volume bones to a specified location."

oni_flags.update({"pretty_places_set_misc":      1 }) 
oni_groups["advanced"].append("pretty_places_set_misc")
oni_labels["pretty_places_set_misc"] = "Relocate the left over misc bones"
oni_notes["pretty_places_set_misc"] = "Relocate these bones."

oni_flags.update({"pretty_places_set_problem":   1 })
oni_groups["advanced"].append("pretty_places_set_problem")
oni_labels["pretty_places_set_problem"] = "Relocate problem bones"
oni_notes["pretty_places_set_problem"] = "Move these somewhere."

oni_flags.update({"pretty_places_set_excluded":  1 })
oni_groups["advanced"].append("pretty_places_set_excluded")
oni_labels["pretty_places_set_excluded"] = "Relocate excluded bones"
oni_notes["pretty_places_set_excluded"] = "Relocate the non available bones."












oni_data.update({"pretty_places_transform_world":     [2.0, 0.0, 0.0 ] })
oni_data.update({"pretty_places_transform_spacing":   [0.05, 0.0, 0.0] })
oni_data.update({"pretty_places_transform_length":    [0.0, 0.0, 0.1 ] })
oni_data.update({"pretty_places_transform_separator": [0.0, 0.0, 0.1 ] })
oni_data.update({"pretty_places_transform_groups":     20})
oni_data.update({"pretty_places_transform_offset":    [0.0, 0.0, 0.15]})
















oni_flags.update({"sanity_check": 1})




oni_flags.update({"vbones_first": 0})
oni_groups["advanced"].append("vbones_first")
oni_labels["vbones_first"] = "Use volume / collision bones first"
oni_notes["vbones_first"] =    "The internal data have a specific structure, it's not random which bones are used first to map to your characters.  "    "However, for the sake of testing I chose to create this feature in order to test the functionality of using the "    "volume bones for animation, like any other bone.  I discovered that it works but I kept the flag here for you to play with.  "    "Note that you can already control which bones are used first by using a text file and importing that map into Onigiri."


oni_flags.update({"match_roll": 1})
oni_groups["general"].append("match_roll")
oni_labels["match_roll"] = "Force pose bone to target bone roll"
oni_notes["match_roll"] =    "Deformations can be effected by incorrect bone roll, this should fix it.  It's usually safe to keep it enabled."



oni_flags.update({"disable_relationship_lines": 0})
oni_groups["general"].append("disable_relationship_lines")
oni_labels["disable_relationship_lines"] = "Disable view of parent / child lines"
oni_notes["disable_relationship_lines"] =    "Disable the dotted lines for links that are not directly connected.  This might confuse you later if you enable this.  "    "The view, however, can be confusing when you haven't unlinked the source bones in a previous flag.  Try one way then  "    "the other.  You can always re-run the tool."


oni_flags.update({"apply_target_transforms": 0})
oni_groups["advanced"].append("apply_target_transforms")
oni_labels["apply_target_transforms"] = "Apply transforms to your rigs"
oni_notes["apply_target_transforms"] =    "Apply all the transforms to your selected rigs.  You may not want to do this if you run into mapping issues where "    "the bones don't end up in the right place.  You probably don't want to do this if your rig is already animated.  "    "If your rig is animated but you think it requires (apply scale), don't use this.  There is a different process for that."


oni_flags.update({"apply_transforms_before_mapping": 1})
oni_groups["advanced"].append("apply_transforms_before_mapping")
oni_labels["apply_transforms_before_mapping"] = "Apply transforms before mapping"
oni_notes["apply_transforms_before_mapping"] = "Applying transforms to the source rig before mapping.  "    "This can clear up some weird behavior when the bones are moved to your targets.  For instance, if your bones "    "don't end up in the right place then try this."


oni_flags.update({"apply_restpose_before_constraints": 1})
oni_groups["advanced"].append("apply_restpose_before_constraints")
oni_labels["apply_restpose_before_constraints"] = "Apply restpose before constraints"
oni_notes["apply_restpose_before_constraints"] = "This is one of two test flags, you probably want one, probably not both.  "    "Applying the rest pose before the constraints are added will prevent a common problem.  However, you "    "will lose the benefit of signaling to Second Life that you have altered all bones."

oni_flags.update({"apply_restpose_after_constraints": 0})
oni_groups["advanced"].append("apply_restpose_after_constraints")
oni_labels["apply_restpose_after_constraints"] = "Apply restpose after constraints"
oni_notes["apply_restpose_after_constraints"] = "Applying restpose after the constraints are attached seems to prevent a different problem, "    "although I haven't completely worked this out yet, so I've put these flags in here for you to utilize."




oni_flags.update({"use_world_matrix": 0})
oni_groups["advanced"].append("use_world_matrix")
oni_labels["use_world_matrix"] = "Use world matrix when moving bones"
oni_notes["use_world_matrix"] =    "This will use the world matrix when moving bones to the new areas.  Try first without it and, if you experience "    "strange results, try with it.  It will have different effects depending on the existing transforms on your target rigs."




oni_flags.update({"remove_empties": 1})
oni_groups["advanced"].append("remove_empties")
oni_labels["remove_empties"] = "Remove empties (debug feature)"
oni_notes["remove_empties"] = "This is a debug feature, you probably never need to use it."



oni_data.update({"oni_arm": "Onigiri"})



oni_data.update({"skel_type": "pivot"})












oni_map = {}

oni_map["type"] = "tbones"














oni_rig = {}
oni_rig["vbones_selectable"] = 0








oni_flags.update({"continue_retargeting": 1})
oni_groups["general"].append("continue_retargeting")
oni_labels["continue_retargeting"] = "Continue retargeting after mode interruption"
oni_notes["continue_retargeting"] = ""    "This flag, when enabled, allows you to move in and out of Blender's POSE mode while in the mapping stage.  "    "If you need to move the rigs around, maybe closer together, you can come out of pose mode, "    "choose a rig, move it, make sure at least one of them is selected, then go back into POSE mode.  "    "This is experimental and I put it here as an option for convenience.  WARNING!:  Do not do anything else when "    "exiting pose mode except to move your rigs, doing so will crash the mode and you WILL have to restart Blender."



