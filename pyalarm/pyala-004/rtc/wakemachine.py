#!/usr/bin/env python

# ------------------------------------------------------------------------
# Python Alarm

import os, sys, getopt, signal, select, socket, time, struct
import random, stat, subprocess

import rtc

if __name__ == '__main__':

    prog = os.path.basename(sys.argv[0])
    
    # Check for correct values
    if len(sys.argv) < 2:
        print "Usage: ", prog, "minutes"
        sys.exit(0)
    plus = int(sys.argv[1])
    if plus < 0:
        print prog + ":", "'minutes' argument must be a positive integer."
        sys.exit(0)
        
    tz = time.timezone - time.daylight * 3600
    
    tt = rtc.readtime() - tz 
    tstr = time.asctime(time.localtime(tt))
    print "Current RTC time ", tstr

    tttt = rtc.readwake() - tz 
    tstr = time.asctime(time.localtime(tttt))
    print "Current RTC wake ", tstr
    
    rtc.setwake(tt + tz + plus * 60)
    
    tttt = rtc.readwake() - tz 
    tstr = time.asctime(time.localtime(tttt))
    print "New RTC wake     ", tstr
    
    print "wakeflag", rtc.readwakeflag()
    





