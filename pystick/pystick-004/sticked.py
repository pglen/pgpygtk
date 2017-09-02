#!/usr/bin/env python

import os, sys, getopt, signal
import gobject, gtk, pango

import random, time
import yellow, treehand, sutil

class StickEd():
    
    def __init__(self, par, cb, head = None, body = None):
    
        self.cb = cb
        self.window = window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Python Sticky Editor")
        window.set_position(gtk.WIN_POS_CENTER)
        
        window.set_modal(True )
        window.set_transient_for(par)
       
        #ic = gtk.Image(); ic.set_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_BUTTON)
        #window.set_icon(ic.get_pixbuf())
        
        #www = gtk.gdk.screen_width(); hhh = gtk.gdk.screen_height();
        www, hhh = sutil.get_screen_wh()
        
        window.set_default_size(www/2, hhh/2)
        
        window.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
         
        window.set_events(  gtk.gdk.POINTER_MOTION_MASK |
                            gtk.gdk.POINTER_MOTION_HINT_MASK |
                            gtk.gdk.BUTTON_PRESS_MASK |
                            gtk.gdk.BUTTON_RELEASE_MASK |
                            gtk.gdk.KEY_PRESS_MASK |
                            gtk.gdk.KEY_RELEASE_MASK |
                            gtk.gdk.FOCUS_CHANGE_MASK )
         
        # W1           
        window.connect("key-press-event", self.key_press_event)        
        window.connect("button-press-event", self.area_button)        
        
        window.set_icon_from_file("icon.png")
        
        vbox = gtk.VBox()
        
        self.vspacer(vbox)
        lab1 = gtk.Label("  Header:")
        hbox2 = gtk.HBox(); hbox2.pack_start(lab1, False )
        vbox.pack_start(hbox2, False )
        self.vspacer(vbox)
 
        hbox3 = gtk.HBox(); 
        self.spacer(hbox3)
        self.head = gtk.Entry();
        if head != None: self.head.set_text(head)
        
        hbox3.pack_start(self.head)
        self.spacer(hbox3)
        vbox.pack_start(hbox3, False )
        hbox4 = gtk.HBox(); 
        self.spacer(hbox4)
        
        self.vspacer(vbox)
        lab2 = gtk.Label("  Text:")
        hbox2b = gtk.HBox(); hbox2b.pack_start(lab2, False )
        vbox.pack_start(hbox2b, False )
        self.vspacer(vbox)
   
        self.text = gtk.TextView();
        self.text.set_border_width(8)
        if body != None: 
            self.text.grab_focus()
            buff = gtk.TextBuffer(); buff.set_text(body)
            self.text.set_buffer(buff)

        sw = gtk.ScrolledWindow()
        sw.add(self.text)
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
       
        self.spacer(hbox4)
        hbox4.pack_start(sw)
        self.spacer(hbox4)
        
        vbox.pack_start(hbox4)
        
        hbox = gtk.HBox()
        
        self.spacer(hbox)
        
        butt1 = gtk.Button(" _OK ")
        butt1.connect("clicked", self.click_ok, window)
        hbox.pack_end(butt1, False)
        
        butt2 = gtk.Button(" _Cancel ")
        butt2.connect("clicked", self.click_can, window)
        hbox.pack_end(butt2, False)
       
        vbox.pack_start(hbox, False ) 
       
        window.add(vbox)
        window.show_all()

    def spacer(self, hbox, xstr = "    "):
        lab = gtk.Label(xstr)
        hbox.pack_start(lab, False )
       
    def vspacer(self, vbox):
        lab = gtk.Label(" ")
        vbox.pack_start(lab, False )
        
    def click_ok(self, butt, xx):
        self.cb(self)
        self.window.destroy()
        pass
        
    def click_can(self, butt, xx):
        self.window.destroy()
        pass
    
    def key_press_event(self, win, event):
    
        if event.keyval == gtk.keysyms.Escape:
            self.window.destroy()
    
    def  area_button(self, butt):
        pass
    
    
    
    
    
    
    
    


