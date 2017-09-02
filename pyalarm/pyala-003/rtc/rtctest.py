#!/usr/bin/env python

# ------------------------------------------------------------------------
# Python Alarm

import os, sys, getopt, signal, select, socket, time, struct
import random, stat, subprocess

import rtc

#print rtc.__doc__

if __name__ == '__main__':

    tz = time.timezone - time.daylight * 3600
    #print rtc.__doc__
    print "RTC module build date:", rtc.rtcx.bdate()
    #print "RTC Interface Version:", rtc.rtcx.version(0)
    tt = rtc.readtime() - tz 
    tstr = time.asctime(time.localtime(tt))
    print "time", tstr, time.timezone / (60 * 60), time.tzname
            
    #aaa[4] -= 3
    #rtc.wtime(aaa)
    #aa = rtc.rtime()
    #print "new", aa
    
    #aa3 = rtc.ralarm()
    #print "alarm", aa3
    #aaa3 = list(aa3); aaa3[3] += 3
    #rtc.walarm(aaa3)
    #aa4 = rtc.ralarm()
    #print "alarm", aa4
    #rtc.alarm(False)
    
    ttt = rtc.readwake() - tz 
    tstr = time.asctime(time.localtime(ttt))
    print "wake", tstr, time.timezone / (60 * 60), time.tzname
    
    rtc.setwake(tt + 30 + tz)
    
    tttt = rtc.readwake() - tz 
    tstr = time.asctime(time.localtime(tttt))
    print "wake", tstr, time.timezone / (60 * 60), time.tzname

    print "wakeflag", rtc.readwakeflag()





