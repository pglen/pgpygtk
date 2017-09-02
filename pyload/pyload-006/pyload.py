#!/usr/bin/env python
                                        
# Load monitor and system sleep application. Kept in one file for robust 
# transportability. Tested on LINUX only. See README for deployment.
# 

import os, sys, glob, getopt, time, string, signal, stat, shutil, syslog
import gobject, gtk, pango, math, traceback, subprocess, thread
import pwd, shlex, gnomeapplet, warnings, gnome.ui, sqlite3

# ------------------------------------------------------------------------
# Callback for right click menu

def rclick_action(self, arg, mained):

    #print "rclick_action", "'" + arg.name + "'" 
    
    if arg.name == "<pydoc>/New":
        mained.newfile()        
        
    if arg.name == "<pydoc>/Open":
        mained.open()

    if arg.name == "<pydoc>/Save":
        mained.save()
        
    if arg.name == "<pydoc>/SaveAs":
        mained.save(True )
    
    if arg.name == "<pydoc>/Copy":
        mained.copy( )
    
    if arg.name == "<pydoc>/Cut":
        mained.cut()
    
    if arg.name == "<pydoc>/Paste":
        mained.paste()
    
def rclick_quit(self, arg):
    print __name__, arg.name
    mained.activate_exit()
    
rclick_menu = (
            ( "/Copy",          "<control>C",   rclick_action, 0, None ),
            ( "/Cut",           "<control>X",   rclick_action, 0, None ),
            ( "/Paste",         "<control>V",   rclick_action, 0, None ),
            )
    
#!/usr/bin/env python

import sys, os, time, sqlite3

# ------------------------------------------------------------------------
# Store some data
class pysql():

    def __init__(self, file):
        try:
            self.conn = sqlite3.connect(file)
        except:
            print "Cannot open/create db:", file, sys.exc_info() 
            return            
        try:
            self.c = self.conn.cursor()
            # Create table
            self.c.execute("create table if not exists config \
             (pri INTEGER PRIMARY KEY, key text, val text)")
            self.c.execute("create index if not exists iconfig on config (key)")            
            self.c.execute("create index if not exists pconfig on config (pri)")            
            self.c.execute("PRAGMA synchronous=OFF")
            # Save (commit) the changes
            self.conn.commit()            
        except:
            print "Cannot create sql tables", sys.exc_info() 
        finally:    
            pass
                            
    # --------------------------------------------------------------------        
    # Return None if no data
    
    def   get(self, kkk):
        try:      
            #c = self.conn.cursor()            
            if os.name == "nt":
                self.c.execute("select * from config where key = ?", (kkk,))
            else: 
                self.c.execute("select * from config indexed by iconfig where key = ?", (kkk,))
            rr = self.c.fetchone()
        except:
            print "Cannot get sql data", sys.exc_info() 
            rr = None
        finally:
            pass
        if rr:            
            return rr[2]
        else:
            return None

    # --------------------------------------------------------------------        
    # Return False if cannot put data
    
    def   put(self, key, val):
        ret = True  
        try:      
            if os.name == "nt":
                self.c.execute("select * from config where key == ?", (key,))
            else: 
                self.c.execute("select * from config indexed by iconfig where key == ?", (key,))            
            rr = self.c.fetchall()
            if rr == []:
                self.c.execute("insert into config (key, val) \
                    values (?, ?)", (key, val))
            else:
                if os.name == "nt":
                    self.c.execute("update config set val = ? where key = ?",\
                                     (val, key))                                     
                else: 
                    self.c.execute("update config indexed by iconfig set val = ? where key = ?",\
                                     (val, key))                                     
            self.conn.commit()          
        except:
            print "Cannot put sql data", sys.exc_info()             
            ret = False  
        finally:
            pass
        return ret

# -----------------------------------------------------------------------
# Sleep just a little, but allow the system to breed

def  usleep(msec):

    got_clock = time.clock() + float(msec) / 1000
    #print got_clock
    while True:
        if time.clock() > got_clock:
            break
        gtk.main_iteration_do(False)

# ------------------------------------------------------------------------
# Pop up dialog

def popup_getstr(title, message, oldstr = ""):

    dialog = gtk.Dialog(title,
                   None,
                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)

    sp = "   "
    try:
        dialog.set_icon_from_file("monitor.png")
    except:
        try:
            dialog.set_icon_from_file( \
                "/usr/share/pyload/monitor.png")
        except:                                              
            pass
    
    label = gtk.Label(message); 
    label2 = gtk.Label(sp);     label3 = gtk.Label(sp)
    hbox = gtk.HBox() ;         hbox.pack_start(label2);  
    hbox.pack_start(label);     hbox.pack_start(label3)
    
    entry = gtk.Entry();    
    #entry.set_invisible_char("*")
    #entry.set_visibility(False)
    
    entry.set_width_chars(32)
    entry.set_text(oldstr)
    
    label21 = gtk.Label(sp);     label31 = gtk.Label(sp)
    hbox.pack_start(label21);     
    hbox.pack_start(entry)
    hbox.pack_start(label31)
    
    label22 = gtk.Label(sp);     label32 = gtk.Label(sp)
    
    dialog.vbox.pack_start(label22)
    dialog.vbox.pack_start(hbox)
    dialog.vbox.pack_start(label32)

    #dialog.set_default_response(gtk.RESPONSE_YES)
    entry.set_activates_default(True)
    
    dialog.add_button("_OK", gtk.RESPONSE_YES)
    dialog.add_button("_Cancel", gtk.RESPONSE_NO)
    
    dialog.connect("key-press-event", area_key)
    dialog.show_all()
    response = dialog.run() 
    text = entry.get_text()
                
    # Convert all responses to cancel
    if  response == gtk.RESPONSE_CANCEL or \
        response == gtk.RESPONSE_REJECT or \
        response == gtk.RESPONSE_CLOSE  or \
        response == gtk.RESPONSE_DELETE_EVENT:
        response = gtk.RESPONSE_CANCEL        
    dialog.destroy()
    
    if response != gtk.RESPONSE_CANCEL:
        return  text
    else: 
        return ""

