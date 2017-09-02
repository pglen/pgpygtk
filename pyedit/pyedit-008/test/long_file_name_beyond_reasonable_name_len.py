#!/usr/bin/env python

# Saving again

import signal, os, time, gobject, gtk, string, pango
from threading import Timer

import keyhand, pedconfig
from pedmenu import *
from pedutil import *

SCROLLGAP = 2           # Gap between the page boundary and scroll
PAGEUP = 20             # One page worth of scroll

# Do not redefine this here, as it is determined by the gtk (pango) lib
TABSTOP = 8             # One tabstop worth of spaces

# Profile line, use it on bottlenecks
#got_clock = time.clock()   
# profiled code here
#print  "Str", time.clock() - got_clock        

last_scanned = None

# Add keywords to your taste
# Keywords for coloring
keywords =  "def ", "import ", "from ", "for ", "while ", "len(", "return ", \
            "range(", "if ", "elif ", "not ", "abs(", "any(", "all(", "min(", "max(",  \
            "map(", "print ", "open("

clwords =  "class ", "self."

# Keywords for summary extraction: (left side window)
sumkeywords = "class ", "def ", "TODO"

# Colors for the text, configure it here

FGCOLOR  = "#000000"
RBGCOLOR = "#bbbbff"              
CBGCOLOR = "#ffbbbb"
KWCOLOR  = "#88aaff"
CLCOLOR  = "#44aa44"
COCOLOR  = "#4444ff"
STCOLOR  = "#ee44ee"
    
