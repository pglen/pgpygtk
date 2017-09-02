#!/usr/bin/env python

import os, sys, getopt, signal
import gobject, gtk, pango

import random, time

import yellow

# ------------------------------------------------------------------------
# This is open source sticker program. Written in python. 


version = 1.0
verbose = False
# Where things are stored (backups, orgs, macros)
config_dir = os.path.expanduser("~/.pystick")


def help():

    print 
    print "PyStick version: ", version
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

# ------------------------------------------------------------------------

def OnExit(aa):
    gtk.main_quit()

def area_button(area, event):
    print "main butt"
    return False 

def key_press_event(area, event):
    
    print "main keypress" #, area, event
    
    if event.state & gtk.gdk.MOD1_MASK:       
        if event.keyval == gtk.keysyms.x or event.keyval == gtk.keysyms.X:
            sys.exit(0)    
                    
    #print area.get_focus()
    #area.propagate_key_event(event)
    return False
    
# Start of program:

if __name__ == '__main__':

    #for aa in gtk.gdk.Window.__dict__:
    #    print aa
        
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
        print "PyStick running on", "'" + os.name + "'", \
            "GTK", gtk.gtk_version, "PyGtk", gtk.pygtk_version

    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.set_title("Python Stickies")
    window.set_position(gtk.WIN_POS_CENTER)
    
    #ic = gtk.Image(); ic.set_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_BUTTON)
    #window.set_icon(ic.get_pixbuf())
    
    www = gtk.gdk.screen_width(); hhh = gtk.gdk.screen_height();
    window.set_default_size(www/2, hhh/2)
    
    window.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
     
    window.set_events(  gtk.gdk.POINTER_MOTION_MASK |
                    gtk.gdk.POINTER_MOTION_HINT_MASK |
                    gtk.gdk.BUTTON_PRESS_MASK |
                    gtk.gdk.BUTTON_RELEASE_MASK |
                    gtk.gdk.KEY_PRESS_MASK |
                    gtk.gdk.KEY_RELEASE_MASK |
                    gtk.gdk.FOCUS_CHANGE_MASK )
                    
    window.connect("destroy", OnExit)
    window.connect("key-press-event", key_press_event)        
    window.connect("button-press-event", area_button)        

    for aa in range(5):                        
        zz = yellow.stickWin(window, "Hello World", "This is a small sticky %d" % aa)
        
    yy = yellow.stickWin(window, "Hello World", "This is a sticky\n"
        "With new longer and longer and longer and longer and longer and longer and longer lines\n"
                        "Done.")

    #for aa in range(200):                        
    for aa in range(20):                        
        zz = yellow.stickWin(window, "Hello World2", "This is a small sticky %d" % aa)
    
    window.show_all()
        
    gtk.main()
    
    #print "PyStick ended."





