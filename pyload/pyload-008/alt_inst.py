# Example of adding a group and giving files group permissions:

gotg = False; grpx = "shutdown"
 
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
    print "Adding group membership:"
    # Add user as a member
    ret = subprocess.call([respath("usermod"), "-a", "-G", grpx, os.getlogin()])
    print "You may need to logout for changes to take effect."
    
# Append init script

sysinit = "/etc/rc.d/rc.local"
try:
    fd = open(sysinit);  xstr = fd.read(); fd.close()
    # Add it if not there
    if xstr.find("$IDEV2") < 0:
        fd3 = open(sysinit + ".old", "w");  
        fd3.write(xstr); fd3.close()
        xstr += \
            "\n"                                            \
            "# Change permissions of shutdown devices\n"    \
            "POWS=/sys/power/state\n"                       \
            "chmod g+rw     $POWS\n"                        \
            "chown .shutdown $POWS\n"                       \
            "# Change permissions of input devices\n"       \
            "IDEV2=`ls /dev/input/by-path/*kbd`\n"          \
            "chmod g+r       $IDEV2\n"                      \
            "chown .shutdown $IDEV2\n"                      \
            "IDEV3=`ls /dev/input/by-path/*mouse`\n"        \
            "chmod g+r       $IDEV3\n"                      \
            "chown .shutdown $IDEV3\n"                      \
            "\n"
        fd2 = open(sysinit, "w");  
        fd2.write(xstr); fd2.close()
        ret = subprocess.call(["./loadperm.sh"])
        print "Written to ", sysinit
            
except:
    print sys.exc_info()
    pass











