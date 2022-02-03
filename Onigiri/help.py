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








class BentoBuddyHelpProperties(bpy.types.PropertyGroup):
    def update_help_some_property(self, context):
        bbh = bpy.context.window_manager.bb_help
        
        if bb_settings['terminate'] == True:
            bb_settings['terminate'] = False
            return
        
        bb_settings['terminate'] = True
        bbh.help_some_property = False
        return









    
    
    
    
    
    
        
    
        
            
        
            
        








    
    
    
    
    
    
    
    
        
        

        
        
        
            
            
        
        
        
            
            
            
            
            
        
        
        
        
            
            
            
            

        






    
    
    

    
    
    
        
    
    


    
    
        






 






