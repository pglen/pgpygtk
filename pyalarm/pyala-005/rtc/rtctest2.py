#!/usr/bin/env python

# ------------------------------------------------------------------------
# Python Alarm

import os, sys, getopt, signal, select, socket, time, struct
import random, stat, subprocess

import rtc

if __name__ == '__main__':

    tz = time.timezone - time.daylight * 3600
    #print rtc.__doc__
    print "RTC module build date:", rtc.rtcx.bdate()
    #print "RTC Interface Version:", rtc.rtcx.version(0)
    tt = rtc.readtime() - tz 
    tstr = time.asctime(time.localtime(tt))
    print "time", tstr, time.timezone / (60 * 60), time.tzname
            



