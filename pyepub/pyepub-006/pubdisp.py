#!/usr/bin/env python

import sys, os, re, subprocess, signal
import pygtk, gobject, pango, copy

import warnings; warnings.simplefilter("ignore"); 
import gtk; warnings.simplefilter("default")

import pubutil

treestore = None

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

# ------------------------------------------------------------------------

xsize = 0

class PubView(gtk.Window):

    hovering_over_link = False
    waiting = False

    hand_cursor = gtk.gdk.Cursor(gtk.gdk.HAND2)
    regular_cursor = None #gtk.gdk.Cursor(gtk.gdk.XTERM)
    wait_cursor = gtk.gdk.Cursor(gtk.gdk.WATCH)
    callback = None
    bscallback = None

    # Create the toplevel window
    def __init__(self, config, parent=None):
    
        self.cnt = 1
        self.config = config
        self.full = False
        self.move = None; self.mark = None
        self.deftitle = "ePub Viewer: "
        self.speech_pid = None        
        self.iterlist = [];  self.iterlist2 = []
        self.stags = []; self.xtags = []; 
                
        gtk.Window.__init__(self)
        
        self.connect("unmap", self.OnExit)
        
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        try:
            self.set_icon_from_file("epub.png")
        except:
            try:
                self.set_icon_from_file("/usr/share/pyepub/epub.png")
            except:
                print "Cannot load app icon."

        www = gtk.gdk.screen_width(); hhh = gtk.gdk.screen_height();
        self.set_default_size(3*www/4, 3*hhh/4)

        if self.config.fullscreen:
            self.set_default_size(www, hhh)
        
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title(self.deftitle);

        hpaned = gtk.HPaned()
        hpaned.set_border_width(2)
        
        vpaned = gtk.VPaned()
        vpaned.set_border_width(2)
        
        self.add(hpaned)
                 
        view1 = gtk.TextView();
        view1.set_border_width(0)
        view1.set_left_margin(8); view1.set_right_margin(8)

        view1.connect("key-press-event", self.key_press_event)
        view1.connect("event-after", self.event_after)
        view1.connect("expose-event", self.expose_event)
        view1.connect("motion-notify-event", self.motion_notify_event)
        view1.connect("visibility-notify-event", self.visibility_notify_event)
        
        self.view = view1

        self.buffer_1 = view1.get_buffer()
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.add(view1)
       
        view2 = gtk.TextView();
        #view2.set_border_width(8)
        view2.set_editable(False)
        view2.set_wrap_mode(gtk.WRAP_WORD)
        
        self.buffer_2 = view2.get_buffer()
        sw2 = gtk.ScrolledWindow()
        sw2.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw2.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw2.add(view2)
        
        view2.connect("key-press-event", self.key_press_event2)
        view2.connect("event-after", self.event_after2)
        view2.connect("motion-notify-event", self.motion_notify_event2)
        view2.connect("visibility-notify-event", self.visibility_notify_event2)
       
        vbox = gtk.VBox(); vbox.set_spacing(5)
        vbox.add(sw)
        
        lab1 = gtk.Label("Idle"); lab1.set_justify(gtk.JUSTIFY_RIGHT)
        lab2 = gtk.Label(" ");
        butt1 = gtk.Button(" Show TOC File ");
        butt2 = gtk.Button(" Next ");
        butt3 = gtk.Button(" Prev ");
        self.butt4 = gtk.Button(" Read "); 
        self.butt4.connect("pressed", self.read_tts)
        butt5 = gtk.Button(" Home ");
        
        hbox = gtk.HBox();
        hbox.pack_start(butt1, False)
        hbox.pack_start(butt2, False)
        hbox.pack_start(butt3, False)
        hbox.pack_start(self.butt4, False)
        hbox.pack_start(butt5, False)
        hbox.pack_start(lab1)
        hbox.pack_start(lab2, False)
        vbox.pack_end(hbox, False)
        self.prog = lab1
        
        vpaned.add(sw2)
        vpaned.add2(vbox)
        hpaned.add2(vpaned)

        treeview = self.create_tree()
        treeview.connect("row-activated",  self.tree_sel)
        treeview.connect("cursor-changed",  self.tree_sel_row)
        treeview.connect("key-press-event", self.key_press_event3)
        self.treeview = treeview
        
        sw3 = gtk.ScrolledWindow()
        sw3.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw3.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw3.add(treeview)
        frame2 = gtk.Frame(); frame2.add(sw3)
        hpaned.add(frame2)
        self.hpaned = hpaned        
        hpaned.set_position(200)
        vpaned.set_position(1)
        self.iter = self.buffer_1.get_iter_at_offset(0)
        self.iter2 = self.buffer_2.get_iter_at_offset(0)
        self.set_focus(view1)
        self.show_all()
    
    def OnExit(self, arg):
        if self.speech_pid:
            self.stop_tts()
    
    # Stop tts instances, kill (all) children
    def read_tts(self, butt):
        # Running?
        if self.speech_pid:
            self.stop_tts()
            return      
        self.butt4.set_label("Stop") 
        clip = gtk.Clipboard()
        self.buffer_1.copy_clipboard(clip)
        cstr = clip.wait_for_text()
        gobject.timeout_add(100,  self.speak, cstr)
    
    def stop_tts(self):
        try:
            dl = os.listdir("/proc")
            for aa in dl:
                fname = "/proc/" + aa + "/stat"
                if os.path.isfile(fname):
                    ff = open(fname, "r").read().split()
                    if  self.speech_pid.pid == int(ff[3]):
                        os.kill(int(ff[0]), signal.SIGKILL)
        except:
            pubutil.print_exception("Cannot kill", self.speech_pid.pid)
        self.speech_pid = None
        self.butt4.set_label("Read") 
        return

    def invalidate(self):
        rc = self.view.get_allocation()
        self.view.queue_draw_area(0, 0, rc.width, rc.height)
    
    def tree_sel_row(self, xtree):
        sel = xtree.get_selection()
        xmodel, xiter = sel.get_selected()
        xstr = xmodel.get_value(xiter, 0)
        #print "tree_sel_row", xstr
        cnt = 0
        for aa in self.stags:
            if aa == xstr:
                #print "got", aa, self.xtags[cnt]
                mm = self.buffer_1.get_mark(self.xtags[cnt])
                if mm:
                    self.view.scroll_to_mark(mm, 0.0, True, 0, 0)
                else:
                    # This is a link
                    #print "link", self.xtags[cnt]
                    self.loader(self.xtags[cnt])
                break;
            cnt += 1
        
    def tree_sel(self, xtree, xiter, xpath):
        pass
        print "tree_sel", xtree, xiter, xpath
        # Focus on main doc
        #vcurr = notebook.get_nth_page(notebook.get_current_page())
        #self.window.activate_focus()
        #self.window.set_focus(vcurr.vbox.area)

    # Create a file, send it to festival
    def speak(self, cstr):
        fname = self.config.data_dir + "/festival.txt"
        try:
            fh = open(fname, "w")
            fh.write(cstr)
        except:
            pubutil.print_exception("Cannot create festival file")
            return
        self.speech_pid = subprocess.Popen(["festival", "--tts", fname])
        print "started", self.speech_pid.pid
        gobject.timeout_add(1000, self.check_speak)

    # Timer to see if the speaker has terminated
    def check_speak(self):
        found = False
        dl = os.listdir("/proc")
        for aa in dl:
            fname = "/proc/" + aa + "/stat"
            if os.path.isfile(fname):
                try:
                    ff = open(fname, "r").read().split()
                    if  self.speech_pid.pid == int(ff[0]):
                        # Zombie does not count:
                        if ff[2] != "Z":
                            found = True
                except: pass
        if not found:
            self.butt4.set_label("Read")             
            self.speech_pid = None
        else:            
            # Look for termination again
            gobject.timeout_add(1000, self.check_speak)
        

    # --------------------------------------------------------------------
    def start_tree(self):

        global treestore

        if not treestore:
            treestore = gtk.TreeStore(str)

        # Delete previous contents
        try:
            while True:
                root = treestore.get_iter_first()
                if not root:
                    break
                try:
                    treestore.remove(root)
                except:
                    print "Exception on rm treestore"
        except:
            print  "strt_tree", sys.exc_info()
            pass

        #piter = treestore.append(None, ["Extracting .."])
        #treestore.append(piter, ["None .."])
        
    # --------------------------------------------------------------------
    def create_tree(self, text = None):

        global treestore
        self.start_tree()

        # create the TreeView using treestore
        tv = gtk.TreeView(treestore)

        # create a CellRendererText to render the data
        cell = gtk.CellRendererText()

        # create the TreeViewColumn to display the data
        tvcolumn = gtk.TreeViewColumn('_Sections')

        # add the cell to the tvcolumn and allow it to expand
        tvcolumn.pack_start(cell, True)

        # set the cell "text" attribute to column 0 - retrieve text
        # from that column in treestore
        tvcolumn.add_attribute(cell, 'text', 0)

        # add tvcolumn to treeview
        tv.append_column(tvcolumn)
        return tv

    def update_tree(self, xstr, tag):
        global treestore
        #print  "update_tree", xstr, tag
        lim = 32
        if len(xstr) > lim:
            xstr = xstr[:lim-3] + " ... "
            
        # Crate unique chapter 
        xstr2 = xstr
        # Try first decorated
        if xstr2 in self.stags:
            xstr2 = xstr + " (" + str(self.cnt) + ")"
        while 1:
            if xstr2 in self.stags:
                self.cnt += 1; 
                xstr2 = xstr + " (" + str(self.cnt) + ")"
            else:
                xstr = xstr2
                break
                
        self.stags.append(xstr)
        self.xtags.append(tag)
        try:
            piter = treestore.append(None, [xstr])
        except:
            print  "Exception in append treestore", sys.exc_info()

    def clear_tree(self):
        global treestore
        # Delete previous contents
        try:
            while True:
                root = treestore.get_iter_first()
                if not root:
                    break
                try:
                    treestore.remove(root)
                except:
                    print "except: treestore remove"
        except:
            print  "update_tree", sys.exc_info()
            pass
                 
    def expose_event(self, win, eve):
        #print win, eve
        if self.move:
            self.view.scroll_to_iter(self.move, 0.1, True, 0, 0)
            self.move = None
            
        if self.mark:
            print "Scroll to mark"
            self.view.scroll_to_mark(self.mark, 0.1, True, 0, 0)
            self.mark = None

    #def set_pane_position(self, pos):        
    #    self.hpaned.set_position(pos);
    #def set_fullscreen(self):
    #    www = gtk.gdk.screen_width();
    #    hhh = gtk.gdk.screen_height();
    #    self.resize(www, hhh)
        
    def apply_size(self):
        self.buffer_1.get_tag_table().foreach(self.tag_iter)

    def showcur(self, flag):
        #return
        self.waiting = flag
        wx, wy, modx = self.view.window.get_pointer()
        bx, by = self.view.window_to_buffer_coords(gtk.TEXT_WINDOW_WIDGET, wx, wy)
        self.set_cursor_if_appropriate (self.view, bx, by)
        self.view.window.get_pointer()

    # We manipulate the buffers through these functions:

    def clear(self, flag=False):
        if flag:
            self.buffer_2.set_text("", 0)        
            self.iter2 = self.buffer_2.get_iter_at_offset(0)        
            self.iterlist2 = []
        else:
            self.buffer_1.set_text("", 0)        
            self.iter = self.buffer_1.get_iter_at_offset(0)
            self.iterlist = []
                    
    def add_pixbuf(self, pixbuf, flag=False):
        if flag:
            self.buffer_2.insert_pixbuf(self.iter2, pixbuf)
        else:
            self.buffer_1.insert_pixbuf(self.iter, pixbuf)
        self.waiting = False

    def add_broken(self, flag=False):
        pixbuf = gtk.gdk.pixbuf_new_from_xpm_data(xpm_data)
        if flag:
            self.buffer_2.insert_pixbuf(self.iter2, pixbuf)
        else:
            self.buffer_1.insert_pixbuf(self.iter, pixbuf)
        self.waiting = False

    def add_text(self, text, flag=False):
        if flag:
            self.buffer_2.insert(self.iter2, text)
        else:
            self.buffer_1.insert(self.iter, text)            
        self.waiting = False
                
    def add_text_tag(self, text, tags, flag=False):
        if flag:
            self.buffer_2.insert_with_tags_by_name(self.iter2, text, tags)
        else:
            self.buffer_1.insert_with_tags_by_name(self.iter, text, tags)
        self.waiting = False

    def add_text_xtag(self, text, tags, flag=False):        
        if flag:
            try: self.buffer_2.get_tag_table().add(tags)
            except: pass
            self.buffer_2.insert_with_tags(self.iter2, text, tags)
        else:
            try: self.buffer_1.get_tag_table().add(tags)
            except: pass
            self.buffer_1.insert_with_tags(self.iter, text, tags)
        self.waiting = False

    def add_text_mark(self, name):
        cc = self.iter.copy()
        mmm = self.buffer_1.create_mark(name, cc, True)
        #print "'" + name + "'", mmm, cc
        
    # --------------------------------------------------------------------
    def key_press_event3(self, text_view, event):
        #print "event3", event.keyval
        
        if event.keyval == gtk.keysyms.F11: 
            if not self.full:
                self.window.fullscreen(); self.full = True
            else:
                self.window.unfullscreen(); self.full = False
                
        elif event.keyval == gtk.keysyms.F12:
            self.view.get_window(gtk.TEXT_WINDOW_WIDGET).focus() 
            pass

        if event.keyval == gtk.keysyms.Escape or event.keyval == gtk.keysyms.q:
            sys.exit(0)
        if event.state & gtk.gdk.MOD1_MASK:       
            if event.keyval == gtk.keysyms.x or event.keyval == gtk.keysyms.X:
                sys.exit(0)            
                
    # --------------------------------------------------------------------
    # Links can be activated by pressing Enter.
    
    def key_press_event(self, text_view, event):
        global xsize
        
        if (event.keyval == gtk.keysyms.Return or
            event.keyval == gtk.keysyms.KP_Enter):
            buffer = text_view.get_buffer()
            iter = buffer.get_iter_at_mark(buffer.get_insert())
            self.follow_if_link(text_view, iter)
        elif event.keyval == gtk.keysyms.Tab: 
            #print "Tab"
            pass
        elif event.keyval == gtk.keysyms.space: 
            #print "Space"
            pass
        elif event.keyval == gtk.keysyms.BackSpace: 
            if self.bscallback:
                self.bscallback()
                
        elif event.keyval == gtk.keysyms.plus or \
                        event.keyval == gtk.keysyms.equal: 
            if xsize < 100:
                bxx, byy = self.view.window_to_buffer_coords(gtk.TEXT_WINDOW_WIDGET, 0, 0)
                mm = self.view.get_iter_at_location(bxx, byy)
                xsize += 1
                self.buffer_1.get_tag_table().foreach(self.tag_iter)
                self.move = mm
                
        elif event.keyval == gtk.keysyms.minus or \
                event.keyval == gtk.keysyms.underscore: 
            if xsize > 7:
                bxx, byy = self.view.window_to_buffer_coords(gtk.TEXT_WINDOW_WIDGET, 0, 0)
                mm = self.view.get_iter_at_location(bxx, byy)
                xsize -= 1
                self.buffer_1.get_tag_table().foreach(self.tag_iter)
                self.move = mm
                
        elif event.keyval == gtk.keysyms._0:
                bxx, byy = self.view.window_to_buffer_coords(gtk.TEXT_WINDOW_WIDGET, 0, 0)
                mm = self.view.get_iter_at_location(bxx, byy)
                xsize = self.view.get_default_attributes().font.get_size() / pango.SCALE
                self.buffer_1.get_tag_table().foreach(self.tag_iter)
                self.move = mm
                
        elif event.keyval == gtk.keysyms.Home:
            #print "home", self.buffer_1.get_char_count()
            hh = self.buffer_1.get_start_iter()
            self.view.scroll_to_iter(hh, 0.0, True, 0, 0)
            self.view.place_cursor_onscreen()
            #self.view.move_visually(hh, 0)
            
        elif event.keyval == gtk.keysyms.End:
            #print "end"
            hh = self.buffer_1.get_end_iter()
            self.view.scroll_to_iter(hh, 0.0, True, 0, 0)
            self.view.place_cursor_onscreen()
            #self.view.move_visually(hh, 0)
            
        elif event.keyval == gtk.keysyms.F11: 
            if not self.full:
                self.window.fullscreen(); self.full = True
            else:
                self.window.unfullscreen(); self.full = False

        if event.keyval == gtk.keysyms.Escape or event.keyval == gtk.keysyms.q:
            sys.exit(0)
           
        if event.state & gtk.gdk.MOD1_MASK:       
            if event.keyval == gtk.keysyms.x or event.keyval == gtk.keysyms.X:
                sys.exit(0)            
        return False

    def tag_iter(self, xtag, user):
        global xsize
        #print "setting size", xsize
        if xsize == 0:
            xsize = self.view.get_default_attributes().font.get_size() / pango.SCALE
        xtag.set_property("size", xsize * pango.SCALE)
    
    def gohome(self):
        hh = self.buffer_1.get_start_iter()
        self.buffer_1.place_cursor(hh)
        #self.move = self.buffer_1.get_start_iter()
        #self.view.scroll_to_iter(hh, 0.0, True, 0, 0)
        #self.view.place_cursor_onscreen()
        
    # Links can also be activated by clicking.
    def event_after(self, text_view, event):
        if event.type != gtk.gdk.BUTTON_RELEASE:
            return False
        if event.button != 1:
            return False
        buffer = text_view.get_buffer()

        # We should not follow a link if the user has selected something
        try:
            start, end = buffer.get_selection_bounds()
        except ValueError:
            # If there is nothing selected, None is return
            pass
        else:
            if start.get_offset() != end.get_offset():
                return False

        x, y = text_view.window_to_buffer_coords(gtk.TEXT_WINDOW_WIDGET,
            int(event.x), int(event.y))
        iter = text_view.get_iter_at_location(x, y)

        self.follow_if_link(text_view, iter)
        return False

    def follow_if_link(self, text_view, iter):
        ''' Looks at all tags covering the position of iter in the text view,
            and if one of them is a link, follow it by showing the page identified
            by the data attached to it.
        '''
        tags = iter.get_tags()
        for tag in tags:
            page = tag.get_data("link")
            if page != None:
                #print "Calling link ", page
                # Paint a new cursor
                #self.waiting = True
                wx, wy, mod = text_view.window.get_pointer()
                bx, by = text_view.window_to_buffer_coords(gtk.TEXT_WINDOW_WIDGET, wx, wy)
                self.set_cursor_if_appropriate (text_view, bx, by)
                text_view.window.get_pointer()

                if self.callback:
                    if page.startswith("http:") or page.startswith("mailto:"):
                        pubutil.message("Cannot load external page: \n\n(" + page + ")", 
                            "ePub Message")
                        break
                    ret = self.callback(page)
                    if not ret:
                        pubutil.message("Cannot load page")
                        
                break

    def waitcursor(self, flag):
        #print "waitcursor", flag
        if flag:
            self.treeview.window.set_cursor(self.wait_cursor)            
            self.view.get_window(gtk.TEXT_WINDOW_TEXT).set_cursor(self.wait_cursor)
        else:
            self.treeview.window.set_cursor(None)
            self.view.get_window(gtk.TEXT_WINDOW_TEXT).set_cursor(None)

        self.treeview.window.get_pointer()
        self.view.get_window(gtk.TEXT_WINDOW_TEXT).get_pointer()

    # Looks at all tags covering the position (x, y) in the text view,
    # and if one of them is a link, change the cursor to the "hands" cursor
    # typically used by web browsers.

    def set_cursor_if_appropriate(self, text_view, x, y):

        hovering = False
        buffer = text_view.get_buffer()
        iter = text_view.get_iter_at_location(x, y)
        tags = iter.get_tags()
        for tag in tags:
            page = tag.get_data("link")
            #if page != 0:
            if page != None:
                self.prog.set_text("Link: " + page)
                #print "page", page
                hovering = True
                break
            else:
                self.prog.set_text(self.fname)

        if hovering != self.hovering_over_link:
            self.hovering_over_link = hovering

        if self.waiting:
            text_view.get_window(gtk.TEXT_WINDOW_TEXT).set_cursor(self.wait_cursor)
        elif self.hovering_over_link:
            text_view.get_window(gtk.TEXT_WINDOW_TEXT).set_cursor(self.hand_cursor)
        else:
            text_view.get_window(gtk.TEXT_WINDOW_TEXT).set_cursor(self.regular_cursor)

    # Update the cursor image if the pointer moved.

    def motion_notify_event(self, text_view, event):
        x, y = text_view.window_to_buffer_coords(gtk.TEXT_WINDOW_WIDGET,
            int(event.x), int(event.y))
        self.set_cursor_if_appropriate(text_view, x, y)
        text_view.window.get_pointer()
        return False

    # Also update the cursor image if the window becomes visible
    # (e.g. when a window covering it got iconified).
    
    def visibility_notify_event(self, text_view, event):
        wx, wy, mod = text_view.window.get_pointer()
        bx, by = text_view.window_to_buffer_coords(gtk.TEXT_WINDOW_WIDGET, wx, wy)

        self.set_cursor_if_appropriate (text_view, bx, by)
        return False

    def key_press_event2(self, text_view, event):
        if (event.keyval == gtk.keysyms.Return or
            event.keyval == gtk.keysyms.KP_Enter):
            buffer = text_view.get_buffer()
            iter = buffer.get_iter_at_mark(buffer.get_insert())
            self.follow_if_link(text_view, iter)
        elif event.keyval == gtk.keysyms.Tab: 
            #print "Tab"
            pass
        elif event.keyval == gtk.keysyms.space: 
            #print "Space"
            pass
        elif event.keyval == gtk.keysyms.BackSpace: 
            if self.bscallback:
                self.bscallback()
                
        if event.keyval == gtk.keysyms.Escape or event.keyval == gtk.keysyms.q:
            sys.exit(0)
           
        if event.state & gtk.gdk.MOD1_MASK:       
            if event.keyval == gtk.keysyms.x or event.keyval == gtk.keysyms.X:
                sys.exit(0)
            
            
        return False

    def event_after2(self, text_view, event):
        if event.type != gtk.gdk.BUTTON_RELEASE:
            return False
        if event.button != 1:
            return False
        buffer = text_view.get_buffer()

        # we should not follow a link if the user has selected something
        try:
            start, end = buffer.get_selection_bounds()
        except ValueError:
            # If there is nothing selected, None is return
            pass
        else:
            if start.get_offset() != end.get_offset():
                return False

        x, y = text_view.window_to_buffer_coords(gtk.TEXT_WINDOW_WIDGET,
            int(event.x), int(event.y))
        iter = text_view.get_iter_at_location(x, y)

        self.follow_if_link(text_view, iter)
        return False

    def visibility_notify_event2(self, text_view, event):
        wx, wy, mod = text_view.window.get_pointer()
        bx, by = text_view.window_to_buffer_coords\
            (gtk.TEXT_WINDOW_WIDGET, wx, wy)

        self.set_cursor_if_appropriate (text_view, bx, by)
        return False

    def motion_notify_event2(self, text_view, event):
        x, y = text_view.window_to_buffer_coords(gtk.TEXT_WINDOW_WIDGET,
            int(event.x), int(event.y))
        self.set_cursor_if_appropriate(text_view, x, y)
        text_view.window.get_pointer()
        return False
        
    def set_cursor_if_appropriate2(self, text_view, x, y):

        hovering = False
        buffer = text_view.get_buffer()
        iter = text_view.get_iter_at_location(x, y)
        tags = iter.get_tags()
        for tag in tags:
            page = tag.get_data("link")
            #if page != 0:
            if page != None:
                hovering = True
                break

        if hovering != self.hovering_over_link:
            self.hovering_over_link = hovering

        if self.waiting:
            text_view.get_window(gtk.TEXT_WINDOW_TEXT).set_cursor(self.wait_cursor)
        elif self.hovering_over_link:
            text_view.get_window(gtk.TEXT_WINDOW_TEXT).set_cursor(self.hand_cursor)
        else:
            text_view.get_window(gtk.TEXT_WINDOW_TEXT).set_cursor(self.regular_cursor)

def main():
    PangoView()
    gtk.main()

if __name__ == '__main__':
    main()








