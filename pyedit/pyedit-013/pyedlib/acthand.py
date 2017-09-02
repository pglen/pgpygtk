#!/usr/bin/env python
 
# Action Handler for the editor. Extracted to a separate module for 
# easy update. These are the actions for pyedit. You may define more
# and attach a key handler to it in the tables of keyhand.py

# Notes:
#
# a.) Navigation may be blind, the doc class will contain the cursor
#       within the document.
#
# b.) Some functions are sensitive to shift ctrl alt etc ...
#       See the arrow key code [left()] how it is implemented to extend 
#       selection.
#
# c.) Anatomy of key handler function: 
#       shift pre - ctrl/alt handler - regular handler - shift post
#       This way the nav keys can select in their original function
#
# d.) Token completion. Tokens are kept in a stack 10 deep. If half of the
#       token is typed, the token complete will fill in the other half.
#       This is a very desirable behavior when writing code, as it feeds the 
#       variable name to the text, essentially preventing var name mistype.
#       Because token completion has a short stack, it has a large 
#       probability to fill in the var names from local scope.
#       If token completion filled in an unwanted string, backpedal to the 
#       half point in the string and type as usual.
#       If the completion behavure is not desired, disable the code marked
#       "Token Completion"
#

import string, gtk, subprocess
import pedync, pedofd, pedspell

# Some action functions have their own file
from pedfind import *
from pedgoto import *
from pedundo import *
from keywords import *

# General set of utilities
from pedutil import *

# Action handler. Called from key handler. 
# Function name hints to key / action. like up() is key up, and the action

