#!/usr/bin/env python
 
import signal, os, time, sys, gtk, gobject

# Cut leading space in half

def cut_lead_space(xstr, divi = 2):
    res = ""; cnt = 0; idx = 0; spcnt = 0
    xlen = len(xstr); 
    while True:
        if cnt >= xlen: break
        chh = xstr[idx]
        if chh == " ":
            spcnt += 1
            if spcnt >= divi:
               spcnt = 0; res += " "
        else:
            res += xstr[idx:]
            break                     
        idx += 1
    return res
    
# ------------------------------------------------------------------------
# Let the higher level deal with errors.

def readfile(strx, sep = "\n"):

    text = []                  
    if strx != "":
        f = open(strx)
        buff = f.read();
        text = str.split(buff, sep)
        f.close()
    return text

def  writefile(strx, buff):          
    #print "writefile", strx
    if strx != "":
        f = open(strx, "w")
        for aa in buff:
            f.write(aa); f.write("\n")
        f.close()
    return

# Expand image name to image path:
def get_img_path(fname):
    img_dir = os.path.join(os.path.dirname(__file__), 'images')
    img_path = os.path.join(img_dir, fname)
    return img_path

# Expand file name to file path in the exec dir:
def get_exec_path(fname):
    exec_dir = os.path.dirname(__file__)
    exec_path = os.path.join(exec_dir, fname)
    return exec_path

# It's totally optional to do this, you could just manually insert icons
# and have them not be themeable, especially if you never expect people
# to theme your app.

def register_stock_icons():
    ''' This function registers our custom toolbar icons, so they
        can be themed.
    '''
    items = [('demo-gtk-logo', '_GTK!', 0, 0, '')]
    # Register our stock items
    gtk.stock_add(items)

    # Add our custom icon factory to the list of defaults
    factory = gtk.IconFactory()
    factory.add_default()

    img_dir = os.path.join(os.path.dirname(__file__), 'images')
    img_path = os.path.join(img_dir, 'gtk-logo-rgb.gif')

    #print img_path
    try:
        pixbuf = gtk.gdk.pixbuf_new_from_file(img_path)
        # Register icon to accompany stock item
     
        # The gtk-logo-rgb icon has a white background, make it transparent
        # the call is wrapped to (gboolean, guchar, guchar, guchar)
        transparent = pixbuf.add_alpha(True, chr(255), chr(255),chr(255))
        icon_set = gtk.IconSet(transparent)
        factory.add('demo-gtk-logo', icon_set)

    except gobject.GError, error:
        #print 'failed to load GTK logo ... trying local'
        try:
		    #img_path = os.path.join(img_dir, 'gtk-logo-rgb.gif')
		    pixbuf = gtk.gdk.pixbuf_new_from_file('gtk-logo-rgb.gif')
		    # Register icon to accompany stock item
		    # The gtk-logo-rgb icon has a white background, make it transparent
		    # the call is wrapped to (gboolean, guchar, guchar, guchar)
		    transparent = pixbuf.add_alpha(True, chr(255), chr(255),chr(255))
		    icon_set = gtk.IconSet(transparent)
		    factory.add('demo-gtk-logo', icon_set)

        except gobject.GError, error:
            print 'failed to load GTK logo for toolbar'


# ------------------------------------------------------------------------
# Utility functions for action handlers

def genstr(strx, num):
    ret = ""
    while num:        
        ret += strx; num -= 1
    return ret

def cntleadchar(strx, chh):
    xlen = len(strx); pos = 0; ret = ""
    if xlen == 0: return ret
    while pos < xlen:
        if strx[pos] != chh:        
            break
        ret += chh
        pos = pos + 1
    return ret

# Find next char
def nextchar(strx, xchar, start):
    idx = start; end =  len(strx) - 1
    while True:
        if idx > end: break
        chh = strx[idx]
        if chh == xchar: break               
        idx += 1
    return idx

# Find next not char
def xnextchar( strx, xchar, start):
    idx = start; end =  len(strx) - 1
    while True:
        if idx > end: break
        chh = strx[idx]
        if chh != xchar:
            break               
        idx += 1
    return idx

# Find next not in str
def xnextchar2( strx, xchar, start):
    idx = start; end =  len(strx) - 1
    while True:
        if idx > end: break
        chh = strx[idx]
        if xchar.find(chh) == -1:
            break               
        idx += 1
    return idx

# Find prev char
def prevchar( strx, xchar, start):
    idx = start; 
    idx = min(len(strx) - 1, idx)
    while True:
        if idx < 0: break
        chh = strx[idx]
        if chh == xchar: break               
        idx -= 1            
    return idx

# Find prev not char
def xprevchar( strx, xchar, start):
    idx = start; 
    idx = min(len(strx) - 1, idx)
    while True:
        if idx < 0: break
        chh = strx[idx]
        if chh != xchar:
            break               
        idx -= 1
    return idx

