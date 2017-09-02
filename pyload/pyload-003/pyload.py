#!/usr/bin/env python

# Load monitor and system sleep application. Kept in one file for 
# robust portability. Tested on LINUX only.
# See README for deployment.

import os, sys, glob, getopt, time, string, signal, stat, shutil, syslog
import gobject, gtk, pango, math, traceback, subprocess, thread
import pwd, shlex, gnomeapplet, warnings, gnome.ui

(
  COLOR_RED,
  COLOR_GREEN,
  COLOR_BLUE
) = range(3)

(
  SHAPE_SQUARE,
  SHAPE_RECTANGLE,
  SHAPE_OVAL,
) = range(3)

mained = None

# ------------------------------------------------------------------------
# Callback for rigth click menu

def rclick_action(self, arg):

    #print "rclick_action", "'" + arg.name + "'" 
    
    if arg.name == "<pydoc>/New":
        mained. newfile()        
        
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
            ( "/New",           "<control>N",   rclick_action, 0, None ),
            ( "/sep1",          None,           None, 0, "<Separator>" ),
            ( "/Open",          "<control>O",   rclick_action, 0, None ),
            ( "/Save",          "<control>S",   rclick_action, 0, None ),
            ( "/SaveAs",        None,           rclick_action, 0, None ),
            ( "/sep1",          None,           None, 0, "<Separator>" ),
            ( "/Copy",          "<control>C",   rclick_action, 0, None ),
            ( "/Cut",           "<control>X",   rclick_action, 0, None ),
            ( "/Paste",         "<control>V",   rclick_action, 0, None ),
            ( "/sep1",          None,           None, 0, "<Separator>" ),
            ( "/Exit",          "<alt>x",       rclick_quit, 0, None ),
            )
    