def area_key(win, event):

    if event.keyval == gtk.keysyms.Return:
        win.response(gtk.RESPONSE_OK)

# ------------------------------------------------------------------------
# Globals. Keep state in a central class. Believe it or not, async data
# did not show up correctly as a global. Fixed, when moved to a class.

class _Globals():

    global conf

    def __init__(self):
    
        self.xsleep      = 10        # Initial values
        self.rerate      = 1000
        self.idletime    = 60
        self.lowtresh    = 30
        self.dampen      = 20
        
        self.idlecount   = 0
        self.erasecnt    = 0
        self.triggered   = False
        self.armed       = False
        self.program     = "gnome-terminal"
        self.old_secs    = 0
        self.old_count   = 0; 
        self.idle_count  = 0
        
        # State changes
        self.xxx = 0; self.yyy = 0; 

        # Prepare configuration and SQL
        conf.conf_dir = os.path.expanduser("~/.pyload")
        if not os.path.isdir(conf.conf_dir):
            os.mkdir(conf.conf_dir)
        conf.sql = pysql(conf.conf_dir + "/" + "config")
        self.readconf()
            
    def readconf(self):
    
        global conf
        val = conf.sql.get("xsleep")
        if val: self.xsleep = int(float(val))
        val = conf.sql.get("rerate")
        if val: self.rerate = int(float(val))
        val = conf.sql.get("idletime")
        if val: self.idletime = int(float(val))
        val = conf.sql.get("lowtresh")
        if val: self.lowtresh = int(float(val))
        
        val = conf.sql.get("program")
        if val: self.program = val
        
        #print self.xsleep, self.rerate, self.idletime, self.lowtresh
      
    def writeconf(self):
        global conf
        conf.sql.put("xsleep", self.xsleep)
        conf.sql.put("rerate", self.rerate)
        conf.sql.put("idletime", self.idletime)
        conf.sql.put("lowtresh", self.lowtresh)
        conf.sql.put("program", self.program)

# ------------------------------------------------------------------------
# State machine for the low pass filter
                
class Filter():

    def __init__(self):
        self.old_ppp = 0; self.old_ppp2 = 0; self.old_ppp3 = 0; 
      
    # Average (first order low pass filter)
    def first(self, val, dampen = 2):
        ppp = self.old_ppp + float(val - self.old_ppp) / dampen
        self.old_ppp = ppp
        return ppp
        
    # Average (first order low pass filter with larger damp factor)
    def first2(self, val, dampen = 10):
        ppp2 = self.old_ppp2 + float(val - self.old_ppp2) / dampen 
        self.old_ppp2 = ppp2
        return ppp2
        
    # Average (second order low pass filter with even larger damp factor)
    def second(self, val, dampen = 10):       
        ppp3 = self.old_ppp3 + float(self.old_ppp - self.old_ppp3) / dampen
        self.old_ppp3 = ppp3; 
        return ppp3
                  
# ------------------------------------------------------------------------
# Drop / Elevate privileges.  We preserve the current directory and set 
# the home dir to reflect the newly set user / privileged entity.
# We ignore errors, as access control will prevail if we failed to 
# acquire resources.

def drop_priv():
    ppp = pwd.getpwnam(os.getlogin())
    old = os.getcwd()
    os.setresuid(ppp[2], ppp[3], -1)
    os.chdir(old)
    os.environ['HOME'] = ppp[5]
    
    #if conf.pgdebug > 5:
    #    print "uid", os.getuid(), "guid", os.getgid()
    #    print "euid", os.geteuid(), "eguid", os.geteuid()

def elevate_priv():
    ppp = pwd.getpwnam("root")
    old = os.getcwd()
    try:
        os.setresuid(ppp[2], ppp[3], -1)
        os.chdir(old)
        os.environ['HOME'] = ppp[5]
    except: pass
    if conf.pgdebug > 5:
        print "uid", os.getuid(), "guid", os.getgid()
        print "euid", os.geteuid(), "eguid", os.geteuid()
    
# ------------------------------------------------------------------------
# Resolve path name

def respath(fname):

    try:
        ppp = string.split(os.environ['PATH'], os.pathsep)
        for aa in ppp:
            ttt = aa + os.sep + fname
            if conf.pgdebug > 8:
                print "respath", ttt
            if os.path.isfile(str(ttt)):
                return ttt
    except:
        print "Cannot resolve path", aa, fname, sys.exc_info()   
    return None   
    
