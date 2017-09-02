#!/usr/bin/env python

import os, sys, glob, getopt, time, string, signal, stat, shutil
import gobject, gtk, pango, math, traceback, subprocess

import gzip, zlib, zipfile

from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):

    '''def handle_starttag(self, tag, attrs):
        print "Encountered the beginning of a %s tag" % tag

    def handle_endtag(self, tag):
        print "Encountered the end of a %s tag" % tag
        
    def handle_data(self, data):
        print "Encountered data '%s'" % data'''

    def handle_comment(self, data):
        print "Encountered comment '%s'" % data

    def handle_comment(self, data):
        print "Encountered comment '%s'" % data
        
    def handle_decl(self, data):
        print "Encountered decl '%s'" % data

    def handle_pi(self, data):
        print "Encountered pi '%s'" % data


class MainWin(gtk.Window):

    # Create the toplevel window
    def __init__(self, parent=None):
    
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title("Skeleton App")
        try:
            self.set_icon_from_file("monitor.png")
        except:
            try:
                self.set_icon_from_file("/usr/share/monitor.png")
            except:
                print "Cannot load app icon."
   
        self.set_geometry_hints(min_width=400, min_height=50)
        www = gtk.gdk.screen_width();
        hhh = gtk.gdk.screen_height();
        self.set_default_size(2*www/4, hhh/4)
        
        self.set_position(gtk.WIN_POS_CENTER)
        
        self.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
        hpaned = gtk.HPaned()
        hpaned.set_border_width(5)
        self.hpaned = hpaned
        
        vpaned = gtk.VPaned()
        vpaned.set_border_width(5)
        self.vpaned = vpaned
        
        self.area = MyView(PlotConfig)
        
        self.connect("button-press-event", self.area_button)
        self.connect("button-release-event", self.area_button)
        self.connect("key-press-event", self.area_key)
        self.connect('unmap', self.unmap)
        self.connect("expose-event", self.area_expose_cb)

        buttonbox = gtk.VButtonBox()
        buttonbox.set_spacing(5)
        button23 = gtk.Button("_Button0");
        button23.connect("clicked", self.idle)
        button23.set_tooltip_text("Program to execute on idle timeout")
        buttonbox.pack_start(button23)

        button24 = gtk.Button("_Button1");
        buttonbox.pack_start(button24)
   
        buttonbox2 = gtk.HBox();   
        
        self.armbutt = gtk.Button("_Arm"); 
        self.armbutt.set_size_request(-1, 30)
        self.armbutt.connect("clicked", self.arm)
        self.armbutt.set_tooltip_text("Arm idle program timeout")
        
        entry14 = gtk.Label("      ")
        self.prog = gtk.Label("Started")
        global erasecnt; erasecnt = 20
        
        buttonbox2.pack_start(entry14)
        buttonbox2.pack_start(self.armbutt)
        buttonbox2.pack_start(self.prog)
        
        vpaned.pack1(self.area, True, False)
        vpaned.pack2(buttonbox2, False, False)
        
        hpaned.pack1(buttonbox)
        hpaned.pack2(vpaned)
        hpaned.set_position(100)
        
        self.add(hpaned)
        self.show_all()
   
    def idle(self, area):
        global program
        program = pydlg.getstr("Idle Program", "Enter Idle program name:", program)
    
    def arm(self, area):
        global armed, triggered, idlecount, idletime, erasecnt;
        if armed:
            armed = False
            self.armbutt.set_label(" _Arm ")
            self.prog.set_text("Idle")
        else:
            armed = True
            triggered = False
            idlecount = 0
            self.armbutt.set_label("_Armed")
            self.prog.set_text("Armed with %d sec" % idletime)
            erasecnt = 20
            
    def area_expose_cb(self, area, event):
        #print "mainwin expose", area, event
        ww, hh = area.window.get_size()
        if hh < 100:
            print "setting pane"
            self.vpaned.set_position = 0
    
    def tresh_change(self, area, value):
        global lowtresh
        lowtresh  = int(area.get_value())
        return False
        
    def dampen_change(self, area, value):
        global dampen
        dampen  = int(area.get_value())
        return False
        
    def rate_change(self, area, value):
        global rerate
        rerate  = int(area.get_value())
        return False
        
    def idle_change(self, area, value):
        global idletime
        idletime = area.get_value()
        return False
        
    def unmap(self, area2):
        xx, yy = area2.window.get_position()
        ww, hh = area2.window.get_size()
        print "unmap", xx, yy, ww, hh

    def area_motion(self, area, event):    
        #print "motion", area, event
        if event.state & gtk.gdk.BUTTON1_MASK:            
            self.coords.append((event.x, event.y, 1))
            clen = len(self.coords)
            if  clen > 1:
                #print "lbdown motion", event.x, event.y
                #ww, hh = area.window.get_size()
                xx = self.coords[clen-2][0]
                yy = self.coords[clen-2][1]
                xx2 = self.coords[clen-1][0]
                yy2 = self.coords[clen-1][1]
                
                rect = gtk.gdk.Rectangle( min(xx,xx2) - 1,
                                            min(yy,yy2) - 1,
                                                abs(xx2-xx) + 2,   
                                                    abs(yy2 - yy) + 2)
                                         
                area.window.invalidate_rect(rect, False)
            
    # Call key handler
    def area_key(self, area, event):
        #print "key", area, event
        if  event.type == gtk.gdk.KEY_PRESS:
            if event.keyval == gtk.keysyms.x or \
                    event.keyval == gtk.keysyms.X:
                if event.state  & gtk.gdk.MOD1_MASK:
                    area.destroy()
    
    def area_button(self, area, event):
        if  event.type == gtk.gdk.BUTTON_PRESS:
            if event.button == 1:
                self.coords.append((event.x, event.y, 0))
                print "Left Click at x=", event.x, "y=", event.y
                self.ldown = True 
            if event.button == 3:
                print "Right Click at x=", event.x, "y=", event.y
                mm = self.build_menu(self.window, plotmenu.rclick_menu)
                mm.popup(None, None, None, event.button, event.time)


        elif  event.type == gtk.gdk.BUTTON_RELEASE:
            if event.button == 1:
                print "Left Release at x=", event.x, "y=", event.y
                self.ldown = False 
                #self.coords.append((event.x, event.y, 0))

            if event.button == 3:
                print "Right Release at x=", event.x, "y=", event.y

