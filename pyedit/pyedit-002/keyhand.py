#!/usr/bin/env python

# Key Handler for the editor. Extracted to a seperate module
# for easy update

import gtk

def genstr(strx, num):
    ret = ""
    while num:        
        ret += strx; num = num - 1
    return ret

def cntleadchar(strx, chh):
    xlen = len(strx); pos = 0; ret = ""
    while pos < xlen:
        if strx[pos] != chh:        
            break
        ret += chh
        pos = pos + 1
    return ret

class KeyHand:

    ctrl = 0; alt = 0; shift = 0

    def __init__(self):
        pass

    def handle_key(self, self2, area, event):
        #print "key event", area, event

        self.handle_modifiers(self2, area, event)
       
        if self.ctrl and self.alt:
            if self.handle_ctrl_alt_key(self2, area, event):
                return
    
        if self.alt:
            if self.handle_alt_key(self2, area, event): 
                return
  
        if self.ctrl:
            if self.handle_ctrl_key(self2, area, event):
                return
          
        #if self.shift:
        #    if self.handle_shift_key(self2, area, event):
        #        return

        self.handle_reg_key(self2, area, event)

    # --------------------------------------------------------------------

    def handle_modifiers(self, self2, area, event):

        if  event.type == gtk.gdk.KEY_PRESS:
            if event.keyval == gtk.keysyms.Alt_L or \
                    event.keyval == gtk.keysyms.Alt_R:
                #print "Alt down"
                self.alt = True
            elif event.keyval == gtk.keysyms.Control_L or \
                    event.keyval == gtk.keysyms.Control_R:
                #print "Ctrl down"
                self.ctrl = True
            if event.keyval == gtk.keysyms.Shift_L or \
                  event.keyval == gtk.keysyms.Shift_R:
                #print "shift down"
                self.shift = True

        # Do key up
        elif  event.type == gtk.gdk.KEY_RELEASE:
            if event.keyval == gtk.keysyms.Alt_L or \
                  event.keyval == gtk.keysyms.Alt_R:
                #print "Alt up"
                self.alt = False
            if event.keyval == gtk.keysyms.Control_L or \
                  event.keyval == gtk.keysyms.Control_R:
                #print "Ctrl up"
                self.ctrl = False
            if event.keyval == gtk.keysyms.Shift_L or \
                  event.keyval == gtk.keysyms.Shift_R:
                #print "shift up"
                self.shift = False
            
    # --------------------------------------------------------------------

    def handle_shift_key(self, self2, area, event):
        #print "Shift hand"
        xidx = self2.caret[0]; idx =  self2.caret[1] 
        ret = False
                
        return ret

    def handle_ctrl_alt_key(self, self2, area, event):
        print "CTrl-Alt hand"
        xidx = self2.caret[0]; idx =  self2.caret[1] 
        ret = False                    
        return ret

    def handle_ctrl_key(self, self2, area, event):
        #print "ctrl hand", event
        xidx = self2.caret[0]; idx =  self2.caret[1] 
        ret = False
        if  event.type == gtk.gdk.KEY_PRESS:
            if event.keyval ==  gtk.keysyms.a or \
               event.keyval ==  gtk.keysyms.A:
                print "CTRL - A"                 
                ret = True

            if event.keyval ==  gtk.keysyms.z or \
                event.keyval ==  gtk.keysyms.Z:
                print "CTRL - Z" 
                ret = True

            if event.keyval ==  gtk.keysyms.Home or \
                event.keyval ==  gtk.keysyms.KP_Home:
                print "CTRL - Home" 
                ret = True
                self2.set_caret(0,0)                 
            
            if event.keyval ==  gtk.keysyms.End or \
                event.keyval ==  gtk.keysyms.KP_End:
                print "CTRL - End" 
                ret = True
                ee = len(self2.text) - 1
                eee = len(self2.text[ee])    
                self2.set_caret(eee, ee)                 
                
            if event.keyval == gtk.keysyms.Tab:
                print "CTRL - Tab"                 
                return False
        
        return ret

    def handle_alt_key(self, self2, area, event):    
        xidx = self2.caret[0]; idx =  self2.caret[1] 
        ret = True
        
        if  event.type == gtk.gdk.KEY_PRESS:
            print "alt hand", event
            
        return ret

    # --------------------------------------------------------------------

    def handle_reg_key(self, self2, area, event):

        xidx = self2.caret[0]; idx =  self2.caret[1] 
        if  event.type == gtk.gdk.KEY_PRESS:
            if event.keyval == gtk.keysyms.Up:
                self2.set_caret(self2.caret[0], self2.caret[1] - 1)
                ret = False
            elif event.keyval == gtk.keysyms.Down:
                self2.set_caret(self2.caret[0], self2.caret[1] + 1)
                ret = False
            elif event.keyval == gtk.keysyms.Left:
                self2.set_caret(self2.caret[0] - 1, self2.caret[1])
                ret = False
            elif event.keyval == gtk.keysyms.Right:
                self2.set_caret(self2.caret[0] + 1, self2.caret[1])
            elif event.keyval == gtk.keysyms.Tab:
                self2.set_caret(self2.caret[0] + 1, self2.caret[1])
            elif event.keyval == gtk.keysyms.Page_Up or\
                    event.keyval == gtk.keysyms.KP_Page_Up:
                self2.set_caret(self2.caret[0], self2.caret[1] - 20)
            elif event.keyval == gtk.keysyms.Page_Down or\
                    event.keyval == gtk.keysyms.KP_Page_Down:
                self2.set_caret(self2.caret[0], self2.caret[1] + 20)

            elif event.keyval == gtk.keysyms.Return:
                line = self2.text[idx][:] 
                spaces = cntleadchar(line, " ")                     
                self2.text[idx] = line[:xidx];             
                # Insert new after current
                idx += 1
                text = self2.text[:idx]
                text.append(spaces + line[xidx:])
                text += self2.text[idx:]
                self2.text = text                
                self2.set_caret(len(spaces), self2.caret[1] + 1)
                self2.invalidate()

            elif event.keyval == gtk.keysyms.Home or \
                    event.keyval == gtk.keysyms.KP_Home:
                self2.set_caret(0, self2.caret[1])

            elif event.keyval == gtk.keysyms.End or \
                    event.keyval == gtk.keysyms.KP_End:
                xlen = len(self2.text[idx])
                self2.set_caret(xlen, self2.caret[1])
            elif event.keyval == gtk.keysyms.BackSpace:
                if self2.caret[0] > 0:
                    line = self2.text[idx][:]      
                    self2.text[idx] = line[:xidx - 1] + line[xidx:]                
                    self2.set_caret(self2.caret[0] - 1, self2.caret[1])
                    self2.inval_line()
                else:                       # move line up
                    if idx > 0:
                        line = self2.text[idx][:]      
                        lenx = len(self2.text[idx-1])
                        self2.text[idx-1] += line
                        self2.set_caret(lenx, self2.caret[1]-1)
                        del (self2.text[idx])
                        self2.invalidate()                                        
                                
            elif event.keyval == gtk.keysyms.Delete or \
                event.keyval == gtk.keysyms.KP_Delete:
                xlen = len(self2.text[idx])
                if xlen:
                    line = self2.text[idx][:]                              
                    if xidx >= xlen:     # bring in line from below
                        self2.text[idx] += genstr(" ", xidx-xlen)
                        self2.text[idx] += self2.text[idx+1][:]                              
                        del (self2.text[idx+1])
                        self2.invalidate()                                        
                    else:               # remove char
                        self2.text[idx] = line[:xidx] + line[xidx+1:]                
                        self2.set_caret(self2.caret[0], self2.caret[1])
                        self2.inval_line()
                else:
                    del (self2.text[idx])
                    self2.invalidate()                
            else:
                print "Other", event.keyval
                line = self2.text[idx][:]      
                ccc = ""            
                try: 
                    ccc = chr(event.keyval) 
                    self2.text[idx] = line[:xidx] + ccc + line[xidx:]                
                    self2.set_caret(self2.caret[0] + 1, self2.caret[1])
                    self2.inval_line()
                except: 
                    pass
        
#self2.grab_focus()


