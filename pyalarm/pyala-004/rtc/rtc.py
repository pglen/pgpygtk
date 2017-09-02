#!/usr/bin/env python

# ------------------------------------------------------------------------
# Python RTC Alarm wrapper

import time, rtcx

# You may access the C module functions like:
# rtcx.verbose = 1

# Grab doc from "C", extend it

__doc__ = "\n" + rtcx.__doc__
__doc__ += \
"\n"            \
"Wrapper Functions:\n"  \
"\n"            \
"   readtime    - read RTC time. Returns seconds since epoch\n" \
"   readalarm   - read RTC alarm time. Returns seconds since epoch\n" \
"   readwake    - read RTC wake time. Returns seconds since epoch\n" \
"\n"            \

# Wrapper for the RTC module. All dates are in RTC timezone, which on
# UNIX is UTC. On Windows it is not UTC, so porting requires some
# tinkering. Some dual boot LINUX configs make the assumption of Windows is
# the primary OS, so the RTC is set to the windows RTC method (localtime).

# ------------------------------------------------------------------------
# Read RTC time, Return seconds since epoch.

def readtime():

    aa = rtcx.rtime()
    #print "time", aa
    aaa = list(aa)
    aaa.append(-1); aaa.append(-1);  aaa.append(-1)
    tt = time.mktime(aaa)
    return tt
    
# ------------------------------------------------------------------------
# Read RTC time, Return seconds since epoch.

def readalarm():

    aa = rtcx.ralarm()
    #print "time", aa
    aaa = list(aa)
    aaa.append(-1); aaa.append(-1);  aaa.append(-1)
    tt = time.mktime(aaa)
    return tt
    
# ------------------------------------------------------------------------
# Read RTC wake time, Return seconds since epoch.

def readwake():

    aa = rtcx.rwake()
    #print "wake", aa
    aaa = list(aa[2:])
    aaa.append(-1); aaa.append(-1);  aaa.append(-1)
    tt = time.mktime(aaa)
    return tt

# ------------------------------------------------------------------------
# Read RTC wake status, Return tuple of (active, triggered)

def readwakeflag():

    aa = rtcx.rwake()
    #print "wake", aa
    return aa[:2]

# ------------------------------------------------------------------------
# Set RTC wake time, argument in seconds since epoch.
# Pass time before NOW to cancel wake.

def setwake(tt):

    ttt = time.localtime(tt)
    #tstr = time.asctime(ttt)
    #print "setwake", tstr, time.timezone / (60 * 60), time.tzname
    www = list((1, 1)); 
    for ii in range(6): www.append(ttt[ii])
    #print "www", www
    rtcx.wwake(www)

# ------------------------------------------------------------------------

if __name__ == '__main__':

    import sys
    
    print 
    tz = time.timezone - time.daylight * 3600
    #print __doc__
    print "RTC module build date:", rtcx.bdate()
    print "RTC Interface Version:", rtcx.version()
    print 
    
    try:
        tt = readtime() - tz; 
    except:
        print sys.exc_info()
        sys.exit(0)
    
    tstr = time.asctime(time.localtime(tt))
    print "rtc time:  ", tstr, "tz:", time.timezone / (60 * 60), time.tzname
    tt = readalarm() - tz; tstr = time.asctime(time.localtime(tt))
    print "rtc alarm: ", tstr, "tz:", time.timezone / (60 * 60), time.tzname
    
    print


