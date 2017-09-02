#!/usr/bin/env python

# Action Handler for find

import re, string, gtk
import peddoc
from pedutil import *


def find(self, self2):

    self.treestore = None

    dialog = gtk.Dialog("pyedit: Find in text",
                   None,
                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                   (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                    gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
    dialog.set_default_response(gtk.RESPONSE_ACCEPT)

    # Spacers
    label1 = gtk.Label("   ");  label2 = gtk.Label("   ") 
    label3 = gtk.Label("   ");  label4 = gtk.Label("   ") 
    label5 = gtk.Label("   ");  label6 = gtk.Label("   ") 
    label7 = gtk.Label("   ");  label8 = gtk.Label("   ") 

    entry = gtk.Entry(); entry.set_activates_default(True)
    entry.set_text(self2.oldsearch)
    dialog.vbox.pack_start(label4)  

    hbox2 = gtk.HBox()
    hbox2.pack_start(label6, False)  
    hbox2.pack_start(entry)  
    hbox2.pack_start(label7, False)  

    dialog.vbox.pack_start(hbox2)

    checkbox = gtk.CheckButton("Use _regular expressions")
    checkbox2 = gtk.CheckButton("Case In_sensitive")
    dialog.vbox.pack_start(label5)  

    hbox = gtk.HBox()
    hbox.pack_start(label1);  hbox.pack_start(checkbox)
    hbox.pack_start(label2);  hbox.pack_start(checkbox2)
    hbox.pack_start(label3);  
    dialog.vbox.pack_start(hbox)
    dialog.vbox.pack_start(label8)  

    #label1.show(); label2.show();  label3.show(); 
    #hbox.show(); checkbox.show(); checkbox2.show(); entry.show()
    dialog.show_all()
    response = dialog.run()   
    self2.oldsearch = entry.get_text()
    self.srctxt = entry.get_text()     
    dialog.destroy()

    if response == gtk.RESPONSE_ACCEPT:
        #print "search", "'" + self.srctxt + "'"
        #print "checkbox", checkbox.get_active()
        #print "checkbox2", checkbox2.get_active()

        if self.srctxt == "":
            self2.mained.update_statusbar("Must specify search string")
            return          

        self.peddoc = self2
        win2 = gtk.Window()
        win2.set_position(gtk.WIN_POS_CENTER)
        
        win2.set_events(    
                        gtk.gdk.POINTER_MOTION_MASK |
                        gtk.gdk.POINTER_MOTION_HINT_MASK |
                        gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.KEY_PRESS_MASK |
                        gtk.gdk.KEY_RELEASE_MASK |
                        gtk.gdk.FOCUS_CHANGE_MASK )

        win2.connect("key-press-event", area_key, self)
        win2.connect("key-release-event", area_key, self)

        # Position it out of the way
        sxx, syy = self2.mained.window.get_position()
        wxx, wyy = self2.mained.window.get_size()
        #print sxx, syy, wxx, wyy

        myww = 2 * wxx / 4; myhh = 2 * wyy / 4
        win2.set_default_size(myww, myhh)
        win2.move(sxx + wxx - myww - 25, syy + 25)        

        vbox = gtk.VBox()
        self.tree = create_tree(self, self.srctxt)
        self.tree.connect("row-activated",  tree_sel, self)
        self.tree.connect("cursor-changed",  tree_sel_row, self)
    
        stree = gtk.ScrolledWindow()
        stree.add(self.tree)
        vbox.pack_start(stree)                                        
        win2.add(vbox)
        win2.show_all()
        
        accum = []; cnt = 0; cnt2 = 0; was = -1
        curr = self2.caret[1] + self2.ypos

        if checkbox.get_active():
            regex = re.compile(self.srctxt)

        for line in self2.text:
            if checkbox2.get_active():
                #print "case search"
                idx = line.lower().find(self.srctxt.lower())
            elif checkbox.get_active():
                res = regex.search(line)
                if res:
                    idx = res.start()
                else:
                    cnt += 1;           # Cont would skip this
                    continue
            else:
                idx = line.find(self.srctxt)

            if  idx >= 0:
                if cnt > curr and was == -1:
                    #accum.append("curr"); 
                    was = cnt2
                line2 =  str(idx) + ":"  + str(cnt) + " " + line
                cnt2 += 1
                accum.append(line2)
            cnt += 1; 
            
        update_treestore(self, accum, was)                    

        #aa, bb, cc, dd = tree.get_path_at_pos(0, 0)
        #tree.set_cursor(aa)
        #print tree.get_cursor()
        self.tree.grab_focus()
        
# --------------------------------------------------------------------
def tree_sel_row(xtree, self):
    sel = xtree.get_selection()
    xmodel, xiter = sel.get_selected()
    xstr = xmodel.get_value(xiter, 0)    
    # Get back numbers
    xxx = xstr[:xstr.find(":")]
    yyy = xstr[xstr.find(":")+1:xstr.find(" ")]
    #print int(xxx), int(yyy)
    try:
        self.peddoc.goto(int(xxx), int(yyy), len(self.srctxt))
    except:
        pass
    
def tree_sel(xtree, xiter, xpath, self):
    pass
    #print "tree_sel", xtree, xiter, xpath     

# Call key handler
def area_key(area, event, self):

    #print "area_key", event
    # Do key down:
    if  event.type == gtk.gdk.KEY_PRESS:
        if event.keyval == gtk.keysyms.Escape:
            print "Esc"
            area.destroy()

    if  event.type == gtk.gdk.KEY_PRESS:
        if event.keyval == gtk.keysyms.Return:
            print "Ret"
            area.destroy()

        if event.keyval == gtk.keysyms.Alt_L or \
                event.keyval == gtk.keysyms.Alt_R:
            self.alt = True;
    
        if event.keyval >= gtk.keysyms._1 and \
                event.keyval <= gtk.keysyms._9:
            print "pedwin Alt num", event.keyval - gtk.keysyms._1
        
        if event.keyval == gtk.keysyms.x or \
                event.keyval == gtk.keysyms.X:
            if self.alt:
                area.destroy()
                                  
    elif  event.type == gtk.gdk.KEY_RELEASE:
        if event.keyval == gtk.keysyms.Alt_L or \
              event.keyval == gtk.keysyms.Alt_R:
            self.alt = False;

# Tree handlers
def start_tree(self):

    if not self.treestore:
        self.treestore = gtk.TreeStore(str)
    
    # Delete previous contents
    try:      
        while True:
            root = self.treestore.get_iter_first() 
            self.treestore.remove(root)                           
    except:
        #print  sys.exc_info()
        pass
    
    piter = self.treestore.append(None, ["Searching .."])
    self.treestore.append(piter, ["None .."])
    
# --------------------------------------------------------------------
def create_tree(self,  match, text = None):
    
    start_tree(self)
    
    # create the TreeView using treestore
    tv = gtk.TreeView(self.treestore)
    tv.set_enable_search(False)

    # create a CellRendererText to render the data
    cell = gtk.CellRendererText()

    # create the TreeViewColumn to display the data
    tvcolumn = gtk.TreeViewColumn("Matches for '" + match + "'")

    # add the cell to the tvcolumn and allow it to expand
    tvcolumn.pack_start(cell, True)

    # set the cell "text" attribute to column 0 - retrieve text
    # from that column in treestore
    tvcolumn.add_attribute(cell, 'text', 0)
    
    # add tvcolumn to treeview
    tv.append_column(tvcolumn)

    return tv

def update_treestore(self, text, was):

    # Delete previous contents
    try:      
        while True:
            root = self.treestore.get_iter_first() 
            self.treestore.remove(root)                           
    except:
        pass
        #print  sys.exc_info()        
    if not text:
        return

    cnt = 0; piter2 = None
    try:
        for line in text:
            piter = self.treestore.append(None, [cut_lead_space(line)])
            if cnt == was:
                piter2 = piter
            cnt += 1
    except:
        pass
        #print  sys.exc_info()

    if piter2:
        self.tree.set_cursor(self.treestore.get_path(piter2))
    

