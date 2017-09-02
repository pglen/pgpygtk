#!/usr/bin/env python

import os, sys, getopt, signal, string
import gobject, gtk, pango, subprocess
import random, time

# ------------------------------------------------------------------------
# Resolve path name, try windows paths too

def respath(fname):

    try:
        ppp = string.split(os.environ['PATH'], os.pathsep)
        for aa in ppp:
            ttt = aa + os.sep + fname
            if os.path.isfile(str(ttt)):
                return ttt
                
        # Try .exe suffix         
        for aa in ppp:
            ttt = aa + os.sep + fname + ".exe"
            if os.path.isfile(str(ttt)):
                return ttt
    except:
        print "Cannot resolve path", fname, sys.exc_info()   
        
    return None   

# ------------------------------------------------------------------------
# An N pixel vertical spacer. Default to 5.

class Spacer(gtk.Label):

    def __init__(self, sp = 5):
        gtk.Label.__init__(self)
        sp *= 1000
        self.set_markup("<span  size=\"" + str(sp) + "\"> </span>")
        
# ------------------------------------------------------------------------

class MainWin():

    def __init__(self):
    
        self.window = window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        
        window.set_title("Word Lookup")
        window.set_position(gtk.WIN_POS_CENTER)
        
        #ic = gtk.Image(); ic.set_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_BUTTON)
        #window.set_icon(ic.get_pixbuf())
        #www = gtk.gdk.screen_width(); hhh = gtk.gdk.screen_height();
        
        disp = gtk.gdk.display_get_default()
        scr = disp.get_default_screen()
        ptr = disp.get_pointer()
        mon = scr.get_monitor_at_point(ptr[1], ptr[2])
        geo = scr.get_monitor_geometry(mon)   
        www = geo.width; hhh = geo.height
        xxx = geo.x;     yyy = geo.y
        
        if www == 0:
            www = gtk.gdk.screen_width(); hhh = gtk.gdk.screen_height();
        
        window.set_default_size(7*www/9, 7*hhh/8)
        
        window.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
         
        window.set_events(  gtk.gdk.POINTER_MOTION_MASK |
                            gtk.gdk.POINTER_MOTION_HINT_MASK |
                            gtk.gdk.BUTTON_PRESS_MASK |
                            gtk.gdk.BUTTON_RELEASE_MASK |
                            gtk.gdk.KEY_PRESS_MASK |
                            gtk.gdk.KEY_RELEASE_MASK |
                            gtk.gdk.FOCUS_CHANGE_MASK )
         
        window.connect("destroy", self.OnExit)
        window.connect("key-press-event", self.key_press_event)        
        window.connect("button-press-event", self.button_press_event)        
        
        try:
            window.set_icon_from_file("icon.png")
        except:
            pass
        
        vbox = gtk.VBox(); 
        hbox = gtk.HBox();   hbox2 = gtk.HBox(); hbox3 = gtk.VBox()
        
        sp1 = Spacer()        
        lab3 = gtk.Label("  Enter Word: ");   hbox2.pack_start(lab3, False)
        self.entry = gtk.Entry();    hbox2.pack_start(self.entry, padding = 4)
        self.entry.connect("activate", self.lookup, window)
        
        butt3 = gtk.Button(" _Lookup ")
        butt3.connect("clicked", self.lookup, window)
        hbox2.pack_start(butt3, False, padding = 4)
        
        butt2 = gtk.Button(" E_xit ")
        butt2.connect("clicked", self.OnExit, window)
        hbox2.pack_start(butt2, False)

        lab4 = gtk.Label("  ");   hbox2.pack_start(lab4, False)
        
        #hbox3.set_spacing(4);  #hbox3.set_homogeneous(True)
        
        sc1 = gtk.ScrolledWindow()
        self.text1 = gtk.TextView();    self.text1.set_wrap_mode(True)  
        sc1.add_with_viewport(self.text1)
        hbox3.pack_start(sc1, True, True, padding = 4)
        
        sc2 = gtk.ScrolledWindow()
        self.text2 = gtk.TextView();    self.text2.set_wrap_mode(True)   
        sc2.add_with_viewport(self.text2)
        hbox3.pack_start(sc2, True, True, padding = 2)
        
        sc3 = gtk.ScrolledWindow()
        self.text3 = gtk.TextView();    self.text3.set_wrap_mode(True)   
        sc3.add_with_viewport(self.text3)
        hbox3.pack_start(sc3, True, True, padding = 2)

        sc4 = gtk.ScrolledWindow()
        self.text4 = gtk.TextView();    self.text4.set_wrap_mode(True)   
        sc4.add_with_viewport(self.text4)
        hbox3.pack_start(sc4, True, True, padding = 4)

        #hbox3.set_child_packing(self.text1, False, True, 4, gtk.PACK_START)
        
        lab1 = gtk.Label("");  hbox.pack_start(lab1)
        
        #butt1 = gtk.Button(" _New ")
        #butt1.connect("clicked", self.show_new, window)
        #hbox.pack_start(butt1, False)
        
        lab2 = gtk.Label("");  hbox.pack_start(lab2)
        
        vbox.pack_start(sp1, False)
        vbox.pack_start(hbox2, False)
        vbox.pack_start(hbox3)
        #vbox.pack_end(hbox, False)
        
        window.add(vbox)
        window.show_all()
        
    def lookup(self, win, butt):
        #print "Lookup", self.entry.get_text()
        pppx = []
        try:
            prog = respath("wn")
            pppx = [prog]
            pppx.append(self.entry.get_text())
            pppx.append("-over")
            out = subprocess.Popen(pppx, stdout=subprocess.PIPE).communicate()[0]
            if out == "":
                self.text1.get_buffer().set_text("No entry or incorrenct spelling")
            else:
                self.text1.get_buffer().set_text(out)
            
            out = ""
            for aa in "nvar":
                out += "(" + aa + ") "
                pppx = [prog]
                pppx.append(self.entry.get_text())
                pppx.append("-syns" + aa)
                out += subprocess.Popen(pppx, stdout=subprocess.PIPE).communicate()[0]
            self.text2.get_buffer().set_text(out)
            
            out = ""
            for aa in "nvar":
                out += "(" + aa + ") "
                pppx = [prog]
                pppx.append(self.entry.get_text())
                pppx.append("-ants" + aa)
                out += subprocess.Popen(pppx, stdout=subprocess.PIPE).communicate()[0]
            self.text3.get_buffer().set_text(out)

            out = ""
            for aa in "coorn", "coorv", "hypon", "hypov", "derin", "deriv", \
                    "meron", "holon", "perta", "attrn":
                pppx = [prog]
                pppx.append(self.entry.get_text())
                pppx.append("-" + aa)
                res = subprocess.Popen(pppx, stdout=subprocess.PIPE).communicate()[0]
                if res != "":
                    out += "----------------------------------------------------------- "
                    out += res
                
            self.text4.get_buffer().set_text(out)
     
        except: 
            print "Cannot execute", pppx, sys.exc_info()        
            self.text1.get_buffer().set_text("Cannot execute 'wn', please install it.")
            
        self.entry.grab_focus()
        
    def  OnExit(self, arg, srg2 = None):
        self.exit_all()
            
    def exit_all(self):
        gtk.main_quit()
            
    def key_press_event(self, win, event):
        #print "key_press_event", win, event
        pass
        
    def button_press_event(self, win, event):
        #print "button_press_event", win, event
        pass
            
# Start of program:

if __name__ == '__main__':

    mainwin = MainWin()    
    gtk.main()











