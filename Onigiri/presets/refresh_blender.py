import bpy
import tempfile
import traceback
import time
import uuid
import os






def run_main():

    temp_path = tempfile.gettempdir()
    temp_blend = temp_path + "/bentobuddy_blend.blend"

    
    for o in bpy.data.objects:
        o.select_set(True)
    bpy.ops.object.delete()

    
    
    
    
    args_path = temp_path + "/bentobuddy_args.py"
    arguments = {}
    try:
        namespace = {}
        exec(open(args_path).read(), namespace)
        arguments.update(namespace['arguments'])
    except Exception as e:
        print(traceback.format_exc())
        print("The args file wasn't able to process")
        return False

    
    
    
    
    
    

    
    if arguments['stage'] == 2:
        print("Spawned process running stage 2")
        
        
        
        
        try:
            bpy.ops.wm.open_mainfile(
                filepath=arguments['file_new'],
                use_scripts=False,
                load_ui=False)
            
            try:
                arguments['status'] = True
                af = open(args_path, "w")
                formatted_text = "arguments = "
                formatted_text += str(arguments)
                af.write(formatted_text)
                af.close()
            except Exception as e:
                print(traceback.format_exc())
                print("The args file wasn't able to process during stage 2")
                return False

        except Exception as e:
            print(traceback.format_exc())
            print("Error in stage 2 when opening file:", arguments['file_new'])

        return True

    
    scene_match = "match"
    
    count = 0
    while scene_match == "match":
        scene_remove = get_unique_name_short()
        if scene_remove not in arguments['scenes']:
            bpy.context.scene.name = scene_remove
            scene_match = "no match"
        count += 1
        if count > 5:
            print("Scene rename attempt failed")
            return False

    with bpy.data.libraries.load(temp_blend) as (data_from, data_to):
        for attr in dir(data_to):
            setattr(data_to, attr, getattr(data_from, attr))

    bpy.data.scenes.remove(bpy.data.scenes[scene_remove])

    
    
    

    
    file_path = arguments['file_new']
    print("refresh_blender reports: new file is", file_path)
    try:
        bpy.ops.wm.save_as_mainfile(filepath=file_path)
    except Exception as e:
        print("Couldn't save the new blender file:", file_path)
        print(traceback.format_exc())
        return False

    
    arguments['status'] = True
    formatted_text = "arguments = "
    formatted_text += str(arguments)
    try:
        af = open(args_path, "w")
        af.write(formatted_text)
        af.close()
    except Exception as e:
        print("A problem occurred during the process of re-writing the args file:", args_path)
        print(traceback.format_exc())
        return False

    return True





    
    with bpy.data.libraries.load(temp_blend) as (data_from, data_to):
        data_to.scenes = ["Scene"]

    return

    
    with bpy.data.libraries.load(filepath) as (data_from, data_to):
        data_to.meshes = data_from.meshes
    
    with bpy.data.libraries.load(filepath, link=True) as (data_from, data_to):
        
        data_to.objects = [name for name in data_from.objects]

    
    with bpy.data.libraries.load(filepath) as (data_from, data_to):
        for attr in dir(data_to):
            setattr(data_to, attr, getattr(data_from, attr))


    
    
    
    with bpy.data.libraries.load(filepath) as (data_from, data_to):
        data_to.meshes = data_from.meshes

    return True







def get_unique_name_short():
    unique_name = str(uuid.uuid4())
    return unique_name.split('-', 1)[0]





run_main()
