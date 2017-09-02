#!/usr/bin/env python

import os, sys, glob, getopt, time, string, signal, stat, shutil
import gobject, gtk, pango, math, traceback, subprocess

import plotmenu, pydlg

# ------------------------------------------------------------------------
# Globals

rerate      = 300
idletime    = 60
dampen      = 10
lowtresh    = 30
idlecount   = 0
erasecnt    = 0

triggered   = False
armed       = False

# ------------------------------------------------------------------------

class MainWin(gtk.Window):

    # Create the toplevel window
    def __init__(self, parent=None):
    
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title("Processor PayLoad")
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
        
        self.area = PlotView(PlotConfig)
        
        self.connect("button-press-event", self.area_button)
        self.connect("button-release-event", self.area_button)
        self.connect("key-press-event", self.area_key)
        self.connect('unmap', self.unmap)
        self.connect("expose-event", self.area_expose_cb)

        buttonbox = gtk.VButtonBox()
        
        global dampen
        text1 = gtk.Label("Dampen:") 
        text1.set_tooltip_text("Dampening factor for line display")
        entry1 = gtk.SpinButton(); entry1.set_range(2, 20)
        entry1.set_value(dampen);       entry1.set_increments(1, 5)
        entry1.connect("input", self.dampen_change)
        
        global idletime
        text2 = gtk.Label("Idle:") 
        text2.set_tooltip_text("Idle time (in secs) before program is executed")
        entry2 = gtk.SpinButton(); entry2.set_range(1, 200)
        entry2.set_value(idletime);      entry2.set_increments(1, 10)
        entry2.connect("input", self.idle_change)
        
        global lowtresh
        text4 = gtk.Label("Low Thresh:") 
        text4.set_tooltip_text("Idle threshold (in %)")
        entry4 = gtk.SpinButton();  entry4.set_range(1, 100)
        entry4.set_value(lowtresh); entry4.set_increments(1, 10)
        entry4.connect("input", self.tresh_change)
        
        text3 = gtk.Label("Rate:") 
        text3.set_tooltip_text("Rate of refresh. (in millisecs)")
        entry3 = gtk.SpinButton(); entry3.set_range(300, 2000)
        entry3.set_increments(100, 500)
        entry3.connect("input", self.rate_change)
        
        text5 = gtk.Label(" ") 
        text6 = gtk.Label(" ") 
         
        buttonbox = gtk.VButtonBox() 
        buttonbox.pack_start(text5); 
        buttonbox.pack_start(text4);  buttonbox.pack_start(entry4)
        buttonbox.pack_start(text3);  buttonbox.pack_start(entry3)
        buttonbox.pack_start(text2);  buttonbox.pack_start(entry2)
        buttonbox.pack_start(text1);  buttonbox.pack_start(entry1)
        buttonbox.pack_start(text6); 
        
        buttonbox2 = gtk.HBox();   
        
        self.armbutt = gtk.Button("_Arm"); 
        self.armbutt.set_size_request(-1, 30)
        self.armbutt.connect("clicked", self.arm)
        self.armbutt.set_tooltip_text("Arm idle program timeout")
        
        button23 = gtk.Button("_Idle Program");
        button23.connect("clicked", self.idle)
        button23.set_tooltip_text("Program to execute on idle timeout")
        
        entry14 = gtk.Label("      ")
        self.prog = gtk.Label("Started")
        global erasecnt; erasecnt = 20
        
        buttonbox2.pack_start(entry14)
        buttonbox2.pack_start(self.armbutt)
        buttonbox2.pack_start(button23)
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
        program = pydlg.getstr("Idle Program", "Enter Idle program name:")
    
    def arm(self, area):
        global armed, triggered, idlecount, idletime
        if armed:
            armed = False
            self.armbutt.set_label(" Arm ")
            self.prog.set_text("Idle")
        else:
            armed = True
            triggered = False
            idlecount = 0
            self.armbutt.set_label("Armed")
            self.prog.set_text("Armed with %d sec" % idletime)
            global erasecnt; erasecnt = 20
            
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
    
    
class PlotView(gtk.DrawingArea):

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

        area.window.draw_line(gcr, self.lgap - 10, hh-10, ww-10, hh-10)
        area.window.draw_line(gcr, self.lgap, 20, self.lgap, hh-10)
        
        for aa in range(self.lgap, ww - 10, 10):
            if aa % 20 == 0: dd = 8
            else: dd = 4
            area.window.draw_line(gcr, aa, hh-10, aa, hh-10 + dd )
                
        for aa in range(20, hh - 10, 10):
            if aa % 20 == 0: dd = 8
            else: dd = 4
            area.window.draw_line(gcr, self.lgap-dd, aa, self.lgap, aa)
            
        vhh = hh - 40   # Leave space on top / buttom
        # Draw points
        if len(self.points):
            gcr.set_foreground(colormap.alloc_color("#808080"))
            oldxx = 0; xx = 0
            fact =  float(vhh) / 100
            slice = len(self.points) - (ww - (self.lgap + self.rgap)) / 2 
            slice = max(slice, 0)
            oldyy = int(vhh - self.points[0] * fact + 30)
            for yy in self.points[slice:]:
                yy2 = int(vhh - yy * fact + 30)
                area.window.draw_line(gcr, oldxx+self.lgap + 2, oldyy, xx+self.lgap + 2, yy2)
                xx += 2; oldxx = xx; oldyy = yy2
                
        if len(self.points2):
            gcr.set_foreground(colormap.alloc_color("#ff0000"))
            oldxx = 0; xx = 1
            fact =  float(vhh) / 100
            slice = len(self.points2) - (ww - (self.lgap + self.rgap)) / 2 
            slice = max(slice, 0)
            oldyy = int(vhh - self.points2[0] * fact + 30)
            for yy in self.points2[slice:]:
                yy2 = int(vhh - yy * fact + 30)
                area.window.draw_line(gcr, oldxx+self.lgap + 4, oldyy, xx+self.lgap+4, yy2)
                xx += 2; oldxx = xx; oldyy = yy2
                
        # Do text
        
        gcr.set_foreground(colormap.alloc_color("#000000"))
        
        self.pangolayout.set_text("0%")
        area.window.draw_layout(gcr, 15, hh - 20, self.pangolayout)
        
        self.pangolayout.set_text("100%")
        area.window.draw_layout(gcr, 2, 12, self.pangolayout)
        
        gcr.set_foreground(colormap.alloc_color("#000080"))
        ttt = "Processor load average: %.2f%%" % self.cpuavg
        self.pangolayout.set_text(ttt)
        xx, yy = self.pangolayout.get_pixel_size()
        area.window.draw_layout(gcr, ww / 2 - xx / 2 + self.lgap / 2, 5, self.pangolayout)
            
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

