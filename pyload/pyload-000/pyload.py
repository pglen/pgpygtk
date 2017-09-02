#!/usr/bin/env python

import os, sys, glob, getopt, time, string, signal, stat, shutil
import gobject, gtk, pango, math, traceback

import plotmenu

class PlotConfig():
    full_screen = False  
    
# ------------------------------------------------------------------------
    
class PlotView(gtk.Window):

    hovering_over_link = False
    waiting = False

    coords = []
    
    hand_cursor = gtk.gdk.Cursor(gtk.gdk.HAND2)
    regular_cursor = gtk.gdk.Cursor(gtk.gdk.XTERM)
    wait_cursor = gtk.gdk.Cursor(gtk.gdk.WATCH)
    callback = None
    bscallback = None

    # Create the toplevel window
    def __init__(self, pvg, parent=None):
    
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title("Processor PayLoad")
        self.lgap = 50
        self.rgap = 20
        
        self.set_default_size(100, 100)

        try:
            self.set_icon_from_file("monitor.png")
        except:
            try:
                self.set_icon_from_file("/usr/share/monitor.png")
            except:
                print "Cannot load app icon."
   
        self.pangolayout = self.create_pango_layout("a")
        fd = pango.FontDescription()
        colormap = gtk.widget_get_default_colormap()
        self.textcol = colormap.alloc_color("#808080")
        self.clear()
        
        www = gtk.gdk.screen_width();
        hhh = gtk.gdk.screen_height();
        if pvg.full_screen:
            self.set_default_size(www, hhh)
        else:
            self.set_default_size(2*www/4, hhh/8)
            #self.set_default_size(3*www/4, 3*hhh/4)
            #self.set_default_size(7*www/8, 7*hhh/8)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
        hpaned = gtk.HPaned()
        hpaned.set_border_width(5)
        area = gtk.DrawingArea()
        area.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
        area.set_events(  gtk.gdk.POINTER_MOTION_MASK |
                            gtk.gdk.POINTER_MOTION_HINT_MASK |
                            gtk.gdk.BUTTON_PRESS_MASK |
                            gtk.gdk.BUTTON_RELEASE_MASK |
                            gtk.gdk.KEY_PRESS_MASK |
                            gtk.gdk.KEY_RELEASE_MASK |
                            gtk.gdk.FOCUS_CHANGE_MASK )
        
        area.connect("expose-event", self.area_expose_cb)
        area.connect("motion-notify-event", self.area_motion)
        self.connect("button-press-event", self.area_button)
        self.connect("button-release-event", self.area_button)
        self.connect("key-press-event", self.area_key)
        self.connect('unmap', self.unmap)
        self.add(area)
        self.show_all()

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
           
    def unmap(self, area2):
        xx, yy = area2.window.get_position()
        ww, hh = area2.window.get_size()
        print "unmap", xx, yy, ww, hh

    def area_expose_cb(self, area, event):
        #print "expose", area, event, len(self.coords)
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
        
        # Draw axes        
        gcr.set_foreground(colormap.alloc_color("#000000"))
        ww, hh = area.window.get_size()

        area.window.draw_line(gcr, self.lgap, hh-10, ww-10, hh-10)
        area.window.draw_line(gcr, self.lgap, 20, self.lgap, hh-10)
        
        for aa in range(self.lgap, ww - 10, 10):
               area.window.draw_line(gcr, aa, hh-10, aa, hh-10 + 3)
                
        for aa in range(20, hh - 10, 10):
            area.window.draw_line(gcr, self.lgap-3, aa, self.lgap, aa)
            
        vhh = hh - 40   # Leave space on top / buttom
        # Draw points
        if len(self.points):
            gcr.set_foreground(colormap.alloc_color("#808080"))
            oldxx = 0; oldyy = self.points[0]; xx = 0
            fact =  float(vhh) / 100
            slice = len(self.points) - (ww - (self.lgap + self.rgap)) / 2 
            slice = max(slice, 0)
            for yy in self.points[slice:]:
                yy2 = vhh - yy * fact + 30
                area.window.draw_line(gcr, oldxx+self.lgap, oldyy, xx+self.lgap, yy2)
                xx += 2; oldxx = xx; oldyy = yy2
                
        if len(self.points2):
            gcr.set_foreground(colormap.alloc_color("#ff0000"))
            fact =  float(vhh) / 100
            oldxx = 0; oldyy = self.points2[0]; xx = 1
            slice = len(self.points) - (ww - (self.lgap + self.rgap)) / 2 
            slice = max(slice, 0)
            for yy in self.points2[slice:]:
                yy2 = vhh - yy * fact + 30
                area.window.draw_line(gcr, oldxx+self.lgap, oldyy, xx+self.lgap, yy2)
                xx += 2; oldxx = xx; oldyy = yy2
                
        # Do text
        gcr.set_foreground(colormap.alloc_color("#000000"))
        ttt = "Processor load average: %.2f%%" % self.cpuavg
        self.pangolayout.set_text(ttt)
        xx, yy = self.pangolayout.get_pixel_size()
        area.window.draw_layout(gcr, ww / 2 - xx / 2, 5, self.pangolayout)
        
        self.pangolayout.set_text("0%")
        xx, yy = self.pangolayout.get_pixel_size()
        area.window.draw_layout(gcr, 2, hh - (yy + 5), self.pangolayout)
        
        self.pangolayout.set_text("100%")
        area.window.draw_layout(gcr, 2, 5, self.pangolayout)
            
    def add_point(self, yy):
        self.points.append(yy)
        if len(self.points) > 3000:
            self.points =  self.points[2000:]
        
    def add_point2(self, yy):
        self.points2.append(yy)
        if len(self.points2) > 3000:
            self.points2 =  self.points2[2000:]
           
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



