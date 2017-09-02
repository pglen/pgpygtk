#!/usr/bin/env python

# ------------------------------------------------------------------------
# This is open source. The motivation for this project was to create a 
# modern multi platform editor. Simple, powerful, configurable, extendable.
# It has macro recording/play, search/replace, functional navigation.
# It is extendable because python lends itself to easy tinkering, and
# the editor itself has a table driven key maping. 
# You can easily edit the key map in keyhand.py, actions in acthand.py
# The default keymap resembles gedit/wed/etp/brief
# ASCII only for now. Requires pygtk.

import os, sys, getopt, signal
import gobject, gtk, gconf

import pedutil, pedwin, pedconfig

mainwin = None

# ------------------------------------------------------------------------

def main(strarr):

    #print "Running gtk", gtk.gtk_version, "Pygtk", gtk.pygtk_version

    signal.signal(signal.SIGTERM, terminate)
    #signal.signal(signal.SIGHUP, terminate)
    #signal.signal(signal.SIGINT, interrupt)
    #signal.signal(signal.SIGQUIT, interrupt)
    
    #print "Signals trapped."

    mainwin = pedwin.EdMainWindow(None, None, strarr)
    pedconfig.conf.pedwin = mainwin 
    
    gtk.main()
     
def help():
    print "Usage: " + sys.argv[0] + " [options] filename"
    print "Options are:"
    print "            -d level  - Debug level (1-10)"
    print "            -v        - Verbose"
    print "            -f        - Full screen"
    print "            -h        - Help"
    print

# ------------------------------------------------------------------------

def terminate(arg1, arg2):
    print "Terminating pyedit.py, saving files to ~/pyedit"
    # Save all     
    pedconfig.conf.pedwin.activate_quit(None)    
    #return signal.SIG_IGN

def interrupt(arg1, arg2):
    print "interrupt", arg1

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

        if aa[0] == "-f": pedconfig.conf.full_screen = True
        ''''if aa[0] == "-v": verbose = True            
        if aa[0] == "-x": show_lexer = True
        if aa[0] == "-t": show_timing = True'''
    
    if not os.path.isdir(pedconfig.conf.config_dir):
        #print "making", pedconfig.con.config_dir
        os.mkdir(pedconfig.conf.config_dir)

    # Let the user know if it needs fixin
    if not os.path.isdir(pedconfig.conf.config_dir):
        print "Cannot access config dir:", pedconfig.conf.config_dir
        sys.exit(1)
    
    cfile = pedconfig.conf.config_dir + "/" + \
                    pedconfig.conf.config_file
    #print cfile

    # Initialize GConf to load / save preferences & other saved info    
    gconf_client = gconf.client_get_default()		
    gconf_client.set_string(pedconfig.conf.config_reg + \
         "/default", "default")
       
    main(args[0:])
    
#EOF

