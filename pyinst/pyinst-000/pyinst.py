#!/usr/bin/env python

import os, sys, getopt, signal, select
import gobject, gtk, pango, gst
import tarfile, subprocess, commands

import filemap

create_proj = False             
install_proj = False            
list_proj = False             
verbose = False  
force = False 
version = 1.0
pgdebug = 0


needed = "install.py", "uninst.py"
optional ="preinst.py", "postinst.py"

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

# ------------------------------------------------------------------------

def install(fname):

    global verbose, force, pgdebug
    
    if verbose:
        print "Installing from archive '" + fname + "'"
        
    # Check prerequisites
    try:
        tar = tarfile.open(fname, "r")
    except:
         print "Cannot extract from tar file. (possible invalid format)"
         if debug:
            print sys.exc_info()
         return
    
    # Expand filemap entries
    filemap2 = []
    for aaa in filemap.map:
        aaa = aaa[0], os.path.expanduser(aaa[1])
        filemap2.append(aaa)
    
    if "install.py" not in tar.getnames():
        print "Warnming: archive must have an install.py script."
        
    if "filemap.py" not in tar.getnames():
        print "Warnming: archive must have an filemap.py script."
    
    if verbose:
        total = 0
        for aa in tar.getmembers(): total += aa.size
        print "Install size:", total, "bytes"
    
    # Create a sandbox for extraction
    olddir = os.getcwd()
    tempdir = "./pyinst-" + str(os.getpid())
    #print tempdir, olddir
    os.mkdir(tempdir);  os.chdir(tempdir)
    
    tar.extractall()
    
    # Pre execution scripts
    try:
        do_exec("preinst.py")
    except:
        cleanup(olddir, tempdir, tar)
        return
        
    #try:
    #    do_exec("install.py")
    #except:
    #    cleanup(olddir, tempdir, tar)
    #    return
    
    # Loop on files, ignore pyinst specific
    for aa in tar.getnames():
    
        # Do not operate on internals:
        internal = False 
        aa2 = os.path.basename(aa)
        if aa2 == "pyinst.py": internal = True;
        if aa2 == "filemap.py": internal = True;
        
        # Ignore directory entries themselves
        if os.path.isdir(aa): internal = True;
        
        for nn in needed:     
            aa2 = os.path.basename(aa)
            if aa2 == nn: 
                internal = True; break 
        for nn in optional:  
             aa2 = os.path.basename(aa)
             if aa2 == nn: 
                internal = True; break 
        if internal:
            continue
    
        found = False         
        for aaa in filemap2:
            if aa == aaa[0]:
                found = True 
                source = aa; targ = aaa[1] + "/" + aa
                cpfile(source, targ)
                break
        # Install to default desination:
        if not found:
            found = False 
            for aaa in filemap2:
                if "*" == aaa[0]:
                    found = True 
                    source = aa; targ = aaa[1] + "/" + aa
                    cpfile(source, targ)
                    break
                    
            if not found:
                print "Warnning: No default destination for '" + aa + "'"
                
    # Post execution script
    try:
        do_exec("postinst.py")
    except:
        cleanup(olddir, tempdir, tar)
        return
        
    cleanup(olddir, tempdir, tar)
    
# ------------------------------------------------------------------------
# Copy file

def cpfile(source, targ):

    dd = os.path.dirname(targ)
    if not os.path.isdir(dd):
        if verbose:
            print "Maiking dir '"+ dd + "'"
        os.makedirs(dd + "//")

    try:
        if verbose:
            print "Installing '"+ source + \
                    "'  to  '" + targ + "'"
            bb = commands.getoutput("cp -u " + source + " " + targ)
            if bb != "":
                print bb
    except:
        print_except("Exception on copy files.")
    
# ------------------------------------------------------------------------
def print_except(xstr):
    print xstr; a,b,c = sys.exc_info();  print a, b, c.print_tb()

# ------------------------------------------------------------------------
def do_exec(fname):
    global verbose
    try:
        if verbose:
            print "Started", fname
            
        pp = subprocess.Popen(["python", fname])
        ret = os.waitpid(pp.pid, 0)
        if ret[1] != 0:
            print "Warninig: ", fname, "returned with", ret[1]
            
        if verbose:
            print "Ended ", fname
    except:
        print "Cannot execute script", fname, sys.exc_info()
        raise  
        return True
        
           
# ------------------------------------------------------------------------
# Clean temp dir

def cleanup(olddir, tempdir, tar):

    # Clean up:
    os.chdir(olddir)
    for root, dirs, files in os.walk(tempdir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))     
    os.rmdir(tempdir)
    tar.close()                
        

# ------------------------------------------------------------------------

def list(fname):

    global verbose, force
    
    if verbose:
        print "Listing archive '" + fname + "'"
    tar = tarfile.open(fname, "r")
    tar.list(verbose)
    tar.close()

def create(fname):

    global verbose, force
    
    for name in needed:
        if not os.path.isfile(name):
            print "Must have file '" +  name + "'"
            sys.exit(2)

    for name in optional:
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

# ------------------------------------------------------------------------

if __name__ == '__main__':

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
        if not os.path.isfile(fname):
            fname = args[0] + ".tgz"
            if not os.path.isfile(fname):
                fname = args[0] + ".tar.gz"
    else: 
        #if args[0][-4:]  != ".tgz":
        fname = os.path.basename(os.getcwd()) + ".tgz"

    if not os.path.isfile(fname):
        print "No file named '" +  fname + "'"
        sys.exit(1)
                
    # Work is done here:
    if  list_proj:
        list(fname)
    elif create_proj:
        create(fname)
        pass
    elif install_proj:
        install(fname)
    else: 
        print
        print "Must specify one of -c -i -l"
        help()
        



