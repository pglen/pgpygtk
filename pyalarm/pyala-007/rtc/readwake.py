#!/usr/bin/env python

# ------------------------------------------------------------------------
# Python RTC utility

import sys, time

import rtc

if __name__ == '__main__':

    tz = time.timezone - time.daylight * 3600
    
    tt = rtc.readtime() - tz; 
    tstr = time.asctime(time.localtime(tt))
    print "RTC time:   ", tstr

    ss = time.time()
    tstr = time.asctime(time.localtime(ss))
    print "Sys time:   ", tstr

    tttt = rtc.readwake() - tz 
    tstr = time.asctime(time.localtime(tttt))
    print "Wake time:  ", tstr
    print "Wake flag:  ", rtc.readwakeflag()




