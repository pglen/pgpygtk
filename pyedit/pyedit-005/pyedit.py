#!/usr/bin/env python

import os, sys, gobject, gtk, getopt, gconf

import pedwin, pedconfig

config_dir  = None
config_file = "defaults"

# ------------------------------------------------------------------------

def main(strarr):

    #print strarr
    mw = pedwin.EdMainWindow(None, None, strarr)
    pedconfig.pedconfig.pedwin = mw
    gtk.main()
     
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

        if aa[0] == "-h": help();  exit(1)

        if aa[0] == "-f": pedconfig.pedconfig.full_screen = True
        ''''if aa[0] == "-v": verbose = True            
        if aa[0] == "-x": show_lexer = True
        if aa[0] == "-t": show_timing = True'''

    config_dir = os.path.expanduser("~/.pyedit")
    if not os.path.isdir(config_dir):
        print "making", config_dir
        os.mkdir(config_dir)

    #if not os.path.isdir(config_dir):
    #    print "Cannot access config dir:", config_dir
    #    sys.exit(1)
    
    cfile = config_dir + "/" + config_file
    #print cfile

    # Initialize GConf to load / save preferences & other saved info    
    gconf_client = gconf.client_get_default()		
    gconf_client.set_string("/apps/pyedit/default", "default")
    gconf_client.set_int("/apps/pyedit/pos1", 100)

    #strx = gconf_client.get_string("/apps/pyedit/default")
    #print strx
    #pos1 = gconf_client.get_int("/apps/pyedit/pos1")
    #print pos1

    #sys.exit(0)

    strx = args[0:]
    
    main(strx)

