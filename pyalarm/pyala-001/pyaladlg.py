#!/usr/bin/env python

# ------------------------------------------------------------------------
# Python Alarm

import os, sys, getopt, signal
import gobject, gtk, pango
import random, time, warnings

from pgutil import  *

def newala(strx = ""):
    
    # Increment to next minute
    now = time.localtime(time.time() + 60)
        
    dialog = gtk.Dialog("New Alarm - " + strx,
               None,
               gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
               (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
                
    dialog.set_default_response(gtk.RESPONSE_ACCEPT)

    try:
        dialog.set_icon_from_file("ala3.png")
    except:
        pass

    hbox3a = gtk.HBox()
    add_spacer(hbox3a)
    dialog.vbox.pack_start(hbox3a)

    hbox3 = gtk.HBox();    
    add_spacer(hbox3)
    cal = gtk.Calendar();   hbox3.pack_start(cal)  
    add_spacer(hbox3)
    dialog.vbox.pack_start(hbox3)

    hbox3a = gtk.HBox()
    add_spacer(hbox3a)
    hh = gtk.SpinButton(); hh.set_range(0, 23); hh.set_increments(1, 4)
    hour = gtk.Label("Hours:");   
    hh.set_value(now.tm_hour)
    hbox3a.pack_start(hour) ;  hbox3a.pack_start(hh)  
    
    mins = gtk.Label("Minutes:") 
    mm = gtk.SpinButton(); mm.set_range(0, 59); mm.set_increments(1, 4)
    mm.set_value(now.tm_min)
    hbox3a.pack_start(mins)  
    hbox3a.pack_start(mm)  
    add_spacer(hbox3a)
    dialog.vbox.pack_start(hbox3a)
    
    '''hbox2 = gtk.HBox()
    combo = gtk.combo_box_entry_new_text()
    combo.append_text("Execute")
    combo.append_text("Play")
    add_spacer(hbox2)
    label1 = gtk.Label("Action:  "); hbox2.pack_start(label1, False)
    hbox2.pack_start(combo)
    add_spacer(hbox2)
    dialog.vbox.pack_start(hbox2)'''
    
    entry  = add_field("Name:  ", dialog)
    entry2 = add_field("Exe:      ", dialog)
    #entry3 = add_field("Arg:      ", dialog)
    #entry4 = add_field("Play:     ", dialog)

    hbox3 = gtk.HBox()
    add_spacer(hbox3)
    dialog.vbox.pack_start(hbox3)
    
    dialog.show_all()
    
    response = dialog.run()   

    # Replicate results for return
    name  = entry.get_text()
    act  =  "" # combo.get_active_text()
    txt2  = entry2.get_text()
    #txt3  = entry3.get_text()
    #txt4  = entry4.get_text()
    ddd = cal.get_date(); 
    # Correct for null based month
    dddd = ddd[0], ddd[1] + 1, ddd[2]
    hhh = int(hh.get_value());   mmm = int(mm.get_value())
    dialog.destroy()
        
    if response != gtk.RESPONSE_ACCEPT:   
        return False
    else:
        ttt = (dddd[0], dddd[1], dddd[2], hhh, mmm, 0, -1, -1, -1)
        tt = time.mktime(ttt)      
        #print time.asctime(time.localtime(tt))
        #print time.asctime(time.localtime(time.time()))
        if time.time() > tt:
            message("Cannot set an alarm in the past.")
            return False
        return  dddd, (hhh, mmm), act, name, txt2 #, txt3, txt4
    
# ------------------------------------------------------------------------
# Add a text field

def add_spacer(hbox):
    label = gtk.Label("   ");
    hbox.pack_start(label, False)
    return label
    
# ------------------------------------------------------------------------
# Add a text field

def add_field(label, dialog):

    hbox = gtk.HBox()
    add_spacer(hbox)
    lab = gtk.Label(label);         hbox.pack_start(lab, False)  
    entry = gtk.Entry();            hbox.pack_start(entry)  
    add_spacer(hbox)
    dialog.vbox.pack_start(hbox)
    return entry
    
if __name__ == '__main__':
    
    newala(sys.argv[1])
    






