#!/usr/bin/env python

# ------------------------------------------------------------------------
# Python Alarm

import os, sys, getopt, signal, select, socket, time, struct
import random, stat, subprocess, gobject, gtk

import rtc.rtc
import pyalalib.pyalawin
import pyalalib.pgutil

# ------------------------------------------------------------------------
# Globals 

version = "0.00"
scanagain = 60          # Seconds between re-scans

# ------------------------------------------------------------------------
# Decode date / time from  filename

def decode_date(onefile):
    global conf
    try:
        ttt = (int(onefile[1:5]), int(onefile[5:7]), \
            int(onefile[7:9]), int(onefile[9:11]), int(onefile[11:13]) \
               , 0, -1, -1, -1)
        tt = time.mktime(ttt)
    except:
        #if conf.verbose:
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
        #if conf.verbose:
        print "Cannot rename alarm file", sys.exc_info()
    try:
        ppp = pyalalib.pgutil.respath("pyalapop.py"); 
        # Pass full path, so the popup app does not need to know internals
        ret = subprocess.Popen([ppp, ala_dir + "/" + threefile])
        mw.listx.add_row("Popped up alarm. Spooler file Name: '%s'" % (threefile))
    except:    
        mw.listx.add_row("Cannot pop up alarm. Spooler file Name: '%s'" % (threefile))
        #if conf.verbose:
        print "Cannot execute alarm subprocess", sys.exc_info()

    fill_spooler()
    fill_history()
    fill_missed()
    
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
        fd.write("NAME="    + ret[2] + "\n") 
        fd.write("EXE="     + ret[3] + "\n") 
        #fd.write("ACTION="  + ret[2] + "\n") 
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
            sstr = decode_state(onefile)
            tt = decode_date(onefile)
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
            sstr = decode_state(onefile)
            tt = decode_date(onefile)
            tstr = time.asctime(time.localtime(tt))
            mw.listd.add_row("%s %s" % (sstr, tstr))
        
# ------------------------------------------------------------------------

def fill_missed():

    global mw, ala_mis
    
    mw.listm.clear()
    dirlist = os.listdir(ala_mis)
    dirlist.sort()
    tstr = ""; sstr = ""
    for onefile in dirlist:
        sss = os.lstat(ala_mis + "/" + onefile)
        if stat.S_ISREG(sss[stat.ST_MODE]):
            sstr = decode_state(onefile)
            tt = decode_date(onefile)
            tstr = time.asctime(time.localtime(tt))
            mw.listm.add_row("%s %s" % (sstr, tstr))
        
# ------------------------------------------------------------------------
# Decode state:
        
def decode_state(onefile):

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
        
    return sstr    
                
# ------------------------------------------------------------------------
# Examine the spool dir, set alarms if any, keep it going

def app_tick(init = "a", init2 = "b"):
    
    global interval, startx, ala_dir, ala_old, ala_mis, scanagain, conf
    
    tz = time.timezone - time.daylight * 3600
    now = time.time()
    
    if conf.verbose:
        print "app_tick:", time.asctime(time.localtime(now)), init
    
    dirlist = os.listdir(ala_dir); dirlist.sort()
    for onefile in dirlist:
        # Filter alarm files
        if onefile[0] == init:
            sss = os.lstat(ala_dir + "/" + onefile)
            if stat.S_ISREG(sss[stat.ST_MODE]):
                # Decode date:
                tt = decode_date(onefile)
                tstr = time.asctime(time.localtime(tt))
                if not tt:
                    continue
                if tt < now:
                    if conf.verbose:
                        "Alarm file in past, removing", onefile
                    mw.listx.add_row("Missed alarm. Date: '%s'" % (tstr))
                    os.rename(ala_dir + "/" + onefile, ala_mis + "/" + onefile)
                    continue
                   
                # Test if new wake is before current wake, or ...
                # current wake is in the past.
                try:
                    pyalalib.pgutil.elevate_priv()
                    ttt = rtc.rtc.readwake() - tz
                    pyalalib.pgutil.drop_priv()
                    if tt < ttt or ttt <= now:
                        # Set RTC to a 2 minutes before, so alarm still goes OK
                        # and triggers after we wake from hybernation
                        pyalalib.pgutil.elevate_priv()
                        rtc.rtc.setwake(tt + tz - 120)
                        pyalalib.pgutil.drop_priv()
                except:
                    pass  # We already let the user know
    
                # Too far into the future, do not add it yet
                if tt > now + scanagain:
                    if conf.verbose:
                        print "Alarm file in future, skipping"
                    continue
                   
                # Move file only if state change needed
                try:
                    if init2:
                        twofile = init2 + onefile[1:]
                        twofile = pyalalib.pgutil.uniquename(twofile, ala_dir)
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
                    #if conf.verbose:
                    print"Cannot rename file", sys.exc_info()

    # Keep the heart beat going
    #if init == "a":
    #    gobject.timeout_add(scanagain * 1000, app_tick)
    
    return True
                                                                                        
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
    
conf = pyalalib.pgutil.Config(optarr)

def print_time(tt):
    print time.asctime(time.localtime(tt))
                        
# ------------------------------------------------------------------------

if __name__ == '__main__':

    global mw, interval, startx, ala_dir, ala_old, ala_mis, lastwake

    pyalalib.pgutil.drop_priv()
    os.chdir(os.environ['HOME'])
    #print os.getcwd()
    
    rtcflag = True
    tz = time.timezone - time.daylight * 3600
    ala_dir = os.path.expanduser("~/.pyala/spool")
    ala_old = os.path.expanduser("~/.pyala/history")
    ala_mis = os.path.expanduser("~/.pyala/missed")
    #print ala_mis
    interval = 1
    startx = time.time()
    args = conf.comline(sys.argv[1:])
    
    try:
        pyalalib.pgutil.elevate_priv()
        tt = rtc.rtc.readtime() - tz 
        pyalalib.pgutil.drop_priv()
        tstr = time.asctime(time.localtime(tt))
        if conf.verbose:
            print "RTC time at startup:", tstr
    except:
        lastwake = startx
        rtcflag = False
        print "Power wake up service will not available", sys.exc_info()
        print "Must run this utility as root -- or 'chmod o+r /dev/rtc' " \
                    "(others + readable)"
    
    if not os.path.isdir(ala_dir):
        os.makedirs(ala_dir)
    if not os.path.isdir(ala_old):
        os.makedirs(ala_old)
    if not os.path.isdir(ala_mis):
        os.makedirs(ala_mis)
        
    # Test it, bail out if no spool dir    
    if not os.path.isdir(ala_dir):
        print "Cannot access local storage"
        sys_exit(1)
        
    # We decorate the window with callbacks to separate logic
    mw = pyalalib.pyalawin.MainWin(rtcflag); mw.app_tick = app_tick
    mw.add_alarm = add_alarm
    mw.fill_spooler = fill_spooler 
    mw.fill_history = fill_history
    mw.fill_missed = fill_missed
    
    mw.listx.limit_row(20)

    # Restart apps in spool dir
    app_tick("b", "") 
    app_tick() 
    # Start monitoring
    gobject.timeout_add(scanagain * 1000, app_tick)
    
    gtk.main()
    sys.exit(0)


