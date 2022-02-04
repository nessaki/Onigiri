import bpy








def get_unique_name():
    
    import uuid
    import time
    idn = str(uuid.uuid4())
    name = idn.replace("-", "")
    idt = str(time.time())
    time_now = idt.replace(".", "_")
    unique_name = name + "_" + time_now
    return unique_name








class OnigiriHelpProperties(bpy.types.PropertyGroup):
    def update_help_some_property(self, context):
        onih = bpy.context.window_manager.oni_help
        
        if oni_settings['terminate'] == True:
            oni_settings['terminate'] = False
            return
        
        oni_settings['terminate'] = True
        onih.help_some_property = False
        return









    
    
    
    
    
    
        
    
        
            
        
            
        








    
    
    
    
    
    
    
    
        
        

        
        
        
            
            
        
        
        
            
            
            
            
            
        
        
        
        
            
            
            
            

        






    
    
    

    
    
    
        
    
    


    
    
        






 






