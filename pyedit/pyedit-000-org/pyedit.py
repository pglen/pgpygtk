#!/usr/bin/env python

import sys
import gobject, gtk
import pedwin
import getopt

# ------------------------------------------------------------------------

def main(strx):

    try:
        f = open(strx)
    except:
        strerr = "File:  '" + strx + "'  must be an existing and readble file. "
        print strerr
        sys.exit(1)
    
    try:
        buff = f.read();
    except:
        strerr2 =  "Cannot read file '" + strx + "'"
        print strerr2
        sys.exit(1)
    
    f.close()

    mw = pedwin.AppMainWindow(buff, strx)

    #print "Started App"
    gtk.main()
    #print "Exited app"
     

def help():
    print "Usage: " + sys.argv[0] + " [options] filename"
    print "Options are:"
    print "            -d level  - Debug level (1-10)"
    print "            -v        - Verbose"
    print "            -f        - Full screen"
    print "            -h        - Help"
    print

if __name__ == '__main__':

    
    opts = []; args = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:vhxft")
    except getopt.GetoptError, err:
        print "Invalid option(s) on command line:", err
        sys.exit(1)

    #print "opts", opts, "args", args
    
    for aa in opts:
        if aa[0] == "-d":
            try:
                pgdebug = int(aa[1])
            except:
                pgdebug = 0

        ''''if aa[0] == "-v": verbose = True            
        if aa[0] == "-h": help();  exit(1)
        if aa[0] == "-x": show_lexer = True
        if aa[0] == "-f": full_screen = True
        if aa[0] == "-t": show_timing = True'''

    try:
        strx = args[0]
    except:
        help(); exit(1)

    main(strx)

