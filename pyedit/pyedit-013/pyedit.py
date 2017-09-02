#!/usr/bin/env python

# ------------------------------------------------------------------------
# This is open source editor. The motivation for this project was to create a 
# modern multi-platform editor. Simple, powerful, configurable, extendable.
# It has macro recording/play, search/replace, functional navigation,
# comment/string spell check, auto backup, persistent undo/redo, 
# auto complete, auto correct, ... and a lot more. It is fast.
# It is extendable, as python lends itself to easy tinkering. The editor
# has a table driven key mapping. One can easily edit the key map in 
# keyhand.py, and the key actions in acthand.py
# The default key map resembles gedit / wed / etp / brief
# ASCII only, fixed font only. For now ... Requires pygtk.

import os, sys, getopt, signal
import gobject, gtk
# gconf

import pyedlib.keyhand, pyedlib.acthand
import pyedlib.pedutil, pyedlib.pedwin
import pyedlib.pedconfig, pyedlib.pedsql

mainwin = None
show_timing = 0
show_config = 0

# ------------------------------------------------------------------------

def main(strarr):

    print "PyEdit running on", "'" + os.name + "'", \
        "GTK", gtk.gtk_version, "PyGtk", gtk.pygtk_version

    #print sys.stdin
    #print sys.stdout, sys.stderr
    
    signal.signal(signal.SIGTERM, terminate)

    #signal.signal(signal.SIGQUIT, interrupt)
    #print "Signals trapped."

    mainwin = pyedlib.pedwin.EdMainWindow(None, None, strarr)
    pyedlib.pedconfig.conf.pedwin = mainwin 
    
    gtk.main()
     
def help():

    print "Usage: " + sys.argv[0] + " [options] filename"
    print "Options are:"
    print "            -d level  - Debug level (1-10)"
    print "            -v        - Verbose"
    print "            -f        - Full screen"
    print "            -c        - Dump config"
    print "            -h        - Help"
    print

# ------------------------------------------------------------------------

def terminate(arg1, arg2):

    print "Terminating pyedit.py, saving files to ~/pyedit"
    # Save all     
    pyedlib.pedconfig.conf.pedwin.activate_quit(None)    
    #return signal.SIG_IGN

def interrupt(arg1, arg2):
    print "interrupt", arg1

if __name__ == '__main__':

    opts = []; args = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:hfvct")
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
        if aa[0] == "-f": pyedlib.pedconfig.conf.full_screen = True
        if aa[0] == "-v": verbose = True            
        if aa[0] == "-c": show_config = True            
        if aa[0] == "-t": show_timing = True
    
    try:
        if not os.path.isdir(pyedlib.pedconfig.conf.config_dir):
            #print "making", pyedlib.pedconfig.con.config_dir
            os.mkdir(pyedlib.pedconfig.conf.config_dir)
    except: pass
    
    # Let the user know it needs fixin'
    if not os.path.isdir(pyedlib.pedconfig.conf.config_dir):
        print "Cannot access config dir:", pyedlib.pedconfig.conf.config_dir
        sys.exit(1)

    if not os.path.isdir(pyedlib.pedconfig.conf.data_dir):
        #print "making", pyedlib.pedconfig.con.data_dir
        os.mkdir(pyedlib.pedconfig.conf.data_dir)
         
    if not os.path.isdir(pyedlib.pedconfig.conf.macro_dir):
        #print "making", pyedlib.pedconfig.con.macro_dir
        os.mkdir(pyedlib.pedconfig.conf.macro_dir)
    
    # Initialize GConf to load / save preferences & other info    
    '''try:
        gconf_client = gconf.client_get_default()		
        gconf_client.set_string(pyedlib.pedconfig.conf.config_reg + \
             "/default", "default")
    except: pass'''
   
    # Initialize sqlite to load / save preferences & other info    
    sql = pyedlib.pedsql.pedsql(pyedlib.pedconfig.conf.sql_data)
        
    # Initialize pedconfig for use  
    pyedlib.pedconfig.conf.sql = sql
    pyedlib.pedconfig.conf.keyh = pyedlib.keyhand.KeyHand()

    # To clear all config vars
    #sql.rmall()        

    sql.put("test", "1234")    
    # To check all config vars
    if show_config:    
        print "Dumping configuration:"
        ss = sql.getall(); 
        for aa in ss: 
            print aa
                       
    main(args[0:])

    #print sql.take
        
# EOF






