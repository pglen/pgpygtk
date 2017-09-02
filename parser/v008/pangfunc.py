#!/usr/bin/env python

import gtk

#import panglib.parser as parser
#import panglib.stack as stack
#import panglib.lexer as lexer
#import panglib.pangodisp as pangodisp

from panglib.utils import *

old_stresc = ""

# Accumulate output: (mostly for testing)
_cummulate = ""

def emit(strx):
    global _cummulate;
    _cummulate += " '" + strx + "' "

def show_debug():
    global _cummulate;
    print _cummulate

# ------------------------------------------------------------------------
# Parser functions that are called on parser events. Note the 'e' prefix
# for the 'end' function -> bold() -> ebold()  (end bold)

def Nbgcol(vparser, token, tentry):
    emit( "<nbgcol> " + vparser.strx[3:len(vparser.strx)-1])
    TextState.bgcolor = vparser.strx[3:len(vparser.strx)-1]
    
def eNbgcol(vparser, token, tentry):
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    TextState.bgcolor = ""
    emit( "<enbgcol> ")
    
def Ncol(vparser, token, tentry):
    emit( "<ncol> " + vparser.strx)
    TextState.color = vparser.strx[1:len(vparser.strx)-1]
    
def Ncol2(vparser, token, tentry):
    emit( "<ncol2> " + vparser.strx)
    TextState.color = vparser.strx[3:len(vparser.strx)-1]
    
def eNcol(vparser, token, tentry):
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    TextState.color = ""
    emit( "<encol> ")
    
def Hid(vparser, token, tentry):
    TextState.hidden = True
    emit( "<hid>")
    
def eHid(vparser, token, tentry):
    TextState.hidden = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<ehid>")

def Indent(vparser, token, tentry):
    TextState.indent += 1
    emit( "<indent>")
    
def eIndent(vparser, token, tentry):
    if TextState.indent > 0:
        TextState.indent -= 1
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<eindent>")

def Margin(vparser, token, tentry):
    TextState.margin += 1
    emit( "<margin>")
    
def eMargin(vparser, token, tentry):
    if TextState.margin > 0:
        TextState.margin -= 1
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<emargin>")
    
def Lmargin(vparser, token, tentry):
    TextState.lmargin += 1
    emit( "<margin>")
    
def eLmargin(vparser, token, tentry):
    if TextState.lmargin > 0:
        TextState.lmargin -= 1
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<emargin>")
    
def Fixed(vparser, token, tentry):
    TextState.fixed = True
    emit( "<fixed>")
    
def eFixed(vparser, token, tentry):
    TextState.fixed = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<efixed>")

def Fill(vparser, token, tentry):
    TextState.fill = True
    emit( "<fill>")
    
def eFill(vparser, token, tentry):
    TextState.fill = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<efill>")

def Sup(vparser, token, tentry):
    TextState.sup = True
    emit( "<sup>")
    
def eSup(vparser, token, tentry):
    TextState.sup = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<esup>")

def Sub(vparser, token, tentry):
    TextState.sub = True
    emit( "<sub>")
    
def eSub(vparser, token, tentry):
    TextState.sub = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<esub>")

def Wrap(vparser, token, tentry):
    TextState.wrap = True
    emit( "<wrap>")
    
def eWrap(vparser, token, tentry):
    TextState.wrap = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<ewrap>")

def Link(vparser, token, tentry):
    emit( "<link>")
    
def Link2(vparser, token, tentry):
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
            fname = docroot + "/" + vv
            if not isfile(fname):
                fname = vv
                if not isfile(fname):
                    fname = "~/" + vv                                                        
                    if not isfile(fname):
                        fname = vv                                                        
                    
            TextState.link = fname                        
        if kk == "color" or kk == "fg":
            #print "setting color in link"
            TextState.color = vv
        
    emit( "<link2>")
    
def eLink(vparser, token, tentry):
    TextState.link = ""
    TextState.color = ""
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<elink>")

def Image(vparser, token, tentry):
    emit( "<image>")