def create_action_group(self):
    # GtkActionEntry
    entries = (
      ( "FileMenu", None, "_File" ),                # name, stock id, label
      ( "EditMenu", None, "_Edit" ),                
      ( "PreferencesMenu", None, "Settings" ),      
      ( "NavMenu", None, "Navigation" ),            
      ( "MacrosMenu", None, "_Macros" ),            
      ( "ColorMenu", None, "_Color"  ),             
      ( "ShapeMenu", None, "Shape" ),               
      ( "WinMenu", None, "Windows" ),               
      ( "HelpMenu", None, "_Help" ),                
      
      # -------------------------------------------------------------------
      
      ( "New", gtk.STOCK_NEW,                       # name, stock id
        "_New", "<control>N",                       # label, accelerator
        "Create a new file",                        # tooltip
        self.activate_action ),
        
      ( "Open", gtk.STOCK_OPEN,                   
        "_Open","<control>O",                     
        "Open a file",                            
        self.activate_action ),                   
        
      ( "Close", gtk.STOCK_CLEAR,                 
        "_Close","<control>W",                    
        "Close current buffer",                   
        self.activate_action ),                   
        
      ( "Save", gtk.STOCK_SAVE,                   
        "_Save","<control>S",                     
        "Save current file",                      
        self.activate_action ),                   
        
      ( "SaveAs", gtk.STOCK_SAVE,                 
        "Save _As...", "<control><shift>S",       
        "Save to a file",                         
        self.activate_action ),                   
        
      ( "Quit", gtk.STOCK_QUIT,                   
        "_Quit  (No Save)", "<control>Q",         
        "Quit program, abandon files",            
         self.activate_quit ),             
                
      ( "Exit", gtk.STOCK_CLOSE,                  
        "_Exit", "<alt>X",                        
        "Exit program, save files",               
         self.activate_exit ),                    
                                                  
      ( "Cut", gtk.STOCK_CUT,                     
        "Cu_t   \t\tCtrl-C", "",                    
        "Cut selection to clipboard",             
         self.activate_action ),
                           
       ( "Copy", gtk.STOCK_COPY,                  
        "_Copy   \t\tCtrl-C", "",                   
        "Copy selection to clipboard",            
         self.activate_action ),                  
         
      ( "Paste", gtk.STOCK_PASTE,                 
        "_Paste  \t\tCtrl-V", "",                   
        "Paste clipboard into text",              
         self.activate_action ),                  
         
      ( "Undo", gtk.STOCK_UNDO,                   
        "_Undo  \t\tCtrl-Z", "",                    
        "Undo last Edit",                         
         self.activate_action ),                  
         
      ( "Redo", gtk.STOCK_REDO,                   
        "_Redo  \t\tCtrl-Y", "",                    
        "Redo last Undo",                         
         self.activate_action ),                  
         
      ( "Discard Undo", gtk.STOCK_REDO,           
        "Discard Undo / Redo", "",                
        "Discard all undo / redo information",    
         self.activate_action ),                  
         
      ( "Spell", gtk.STOCK_REDO,                   
        "_Spell (code) \tF9", "",                    
        "Spell Buffer (code mode)",                         
         self.activate_action ),                  
         
      ( "Spell2", gtk.STOCK_REDO,                   
        "S_pell (text) \tShift-F9", "",                    
        "Spell Buffer (text mode)",                         
         self.activate_action ),                  
         
      ( "Settings", gtk.STOCK_REDO,           
        "Settings", "",                
        "Change program settings",    
         self.activate_action ),                  
                                                  
      ( "Goto", gtk.STOCK_INDEX,       
        "Goto Line\t\tAlt-G", "",        
        "Goto line in file",           
         self.activate_action ),       
         
      ( "Find", gtk.STOCK_FIND,        
        "Find in File \t\tCtrl-F", "",   
        "Find line in file",           
         self.activate_action ),                  
         
      ( "Next", None,                             
        "Next Match \t\tAlt-N F6", "",              
        "Goto Next match in file",                
         self.activate_action ),                  
         
        ( "Prev", None,                           
        "Prev Match\t\tAlt-P F5", "",               
        "Goto previous match in file",            
         self.activate_action ),                  
         
        ( "Begin", None,                          
        "Begin of doc\t\tCtrl-Home", "",            
        "Goto the beginning of document",         
         self.activate_action ),                  
         
        ( "End", None,                            
        "End of doc\t\tCtrl-End", "",               
        "Goto the end of document",               
         self.activate_action ),                  
                                                  
      ( "Record", gtk.STOCK_MEDIA_RECORD,         
        "Start / Stop Record\t\tF7", "",            
        "Start / Stop Recording macro",           
         self.activate_action ),                  
         
      ( "Play", gtk.STOCK_MEDIA_PLAY,   
        "Play Macro       \t\tF8", "",             
        "Play macro",                   
         self.activate_action ),                  
         
      ( "Animate", None,                
        "_Animate macro\t\tShift-F8", None,                  
        "Play macro with animation effect",
         self.activate_action ),                  
         
      ( "Savemacro", None,                        
        "Save macro", None,                       
        "Save macro to file",      
         self.activate_action ),                  
         
      ( "Loadmacro", None,                        
        "Load macro", None,                       
        "Load macro from file",    
         self.activate_action ),                  
                                                  
      ( "Colors", None,            
        "Set Colors", None,                       
        "Set Editor window colors",  
         self.activate_action ),                  
                                                  
      ( "Fonts", None,               
        "Set Font", None,           
        "Set Editor Window Font",   
         self.activate_action ),

      ( "NextWin", None,               
        "Next Window\t\tAlt-PgUp", None,           
        "Switch to next window",   
         self.activate_action ),
         
      ( "PrevWin", None,               
        "Prev. Window\t\tAlt-PgDn", None,           
        "Switch to next window",   
         self.activate_action ),
         
      ( "SaveAll", None,               
        "Sava All   \t\tAlt-A", None,           
        "Save all Buffers",   
         self.activate_action ),

      ( "ShowLog", None,               
        "Show Log", None,           
        "Show log window",   
         self.activate_action ),

      ( "About", "demo-gtk-logo",          
        "_About", "",                      
        "About",                           
        self.activate_about ),
        
      ( "QuickHelp", gtk.STOCK_INFO,       
        "_Quick Help", "",                 
        "Show quick help",                 
        self.activate_qhelp ),
      
      ( "KeyHelp", gtk.STOCK_INFO,       
        "_Key Help         \tF3", "",                 
        "Show keyboard help",                 
        self.activate_khelp ),
                
      ( "DevHelp", gtk.STOCK_INFO,       
        "_Developer Help\tF2", "",                 
        "Show developer help",                 
        self.activate_dhelp ),
        
        ( "Help", gtk.STOCK_HELP,          
         "_Help        \t\tF1", "",                      
        "Show Help",                       
        self.activate_action ),
        
      ( "Logo", "demo-gtk-logo",           
         None, None,                       
        "GTK+",                            
        self.activate_action ),                    
    );

    # GtkToggleActionEntry
    toggle_entries = (
      ( "Bold", gtk.STOCK_BOLD,                    # name, stock id
         "_Bold", "<control>B",                    # label, accelerator
        "Bold",                                    # tooltip
        self.activate_action,
        True ),                                    # is_active
    )

    # GtkRadioActionEntry
    color_entries = (
      ( "Red", None,                               # name, stock id
        "_Red", "<control><shift>R",               # label, accelerator
        "Blood", COLOR_RED ),                      # tooltip, value
      ( "Green", None,                             # name, stock id
        "_Green", "<control><shift>G",             # label, accelerator
        "Grass", COLOR_GREEN ),                    # tooltip, value
      ( "Blue", None,                              # name, stock id
        "_Blue", "<control><shift>B",              # label, accelerator
        "Sky", COLOR_BLUE ),                       # tooltip, value
    )

    # GtkRadioActionEntry
    shape_entries = (
      ( "Square", None,                            # name, stock id
        "_Square", "<control><shift>S",            # label, accelerator
        "Square",  SHAPE_SQUARE ),                 # tooltip, value
      ( "Rectangle", None,                         # name, stock id
        "_Rectangle", "<control><shift>R",         # label, accelerator
        "Rectangle", SHAPE_RECTANGLE ),            # tooltip, value
      ( "Oval", None,                              # name, stock id
        "_Oval", "<control><shift>O",              # label, accelerator
        "Egg", SHAPE_OVAL ),                       # tooltip, value
    )

    # Create the menubar and toolbar
    action_group = gtk.ActionGroup("AppWindowActions")
    action_group.add_actions(entries)
    #action_group.add_toggle_actions(toggle_entries)
    #action_group.add_radio_actions(color_entries, COLOR_RED, self.activate_radio_action)
    #action_group.add_radio_actions(shape_entries, SHAPE_OVAL, self.activate_radio_action)

    return action_group

