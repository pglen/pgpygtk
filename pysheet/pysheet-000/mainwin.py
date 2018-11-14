#!/usr/bin/env python

import os, sys, getopt, signal, string
import gobject, gtk, pango, subprocess
import random, time, pickle

from datetime import *

from pgutil import  *

MAXPROJ = 12
picklefile = "pysheet.cfg"
logfile = "pysheet.txt"

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
        
        window.set_title("Project time sheets")
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
        
        window.set_default_size(www/3, hhh/3)
        
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
        
        vbox.pack_start(Spacer(), True)
        
        hboxarr = []; 
        self.entryarr = []; self.descarr = []; 
        self.notearr = []; self.imgarr = []
        self.countarr = []; self.flagarr = []
        self.cntarr = []; 
        
        for aa in range(MAXPROJ):
            hboxarr.append( self.create_row(aa))
            self.countarr.append(0); 
            self.flagarr.append(0)
            
        try:
            pfl = open(picklefile, "rb")
            entryarr2 = pickle.load(pfl)
            for bb in  range(len(entryarr2)):
                self.entryarr[bb].set_text(entryarr2[bb])
                
            descarr2 = pickle.load(pfl)
            for bb in  range(len(descarr2)):
                self.descarr[bb].set_text(descarr2[bb])
            pfl.close()
            
        except:
            print_exception("On loading project strings")
               
        # ------------------------------------------------------------------
        
        # Create exit button row
        xbox = gtk.HBox();
        butt2s = gtk.Button("   _Stop All     ")
        butt2s.connect("clicked", self.StopAll, window)
        
        butt2 = gtk.Button("   E_xit and Save    ")
        butt2.connect("clicked", self.OnExit, window)
        
        xbox.pack_start(gtk.Label(" "), True)
        xbox.pack_start(butt2s, False)
        xbox.pack_start(gtk.Label("       "), False)
        xbox.pack_start(butt2, False)
        xbox.pack_start(gtk.Label(" "), True)
        
        # Assemble hBoxes
        for aa in range(len(hboxarr)):
            vbox.pack_start(Spacer(), False)
            vbox.pack_start(hboxarr[aa], False)

        vbox.pack_start(Spacer(12), True)
        vbox.pack_start(xbox, False)
        vbox.pack_start(Spacer(), False)

        #vbox.pack_end(hbox, False)
        
        window.add(vbox)
        window.show_all()
        
        lfp = None
        try:
            lfp = open(logfile, "at")
        except:
            print_exception("On opening logfile")
    
        ddd = datetime.today(); dstr = ddd.strftime("%d/%m/%Y %H:%M:%S")
        dord = ddd.toordinal()
        
        try:
            logstr = "%s (%s) Started pysheet.\n" % (dstr, dord)
            lfp.write(logstr)
        except:
            print_exception("On appending startup entry")
        
        # We use gobj instead of SIGALRM, so it is more multi platform
        gobject.timeout_add(1000, self.handler_tick)
        
    def action2(self, win, row):
        #print "action2", row
        self.imgarr[row].set_from_stock(gtk.STOCK_INFO, gtk.ICON_SIZE_BUTTON)
        self.flagarr[row] = 0
        
    def action(self, win, row):
        #print "action", row
        self.imgarr[row].set_from_stock(gtk.STOCK_APPLY, gtk.ICON_SIZE_BUTTON)
        self.flagarr[row] = 1
        
    def  OnExit(self, arg, srg2 = None):
    
        lfp = None
        try:
            lfp = open(logfile, "at")
        except:
            print_exception("On appending results")
    
        ddd = datetime.today()
        dstr = ddd.strftime("%d/%m/%Y %H:%M:%S")
        dord = ddd.toordinal()
        try:
            for aa in range(MAXPROJ):
                if self.countarr[aa]:
                    cc = self.countarr[aa]
                    #print self.entryarr[aa].get_text(), "   ", 
                    #print aa, ":  ", self.countarr[aa], "sec"
                    hhh = cc / 3600 
                    mmm = (cc % 3600) / 60
                    sss = (cc % 60)
                    
                    logstr2 = "%s (%d) %02d:%02d:%02d in project %s (%d)\n" % \
                        (dstr, dord, hhh, mmm, sss, self.entryarr[aa].get_text(), aa) 
                    lfp.write(logstr2)
                    
            logstr = "%s (%s) Exited pysheet.\n" % (dstr, ddd.toordinal())
            lfp.write(logstr)
            
            lfp.close()
        except:
            print_exception("On saving results")
          
        try:
            pfh = open(picklefile, "wb")
            txtarr = []
            for bb in self.entryarr:
                txtarr.append(bb.get_text())    
            pickle.dump(txtarr, pfh);
            
            txtarr = []
            for bb in self.descarr:
                txtarr.append(bb.get_text())    
            pickle.dump(txtarr, pfh);
            pfh.close()
            
        except:
            print_exception("On pickle")
        
                                                        
        self.exit_all()
   
    def  StopAll(self, arg, srg2 = None):
        for aa in range(MAXPROJ):
            self.imgarr[aa].set_from_stock(gtk.STOCK_INFO, gtk.ICON_SIZE_BUTTON)
            
    def exit_all(self):
        gtk.main_quit()
            
    def key_press_event(self, win, event):
        #print "key_press_event", win, event
        pass
        
    def button_press_event(self, win, event):
        #print "button_press_event", win, event
        pass

    def create_row(self, row):

        hbox2 = gtk.HBox();
        lab3a = gtk.Label("     ");   hbox2.pack_start(lab3a, False)
        
        lab3d = gtk.Image();   
        lab3d.set_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_BUTTON)
        hbox2.pack_start(lab3d, False)
        self.imgarr.append(lab3d)
        
        lab3 = gtk.Label(" Project: ");   hbox2.pack_start(lab3, False)
        entry = gtk.Entry();    hbox2.pack_start(entry, padding = 4)
        self.entryarr.append(entry)
        
        lab3a = gtk.Label(" Description: ");   hbox2.pack_start(lab3a, False)
        desc = gtk.Entry();    hbox2.pack_start(desc, padding = 4)
        self.descarr.append(desc)
        
        lab3c = gtk.Label("  Note: ");   hbox2.pack_start(lab3c, False)
        note = gtk.Entry();    hbox2.pack_start(note, True, padding = 4)
        self.notearr.append(note)
        
        lab3e = gtk.Label("  00:00:00  ");  hbox2.pack_start(lab3e, False)
        self.cntarr.append(lab3e)
        
        if row < 9:
            sstr = "     Start _%-2d     " % (row + 1)
        else:
            sstr = "     Start  %-2d     " % (row + 1)  
            
        butt3 = gtk.Button(sstr)
        butt3.connect("clicked", self.action, row)
        hbox2.pack_start(butt3, False, padding = 4)
        
        butt3a = gtk.Button("     Stop      ")
        butt3a.connect("clicked", self.action2, row)
        hbox2.pack_start(butt3a, False, padding = 4)
        
        lab3b = gtk.Label("     ");   hbox2.pack_start(lab3b, False)
        
        return hbox2
    
    def handler_tick(self):
        global cnt
        for aa in range(MAXPROJ):
            #print self.entryarr[aa].get_text(),
            if self.flagarr[aa]:
                self.countarr[aa] = self.countarr[aa] + 1
                
        if cnt % 10 == 0:
            for aa in range(MAXPROJ):
                if self.flagarr[aa]:
                    cc = self.countarr[aa]
                    hhh = cc / 3600 
                    mmm = (cc % 3600) / 60
                    sss = (cc % 60)
                    xxx = "  %02d:%02d:%02d   " % (hhh, mmm, sss)
                    #print xxx 
                    self.cntarr[aa].set_text(xxx)
        
        cnt += 1                          
        gobject.timeout_add(1000, self.handler_tick)

cnt = 0
   
# EOF

