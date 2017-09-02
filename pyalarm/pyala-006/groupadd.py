# Example of adding an TRTC group

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


