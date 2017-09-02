#!/usr/bin/env python

# ------------------------------------------------------------------------
# Python Alarm

import os, sys, getopt, signal, gobject, gtk, pango
import random, time, warnings, stat

from pgutil import  *

def newala(strx = "", adate = ""):
    parms = []
    while 1:
        parms = _newala(strx, parms)
        if not parms:
            break
        ddd = parms[0]; ttt = parms[1]
        ttt = (ddd[0], ddd[1], ddd[2], ttt[0], ttt[1], 0, -1, -1, -1)
        tt = time.mktime(ttt)      
        if time.time() > tt:
            message("Cannot set an alarm in the past.")
        elif not is_executable(parms[3]):
            message("Alarm action must be an executable file.")
        else:
            break
    return parms
             
def resp(dialog, arg2 = None):
    print "event", dialog, arg2
    #return True
    
# ------------------------------------------------------------------------

def _newala(strx = "", parms = []):
                
    # Increment to next minute
    if parms:
        ddd = parms[0]; ttt = parms[1]
        ttt = (ddd[0], ddd[1], ddd[2], ttt[0], ttt[1], 0, -1, -1, -1)
        now = time.localtime(time.mktime(ttt))
    else:
        now = time.localtime(time.time() + 60)
        
    dialog = gtk.Dialog("New Alarm - " + strx,
               None,
               gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
               (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
                
    dialog.set_default_response(gtk.RESPONSE_ACCEPT)
    
    #dialog.connect("event", resp)  
    #ok = dialog.get_widget_for_response(gtk.RESPONSE_ACCEPT)
    #ok.connect("activate", ok_button, dialog)
    
    try:
        dialog.set_icon_from_file("/usr/share/pyala/ala3.png")
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
    
    entry  = add_field("Name:  ", dialog)
    if parms:
        entry.set_text(parms[2])
    entry2 = add_field("Exe:      ", dialog); 
    entry.connect("activate", activate, entry2)
    entry2.connect("activate", activate2, dialog)
    
    if parms:
        entry2.set_text(parms[3])
    
    hbox3 = gtk.HBox()
    add_spacer(hbox3)
    dialog.vbox.pack_start(hbox3)
    
    dialog.show_all()
    response = dialog.run()   

    # Replicate results for return
    name  = entry.get_text()
    exe   = entry2.get_text()
    
    # Correct for zero based month
    ddd = cal.get_date(); 
    dddd = ddd[0], ddd[1] + 1, ddd[2]
    hhh = int(hh.get_value());   mmm = int(mm.get_value())
    
    dialog.destroy()
        
    if response != gtk.RESPONSE_ACCEPT:   
        return False
        
    return  dddd, (hhh, mmm), name, exe

# ------------------------------------------------------------------------
def ok_button(butt, dialog):
    print "ok_button", butt, dialog

def activate(txt, field):
    #print "activate", txt, dialog
    field.grab_focus()
    
def activate2(txt, dialog):
    #print "activate2", txt, dialog
    dialog.response(gtk.RESPONSE_ACCEPT)
    
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

# ------------------------------------------------------------------------

def is_executable(fname):

    ppp = respath(fname);  reln = os.path.expanduser(fname)
    if not os.access(reln, os.X_OK) and not ppp:
        return False
    return True

if __name__ == '__main__':
    
    newala(sys.argv[1])
    









