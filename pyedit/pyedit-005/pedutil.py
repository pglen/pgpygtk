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

def readfile(strx):

    text = []                  
    if strx != "":
        f = open(strx)
        buff = f.read();
        text = str.split(buff, "\n")
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


