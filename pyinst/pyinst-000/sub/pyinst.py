#!/usr/bin/env python

import os, sys, getopt, signal, select
import gobject, gtk, pango, gst
import tarfile

create_proj = False             
install_proj = False            
list_proj = False             
verbose = False  
force = False 
version = 1.0

def help():

    #print os.path.basename("help")
    print 
    print "Usage: " + os.path.basename(sys.argv[0]) + " command [options] [archive_filename]"
    print 
    print "Command:"
    print "            -c           Create archive from project"          
    print "            -i           Install to system from archive"
    print "            -l           List arcive"
    print "Options:"
    print "            -d level  - Debug level 1-10. (Limited implementation)"
    print "            -v        - Verbose"
    print "            -f        - Force"
    print "            -h        - Help"
    print
    sys.exit(0)

def create(fname):

    global verbose, force
    
    for name in "install.py", "uninst.py":
        if not os.path.isfile(name):
            print "Must have file '" +  name + "'"
            sys.exit(2)

    for name in "preinst.py", "postinst.py":
        if not os.path.isfile(name):
            print "Warning: creating empty file '" +  name + "'"
            fd = open(name, "w"); fd.close

    if verbose:
        print "Creating archive '" + fname + "'"
        
    if os.path.isfile(fname) and not force:
        print "Cannot overwrite ", fname, "use -f to force"      
        sys.exit(0)
        
    tar = tarfile.open(fname, "w:gz")
    
    for name in os.listdir("."):
        if name == fname:
            continue
        if verbose:
            print "Adding: '" + name + "'"
        try:
            tar.add(name)
        except:
            print "Cannot add:", name
            
    tar.close()    

if __name__ == '__main__':

    #global version, force
    
    opts = []; args = []
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvcilVf")
    except getopt.GetoptError, err:
        print "Invalid option(s) on command line:", err
        sys.exit(1)

    #print "opts", opts, "args", args
    
    for aa in opts:
        if aa[0] == "-d":
            try:
                pgdebug = int(aa[1])
            except:
                pgdebug = 0

        if aa[0] == "-h": help();  exit(1)
        if aa[0] == "-v": verbose = True            
        if aa[0] == "-f": force = True            
        if aa[0] == "-V": 
            print os.path.basename(sys.argv[0]), "Version", version
        
        if aa[0] == "-c": create_proj = True            
        if aa[0] == "-i": install_proj = True            
        if aa[0] == "-l": list_proj = True            
     
    if len(args) > 0: 
        fname = args[0]
        if args[0][-4:]  != ".tgz":
            fname = args[0] + ".tgz"
    else: 
        fname = os.path.basename(os.getcwd()) + ".tgz"
        
    if  list_proj:
        pass
    elif create_proj:
        create(fname)
        pass
    elif install_proj:
        pass
    else: 
        print
        print "Must specify one of -c -i -l"
        help()
        
