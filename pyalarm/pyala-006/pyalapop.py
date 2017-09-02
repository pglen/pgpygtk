#!/usr/bin/env python

# ------------------------------------------------------------------------
# Python Alarm. Pop up window and execute instructions.

import os, sys, getopt, signal, subprocess
import gobject, gtk, pango, random, time, warnings
  
from pyalalib.pgutil import *

class Blank():
    def __init__(self):
        self.date = ""
        self.name = ""
        self.act = ""
        self.exe = ""
        self.arg = "" 
        self.play  = ""

def parseline(strx, pobj):
    #print "strx", strx
    if strx[0].startswith("#"):
        return
        
    if strx[0] == "DATE":
        #print "   alarm date", strx[1]
        pobj.date = strx[1]
        return
        
    if strx[0] == "NAME":
        #print "   alarm name", strx[1]
        pobj.name = strx[1]
        return
        
    if strx[0] == "EXE":
        #print "   alarm exe", strx[1]
        pobj.exe = strx[1]
        return
    
    if strx[0] == "ARG":
        #print "   alarm arg", strx[1]
        pobj.arg = strx[1]
        return
    
    if strx[0] == "PLAY":
        #print "   alarm arg", strx[1]
        pobj.play = strx[1]
        return
        
    if strx[0] == "ACTION":
        #print "   alarm arg", strx[1]
        pobj.act = strx[1]
        return

def idle_tick(dialog):
    #dialog.
    sys.exit(0)

def action_tick(dialog):

    if dialog.pobj.exe:
        #print "exe", dialog.pobj.exe
        try:
            ret = subprocess.Popen([dialog.pobj.exe], shell = True)
        except:    
            print "Cannot execute play subprocess", sys.exc_info()
        
# ------------------------------------------------------------------------

def newala(strx = ""):
    
    now = time.localtime()
    
    dialog = gtk.Dialog("Alarm Progress",
               None,
               gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
               #(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
               # gtk.STOCK_OK, gtk.RESPONSE_ACCEPT)
                )
                
    try:
        dialog.set_icon_from_file("/usr/share/pyala/ala2.png")
    except:
        pass

    www = gtk.gdk.screen_width(); hhh = gtk.gdk.screen_height();
    dialog.set_default_size(www/4, hhh/4)
    
    # Don't bother the user
    dialog.set_focus_on_map(False)
    
    #dialog.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_TOOLBAR)
    dialog.set_default_response(gtk.RESPONSE_ACCEPT)

    dialog.pobj = Blank()    
    if strx:
        try:
            ff = open(strx, "r").read()
            fff = ff.split("\n")
            for aa in fff:
                aaa = aa.split("=")
                bbb = []
                for cc in aaa:
                    bbb.append(cc.strip())
                if len(bbb):
                    parseline(bbb, dialog.pobj)
        except:
            print "Cannot read file", sys.exc_info()
            pass
        
    hbox5 = gtk.HBox()
    add_spacer(hbox5)
    dialog.vbox.pack_start(hbox5, True)

    add_field(dialog.pobj.date, "Date: ", dialog)
    add_field(dialog.pobj.name, "Name: ", dialog)
    add_field(dialog.pobj.exe,  "Exe:  ", dialog)
    
    hbox3 = gtk.HBox()
    add_spacer(hbox3)
    dialog.vbox.pack_start(hbox3, True)

    # Done loading, shift name to reflect delete status    
    if strx != "":
        fourdir, fourname  = os.path.split(strx)
        #print "fourdir", fourdir, fourname
        
        newdir = fourdir + "/../history/"
        try:
            if not os.path.isdir(newdir):
                os.mkdir(newdir)
        except: 
            #print "Cannot create dir",  newdir, sys.exc_info()
            pass
        
        fourfile = "d" + os.path.basename(strx)[1:]
        try:
            os.rename(strx, newdir + fourfile)
        except:
            #print "Cannot rename file", strx, newdir + fourfile, sys.exc_info()
            pass
            
    dialog.show_all()
    gobject.timeout_add(10, mod_pos, dialog)
    gobject.timeout_add(10000, idle_tick, dialog)
    gobject.timeout_add(100, action_tick, dialog)
    
    response = dialog.run()   
    dialog.destroy()
    
    if response != gtk.RESPONSE_ACCEPT:   
        return False
    return True
    
# Wait for the window to display, modulate by random number    
    
def mod_pos(dialog):
    for aa in range(2000):
        if dialog.window.is_visible():
            break
        else:
            pgutils.usleep(10)
            cnt += 1
            
    # Modulate position
    xx, yy = dialog.window.get_position()
    xx += 100 * random.random() - 50
    yy += 100 * random.random() - 50
    dialog.move(int(xx), int(yy))
    
# ------------------------------------------------------------------------
# Add a text field

def add_spacer(hbox):
    label = gtk.Label("   ");
    hbox.pack_start(label, False)
    return label
    
def add_field(strx, label, dialog):

    label1  = gtk.Label("   ");   
    label2a = gtk.Label(label) 
    label2  = gtk.Label(strx) 
    label3  = gtk.Label("   ") 
    hbox = gtk.HBox()
    hbox.pack_start(label1, False)  
    hbox.pack_start(label2a, False)  
    hbox.pack_start(label2)  
    hbox.pack_start(label3, False)  
    dialog.vbox.pack_start(hbox)
    
# For testing
if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.argv.append("")
    newala(sys.argv[1])
    










