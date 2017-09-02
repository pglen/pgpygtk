#!/usr/bin/env python

import os, sys, getopt, signal
import gobject, gtk, pango
import random, time

from pgutil import  *
import pyaladlg
import pyalalist
import pyalaclock

# ------------------------------------------------------------------------

class MainWin(gtk.Window):

    def __init__(self, rtcflag, conf):
    
        self.rtcflag = rtcflag
        self.conf = conf
        self.titles = "Showing Events", "Current Spooler Content", \
                            "Alarm History", "Missed Alarms", "Clock"
                
        gtk.Window.__init__(self)
      
        self.set_title("PyAla")
        self.set_position(gtk.WIN_POS_CENTER)
        
        www = gtk.gdk.screen_width(); hhh = gtk.gdk.screen_height();
        self.set_default_size(www/2, hhh/2)
        self.set_geometry_hints(min_width=450, min_height=100)
        self.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
         
        self.set_events(  gtk.gdk.POINTER_MOTION_MASK |
                            gtk.gdk.POINTER_MOTION_HINT_MASK |
                            gtk.gdk.BUTTON_PRESS_MASK |
                            gtk.gdk.BUTTON_RELEASE_MASK |
                            gtk.gdk.KEY_PRESS_MASK |
                            gtk.gdk.KEY_RELEASE_MASK |
                            gtk.gdk.FOCUS_CHANGE_MASK )
         
        self.connect("destroy", self.OnExit)
        self.connect("key-press-event", self.key_press_event)        
        self.connect("button-press-event", self.button_press_event)        
        
        self.focus = False
        try:
            self.set_icon_from_file("ala.png")
        except:
            try:
                self.set_icon_from_file("/usr/share/pyala/ala.png")
            except:
                print "Cannot load icon file.", sys.exc_info()

        vbox = gtk.VBox(); hbox = gtk.HBox()
        lab1 = gtk.Label("");  hbox.pack_start(lab1)
        
        butt1 = gtk.Button(" _New Alarm")
        butt1.connect("clicked", self.show_new, self)
        hbox.pack_start(butt1, False)
        
        self.connect('show', self.showme)

        if self.conf.hide:
            self.set_decorated(False)
            self.connect('destroy', self.hideme)
        else: 
            self.connect('destroy', self.destroyme)
        
        if not self.conf.hide:
            butt2 = gtk.Button(" E_xit ")
            butt2.connect("clicked", self.OnExit, self)
            hbox.pack_start(butt2, False)
            
        butt3 = gtk.Button(" Hi_de ")
        butt3.connect("clicked", self.hideme)
        hbox.pack_start(butt3, False)
        
        lab2 = gtk.Label("");  hbox.pack_start(lab2)
        vbox.pack_end(hbox, False)
        
        # Create note for the main window, give access to it for all
        self.notebook = gtk.Notebook(); 
        #self.notebook.popup_enable()
        self.notebook.set_scrollable(True)

        #notebook.add_events(gtk.gdk.FOCUS_CHANGE_MASK)
        self.notebook.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.notebook.connect("switch-page", self.note_swpage_cb)
        self.notebook.connect("focus-in-event", self.note_focus_in)
        
        hbox2 = gtk.HBox()
        lab3  = gtk.Label("");  hbox2.pack_start(lab3, False)
        hbox2.pack_start(self.notebook)
        
        self.listx = pyalalist.PySAlaList(); 
        self.notebook.append_page(self.listx)
        tablab = gtk.Label(" Events ")
        ppp = self.notebook.get_nth_page(0)
        self.notebook.set_tab_label(ppp, tablab)
        
        self.lists = pyalalist.PySAlaList(); 
        self.notebook.append_page(self.lists)
        tablab2 = gtk.Label(" Spooler ")
        ppp = self.notebook.get_nth_page(1)
        self.notebook.set_tab_label(ppp, tablab2)
        
        self.listd = pyalalist.PySAlaList(); 
        self.notebook.append_page(self.listd)
        tablab3 = gtk.Label(" History ")
        ppp = self.notebook.get_nth_page(2)
        self.notebook.set_tab_label(ppp, tablab3)
        
        self.listm = pyalalist.PySAlaList(); 
        self.notebook.append_page(self.listm)
        tablab4 = gtk.Label(" Missed ")
        ppp = self.notebook.get_nth_page(3)
        self.notebook.set_tab_label(ppp, tablab4)
        
        self.listc = pyalaclock.PySAlaClock(); 
        self.notebook.append_page(self.listc)
        tablab5 = gtk.Label(" Clock ")
        ppp = self.notebook.get_nth_page(4)
        self.notebook.set_tab_label(ppp, tablab5)
        
        vbox.pack_start(hbox2)
        
        self.add(vbox)
        self.show_all()
        if self.conf.hide:
            self.window.hide()
        
        # Iterate thru tabs, show them, set landing page
        for aa in range(self.notebook.get_n_pages()):
            self.notebook.set_current_page(aa)
        self.notebook.set_current_page(0)

    def showme(self, win, event = None):
        if self.conf.hide:
            self.window.set_functions(\
             gtk.gdk.FUNC_MOVE | gtk.gdk.FUNC_RESIZE | \
                gtk.gdk.FUNC_MINIMIZE | gtk.gdk.FUNC_MAXIMIZE)
        
            self.window.set_decorations(\
            gtk.gdk.DECOR_TITLE | gtk.gdk.DECOR_BORDER | gtk.gdk.DECOR_RESIZEH)
            
    def hideme(self, win):
        #globals.writeconf()
        self.window.hide()
        
    def destroyme(self, win):
        gtk.main_quit()

    def  note_focus_in(self, win, act):
        #print "note_focus_in"
        pass
        
    # Hack: we test if window created, and call show_all
    # The constructor calls us to create the windows, so they are ready
    # when needed
    def note_swpage_cb(self, tabx, page, num):
        #print "note_swpage", num
        if num == 0:
            if not self.listx.window:
                self.listx.show_all()
                return
        if num == 1:
            if not self.lists.window:
                self.lists.show_all()
                return
            self.fill_spooler()  
        if num == 2:
            if not self.listd.window:
                self.listd.show_all()
                return
            self.fill_history()  
        if num == 3:
            if not self.listm.window:
                self.listm.show_all()
                return
            self.fill_missed()  
                
        if num == 4:
            if not self.listc.window:
                self.listc.show_all()
                return
            #self.fill_missed()  
        
        vcurr = self.notebook.get_nth_page(num)
        ttt = "pyala: %s" % self.titles[num]
        if not self.rtcflag:
            ttt += " (No RTC access)" 
        self.set_title(ttt)
        
    def show_new(self, butt, win):
        #print butt, win
        self.app_tick()
        ret = pyaladlg.newala()
        if not ret:
            return
        self.add_alarm(ret)    
        
    def  OnExit(self, arg, srg2 = None):
        gtk.main_quit()
            
    def key_press_event(self, win, event):
        #print "key_press_event", win, event
        if  event.state & gtk.gdk.MOD1_MASK:
            if event.keyval == gtk.keysyms._1:
                self.notebook.set_current_page(0)
            if event.keyval == gtk.keysyms._2:
                self.notebook.set_current_page(1)
            if event.keyval == gtk.keysyms._3:
                self.notebook.set_current_page(2)
            if event.keyval == gtk.keysyms._4:
                self.notebook.set_current_page(3)
            if event.keyval == gtk.keysyms._5:
                self.notebook.set_current_page(4)
        
    def button_press_event(self, win, event):
        #print "butt_press_event", win, event
        pass
            
# Start of program:

if __name__ == '__main__':

    mainwin = MainWin()    
    gtk.main()




