class pedDoc(gtk.DrawingArea):

    #notebook = None

    def __init__(self, buff, appwin, focus = False, readonly = False):
        
        # Save params
        self.appwin = appwin; 

        #if focus: 
        #    self.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE | gtk.CAN_DEFAULT)

        self.readonly = readonly      
        
        # Gather globals
        self.keyh = pedconfig.pedconfig.keyh

        # Init vars
        self.xpos = 0; self.ypos = 0
        self.changed = False; self.changed2 = False; 
        self.needscan = True; 
        self.colsel = False
        self.oldsearch = ""
        self.xsel = -1; self.ysel = -1
        self.xsel2 = -1; self.ysel2 = -1
        self.caret = []; self.caret.append(0); self.caret.append(0)        
        self.focus = False
        
        # Init configurables
        self.scgap = SCROLLGAP      
        self.pgup  = PAGEUP
        self.tabstop = TABSTOP

        # Process buffer into list
        self.text = buff
        self.maxlinelen = 0
        for aa in self.text:       
            xlen = len(aa)  
            if self.maxlinelen < xlen:
                self.maxlinelen = xlen
        #print "self.maxlinelen", self.maxlinelen

        # Parent widget                 
        gtk.DrawingArea.__init__(self)
        self.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
        self.pangolayout = self.create_pango_layout("a")
    
        # Our font
        fd = pango.FontDescription()
        fd.set_size(14*1024); fd.set_family("mono")
        self.pangolayout.set_font_description(fd)

        # Get Pango steps
        self.cxx, self.cyy = self.pangolayout.get_pixel_size()
        ts = self.pangolayout.get_tabs()
        if ts == None: self.tabstop = TABSTOP    
        else: al, self.tabstop = ts.get_tab(0)

        #print "tabstop", self.tabstop
        # Set up scroll bars        
        sm = len(self.text) + self.get_height() / self.cyy + 10
        self.hadj = gtk.Adjustment(0, 0, self.maxlinelen, 1, 15, 25);
        self.vadj = gtk.Adjustment(0, 0, sm, 1, 15, 25);
        
        self.vscroll = gtk.VScrollbar(self.vadj)
        self.hscroll = gtk.HScrollbar(self.hadj)
        
        # We connect scrollers after construction
        self.hadj.connect("value-changed", self.hscroll_cb)
        self.vadj.connect("value-changed", self.vscroll_cb)

        self.set_events(    gtk.gdk.POINTER_MOTION_MASK |
                            gtk.gdk.POINTER_MOTION_HINT_MASK |
                            gtk.gdk.BUTTON_PRESS_MASK |
                            gtk.gdk.BUTTON_RELEASE_MASK |
                            gtk.gdk.KEY_PRESS_MASK |
                            gtk.gdk.KEY_RELEASE_MASK )
    
        self.set_events(    gtk.gdk.ALL_EVENTS_MASK )

        self.colormap = gtk.widget_get_default_colormap()

        # Set default background color
        if self.readonly:
            color = self.colormap.alloc_color("#d8d8d8")
            self.modify_bg(gtk.STATE_NORMAL, color)
        
        # Customize your colors here
        
        self.fgcolor  = self.colormap.alloc_color(FGCOLOR)              
        self.rbgcolor = self.colormap.alloc_color(RBGCOLOR)              
        self.cbgcolor = self.colormap.alloc_color(CBGCOLOR)              
        self.kwcolor  = self.colormap.alloc_color(KWCOLOR)
        self.clcolor  = self.colormap.alloc_color(CLCOLOR)
        self.cocolor  = self.colormap.alloc_color(COCOLOR)
        self.stcolor  = self.colormap.alloc_color(STCOLOR)

        self.connect("expose-event", self.area_expose_cb)
        self.connect("motion-notify-event", self.area_motion)
        self.connect("button-press-event", self.area_button)
        self.connect("button-release-event", self.area_button)
        self.connect("key-press-event", self.area_key)
        self.connect("key-release-event", self.area_key)
        self.connect("focus", self.area_focus)
        self.connect("configure_event", self.configure_event)
        self.connect("size-request", self.size_request)
        self.connect("size-allocate", self.size_alloc)    
        self.connect("scroll-event", self.scroll_event)    
        #self.connect("enter-notify-event", self.area_enter)
        #self.connect("leave-notify-event", self.area_leave)
        self.connect("focus-in-event", self.focus_in_cb)    
        self.connect("focus-out-event", self.focus_out_cb)    

    def locate(self, xstr):
        #print "locate '" + xstr +"'"        
        cnt = 0
        for line in self.text:
            if line.find(xstr) >= 0:
                off = (self.get_height() / self.cyy) / 4
                self.ypos = cnt - off
                self.ysel = self.ypos + off; self.ysel2 = self.ypos + off
                self.xsel = 0; self.xsel2 = len(self.text[self.ysel])
                self.set_caret(self.caret[0], self.caret[1])
                self.invalidate()
                break
            cnt += 1
        
    def focus_out_cb(self, widget, event):
        self.focus = False
        self.currented = None
        #print "focus_out_cb", widget, event
    
    def focus_in_cb(self, widget, event):
        self.focus = True
        self.currented = self
        
        # Is this the doc in scanned pane?
        global last_scanned

        if last_scanned != self:
            self.needscan = True

        self.do_chores()
        #print "focus_in_cb"
    
    def grab_focus_cb(self, widget):
        print "grab_focus_cb", widget
        pass
        
    def area_enter(self, widget, event):
        print "area_enter"
        
    def area_leave(self, widget, event):
        print "area_leave"

    def scroll_event(self, widget, event):
        if event.direction == gtk.gdk.SCROLL_UP:
            self.ypos -= self.pgup / 2
        else:
            self.ypos += self.pgup / 2
        
        # Contain, show
        self.ypos = max(0, self.ypos)
        self.ypos = min(len(self.text), self.ypos)        
        self.set_caret(self.caret[0], self.caret[1])
        self.invalidate()
        
    def hscroll_cb(self, widget):
        #print "hscroll", widget.get_value()
        self.xpos = int(widget.get_value())
        self.invalidate()

    def vscroll_cb(self, widget):
        #print "vscroll", widget.get_value()
        self.ypos = int(widget.get_value())
        self.invalidate()

    def size_request(self, widget, req):
        #print "size_request", req
        pass

    def size_alloc(self, widget, req):
        #print "size_alloc", req
        pass

    def configure_event(self, widget, event):
        #print "configure_event", event
        #self.grab_focus()
        #self.width = 0; self.height = 0
        #self.invalidate()
        #print self, event
        pass
        
    def _draw_text(self, gc, x, y, text, foreground = None, background = None):
        #print "draw_text"
        self.pangolayout.set_text(text)
        xx, yy = self.pangolayout.get_pixel_size()
        self.window.draw_layout(gc, x, y, self.pangolayout, foreground, background)
        return xx, yy

	# Calculate tabs up to till count
    def calc_tabs(self, strx, till):
        idx = 0; cnt = 0
        xlen = min(len(strx), till); 
        while True:
            if idx >= xlen: break
            chh = strx[idx]
            if  chh == "\t":
                cnt += self.tabstop - (cnt % self.tabstop)
            else:
                cnt += 1
            idx += 1
        return cnt

    def area_expose_cb(self, area, event):

        #print "area_expose_cb()", event.area.width, event.area.height
        
        self.do_chores()

        hhh = self.get_height()
        xlen = len(self.text)

        style = self.get_style()
        self.gc = style.fg_gc[gtk.STATE_NORMAL]
        gcx = gtk.gdk.GC(self.window); gcx.copy(self.gc)

        #got_clock = time.clock()   
            
        # Paint text        
        xx = 0; yy = 0; 
        cnt = self.ypos;
        while cnt <  xlen:
            #dx, dy = self._draw_text(self.gc, xx, yy, self.text[cnt])
            dx, dy = self._draw_text(gcx, xx, yy, self.text[cnt], self.fgcolor)
            cnt = cnt + 1
            yy += dy
            if yy > hhh:
                break

        # Paint selection        
        xx = 0; yy = 0; 
        cnt = self.ypos;
    
        # Normalize 
        xssel = min(self.xsel, self.xsel2)
        xesel = max(self.xsel, self.xsel2)
        yssel = min(self.ysel, self.ysel2)
        yesel = max(self.ysel, self.ysel2)
        draw_start = xssel

        if xssel != -1:
            if self.colsel: bgcol = self.cbgcolor
            else: bgcol = self.rbgcolor
            
            while cnt <  xlen:
                if cnt >= yssel and cnt <= yesel:
                    line = self.text[cnt]
                    if self.colsel:
                        frag = line[xssel:xesel]
                    else :   # Startsel - endsel                        
                        if cnt == yssel and cnt == yesel:   # sel on the same line
                            frag = line[xssel:xesel]
                        elif cnt == yssel:                  # start line
                            frag = line[xssel:]
                        elif cnt == yesel:                  # end line
                            draw_start = 0
                            frag = line[:xesel]
                        else:
                            draw_start = 0                  # intermediate line
                            frag = line[:]

                    self._draw_text(gcx, draw_start * self.cxx, yy, frag,
                             self.fgcolor, bgcol)
                cnt = cnt + 1
                yy += self.cyy
                if yy > hhh:
                    break

        #print  "sel", time.clock() - got_clock        
        
        # Color keywords. Very primitive coloring, a compromize for speed
        xx = 0; yy = 0; 
        cnt = self.ypos;
        while cnt <  xlen:
            line = self.text[cnt]
            for kw in keywords:
                ff = 0          # SOL
                while True:
                    ff = line.find(kw, ff)
                    if ff >= 0:
                        ff2 = self.calc_tabs(line, ff)                    
                        self._draw_text(gcx, ff2 * self.cxx, yy, line[ff:ff+len(kw)],
                            self.kwcolor, None)
                        ff += len(kw)
                        #break
                    else:        
                        break
                    
            for kw in clwords:
                cc = 0      # SOL
                while True:
                    cc = line.find(kw, cc)
                    if cc >= 0:
                        cc2 = self.calc_tabs(line, cc)                    
                        self._draw_text(gcx, cc2 * self.cxx, yy, line[cc:cc+len(kw)],
                            self.clcolor, None)
                        cc += len(kw)
                        #break
                    else:        
                        break
                    
            # Comments      
            ccc = line.find("#"); cccc = line.find('"')

            # See if hash preceeds quote (if any)
            if ccc >= 0 and (cccc > ccc or cccc == -1):
                ccc2 = self.calc_tabs(line, ccc)                    
                self._draw_text(gcx, ccc2 * self.cxx, yy, line[ccc:],
                        self.cocolor, None)
            else:   
                qqq = 0                                 
                while True:
                    qqq = line.find('"', qqq); 
                    if qqq >= 0:
                        qqq += 1
                        qqqq = line.find('"', qqq)
                        if qqqq >= 0:
                            qqq2 = self.calc_tabs(line, qqq)                    
                            self._draw_text(gcx, qqq2 * self.cxx, yy, line[qqq:qqqq],
                            self.stcolor, None)
                            qqq = qqqq + 1
                        else:
                            break
                    else:
                        break

            cnt = cnt + 1
            yy += self.cyy
            if yy > hhh:
                break

        #print  "kw", time.clock() - got_clock        
        
        self._drawcaret()        
        return True

    # --------------------------------------------------------------------
    # Draw caret

    def _drawcaret(self):

        #print "drawing caret", self.caret[0], self.caret[1], \
        #        self.caret[0] * self.cxx, self.caret[1] * self. cyy  
                
        
        colormap = gtk.widget_get_default_colormap()
        if self.focus:    
            color = colormap.alloc_color("#008888")
        else:
            color = colormap.alloc_color("#aaaaaa")
        
        gcx = gtk.gdk.GC(self.window); gcx.copy(self.gc)
        gcx.set_foreground(color)
      
        xx = self.caret[0] * self.cxx #+ self.cxx / 2
        yy = self.caret[1] * self.cyy
        cw = self.cxx / 2

        # The actual caret. Change drawing instructions for a different caret.
        # Order: Top, left right, buttom
        if self.focus:    
            self.window.draw_line(gcx, xx, yy, xx + cw, yy)
        self.window.draw_line(gcx, xx + 1, yy, xx + 1, yy + self.cyy )
        self.window.draw_line(gcx, xx + 3, yy, xx + 3, yy + self.cyy )
        if self.focus:    
            self.window.draw_line(gcx, xx , yy + self.cyy, xx + cw, yy + self.cyy )

    def area_motion(self, area, event):
        #print "motion event", event
        pass

    def goto(self, xx, yy, sel = None):

        # Contain
        ylen = len(self.text)
        xx = max(xx, 0);  yy = max(yy, 0)
        xx = min(xx, self.maxlinelen);  yy = min(yy, ylen)
        if sel:
            self.xsel = xx; self.xsel2 = xx + sel
            self.ysel = yy; self.ysel2 = yy
            self.invalidate()

        self.set_caret(xx - self.xpos, yy - self.ypos)

    # --------------------------------------------------------------------
    def set_caret(self, xx, yy):

        # Needs scroll?
        xxx, yyy = self.get_size()        
        need_inval = False        
        xlen = len(self.text)

         # Put it back in view:                    
        hhh = yyy - self.scgap * self.cyy
        if  yy * self.cyy  > hhh:
            #print "Scroll from caret down"
            self.ypos += yy - (yyy / self.cyy - self.scgap) 
            yy = yyy / self.cyy - self.scgap 
            need_inval = True
       
        colormap = gtk.widget_get_default_colormap()
        color = colormap.alloc_color("#008888")
        
        gcx = gtk.gdk.GC(self.window); gcx.copy(self.gc)
        gcx.set_foreground(color)
           
        if yy < self.scgap and self.ypos > 0:
            #print "Scroll from caret up"
            #self.ypos = yy - yyy / self.cyy
            self.ypos += yy - self.scgap            
            yy = self.scgap
            need_inval = True
            
        if self.ypos >  xlen - self.scgap:
               self.ypos = xlen - self.scgap            

        if self.ypos < 0:
            self.ypos = 0
            
        oldx = self.caret[0] * self.cxx; 
        oldy = self.caret[1] * self.cyy

        self.caret[0] = xx; self.caret[1] = yy

        # Low limit
        if self.caret[0] < 0: self.caret[0] = 0
        if self.caret[1] < 0: self.caret[1] = 0

        # High Limit
        xxxx = xxx / self.cxx; yyyy = yyy / self.cyy
        if self.caret[0] > xxxx: self.caret[0] = xxxx       
        if self.caret[1] > yyyy: self.caret[1] = yyyy       
               
        wxx = self.caret[0] * self.cxx
        wyy = self.caret[1] * self.cyy

        # Optimize cursor movement invalidation
        rect = gtk.gdk.Rectangle(wxx, wyy, self.cxx * self.cxx /2, self.cyy + 1)
        self.invalidate(rect)

        rect = gtk.gdk.Rectangle(oldx, oldy, self.cxx + self.cxx /2 , self.cyy + 1)
        self.invalidate(rect)

        # Update scroll bars:
        self.vscroll.set_value(self.ypos)        
        #self.hscroll = 
        
        self.mained.update_statusbar2(self.caret[0] + self.xpos, self.caret[1] + self.ypos)
               
        if  need_inval:
            self.invalidate()            

        if  self.changed and not self.changed2:
            self.changed2 = True
            print "Setting changed on ", self.fname
            vcurr = self.notebook.get_nth_page(self.notebook.get_current_page())
            ss = shortenstr(os.path.basename(self.fname), 24)
            label = gtk.Label(" " + ss + " *")
            self.notebook.set_tab_label(vcurr, label)
                
    def clearsel(self):
        old = self.xsel
        self.xsel = -1;   self.ysel = -1
        self.xsel2 = -1;  self.ysel2 = -1
        if old != -1:
            self.invalidate()

    def area_button(self, area, event):
        if  event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
            ttt = "Press right mouse"
            #print "Right Click at x=", event.x, "y=", event.y
            self.poprclick(area, event)                       
        elif  event.type == gtk.gdk.BUTTON_PRESS and event.button == 1:
            ttt = "Press left mouse"
            print "Left Click at x=", event.x, "y=", event.y
            # Find current line    
            self.set_caret(int(event.x) / self.cxx, 
                                 int(event.y) / self.cyy )                                
        else:
            ttt = "Release"

        #print "button event ", "type = ", ttt, "x= ", event.x, \
        #    "y= ", event.y, "button = ", event.button                
        self.grab_focus()
        return True

    # Call key handler
    def area_key(self, area, event):
        self.keyh.handle_key(self, area, event)
        return True

     # Invalidate current line
    def inval_line(self):
        rect = gtk.gdk.Rectangle(0, self.caret[1] * self.cyy, 
                self.get_width(), self.cyy)
        self.invalidate(rect)
   
    def invalidate(self, rect = None):                        
        if rect == None:
            ww, hh = self.window.get_size()
            rect = gtk.gdk.Rectangle(0,0, ww, hh)
        #print "Invalidate:", rect
        self.window.invalidate_rect(rect, False)

    def area_focus(self, area, event):
        #print "peddoc area focus", event
        return False

    def poprclick(self, widget, event):
        #print "Making rclick"
        mm = self.build_menu(self.window, rclick_menu)
        mm.popup(None, None, None, event.button, event.time)

        # Create a new menu-item with a name...
        #menu = gtk.Menu()
        #menu.append(self.create_menuitem("Menu 1", self.menuitem_response1))
        #menu.append(self.create_menuitem("Menu 2", self.menuitem_response2))
        #menu.append(self.create_menuitem("Menu 3", self.menuitem_response3))
        #menu.popup(None, None, None, event.button, event.time)

    def menuitem_response1(self, widget, string):
        self.draw_segments(10, 200)
        print "response1 %s" % string

    def menuitem_response2(self, widget, string):
        print "response2 %s" % string

    def menuitem_response3(self, widget, string):
        print "response3 %s" % string

    def activate_action(self, action):
        dialog = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE,
            'You activated action: "%s" of type "%s"' % (action.get_name(), type(action)))
        # Close dialog on user response
        dialog.connect ("response", lambda d, r: d.destroy())
        dialog.show()

    def create_menuitem(self, string, action):
        rclick_menu = gtk.MenuItem(string)
        rclick_menu.connect("activate", action, string);
        rclick_menu.show()        
        return rclick_menu
   
        # Create the menubar and toolbar
        action_group = gtk.ActionGroup("DocWindowActions")
        action_group.add_actions(entries)      
        return action_group

    def build_menu(self, window, items):
        accel_group = gtk.AccelGroup()
        item_factory = gtk.ItemFactory(gtk.Menu, "<pydoc>", accel_group)
        item_factory.create_items(items)
        self.item_factory = item_factory
        return item_factory.get_widget("<pydoc>")

    def get_size(self):
        rect = self.get_allocation()
        return rect.width, rect.height

    def get_height(self):
        rect = self.get_allocation()
        return rect.height

    def get_width(self):
        rect = self.get_allocation()
        return rect.width

    def prompt_save(self):
        dialog = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT,
        gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
        "\nWould you like to save:\n\n  \"%s\" \n" % self.fname)
        dialog.set_title("Save file ?")
        dialog.set_default_response(gtk.RESPONSE_YES)

        # Close dialog on user response
        dialog.connect("response", self.done_dlg)
        dialog.run()            

    def done_dlg(self, win, resp):
        #print "done_dlg", win, resp
        if resp == gtk.RESPONSE_YES:
            print "saving ..."
            but =   "Cancel", gtk.BUTTONS_CANCEL, "Save File", gtk.BUTTONS_OK
            fc = gtk.FileChooserDialog("Save file", win, gtk.FILE_CHOOSER_ACTION_SAVE, \
                but)
            fc.set_default_response(gtk.BUTTONS_OK)
            fc.connect("response", self.done_fc)                
            fc.set_current_name(self.fname)
            fc.run()    
            pass

    def done_fc(self, win, resp):
        print "done_fc", win, resp
        if resp == gtk.BUTTONS_OK:
            fname = win.get_filename()
            if not fname:
                print "must have filename"
            else:                
                print "saving '"+ self.fname + "'"
                writefile(fname, self.text)

    def do_chores(self):
        if  not self.needscan:
            return
            
        global last_scanned
        last_scanned = self    
        self.needscan = False        

        self.appwin.start_tree()    
        arg = self,
        Timer(1, run_async_time, arg).start()

# Run this on a timer so the user can work while this is going

def run_async_time(win):

    #print "From async_time", win, time.time()    
    sumw = []
    if win.text:
        try:
            for kw in sumkeywords:
                for line in win.text:
                    if line.find(kw) >= 0:
                        sumw.append(line)
        except:
            pass
        
    win.appwin.update_treestore(sumw)