class PlotConfig():
    full_screen = False  
    
  
# Custom View

class MyView(gtk.DrawingArea):

    hovering_over_link = False
    waiting = False
    coords = []
    hand_cursor = gtk.gdk.Cursor(gtk.gdk.HAND2)
    regular_cursor = gtk.gdk.Cursor(gtk.gdk.XTERM)
    wait_cursor = gtk.gdk.Cursor(gtk.gdk.WATCH)
    callback = None
    bscallback = None

    def __init__(self, pvg, parent=None):
    
        #gtk.Window.__init__(self)
        gtk.DrawingArea.__init__(self)
        
        www = gtk.gdk.screen_width();
        hhh = gtk.gdk.screen_height();
        
        #self.set_size_request(www/4, hhh/8)
        self.set_size_request(20, 20)
        
        self.lgap = 60; self.rgap = 20
        self.pangolayout = self.create_pango_layout("a")
        fd = pango.FontDescription()
        self.colormap = gtk.widget_get_default_colormap()
        self.textcol = self.colormap.alloc_color("#808080")
        self.clear()
        self.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
        self.set_events(  gtk.gdk.POINTER_MOTION_MASK |
                            gtk.gdk.POINTER_MOTION_HINT_MASK |
                            gtk.gdk.BUTTON_PRESS_MASK |
                            gtk.gdk.BUTTON_RELEASE_MASK |
                            gtk.gdk.KEY_PRESS_MASK |
                            gtk.gdk.KEY_RELEASE_MASK |
                            gtk.gdk.FOCUS_CHANGE_MASK )
                            
        self.connect("expose-event", self.area_expose_cb)
        self.connect("motion-notify-event", self.area_motion)
        self.connect("button-press-event", self.area_button)
        self.connect("button-release-event", self.area_button)

    def invalidate(self, rect = None):
        if rect == None:
            ww, hh = self.window.get_size()
            rect = gtk.gdk.Rectangle(0,0, ww, hh)
        self.window.invalidate_rect(rect, True)
                    
    # Call key handler
    def area_key(self, area, event):
        #print "key", area, event
        if  event.type == gtk.gdk.KEY_PRESS:
            if event.keyval == gtk.keysyms.x or \
                    event.keyval == gtk.keysyms.X:
                if event.state  & gtk.gdk.MOD1_MASK:
                    area.destroy()
           
    def area_expose_cb(self, area, event):
        #print "expose", area, event, len(self.coords)
        ww, hh = area.window.get_size()
        style = self.get_style()
        self.gc = style.fg_gc[gtk.STATE_NORMAL]
        gcx = gtk.gdk.GC(self.window); gcx.copy(self.gc)
        gcr = gtk.gdk.GC(self.window); gcr.copy(self.gc)
        colormap = gtk.widget_get_default_colormap()        
        gcr.set_foreground(colormap.alloc_color("#ff0000"))

        if len(self.coords) > 1:
            olda = self.coords[0][0]; oldb = self.coords[0][1]
            for aa, bb, cc in self.coords:
                if cc != 0:
                    area.window.draw_line(gcr, olda, oldb, aa, bb)
                olda = aa; oldb = bb
        
        # Draw text
        gcr.set_foreground(colormap.alloc_color("#000080"))
        ttt = "Text in custom View"
        self.pangolayout.set_text(ttt)
        xx, yy = self.pangolayout.get_pixel_size()
        area.window.draw_layout(gcr, ww / 2 - xx / 2 + self.lgap / 2, 5, self.pangolayout)
            
    def clear(self):
        self.points = []; self.points2 = []; self.cpuavg = 0.0
                                                                   
    def area_motion(self, area, event):    
        #print "motion", area, event
        if event.state & gtk.gdk.BUTTON1_MASK:            
            self.coords.append((event.x, event.y, 1))
            clen = len(self.coords)
            if  clen > 1:
                #print "lbdown motion", event.x, event.y
                #ww, hh = area.window.get_size()
                xx = self.coords[clen-2][0]
                yy = self.coords[clen-2][1]
                xx2 = self.coords[clen-1][0]
                yy2 = self.coords[clen-1][1]
                
                rect = gtk.gdk.Rectangle( min(xx,xx2) - 1,
                                            min(yy,yy2) - 1,
                                                abs(xx2-xx) + 2,   
                                                    abs(yy2 - yy) + 2)
                                         
                area.window.invalidate_rect(rect, False)
    
    def build_menu(self, window, items):
        accel_group = gtk.AccelGroup()
        item_factory = gtk.ItemFactory(gtk.Menu, "<pydoc>", accel_group)
        item_factory.create_items(items)
        self.item_factory = item_factory
        return item_factory.get_widget("<pydoc>")

    def area_button(self, area, event):
        if  event.type == gtk.gdk.BUTTON_PRESS:
            if event.button == 1:
                self.coords.append((event.x, event.y, 0))
                print "Left Click at x=", event.x, "y=", event.y
                self.ldown = True 
            if event.button == 3:
                print "Right Click at x=", event.x, "y=", event.y
                mm = self.build_menu(self.window, plotmenu.rclick_menu)
                mm.popup(None, None, None, event.button, event.time)


        elif  event.type == gtk.gdk.BUTTON_RELEASE:
            if event.button == 1:
                print "Left Release at x=", event.x, "y=", event.y
                self.ldown = False 
                #self.coords.append((event.x, event.y, 0))

            if event.button == 3:
                print "Right Release at x=", event.x, "y=", event.y


def main():
    global mw
    mw = MainWin()
    gtk.main()

# ------------------------------------------------------------------------
# Start of program:

if __name__ == '__main__':
    
    #aa = zlib.compress("12345678901234567890123456789012345678901234567890")
    #bb = zlib.decompress(aa)
    #print  len(aa), "'" + aa + "'", len(bb), "'" + bb + "'",
    #sys.exit(0)
    
    zf = zipfile.ZipFile("test1.epub")
    #print zf.infolist()
    #print zf.namelist()
    
    for aa in zf.infolist():
        #print aa.filename, aa.file_size 
        if os.path.splitext(aa.filename)[1] == ".html":
            print   aa.filename
            fh = zf.open(aa.filename)
            ht = MyHTMLParser()
            while 1:
                sss = fh.readline()
                if sss == "": break
                #print sss,  
                ht.feed(sss)
    
    sys.exit(0)
    
    '''fh = open("test1.epub", "rb")
    ccc = fh.read(100)
    print "ccc", ccc
    ddd = zlib.decompress(ccc)
    print "ddd", ddd'''
    
    #main()



