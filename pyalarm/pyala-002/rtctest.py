#!/usr/bin/env python

# ------------------------------------------------------------------------
# Python Alarm

import os, sys, getopt, signal, select, socket, time, struct
import random, stat, subprocess

import rtc

def readtime():

    aa = rtc.rtime()
    #print "time", aa
    aaa = list(aa)
    aaa.append(-1); aaa.append(-1);  aaa.append(-1)
    tt = time.mktime(aaa)
    return tt
    
def readwake():

    aa = rtc.rwake()
    #print "wake", aa
    aaa = list(aa[2:])
    aaa.append(-1); aaa.append(-1);  aaa.append(-1)
    tt = time.mktime(aaa)
    return tt
    
# ------------------------------------------------------------------------

def setwake(tt):

    ttt = time.localtime(tt)
    tstr = time.asctime(ttt)
    print "setwake", tstr, time.timezone / (60 * 60), time.tzname
    www = list((1, 1)); 
    for ii in range(6): www.append(ttt[ii])
    #print "www", www
    rtc.wwake(www)

if __name__ == '__main__':

    tz = time.timezone - time.daylight * 3600
    #print rtc.__doc__
    print "RTC module build date:", rtc.bdate()
    #print "RTC Interface Version:", rtc.version(0)
    tt = readtime() - tz 
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
    
    ttt = readwake() - tz 
    tstr = time.asctime(time.localtime(ttt))
    print "wake", tstr, time.timezone / (60 * 60), time.tzname
    
    setwake(tt + tz)
    
    tttt = readwake() - tz 
    tstr = time.asctime(time.localtime(tttt))
    print "wake", tstr, time.timezone / (60 * 60), time.tzname



