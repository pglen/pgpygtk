#!/usr/bin/env python

# Action Handler for goto

import gtk

def goto(self2):

    dialog = gtk.Dialog("pyedit: Goto Line",
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
    entry.set_width_chars(24)
    dialog.vbox.pack_start(label4)  

    hbox2 = gtk.HBox()
    hbox2.pack_start(label6, False)  
    hbox2.pack_start(entry)  
    hbox2.pack_start(label7, False)  
    dialog.vbox.pack_start(hbox2)
    dialog.vbox.pack_start(label5)  

    hbox = gtk.HBox()
    dialog.vbox.pack_start(hbox)
    dialog.vbox.pack_start(label8)  
    
    dialog.show_all()
    response = dialog.run()   
    self2.oldsearch = entry.get_text()
    srctxt = entry.get_text()     
    dialog.destroy()

    if response == gtk.RESPONSE_ACCEPT:
        #print "goto", "'" + srctxt + "'"
        if srctxt == "":
            self2.mained.update_statusbar("Must specify line to goto.")
            return          
        try:
            num = int(srctxt)
        except:
            self2.mained.update_statusbar("Invalid line number.")
            return

        self2.gotoxy(self2.caret[0], num)
        if num > len(self2.text):
            xpos = self2.ypos + int(self2.caret[1])                    
            self2.mained.update_statusbar("Goto line passed end, landed on %d" %  xpos)
        else:
            self2.mained.update_statusbar("Done goto line %d" % num)
        
