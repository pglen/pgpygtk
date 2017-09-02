#!/usr/bin/env python

import os, sys, getopt, signal
import gobject, gtk

# ------------------------------------------------------------------------
# This is camera test for pg computer vision

# Start of program:

if __name__ == '__main__':

    opts = []; args = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:hfvxct")
    except getopt.GetoptError, err:
        print "Invalid option(s) on command line:", err
        sys.exit(1)

    print "pgvis camera test"
    
        
