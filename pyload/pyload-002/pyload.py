#!/usr/bin/env python

# Load monitor and system sleep application. Kept in one file for 
# robust portability. Tested on LINUX only.
# See README for deployment.

import os, sys, glob, getopt, time, string, signal, stat, shutil, syslog
import gobject, gtk, pango, math, traceback, subprocess, thread, pwd, shlex

import plotmenu, pydlg

# ------------------------------------------------------------------------
# Globals. Keep state in a central class. Belive it or not, async data
# did not show up correctly as a global. Fixed, when moved to a class.

class Globals():

    def __init__(self):
        self.xsleep      = 10        # Initial values
        self.rerate      = 1000
        self.idletime    = 60
        self.lowtresh    = 30
        
        self.idlecount   = 0
        self.erasecnt    = 0
        
        self.triggered   = False
        self.armed       = False
        self.program     = "gnome-terminal"
        self.old_secs    = 0
        self.old_count = 0; 
        self.idle_count = 0
        
        # State changes
        self.xxx = 0; self.yyy = 0; 

# State machine for the low pass filter
                
class Filter():

    def __init__(self):
        # Config
        self.dampen  = 10
        # States
        self.old_ppp = 0; 
        self.old_ppp2 = 0; 
        self.old_ppp3 = 0; 
            
# ------------------------------------------------------------------------
# Drop / Elevate privileges.  We preserve the current directory and set 
# the home dir to reflect the newly set user / priviledged entity.
# We ignore errors, as access control will prevail if we failed to 
# aquire resources.

def drop_priv():
    ppp = pwd.getpwnam(os.getlogin())
    old = os.getcwd()
    os.setresuid(ppp[2], ppp[3], -1)
    os.chdir(old)
    os.environ['HOME'] = ppp[5]
    #os.chdir(ppp[5])
    #print "uid", os.getuid(), "guid", os.getgid()
    #print "euid", os.geteuid(), "eguid", os.geteuid()

def elevate_priv():
    ppp = pwd.getpwnam("root")
    old = os.getcwd()
    try:
        os.setresuid(ppp[2], ppp[3], -1)
        os.chdir(old)
        os.environ['HOME'] = ppp[5]
    except: pass
    #print "uid", os.getuid(), "guid", os.getgid()
    #print "euid", os.geteuid(), "eguid", os.geteuid()
    
# ------------------------------------------------------------------------
# Resolve path name

def respath(fname):
    ppp = string.split(os.environ['PATH'], os.pathsep)
    for aa in ppp:
        ttt = aa + os.sep + fname
        #print ttt
        if os.path.isfile(ttt):
            return ttt
            
# ------------------------------------------------------------------------

