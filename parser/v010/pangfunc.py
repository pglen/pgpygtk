#!/usr/bin/env python

import pygtk, gobject, gtk, pango
from    panglib.utils import *

# Extracted the trivial functions to here

old_stresc = ""

# Callback class
class CallBack():

    def __init__(self, TextState, Mainview, Emit):
        self.TextState = TextState
        self.Mainview = Mainview
        self.emit = Emit

    def Span(vparser, token, tentry):
        emit("<span ")

    def Tab(self, vparser, token, tentry):
        #print "textstate tab"
        self.TextState.tab = True
        self.emit( "<tab>")
    
    def Strike(self, vparser, token, tentry):
        self.TextState.strike = True
        self.emit( "<strike>")
        
    def eStrike(self, vparser, token, tentry):
        self.TextState.strike = False
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<estrike>")    
                
    def Bold(self, vparser, token, tentry):
        #print "got bold"
        self.TextState.bold = True
        self.emit( "<bold>")
    
    def eBold(self, vparser, token, tentry):
        #print "got ebold"
        self.TextState.bold = False
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<ebold>")
    
    def Italic(self, vparser, token, tentry):
        #print "Got Italic"
        self.TextState.italic = True
        self.emit("<italic>")
    
    def eItalic(self, vparser, token, tentry):
        self.TextState.italic = False
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit ( "<eitalic>")
    
    def Text(self, vparser, token, tentry):
    
        self.emit(vparser.strx)        
        xtag = gtk.TextTag()
        xtag2 = gtk.TextTag()
       
        if self.TextState.font != "":
            xtag.set_property("font", self.TextState.font)
    
        # This is one shot, reset tab
        if  self.TextState.tab:                
            vparser.strx = "\t" + vparser.strx
            self.TextState.tab = False  
        
        # Decorate textag according to machine state
        if self.TextState.fixed:    xtag.set_property("family", "Monospace")
        if self.TextState.bold:     xtag.set_property("weight", pango.WEIGHT_BOLD)
        if self.TextState.italic:   xtag.set_property("style", pango.STYLE_ITALIC)
        #if self.TextState.itbold:   xtag.set_property("foreground", "red")
        if self.TextState.large:    xtag.set_property("scale", pango.SCALE_LARGE) 
        if self.TextState.xlarge:   xtag.set_property("scale", pango.SCALE_X_LARGE) 
        if self.TextState.xxlarge:  xtag.set_property("scale", pango.SCALE_XX_LARGE) 
        if self.TextState.small:    xtag.set_property("scale", pango.SCALE_SMALL) 
        if self.TextState.xsmall:    xtag.set_property("scale", pango.SCALE_X_SMALL) 
        if self.TextState.ul:       xtag.set_property("underline", pango.UNDERLINE_SINGLE)
        if self.TextState.dul:      xtag.set_property("underline", pango.UNDERLINE_DOUBLE)
    
        if self.TextState.red:      xtag.set_property("foreground", "red")
        if self.TextState.green:    xtag.set_property("foreground", "green")
        if self.TextState.blue:     xtag.set_property("foreground", "blue")
        
        if self.TextState.bgred:    xtag.set_property("background", "red")
        if self.TextState.bggreen:  xtag.set_property("background", "green")
        if self.TextState.bgblue:   xtag.set_property("background", "blue")
        
        if self.TextState.strike:   xtag.set_property("strikethrough", True)
        if self.TextState.wrap:     xtag.set_property("wrap_mode", gtk.WRAP_WORD)
    
        if self.TextState.center:   xtag.set_property("justification", gtk.JUSTIFY_CENTER)
        if self.TextState.right:    xtag.set_property("justification", gtk.JUSTIFY_RIGHT)
        if self.TextState.fill:     xtag.set_property("justification", gtk.JUSTIFY_FILL)
        
        #print "bgcolor:",  self.TextState.bgcolor 
        if self.TextState.bgcolor != "":
            xtag.set_property("background", self.TextState.bgcolor)
    
        #print "color:",  self.TextState.color 
        if self.TextState.color != "":
            xtag.set_property("foreground", self.TextState.color)
    
        if self.TextState.size != 0:
            xtag.set_property("size", self.TextState.size * pango.SCALE)
    
        if self.TextState.link != "":        
            xtag.set_data("link", self.TextState.link)
            if self.TextState.color == "":
                xtag.set_property("foreground", "blue")
    
        # Sub / Super sets the size again ...
        if self.TextState.sub:       
            rr = -4; ss = 8
            if self.TextState.size != 0:
                rr = - self.TextState.size / 6
                ss  = self.TextState.size / 2
            xtag.set_property("rise", rr * pango.SCALE)        
            xtag.set_property("size", ss * pango.SCALE)
    
        if self.TextState.sup:       
            rr = 6; ss = 8
            if self.TextState.size != 0:
                rr =  self.TextState.size / 2
                ss  = self.TextState.size /2
            xtag.set_property("rise", rr * pango.SCALE)        
            xtag.set_property("size", ss * pango.SCALE)
    
        # Calculate current indent
        ind = self.TextState.indent * 32;
        #if self.TextState.indent > 0:   
        xtag.set_property("indent", ind)
            
        # Calculate current margin
        ind = self.TextState.margin * 32;
        if self.TextState.margin > 0:
            xtag.set_property("left_margin", ind)
            xtag.set_property("right_margin", ind)
     
        # Calculate current Left margin
        ind = self.TextState.lmargin * 32;
        if self.TextState.lmargin > 0:
            xtag.set_property("left_margin", ind)
    
        stresc = unescape(vparser.strx)    
        
        # If wrapping, output one space only
        global old_stresc
        if self.TextState.wrap:
            if stresc == " ": 
                if old_stresc == " ":                        
                    return
                old_stresc = " "
            else:
                old_stresc = ""
            
        if not self.TextState.hidden:
            self.Mainview.add_text_xtag(stresc, xtag)
        else:
            print stresc
    


