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
    
        self.cnt = 1;       self.conf = config
        self.lastsel = "";  self.oldfind = ""
        self.full = False
        self.stopspeak = True
        self.olditer = None; self.move = None; self.mark = None
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
        view1.set_editable(False)

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
        view2.unset_flags(gtk.CAN_FOCUS)
        
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
        lab3 = gtk.Label("     ");    
        lab4 = gtk.Label("     ");    
        lab5 = gtk.Label(" ");
        
        #butt1 =      gtk.Button(" Show TOC File ");
        butt2 =       gtk.Button(" Pre_v ");
        butt3 =       gtk.Button(" N_ext ");
        butt2a =      gtk.Button(" PgUp ");
        butt3a =      gtk.Button(" PgDn ");
        self.butt4 =  gtk.Button(" _Read ");  self.butt4.connect("clicked", self.read_tts)
        butt5 =       gtk.Button(" _Home ");  butt5.connect("clicked", self.home)
        butt6 =       gtk.Button("  E_xit "); butt6.connect("clicked", self.exit)
        butt7 =       gtk.Button(" _Find ");  butt7.connect("clicked", self.find)
        
        hbox = gtk.HBox();
        #hbox.pack_start(butt1, False)
        hbox.pack_start(butt2, False)
        hbox.pack_start(butt3, False)
        
        hbox.pack_start(butt2a, False)
        hbox.pack_start(butt3a, False)
        
        hbox.pack_start(butt5, False)
        hbox.pack_start(butt7, False)
        hbox.pack_start(lab3, False)
        hbox.pack_start(self.butt4, False)
        hbox.pack_start(lab4, False)
        hbox.pack_start(butt6, False)
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
        
        if self.conf.fullscreen:
            #self.set_default_size(www, hhh)
            self.window.fullscreen(); self.full = True
            self.hpaned.set_position(0)
        
    
    def home(self, butt):
        self.gohome()
        
    def exit(self, butt):
        self.destroy()
        
    def OnExit(self, arg):
        #print "onexit"
        self.stopspeak = True
        if self.speech_pid:
            self.stop_tts()
            
        # Save configuration
        last = self.conf.sql.get_int("lastrun")
        last = int(last) + 1
        self.conf.sql.put("lastrun", last)
        
        #print "Saving lastfile:", self.conf.basefile, self.fname
        self.conf.sql.put(self.conf.basefile, self.fname)
        
        offs = 0; 
        iter2 = self.buffer_1.get_iter_at_mark(self.buffer_1.get_insert())
        try: offs = iter2.get_offset(); 
        except: pass
        
        comp = self.conf.basefile + "/" + self.fname
        #print "Saving last offset:", comp, offs
        self.conf.sql.put(comp, offs)      
        
    def find(self, arg):
        ret = pubutil.find(self)
        if not ret:
            return
        self.oldfind = ret[0]
        if self.olditer:
            iter3 =  self.olditer
        else:
            iter3 = self.buffer_1.get_iter_at_mark(self.buffer_1.get_insert())
        if not iter3:
            iter3 = self.buffer_1.get_start_iter()
        eiter = iter3.forward_search(ret[0], 0)
        if not eiter:
            self.prog.set_text(ret[0] + " Not Found")
            pubutil.message("Text " + "'" + ret[0] + "'" + " Not Found", "Search")
            self.olditer = None
            return
        self.view.scroll_to_iter(eiter[0], 0.3) #, True, 0, 0)
        self.view.place_cursor_onscreen()
        self.buffer_1.select_range(eiter[0], eiter[1])
        self.olditer = eiter[1]

    def tag_find_iter(self, xtag, data):
        print xtag
        print xtag.get_text(xtag)
    
    # Stop tts instances, kill (all) children
    def read_tts(self, butt):
        self.view.grab_focus()
        # Running?
        self.stopspeak = True
        if self.speech_pid:
            self.stop_tts()
            return      
        self.prog.set_text("Started Reading")
            
        cstr = ""
        iters = self.buffer_1.get_selection_bounds()
        if iters:
            cstr = self.buffer_1.get_text(iters[0], iters[1])
        if cstr:
            self.butt4.set_label("S_top") 
            gobject.timeout_add(100,  self.speak, cstr)
        else:
            self.stopspeak = False
            # Speak from current location, para by para
            iter = self.buffer_1.get_iter_at_mark(self.buffer_1.get_insert())
            if not iter:
                iter = self.buffer_1.get_start_iter()
            iterx = iter.copy()
            while True:
                # Adapt new position if changed
                iter3 = self.buffer_1.get_iter_at_mark(self.buffer_1.get_insert())
                #if iterx.get_offset() != iter3.get_offset():
                #    iterx = iter3.copy
                #    iter  = iter3.copy()
                iter2 = iter.copy  
                eiter = iter.forward_search("\n", 0)
                if eiter:
                    iter2 = eiter[1]
                else:
                    iter2 = iter.copy(); iter2.forward_sentence_end() 
                    
                self.view.scroll_to_iter(iter, 0.2) #, True, 0, 0)
                self.view.place_cursor_onscreen()
                self.buffer_1.select_range(iter, iter2)
                cstr = self.buffer_1.get_text(iter, iter2)
                if self.stopspeak:
                    break
                if cstr != "\n":
                    self.butt4.set_label("S_top") 
                    # Speak and wait for it to finish
                    self.speak(cstr)
                    while True:
                        if not self.speech_pid:
                            break
                        pubutil.usleep(100)
                iter = iter2
                # End of buffer?
                if iter2.get_offset() >= \
                    self.buffer_1.get_end_iter().get_offset():
                    self.gohome()          
                    break
                if self.stopspeak:
                    break
                
    def stop_tts2(self, ss, opt):
        if ss[1] == "(audsp)":
            #print "killing", ss
            os.kill(int(ss[0]), signal.SIGKILL)
        
    def stop_tts(self):
        self.stopspeak = True
        self.prog.set_text("Stopped Reading")
        try:
           pubutil.withps(self.stop_tts2)
        except:
            pubutil.print_exception("Cannot kill")
            #self.speech_pid.pid
        self.speech_pid = None
        self.butt4.set_label("_Read") 
        return

    def invalidate(self):
        rc = self.view.get_allocation()
        self.view.queue_draw_area(0, 0, rc.width, rc.height)
    
    def tree_sel_row(self, xtree):
        self.stop_tts()
        sel = xtree.get_selection()
        xmodel, xiter = sel.get_selected()
        xstr = xmodel.get_value(xiter, 0)
        self.sel_item(xstr)
        
    def sel_item(self, xstr):
        self.lastsel = xstr
        #print "sel_item", xstr
        cnt = 0
        try:
            for aa in self.stags:
                if aa == xstr:
                    #print "got", aa, self.xtags[cnt]
                    mm = self.buffer_1.get_mark(self.xtags[cnt])
                    if mm:
                        self.view.scroll_to_mark(mm, 0.0, True, 0, 0)
                    else:
                        # This is a link
                        #print "link", self.xtags[cnt]
                        self.callback(self.xtags[cnt])
                        #self.view.set_focus()
                        #self.set_focus(self.view)
                        self.view.grab_focus()
                        #self.gohome()
                    break;
                cnt += 1
        except: pass
            
    def tree_sel(self, xtree, xiter, xpath):
        pass
        #print "tree_sel", xtree, xiter, xpath

    # Create a file, send it to festival
    def speak(self, cstr):
        fname = self.conf.data_dir + "/festival.txt"
        try:
            fh = open(fname, "w")
            fh.write(cstr)
        except:
            pubutil.print_exception("Cannot create festival file")
            return
        self.speech_pid = subprocess.Popen(["festival", "--tts", fname])
        #print "started", self.speech_pid.pid
        gobject.timeout_add(100, self.check_speak)

    def check_speak2(self, ss, opt):
        if self.speech_pid:
            if  self.speech_pid.pid == int(ss[0]):
                # Zombie does not count:
                if ss[2] != "Z":
                    return True
                
    # Timer to see if the speaker has terminated
    def check_speak(self):
        # If found, the search returns True
        ret = pubutil.withps(self.check_speak2)
        if not ret:
            self.butt4.set_label("_Read")             
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
        #print "'" + name + "'", mmm, cc.get_offset
        
    # --------------------------------------------------------------------
    def key_press_event3(self, text_view, event):
        #print "event3", event.keyval
        
        if event.keyval == gtk.keysyms.F11: 
            if not self.full:
                self.window.fullscreen(); self.full = True
                self.hpaned.set_position(0)
            else:
                self.window.unfullscreen(); self.full = False
                self.hpaned.set_position(200)
                
        elif event.keyval == gtk.keysyms.F12:
            self.view.get_window(gtk.TEXT_WINDOW_WIDGET).focus() 
            pass

        #if event.keyval == gtk.keysyms.Escape or 
        if event.keyval == gtk.keysyms.q:
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
            hh = self.buffer_1.get_start_iter()
            self.view.scroll_to_iter(hh, 0.0, True, 0, 0)
            self.view.place_cursor_onscreen()
            
        elif event.keyval == gtk.keysyms.End:
            hh = self.buffer_1.get_end_iter()
            self.view.scroll_to_iter(hh, 0.0, True, 0, 0)
            self.view.place_cursor_onscreen()

        elif event.keyval == gtk.keysyms.F10: 
            if self.hpaned.get_position() < 10:
                self.hpaned.set_position(200)
            else:
                self.hpaned.set_position(0)
                  
        elif event.keyval == gtk.keysyms.F11: 
            if not self.full:
                self.window.fullscreen(); 
                self.hpaned.set_position(0)
                self.full = True
            else:
                self.window.unfullscreen(); 
                self.hpaned.set_position(200)
                self.full = False
                
        if event.keyval == gtk.keysyms.Escape:
            if self.full:
                self.window.unfullscreen(); self.full = False
                self.hpaned.set_position(200)
            if self.speech_pid:
                self.stop_tts()
                
        if event.keyval == gtk.keysyms.f and \
                event.state == gtk.gdk.CONTROL_MASK:
            self.find(None)
            
        if event.keyval == gtk.keysyms.q:
            sys.exit(0)
           
        if event.state & gtk.gdk.MOD1_MASK:       
            if event.keyval == gtk.keysyms.x or event.keyval == gtk.keysyms.X:
                sys.exit(0)            
        return False

    # Set all tags to new size, correct for headers
    def tag_iter(self, xtag, user):
        global xsize
        defsize = self.view.get_default_attributes().font.get_size() / pango.SCALE
        if xsize < 5:
            xsize = defsize
        newsize = xsize * pango.SCALE
        hh = xtag.get_data("header")
        if hh:
            dd = float(hh) / defsize
            newsize = (dd * xsize) * pango.SCALE
        xtag.set_property("size", newsize)
    
    def gohome(self):
        hh = self.buffer_1.get_start_iter()
        self.buffer_1.place_cursor(hh)
        self.view.scroll_to_iter(hh, 0.0, True, 0, 0)
        self.view.place_cursor_onscreen()
        
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
                        pubutil.message("Cannot load page: '" + page + "'")
                        
                break

    def waitcursor(self, flag):
        #print "waitcursor", flag
        if flag:
            self.waiting = True
            self.treeview.window.set_cursor(self.wait_cursor)            
            self.view.get_window(gtk.TEXT_WINDOW_TEXT).set_cursor(self.wait_cursor)
        else:
            self.treeview.window.set_cursor(None)
            self.view.get_window(gtk.TEXT_WINDOW_TEXT).set_cursor(None)
            self.waiting = False
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
                self.prog.set_text("Link: " + page[-18:])
                #print "page", page
                hovering = True
                break
            else:
                self.prog.set_text(self.fname[-18:])

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
                
        #if event.keyval == gtk.keysyms.Escape or 
        if event.keyval == gtk.keysyms.q:
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























