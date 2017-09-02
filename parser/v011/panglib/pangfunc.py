#!/usr/bin/env python

import pygtk, gobject, gtk, pango
import  panglib.stack as stack
import  panglib.parser as parser

from    panglib.utils import *

# Callback class, extraction of callback functions from the pangview parser.
# The class TextState is the format controlling class, Mainview is the target
# window, and the Emit() function is to aid debug. These funtions may also 
# manipulate the parser stack. Note the naming convention like Bold() for 
# bold start, eBold() for bold end.

old_stresc = ""

class CallBack():

    def __init__(self, TextState, Mainview, Emit, Pvg):
        self.TextState = TextState
        self.Mainview = Mainview
        self.emit = Emit
        self.pvg = Pvg

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
            #print   "func", self.pvg.flag
            self.Mainview.add_text_xtag(stresc, xtag, self.pvg.flag)
        else:
            if self.pvg.verbose:
                print "Hidden:", stresc
    
    def Bgred(self, vparser, token, tentry):
        self.TextState.bgred = True
        self.emit( "<bgred>")
        
    def eBgred(self, vparser, token, tentry):
        self.TextState.bgred = False
        #    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        vparser.popstate()
        self.emit( "<ebgred>")
        
    def Bggreen(self, vparser, token, tentry):
        self.TextState.bggreen = True
        self.emit( "<bggreen>")
        
    def eBggreen(self, vparser, token, tentry):
        self.TextState.bggreen = False
        #    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        vparser.popstate()
        self.emit( "<ebggreen>")
    
    def Bgblue(self, vparser, token, tentry):
        self.TextState.bgblue = True
        self.emit( "<bgblue>")
        
    def eBgblue(self, vparser, token, tentry):
        self.TextState.bgblue = False
        #    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        vparser.popstate()
        self.emit( "<ebgblue>")
    
    def Xlarge(self, vparser, token, tentry):
        self.TextState.xlarge = True
        self.emit( "<xlarge>")
        
    def eXlarge(self, vparser, token, tentry):
        self.TextState.xlarge = False
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<exlarge>")
    
    def Large(self, vparser, token, tentry):
        self.TextState.large = True
        self.emit( "<large>")
        
    def eLarge(self, vparser, token, tentry):
        self.TextState.large = False
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<elarge>")
    
    def Dunderline(self, vparser, token, tentry):
        self.TextState.dul = True
        self.emit( "<dunderline>")
        
    def eDunderline(self, vparser, token, tentry):
        self.TextState.dul = False
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<edunderline>")
       
    def Underline(self, vparser, token, tentry):
        self.TextState.ul = True
        self.emit( "<underline>")
        
    def eUnderline(self, vparser, token, tentry):
        self.TextState.ul = False
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<eunderline>")
       
    def ItBold(self, vparser, token, tentry):
        self.TextState.itbold = True
        self.emit( "<itbold>")
        
    def eItBold(self, vparser, token, tentry):
        self.TextState.itbold = False
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<eitbold>")
    
    def Green(self, vparser, token, tentry):
        self.TextState.green = True
        self.emit( "<green>")
        
    def eGreen(self, vparser, token, tentry):
        self.TextState.green = False
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<egreen>")
        
    def Blue(self, vparser, token, tentry):
        self.TextState.blue = True
        self.emit( "<blue>")
        
    def eBlue(self, vparser, token, tentry):
        self.TextState.blue = False
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<eblue>")
        
    def Red(self, vparser, token, tentry):
        self.TextState.red = True
        self.emit( "<red>")
        
    def eRed(self, vparser, token, tentry):
        self.TextState.red = False
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<ered>")
        
    def Center(self, vparser, token, tentry):
        self.TextState.center = True
        self.emit( "<center>")
        
    def eCenter(self, vparser, token, tentry):
        self.TextState.center = False
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<ecenter>")
    
    def Right(self, vparser, token, tentry):
        self.TextState.right = True
        self.emit( "<right>")
        
    def eRight(self, vparser, token, tentry):
        self.TextState.right = False
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<eright>")
    
    def Xsmall(self, vparser, token, tentry):
        self.TextState.xsmall = True
        self.emit( "<xsmall>")
        
    def eXsmall(self, vparser, token, tentry):
        self.TextState.xsmall = False
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<exsmall>")
    
    def Small(self, vparser, token, tentry):
        self.TextState.small = True
        self.emit( "<small>")
        
    def eSmall(self, vparser, token, tentry):
        self.TextState.small = False
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<esmall>")
    
    def Xxlarge(self, vparser, token, tentry):
        self.TextState.xxlarge = True
        self.emit( "<xxlarge>")
        
    def eXxlarge(self, vparser, token, tentry):
        self.TextState.xxlarge = False
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<exxlarge>")
    
    def Margin(self, vparser, token, tentry):
        self.TextState.margin += 1
        self.emit( "<margin>")
        
    def eMargin(self, vparser, token, tentry):
        if self.TextState.margin > 0:
            self.TextState.margin -= 1
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<emargin>")
        
    def Lmargin(self, vparser, token, tentry):
        self.TextState.lmargin += 1
        self.emit( "<margin>")
        
    def eLmargin(self, vparser, token, tentry):
        if self.TextState.lmargin > 0:
            self.TextState.lmargin -= 1
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<emargin>")
        
    def Fixed(self, vparser, token, tentry):
        self.TextState.fixed = True
        self.emit( "<fixed>")
        
    def eFixed(self, vparser, token, tentry):
        self.TextState.fixed = False
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<efixed>")
    
    def Sup(self, vparser, token, tentry):
        self.TextState.sup = True
        self.emit( "<sup>")
        
    def eSup(self, vparser, token, tentry):
        self.TextState.sup = False
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<esup>")
    
    def Sub(self, vparser, token, tentry):
        self.TextState.sub = True
        self.emit( "<sub>")
        
    def eSub(self, vparser, token, tentry):
        self.TextState.sub = False
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<esub>")
    
    def Hid(self, vparser, token, tentry):
        self.TextState.hidden = True
        self.emit( "<hid>")
        
    def eHid(self, vparser, token, tentry):
        self.TextState.hidden = False
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<ehid>")
    
    def Indent(self, vparser, token, tentry):
        self.TextState.indent += 1
        self.emit( "<indent>")
        
    def eIndent(self, vparser, token, tentry):
        if self.TextState.indent > 0:
            self.TextState.indent -= 1
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<eindent>")
    
    def Wrap(self, vparser, token, tentry):
        self.TextState.wrap = True
        self.emit( "<wrap>")
        
    def eWrap(self, vparser, token, tentry):
        self.TextState.wrap = False
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<ewrap>")
    
    def Fill(self, vparser, token, tentry):
        self.TextState.fill = True
        self.emit( "<fill>")
        
    def eFill(self, vparser, token, tentry):
        self.TextState.fill = False
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<efill>")
    
    def Nbgcol(self, vparser, token, tentry):
        self.emit( "<nbgcol> " + vparser.strx[3:len(vparser.strx)-1])
        self.TextState.bgcolor = vparser.strx[3:len(vparser.strx)-1]
        
    def eNbgcol(self, vparser, token, tentry):
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.TextState.bgcolor = ""
        self.emit( "<enbgcol> ")
    
    def Ncol(self, vparser, token, tentry):
        self.emit( "<ncol> " + vparser.strx)
        self.TextState.color = vparser.strx[1:len(vparser.strx)-1]
        
    def Ncol2(self, vparser, token, tentry):
        self.emit( "<ncol2> " + vparser.strx)
        self.TextState.color = vparser.strx[3:len(vparser.strx)-1]
        
    def eNcol(self, vparser, token, tentry):
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.TextState.color = ""
        self.emit( "<encol> ")
    
    def Link(self, vparser, token, tentry):
        self.emit( "<link>")
       
    def Link2(self, vparser, token, tentry):
        xstack = stack.Stack()
        # Walk optionals:
        while True:             
            vparser.popstate()
            if vparser.fsm == parser.KEYVAL:          
                #print " Reducing keyval", fsm, "'"+ttt+"'", "\"" + stry + "\""            
                xstack.push([vparser.ttt, "=", vparser.stry])
            if vparser.contflag == 0:            
                break
    
        while True:
            xkey = xstack.pop()     
            if not xkey:
                break
            kk, ee, vv = xkey;
            vv = vv.replace("\"",""); vv = vv.replace("\'","")
    
            #print "link key: '" + kk + "' val: '" + vv + "'"
            if kk == "file" or kk == "name":
                # Try docroot - current dir - home dir
                fname = self.pvg.docroot + "/" + vv
                if not isfile(fname):
                    fname = vv
                    if not isfile(fname):
                        fname = "~/" + vv                                                        
                        if not isfile(fname):
                            fname = vv                                                        
                        
                self.TextState.link = fname                        
            if kk == "color" or kk == "fg":
                #print "setting color in link"
                self.TextState.color = vv
            
        self.emit( "<link2>")
        
    def eLink(self, vparser, token, tentry):
        self.TextState.link = ""
        self.TextState.color = ""
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<elink>")
    
    def Image(self, vparser, token, tentry):
        self.emit( "<image>")
    
    def Image2(self, vparser, token, tentry):
        xstack = stack.Stack()
        # Walk optionals:
        while True:             
            vparser.popstate()
            if vparser.fsm == parser.KEYVAL:          
                #print " Reducing keyval", fsm, "'"+ttt+"'", "\"" + stry + "\""            
                xstack.push([vparser.ttt, "=", vparser.stry])
            if vparser.contflag == 0:            
                break
    
        xtag = gtk.TextTag();  fname = ""; www = 0; hhh = 0
    
        while True:
            xkey = xstack.pop()     
            if not xkey:
                break
            kk, ee, vv = xkey;
            vv = vv.replace("\"",""); vv = vv.replace("\'","")
    
            #print "key: '" + kk + "' val: '" + vv + "'"
    
            if kk == "align":
                if vv == "left":
                    xtag.set_property("justification", gtk.JUSTIFY_LEFT)
                elif vv == "center":
                    xtag.set_property("justification", gtk.JUSTIFY_CENTER)
                elif vv == "right":
                    xtag.set_property("justification", gtk.JUSTIFY_RIGHT)
    
            if kk == "width":
                www = int(vv)
                
            if kk == "height":
                hhh = int(vv)
                
            if kk == "name" or kk == "file":
                # Try docroot - curr dir - home/Pictures - home
                fname = self.pvg.docroot + "/" + vv
                if not isfile(fname):
                    fname = vv
                    if not isfile(fname):
                        fname = "~/Pictures" + vv
                        if not isfile(fname):
                            fname = "~/" + vv
            
        # Exec collected stuff
        self.Mainview.add_text_xtag(" ", xtag, self.pvg.flag)
        try:
            pixbuf = gtk.gdk.pixbuf_new_from_file(fname)
            if www and hhh:
                #print "scaling to", www, hhh
                pixbuf2 = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, www, hhh)
                pixbuf.scale(pixbuf2, 0, 0, www, hhh, 
                    0, 0, float(www)/pixbuf.get_width(), float(hhh)/pixbuf.get_height(), 
                gtk.gdk.INTERP_BILINEAR)
                self.Mainview.add_pixbuf(pixbuf2, self.pvg.flag)
            else:
                self.Mainview.add_pixbuf(pixbuf, self.pvg.flag)
            
        except gobject.GError, error:
            #print "Failed to load image file '" + vv + "'"
            self.Mainview.add_broken(self.pvg.flag)
                                     
        #vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<image2>")
        
    def eImage(self, vparser, token, tentry):
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit( "<eimage>")
    
    def Span2(self, vparser, token, tentry):
        xstack = stack.Stack()
        # Walk optionals:
        while True:             
            fsm, contflag, ttt, stry = vparser.fstack.pop()
            if fsm == parser.KEYVAL:          
                #print " Reducing keyval", fsm, "'"+ttt+"'", "\"" + stry + "\""            
                xstack.push([ttt, "=", stry])
            if contflag == 0:
                break
        
        # Set font parameters:
        while True:
            xkey = xstack.pop()     
            if not xkey:
                break
            kk, ee, vv = xkey;
            vv = vv.replace("\"",""); vv = vv.replace("\'","")
    
            #print "key ",kk, vv
            if kk == "background" or kk == "bg" or kk == "bgcolor":
                self.TextState.bgcolor = vv
            if kk == "foreground" or kk == "fg" or kk == "color":
                self.TextState.color = vv
            elif kk == "size":
                self.TextState.size = int(vv)
            elif kk == "font":
                self.TextState.font = vv
            elif kk == "bold":
                if isTrue(vv):
                    self.TextState.bold = True
                else:
                    self.TextState.bold = False
                
            elif kk == "italic":
                if isTrue(vv):
                    self.TextState.italic = True
                else:
                    self.TextState.italic = False
    
            elif kk == "under" or kk == "underline":
                if isTrue(vv):
                    self.TextState.ul = True
                else:
                    self.TextState.ul = False
    
            elif kk == "align" or kk == "alignment":
                vvv = vv.lower()
                if vvv == "left":
                    self.TextState.left = True
                elif vvv == "right":
                    self.TextState.right = True
                elif vvv == "center":
                    #print " centering"
                    self.TextState.center = True
    
        self.emit(" spantxt >");
    
    
    def eSpan(self, vparser, token, tentry):
        #print "called span", parser.strx
        self.TextState.color = ""
        self.TextState.bgcolor = ""
        self.TextState.size = 0
        self.TextState.font = ""
        self.TextState.left = False
        self.TextState.center = False
        self.TextState.right = False
        self.TextState.ul = False
    
        vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
        self.emit ("<espan>" )
            
    def Keyval(self, vparser, token, tentry):
    
        #print "called keyval", vparser.fsm, token, vparser.strx
        
        # Pop two items, create keyval
        fsm, contflag, ttt, stry = vparser.fstack.pop()      # EQ
        fsm2, contflag2, ttt2, stry2 = vparser.fstack.pop()  # Key
    
        # Push back summed item (reduce)
        vparser.fstack.push([parser.KEYVAL, 1, stry2, vparser.strx])
        vparser.fsm = fsm2
    

