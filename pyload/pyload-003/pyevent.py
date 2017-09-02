#!/usr/bin/env python

import os, sys, glob, getopt, time, string, signal, stat, shutil
import gobject, gtk, pango, math, traceback, subprocess, thread

def run_thread(fd):
    global count
    print "Started thread"
    while 1:
        buff = fd.read(48)
        count += 1

# ------------------------------------------------------------------------
# Start of program:

if __name__ == '__main__':

    print "Event capture"

    global count
    
    count = 1
    drv = "/dev/input/event3"
    ddd = "/dev/input/by-path"
    # Find the driver
    dl = os.listdir(ddd)
    for aa in dl:
        if aa.find("kbd") >= 0:
            drv = ddd + "/" + aa
            break
            
    # Cycle on event buffer
    fd = open(drv, "r")
    tid = thread.start_new_thread(run_thread, (fd,))
    old_count = 0; idle_count = 0
    
    while 1:    
        time.sleep(1)
        print "count =", count
        if count == old_count:
            idle_count += 1
        else:
            idle_count = 0
       
        if idle_count > 10:
            print "IDLE"
            
        old_count = count