xxx = 0; yyy = 0; old_ppp = 0; old_ppp2 = 0; old_ppp3 = 0; old_secs = 0

def handler_tick():

    global mw, xxx, yyy, old_ppp, old_ppp2, old_ppp3, dampen, armed;

    try:
        ppp3 = ppp2 = ppp = proc_body()
        if ppp == 0:
            ppp = old_ppp
        if ppp2 == 0:
            ppp2 = old_ppp2
            
        # Average (first order low pass filter)
        ppp = old_ppp + float(ppp - old_ppp) / 2
        mw.area.add_point(ppp)
        old_ppp = ppp
        
        # Average (first order low pass filter with larger damp factor)
        ppp2 = old_ppp2 + float(ppp2 - old_ppp2) / dampen 
        mw.area.add_point2(ppp2)
        old_ppp2 = ppp2
        
        # Average (second order low pass filter with even larger damp factor)
        ppp3 = old_ppp3 + float(old_ppp - old_ppp3) / 5
        old_ppp3 = ppp3; mw.area.cpuavg = ppp3
        
        #print "Timer tick", ppp, ppp2, ppp3
   
        mw.area.invalidate()
    except:
        print "Exception in timer handler", sys.exc_info()
        put_exception("Timer handler")
    
    try:
        global rerate, idlecount, triggered
        if ppp2 < lowtresh:
            idlecount += rerate
        else:                   
            idlecount = 0
        
        global old_secs
        if armed:
            new_secs = (idletime - idlecount / 1000) 
            if old_secs != new_secs and new_secs < 30:
                mw.prog.set_text("%d sec till trigger" % int(new_secs))
                old_secs = new_secs    
        
        if idlecount > idletime * 1000:
            #print "Idlecount Trigger:", idlecount
            if armed:
                if not triggered:
                    pid = subprocess.Popen(["/usr/bin/gnome-terminal", ""]).pid
                idlecount = 0
                triggered = True
                armed = False
                mw.armbutt.set_label(" Arm ")
                mw.prog.set_text("Triggered.")
                global erasecnt; erasecnt = 20

        global erasecnt
        if erasecnt == 1:
             mw.prog.set_text("")

        if erasecnt > 0:
            erasecnt -= 1
                                
        gobject.timeout_add(rerate, handler_tick)
    except:
        print "Exception in setting timer handler", sys.exc_info()

def help():

    print "Usage: " + sys.argv[0] + " [options] file_regex"
    print "Options:    -v        - Verbose"
    print "            -h        - Help"
    print

# ------------------------------------------------------------------------
# Return processor load. Returns 0 - 100 (0% - 100%)

old_tot = 0; old_idle = 0

def proc_body():
    global old_tot, old_idle
    ppp = 0; uuu = 0; tot = 0; buf = ""
    try:
        fh = open("/proc/stat")
        buf = fh.read()
        fh.close()
    except:
        print sys.exc_info()
        return 0
    buf3 = buf.split("\n")[0].split()
    for aa in buf3[1:5]: 
        tot += float(aa)
    idle =  float(buf3[4])
    #print "tot", tot, "idle", idle
    dtot = tot - old_tot; didle = idle - old_idle
    ppp = 100 * float(dtot -  didle) / dtot
    old_tot = tot; old_idle = idle

    #print "proc_body", ppp              
    return ppp
    
def main():
    global mw
    ppp = proc_body()
    mw = MainWin()
    global rerate
    gobject.timeout_add(rerate, handler_tick)
    gtk.main()

# ------------------------------------------------------------------------
# Start of program:

if __name__ == '__main__':
    main()