class MainWin(gtk.Window):

    # Create the toplevel window
    def __init__(self, nokey = False, parent=None):
    
        global globals
        
        self.nokey = nokey
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        title = "Processor PayLoad"
        if nokey:
            self.set_title(title + " (No Keyboard Monitoring)")
        else:
            self.set_title(title)
        
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
        
        '''text1 = gtk.Label("Dampen:") 
        text1.set_tooltip_text("Dampening factor for line display")
        entry1 = gtk.SpinButton(); entry1.set_range(2, 20)
        entry1.set_value(globals.dampen);       entry1.set_increments(1, 5)
        entry1.connect("input", self.dampen_change)'''
        
        text2 = gtk.Label("Idle:") 
        text2.set_tooltip_text("Idle time before program is executed (in secs)")
        entry2 = gtk.SpinButton(); entry2.set_range(1, 200)
        entry2.set_value(globals.idletime);      entry2.set_increments(1, 10)
        entry2.connect("input", self.idle_change)
        
        text4 = gtk.Label("Low Thresh:") 
        text4.set_tooltip_text("Idle processor threshold (in %)")
        entry4 = gtk.SpinButton();  entry4.set_range(1, 100)
        entry4.set_value(globals.lowtresh); entry4.set_increments(1, 10)
        entry4.connect("input", self.tresh_change)
        
        text3 = gtk.Label("Rate:") 
        text3.set_tooltip_text("Rate of refresh. (in millisecs)")
        entry3 = gtk.SpinButton(); entry3.set_range(300, 2000)
        entry3.set_value(globals.rerate); 
        entry3.set_increments(100, 500)
        entry3.connect("input", self.rate_change)
        
        text7 = gtk.Label("Sleep:") 
        text7.set_tooltip_text("Idle keyboard time before sleep (in minutes)")
        entry7 = gtk.SpinButton(); entry7.set_range(1, 120)
        entry7.set_value(globals.xsleep); 
        entry7.set_increments(1, 10)
        entry7.connect("input", self.sleep_change)
        
        text5 = gtk.Label(" ");     text6 = gtk.Label(" ") 
         
        buttonbox = gtk.VButtonBox() 
        buttonbox.pack_start(text5); 
        buttonbox.pack_start(text4);  buttonbox.pack_start(entry4)
        buttonbox.pack_start(text3);  buttonbox.pack_start(entry3)
        buttonbox.pack_start(text2);  buttonbox.pack_start(entry2)
        #buttonbox.pack_start(text1);  buttonbox.pack_start(entry1)
        buttonbox.pack_start(text7);  buttonbox.pack_start(entry7)
        buttonbox.pack_start(text6); 
        
        buttonbox2 = gtk.HBox();   
        
        self.armbutt = gtk.Button("_Arm"); 
        self.armbutt.set_size_request(-1, 30)
        self.armbutt.connect("clicked", self.arm)
        self.armbutt.set_tooltip_text("Arm idle program timeout")
        
        button23 = gtk.Button("_Idle");
        button23.connect("clicked", self.idle)
        button23.set_tooltip_text("Program to execute on idle timeout")
        
        buttonx = gtk.Button("E_xit");
        buttonx.connect("clicked", self.exit)
        buttonx.set_tooltip_text("Exit program")
        
        buttonh = gtk.Button("Hi_de");
        buttonh.connect("clicked", self.hidebutt)
        buttonh.set_tooltip_text("Hide Program")
        
        entry14 = gtk.Label("      ")
        self.prog = gtk.Label("Started")
        globals.erasecnt = 5000
        
        buttonbox2.pack_start(entry14)
        buttonbox2.pack_start(self.armbutt)
        buttonbox2.pack_start(button23)
        buttonbox2.pack_start(buttonx)
        buttonbox2.pack_start(buttonh)
        buttonbox2.pack_start(self.prog, True)
        
        vpaned.pack1(self.area, True, False)
        vpaned.pack2(buttonbox2, False, False)
        
        hpaned.pack1(buttonbox)
        hpaned.pack2(vpaned)
        hpaned.set_position(120)
        
        self.add(hpaned)
        self.show_all()
   
    def hidebutt(self, butt):
        self.hide()
        
    def exit(self, butt):
        sys.exit(0)
    
    def idle(self, area):
        global globals
        globals.program = pydlg.getstr("Idle Program", \
                    "Enter Idle program name:", globals.program)
    
    def arm(self, area):
        global globals
        if globals.armed:
            globals.armed = False
            self.armbutt.set_label(" _Arm ")
            self.prog.set_text("Idle")
        else:
            globals.armed = True
            globals.triggered = False
            globals.idlecount = 0
            self.armbutt.set_label("_Armed")
            self.prog.set_text("Armed with %d sec" % globals.idletime)
            globals.erasecnt = 5000
            
    def area_expose_cb(self, area, event):
        #print "mainwin expose", area, event
        ww, hh = area.window.get_size()
        if hh < 100:
            #print "setting pane"
            self.vpaned.set_position = 0
    
    def tresh_change(self, area, value):
        global globals
        globals.lowtresh  = int(area.get_value())
        return False
        
    def sleep_change(self, area, value):
        global globals
        globals.xsleep  = int(area.get_value())
        return False
        
    def dampen_change(self, area, value):
        global globals
        globals.dampen  = int(area.get_value())
        return False
        
    def rate_change(self, area, value):
        global globals
        globals.rerate  = int(area.get_value())
        return False
        
    def idle_change(self, area, value):
        global globals
        globals.idletime = area.get_value()
        return False
        
    def unmap(self, area2):
        xx, yy = area2.window.get_position()
        ww, hh = area2.window.get_size()
        #print "unmap", xx, yy, ww, hh

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
        pass
        '''if  event.type == gtk.gdk.KEY_PRESS:
            if event.keyval == gtk.keysyms.x or \
                    event.keyval == gtk.keysyms.X:
                if event.state  & gtk.gdk.MOD1_MASK:
                    area.destroy()'''
    
    def area_button(self, area, event):
        if  event.type == gtk.gdk.BUTTON_PRESS:
            if event.button == 1:
                self.coords.append((event.x, event.y, 0))
                #print "Left Click at x=", event.x, "y=", event.y
                self.ldown = True 
            if event.button == 3:
                #print "Right Click at x=", event.x, "y=", event.y
                mm = self.build_menu(self.window, plotmenu.rclick_menu)
                mm.popup(None, None, None, event.button, event.time)

        elif  event.type == gtk.gdk.BUTTON_RELEASE:
            if event.button == 1:
                #print "Left Release at x=", event.x, "y=", event.y
                self.ldown = False 
                #self.coords.append((event.x, event.y, 0))

            if event.button == 3:
                #print "Right Release at x=", event.x, "y=", event.y
                pass

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
                
        # Draw text
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
                #print "Left Click at x=", event.x, "y=", event.y
                self.ldown = True 
            if event.button == 3:
                #print "Right Click at x=", event.x, "y=", event.y
                mm = self.build_menu(self.window, plotmenu.rclick_menu)
                mm.popup(None, None, None, event.button, event.time)


        elif  event.type == gtk.gdk.BUTTON_RELEASE:
            if event.button == 1:
                #print "Left Release at x=", event.x, "y=", event.y
                self.ldown = False 
                #self.coords.append((event.x, event.y, 0))

            if event.button == 3:
                #print "Right Release at x=", event.x, "y=", event.y
                pass

