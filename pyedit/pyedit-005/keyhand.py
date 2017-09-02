#!/usr/bin/env python

# Key Handler for the editor. Extracted to a seperate module
# for easy update. The key handler is table driven, so new key 
# assignments can be made with ease

import gtk
import acthand

# ------------------------------------------------------------------------
# Handle keys:

class KeyHand:

    ctrl = 0; alt = 0; shift = 0

    def __init__(self):

        self.act = acthand.ActHand()

        # Here one can customize the key / function assingments
        self.reg_keytab = [
            [gtk.keysyms.Up, self.act.up],
            [gtk.keysyms.KP_Up, self.act.up],
            [gtk.keysyms.Down, self.act.down],
            [gtk.keysyms.KP_Down, self.act.down],
            [gtk.keysyms.Left, self.act.left],
            [gtk.keysyms.KP_Left, self.act.left],
            [gtk.keysyms.Right, self.act.right],
            [gtk.keysyms.KP_Right, self.act.right],
            [gtk.keysyms.Page_Up, self.act.pgup],
            [gtk.keysyms.KP_Page_Up, self.act.pgup],
            [gtk.keysyms.Page_Down, self.act.pgdn],
            [gtk.keysyms.KP_Page_Down, self.act.pgdn],
            [gtk.keysyms.Home, self.act.home],
            [gtk.keysyms.KP_Home, self.act.home],
            [gtk.keysyms.End, self.act.end],
            [gtk.keysyms.KP_End, self.act.end],
            [gtk.keysyms.Delete, self.act.delete],
            [gtk.keysyms.KP_Delete, self.act.delete],
            [gtk.keysyms.BackSpace, self.act.bs],
            [gtk.keysyms.Return, self.act.ret],
            [gtk.keysyms.Escape, self.act.esc],
            ]

        # Separate keytab on ctrl for easy customization. May call functions
        # in any other keytabs. (if sensitive to mod key, separate actions result)
        
        self.ctrl_keytab = [
            [gtk.keysyms.Up, self.act.up],
            [gtk.keysyms.KP_Up, self.act.up],
            [gtk.keysyms.Down, self.act.down],
            [gtk.keysyms.KP_Down, self.act.down],
            [gtk.keysyms.Left, self.act.left],
            [gtk.keysyms.KP_Left, self.act.left],
            [gtk.keysyms.Right, self.act.right],
            [gtk.keysyms.KP_Right, self.act.right],
            [gtk.keysyms.Page_Up, self.act.pgup],
            [gtk.keysyms.KP_Page_Up, self.act.pgup],
            [gtk.keysyms.Page_Down, self.act.pgdn],
            [gtk.keysyms.KP_Page_Down, self.act.pgdn],
            [gtk.keysyms.Home, self.act.home],
            [gtk.keysyms.KP_Home, self.act.home],
            [gtk.keysyms.End, self.act.end],
            [gtk.keysyms.KP_End, self.act.end],
            [gtk.keysyms.Delete, self.act.delete],
            [gtk.keysyms.KP_Delete, self.act.delete],
            [gtk.keysyms.BackSpace, self.act.bs],
            [gtk.keysyms.a, self.act.ctrl_a],
            [gtk.keysyms.A, self.act.ctrl_a],
            [gtk.keysyms.c, self.act.ctrl_c],
            [gtk.keysyms.C, self.act.ctrl_c],
            [gtk.keysyms.f, self.act.ctrl_f],
            [gtk.keysyms.F, self.act.ctrl_f],
            [gtk.keysyms.v, self.act.ctrl_v],
            [gtk.keysyms.V, self.act.ctrl_v],
            [gtk.keysyms.x, self.act.ctrl_x],
            [gtk.keysyms.X, self.act.ctrl_x],
            [gtk.keysyms.z, self.act.ctrl_z],
            [gtk.keysyms.Z, self.act.ctrl_z],
            ]

        # Separate keytab on ctrl - alt for easy customization. 

        self.ctrl_alt_keytab = [
            [gtk.keysyms.a, self.act.ctrl_alt_a],
            [gtk.keysyms.A, self.act.ctrl_alt_a],
            ]

        # Separate keytab on alt for easy customization. 

        self.alt_keytab = [
            [gtk.keysyms.Up, self.act.up],
            [gtk.keysyms.KP_Up, self.act.up],
            [gtk.keysyms.Down, self.act.down],
            [gtk.keysyms.KP_Down, self.act.down],
            [gtk.keysyms.Left, self.act.left],
            [gtk.keysyms.KP_Left, self.act.left],
            [gtk.keysyms.Right, self.act.right],
            [gtk.keysyms.KP_Right, self.act.right],
            [gtk.keysyms.Page_Up, self.act.pgup],
            [gtk.keysyms.KP_Page_Up, self.act.pgup],
            [gtk.keysyms.Page_Down, self.act.pgdn],
            [gtk.keysyms.KP_Page_Down, self.act.pgdn],
            [gtk.keysyms.Home, self.act.home],
            [gtk.keysyms.KP_Home, self.act.home],
            [gtk.keysyms.End, self.act.end],
            [gtk.keysyms.KP_End, self.act.end],
            [gtk.keysyms.Delete, self.act.delete],
            [gtk.keysyms.KP_Delete, self.act.delete],
            [gtk.keysyms.BackSpace, self.act.bs],
            [gtk.keysyms.s, self.act.alt_s],
            [gtk.keysyms.S, self.act.alt_s],
            ]

    # When we get focus, we start out with no modifier keys

    def reset(self):
        self.ctrl = 0; self.alt = 0; self.shift = 0

    # Main entry point for handling keys:

    def handle_key(self, self2, area, event):

        #print "key event", area, event

        ret = self.handle_modifiers(self2, area, event)
        if ret: return

        # Propagate to document (just for easy access)
        self2.ctrl = self.ctrl
        self2.alt = self.alt
        self2.shift = self.shift
       
        # Call the appropriate handlers
        if self.ctrl and self.alt:
            self.handle_ctrl_alt_key(self2, area, event)
        elif self.alt:
            self.handle_alt_key(self2, area, event)
        elif self.ctrl:
            self.handle_ctrl_key(self2, area, event)
            
        # We handle shift internally in the prev functions
        #elif self.shift: 
        #    if self.handle_shift_key(self2, area, event):
        #        return
        else:
            self.handle_reg_key(self2, area, event)

    # --------------------------------------------------------------------
    # Note that it does not handle stacked contol keys - just on / off

    def handle_modifiers(self, self2, area, event):

        ret = False

        # Do key down:
        if  event.type == gtk.gdk.KEY_PRESS:
            if event.keyval == gtk.keysyms.Alt_L or \
                    event.keyval == gtk.keysyms.Alt_R:
                #print "Alt down"
                self.alt = True; ret = True
            elif event.keyval == gtk.keysyms.Control_L or \
                    event.keyval == gtk.keysyms.Control_R:
                #print "Ctrl down"
                self.ctrl = True; ret = True
            if event.keyval == gtk.keysyms.Shift_L or \
                  event.keyval == gtk.keysyms.Shift_R:
                #print "shift down"
                self.shift = True; ret = True

        # Do key up
        elif  event.type == gtk.gdk.KEY_RELEASE:
            if event.keyval == gtk.keysyms.Alt_L or \
                  event.keyval == gtk.keysyms.Alt_R:
                #print "Alt up"
                self.alt = False; ret = True
            if event.keyval == gtk.keysyms.Control_L or \
                  event.keyval == gtk.keysyms.Control_R:
                #print "Ctrl up"
                self.ctrl = False; ret = True
            if event.keyval == gtk.keysyms.Shift_L or \
                  event.keyval == gtk.keysyms.Shift_R:
                #print "shift up"
                self.shift = False; ret = True
            
        return ret
    # --------------------------------------------------------------------

    # Obsolete:
    def handle_shift_key(self, self2, area, event):
        #print "Shift hand"
        xidx = self2.caret[0]; idx =  self2.caret[1] 
        ret = False                
        return ret

    def handle_ctrl_alt_key(self, self2, area, event):
        self._handle_key(self2, area, event, self.ctrl_alt_keytab)

    # --------------------------------------------------------------------
    # Regular key

    def handle_reg_key(self, self2, area, event):
        self._handle_key(self2, area, event, self.reg_keytab)

    # --------------------------------------------------------------------
    # Control key

    def handle_ctrl_key(self, self2, area, event):
        self._handle_key(self2, area, event, self.ctrl_keytab)

    # --------------------------------------------------------------------
    # Alt key

    def handle_alt_key(self, self2, area, event):
        if  event.type == gtk.gdk.KEY_PRESS:
            #print "alt hand", event
            if event.keyval >= gtk.keysyms._1 and event.keyval <= gtk.keysyms._9:
                #print "Alt num", event.keyval - gtk.keysyms._1
                self2.notebook.set_current_page(event.keyval - gtk.keysyms._1)
            elif event.keyval == gtk.keysyms._0:
                self2.appwin.window.set_focus(self2.appwin.treeview)
            else:
                self._handle_key(self2, area, event, self.alt_keytab)
        
    # Internal key handler

    def _handle_key(self, self2, area, event, xtab):

        ret = False
        if  event.type == gtk.gdk.KEY_PRESS:
            gotkey = False
            for kk, func in xtab:
                if event.keyval == kk:        
                    gotkey = True
                    func(self2)
                    break

            # No key assignment found, assume char
            if not gotkey:
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
                    self2.text[yidx] = line2[:xidx] + ccc + line2[xidx:]                
                    self2.set_caret(self2.caret[0] + 1, self2.caret[1])
                    self2.inval_line()
                    self2.changed = True
                except: 
                    # Could not convert it to character, alert user
                    # Usualy unhandled control, so helps developmet
                    print "Other", event.keyval
                    pass

        return ret