class ActHand:

    def __init__(self):
        self.was_home = 0
        self.was_end = 0

    # -----------------------------------------------------------------------
            
    def up(self, self2):
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 

        if self2.alt:
            self.pgup(self2)
        elif self2.ctrl:
            pass
        elif self2.shift:
            # Begin select
            if self2.xsel == -1:
                self2.xsel = xidx
                self2.xsel2 = xidx + 1
            if self2.ysel == -1:
                self2.ysel = yidx

        self2.set_caret(xidx, yidx - 1)            
        
        if self2.shift:
            self2.ysel2 = self2.caret[1] + self2.ypos 
            self2.invalidate()
        else:
            self2.clearsel()
            
    # --------------------------------------------------------------------

    def down(self, self2):
    
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 

        if self2.ctrl:
            pass
        elif self2.alt:
            self.pgdn(self2)
        elif self2.shift:
            # Begin select
            if self2.xsel == -1:
                self2.xsel = xidx
                self2.xsel2 = xidx 
                self2.colsel = False
            if self2.ysel == -1:
                self2.ysel = yidx

        self2.set_caret(xidx, yidx + 1)
            
        if self2.shift:            
            self2.ysel2 = self2.caret[1] + self2.ypos 
            self2.invalidate()
        else:
            self2.clearsel()
                
    # --------------------------------------------------------------------

    def left(self, self2):
    
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        
        if self2.shift:
            # Begin select
            if self2.xsel == -1:
                self2.xsel = xidx
                #self2.colsel = True
            if self2.ysel == -1:
                self2.ysel = yidx
                
        if self2.ctrl:
            line = self2.text[yidx]
            idx  = xprevchar(line, " ", self2.caret[0] - 1)
            idx2 = prevchar(line, " ", idx) 
            idx3 = xprevchar(line, " ", idx2) 
            if idx == -1:
                #print "ctrl - L prev line"
                if yidx:
                    yidx -= 1                    
                    line = self2.text[yidx]
                    xidx = len(line)
                    idx = xprevchar(line, " ", xidx)
                    self2.set_caret(idx+1 , yidx)             
            else:        
                self2.set_caret(idx3+1, yidx)                             
            self2.invalidate()
        elif self2.alt:
            line = self2.text[yidx]
            begs, ends = selword(line, xidx-1)
            self2.set_caret(begs, yidx)                    
        else:
            self2.set_caret(xidx - 1, yidx)
            
        # Extend selection
        if self2.shift:
            self2.ysel2 = self2.caret[1] + self2.ypos            
            if self2.ysel > self2.ysel2:
                self2.xsel = self2.caret[0] + self2.xpos
            else:
                self2.xsel2 = self2.caret[0] + self2.xpos
        else:
            self2.clearsel()
                
    # ---------------------------------------------------------------------

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
            idx = nextchar(line, " ", xidx)
            idx2 = xnextchar(line, " ", idx)
            #print idx, idx2, len(line)            
            # Jump to next line
            if idx2 == idx or idx2 == len(line):
                yidx += 1
                if yidx < len(self2.text):
                    self2.caret[0] = 0
                    line = self2.text[yidx]
                    idx2 = xnextchar(line, " ", 0)
                    self2.set_caret(idx2, yidx) 
                    self2.invalidate()           
            else:
                #print "ctrl_right", idx2, yidx 
                self2.set_caret(idx2, yidx)                                    
        elif self2.alt:
            line = self2.text[yidx]
            begs, ends = selword(line, xidx)
            self2.set_caret(ends, yidx)                    
        else:
            self2.set_caret(xidx + 1, yidx)

        # Extend selection
        if self2.shift:
            self2.ysel2 = self2.caret[1] + self2.ypos            
            if self2.ysel > self2.ysel2:
                self2.xsel = self2.caret[0] + self2.xpos
            else:
                self2.xsel2 = self2.caret[0] + self2.xpos
            self2.invalidate()
        else:
            self2.clearsel()
        
    # ---------------------------------------------------------------------
    # This handler is also used for:
    #       o  addig new lines 
    #       o  signaling for rescan 
    #       o  signaling for rescan 

    def ret(self, self2):
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        self.pad_list(self2, yidx)
        line = self2.text[yidx][:] 
        self2.undoarr.append((xidx, yidx, MODIFIED, self2.text[yidx]))
        spaces = cntleadchar(line, " ")                     
        self2.text[yidx] = line[:xidx];             
        # Insert new after current
        yidx += 1
        self2.undoarr.append((xidx, yidx, ADDED + CONTFLAG, spaces + line[xidx:]))
        text = self2.text[:yidx]
        text.append(spaces + line[xidx:])
        text += self2.text[yidx:]
        self2.text = text                
        self2.set_caret(len(spaces), yidx)

        # Signal the rest for ...
        for aa in peddoc.sumkeywords:
            if line.find(aa) >= 0:
                self2.needscan = True
                
        # Contain undo 
        limit_undo(self2)
        
        # Update maxlines 
        mlines = len(self2.text)
        if mlines > self2.maxlines + 10:
            self2.set_maxlines(mlines)
            
        self2.set_changed(True)
        self2.invalidate()

    def delete(self, self2):
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        
        # Delete selection
        if self2.xsel != -1:
            #print "sel del"
            self.cut(self2, True)            
        else:        
            xlen = len(self2.text[yidx])
            if xlen:
                line = self2.text[yidx][:]                              
                if xidx >= xlen:     # bring in line from below
                    self2.undoarr.append((xidx, yidx, MODIFIED, self2.text[yidx]))
                    self2.text[yidx] += genstr(" ", xidx-xlen)
                    self2.text[yidx] += self2.text[yidx+1][:]                              
                    self2.undoarr.append(\
                                (xidx, yidx+1, DELETED + CONTFLAG, self2.text[yidx+1]))
                    del (self2.text[yidx+1])
                    self2.invalidate()                                        
                else:               # remove char
                    self2.undoarr.append((xidx, yidx, MODIFIED, self2.text[yidx]))
                    self2.text[yidx] = line[:xidx] + line[xidx+1:]                
                    self2.set_caret(xidx, yidx)
                    self2.inval_line()
            else:
                del (self2.text[yidx])

        self2.set_changed(True)
        self2.invalidate()       

    # --------------------------------------------------------------------

    def bs(self, self2):
    
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 

        # Delete selection
        if self2.xsel != -1:
            #print "sel del"
            self.cut(self2, True)            
        else:
            if xidx > 0:
                line = self2.text[yidx][:]      
                self2.undoarr.append((xidx, yidx, MODIFIED, self2.text[yidx]))
                self2.text[yidx] = line[:xidx - 1] + line[xidx:]                
                self2.set_caret(xidx - 1, yidx)
                self2.inval_line()
            else:                                   # Move line up
                if yidx > 0:
                    if yidx < len(self2.text):      # Any text?
                        self2.undoarr.append((xidx, yidx-1, MODIFIED, self2.text[yidx-1]))
                        line = self2.text[yidx][:]      
                        lenx = len(self2.text[yidx-1])
                        self2.text[yidx-1] += line
                        self2.set_caret(lenx, yidx-1)
                        self2.undoarr.append(\
                                (xidx, yidx, DELETED + CONTFLAG, self2.text[yidx]))
                        del (self2.text[yidx])
                        self2.invalidate()                                        
                    else:                           # Just update cursor
                        self2.set_caret(xidx, yidx-1)               

        self2.set_changed(True)

    # --------------------------------------------------------------------

    def pgup(self, self2):
    
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        
        if self2.shift:
            # Begin select
            if self2.xsel == -1:
                self2.xsel = xidx
                self2.colsel = False
            if self2.ysel == -1:
                self2.ysel = yidx
                   
        if self2.alt:
            #print "alt-pgup"
            self2.mained.nextwin()
        elif self2.ctrl:
            self2.set_caret(self2.caret[0], yidx - 2 * self2.pgup)                
        else:
            self2.set_caret(self2.caret[0], yidx - self2.pgup)                
        
        # Extend selection
        if self2.shift:
            self2.ysel2 = self2.caret[1] + self2.ypos            
            if self2.ysel > self2.ysel2:
                self2.xsel = self2.caret[0] + self2.xpos
            else:
                self2.xsel2 = self2.caret[0] + self2.xpos
            self2.invalidate()
        else:
            self2.clearsel()
       
    # --------------------------------------------------------------------

    def pgdn(self, self2):
    
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        
        if self2.shift:
            # Begin select
            if self2.xsel == -1:
                self2.xsel = xidx
                self2.colsel = False
            if self2.ysel == -1:
                self2.ysel = yidx
                   
        if self2.alt:
            #print "alt-pgdn"
            self2.mained.prevwin()            
        elif self2.ctrl:
            self2.set_caret(self2.caret[0], yidx + 2 * self2.pgup)
        else:
            self2.set_caret(self2.caret[0], yidx + self2.pgup)
            
        # Extend selection
        if self2.shift:
            self2.ysel2 = self2.caret[1] + self2.ypos            
            if self2.ysel > self2.ysel2:
                self2.xsel = self2.caret[0] + self2.xpos
            else:
                self2.xsel2 = self2.caret[0] + self2.xpos
            self2.invalidate()
        else:
            self2.clearsel()
       

    # --------------------------------------------------------------------

    def home(self, self2):
    
        xidx = self2.caret[0] + self2.xpos
        yidx = self2.caret[1] + self2.ypos 
        if self2.shift:
            # Begin select
            if self2.xsel == -1:
                self2.xsel = xidx
            if self2.ysel == -1:
                self2.ysel = yidx
        if self2.alt:
            #print "alt-home"
            self2.mained.firstwin()
        elif self2.ctrl:
            self2.set_caret(0, 0)
            self2.invalidate()           
        else:
            self.was_home += 1
            if self.was_home == 1:
                self2.set_caret(0, yidx)
                self2.invalidate()                                       
            if self.was_home == 2:
                self2.set_caret(0, yidx - self2.pgup)
                self2.invalidate()                                         
            elif self.was_home == 3:
                #print "bof"
                self2.set_caret(0, 0)
                self2.invalidate()                           
                self.was_home = 0                
             
        if self2.shift:        
            # End select
            self2.xsel2 = self2.caret[0] + self2.xpos
            self2.ysel2 = self2.caret[1] + self2.ypos
            self2.invalidate()
        else:
            self2.clearsel()
            self2.invalidate()
 
    # --------------------------------------------------------------------

    def end(self, self2):        
    
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
 
        if self2.shift:
            # Begin select
            if self2.xsel == -1:
                self2.xsel = xidx
            if self2.ysel == -1:
                self2.ysel = yidx
        if self2.alt:
            #print "alt-end"
            self2.mained.lastwin()
        elif self2.ctrl:
            last = len(self2.text) - 1
            xlen = len(self2.text[last])
            self2.set_caret(xlen, last)
            self2.invalidate()            
        elif self2.shift:
            # Begin select
            if self2.xsel == -1:
                self2.xsel = self2.caret[0]  + self2.xpos
            if self2.ysel == -1:
                self2.ysel = self2.caret[1]  + self2.ypos
            xlen = len(self2.text[yidx])
            self2.set_caret(xlen, self2.caret[1] + self2.ypos)
            self2.xsel2 = self2.caret[0] + self2.xpos
            self2.ysel2 = self2.caret[1] + self2.ypos
            self2.invalidate()
        else:        
            self2.clearsel()
            self.was_end += 1
            if self.was_end == 2:
                #print "eop"
                yidx += 20
                xlen = len(self2.text[yidx])
                self2.set_caret(xlen, yidx)
                self2.invalidate()           
                              
            elif self.was_end == 3:
                #print "eof"
                last = len(self2.text) - 1
                xlen = len(self2.text[last])
                self2.set_caret(xlen, last)
                self2.invalidate()            
                self.was_end = 0                
            else:    
                xlen = len(self2.text[yidx])
                self2.set_caret(xlen, yidx)
                
        if self2.shift:        
            # End select
            self2.xsel2 = self2.caret[0] + self2.xpos
            self2.ysel2 = self2.caret[1] + self2.ypos
            self2.invalidate()
        else:
            self2.clearsel()
            self2.invalidate()
 
                
    # --------------------------------------------------------------------
    
    def esc(self, self2):
    
        self2.mained.update_statusbar("Esc")                     
        self2.clearsel()
        #print "ESC"

    def ins(self, self2):
        #print "INS"
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        self2.insert = not self2.insert
        self2.set_caret(xidx, yidx)
        
    def ctrl_a(self, self2):
        #print "CTRL -- A"                 
        self2.xsel = 0; self2.ysel = 0
        self2.ysel2 = len(self2.text)
        self2.xsel2 = self2.maxlinelen
        self2.set_caret(self2.maxlinelen,  len(self2.text))
        self2.invalidate()
            
    def ctrl_b(self, self2):
        #print "CTRL -- B"                 
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        line = self2.text[yidx]
        bb, ee = selword(line, xidx)
        if bb != ee:
            self2.xsel = bb; self2.xsel2 =  ee               
            self2.ysel = self2.ysel2 = yidx
        else:
            self2.mained.update_statusbar("Please navigate to word.")                     
        
        self2.invalidate()
        self2.set_changed(True)
            
    # --------------------------------------------------------------------
    
    def ctrl_alt_a(self, self2):
        #print "CTRL - ALT - A"                 
        pass
             
     # --------------------------------------------------------------------
     
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
            
        #print "clip:", cumm
        clip = gtk.Clipboard()
        clip.set_text(cumm)

    # --------------------------------------------------------------------
    
    def ctrl_e(self, self2):
    
        #print "CTRL - E"                 
        
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        line = self2.text[yidx]
        self2.undoarr.append((xidx, yidx, MODIFIED, self2.text[yidx]))
        
        cntb, cnte = selword(line, xidx)        
        wlow = line[cntb:cnte].capitalize()
        #print "word   '" + line[cntb:cnte] + "'", wlow
        self2.text[yidx] = line[:cntb] + wlow + line[cnte:]
        self2.set_changed(True)
        self2.inval_line()   

    def alt_f(self, self2):
        #print "ALT - F"                 
        pass
    
    def ctrl_f(self, self2):
        #print "CTRL - F"                 
        find(self, self2)
    
    def ctrl_h(self, self2):
        #print "CTRL - H"                 
        find(self, self2, True)
            
    def ctrl_g(self, self2):
        #print "CTRL - G"                 
        #self2.closedoc()
        if self2.shift:
            self.f5(self2)
        else:
            self.f6(self2)
        pass
        
    def ctrl_i(self, self2):
        #print "CTRL - I"  
        if self2.shift and self2.countup:
            self2.countup = 0
        
        strx = "%d" % self2.countup               
        for aa in strx:
            event = gtk.gdk.Event(gtk.gdk.KEY_PRESS); 
            event.keyval = ord(aa)
            self.add_key(self2, event)
        self2.countup += 1
         
    def ctrl_j(self, self2):
        #print "CTRL - J"                         
        self2.coloring(not self2.colflag)
        if self2.colflag: strx = "on"
        else: strx = "off"        
        self2.mained.update_statusbar("Coloring is %s." % strx) 
       
    def ctrl_k(self, self2):
        #print "CTRL - K"                 
        self2.hexview(not self2.hex)
    
    def ctrl_l(self, self2):
        #print "CTRL - L"                 
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        line = self2.text[yidx]

        cntb, cnte = selword(line, xidx)        
        wlow = line[cntb:cnte].lower()            
        #print "word   ", line[cntb:cnte], wlow            
        self2.text[yidx] = line[:cntb] + wlow + line[cnte:]
        self2.inval_line()   
        self2.set_changed(True)

    def ctrl_m(self, self2):
        #print "CTRL - M"                 
        self2.acorr = not self2.acorr
        if self2.acorr:  
            self2.mained.update_statusbar(\
                "Autocorrect is on with %d enties." % len(acorr))
        else:  
            self2.mained.update_statusbar("Autocorrect is off.") 
       
    def ctrl_r(self, self2):    
        #print "CTRL - R"     
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        line = self2.text[yidx]
        self2.undoarr.append((xidx, yidx, MODIFIED, self2.text[yidx]))

        cntb, cnte = selword(line, xidx) 
        if cntb == cnte:
              self2.mained.update_statusbar("Please nav to a word first.")
              return        
        w1 = line[cntb:cnte]        
        #print "word1", w1
        
        idx = xnextchar(line, " ", cnte)
        cntb2, cnte2 = selword(line, idx) 
        if cntb2 == cnte2:
              self2.mained.update_statusbar("No second word on line.")
              return              
        w2 = line[cntb2:cnte2]
        #print "word2", w2        
        
        idx2 = xnextchar(line, " ", cnte2)
        cntb3, cnte3 = selword(line, idx2) 
        if cntb3 == cnte3:
              self2.mained.update_statusbar("No third word on line.")
              return              
        w3 = line[cntb3:cnte3]
        #print "word3", w3        
        
        self2.text[yidx] = line[:cntb] + \
                w3 + " " + w2 + " " + w1 + line[cnte3:] 
        self2.inval_line()    
        
    
    # ---------------------------------------------------------------------
     
    def ctrl_t(self, self2):
    
        #print "CTRL - T"     
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        line = self2.text[yidx]
        self2.undoarr.append((xidx, yidx, MODIFIED, self2.text[yidx]))                      

        cntb, cnte = selword(line, xidx) 
        if cntb == cnte:
              self2.mained.update_statusbar("Please nav to a word first.")
              return        
        w1 = line[cntb:cnte]        
        #print "word1", w1
        
        idx = xnextchar(line, " ", cnte)
        cntb2, cnte2 = selword(line, idx) 
        if cntb2 == cnte2:
              self2.mained.update_statusbar("No second word on line.")
              return              
        w2 = line[cntb2:cnte2]
        #print "word2", w2        
        
        self2.text[yidx] = line[:cntb] + w2 + " " + w1 + line[cnte2:] 
        self2.inval_line()    
                            
    def ctrl_u(self, self2):
        #print "CTRL - U"                 
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        line = self2.text[yidx]
        self2.undoarr.append((xidx, yidx, MODIFIED, self2.text[yidx]))                      

        cntb, cnte = selword(line, xidx)        
        wlow = line[cntb:cnte].upper()            
        #print "word   ", line[cntb:cnte], wlow            
        self2.text[yidx] = line[:cntb] + wlow + line[cnte:]
        self2.inval_line()   
 
    def ctrl_v(self, self2):
        #print "CTRL - V"    
        clip = gtk.Clipboard()
        clip.request_text(self.clip_cb, self2)
    
    # Pad line list to accomodate insert
    # We group this operation into change (no undo needed)
    def pad_list(self, self2, yidx):     
         # Extend list to accomodate insert
        ylen = len(self2.text) - 1 # dealing with index vs len
        if yidx >= ylen:
            cnt = 0
            for aa in range(yidx - ylen):
                #self2.undoarr.append((0,  yidx + cnt, ADDED + CONTFLAG, ""))
                self2.text.append("")
                cnt += 1
            #self2.undoarr.append((0, yidx, NOOP, ""))            

    # Pad line to accomodate insert
    def pad_line(self, self2, xidx, yidx):
        xlen = len(self2.text[yidx])
        if xidx >= xlen:            
            #self2.undoarr.append((xidx, yidx, MODIFIED, self2.text[yidx]))                      
            for aa in range(xidx - xlen):                        
                self2.text[yidx] += " "
        
    # Paste clipboard
    def clip_cb(self, clip, text, self2):
        #print "Clipboard: '" + text + "'", self2.caret[1], self2.ypos          
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        
        # Replace selection
        if self2.xsel != -1:
            #print "sel replace"
            #self2.set_caret(self., yidx)
            self.cut(self2, True)
            
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
                
        cnt = yidx; cc = ""; ttt = str.split(text, "\n")
        
        if self2.colsel:
            self2.undoarr.append((xidx, yidx, NOOP, ""))
            for aa in ttt:           
                self.pad_list(self2, yidx)        
                line = self2.text[yidx]
                self2.undoarr.append((xidx, yidx, MODIFIED  + CONTFLAG, \
                                 self2.text[yidx]))
                if xidx > len(line):    # pad line
                    line +=  genstr(" ", xidx - len(line))                                  
                self2.text[yidx] = line[:xidx] + aa + line[xidx:]                        
                self2.gotoxy(xidx, yidx)
                yidx += 1
        else:
            if len(ttt) == 1:           # single line            
                self.pad_list(self2, yidx)        
                line = self2.text[yidx]
                self2.undoarr.append((xidx, yidx, MODIFIED, self2.text[yidx]))
                if xidx > len(line):    # pad line
                    line +=  genstr(" ", xidx - len(line))                                  
                self2.text[yidx] = line[:xidx] + ttt[0] + line[xidx:]                        
                self2.gotoxy(xidx+len(ttt[0]), yidx)
            else:
                self2.undoarr.append((xidx, yidx, NOOP, ""))            
                for aa in ttt: 
                    self.pad_list(self2, cnt)        
                    if cnt == yidx :            # first line            
                        line = self2.text[yidx]
                        if xidx > len(line):    # pad line
                            line += genstr(" ", xidx - len(line))                       
                        self2.undoarr.append((xidx, yidx, MODIFIED + CONTFLAG, \
                                        self2.text[yidx]))
                        bb  =  line[:xidx] + aa 
                        cc = line[xidx:]
                        self2.text[yidx] = bb
                    else:   
                        self2.undoarr.append((xidx, cnt, ADDED + CONTFLAG,\
                                        self2.text[cnt]))
                        text2 = self2.text[:cnt]
                        text2.append(aa)
                        text2 += self2.text[cnt:]
                        self2.text = text2        
                    cnt += 1
                #last line:     
                self2.undoarr.append((xidx, cnt-1, MODIFIED + CONTFLAG,\
                     self2.text[cnt-1]))                    
                text2 = self2.text[cnt-1]                    
                self2.text[cnt-1] = text2 + cc
                self2.gotoxy(len(text2), yidx + len(ttt)-1)
                
        self2.set_changed(True)
        self2.invalidate()
        
    # --------------------------------------------------------------------
    # Cut to clipboard
    
    def ctrl_x(self, self2):
        self.cut(self2)
    
    def cut(self, self2, fake = False):
        #print "CTRL - X"                 
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        
        if self2.xsel == -1 or  self2.ysel == -1:
            self2.mained.update_statusbar("Nothing selected")                     
            return 
            
        if self2.colsel:
            # Normalize 
            xssel = min(self2.xsel, self2.xsel2)
            xesel = max(self2.xsel, self2.xsel2)
            yssel = min(self2.ysel, self2.ysel2)
            yesel = max(self2.ysel, self2.ysel2)                                    
        else:
            if self2.ysel < self2.ysel2:        
                yssel = self2.ysel
                yesel = self2.ysel2
                xssel = self2.xsel
                xesel = self2.xsel2
            elif self2.ysel == self2.ysel2:        
                yssel = self2.ysel
                yesel = self2.ysel2
                xssel = min(self2.xsel, self2.xsel2)
                xesel = max(self2.xsel, self2.xsel2)            
            else:
                yssel = self2.ysel2 
                yesel = self2.ysel        
                xssel = self2.xsel2
                xesel = self2.xsel
            
        #print xssel, xesel, yssel, yesel
        
        # Boundary undo (grouping stops)
        self2.undoarr.append((xidx, yidx, NOOP, ""))            

        cnt = yssel; cnt2 = 0; cumm = ""; darr = []
        while True:
            if cnt > yesel: break
            xidx = self2.caret[0] + self2.xpos; 
            yidx = self2.caret[1] + self2.ypos 
            line = self2.text[cnt]
            # TODO
            if self2.colsel:
                #self2.undoarr.append((xidx, yidx, MODIFIED + CONTFLAG, self2.text[cnt]))            
                #frag = line[xssel:xesel]
                #self2.text[cnt] = line[:xssel] + line[xesel:]
                pass
            else :                                  
                self2.undoarr.append((xssel, cnt, MODIFIED + CONTFLAG, self2.text[cnt]))            
                if cnt == yssel and cnt == yesel:   # Selection on one line
                    frag = line[xssel:xesel]
                    self2.text[cnt] = line[:xssel] + line[xesel:]
                    #if xssel == 0:
                    #    darr.append(cnt)                                   
                elif cnt == yssel:                  # On start line
                    sline = cnt
                    frag = line[xssel:]
                    self2.text[cnt] = line[:xssel]
                    #if xssel == 0:
                    #    darr.append(cnt)                                   
                elif cnt == yesel:                  # On end line
                    frag = line[:xesel]
                    self2.text[sline] = self2.text[sline] + line[xesel:]
                    darr.append(cnt)                                    
                else:                               # On selected line                   
                    frag = line[:]
                    #self2.text[cnt] = ""
                    darr.append(cnt)                       
            
            if cnt2: frag = "\n" + frag
            cumm += frag
            cnt += 1; cnt2 += 1
        
        #print "clip x: '", cumm, "'" 
        
        # Delete from the end to the beginning
        darr.reverse()
        for aa in darr:
            self2.undoarr.append((xidx, aa, DELETED + CONTFLAG, self2.text[aa]))                            
            #print "del", aa
            del(self2.text[aa])

        self2.mained.update_statusbar("Cut %d lines" % (yesel - yssel))                     
        
        self2.clearsel()
        self2.gotoxy(xssel, yssel)    
        
        # We use this forr deleting as well, so fake clip op 
        if not fake:
            clip = gtk.Clipboard()
            clip.set_text(cumm)
            
        self2.invalidate()
        self2.set_changed(True)

    def ctrl_y(self, self2):
        #print "CTRL - Y"                         
        redo(self2, self)
        
    def ctrl_z(self, self2):
        #print "CTRL - Z"                         
        undo(self2, self)            

    def alt_c(self, self2):
        #print "ALT - C"                         
        pass
        
    def alt_d(self, self2):
        #print "ALT - D"                 
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        
        # After EOF, eat content
        if yidx >= len(self2.text):
            yidx = len(self2.text) - 1
            yidx = max(yidx, 0)
            self2.set_caret(xidx, self2.caret[1] - 1)
            
        self2.undoarr.append((xidx, yidx, DELETED, self2.text[yidx]))
        del (self2.text[yidx])
        self2.invalidate()                                                
        self2.set_changed(True)

    def alt_k(self, self2):
        #print "ALT - K"                 
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        self2.undoarr.append((xidx, yidx, MODIFIED, self2.text[yidx]))
        line = self2.text[yidx]
        self2.text[yidx] = line[:xidx]
        self2.invalidate()                                                
        self2.set_changed(True)

    def alt_l(self, self2):
        #print "ALT - L"                 
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos         
        self2.xsel = 0; self2.xsel2 = len(self2.text[yidx]) 
        self2.ysel = self2.ysel2 = yidx
        self2.inval_line()   
        
    def alt_o(self, self2):
        # Simplified open
        fname = pedofd.ofd("")
        if fname != "":
            self2.mained.openfile(fname)
            
    def alt_s(self, self2):
        #print "ALT - S"                 
        find(self, self2)
        
    def alt_v(self, self2):
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos         
        line = self2.text[yidx]
        self2.xsel, self2.xsel2 = selasci2(line, xidx, "-_.[]")        
        self2.ysel = self2.ysel2 = yidx
        self2.inval_line()   
        
    def alt_w(self, self2):
        #print "ALT - S"                 
        self2.save()
        
    def f1(self, self2):
        #print "F1"                         
        self2.mained.update_statusbar("Opening help file ...")                             
        try:
            ret = subprocess.Popen(["gnome-help",])
        except:
            pedync.message("\n   Cannot launch devhelp   \n\n"
                           "              (Please install)")                            
    def f2(self, self2):
        #print "F2" 
        self2.mained.update_statusbar("Opening DEV help file ...")                             
        try:
            ret = subprocess.Popen(["devhelp",])
        except:
            pedync.message("\n   Cannot launch devhelp   \n\n"
                           "              (Please install)")                            
    def f3(self, self2):
        #print "F3"
        self2.mained.update_statusbar("Opening KEYS help file ...")                             
        rr = get_exec_path("KEYS")
        ret = subprocess.Popen(["pangview.py",  rr])                 
        
    def f4(self, self2):
        #print "F4"        
        self.play(self2, True)

    def f5(self, self2):
        #print "F5"                 
        if len(self2.accum) == 0:
            self2.mained.update_statusbar("Please specify a search string (Ctrl-F) or (Alt-S)")                     
            return
        
        self2.mained.update_statusbar("Locating previous match.")                     
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        cnt = len (self2.accum) - 1; match = False
        while True:
            if cnt < 0 : break
            xstr = self2.accum[cnt]            
            
            try:
                bb = xstr.split(" ")[0].split(":")
            except: pass
            #print "TREE sel", bb
            if int(bb[1]) < yidx:
                self.peddoc.gotoxy(int(bb[0]), int(bb[1]), int(bb[2]), True)
                match = True
                break

            cnt -= 1
            
        if not match:
            self2.mained.update_statusbar("At or before first match.") 
            
    def f6(self, self2):
        #print "F6"                 
        if len(self2.accum) == 0:
            self2.mained.update_statusbar(\
                "Please specify a search string (Ctrl-F) or (Alt-S)")
            return
            
        self2.mained.update_statusbar("Locating Next match.") 
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        match = False
        
        for xstr in self2.accum:
            # Get back numbers the python way
            try:
                bb = xstr.split(" ")[0].split(":")
            except: pass
            #print "TREE sel", bb
            if int(bb[1]) > yidx:
                self.peddoc.gotoxy(int(bb[0]), int(bb[1]), int(bb[2]), True)
                match = True
                break
                
        if not match:
            self2.mained.update_statusbar("At or after last match.")                                     
               
    def f7(self, self2):
        #print "F7"                         
        self.keyhand.reset()               
        if self2.record:
            self2.mained.update_statusbar("Ended recording.")                     
            self2.record = False
        else:
            self2.mained.update_statusbar("Started recording ...")                     
            self2.recarr = []
            self2.record = True
        self.keyhand.reset()               
    
    # ---------------------------------------------------------------------
      
    def play(self, self2, anim = False):
    
        if self2.record:
            self2.mained.update_statusbar("Still recording, press F7 to stop")                     
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

            #var = (int(event.type), event.keyval, int(event.state))            
             
            tt, kk, ss, \
            self.keyhand.shift, self.keyhand.ctrl, self.keyhand.alt = self2.recarr[idx]
            #print "macro", tt, kk, ss            
            idx+=1
            
            # Synthesize keystroke. We do not replicate state as 
            # pyedit maintains its own internally. (see keyhand.reset())
            event = gtk.gdk.Event(tt); 
            event.keyval = kk; 
        
            self.keyhand.state2 = ss
            self.keyhand.handle_key2(self2, None, event)        
            if anim:
                usleep(30)
            
        # If the state gets out or sync ...
        self.keyhand.reset()               
        self2.mained.update_statusbar("Ended Play.")                     
    
      
    def f8(self, self2, anim = False):
        #print "F8"      
        self.play(self2, anim)
        
    def f9(self, self2):
        #print "F9 spell"              
        self2.spell = not self2.spell
        if self2.spell: ooo = "on"
        else: ooo = "off" 
        self2.mained.update_statusbar("Spell checking is %s" % ooo)                     
        pedspell.spell(self2)
        
    # This will not be called, as it activates menu
    def f10(self, self2):
        if self2.shself2.shift:
            #print "shift F10"                 
            pass
        if self2.ctrl:
            #print "ctrl F10"                 
            pass

    def f11(self, self2):                
        if self2.mained.full:
            self2.mained.window.unfullscreen()
            self2.mained.full = False
        else:
            self2.mained.window.fullscreen()
            self2.mained.full = True
        #print "F11"                 

    def f12(self, self2):
        #print "F12"                 
        pass

    # ---------------------------------------------------------------------
    # Add regular key
    
    def add_key(self, self2, event):

        if self2.readonly:
            self2.mained.update_statusbar("This buffer is read only.")                     
            return
            
        if self2.hex:
            self2.mained.update_statusbar("Cannot edit in hex mode.")                     
            return

        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 

        # Extend list to accomodate insert
        self.pad_list(self2, yidx)
        
        # Pad string to accomodate insert
        self.pad_line(self2, xidx, yidx)
        
        line2 = self2.text[yidx][:]      
        ccc = ""            
        try: 
            ccc = chr(event.keyval)                 
            self2.undoarr.append((xidx, yidx, MODIFIED, self2.text[yidx]))
            # Replace selection
            if self2.xsel != -1:
                #print "sel replace"
                self.ctrl_x(self2, True)
                line2 = self2.text[yidx][:]      
                
            if self2.insert:                
                self2.text[yidx] = line2[:xidx] + ccc + line2[xidx:]                                
            else:
                self2.text[yidx] = line2[:xidx] + ccc + line2[xidx+1:]
                                
            mlen = len(self2.text[yidx])            
            if  mlen > self2.maxlinelen:                
                self2.set_maxlinelen(mlen)
        
            #self2.set_caret(calc_tabs(self2.text[yidx], xidx + 1), yidx)
            self2.set_caret(xidx + 1, yidx)

            if self2.acorr:
                # See if autocorrect is needed 
                for acs, acs2 in acorr:
                    lendiff = len(acs2) - len(acs)
                    ss = self2.text[yidx][xidx-(len(acs)-1):xidx+1]
                    if ss == acs:
                        xstr =  "Autocorrected to "'"%s"'"" % acs2
                        self2.mained.update_statusbar(xstr)
                        line = self2.text[yidx]
                        self2.text[yidx] = line[:xidx-(len(acs)-1)] + acs2 + line[xidx+1:]            
                        #self2.set_caret(calc_tabs(self2.text[yidx], \
                        #    xidx + lendiff), yidx)
                        self2.set_caret(xidx + lendiff, yidx)
                        
            ''' # See if token is complete
            if ccc == " ":            
                line = self2.text[yidx]
                begs, ends = selword(line, xidx - 1)
                if ends - begs >= 4:                  
                    #print "token complete", line[begs:ends]
                    # Limit size of token stack
                    if len(self2.tokens) > 10:
                        del(self2.tokens[0])
                    self2.tokens.append(line[begs:ends])                    
                    #print self2.tokens
                            
            # See if token completion is needed 
            line = self2.text[yidx]
            idx = prevchar(line, " ", xidx - 1)
            word = line[idx+1:xidx+1]
            #print "word", word
            for aa in self2.tokens:
                lendiff = len(aa) - len(word)                
                #print "src",  AA[:LEN(AA) / 2] 
                if aa[:len(aa) / 2] == word:
                    #print "completion", aa                    
                    self2.text[yidx] = line[:idx+1] + aa + line[xidx+1:]            
                    self2.set_caret(calc_tabs(self2.text[yidx], \
                        xidx + lendiff), yidx)                    
                    xstr =  "Autocompleted to "'"%s"'"" % aa
                    self2.mained.update_statusbar(xstr)'''
            
            ''' # See if spell checking needed
            if ccc == " ":           
                #err = pedspell.spell_line(line, 0, len(line))
                #self2.ularr = []
                #for ss, ee in err:
                #    self2.ularr.append((ss, yidx, ee))
                self2.invalidate()    '''
                
            self2.inval_line()
            self2.set_changed(True)
        except: 
            # Could not convert it to character, alert user
            # Usualy unhandled control, so helps developmet
            #print  "Other key", sys.exc_info(), event.keyval
            print "Other key", event.keyval, hex(event.keyval), hex(event.state)
            pass
        return True

    def alt_a(self, self2):
        #print "ALT - A"
        self2.mained.saveall()
        
    def alt_g(self, self2):
        goto(self2)
        
    # --------------------------------------------------------------
    # Tab handle is awkward. The regular key tab will insert 
    # spaces to the next multiple of four.
    # To insert a real tab, use shift tab  (like for makefiles)
    
    def tab(self, self2):
    
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 

        #print "TAB", self2.shift
        tabstop = 4
        #tabstop = self2.tabstop

        # No Selection, do tab
        if self2.ysel == -1:
            self2.undoarr.append((xidx, yidx, MODIFIED, self2.text[yidx]))
            if self2.shift:
                line2 = self2.text[yidx][:]              
                self2.text[yidx] = line2[:xidx] + "\t" + line2[xidx:]
                spaces = self2.tabstop - (xidx % self2.tabstop)
                self2.set_caret(xidx+1, yidx)
                    
                #print "shif tab", spaces
                #self2.set_caret(xidx + tabstop, yidx)
            else:
                spaces = tabstop - (xidx % tabstop)
                while spaces:
                    event = gtk.gdk.Event(gtk.gdk.KEY_PRESS); 
                    event.keyval = ord(" ")
                    self.add_key(self2, event)
                    spaces -= 1
            self2.invalidate()
        else:
            # Indent, normalize 
            yssel = min(self2.ysel, self2.ysel2)
            yesel = max(self2.ysel, self2.ysel2)
            #print "TAB in sel"
            cnt = yssel
            self2.undoarr.append((xidx, yidx, NOOP, ""))                    
            if self2.shift:
                while True:
                    if cnt > yesel: break
                    self2.undoarr.append((xidx, cnt, MODIFIED | CONTFLAG, self2.text[cnt]))
                    self2.text[cnt] =  rmlspace(self2.text[cnt], 4)
                    cnt += 1                
            else:
                while True:
                    if cnt > yesel: break
                    self2.undoarr.append((xidx, cnt, MODIFIED | CONTFLAG, self2.text[cnt]))
                    self2.text[cnt] = "    " + self2.text[cnt]
                    cnt += 1                
            self2.invalidate()


# EOF


