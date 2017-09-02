#!/usr/bin/env python
                                        
# SUDO Starter frontend for pyload.py

import os, sys, subprocess

# ------------------------------------------------------------------------
# Start of program:

if __name__ == '__main__':

    # Redirect to a file in /tmp (debug only) This solves the difficulty 
    # in seeing stdout while in tray mode.
    '''args = []
    #args.append("sudo")
    args.append("/usr/bin/sudo")
    args.append("/usr/bin/pyload.py")
    for aa in sys.argv[1:]:
        args.append(aa)
    sys.stdout.flush()     
    print "Exec", args
    sp = subprocess.Popen(args)
    #ret = subprocess.call(args)
    #print sp.pid
    #os.waitpid(sp.pid, 0)
    #print "returncode", sp.returncode
    #print "returncode", ret'''
    
    os.execl("/usr/bin/sudo",  "/usr/bin/python", "/usr/bin/pyload.py")
    print "Exec done."
    #sys.exit(0)









