#!/usr/bin/env python

import os, sys, getopt, signal
import gobject, gtk, pango
import random, time

from pgutil import  *
import pyaladlg
import pyalalist

# ------------------------------------------------------------------------

class MainWin():

    def __init__(self, rtcflag):
    
        self.rtcflag = rtcflag
        self.titles = "Showing Events", "Current Spooler Content", \
                            "Alarm History", "Missed Alarms"
                
        self.window = window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("PyAla")
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
         
        window.connect("destroy", self.OnExit)
        window.connect("key-press-event", self.key_press_event)        
        window.connect("button-press-event", self.button_press_event)        
        
        self.focus = False
        try:
            window.set_icon_from_file("ala.png")
        except:
            pass

        vbox = gtk.VBox(); hbox = gtk.HBox()
        lab1 = gtk.Label("");  hbox.pack_start(lab1)
        
        butt1 = gtk.Button(" _New Alarm")
        butt1.connect("clicked", self.show_new, window)
        hbox.pack_start(butt1, False)
        
        butt2 = gtk.Button(" E_xit ")
        butt2.connect("clicked", self.OnExit, window)
        hbox.pack_start(butt2, False)
        
        butt3 = gtk.Button(" Hide ")
        butt3.connect("clicked", self.some, window)
        hbox.pack_start(butt3, False)
        
        lab2 = gtk.Label("");  hbox.pack_start(lab2)
        vbox.pack_end(hbox, False)
        
        # Create note for the main window, give access to it for all
        self.notebook = gtk.Notebook(); 
        self.notebook.popup_enable()
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
        tablab = gtk.Label(" Alarm Events ")
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
        lab4  = gtk.Label("");  hbox2.pack_start(lab4, False)
        
        self.listm = pyalalist.PySAlaList(); 
        self.notebook.append_page(self.listm)
        tablab2 = gtk.Label(" Missed ")
        ppp = self.notebook.get_nth_page(3)
        self.notebook.set_tab_label(ppp, tablab2)
        
        vbox.pack_start(hbox2)
        
        window.add(vbox)
        window.show_all()
        
        # Iterate thru tabs, show them, set landing page
        for aa in range(4):
            self.notebook.set_current_page(aa)
        self.notebook.set_current_page(0)

    def some(self, win, act):
        #self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_TOOLBAR)
        self.window.iconify()
    
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
                
        vcurr = self.notebook.get_nth_page(num)
        ttt = "pyala: %s" % self.titles[num]
        if not self.rtcflag:
            ttt += " (No RTC access)" 
        self.window.set_title(ttt)
        
    def show_new(self, butt, win):
        #print butt, win
        self.app_tick()
        ret = pyaladlg.newala()
        if not ret:
            return
        self.add_alarm(ret)    
        
    def  OnExit(self, arg, srg2 = None):
        self.exit_all()
            
    def exit_all(self):
        gtk.main_quit()
            
    def key_press_event(self, win, event):
        #print "key_press_event", win, event
        pass
        
    def button_press_event(self, win, event):
        #print "butt_press_event", win, event
        pass
            
# Start of program:

if __name__ == '__main__':

    mainwin = MainWin()    
    gtk.main()





















