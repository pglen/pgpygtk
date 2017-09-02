#!/usr/bin/env python

import time, sys, os, re, stat, subprocess
import string, pickle, commands, site, grp

import distutils.sysconfig

installerdir = sys.argv[0][:sys.argv[0].rfind("/")] + "/"

depfailed = False

PROJNAME  = "pyala"
PROJLIB   = "pyedlib"
PROJLIB2  = "panglib"

# ------------------------------------------------------------------------
# Resolve path name

def respath(fname):
    ppp = string.split(os.environ['PATH'], os.pathsep)
    for aa in ppp:
        ttt = aa + os.sep + fname
        if os.path.isfile(ttt):
            return ttt

# ------------------------------------------------------------------------
# Return True if exists

def isdir(fname):

    try:    
        ss = os.stat(fname)
    except:
        return False
    if stat.S_ISDIR(ss[stat.ST_MODE]):
        return True
    return False

# ------------------------------------------------------------------------
# Make dir if it does not exist

def softmkdir(dirx):
    if not isdir(dirx):
        #print "Creating directory '" + dirx + "'"
        os.mkdir(dirx, 0755)
        if not isdir(dirx):
            return False
    return True
   
# See if path contains user dirs:

path = os.environ['PATH']; home = os.environ['HOME']
user = os.environ['USER']

#print "path", path
#print "home", home, "user", user

if commands.getoutput("whoami").strip() != "root":

    gotbin = ""
    for aa in str.split(path, ":"):   
        if aa.find(home) >= 0:    
            gotbin = aa    
    if  gotbin == "":
        print "FAILED: You must be root to install pangview."
        sys.exit()
    else: 
        print "installing in", gotbin
        sys.exit()
   
    print "FAILED: You must be root to install", PROJNAME
    sys.exit()
           
#print "Verifying dependencies:"
 
try:
    import pygtk
    pygtk.require('2.0')
    import gtk
    import gobject
except ImportError:
    print "  >>>  Missing Dependencies: Python GTK+ bindings (python-gtk2)."
    depfailed = True

try:
    import gnome.ui
except ImportError:
    print "  >>>  Missing Dependencies: Python GNOME bindings (python-gnome2)."
    depfailed = True

# not stricly needed, just a validity check

prefix = sys.prefix
if not isdir(prefix):
    print "  >>>  Missing Dependencies: sys prefix dir does not exist."
    depfailed = True

pylib = distutils.sysconfig.get_python_lib()
if not isdir(pylib):
    print "  >>>  Missing Dependencies: Python Library dir does not exist."
    depfailed = True

# ------------------------------------------------------------------------

if depfailed:
    print "FAILED: Dependencies not met. Exiting."
    sys.exit(1)

print "All dependencies are met."

shared  = "/usr/share" + "/" + PROJNAME
bindir = "/usr/bin"

#print "prefix:", prefix
#print "libdir:", libdir
#print "bonobo:", bonobo

    # --- file  ---  target dir ---- exec flag ----
filelist = \
    ['pyload.py',               bindir,         True ],     \
    ['README',                  shared,         False ],    \
    ['ala.png',                 shared,         False ],    \
    ['ala2.png',                shared,         False ],    \
    ['ala3.png',                shared,         False ],    \
    
    # --- dir  ---  target dir ---- root owner flag ----
dirlist = \
    [PROJNAME,     "/usr/share",    True ], \
    ["pyala",         pylib,          True ], \

# Copy all to target:

print "Making target directories:"

for source, dest, exe in dirlist:
    targ = dest + "/" + source
    print "   '" + targ + "'" 
    softmkdir(targ)   

print "Copying files:"

for source, dest, exe in filelist:
    try:
        targ =  dest +  "/" + source 
        print "   '" + source + "'\t->'" + targ + "'"
        # Do not overwrite newer stuff
        commands.getoutput("cp -u " + source + " " + targ)
        if exe:
            os.chmod(targ, 0755) # Root can rwx; can rx 
        else:
            os.chmod(targ, 0644) # Root can rw; others r
    except:
        print sys.exc_info()

print "Copying directories:"

for source, dest, exe in dirlist:
    try:
        print "   '" + source + "'\t->'" + dest + "'"
        commands.getoutput ("cp -a " + source + " " + dest)
        if exe:
            commands.getoutput(" chown root.root " + dest + "/" + source + "/*")
    except:
        print sys.exc_info()

# Execute supplementary actions

gotg = False; grpx = "rtc"
 
# Add group if not there:            
for aa in grp.getgrall(): 
    if aa[0] == grpx: 
        gotg = True; break
if not gotg:
    print "Adding group:"
    ret = subprocess.call([respath("groupadd"), grpx, ])
    
# Add group membership if not there:            
output = subprocess.Popen(\
        [respath("groups"), os.getlogin()], stdout=subprocess.PIPE).communicate()[0]
gotu = False
for aa in output.split(" "):
    aa = string.strip(aa)
    if aa == grpx:
        gotu = True

if not gotu:
    print "Adding group", "(" + grpx + ")", "membership:"
    # Add user as a member
    ret = subprocess.call([respath("usermod"), "-a", "-G", grpx, os.getlogin()])
    print "You may need to logout for changes to take effect."
 
# Append init script

sysinit = "/etc/rc.d/rc.local"
try:
    fd = open(sysinit);  xstr = fd.read(); fd.close()
        
    # Add it if not there
    if xstr.find("RTC") < 0:
        print "Installing startup:"
        fd3 = open(sysinit + ".old", "w"); fd3.write(xstr); fd3.close()
        xstr += \
            "\n"                                        \
            "# Change permissions of RTC device\n"      \
            "RTCDEV=/dev/rtc\n"                         \
            "chown  .rtc  $RTCDEV\n"                    \
            "chmod g+r   $RTCDEV\n"                     \
            "\n"
        fd2 = open(sysinit, "w");  
        fd2.write(xstr); fd2.close()
        #print "Written to ", sysinit
except:
    print sys.exc_info()
    pass

print 
print "You may now use the", PROJNAME, "utility on your system."
print