# ------------------------------------------------------------------------
# LED imitation device.

class LED(gtk.DrawingArea):

    def __init__(self, parent=None):
        gtk.DrawingArea.__init__(self)
        self.set_size_request(25, 25)
        self.connect("expose-event", self.area_expose_cb)
        self.on = False
        self.set_tooltip_text("LED")

    def area_expose_cb(self, area, event):
        style = self.get_style()
        self.gc = style.fg_gc[gtk.STATE_NORMAL]
        colormap = gtk.widget_get_default_colormap()        
        gcx = gtk.gdk.GC(self.window); gcx.copy(self.gc)
        gcr = gtk.gdk.GC(self.window); gcr.copy(self.gc)
        
        if self.on: 
            gcr.set_foreground(colormap.alloc_color("#ff4444"))
        else:
            gcr.set_foreground(colormap.alloc_color("#888888"))
        area.window.draw_arc(gcr, True, 0, 5, 20, 20, 0, 360 * 64)
        
        if self.on: 
            gcx.set_foreground(colormap.alloc_color("#ffcccc"))
        else:
            gcx.set_foreground(colormap.alloc_color("#aaaaaa"))
        
        area.window.draw_arc(gcx, True, 5, 10, 10, 10, 0, 360 * 64)

    def led(self, on = True):
        self.on = on
        ww, hh = self.window.get_size()
        rect = gtk.gdk.Rectangle(0, 0, ww, hh)
        self.window.invalidate_rect(rect, True)
        
    def flash(self):
        self.led()
        gobject.timeout_add(200, self.led, False)

# ------------------------------------------------------------------------
# An N pixel vertical spacer. Default to 5.

class Spacer(gtk.Label):

    def __init__(self, sp = 5):
        gtk.Label.__init__(self)
        sp *= 1000
        self.set_markup("<span  size=\"" + str(sp) + "\"> </span>")
        
# ------------------------------------------------------------------------