# ------------------------------------------------------------------------
# Put system to sleep. cat "standby" to /sys/power/state. We elected stanby,
# as it is most widely supported. You may cusomize this based upon the
# string you get from reading /sys/power/state. (like: freeze standby disk)
# freeze did not work on most older systems, disk is hybernating to 
# storage which takes longer, but reqires less power to keep around.
# If you deploy this on a laptop, on avarage standby gives a day of battery 
# life, hybernate gives three days. 
# (Note that your laptop may have different battery capacity.)

def do_sleep():

    global conf
    
    syslog.syslog("Sleeping")
    
    if conf.verbose:
        print "Flushing disks"
    # Make sure disks are flushed
    ppp = respath("sync")
    sp = subprocess.Popen([ppp,])
    os.waitpid(sp.pid, 0)
    if conf.verbose:
        print "Buffers flushed"
    
    # Set EUID to root. 
    # If it is not feasable, print message and set window title
    try:
        elevate_priv()
        #print os.getcwd()
    except:
        print "Cannot set EUID", sys.exc_info()
        mw.set_title("No Permission for Standby")
        return
    
    sstr = "/sys/power/state"; comm = "standby";  xstr = ""; 
    try:
        fd = open(sstr, "r");  xstr = fd.read(); fd.close
    except:
        pass
    if xstr.find(comm) >= 0:
        try:
            fd2 = open(sstr, "w"); fd2.write(comm)
            fd2.close()
        except:
            print "Cannot issue sleep command", sys.exc_info()
    else:
        print "Sysem does not have standby capability."
        
    if conf.verbose:
        print "Back from Sleep"
    
    # Drop privileges
    drop_priv()
    syslog.syslog("Back from Sleep")

# ------------------------------------------------------------------------
# Globals to maintain state:

def handler_tick():

    global globals, keycount, filter
    
    # Evaluate keys
    if keycount == globals.old_count:
        globals.idle_count += globals.rerate
    else:
        mw.prog.set_text("")
        globals.idle_count = 0
    globals.old_count = keycount

    # Sleep Seconds warning
    warn = (globals.xsleep * 60) - (globals.idle_count / 1000);
    if warn < 30 and warn >= 0:
        mw.show()
        mw.prog.set_text("%d sec till sleep" % warn)
        globals.erasecount = 5000
     
    # This is how we know the async var lag .. try it .. adjust sleep spin
    # and watch the xsleep count
    #print globals.idle_count, warn, globals.xsleep * 1000 * 60      
                
    # Sleep time expired:
    if globals.idle_count > globals.xsleep * 1000 * 60:
        # When it comes back, stat fresh cycle
        globals.idle_count = 0
        do_sleep()

    # Evaluate processor:
    try:
        ppp3 = ppp2 = ppp = proc_body()
        if ppp == 0:
            ppp = filter.old_ppp
        if ppp2 == 0:
            ppp2 = filter.old_ppp2
            
        # Average (first order low pass filter)
        ppp = filter.old_ppp + float(ppp - filter.old_ppp) / 2
        mw.area.add_point(ppp)
        filter.old_ppp = ppp
        
        # Average (first order low pass filter with larger damp factor)
        ppp2 = filter.old_ppp2 + float(ppp2 - filter.old_ppp2) / filter.dampen 
        mw.area.add_point2(ppp2)
        filter.old_ppp2 = ppp2
        
        # Average (second order low pass filter with even larger damp factor)
        ppp3 = filter.old_ppp3 + float(filter.old_ppp - filter.old_ppp3) / 5
        filter.old_ppp3 = ppp3; mw.area.cpuavg = ppp3
        
        #print "Timer tick", ppp, ppp2, ppp3
   
        mw.area.invalidate()
    except:
        print "Exception in timer handler", sys.exc_info()
    
    # Evaluate idle trigger
    try:
        if ppp2 < globals.lowtresh:
            globals.idlecount += globals.rerate
        else:                   
            globals.idlecount = 0
        
        if globals.armed:
            new_secs = (globals.idletime - globals.idlecount / 1000) 
            if globals.old_secs != new_secs and new_secs < 30:
                mw.show()
                mw.prog.set_text("%d sec till trigger" % int(new_secs))
                globals.old_secs = new_secs    
        
        if globals.idlecount > globals.idletime * 1000:
            if globals.armed:
                if conf.verbose:
                    print "Starting program:", "'" + globals.program + "'"
                if not globals.triggered:
                    try:
                        cmd = shlex.split(globals.program)
                        prog = respath(cmd[0])
                        ppp = [prog]
                        for aaa in cmd[1:]: ppp.append(aaa)
                        if conf.pgdebug:
                            print "Subprocess arguments:", ppp
                        sp = subprocess.Popen(ppp, shell=True)
                    except: 
                        print "Cannot execute", ppp, sys.exc_info()
                globals.triggered = True
                globals.armed = False
                mw.armbutt.set_label(" _Arm ")
                mw.prog.set_text("Triggered.")
                globals.erasecnt = 5000
            globals.idlecount = 0
    except:
        print "Exception in timer handler", sys.exc_info()
          
    # Evaluate progress text erase
    if globals.erasecnt <= 1000 and globals.erasecnt > 0:
         mw.prog.set_text("")
    if globals.erasecnt > 0:
        globals.erasecnt -= globals.rerate
                                                        
    gobject.timeout_add(globals.rerate, handler_tick)

def help():

    print "Usage: " + sys.argv[0] + " [options]"
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
        fh = open("/proc/stat");  buf = fh.read()
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

# ------------------------------------------------------------------------
# Cycle on the event buffer. Set a global var with key press count.

def run_thread(fd):

    global keycount, thdone
    #print "Started thread"
    try:
        while 1:
            buff = fd.read(48)
            keycount += 1
            if thdone:
                break
            #print count
    except:
        pass
    
# ------------------------------------------------------------------------

def main():

    global mw, keycount, thdone, globals, filter, conf
    
    syslog.openlog("PyLoad")
    syslog.syslog("Starting")
    
    globals = Globals()
    globals.xsleep = conf.timeout
    
    filter  = Filter()
    
    keycount = 1; thdone = False; nokey = False
    
    drv = "/dev/input/event3";  ddd = "/dev/input/by-path"
    # Find the driver
    dl = os.listdir(ddd)
    for aa in dl:
        if aa.find("kbd") >= 0:
            drv = ddd + "/" + aa
            break
    try:
        fd = open(drv, "r")
        tid = thread.start_new_thread(run_thread, (fd,))
    except:
        nokey = True
        print "Cannot open keyboard device, keyboard sleep timeout will not be available"
        print "You may want to start pyload with sudo or as root."
        print sys.exc_info()

    ppp = proc_body()
    mw = MainWin(nokey)
    gobject.timeout_add(globals.rerate, handler_tick)
    gtk.main()
    done = True
    syslog.syslog("Ended Normally.")
    sys.exit(0)

def pyload_applet_factory(applet, iid):
    try:
        PyLoadapplet(applet, iid)
    except:
        print  sys.exc_info()
        traceback.print_tb(sys.exc_info()[2])
    return True