def Image2(vparser, token, tentry):
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
            fname = docroot + "/" + vv
            if not isfile(fname):
                fname = vv
                if not isfile(fname):
                    fname = "~/Pictures" + vv
                    if not isfile(fname):
                        fname = "~/" + vv
        
    # Exec collected stuff
    mainview.add_text_xtag(" ", xtag)
    try:
        pixbuf = gtk.gdk.pixbuf_new_from_file(fname)
        if www and hhh:
            #print "scaling to", www, hhh
            pixbuf2 = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, www, hhh)
            pixbuf.scale(pixbuf2, 0, 0, www, hhh, 
                0, 0, float(www)/pixbuf.get_width(), float(hhh)/pixbuf.get_height(), 
            gtk.gdk.INTERP_BILINEAR)
            mainview.add_pixbuf(pixbuf2)
        else:
            mainview.add_pixbuf(pixbuf)
        
    except gobject.GError, error:
        #print "Failed to load image file '" + vv + "'"
        mainview.add_broken()

    #vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<image2>")
    
def eImage(vparser, token, tentry):
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<eimage>")

def Center(vparser, token, tentry):
    TextState.center = True
    emit( "<center>")
    
def eCenter(vparser, token, tentry):
    TextState.center = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<ecenter>")

def Right(vparser, token, tentry):
    TextState.right = True
    emit( "<right>")
    
def eRight(vparser, token, tentry):
    TextState.right = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<eright>")

def Xsmall(vparser, token, tentry):
    TextState.xsmall = True
    emit( "<xsmall>")
    
def eXsmall(vparser, token, tentry):
    TextState.xsmall = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<exsmall>")

def Small(vparser, token, tentry):
    TextState.small = True
    emit( "<small>")
    
def eSmall(vparser, token, tentry):
    TextState.small = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<esmall>")

def Xxlarge(vparser, token, tentry):
    TextState.xxlarge = True
    emit( "<xxlarge>")
    
def eXxlarge(vparser, token, tentry):
    TextState.xxlarge = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<exxlarge>")

def Xlarge(vparser, token, tentry):
    TextState.xlarge = True
    emit( "<xlarge>")
    
def eXlarge(vparser, token, tentry):
    TextState.xlarge = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<exlarge>")

def Large(vparser, token, tentry):
    TextState.large = True
    emit( "<large>")
    
def eLarge(vparser, token, tentry):
    TextState.large = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<elarge>")

def Dunderline(vparser, token, tentry):
    TextState.dul = True
    emit( "<dunderline>")
    
def eDunderline(vparser, token, tentry):
    TextState.dul = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<edunderline>")
   
def Underline(vparser, token, tentry):
    TextState.ul = True
    emit( "<underline>")
    
def eUnderline(vparser, token, tentry):
    TextState.ul = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<eunderline>")
   
def ItBold(vparser, token, tentry):
    TextState.itbold = True
    emit( "<itbold>")
    
def eItBold(vparser, token, tentry):
    TextState.itbold = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<eitbold>")

def Green(vparser, token, tentry):
    TextState.green = True
    emit( "<green>")
    
def eGreen(vparser, token, tentry):
    TextState.green = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<egreen>")
    
def Blue(vparser, token, tentry):
    TextState.blue = True
    emit( "<blue>")
    
def eBlue(vparser, token, tentry):
    TextState.blue = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<eblue>")
    
def Strike(vparser, token, tentry):
    TextState.strike = True
    emit( "<strike>")
    
def eStrike(vparser, token, tentry):
    TextState.strike = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<estrike>")    
    
def Bgred(vparser, token, tentry):
    TextState.bgred = True
    emit( "<bgred>")
    
def eBgred(vparser, token, tentry):
    TextState.bgred = False
    #    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    vparser.popstate()
    emit( "<ebgred>")
    
def Bggreen(vparser, token, tentry):
    TextState.bggreen = True
    emit( "<bggreen>")
    
def eBggreen(vparser, token, tentry):
    TextState.bggreen = False
    #    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    vparser.popstate()
    emit( "<ebggreen>")

def Bgblue(vparser, token, tentry):
    TextState.bgblue = True
    emit( "<bgblue>")
    
def eBgblue(vparser, token, tentry):
    TextState.bgblue = False
    #    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    vparser.popstate()
    emit( "<ebgblue>")
    
def Red(vparser, token, tentry):
    TextState.red = True
    emit( "<red>")
    
