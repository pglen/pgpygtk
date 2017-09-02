#!/usr/bin/env python

import os, sys, getopt, signal, select
import gobject, gtk, pango

import pypossql

# ------------------------------------------------------------------------
# This is open source sticker program. Written in python. 

GAP = 4                 # Gap in pixels
TABSTOP = 4
FGCOLOR  = "#000000"
BGCOLOR  = "#ffff88"              

sdev = "/dev/ttyS0"
fd = None

version = 1.0
verbose = False

# Where things are stored (backups, orgs, macros)
config_dir = os.path.expanduser("~/.pypos")

# ------------------------------------------------------------------------
#

class BarWin():

    def __init__(self):
        
        www = gtk.gdk.screen_width(); hhh = gtk.gdk.screen_height();
    
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_default_size(3*www/4, 3*hhh/4)
        window.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
        window.connect("destroy", OnExit)
            
        vbox = gtk.VBox(); 
        
        butt1 = gtk.Button(" E_xit ")
        butt1.connect("clicked", self.click_ok, window)
        vbox.pack_end(butt1, False)
        
        self.vspacer(vbox) 
        vbox.pack_start(self.header("  Bar Code:"), False )
        self.vspacer(vbox) 
        
        hbox = gtk.HBox(); 
        vbox.pack_start(hbox, False)
        self.barcode = gtk.Entry();
        self.spacer(hbox) 
        hbox.add(self.barcode)
        self.spacer(hbox) 
        
        self.vspacer(vbox) 
        vbox.pack_start(self.header("  Item:"), False )
        self.vspacer(vbox) 
        
        hbox4 = gtk.HBox(); 
        vbox.pack_start(hbox4, False)
        self.item = gtk.Entry();
        self.spacer(hbox4) 
        hbox4.add(self.item)
        self.spacer(hbox4) 
        
        self.vspacer(vbox) 
        vbox.pack_start(self.header("  Description:"), False )
        self.vspacer(vbox) 
        
        hbox5 = gtk.HBox(); 
        self.desc = gtk.TextView();
        self.desc.set_border_width(8)
        
        sw = gtk.ScrolledWindow()
        sw.add(self.desc)
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.spacer(hbox5) 
        hbox5.add(sw)
        vbox.pack_start(hbox5, False)
        self.spacer(hbox5) 
        
        # ---------------------------------------------------------------  
        window.add(vbox)
        window.show_all()
    
    def click_ok(self, win, aa):
        gtk.main_quit()
        pass
        
    def header(self, xstr):
        lab3 = gtk.Label(xstr)
        hbox3 = gtk.HBox(); hbox3.pack_start(lab3, False )
        return hbox3
        
    def spacer(self, hbox, xstr = "    "):
        lab = gtk.Label(xstr)
        hbox.pack_start(lab, False )
       
    def vspacer(self, vbox):
        lab = gtk.Label(" ")
        vbox.pack_start(lab, False )

    def newcode(self, line):
        self.barcode.set_text(line)
        print posdb.get(line)
        self.item.set_text("This is item '" + line + "'")
  
              
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


def OpenSerial(*par):
    global fd, sdev
    print "Using device:", sdev
    try:
        fd = open (sdev, "rb", 1)
    except:
        print "cannot open ", sdev
        return
    
    '''try:
        while True:    
            line = fd.readline() 
            print line
    except:
        print "ended exc"
         
    print "Ended thread"'''
    
# ------------------------------------------------------------------------

tick = 0

def handler_tick():

    global mainwin, fd, tick
    
    tick += 1
    
    #if tick % 10 == 0:
    #    print 'handler called', fd.fileno(), tick
        
    # See if file descriptor has data:
    sel = select.select( (fd,), (), (), 0)
    if sel[0]:
        #print sel
        line = fd.readline() 
        #for aa in line:
        #    print ord(aa),
        #print
            
        line = line.replace("\r", "").replace("\n", "")
        #print line
        if line != "":
            mainwin.newcode(line)
        
    gobject.timeout_add(100, handler_tick)

# Start of program:

if __name__ == '__main__':

    global mainwin, posdb
    
    try:
        if not os.path.isdir(config_dir):
            os.mkdir(config_dir)
    except: pass
    
    # Let the user know it needs fixin'
    if not os.path.isdir(config_dir):
        print "Cannot access config dir:", config_dir
        sys.exit(1)

    posdb = pypossql.Possql(config_dir + "/data")

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

    OpenSerial()
    
    # Poll the serial port of the scanner
    gobject.timeout_add(200, handler_tick)

    mainwin = BarWin()
    
    gtk.main()


