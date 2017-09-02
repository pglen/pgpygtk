#!/usr/bin/env python

# ------------------------------------------------------------------------
# Python Alarm

import os, sys, getopt, signal
import gobject, gtk, pango
import random, time, warnings

def newala(strx = ""):
    
    now = time.localtime()
    
    dialog = gtk.Dialog("New Alarm - " + strx,
               None,
               gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
               (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
                
    dialog.set_default_response(gtk.RESPONSE_ACCEPT)

     # Spacers
    label1  = gtk.Label("   ");   label2  = gtk.Label("   ") 
    label1a = gtk.Label("   ");   label2a = gtk.Label("   ") 
    label3  = gtk.Label("   ");   label4  = gtk.Label("   ") 
    label3a = gtk.Label("   ");   label4a = gtk.Label("   ") 
    label5  = gtk.Label("   ");   label6  = gtk.Label("   ") 
    label5a = gtk.Label("   ");   label6a = gtk.Label("   ") 
    label7  = gtk.Label("   ");   label8  = gtk.Label("   ") 

    hbox3a = gtk.HBox()
    hbox3a.pack_start(label1a, False)  
    dialog.vbox.pack_start(hbox3a)

    cal = gtk.Calendar()
    hbox3 = gtk.HBox()
    hbox3.pack_start(label3a, False)  
    hbox3.pack_start(cal)  
    hbox3.pack_start(label4a, False)  
    dialog.vbox.pack_start(hbox3)

    hbox3a = gtk.HBox()
    hbox3a.pack_start(label3, False)  
    hour = gtk.Label("Hours:");   mins = gtk.Label("Minutes:") 
    hh = gtk.SpinButton(); hh.set_range(0, 23); hh.set_increments(1, 4)
    hh.set_value(now.tm_hour)
    hbox3a.pack_start(hour)  
    hbox3a.pack_start(hh)  
    mm = gtk.SpinButton(); mm.set_range(0, 59); mm.set_increments(1, 4)
    mm.set_value(now.tm_min)
    hbox3a.pack_start(mins)  
    hbox3a.pack_start(mm)  
    hbox3a.pack_start(label4, False)  
    dialog.vbox.pack_start(hbox3a)
    
    entry3 = gtk.Entry(); 
    hbox6 = gtk.HBox()
    hbox6.pack_start(label5a, False)  
    ent  = gtk.Label(" Name: ")
    hbox6.pack_start(ent, False)
    hbox6.pack_start(entry3)  
    hbox6.pack_start(label6a, False)  
    dialog.vbox.pack_start(hbox6)
    
    hbox2 = gtk.HBox()
    entry = gtk.combo_box_entry_new_text()
    entry.append_text("Execute")
    entry.append_text("Play")
    hbox2.pack_start(label1, False)  
    exe = gtk.Label(" Exe:     ");   
    hbox2.pack_start(exe, False)  
    hbox2.pack_start(entry)  
    hbox2.pack_start(label2, False)  
    dialog.vbox.pack_start(hbox2)
    
    entry2 = gtk.Entry(); 
    hbox4 = gtk.HBox()
    hbox4.pack_start(label5, False)  
    arg = gtk.Label(" Arg:     ") 
    hbox4.pack_start(arg, False)  
    hbox4.pack_start(entry2)  
    hbox4.pack_start(label6, False)  
    dialog.vbox.pack_start(hbox4)
    
    dialog.show_all()
    response = dialog.run()   
    
    # Replicate results for return
    txt =  entry.get_active_text()
    txt2 = entry2.get_text()
    name = entry3.get_text()
    ddd = cal.get_date(); 
    # Correct for null based month
    dddd = ddd[0], ddd[1] + 1, ddd[2]
    
    hhh = int(hh.get_value())
    mmm = int(mm.get_value())
    
    dialog.destroy()
        
    if response != gtk.RESPONSE_ACCEPT:   
        return False
    else:
        return  name, txt, txt2, dddd, (hhh, mmm)

if __name__ == '__main__':
    
    newala(sys.argv[1])
    