def eRed(vparser, token, tentry):
    TextState.red = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<ered>")
    
def Bold(vparser, token, tentry):
    print "bold called"
    mw = get_mainview2()

    TextState.bold = True
    emit( "<bold>")

def Tab(vparser, token, tentry):
    #print "textstate tab"
    TextState.tab = True
    emit( "<tab>")
    
def eBold(vparser, token, tentry):
    TextState.bold = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<ebold>")
    
def Italic(vparser, token, tentry):
    TextState.italic = True
    emit("<italic>")
    
def eItalic(vparser, token, tentry):
    TextState.italic = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit ( "<eitalic>")
    
def Ident(vparser, token, tentry):
    #print "called ident"
    pass

def Span(vparser, token, tentry):
    emit("<span ");
    pass

def Span2(vparser, token, tentry):
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
            TextState.bgcolor = vv
        if kk == "foreground" or kk == "fg" or kk == "color":
            TextState.color = vv
        elif kk == "size":
            TextState.size = int(vv)
        elif kk == "font":
            TextState.font = vv
        elif kk == "bold":
            if isTrue(vv):
                TextState.bold = True
            else:
                TextState.bold = False
            
        elif kk == "italic":
            if isTrue(vv):
                TextState.italic = True
            else:
                TextState.italic = False

        elif kk == "under" or kk == "underline":
            if isTrue(vv):
                TextState.ul = True
            else:
                TextState.ul = False

        elif kk == "align" or kk == "alignment":
            vvv = vv.lower()
            if vvv == "left":
                TextState.left = True
            elif vvv == "right":
                TextState.right = True
            elif vvv == "center":
                #print " centering"
                TextState.center = True

    emit(" spantxt >");


def eSpan(vparser, token, tentry):
    #print "called span", parser.strx
    TextState.color = ""
    TextState.bgcolor = ""
    TextState.size = 0
    TextState.font = ""
    TextState.left = False
    TextState.center = False
    TextState.right = False
    TextState.ul = False

    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit ("<espan>" )
        
def Keyval(vparser, token, tentry):

    #print "called keyval", vparser.fsm, token, vparser.strx
    
    # Pop two items, create keyval
    fsm, contflag, ttt, stry = vparser.fstack.pop()      # EQ
    fsm2, contflag2, ttt2, stry2 = vparser.fstack.pop()  # Key

    # Push back summed item (reduce)
    vparser.fstack.push([parser.KEYVAL, 1, stry2, vparser.strx])
    vparser.fsm = fsm2

# ------------------------------------------------------------------------
# Text display state:
   
class TextState():

    bold = False;  itbold = False;  italic = False
    ul = False; dul = False
    red = False;  blue = False; green = False
    bgred = False;  bgblue = False; bggreen = False
    strike = False; large = False; small = False; xsmall = False
    xlarge = False; xxlarge = False; center = False
    wrap = False; hidden = False; color =  ""; right = False
    indent = 0; margin = 0; size = 0; font = ""; fixed = False; bgcolor = ""
    sub = False; sup = False; image = ""; link = ""; lmargin = 0
    fill = False; tab = False  
    
def clearTextState():

    TextState.bold = False;  TextState.itbold = False;  TextState.italic = False
    TextState.ul = False; TextState.dul = False
    TextState.red = False;  TextState.blue = False; TextState.green = False
    TextState.bgred = False;  TextState.bgblue = False; TextState.bggreen = False
    TextState.strike = False; TextState.large = False; TextState.small = False; 
    TextState.xsmall = False
    TextState.xlarge = False; TextState.xxlarge = False; TextState.center = False
    TextState.wrap = False; TextState.hidden = False; TextState.color =  ""; 
    TextState.right = False
    TextState.indent = 0; TextState.margin = 0; TextState.size = 0; 
    TextState.font = ""; TextState.fixed = False; TextState.bgcolor = ""
    TextState.sub = False; TextState.sup = False; TextState.image = ""; 
    TextState.link = ""; TextState.lmargin = 0;
    TextState.fill = False
        
