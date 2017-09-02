#!/usr/bin/env python

# ------------------------------------------------------------------------
# Python Alarm. Pop up window and execute instructions.

import os, sys, getopt, signal
import gobject, gtk, pango
import random, time, warnings

def parseline(strx):
    #print "strx", strx
    if strx[0].startswith("#"):
        return
    if strx[0] == "DATE":
        print "   alarm time", strx[1]

# ------------------------------------------------------------------------

def newala(strx = ""):
    
    now = time.localtime()
    
    dialog = gtk.Dialog("Alarm Progress",
               None,
               gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
               (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
                
    dialog.set_default_response(gtk.RESPONSE_ACCEPT)
    
    if strx:
        try:
            ff = open(strx, "r").read()
            fff = string.split(ff, "\n")
            for aa in fff:
                aaa = string.split(aa, "=")
                bbb = []
                for cc in aaa:
                    bbb.append(string.strip(cc))
                if len(bbb):
                    parseline(bbb)
        except:
            print "Cannot read file", sys.exc_info()
            pass
        
    label3  = gtk.Label("   ");   label4  = gtk.Label("   ") 
    label5  = gtk.Label("   ");   label6  = gtk.Label("   ") 
    
    hbox3 = gtk.HBox()
    hbox3.pack_start(label3, False)  
    dialog.vbox.pack_start(hbox3)
    
    hbox4 = gtk.HBox()
    hbox4.pack_start(label5, False)  
    if not strx :
        strx = "No file Specified"
        
    arg = gtk.Label(strx) 
    hbox4.pack_start(arg, False)  
    hbox4.pack_start(label6, False)  
    dialog.vbox.pack_start(hbox4)

    hbox5 = gtk.HBox()
    hbox5.pack_start(label4, False)  
    dialog.vbox.pack_start(hbox5)
    
    fourfile = "d" + strx[1:]
    try:
        os.rename(strx, fourfile)
    except:
        print "Cannot rename file", sys.exc_info()
        pass
 
    dialog.show_all()
    response = dialog.run()   
    
    dialog.destroy()
        
    if response != gtk.RESPONSE_ACCEPT:   
        return False
        
    return True
    
if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        sys.argv.append("")
    
    newala(sys.argv[1])
    

