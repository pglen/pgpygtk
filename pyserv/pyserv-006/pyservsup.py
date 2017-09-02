#!/usr/bin/env python

import os, sys, getopt, signal, select, string, time
import traceback

# ------------------------------------------------------------------------
# A more informative exception print 
 
def put_debug(xstr):
    try:
        if os.isatty(sys.stdout.fileno()):
            print xstr
        else:
            syslog.syslog(xstr)
    except:
        print "Failed on debug output."
        print sys.exc_info()

def put_exception(xstr):

    cumm = xstr + " "
    a,b,c = sys.exc_info()
    if a != None:
        cumm += str(a) + " " + str(b) + "\n"
        try:
            #cumm += str(traceback.format_tb(c, 10))
            ttt = traceback.extract_tb(c)
            for aa in ttt: 
                cumm += "File: " + os.path.basename(aa[0]) + \
                        " Line: " + str(aa[1]) + "\n" +  \
                    "   Context: " + aa[2] + " -> " + aa[3] + "\n"
        except:
            print "Could not print trace stack. ", sys.exc_info()
            
    put_debug(cumm)    
    #syslog.syslog("%s %s %s" % (xstr, a, b))

# ------------------------------------------------------------------------
# Helper functions.
# Escape spaces to %20

def escape(strx):
    aaa = strx.replace("%", "%%")
    aaa = aaa.replace(" ", "%20")
    return aaa
    
# ------------------------------------------------------------------------
# Remove dup //

def dirclean(strx):
    rrr = ""; aaa = strx.split("/")
    for aa in aaa:
        if aa != "": rrr += "/" + aa
    return rrr    

# ------------------------------------------------------------------------
# Change directory to up (..)

def chup(strx):
    # Stage 1: clean
    rrr2 = ""; rrr = dirclean(strx)
    # Stage 2: cut end
    for aa in rrr.split("/")[:-1]: 
        rrr2 += "/" + aa
    return rrr2