# Starting here ... this is mainly for development

'''
if len(sys.argv) == 2 and sys.argv[1].find("window") != -1:

    syslog.openlog("PyLoad")
    syslog.syslog("Starting in window")
    
    main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    main_window.set_title("HSENCFC Applet")
    main_window.connect("destroy", gtk.main_quit) 
    main_window.connect("key-press-event", key_press_event) 
    app = gnomeapplet.Applet()
    HS_applet_factory(app, None)
    app.reparent(main_window)
    main_window.show_all()
    gtk.main()
    
    syslog.syslog("Ended window")
    sys.exit()

'''
# ------------------------------------------------------------------------
# Handle command line. Interpret optarray and decorate the class      

class Config:

    def __init__(self, optarr):
        self.optarr = optarr
        self.error = False

    def comline(self, argv):
        optletters = ""
        for aa in self.optarr:
            if aa[0] in optletters:
                print "Warning: duplicate option", "'" + aa[0] + "'"
            optletters += aa[0]
        #print optletters    
        
        # Create defaults:
        for bb in range(len(self.optarr)):
            if self.optarr[bb][1]:
                # Coerse type
                if type(self.optarr[bb][2]) == type(0):
                    self.__dict__[self.optarr[bb][1]] = int(self.optarr[bb][2])
                if type(self.optarr[bb][2]) == type(""):
                    self.__dict__[self.optarr[bb][1]] = str(self.optarr[bb][2])
        try:
            opts, args = getopt.getopt(argv, optletters)
        except getopt.GetoptError, err:
            print "Invalid option(s) on command line:", err
            self.error = True
            return ()
            
        #print "opts", opts, "args", args
        for aa in opts:
            for bb in range(len(self.optarr)):
                if aa[0][1] == self.optarr[bb][0][0]:
                    #print "match", aa, self.optarr[bb]
                    if len(self.optarr[bb][0]) > 1:
                        #print "arg", self.optarr[bb][1], aa[1]
                        if self.optarr[bb][2] != None: 
                            if type(self.optarr[bb][2]) == type(0):
                                self.__dict__[self.optarr[bb][1]] = int(aa[1])
                            if type(self.optarr[bb][2]) == type(""):
                                self.__dict__[self.optarr[bb][1]] = str(aa[1])
                    else:
                        #print "set", self.optarr[bb][1], self.optarr[bb][2]
                        if self.optarr[bb][2] != None: 
                            self.__dict__[self.optarr[bb][1]] = 1
                        #print "call", self.optarr[bb][3]
                        if self.optarr[bb][3] != None: 
                            self.optarr[bb][3]()
        return args

# ------------------------------------------------------------------------

def phelp():

    print
    print "Usage: " + os.path.basename(sys.argv[0]) + " [options]"
    print
    print "Options:    -d level    - Debug level 0-10"
    print "            -t minutes  - Sleep timeout"
    print "            -v          - Verbose"
    print "            -V          - Version"
    print "            -q          - Quiet"
    print "            -h          - Help"
    print
    sys.exit(0)

def pversion():
    print os.path.basename(sys.argv[0]), "Version", version
    sys.exit(0)
    
    # option, var_name, initial_val, function
optarr = \
    ["d:",  "pgdebug",  0,      None],      \
    ["t:",  "timeout",  10,     None],      \
    ["v",   "verbose",  0,      None],      \
    ["q",   "quiet",    0,      None],      \
    ["V",   None,       None,   pversion],  \
    ["h",   None,       None,   phelp]      \
    
conf = Config(optarr)

# ------------------------------------------------------------------------
# Start of program:

if __name__ == '__main__':

    # Back off from privileged operation
    drop_priv()
    args = conf.comline(sys.argv[1:])
    if conf.error:
        sys.exit(0)
    
    if conf.timeout < 1 or conf.timeout > 120:
        print "Minutes (option -t) must be between 1 - 120."
        sys.exit(0)
      
    main()

    '''
    try:
        gnomeapplet.bonobo_factory("OAFIID:GNOME_HSENCApplet_Factory",
                gnomeapplet.Applet.__gtype__,"", "0", HS_applet_factory)
    except:
        print  sys.exc_info()
        syslog.syslog("Ended with exception. %s", sys.exc_info()[1])
        sys.exit(1)
    '''