def Text(vparser, token, tentry):
    #global mainview
    
    mw = get_mainview2()
    
    #print "Text", vparser.strx
    
    emit(vparser.strx)        
    
    xtag = gtk.TextTag()
    xtag2 = gtk.TextTag()
   
    if TextState.font != "":
        xtag.set_property("font", TextState.font)

    # This is one shot, reset tab
    if  TextState.tab:                
        vparser.strx = "\t" + vparser.strx
        TextState.tab = False  
    
    # Decorate textag according to machine state
    if TextState.fixed:    xtag.set_property("family", "Monospace")
    if TextState.bold:     xtag.set_property("weight", pango.WEIGHT_BOLD)
    if TextState.italic:   xtag.set_property("style", pango.STYLE_ITALIC)
    #if TextState.itbold:   xtag.set_property("foreground", "red")
    if TextState.large:    xtag.set_property("scale", pango.SCALE_LARGE) 
    if TextState.xlarge:   xtag.set_property("scale", pango.SCALE_X_LARGE) 
    if TextState.xxlarge:  xtag.set_property("scale", pango.SCALE_XX_LARGE) 
    if TextState.small:    xtag.set_property("scale", pango.SCALE_SMALL) 
    if TextState.xsmall:    xtag.set_property("scale", pango.SCALE_X_SMALL) 
    if TextState.ul:       xtag.set_property("underline", pango.UNDERLINE_SINGLE)
    if TextState.dul:      xtag.set_property("underline", pango.UNDERLINE_DOUBLE)

    if TextState.red:      xtag.set_property("foreground", "red")
    if TextState.green:    xtag.set_property("foreground", "green")
    if TextState.blue:     xtag.set_property("foreground", "blue")
    
    if TextState.bgred:    xtag.set_property("background", "red")
    if TextState.bggreen:  xtag.set_property("background", "green")
    if TextState.bgblue:   xtag.set_property("background", "blue")
    
    if TextState.strike:   xtag.set_property("strikethrough", True)
    if TextState.wrap:     xtag.set_property("wrap_mode", gtk.WRAP_WORD)

    if TextState.center:   xtag.set_property("justification", gtk.JUSTIFY_CENTER)
    if TextState.right:    xtag.set_property("justification", gtk.JUSTIFY_RIGHT)
    if TextState.fill:     xtag.set_property("justification", gtk.JUSTIFY_FILL)
    
    #print "bgcolor:",  TextState.bgcolor 
    if TextState.bgcolor != "":
        xtag.set_property("background", TextState.bgcolor)

    #print "color:",  TextState.color 
    if TextState.color != "":
        xtag.set_property("foreground", TextState.color)

    if TextState.size != 0:
        xtag.set_property("size", TextState.size * pango.SCALE)

    if TextState.link != "":        
        xtag.set_data("link", TextState.link)
        if TextState.color == "":
            xtag.set_property("foreground", "blue")

    # Sub / Super sets the size again ...
    if TextState.sub:       
        rr = -4; ss = 8
        if TextState.size != 0:
            rr = - TextState.size / 6
            ss  = TextState.size / 2
        xtag.set_property("rise", rr * pango.SCALE)        
        xtag.set_property("size", ss * pango.SCALE)

    if TextState.sup:       
        rr = 6; ss = 8
        if TextState.size != 0:
            rr =  TextState.size / 2
            ss  = TextState.size /2
        xtag.set_property("rise", rr * pango.SCALE)        
        xtag.set_property("size", ss * pango.SCALE)

    # Calculate current indent
    ind = TextState.indent * 32;
    #if TextState.indent > 0:   
    xtag.set_property("indent", ind)
        
    # Calculate current margin
    ind = TextState.margin * 32;
    if TextState.margin > 0:
        xtag.set_property("left_margin", ind)
        xtag.set_property("right_margin", ind)
 
    # Calculate current Left margin
    ind = TextState.lmargin * 32;
    if TextState.lmargin > 0:
        xtag.set_property("left_margin", ind)

    stresc = unescape(vparser.strx)    

    # if wrapping, output one space only
    global old_stresc
    if TextState.wrap:
        if stresc == " ": 
            if old_stresc == " ":                        
                return
            old_stresc = " "
        else:
            old_stresc = ""

    if not TextState.hidden:
        mainview.add_text_xtag(stresc, xtag)
    else:
        print stresc


