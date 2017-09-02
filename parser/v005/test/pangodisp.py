#!/usr/bin/env python

import sys, os, re
import pygtk, gobject, gtk
import pango
        
# XPM data for missing image

xpm_data = [
"16 16 3 1",
"       c None",
".      c #000000000000",
"X      c #FFFFFFFFFFFF",
"                ",
"   ......       ",
"   .XXX.X.      ",
"   .XXX.XX.     ",
"   .XXX.XXX.    ",
"   .XXX.....    ",
"   ..XXXXX..    ",
"   .X.XXX.X.    ",
"   .XX.X.XX.    ",
"   .XXX.XXX.    ",
"   .XX.X.XX.    ",
"   .X.XXX.X.    ",
"   ..XXXXX..    ",
"   .........    ",
"                ",
"                "
]

class PangoView(gtk.Window):
    def __init__(self, parent=None):
        # Create the toplevel window
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        #self.set_border_width(0)
    
        www = gtk.gdk.screen_width();
        hhh = gtk.gdk.screen_height();
        
        #self.set_default_size(7*www/8, 7*hhh/8)
        self.set_default_size(3*www/4, 3*hhh/4)
        self.set_position(gtk.WIN_POS_CENTER)
        #self.set_title("Pango test display");

        vpaned = gtk.VPaned()
        vpaned.set_border_width(5)
        self.add(vpaned)

        view1 = gtk.TextView();
        view1.set_border_width(8)
        self.buffer_1 = view1.get_buffer()
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        vpaned.add1(sw)
        sw.add(view1)
        self.iter = self.buffer_1.get_iter_at_offset(0)
        self.show_all()

    # We manipulete the buffer through these functions:

    def add_text(self, text):
        self.buffer_1.insert(self.iter, text)

    def add_text_tag(self, text, tags):
        self.buffer_1.insert_with_tags_by_name(self.iter, text, tags)

    def add_text_xtag(self, text, tags):        
        self.buffer_1.get_tag_table().add(tags)
        self.buffer_1.insert_with_tags(self.iter, text, tags)

def main():
    PangoView()
    gtk.main()

if __name__ == '__main__':
    main()

