#!/usr/bin/env python

import os, sys, getopt, signal
import gobject, gtk, pango

# ------------------------------------------------------------------------
# This is open source sticker program. Written in python. 

GAP = 4                 # Gap in pixels
TABSTOP = 4
FGCOLOR  = "#000000"
BGCOLOR  = "#ffff88"              

version = 1.0
verbose = False
# Where things are stored (backups, orgs, macros)
config_dir = os.path.expanduser("~/.pypos")

def OnExit(win):
    gtk.main_quit()

def help():

    print 
    print "Pypos version: ", version
    print 
    print "Usage: " + os.path.basename(sys.argv[0]) + " [options] [[filename] ... [filenameN]]"
    print 
    print "Options:"
    print 
    print "            -d level  - Debug level 1-10. (Limited implementation)"
    print "            -v        - Verbose (to stdout and log)"
    print "            -c        - Dump Config"
    print "            -h        - Help"
    print

def area_motion(self, area, event):    
    print "window motion event", event.state, event.x, event.y        
    if event.state & gtk.gdk.BUTTON1_MASK:            
        print "drag"

# Start of program:

if __name__ == '__main__':

    try:
        if not os.path.isdir(config_dir):
            os.mkdir(config_dir)
    except: pass
    
    # Let the user know it needs fixin'
    if not os.path.isdir(config_dir):
        print "Cannot access config dir:", config_dir
        sys.exit(1)

    opts = []; args = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hv")
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
        if aa[0] == "-v": verbose = True            
        #if aa[0] == "-x": clear_config = True            
        #if aa[0] == "-c": show_config = True            
        #if aa[0] == "-t": show_timing = True

    if verbose:
        print "PyPos running on", "'" + os.name + "'", \
            "GTK", gtk.gtk_version, "PyGtk", gtk.pygtk_version

    www = gtk.gdk.screen_width(); hhh = gtk.gdk.screen_height();

    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    #window.set_decorated(False)
    window.set_position(gtk.WIN_POS_CENTER)
    window.set_default_size(3*www/4, 3*hhh/4)
    window.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
    window.connect("destroy", OnExit)
     
    window.show_all()
           
    gtk.main()