def put_exception(xstr):

    cumm = xstr + " "
    a,b,c = sys.exc_info()
    if a != None:
        cumm += str(a) + " " + str(b) + "\n"
        try:
            #cumm += str(traceback.format_tb(c, 10))
            ttt = traceback.extract_tb(c)
            for aa in ttt: 
                cumm += "File: " + os.path.basename(aa[0]) + \
                        " Line: " + str(aa[1]) + "\n" +  \
                    "   Context: " + aa[2] + " -> " + aa[3] + "\n"
        except:
            print "Could not print trace stack. ", sys.exc_info()
            
    print cumm
    #syslog.syslog("%s %s %s" % (xstr, a, b))


# ------------------------------------------------------------------------

xxx = 0; yyy = 0; old_ppp = 0; old_ppp2 = 0; old_ppp3 = 0

def handler_tick():

    global pv, xxx, yyy, old_ppp, old_ppp2, old_ppp3;

    try:
        ppp3 = ppp2 = ppp = proc_body()
        if ppp == 0:
            ppp = old_ppp
        if ppp2 == 0:
            ppp2 = old_ppp2
            
        # Average (first order low pass filter)
        ppp = old_ppp + float(ppp - old_ppp) / 3
        pv.add_point(ppp)
        old_ppp = ppp
        
        # Average (first order low pass filter with larger damp factor)
        ppp2 = old_ppp2 + float(ppp2 - old_ppp2) / 10
        pv.add_point2(ppp2)
        old_ppp2 = ppp2
        
        # Average (second order low pass filter with even larger damp factor)
        ppp3 = old_ppp3 + float(old_ppp - old_ppp3) / 5
        old_ppp3 = ppp3; pv.cpuavg = ppp3
        
        pv.invalidate()
        #print "Timer tick", ppp, ppp2, ppp3

    except:
        print "Exception in timer handler", sys.exc_info()
        put_exception("Timer handler")
    
    try:
        gobject.timeout_add(300, handler_tick)
    except:
        print "Exception in setting timer handler", sys.exc_info()

def help():

    print "Usage: " + sys.argv[0] + " [options] file_regex"
    print "Options:    -v        - Verbose"
    print "            -h        - Help"
    print

def main():
    global pv
    ppp = proc_body()
    pv = PlotView(PlotConfig)
    gobject.timeout_add(300, handler_tick)
    gtk.main()

def get_proc():
    try:
        fh = open("/proc/stat")
        buf = fh.read()
        fh.close()
        return buf;
    except:
        return None

# ------------------------------------------------------------------------
# Return processor load. Returns 0 - 100 (0% - 100%)

old_tot = 0; old_idle = 0

def proc_body():

    global old_tot, old_idle
    
    ppp = 0; uuu = 0; tot = 0
    try:
        buf = get_proc()
        buf3 = buf.split("\n")[0].split()
        for aa in buf3[1:5]: 
            tot += int(aa)
        idle =  int(buf3[4])
        dtot = tot - old_tot; didle = idle - old_idle
        ppp = 100 * float(dtot -  didle) / dtot
        old_tot = tot; old_idle = idle
    except:
        pass
        
    return ppp
    
# ------------------------------------------------------------------------
# Start of program:

if __name__ == '__main__':
    main()


