#!/usr/bin/env python

# Action Handler for the editor. Extracted to a seperate module
# for easy update. These are the actions for pyedit. You may define more
# and attach a key handler to it in keyhand.py

# Notes:
#
# a.) Navigation may be blind, the doc class will contain the cursor
# within the document.
# b.) Some functions are sensitive to shift ctrl alt
# c.) Anatomy of function: 
#       shift pre - ctrl/alt handler - regular handler - shift post
#

import string, marshal, gtk

import peddoc
from pedutil import *
from pedfind import *

CONTFLAG = 0x80
CONTMASK = CONTFLAG -1

#print hex(CONTFLAG), hex(CONTMASK)

class ActHand:

    def __init__(self):
        pass

    def up(self, self2):
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 

        if self2.ctrl:
            pass
        elif self2.shift:
            # Begin select
            if self2.xsel == -1:
                self2.xsel = xidx
                self2.xsel2 = xidx + 1
            if self2.ysel == -1:
                self2.ysel = yidx

            self2.set_caret(self2.caret[0], self2.caret[1] - 1)
            self2.ysel2 = self2.caret[1] + self2.ypos 
            self2.invalidate()
        else:
            self2.clearsel()
            self2.set_caret(self2.caret[0], self2.caret[1] - 1)

    def down(self, self2):
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 

        if self2.ctrl:
            pass
        elif self2.shift:
            # Begin select
            if self2.xsel == -1:
                self2.xsel = xidx
                self2.xsel2 = xidx + 1
                self2.colsel = False
            if self2.ysel == -1:
                self2.ysel = yidx

            self2.set_caret(self2.caret[0], self2.caret[1] + 1)
            self2.ysel2 = self2.caret[1] + self2.ypos 
            self2.invalidate()
        else:
            self2.clearsel()
            self2.set_caret(self2.caret[0], self2.caret[1] + 1)
                
    def left(self, self2):
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 

        if self2.shift:
            # Begin select
            if self2.xsel == -1:
                self2.xsel = self2.caret[0]
                self2.colsel = True
            if self2.ysel == -1:
                self2.ysel = self2.caret[1]
        if self2.ctrl:
            line = self2.text[yidx]
            idx = xprevchar(line, " ", self2.caret[0] - 1)
            idx2 = prevchar(line, " ", idx) 
            self2.set_caret(idx2 , self2.caret[1])             
            self2.invalidate()
        else:
            self2.set_caret(self2.caret[0] - 1, self2.caret[1])
            
        if self2.shift:
            self2.xsel2 = self2.caret[0] + self2.xpos
            self2.ysel2 = self2.caret[1] + self2.ypos            
        else:
            self2.clearsel()
            
    def right(self, self2):
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        if self2.shift:
            # Begin select
            if self2.xsel == -1:
                self2.xsel = xidx
                self2.colsel = False
            if self2.ysel == -1:
                self2.ysel = yidx
            
        if self2.ctrl:
            line = self2.text[yidx]
            idx = nextchar(line, " ", self2.caret[0])
            idx2 = xnextchar(line, " ", idx)
            self2.set_caret(idx2 - 1, self2.caret[1])            
        
            self2.set_caret(self2.caret[0] + 1, self2.caret[1])            
            self2.xsel2 = self2.caret[0] + self2.xpos
            self2.ysel2 = self2.caret[1] + self2.ypos
            self2.invalidate()
        else:
            self2.set_caret(self2.caret[0] + 1, self2.caret[1])

        if self2.shift:
            self2.xsel2 = self2.caret[0] + self2.xpos
            self2.ysel2 = self2.caret[1] + self2.ypos
            self2.invalidate()
        else:
            self2.clearsel()
                
    def ret(self, self2):
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        line = self2.text[yidx][:] 
        self2.undoarr.append((xidx, yidx, 0, self2.text[yidx]))
        spaces = cntleadchar(line, " ")                     
        self2.text[yidx] = line[:xidx];             
        # Insert new after current
        yidx += 1
        self2.undoarr.append((xidx, yidx, 1 + CONTFLAG, ""))
        text = self2.text[:yidx]
        text.append(spaces + line[xidx:])
        text += self2.text[yidx:]
        self2.text = text                
        self2.set_caret(len(spaces), self2.caret[1] + 1)
        for aa in peddoc.sumkeywords:
            if line.find(aa) >= 0:
                self2.needscan = True

        self2.set_changed(True)
        self2.invalidate()

    def delete(self, self2):
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        xlen = len(self2.text[yidx])
        if xlen:
            line = self2.text[yidx][:]                              
            if xidx >= xlen:     # bring in line from below
                self2.text[yidx] += self.genstr(" ", xidx-xlen)
                self2.text[yidx] += self2.text[yidx+1][:]                              
                del (self2.text[yidx+1])
                self2.invalidate()                                        
            else:               # remove char
                self2.text[yidx] = line[:xidx] + line[xidx+1:]                
                self2.set_caret(self2.caret[0], self2.caret[1])
                self2.inval_line()
        else:
            del (self2.text[yidx])

        self2.set_changed(True)
        self2.invalidate()       

    def bs(self, self2):
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 

        if xidx > 0:
            line = self2.text[yidx][:]      
            self2.undoarr.append((xidx, yidx, 0, self2.text[yidx]))
            self2.text[yidx] = line[:xidx - 1] + line[xidx:]                
            self2.set_caret(self2.caret[0] - 1, self2.caret[1])
            self2.inval_line()
        else:                                   # Move line up
            if yidx > 0:
                if yidx < len(self2.text):      # Any text?
                    self2.undoarr.append((xidx, yidx-1, 0, self2.text[yidx-1]))
                    line = self2.text[yidx][:]      
                    lenx = len(self2.text[yidx-1])
                    self2.text[yidx-1] += line
                    self2.set_caret(lenx, self2.caret[1]-1)
                    self2.undoarr.append(\
                            (xidx, yidx, 2 + CONTFLAG, self2.text[yidx]))
                    del (self2.text[yidx])
                    self2.invalidate()                                        
                else:                           # Just update cursor
                    self2.set_caret(self2.caret[0], self2.caret[1]-1)               

        self2.set_changed(True)

    def pgup(self, self2):
        if self2.ctrl:
            self2.set_caret(self2.caret[0], self2.caret[1] - 2 * self2.pgup)                
        else:
            self2.set_caret(self2.caret[0], self2.caret[1] - self2.pgup)                

    def pgdn(self, self2):
        if self2.ctrl:
            self2.set_caret(self2.caret[0], self2.caret[1] + 2 * self2.pgup)
        else:
            self2.set_caret(self2.caret[0], self2.caret[1] + self2.pgup)

    def home(self, self2):
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        if self2.shift:
            # Begin select
            if self2.xsel == -1:
                self2.xsel = xidx
            if self2.ysel == -1:
                self2.ysel = yidx
        if self2.ctrl:
            self2.ypos  = 0
            self2.set_caret(0, 0)
            self2.invalidate()           
        else:
            self2.set_caret(0, self2.caret[1])
        if self2.shift:        
            # End select
            self2.xsel2 = self2.caret[0] + self2.xpos
            self2.ysel2 = self2.caret[1] + self2.ypos
            self2.invalidate()
 
    def end(self, self2):        
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
 
        if self2.ctrl:
            last = len(self2.text) - 1
            xlen = len(self2.text[last])
            self2.set_caret(xlen, last)
            self2.invalidate()            
        elif self2.shift:
            # Begin select
            if self2.xsel == -1:
                self2.xsel = self2.caret[0]
            if self2.ysel == -1:
                self2.ysel = self2.caret[1]
            xlen = len(self2.text[yidx])
            self2.set_caret(xlen, self2.caret[1])
            self2.xsel2 = self2.caret[0] + self2.xpos
            self2.ysel2 = self2.caret[1] + self2.ypos
            self2.invalidate()
        else:        
            xlen = len(self2.text[yidx])
            self2.set_caret(xlen, self2.caret[1])

    def esc(self, self2):
        print "ESC"

    def ins(self, self2):
        print "INS"
        self2.insert = not self2.insert
        self2.set_caret(self2.caret[0], self2.caret[1])
        
    def ctrl_a(self, self2):
        #print "CTRL -- A"                 
        self2.xsel = 0; self2.ysel = 0
        self2.ysel2 = len(self2.text)
        self2.xsel2 = self2.maxlinelen
        self2.set_caret(self2.maxlinelen,  len(self2.text))
        self2.invalidate()
            
    def ctrl_alt_a(self, self2):
        print "CTRL - ALT - A"                 
     
    def ctrl_c(self, self2):
        #print "CTRL - C"             
        if self2.xsel == -1 or  self2.ysel == -1:
            self2.mained.update_statusbar("Nothing selected")                     
            return 
        # Normalize 
        xssel = min(self2.xsel, self2.xsel2)
        xesel = max(self2.xsel, self2.xsel2)
        yssel = min(self2.ysel, self2.ysel2)
        yesel = max(self2.ysel, self2.ysel2)

        cnt = yssel; cnt2 = 0; cumm = ""
        while True:
            if cnt > yesel: break
            line = self2.text[cnt]
            if self2.colsel:
                frag = line[xssel:xesel]
            else :                                  # startsel - endsel                        
                if cnt == yssel and cnt == yesel:   # sel on the same line
                    frag = line[xssel:xesel]
                elif cnt == yssel:                  # start line
                    frag = line[xssel:]
                elif cnt == yesel:                  # end line
                    frag = line[:xesel]
                else:
                    frag = line[:]

            if cnt2: frag = "\n" + frag
            cumm += frag
            cnt += 1; cnt2 += 1

        #print "cumm: '", cumm, "'" 

        clip = gtk.Clipboard()
        clip.set_text(cumm)
    
    def ctrl_f(self, self2):
        #print "CTRL - F"                 
        find(self, self2)
        
    def ctrl_v(self, self2):
        #print "CTRL - V"    
        clip = gtk.Clipboard()
        clip.request_text(self.clip_cb, self2)
        
    # Paste clipboard
    def clip_cb(self, clip, text, self2):
        #print "Clipboard: '" + text + "'"          
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        cnt = yidx; cc = ""; ttt = str.split(text, "\n")
        if len(ttt) == 1:           # single line            
            line = self2.text[yidx]
            self2.undoarr.append((xidx, yidx, 0, self2.text[yidx]))
            if xidx > len(line):    # pad line
                line +=  genstr(" ", xidx - len(line))                                  
            self2.text[yidx] = line[:xidx] + ttt[0] + line[xidx:]                        
            self2.goto(xidx+len(ttt[0]), yidx)
        else:
            for aa in ttt: 
                if cnt == yidx :            # first line            
                    line = self2.text[yidx]
                    if xidx > len(line):    # pad line
                        line += genstr(" ", xidx - len(line))                       
                    self2.undoarr.append((xidx, yidx, 0, self2.text[yidx]))
                    bb  =  line[:xidx] + aa 
                    cc = line[xidx:]
                    self2.text[yidx] = bb
                else:   
                    self2.undoarr.append((xidx, cnt, 1 + CONTFLAG,\
                                    self2.text[cnt]))
                    text2 = self2.text[:cnt]
                    text2.append(aa)
                    text2 += self2.text[cnt:]
                    self2.text = text2        
                cnt += 1
            #last line:     
            self2.undoarr.append((xidx, cnt-1, 0 + CONTFLAG,\
                 self2.text[cnt-1]))                    
            text2 = self2.text[cnt-1]                    
            self2.text[cnt-1] = text2 + cc
            self2.goto(len(text2), yidx + len(ttt)-1)
        self2.set_changed(True)
        self2.invalidate()
        
    def ctrl_x(self, self2):
        print "CTRL - X"                 
        self2.set_changed(True)
        
    def ctrl_z(self, self2):
        #print "CTRL - Z"                         
        xlen = len(self2.undoarr); uyy = 0
        if xlen == 0:
            self2.mained.update_statusbar("Nothing to undo.")                     
            self2.set_changed(False)
            return
  
        while True:
            xlen = len(self2.undoarr)
            xx, yy, mode, line = self2.undoarr[xlen-1]
            uyy = yy
            mode2 = mode & CONTMASK
            if mode2 == 0:                   # Line change
                self2.text[yy] = line
                self2.goto(xx, yy)
                self2.invalidate()
            elif mode2 == 1:                 # Addition
                del (self2.text[yy])
                self2.invalidate()
            elif mode2 == 2:                 # Deletion
                print "undo deleted"
                text = self2.text[:yy]
                text.append(line)
                text += self2.text[yy:]
                self2.text = text                                        
            else:
                print "undo: invalid mode"
                pass

            del (self2.undoarr[xlen-1])

            # Continue if cont flag is on
            if mode & CONTFLAG:  pass
            else: break

        self2.mained.update_statusbar("Undo done at line %d" % uyy)                     
                    

    def alt_s(self, self2):
        find(self, self2)
        #print "ALT - S"                 

    def alt_w(self, self2):
        self2.save()
        #print "ALT - S"                 

    def f1(self, self2):
        print "F1"                 

    def f2(self, self2):
        print "F2"                 

    def f3(self, self2):
        print "F3"                 

    def f4(self, self2):
        print "F4"                 

    def f5(self, self2):
        print "F5"                 

    def f6(self, self2):
        print "F6"                 

    def f7(self, self2):
        print "F7"                         
        self.keyhand.reset()               
        if self2.record:
            self2.mained.update_statusbar("Ended recording.")                     
            self2.record = False
        else:
            self2.mained.update_statusbar("Started recording ...")                     
            self2.recarr = []
            self2.record = True
        self.keyhand.reset()               
        
    def f8(self, self2, anim = False):
        print "F8"      
        if self2.record:
            self2.mained.update_statusbar("Still recording, press F5 to stop")                     
            return True
        
        xlen = len(self2.recarr) 
        if xlen == 0:
            self2.mained.update_statusbar("Nothing recorded, cannot play.")                     
            return True
            
        self.keyhand.reset()               
                
        self2.mained.update_statusbar("Started Play ...")                     
        idx = 0
        while True:
            if idx >= xlen: break

            tt = marshal.loads(self2.recarr[idx])        # Type
            kk = marshal.loads(self2.recarr[idx+1])      # Key
                    
            if kk == gtk.keysyms.F5 or kk == gtk.keysyms.F6:
                print "play: avoiding recursion"
                pass
            else:
                # Translate type
                if tt: tt = gtk.gdk.KEY_PRESS
                else: tt = gtk.gdk.KEY_RELEASE
                #print "play", tt, kk

                # Synthesize keystroke. We do not replicate state as 
                # pyedit maintains its own internally. (see keyhand.reset())
                event = gtk.gdk.Event(tt); event.keyval = kk
                
                # Access provided in keyhand line 20
                # Calling a parent class this way is unusual. We make sure
                # no recording key (F5 F6) is recorded to avoid o-o recursion.
                self.keyhand.handle_key(self2, None, event)        
                if anim:
                    usleep(10)
            idx += 2

        # If the state gets out or sync ...
        self.keyhand.reset()               
        self2.mained.update_statusbar("Ended Play.")                     
        
    def f9(self, self2):
        print "F9"                 

    # This will not be called, as it activates menu
    def f10(self, self2):
        print "F10"                 

    def f11(self, self2):                
        if self2.mained.full:
            self2.mained.window.unfullscreen()
            self2.mained.full = False
        else:
            self2.mained.window.fullscreen()
            self2.mained.full = True
        print "F11"                 

    def f12(self, self2):
        print "F12"                 

    # Add regular key
    def add_key(self, self2, event):
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 

        if self2.readonly:
            self2.mained.update_statusbar("This buffer is read only.")                     
            return ret
       
        # Extend list to accomodate insert
        ylen = len(self2.text) - 1 # dealing with index vs len
        if yidx >= ylen:
            for aa in range(yidx - ylen):
                self2.text.append("")

        # Pad string to accomodate insert
        xlen = len(self2.text[yidx])
        if xidx >= xlen:
            for aa in range(xidx - xlen):                        
                self2.text[yidx] += " "

        line2 = self2.text[yidx][:]      
        ccc = ""            
        try: 
            ccc = chr(event.keyval)                 
            self2.undoarr.append((xidx, yidx, 0, self2.text[yidx]))
            if self2.insert:
                self2.text[yidx] = line2[:xidx] + ccc + line2[xidx:]                
            else:
                self2.text[yidx] = line2[:xidx] + ccc + line2[xidx+1:]                

            self2.set_caret(self2.caret[0] + 1, self2.caret[1])
            self2.inval_line()
            self2.set_changed(True)
        except: 
            # Could not convert it to character, alert user
            # Usualy unhandled control, so helps developmet
            print "Other", sys.exc_info(), event.keyval
            pass

        return True

    def alt_g(self, self2):

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
        self.srctxt = entry.get_text()     
        dialog.destroy()

        if response == gtk.RESPONSE_ACCEPT:
            print "goto", "'" + self.srctxt + "'"
            
            if self.srctxt == "":
                self2.mained.update_statusbar("Must specify line to goto.")
                return          
            num = int(self.srctxt)
            self2.goto(self2.caret[0], num)
            if num > len(self2.text):
                xpos = self2.ypos + int(self2.caret[1])                    
                self2.mained.update_statusbar("Goto line passed end, landed on %d" %  xpos)
            else:
                self2.mained.update_statusbar("Done goto line %d" % num)
            
            


