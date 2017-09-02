#!/usr/bin/env python

# ------------------------------------------------------------------------
# Python Alarm

import os, sys, getopt, signal, select, socket, time, struct
import random, stat, subprocess

from pgutil import  *
from mainwin import  *

import rtc

# ------------------------------------------------------------------------
# Globals 

version = "0.00"
scanagain = 120     # Seconds

# ------------------------------------------------------------------------
# Decode date / time from  filename

def decode_name(onefile):
    global conf
    try:
        ttt = (int(onefile[1:5]), int(onefile[5:7]), \
            int(onefile[7:9]), int(onefile[9:11]), int(onefile[11:13]) \
               , 0, -1, -1, -1)
        tt = time.mktime(ttt)
    except:
        if conf.verbose:
            print "Cannot convert time", sys.exc_info()
        tt = None
    return tt
                    
# ------------------------------------------------------------------------
# Pop up alarm now

def alarm(fname):

    global conf, ala_dir
    
    threefile = "c" + fname[1:]
    # Move to next state
    try:
        os.rename(ala_dir + "/" + fname, ala_dir + "/" + threefile)
    except:
        if conf.verbose:
            print "Cannot rename alarm file", sys.exc_info()
    try:
        ppp = respath("python"); 
        # Pass full path, so the popup app does not need to know internals
        ret = subprocess.Popen([ppp, "pyalapop.py", ala_dir + "/" + threefile])
        mw.listx.add_row("Popped up alarm. Spooler file Name: '%s'" % (threefile))
    except:    
        mw.listx.add_row("Cannot pop up alarm. Spooler file Name: '%s'" % (threefile))
        if conf.verbose:
            print "Cannot execute alarm subprocess", sys.exc_info()

    fill_spooler()
    fill_history()
    
# ------------------------------------------------------------------------
# The GUI requested an alarm

def  add_alarm(ret):

    global mw, ala_dir
    try:
        # Decorate alarm file
        fname = "a%04d%02d%02d%02d%02d" % \
                  (ret[0][0], ret[0][1], ret[0][2], ret[1][0], ret[1][1]) 
        fname = ala_dir + "/" + fname
        #print ret, fname    
        ddd =  "%04d/%02d/%02d %02d:%02d" % \
                (ret[0][0], ret[0][1], ret[0][2], ret[1][0], ret[1][1]) 
        num = 1
        fname2 = fname
        while 1:
            if os.path.isfile(fname2):
                fname2 = "%s#%d" % (fname, num); num += 1
            else:
                break
        fd = open(fname2, "w")
        fd.write("DATE=" + ddd + "\n") 
        fd.write("ACTION="  + ret[2] + "\n") 
        fd.write("NAME="    + ret[3] + "\n") 
        fd.write("EXE="     + ret[4] + "\n") 
        fd.close()
        mw.listx.add_row("Created alarm. Name: '%s' Date: %s" % (ret[3], ddd))
        app_tick()
        
    except:
        print "Add alarm", sys.exc_info()     
        
# ------------------------------------------------------------------------
        
def fill_spooler():

    global mw, ala_dir
    
    mw.lists.clear()
    dirlist = os.listdir(ala_dir)
    dirlist.sort()
    tstr = ""; sstr = ""
    for onefile in dirlist:
        sss = os.lstat(ala_dir + "/" + onefile)
        if stat.S_ISREG(sss[stat.ST_MODE]):
            # Decode name:
            if onefile[0] == "a":
                sstr = "Waiting "
            elif onefile[0] == "b":
                sstr = "Queued  "
            elif onefile[0] == "c":
                sstr = "Popped   "
            else:
                sstr = "Other "    
            
            tt = decode_name(onefile)
            tstr = time.asctime(time.localtime(tt))
            mw.lists.add_row("%s %s" % (sstr, tstr))

# ------------------------------------------------------------------------

def fill_history():

    global mw, ala_old
    
    mw.listd.clear()
    dirlist = os.listdir(ala_old)
    dirlist.sort()
    tstr = ""; sstr = ""
    for onefile in dirlist:
        sss = os.lstat(ala_old + "/" + onefile)
        if stat.S_ISREG(sss[stat.ST_MODE]):
            # Decode name:
            if onefile[0] == "a":
                sstr = "Waiting "
            elif onefile[0] == "b":
                sstr = "Queing "
            elif onefile[0] == "c":
                sstr = "Alarm  "
            elif onefile[0] == "d":
                sstr = "Done  "
            else:
                sstr = "Other "    
            
            tt = decode_name(onefile)
            tstr = time.asctime(time.localtime(tt))
            mw.listd.add_row("%s %s" % (sstr, tstr))
        
