#!/usr/bin/env python

# ------------------------------------------------------------------------

import os, sys, getopt, signal, subprocess
import gobject, gtk

# Start of program:

if __name__ == '__main__':
    print "Player"
    ret = subprocess.Popen(["totem", "--replace ",])
    ret = subprocess.Popen(["totem", "--play",])

    