def shortenstr(xstr, xlen):
    ret = ""; zlen = len(xstr)
    if(zlen > xlen):
        if xlen < 5: raise Valuerror;
        xlen -= 5
        ret = xstr[:xlen / 2] + "..." + xstr[zlen - xlen / 2:]
    else:
        ret = xstr        

    return ret

def handle_keys(host):

    # Do key down:
    if  event.type == gtk.gdk.KEY_PRESS:
        if event.keyval == gtk.keysyms.Alt_L or \
                event.keyval == gtk.keysyms.Alt_R:
            #print "Alt down"
            host.alt = True; 
        elif event.keyval == gtk.keysyms.Control_L or \
                event.keyval == gtk.keysyms.Control_R:
            #print "Ctrl down"
            self.ctrl = True; ret = True
        if event.keyval == gtk.keysyms.Shift_L or \
              event.keyval == gtk.keysyms.Shift_R:
            #print "shift down"
            host.shift = True;

    # Do key up
    elif  event.type == gtk.gdk.KEY_RELEASE:
        if event.keyval == gtk.keysyms.Alt_L or \
              event.keyval == gtk.keysyms.Alt_R:
            #print "Alt up"
            host.alt = False;
        if event.keyval == gtk.keysyms.Control_L or \
              event.keyval == gtk.keysyms.Control_R:
            #print "Ctrl up"
            host.ctrl = False;
        if event.keyval == gtk.keysyms.Shift_L or \
              event.keyval == gtk.keysyms.Shift_R:
            #print "shift up"
            host.shift = False; 
        
# -----------------------------------------------------------------------
# Sleep just a little, but allow the system to breed

def  usleep(msec):

    got_clock = time.clock() + float(msec) / 1000
    #print got_clock
    while True:
        if time.clock() > got_clock:
            break
        gtk.main_iteration_do(False)        
      
# Create a one way hash of a name. Not cryptographically secure,
# but it can make a good unique name in hex.

def hash_name(strx):

    lenx = len(strx);  hashx = int(0)
    for aa in strx:
        bb = ord(aa)
        hashx +=  int((bb << 12) + bb)
        hashx &= 0xffffffff
        hashx = int(hashx << 8) + int(hashx >> 8)
        hashx &= 0xffffffff

    return "%x" % hashx

# Calculate tabs up to till count
def calc_tabs(strx, till, tabstop = 8):
    idx = 0; cnt = 0
    xlen = min(len(strx), till); 
    while True:
        if idx >= xlen: break
        chh = strx[idx]
        if  chh == "\t":
            cnt += tabstop - (cnt % tabstop)
        else:
            cnt += 1
        idx += 1
    return cnt

# Calculate tabs up to till count, include full length
def calc_tabs2(strx, till, tabstop = 8):
    idx = 0; cnt = 0; slen = len(strx)
    xlen = min(slen, till); 
    while True:
        if idx >= xlen: break
        chh = strx[idx]
        if  chh == "\t":
            cnt += tabstop - (cnt % tabstop)
        else:
            cnt += 1
        idx += 1
        
    # Pad full lengh
    if till > slen:
        cnt += till - slen
    return cnt

# Remove up to num leading spaces
def rmlspace(strx, num):
    idx = 0;    xlen = len(strx)
    while True:
        if idx >= xlen:  break
        if strx[idx] != " ": break
        if idx >= num: break
        idx += 1
    return strx[idx:]

# ------------------------------------------------------------------------
# Select word - Return tuple of begin and end index

def  selword(strx, xidx):

    xlen = len(strx); 
    if xlen == 0: return 0, 0        
    if xidx >= xlen: return xlen, xlen
    
    if strx[xidx] == " ":
        return xidx, xidx
        
    cnte = xidx; cntb = xidx
    
    # Find space to end
    while True:
        if cnte >= xlen:    break
        if strx[cnte] == " ":
            break
        cnte += 1
    # Find space to begin
    while True:
        if cntb <= 0:       break
        if strx[cntb] == " ":
            cntb += 1               # Already on space, back off
            break
        cntb -= 1            
        
    return cntb, cnte

# ------------------------------------------------------------------------
# Select an ascii word - Return tuple of begin and end index

def  selasci(strx, xidx, additional = None):

    xlen = len(strx); 
    if xlen == 0: return 0, 0        
    if xidx >= xlen: return xlen, xlen
    if strx[xidx] == " ":
        return xidx, xidx
        
    cnte = xidx; cntb = xidx
    
    # Find space to end
    while True:
        if cnte >= xlen:    break
        if not strx[cnte].isalnum(): # and strx[cnte] != "_":
            break
        cnte += 1
    # Find space to begin
    while True:
        if cntb <= 0:       break
        if not strx[cntb].isalnum(): # and strx[cntb] != "_":
            cntb += 1               # Already on space, back off
            break
        cntb -= 1            
        
    return cntb, cnte
               
# EOF