# -----------------------------------------------------------------------
# Sleep just a little, but allow the system to breed

def  usleep(msec):

    got_clock = time.clock() + float(msec) / 1000
    #print got_clock
    while True:
        if time.clock() > got_clock:
            break
        gtk.main_iteration_do(False)

# Pop up dialog

def getstr(title, message, oldstr = ""):

    dialog = gtk.Dialog(title,
                   None,
                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)

    sp = "   "
    try:
        dialog.set_icon_from_file("monitor.png")
    except:
        try:
            dialog.set_icon_from_file( \
                "/usr/local/share/icons/hsencfs/hsicon.png")
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
    if conf.pgdebug > 5:
        print "uid", os.getuid(), "guid", os.getgid()
        print "euid", os.geteuid(), "eguid", os.geteuid()

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
    ppp = string.split(os.environ['PATH'], os.pathsep)
    for aa in ppp:
        ttt = aa + os.sep + fname
        if conf.pgdebug > 9:
            print "respath", ttt
        if os.path.isfile(ttt):
            return ttt
            
# ------------------------------------------------------------------------

class MainWin(gtk.Window):

    # Create the toplevel window
    def __init__(self, nokey = False, parent=None):
    
        global globals, conf
        self.nokey = nokey
        gtk.Window.__init__(self)
      
        #self.set_decorated(False)
        #self.set_has_frame(True)
          
        '''try:
            self.set_screen(parent.get_screen())
        except AttributeError:'''
            
        if conf.tray:
            pass
        else: 
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.titlex = "Processor PayLoad"
        if nokey:
            self.set_title(self.titlex + " (No Keyboard Monitoring)")
        else:
            self.set_title(self.titlex)
        
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
        buttonh.set_tooltip_text("Hide Program")
        
        buttonx = gtk.Button(" E_xit ");
        buttonx.connect("clicked", self.exit)
        buttonx.set_tooltip_text("Exit program")
        
        self.prog = gtk.Label("Started")
        globals.erasecnt = 5000
        
        entry14 = gtk.Label("           ")
        buttonbox2.pack_start(entry14, False, False)
        buttonbox2.pack_start(self.armbutt, False, False)
        buttonbox2.pack_start(button23, False, False)
        buttonbox2.pack_start(buttonh, False, False)
        if not conf.tray:
            buttonbox2.pack_start(buttonx, False, False)
        buttonbox2.pack_start(self.prog)
        
        vpaned.pack1(self.area, True, False)
        #vpaned.pack2(buttonbox2, False, False)
        vpaned.pack2(buttonbox2, False, True)
        
        hpaned.pack1(buttonbox)
        hpaned.pack2(vpaned)
        hpaned.set_position(120)
        
        self.add(hpaned)
        self.show_all()
   
    def hidebutt(self, butt):
        self.hide()
        
    def exit(self, butt):
        self.destroy()
        #sys.exit(0)
    
    def idle(self, area):
        global globals
        globals.program = getstr("Idle Program", \
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
                mm = self.build_menu(self.window, rclick_menu)
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
                mm = self.build_menu(self.window, rclick_menu)
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
        if warn == 29:
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
        print "Exception in timer handler buttom", sys.exc_info()
          
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

def main(tray = False):

    global mw, keycount, thdone, globals, filter, conf
    
    syslog.openlog("PyLoad")
    syslog.syslog("Started")
    
    globals = Globals()
    try:
        globals.xsleep = conf.timeout
    except: pass
    
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
conf.pgdebug = 0
conf.tray = False

# -------------------------------------------------------------------------

# Main applet code that creates the applet interface

class PYL_applet:

    def __init__(self, applet, iid):
         
        #syslog.syslog("Init Applet")       
        
        self.applet = applet
        self.apselect = None
        self.prefsdialog = None
        
        self.dict = {}
        self.ttext = "Processor Load Display\n"\
                     "  System Sleep timer "
        
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
        gnome.init("HSTray", "1.03")
        warnings.simplefilter("default", Warning)
        
        try:
            self.logo_pixbuf = gtk.gdk.pixbuf_new_from_file(\
                        os.path.basename(imgname))
        except:
            try:
                self.logo_pixbuf = gtk.gdk.pixbuf_new_from_file(imgname)
            except:
                try:
                    self.logo_pixbuf = gtk.gdk.pixbuf_new_from_file(imgname2)
                except:
                    pass
            
        self.ev_box = gtk.EventBox()
        #self.applet.set_size_request(-1, -1)
        
        self.ev_box.connect("event", self.button_press)
        self.applet.connect("change-background", self.panel_bg)
        
        self.main_icon = gtk.Image()
        main_pixbuf = None
        
        try:
            main_pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.basename(imgname))
        except:
            try:
                #global imgname
                main_pixbuf = gtk.gdk.pixbuf_new_from_file(imgname)
            except:
                try:
                    main_pixbuf = gtk.gdk.pixbuf_new_from_file(imgname2)
                except:    
                    pass
                    #print "img", sys.exc_info()
       
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
        print "Load pressed"
        mw.show()

    def cleanup(self,event,widget):
        del self.applet

    # Update the display on a regular interval (unused)
    def timeout_callback(self,event):
        #print "Timeout callback"
        return 1
        
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
                "Public Release One (0.03)", 
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
    print "starting in window"
    
    args = conf.comline(sys.argv[1:])
    
    def key_press_event(win, event):
        if event.keyval == gtk.keysyms.Escape:
            win.destroy()

    main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    main_window.set_title("PyLoad Applet")
    #main_window.connect("destroy", gtk.main_quit) 
    main_window.connect("key-press-event", key_press_event) 
    app = gnomeapplet.Applet()
    PYL_applet_factory(app, None)
    app.reparent(main_window)
    main_window.show_all()
    
    # Back off from privileged operation
    drop_priv()
    main(True)
    mw.hide()
    gtk.main()
    
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
            print "Tray"
    
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
        pylog = open("/tmp/pylog", "w")
        pylog.write("Started pylog.\n")
        sys.stdout = pylog;  sys.stderr = pylog
        try:
            gnomeapplet.bonobo_factory("OAFIID:GNOME_PYLApplet_Factory",
                    gnomeapplet.Applet.__gtype__,"", "0", PYL_applet_factory)
        except:
            print  sys.exc_info()
            syslog.syslog("Ended with exception. %s", sys.exc_info()[1])
            sys.exit(1)
    

