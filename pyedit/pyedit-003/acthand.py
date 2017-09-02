#!/usr/bin/env python

# Action Handler for the editor. Extracted to a seperate module
# for easy update. These are the actions for pyedit. You may define more
# and attach a key handler to it in keyhand.py

# Notes:
#
# a.) Navigation may be blind, the doc class will contain the cursor
# within the document.
# b.) Some functions are sensitive to shift ctrl alt

import string

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
        if self2.ctrl:
            line = self2.text[yidx]
            idx = self.prevchar(line, " ", self2.caret[0] - 1)
            idx2 = self.xprevchar(line, " ", idx) + 1
            self2.set_caret(idx2, self2.caret[1])            
        elif self2.shift:
            # Begin select
            if self2.xsel == -1:
                self2.xsel = self2.caret[0]
            if self2.ysel == -1:
                self2.ysel = self2.caret[1]
            self2.set_caret(self2.caret[0] - 1, self2.caret[1])            
            self2.xsel2 = self2.caret[0] + self2.xpos
            self2.ysel2 = self2.caret[1] + self2.ypos
            self2.invalidate()
        else:
            self2.clearsel()
            self2.set_caret(self2.caret[0] - 1, self2.caret[1])
            
    def right(self, self2):
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        if self2.ctrl:
            line = self2.text[yidx]
            idx = self.nextchar(line, " ", self2.caret[0])
            idx2 = self.xnextchar(line, " ", idx)
            self2.set_caret(idx2, self2.caret[1])            
        if self2.shift:
            # Begin select
            if self2.xsel == -1:
                self2.xsel = xidx
            if self2.ysel == -1:
                self2.ysel = yidx

            self2.set_caret(self2.caret[0] + 1, self2.caret[1])            
            self2.xsel2 = self2.caret[0] + self2.xpos
            self2.ysel2 = self2.caret[1] + self2.ypos
            self2.invalidate()
        else:
            self2.clearsel()
            self2.set_caret(self2.caret[0] + 1, self2.caret[1])
                
    def ret(self, self2):
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        line = self2.text[yidx][:] 
        spaces = self.cntleadchar(line, " ")                     
        self2.text[yidx] = line[:xidx];             
        # Insert new after current
        yidx += 1
        text = self2.text[:yidx]
        text.append(spaces + line[xidx:])
        text += self2.text[yidx:]
        self2.text = text                
        self2.set_caret(len(spaces), self2.caret[1] + 1)
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
        self2.invalidate()       

    def bs(self, self2):
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 

        if xidx > 0:
            line = self2.text[yidx][:]      
            self2.text[yidx] = line[:xidx - 1] + line[xidx:]                
            self2.set_caret(self2.caret[0] - 1, self2.caret[1])
            self2.inval_line()
        else:                       # move line up
            if yidx > 0:
                line = self2.text[yidx][:]      
                lenx = len(self2.text[yidx-1])
                self2.text[yidx-1] += line
                self2.set_caret(lenx, self2.caret[1]-1)
                del (self2.text[yidx])
                self2.invalidate()                                        

    def pgup(self, self2):
        if self2.ctrl:
            self2.set_caret(self2.caret[0], self2.caret[1] - self2.pgup)                
        else:
            self2.set_caret(self2.caret[0], self2.caret[1] - self2.pgup)                

    def pgdn(self, self2):
        self2.set_caret(self2.caret[0], self2.caret[1] + self2.pgup)

    def home(self, self2):
        if self2.ctrl:
            self2.ypos  = 0
            self2.set_caret(0, 0)
            self2.invalidate()            
        elif self2.shift:
            # Begin select
            if self2.xsel == -1:
                self2.xsel = self2.caret[0]
            if self2.ysel == -1:
                self2.ysel = self2.caret[1]
            self2.set_caret(0, self2.caret[1])
            self2.xsel2 = self2.caret[0] + self2.xpos
            self2.ysel2 = self2.caret[1] + self2.ypos
            self2.invalidate()
        else:
            self2.set_caret(0, self2.caret[1])

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

    def ctrl_a(self, self2):
        print "CTRL -- A"                 
        self2.xsel = 0; self2.ysel = 0
        self2.ysel2 = len(self2.text)
        self2.xsel2 = 100
        self2.set_caret(100,  len(self2.text))
        self2.invalidate()
            
    def ctrl_alt_a(self, self2):
        print "CTRL - ALT - A"                 
    
    def ctrl_c(self, self2):
        print "CTRL - C"                 
    
    def ctrl_v(self, self2):
        print "CTRL - V"                 
                
    def ctrl_z(self, self2):
        print "CTRL - Z"                 
                


# ------------------------------------------------------------------------
# Utility functions for action handlers

    def genstr(self, strx, num):
        ret = ""
        while num:        
            ret += strx; num = num - 1
        return ret

    def cntleadchar(self, strx, chh):
        xlen = len(strx); pos = 0; ret = ""
        while pos < xlen:
            if strx[pos] != chh:        
                break
            ret += chh
            pos = pos + 1
        return ret

    # Find next char
    def nextchar(self, strx, xchar, start):
        idx = start; end =  len(strx) - 1
        while True:
            if idx > end: break
            chh = strx[idx]
            if chh == xchar: break               
            idx += 1
        return idx

    # Find next not char
    def xnextchar(self, strx, xchar, start):
        idx = start; end =  len(strx) - 1
        while True:
            if idx > end: break
            chh = strx[idx]
            if chh != xchar:
                break               
            idx += 1
        return idx

    # Find prev char
    def prevchar(self, strx, xchar, start):
        idx = start; 
        idx = min(len(strx) - 1, idx)
        while True:
            if idx < 0: break
            chh = strx[idx]
            if chh == xchar: break               
            idx -= 1            
        return idx

    # Find prev not char
    def xprevchar(self, strx, xchar, start):
        idx = start; 
        idx = min(len(strx) - 1, idx)
        while True:
            if idx < 0: break
            chh = strx[idx]
            if chh != xchar:
                break               
            idx -= 1
        return idx

