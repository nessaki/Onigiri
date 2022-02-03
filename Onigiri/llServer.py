import os
import sys
import time
import uuid

import threading
import tempfile
import traceback
import http.server
import socketserver















def run_main():

    
    

    
    
    args = sys.argv[sys.argv.index("--") + 1:]

    temp_dir = tempfile.gettempdir()
    print("Temp Folder:", temp_dir)

    
    

    args_file = args[0]
    arguments = {}
    try:
        namespace = {}
        exec(open(args_file, 'r', encoding='UTF8').read(), namespace)
        arguments.update(namespace['arguments'])
    except Exception as e:
        print(traceback.format_exc())
        print("llServer reports: Couldn't open arguments file, this is a fatal error")
        return False

    if 1 == 0:
        folder = "."
        file = "log.txt"
        path = folder + "/" + file
        time_now = time.time() 
        fd = open(path, "a", encoding='UTF8') 

        time_formatted = time.ctime(time_now)

        fd.write("Mark: " + time_formatted + "\n")
        fd.close()

    print("llServer reports: reached end of execution")

    return




def get_unique_name():
    idn = str(uuid.uuid4())
    name = idn.replace("-", "")
    idt = str(time.time())
    time_now = idt.replace(".", "_")
    unique_name = name + "_" + time_now
    return unique_name





def check_parent():
    print("check_parent child thread runs from parent pid", pid)

    temp_dir = tempfile.gettempdir()
    run_file = temp_dir + "/bentobuddy_llServer.run"
    if os.path.exists(run_file):
        try:
            os.remove(run_file)
        except Exception as e:
            print(traceback.format_exc())
            print("llServer reports: Something went wrong when trying to delete the run file")
            t_event_cancel()
            os.kill(pid, -9)
            return False
        return True
    print("llServer reports: Parent seems to have vanished")
    t_event.cancel()
    os.kill(pid, -9)
    return False





temp_dir = tempfile.gettempdir()
run_file = temp_dir + "/bentobuddy_llServer.run"

if os.path.exists(run_file):
    print("llServer reports: Initial run file exists, removing and setting up timer event")
    try:
        os.remove(run_file)
    except Exception as e:
        print(traceback.format_exc())
        print("llServer reports: Couldn't remove run file, fatal error")
        sys.exit()
else:
    print("llServer reports: Initial run file is missing, fatal error")
    sys.exit()


pid = os.getpid()
print("llServer reports: pid is", pid)




t_event = threading.Timer(10.0, check_parent)
t_event.start()


run_main()