# ------------------------------------------------------------------------
# Examine the spool dir, set alarms if any, keep it going

def app_tick(init = "a", init2 = "b"):
    
    global interval, startx, ala_dir, ala_old, scanagain, conf
    
    now = time.time()
    if conf.verbose:
        print "app_tick:", time.asctime(time.localtime(now))
    
    dirlist = os.listdir(ala_dir)
    dirlist.sort()
    for onefile in dirlist:
        # Filter alarm files
        if onefile[0] == init:
            sss = os.lstat(ala_dir + "/" + onefile)
            if stat.S_ISREG(sss[stat.ST_MODE]):
                # Decode name:
                tt = decode_name(onefile)
                tstr = time.asctime(time.localtime(tt))
                if not tt:
                    continue
                    
                if tt < now:
                    if conf.verbose:
                        "Alarm file in past, removing", onefile
                    mw.listx.add_row("Missed alarm. Date: '%s'" % (tstr))
                    os.rename(ala_dir + "/" + onefile, ala_old + "/" + onefile)
                    continue
                   
                # Too far into the future, no action 
                if tt > now + scanagain:
                    if conf.verbose:
                        print "Alarm file in future, skipping"
                    continue
                   
                # Move file only if state change needed
                try:
                    if init2:
                        twofile = init2 + onefile[1:]
                        twofile = uniquename(twofile, ala_dir)
                        os.rename(ala_dir + "/" + onefile, ala_dir + "/" + twofile)
                    else:
                        twofile = onefile
                    delay = tt - now
                    if conf.verbose:
                        print "Added alarm, alarm delay time:", delay, \
                                "Spooler file", twofile
                    mw.listx.add_row("Using Spooler file '%s'" % (twofile))
                    mw.listx.add_row("Set alarm for %s" % tstr )
                    
                    gobject.timeout_add(int(delay * 1000), alarm, twofile)
                except:
                    if conf.verbose:
                        print"Cannot rename file", sys.exc_info()

    # Keep the heart beat going
    gobject.timeout_add(scanagain * 1000, app_tick)
                                                                                        
# ------------------------------------------------------------------------

def phelp():

    print
    print "Usage: " + os.path.basename(sys.argv[0]) + " [options]"
    print
    print "Options:    -d level  - Debug level 0-10"
    print "            -p        - Port to use (default: 9999)"
    print "            -v        - Verbose"
    print "            -V        - Version"
    print "            -q        - Quiet"
    print "            -h        - Help"
    print
    sys.exit(0)

# ------------------------------------------------------------------------
def pversion():
    print os.path.basename(sys.argv[0]), "Version", version
    sys.exit(0)
    
    # option, var_name, initial_val, function
optarr = \
    ["d:",  "pgdebug",  0,      None],      \
    ["p:",  "port",     9999,   None],      \
    ["v",   "verbose",  0,      None],      \
    ["q",   "quiet",    0,      None],      \
    ["t",   "test",     "x",    None],      \
    ["V",   None,       None,   pversion],  \
    ["h",   None,       None,   phelp]      \
    
conf = Config(optarr)

if __name__ == '__main__':

    global mw, interval, startx, ala_dir, ala_old, lastwake

    ala_dir = os.path.expanduser("~/.pyala/spool")
    ala_old = os.path.expanduser("~/.pyala/history")
    
    interval = 1
    startx = time.time()
    
    try:
        ww = rtc.rwake()
        print "wake", ww
        www = list(ww[2:])  
        www.append(-1); www.append(-1);  www.append(-1)
        lastwake = time.mktime(www) #- time.timezone
        tstr = time.asctime(time.localtime(lastwake))
        print "Lastwake:", tstr, time.timezone / (60 * 60), time.tzname
    except:
        lastwake = startx
        print "Power down / wake up servicwe will not available", sys.exc_info()
        print "Must run as root -- or chmod o+r /dev/rtc (RTC to user readable)"
    
    if not os.path.isdir(ala_dir):
        os.makedirs(ala_dir)
    if not os.path.isdir(ala_old):
        os.makedirs(ala_old)
        
    # Test it, bail out if no spool dir    
    if not os.path.isdir(ala_dir):
        print "Cannot access local storage"
        sys_exit(1)
        
    args = conf.comline(sys.argv[1:])
    # We decorate the window with callbacks to separate logic
    mw = MainWin(); mw.app_tick = app_tick; 
    mw.add_alarm = add_alarm
    mw.fill_spooler = fill_spooler 
    mw.fill_history = fill_history
    
    mw.listx.limit_row(20)

    # Restart apps in spool dir
    app_tick("b", "") 
    gtk.main()
    sys.exit(0)


