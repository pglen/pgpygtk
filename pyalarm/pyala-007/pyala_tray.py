#!/usr/bin/env python
                                        
# Extracted pyala tray part for SUDO separation

import os, sys, subprocess, syslog, gtk, traceback, signal
import pwd, shlex, gnomeapplet, warnings, gnome.ui, gobject

# -------------------------------------------------------------------------

# Main applet code that creates the applet interface

class PYAla_applet:

    def __init__(self, applet, iid):
         
        syslog.syslog("Started")       
        
        self.applet = applet
        self.apselect = None
        self.prefsdialog = None
        
        self.dict = {}
        self.ttext = " System Alarm and Wake"
        
        # Start from a known place
        os.chdir(os.environ['HOME'])
        
        #<menuitem name="Item 2" verb="Props" label="_Preferences" pixtype="stock" pixname="gtk-properties"/>
        
        self.propxml = """
        <popup name="button3">
        <menuitem name="Item 1" verb="Load" label="_Show Window" pixtype="stock" pixname="gtk-properties"/>
        <menuitem name="Item 3" verb="About" label="_About ..." pixtype="stock" pixname="gnome-stock-about"/>
        </popup>
        """
        
        #( "Props",  self.props ),
        self.verbs = [  
                        ( "Load",  self.Load ),
                        ( "About",  self.about_info ) ]
            
        warnings.simplefilter("ignore", Warning)
        gnome.init("pyala", "0.05")
        warnings.simplefilter("default", Warning)
        
        try:
            self.logo_pixbuf = gtk.gdk.pixbuf_new_from_file(\
                        os.path.basename(imgname))
        except:
            try:
                self.logo_pixbuf = gtk.gdk.pixbuf_new_from_file("ala.png")
            except:
                try:
                    self.logo_pixbuf = gtk.gdk.pixbuf_new_from_file(\
                        "/usr/share/pyala/ala.png")
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
            main_pixbuf = gtk.gdk.pixbuf_new_from_file("ala.png")
        except:
            try:
                main_pixbuf = gtk.gdk.pixbuf_new_from_file(\
                      "/usr/share/pyala/ala.png")
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
        # Start main app window, hide it
        self.start_app("-i")
        
    def start_app(self, opt = None):
        try:
            syslog.syslog("Showing Window")       
            args = []
            args.append("/usr/bin/sudo")
            args.append("/usr/bin/pyala.py")
            if opt:
                args.append(opt)
            #print "args", args
            sp = subprocess.Popen(args)
        except:
            #print  sys.exc_info()
            syslog.syslog(sys.exc_info())       
        
    def show_tooltip(self, tip):
        #print tip
        pass
        
    def props(self, win, arg):
        #print "props pressed"
        pass

    def Load(self, win, arg):
        self.start_app()

    def cleanup(self, event = None, widget = None):
        #print "Cleanup"
        self.start_app("-m")
        syslog.syslog("Ended.")       
        del self.applet
        #gtk.main_quit()
        
    def button_press(self,widget,event):
        if event.type == gtk.gdk.BUTTON_PRESS:
            #print "pressed main button", event.button
            if event.button == 3:
                self.create_menu()

            if  event.button == 1:
                self.start_app()
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
        about = gnome.ui.About("PyAla", 
            "\nSystem Wake and Alarm\n", 
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

def PYAla_applet_factory(applet, iid):

    global xapplet
    try:
        xapplet = PYAla_applet(applet, iid)
    except:
        print  sys.exc_info()
        traceback.print_tb(sys.exc_info()[2])
    return True

# ------------------------------------------------------------------------
# Starting here ... this is mainly for development

if len(sys.argv) == 2 and sys.argv[1].find("window") != -1:

    syslog.openlog("pyala")
    syslog.syslog("Starting in window")
    
    #print "Starting in window"
    
    def key_press_event(win, event):
        global xapplet
        if event.keyval == gtk.keysyms.Escape:
            gtk.main_quit()
            #sys.exit(0)
            #xapplet.cleanup()

    main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    main_window.set_title("pyala Applet")
    main_window.connect("key-press-event", key_press_event) 
    app = gnomeapplet.Applet()
    PYAla_applet_factory(app, None)
    app.reparent(main_window)
    
    warnings.simplefilter("ignore", Warning)
    main_window.show_all()
    warnings.simplefilter("default", Warning)
    
    gtk.main()
    
    #print "Ended in window"
    syslog.syslog("Ended in window")
    sys.exit(0)

# ------------------------------------------------------------------------
# Start of program:

if __name__ == '__main__':

    # Redirect to a file in /tmp (debug only) This solves the difficulty 
    # in seeing stdout while in tray mode.
    if 1:
        pylog = open("/tmp/pyala_tray", "w")
        pylog.write("Started pyala tray starter.\n")
        sys.stdout = pylog;  sys.stderr = pylog
        # Set these for tray
        print "Channelled stdout"
        print sys.argv
        print os.environ['PATH']
        print os.environ['HOME']
        print "uid", os.getuid(), "guid", os.getgid()
        print "euid", os.geteuid(), "eguid", os.geteuid()
        
    syslog.openlog("PyAla tray")

    try:
        gnomeapplet.bonobo_factory("OAFIID:GNOME_PYAlaApplet_Factory",
                gnomeapplet.Applet.__gtype__,"", "0", PYAla_applet_factory)
    except:
        print  sys.exc_info()
        syslog.syslog("Ended with exception. %s", sys.exc_info()[1])
        sys.exit(1)