class MainWin(gtk.Window):

    # Create the toplevel window
    def __init__(self, nokey = False, parent=None):
    
        global globals, conf
        self.nokey = nokey
        
        gtk.Window.__init__(self)
      
        # Will be reset on show event
        
        if conf.tray:
            self.set_decorated(False)
            
        if conf.tray:
            self.connect('destroy', self.hideme)
        else: 
            self.connect('destroy', self.destroyme)

        self.connect('show', self.showme)
        self.connect('show', self.showme)
        
        self.titlex = "System PayLoad"
        if nokey:
            self.set_title(self.titlex + " (No Keyboard Monitoring)")
        else:
            self.set_title(self.titlex)
        
        try:
            self.set_icon_from_file("monitor.png")
        except:
            try:
                self.set_icon_from_file("/usr/share/pyload/monitor.png")
            except:
                print "Cannot load app icon."
   
        self.set_geometry_hints(min_width=650, min_height=140)
        www = gtk.gdk.screen_width();
        hhh = gtk.gdk.screen_height();
        self.set_default_size(5 * www/8, hhh/3)
        
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

        text1 = gtk.Label("Dampen:") 
        text1.set_tooltip_text("Dampening factor for line display")
        entry1 = gtk.SpinButton(); entry1.set_range(2, 20)
        entry1.set_value(globals.dampen);       entry1.set_increments(1, 5)
        entry1.connect("input", self.dampen_change)
        
        text2 = gtk.Label("Idle:") 
        text2.set_tooltip_text("Idle time before program is executed (in secs)")
        entry2 = gtk.SpinButton(); entry2.set_range(1, 200)
        entry2.set_value(globals.idletime);      entry2.set_increments(1, 10)
        entry2.connect("input", self.idle_change)
        
        text4 = gtk.Label("Low Thresh:") 
        text4.set_tooltip_text("Idle system activity threshold (in %)")
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
        text7.set_tooltip_text("Idle system time before sleep (in minutes)")
        entry7 = gtk.SpinButton(); entry7.set_range(1, 120)
        entry7.set_value(globals.xsleep); 
        entry7.set_increments(1, 10)
        entry7.connect("input", self.sleep_change)
        
        text5  = Spacer();          text50  = Spacer()
        text51 = Spacer();          text52 = Spacer();
        text53 = Spacer();          text54 = Spacer();
        text6  = Spacer();
         
        butbox = gtk.VBox() 
        butbox.pack_start(text5, False); 
        
        butbox.pack_start(text7, False);  butbox.pack_start(entry7, False)
        butbox.pack_start(text54, False);
        
        butbox.pack_start(text4, False);  butbox.pack_start(entry4, False)
        butbox.pack_start(text51, False); 
        
        butbox.pack_start(text1, False);  butbox.pack_start(entry1, False)
        butbox.pack_start(text50, False); 
       
        butbox.pack_start(text3, False);  butbox.pack_start(entry3, False)
        butbox.pack_start(text52, False);
         
        butbox.pack_start(text2, False);  butbox.pack_start(entry2, False)
        butbox.pack_start(text53, False);
        hbutbox = gtk.HBox()
        label99 = gtk.Label("    ")
        hbutbox.pack_start(label99, False)
        hbutbox.pack_start(butbox)
        
        buttonbox2 = gtk.HBox(); buttonbox2.set_spacing(2)  
        
        self.armbutt = gtk.Button(" _Arm Idle "); 
        self.armbutt.set_size_request(-1, 30)
        self.armbutt.connect("clicked", self.arm)
        self.armbutt.set_tooltip_text("Arm idle program timeout")
        
        button23 = gtk.Button(" _Idle Prog ");
        button23.connect("clicked", self.idle)
        button23.set_tooltip_text("Program to execute on idle timeout")
        
        buttonh = gtk.Button(" Hi_de ");
        buttonh.connect("clicked", self.hidebutt)
        buttonh.set_tooltip_text("Hide Window")
        
        buttonx = gtk.Button(" E_xit ");
        buttonx.connect("clicked", self.exitbutt)
        buttonx.set_tooltip_text("Exit program")
        
        self.prog = gtk.Label("Started")
        globals.erasecnt = 5000
        
        self.led = LED();  self.led.set_tooltip_text("Keyboard")
        self.led2 = LED(); self.led2.set_tooltip_text("Mouse")
        self.led3 = LED(); self.led3.set_tooltip_text("Network")
        self.led4 = LED(); self.led4.set_tooltip_text("Disk")

        entry14 = gtk.Label("           ")
        entry15 = gtk.Label(" ")
        buttonbox2.pack_start(entry14, False, False)
        buttonbox2.pack_start(self.led, False, False)
        buttonbox2.pack_start(self.led2, False, False)
        buttonbox2.pack_start(self.led3, False, False)
        buttonbox2.pack_start(self.led4, False, False)
        buttonbox2.pack_start(entry15, False, False)
        buttonbox2.pack_start(self.armbutt, False, False)
        buttonbox2.pack_start(button23, False, False)
        buttonbox2.pack_start(buttonh, False, False)
        if not conf.tray:               # No exit for tray
            buttonbox2.pack_start(buttonx, False, False)
        buttonbox2.pack_start(self.prog)
        
        vpaned.pack1(self.area, True, False)
        vpaned.pack2(buttonbox2, False, True)
        
        hpaned.pack1(hbutbox)
        hpaned.pack2(vpaned)
        hpaned.set_position(120)
        
        self.add(hpaned)
        self.show_all()

    def showme(self, win, event = None):
        if conf.tray:
            self.window.set_functions(\
             gtk.gdk.FUNC_MOVE | gtk.gdk.FUNC_RESIZE | \
                gtk.gdk.FUNC_MINIMIZE | gtk.gdk.FUNC_MAXIMIZE)
        
            self.window.set_decorations(\
            gtk.gdk.DECOR_TITLE | gtk.gdk.DECOR_BORDER | gtk.gdk.DECOR_RESIZEH)
            
    def hideme(self, win):
        globals.writeconf()
        self.hide()
        
    def destroyme(self, win):
        gtk.main_quit()
    
    def hidebutt(self, butt):
        globals.writeconf()
        self.hide()
        
    def exitbutt(self, butt):
        self.destroy()
    
    def idle(self, area):
        global globals
        globals.program = popup_getstr("Idle Program", \
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
        global globals
        xx, yy = area2.window.get_position()
        ww, hh = area2.window.get_size()
        #print "unmap", xx, yy, ww, hh
        globals.writeconf()

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
        global conf
        if conf.tray:
            if  event.type == gtk.gdk.KEY_PRESS:
                if event.keyval == gtk.keysyms.Escape:
                    area.hide()
    
    def area_button(self, area, event):
        if  event.type == gtk.gdk.BUTTON_PRESS:
            if event.button == 1:
                #self.coords.append((event.x, event.y, 0))
                #print "Left Click at x=", event.x, "y=", event.y
                self.ldown = True 
            if event.button == 3:
                #print "Right Click at x=", event.x, "y=", event.y
                #mm = self.build_menu(self.window, rclick_menu)
                #mm.popup(None, None, None, event.button, event.time)
                pass

        elif  event.type == gtk.gdk.BUTTON_RELEASE:
            if event.button == 1:
                #print "Left Release at x=", event.x, "y=", event.y
                #self.ldown = False 
                #self.coords.append((event.x, event.y, 0))
                pass

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
        
        self.set_tooltip_text(      "Gray: \tProcessor\n"
                                    "Green:\tProcessor (Low Pass)\n"\
                                    "Blue: \tNetwork Transfers\n"\
                                    "Yellow:\tDisk Activity")
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
        print "key", area, event
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

        '''if len(self.coords) > 1:
            olda = self.coords[0][0]; oldb = self.coords[0][1]
            for aa, bb, cc in self.coords:
                if cc != 0:
                    area.window.draw_line(gcr, olda, oldb, aa, bb)
                olda = aa; oldb = bb'''
        
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
            gcr.set_foreground(colormap.alloc_color("#00ff00"))
            oldxx = 0; xx = 1
            fact =  float(vhh) / 100
            slice = len(self.points2) - (ww - (self.lgap + self.rgap)) / 2 
            slice = max(slice, 0)
            oldyy = int(vhh - self.points2[0] * fact + 30)
            for yy in self.points2[slice:]:
                yy2 = int(vhh - yy * fact + 30)
                area.window.draw_line(gcr, oldxx+self.lgap + 4, oldyy, xx+self.lgap+4, yy2)
                xx += 2; oldxx = xx; oldyy = yy2
                
        if len(self.points3):
            gcr.set_foreground(colormap.alloc_color("#0000ff"))
            oldxx = 0; xx = 1
            fact =  float(vhh) / 100
            slice = len(self.points3) - (ww - (self.lgap + self.rgap)) / 2 
            slice = max(slice, 0)
            oldyy = int(vhh - self.points3[0] * fact + 30)
            for yy in self.points3[slice:]:
                yy2 = int(vhh - yy * fact + 30)
                area.window.draw_line(gcr, oldxx+self.lgap + 4, oldyy, xx+self.lgap+4, yy2)
                xx += 2; oldxx = xx; oldyy = yy2
                
        if len(self.points4):
            gcr.set_foreground(colormap.alloc_color("#ffff00"))
            oldxx = 0; xx = 1
            fact =  float(vhh) / 100
            slice = len(self.points4) - (ww - (self.lgap + self.rgap)) / 2 
            slice = max(slice, 0)
            oldyy = int(vhh - self.points4[0] * fact + 30)
            for yy in self.points4[slice:]:
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
           
    def add_point3(self, yy):
        self.points3.append(yy)
        if len(self.points3) > 3000:
            self.points3 =  self.points3[2000:]
            
    def add_point4(self, yy):
        self.points4.append(yy)
        if len(self.points4) > 3000:
            self.points4 =  self.points4[2000:]
            
    def clear(self):
        self.points = [];  self.points2 = []; 
        self.points3 = []; self.points4 = []; 
        self.cpuavg = 0.0
                                                                   
    def area_motion(self, area, event):    
        #print "motion", area, event
        if event.state & gtk.gdk.BUTTON1_MASK:       
            '''self.coords.append((event.x, event.y, 1))
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
                                         
                area.window.invalidate_rect(rect, False)'''
            pass
    
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
                #mm = self.build_menu(self.window, rclick_menu)
                #mm.popup(None, None, None, event.button, event.time)
                pass

        elif  event.type == gtk.gdk.BUTTON_RELEASE:
            if event.button == 1:
                #print "Left Release at x=", event.x, "y=", event.y
                self.ldown = False 
                #self.coords.append((event.x, event.y, 0))

            if event.button == 3:
                #print "Right Release at x=", event.x, "y=", event.y
                pass

# ------------------------------------------------------------------------
# Put system to sleep. cat "standby" to /sys/power/state. We elected standby,
# as it is most widely supported. You may customize this based upon the
# string you get from reading /sys/power/state. (like: freeze standby disk)
# freeze did not work on most older systems, disk is hibernating to 
# storage which takes longer, but requires less power to keep around.
# If you deploy this on a laptop, on average standby gives a day of battery 
# life, hibernate gives three days. 
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
    except:
        print "Cannot set EUID", sys.exc_info()
        mw.set_title("No Permission for Standby")
        return
    
    xstr = ""; 
    # Configure these strings for your system's sleep
    sstr = "/sys/power/state"; comm = "standby";  
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

    global globals, event_count, filter
    
    # Evaluate events from listeners
    if event_count == globals.old_count:
        globals.idle_count += globals.rerate
    else:
        mw.prog.set_text("")
        globals.idle_count = 0
    globals.old_count = event_count

    # Sleep Seconds warning
    warn = (globals.xsleep * 60) - (globals.idle_count / 1000);
    if warn < 30 and warn >= 0:
    # Show it in impending phase
        if warn < 29 and warn > 25:
            mw.show()
        mw.prog.set_text("%d sec till sleep" % warn)
        globals.erasecount = 5000         
     
    # This is how we know the async var lag .. try it .. adjust sleep spin
    # and watch the xsleep count
    #print globals.idle_count, warn, globals.xsleep * 1000 * 60      
                
    # Sleep time expired:
    if globals.idle_count > globals.xsleep * 1000 * 60:
        # When it comes back, start with a fresh cycle
        globals.idle_count = 0
        do_sleep()
    
    # Evaluate IO traffic:
    try:             
        elevate_priv()
        ddd = get_disk_usage()
        drop_priv()
        #print "disk usage", ddd
    except:
        pass
    ddd2 = conf.filter_disk.first(ddd)
    if ddd2 > globals.lowtresh:
        mw.led4.flash()
        event_count += 1
    mw.area.add_point4(ddd2)
                                                      
    # Evaluate network traffic:
    try:
        nnn = get_net_usage()
        if nnn > globals.lowtresh:
            mw.led3.flash()
        
        nnn2 = conf.filter_net.first(nnn)
        if nnn2 > globals.lowtresh:
            event_count += 1
        mw.area.add_point3(nnn2)
    except:
        pass
    
    # Evaluate processor load:
    try:
        ppp = get_proc_usage()
        ppp2 = conf.filter_cpu.first(ppp)
        if ppp2 > globals.lowtresh:
            event_count += 1
        mw.area.add_point(ppp2)
        
        ppp3 = conf.filter_cpu.first2(ppp2)
        mw.area.add_point2(ppp3)
        
        ppp4 = conf.filter_cpu.second(ppp3)
        mw.area.cpuavg = ppp3
        
        #print "Timer tick", ppp, ppp2, ppp3
   
        mw.area.invalidate()
    except:
        print "Exception in timer handler top", sys.exc_info()
    
    # Evaluate idle trigger                    
    try:
        if ppp2 < globals.lowtresh:
            globals.idlecount += globals.rerate
        else:                   
            globals.idlecount = 0
        
        if globals.armed:
            new_secs = (globals.idletime - globals.idlecount / 1000) 
            if globals.old_secs != new_secs and new_secs < 30:
                if int(new_secs) == 29:
                    mw.show()
                mw.prog.set_text("%d sec till trigger" % int(new_secs))
                globals.old_secs = new_secs    
        
        if globals.idlecount > globals.idletime * 1000:
            if globals.armed:
                if conf.verbose:
                    print "Starting program:", "'" + globals.program + "'"
                    syslog.syslog("Starting '%s'" % globals.program)
                if not globals.triggered:
                    pppx = []
                    try:
                        cmd = shlex.split(str(globals.program))
                        prog = respath(cmd[0])
                        pppx = [prog]
                        for aaa in cmd[1:]: pppx.append(aaa)
                        if conf.pgdebug > 1:
                            print "Subprocess arguments:", pppx
                        sp = subprocess.Popen(pppx, shell=True)
                    except: 
                        print "Cannot execute", pppx, sys.exc_info()
                globals.triggered = True
                globals.armed = False
                mw.armbutt.set_label(" _Arm ")
                mw.prog.set_text("Triggered.")
                globals.erasecnt = 5000
            globals.idlecount = 0
    except:
        print "Exception in timer handler buttom part", sys.exc_info()
        traceback.print_tb(sys.exc_info()[2])
          
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

old_tot = 0.; old_idle = 0.

def get_proc_usage():

    global old_tot, old_idle
    ppp = 0.; tot = 0.0; buf = ""
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
    if conf.pgdebug > 9:
        print "tot", tot, "idle", idle
    dtot = tot - old_tot; didle = idle - old_idle
    ppp = 100 * float(dtot -  didle) / dtot
    old_tot = tot; old_idle = idle
    if conf.pgdebug > 4:
        print "get_proc_usage", ppp              
    return ppp

# ------------------------------------------------------------------------
# Read every process's IO stat, add them and report

old_dtot = 0.; old_wtot = 0.; old_dmax = 0.; old_wmax = 0.
   
def get_disk_usage():

    global old_dtot, old_wtot, old_dmax, old_wmax
    
    totr = 0.; totw = 0.; 
    buf = ""; ret = 0; ret2 = 0
    
    ddd = "/proc"
    
    dl = os.listdir(ddd)
    for aa in dl:
        ff = ddd + os.sep + aa + os.sep + "io"
        if os.path.isfile(ff):
            try:
                fh = open(ff);  ss = fh.readlines(); fh.close()
                for bb in ss:
                    ss = bb.split(":")
                    if len(ss) == 2:
                        if ss[0].strip() == "read_bytes":
                        #if ss[0].strip() == "rchar":
                            totr += float(ss[1].strip())
                        if ss[0].strip() == "write_bytes":
                        #if ss[0].strip() == "wchar":
                            totw += float(ss[1].strip())
            except:
                # Ignoring inaccessable (system) activity
                #print "Cannot read ", ff, sys.exc_info()
                pass
                
    #print "totr", totr, "totw", totw 
    
    # First run
    if old_dtot == 0.:
        old_dtot = totr
    if old_wtot == 0.:
        old_wntot = totw
    
    # Calc read diff:
    ddiff = totr - old_dtot
    if old_dmax < ddiff:               # Adapt
        old_dmax = ddiff
    old_dtot = totr; 
    try:
        ret = int(100 * ddiff / old_dmax)
    except: pass
    
    # Calc write diff:
    wdiff = totr - old_wtot
    if old_wmax < wdiff:                # Adapt
        old_wmax = wdiff
    old_wtot = totw; 
    try:
        retw = int(100 * wdiff / old_wmax)
    except: pass
    
    return max (ret, ret2)

# ------------------------------------------------------------------------

old_ntot = 0.; old_nmax = 0.

def get_net_usage():

    global old_ntot, old_nmax
    ppp = 0.; tot = 0.0; buf = ""
    try:
        fh = open("/proc/net/dev");  buf = fh.read()
        fh.close()
    except:
        print "Error on getting net usage: ", sys.exc_info()
        return 0
    #print buf   
    buf3 = buf.split("\n")
    for aa in buf3:
        cc = []; dd =  aa.split(" "); 
        for bb in dd:
            if bb:                  # Filter empty
                cc.append(bb)
        if len(cc):
            if ":" in cc[0]:
                tot += float(cc[1]); tot += float(cc[2])
   
    # First run
    if old_ntot == 0.:
        old_ntot = tot
        
    ndiff = tot - old_ntot
    if old_nmax < ndiff:
        old_nmax = ndiff
    #print "tot", tot, "ndiff", ndiff, "old_nmax", old_nmax              
    old_ntot = tot; ret = 0
    try:
        ret = int(100 * ndiff / old_nmax)
    except: pass
    return ret
    
# ------------------------------------------------------------------------

def hexdump(buff):
    aaa = ""
    for aa in buff:
         aaa += "%02x " % ord(aa)
    return aaa
    
# ------------------------------------------------------------------------
# Cycle on the event buffer. Set a global var with key press count.

def run_thread(fd, arg):

    global event_count, thdone, verbose, conf
    
    if conf.verbose:
        print "Started thread", arg
        
    while 1:
        try:
            buff = fd.read(8)
            #if conf.pgdebug > 9:
            #    print hexdump(buff)
            event_count += 1
            if arg == 0:
                mw.led.flash()
            else:
                mw.led2.flash()
            if thdone:
                break
        except AttributeError:
            pass
        except:
            print "error in thread", sys.exc_info()
            break
        
# ------------------------------------------------------------------------

def monitor(monstr, idx):

    global nokey
    drv = "";  ddd = "/dev/input/by-path"
    
    # Find the driver
    dl = os.listdir(ddd)
    for aa in dl:
        if aa.find(monstr) >= 0:
            drv = ddd + "/" + aa
            break
    try:
        fd = open(drv, "r")
        tid = thread.start_new_thread(run_thread, (fd, idx))
    except:
        nokey = True
        print "Cannot open %s device, keyboard sleep " \
            "timeout on %s will not be available" % (monstr, drv)
        print "You may want to start pyload.py with sudo or as root."
        print sys.exc_info()

def main(tray = False):

    global mw, event_count, thdone, globals, filter, conf, nokey
    
    syslog.openlog("PyLoad")
    syslog.syslog("Started")
    
    globals = _Globals()
    
    if conf.timeout != 10:
        globals.xsleep = conf.timeout
    
    filter  = Filter()
    event_count = 1; thdone = False; nokey = False
    
    elevate_priv()
    monitor("kbd", 0)
    monitor("mouse", 1)
    drop_priv()

    ppp = get_proc_usage()
    nnn = get_net_usage()
    mw = MainWin(nokey)
    gobject.timeout_add(globals.rerate, handler_tick)
    
    if not tray:    
        gtk.main()
        done = True
        syslog.syslog("Ended")
        if conf.verbose:
            print "pyload ended"
        sys.exit(0)

def pyload_applet_factory(applet, iid):
    try:
        PyLoadapplet(applet, iid)
    except:
        print  sys.exc_info()
        traceback.print_tb(sys.exc_info()[2])
    return True

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
        #print self.__dict__    
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

# -------------------------------------------------------------------------
# Decorate additional vars, filters, carry it in config

conf.tray = False
conf.filter_cpu  = Filter()
conf.filter_net  = Filter()
conf.filter_disk = Filter()

# -------------------------------------------------------------------------

# Main applet code that creates the applet interface

class PYL_applet:

    def __init__(self, applet, iid):
         
        #syslog.syslog("Init Applet")       
        
        self.applet = applet
        self.apselect = None
        self.prefsdialog = None
        
        self.dict = {}
        self.ttext = " Processor Load Display\n"\
                     "Disk and Network Activity\n"\
                     "   System Sleep Timer"\
        
        # Start from a known place
        os.chdir(os.environ['HOME'])
        
        #<menuitem name="Item 2" verb="Props" label="_Preferences" pixtype="stock" pixname="gtk-properties"/>
        
        self.propxml = """
        <popup name="button3">
        <menuitem name="Item 1" verb="Load" label="Show _Load Window" pixtype="stock" pixname="gtk-properties"/>
        <menuitem name="Item 3" verb="About" label="_About ..." pixtype="stock" pixname="gnome-stock-about"/>
        </popup>
        """
        
        #( "Props",  self.props ),
        self.verbs = [  
                        ( "Load",  self.Load ),
                        ( "About",  self.about_info ) ]
            
        warnings.simplefilter("ignore", Warning)
        gnome.init("PyLoad", "0.05")
        warnings.simplefilter("default", Warning)
        
        try:
            self.logo_pixbuf = gtk.gdk.pixbuf_new_from_file(\
                        os.path.basename(imgname))
        except:
            try:
                self.logo_pixbuf = gtk.gdk.pixbuf_new_from_file("monitor.png")
            except:
                try:
                    self.logo_pixbuf = gtk.gdk.pixbuf_new_from_file(\
                        "/usr/share/pyload/monitor.png")
                except:
                    print "Cannot load image", sys.exc_info()
                    pass
            
        self.ev_box = gtk.EventBox()
        #self.applet.set_size_request(-1, -1)
        
        self.ev_box.connect("event", self.button_press)
        self.applet.connect("change-background", self.panel_bg)
        
        self.main_icon = gtk.Image()
        main_pixbuf = None
        
        try:
            main_pixbuf = gtk.gdk.pixbuf_new_from_file("monitor.png")
        except:
            try:
                main_pixbuf = gtk.gdk.pixbuf_new_from_file(\
                      "/usr/share/pyload/monitor.png")
            except:
                    print "Cannot load image", sys.exc_info()
       
        if main_pixbuf:    
            main_pixbuf2 = main_pixbuf.scale_simple(25, 25, gtk.gdk.INTERP_BILINEAR)
            self.main_icon.set_from_pixbuf(main_pixbuf2)
        else: 
            # This will let a broken image go through
            self.main_icon.set_from_file("")
             
        #self.label = gtk.Label("")
        self.main_hbox = gtk.HBox()
        
        self.main_hbox.pack_start(self.main_icon, False, False, 5)
        self.ev_box.add(self.main_hbox)
        
        self.main_hbox.show()
        
        applet.add(self.ev_box)
        applet.connect("destroy", self.cleanup, None)
        applet.show_all()
        
        # Set the tooltip
        self.main_hbox.set_has_tooltip(True)
        self.main_hbox.set_tooltip_text(self.ttext)
        gobject.timeout_add(100, self.startme)
       
    def startme(self): 
        # Start supplementary window
        try:
            main(True)
            mw.show_all()
            usleep(10)
            mw.hide()
        except:
            print  sys.exc_info()
        
    def show_tooltip(self, tip):
        #print tip
        pass
        
    def props(self, win, arg):
        #print "props pressed"
        pass

    def Load(self, win, arg):
        global mw
        #print "Load pressed"
        mw.show()

    def cleanup(self,event,widget):
        #print "Cleanup"
        del self.applet
        gtk.main_quit()
        
    def button_press(self,widget,event):
        if event.type == gtk.gdk.BUTTON_PRESS:
            #print "pressed main button", event.button
            if event.button == 3:
                self.create_menu()

            if  event.button == 1:
                pass
            
    # Handle Gnome Panel background
    def panel_bg(self, applet, bg_type, color, pixmap):
        # Reset styles
        rc_style = gtk.RcStyle()
        self.applet.set_style(None)
        self.ev_box.set_style(None)
        self.applet.modify_style(rc_style)
        self.ev_box.modify_style(rc_style)
        
        if bg_type == gnomeapplet.PIXMAP_BACKGROUND:
            style = self.applet.get_style()
            style.bg_pixmap[gtk.STATE_NORMAL] = pixmap
            self.applet.set_style(style)
            self.ev_box.set_style(style)
        if bg_type == gnomeapplet.COLOR_BACKGROUND:
            self.applet.modify_bg(gtk.STATE_NORMAL, color)
            self.ev_box.modify_bg(gtk.STATE_NORMAL, color)
            
    def about_info(self,event,data=None):
        about = gnome.ui.About("PyLoad", 
            "\nProcessor Load and System Sleep\n", 
                "Released to Public Domain by Peter Glen", 
                "Public Release One (0.05)", 
                    ["<Peter Glen> peterglen99@gmail.com"])
        about.show()

    def properties(self,event,data):
        if self.prefsdialog != None:
            self.prefsdialog.window.present()
        else:
            self.prefsdialog = preferencedialog.PreferenceDialog(status, settings)
        return 1

    def create_menu(self):
        self.applet.setup_menu(self.propxml, self.verbs, None)

def PYL_applet_factory(applet, iid):

    try:
        PYL_applet(applet, iid)
    except:
        print  sys.exc_info()
        traceback.print_tb(sys.exc_info()[2])
    return True
    
# ------------------------------------------------------------------------
# Starting here ... this is mainly for development

if len(sys.argv) == 2 and sys.argv[1].find("window") != -1:

    syslog.openlog("PyLoad")
    syslog.syslog("Starting in window")
    
    conf.tray = True
    #print "Starting in window"
    
    args = conf.comline(sys.argv[1:])
    
    def key_press_event(win, event):
        if event.keyval == gtk.keysyms.Escape:
            win.destroy()

    main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    main_window.set_title("PyLoad Applet")
    main_window.connect("key-press-event", key_press_event) 
    app = gnomeapplet.Applet()
    PYL_applet_factory(app, None)
    app.reparent(main_window)
    
    warnings.simplefilter("ignore", Warning)
    main_window.show_all()
    warnings.simplefilter("default", Warning)
    
    # Back off from privileged operation
    drop_priv()
    gtk.main()
    
    #print "Ended in window"
    syslog.syslog("Ended in window")
    sys.exit(0)

# ------------------------------------------------------------------------
# Start of program:

if __name__ == '__main__':

    # Back off from privileged operation
    drop_priv()
    
    #print  "Command line", sys.argv
    #print "uid", os.getuid(), "guid", os.getgid()
    #print "euid", os.geteuid(), "eguid", os.geteuid()

    args = conf.comline(sys.argv[1:])
    conf.tray = False
        
    for aa in sys.argv[1:]:
        if aa.find("--oaf") >= 0:
            conf.tray = True
            #print "Tray"
    
    # Regular execution:
    if not conf.tray:
        if conf.error:
            sys.exit(1)
    
        if conf.timeout < 1 or conf.timeout > 120:
            print "Minutes (option -t) must be between 1 - 120."
            sys.exit(1)
        main()
    # GNOME System tray
    else:
        # Redirect to a file in /tmp (debug only) This solves the difficulty 
        # in seeing stdout while in tray mode.
        if 1:
            pylog = open("/tmp/pylog", "w")
            pylog.write("Started pylog.\n")
            sys.stdout = pylog;  sys.stderr = pylog
            # Set these for tray
            conf.verbose = 1; conf.pgdebug = 10
            print "Channelled stdout"
            print sys.argv
            
        try:
            gnomeapplet.bonobo_factory("OAFIID:GNOME_PYLApplet_Factory",
                    gnomeapplet.Applet.__gtype__,"", "0", PYL_applet_factory)
        except:
            print  sys.exc_info()
            syslog.syslog("Ended with exception. %s", sys.exc_info()[1])
            sys.exit(1)
    









