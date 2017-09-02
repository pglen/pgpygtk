#!/usr/bin/env python
 
import sys, os, re
import pygtk, gobject, gtk, pango

# Our modules
import stack, lexer, parser
import pangodisp

# This parser digests formatted text similar to pango in GTK.
# Was created to quickly display formatted messages.
# See SYNTAX for details on text formats

'''
# We initialize parser variables in the context of the parser module.
#
# a.) Token definitions, b.) Lexer tokens, 
# c.) Parser functions,  d.) Parser state, e.) Parse table
#
# To create a custom parser, just add new tokens / states
#

# Quick into: The lexer creates a stack of tokens. The parser scans
# the tokens, and walks the state machine for matches. If match 
# is encountered, the parser calls the function in the state table, 
# and / or changes state. Reduce is called after the state has been 
# successfully digested. For more info see lex / yacc literature.
'''

# Connect parser token to lexer item. This way the definitions
# are synced without the need for double definition

def parse_lookup(strx):
    ret = None
    for aa in parser.tokdef:
        if strx == aa[1]:
            #print "found", aa
            ret = aa
            break
    if ret == None: 
        print "Token '" + strx + "' not found, please correct."
        sys.exit(1)
    return aa

# ------------------------------------------------------------------------
# Token definitions:
# Use textual context [x][1] for development, numeric [x][0] for production  
# The order of the definitions do not matter.
#
# To add a new syntactic element, search for an existing feature (like 'wrap')
# Add the new element into the a.) definition, b.) regex defintion, 
# c.) state definition, d.) state table, c.) action function.
# The script is self checking, will report on missing defintions. However,
# it can not (will not) report on syntactic anomalies.
#

parser.tokdef = \
         [parser.unique(), "span"   ],  \
         [parser.unique(), "espan"],    \
         [parser.unique(), "it"     ],  \
         [parser.unique(), "eit"    ],  \
         [parser.unique(), "bold"   ],  \
         [parser.unique(), "ebold"  ],  \
         [parser.unique(), "itbold" ],  \
         [parser.unique(), "eitbold"],  \
         [parser.unique(), "ul"   ],    \
         [parser.unique(), "eul"  ],    \
         [parser.unique(), "dul"   ],    \
         [parser.unique(), "edul"  ],    \
         [parser.unique(), "ncol"   ],   \
         [parser.unique(), "ncol2"   ],   \
         [parser.unique(), "encol"  ],   \
         [parser.unique(), "nbgcol"   ],  \
         [parser.unique(), "enbgcol"  ],  \
         [parser.unique(), "hid"   ],    \
         [parser.unique(), "ehid"  ],    \
         [parser.unique(), "indent"   ], \
         [parser.unique(), "eindent"  ],  \
         [parser.unique(), "margin"   ], \
         [parser.unique(), "emargin"  ],  \
         [parser.unique(), "wrap"   ],    \
         [parser.unique(), "ewrap"  ],    \
         [parser.unique(), "link"   ],    \
         [parser.unique(), "elink"  ],    \
         [parser.unique(), "image"   ],    \
         [parser.unique(), "eimage"  ],    \
         [parser.unique(), "sub"   ],    \
         [parser.unique(), "esub"  ],    \
         [parser.unique(), "sup"   ],    \
         [parser.unique(), "esup"  ],    \
         [parser.unique(), "fill"   ],    \
         [parser.unique(), "efill"  ],    \
         [parser.unique(), "fixed"   ],    \
         [parser.unique(), "efixed"  ],    \
         [parser.unique(), "cent"   ],    \
         [parser.unique(), "ecent"  ],    \
         [parser.unique(), "right"   ],   \
         [parser.unique(), "eright"  ],   \
         [parser.unique(), "red"   ],     \
         [parser.unique(), "ered"  ],     \
         [parser.unique(), "bgred"   ],   \
         [parser.unique(), "ebgred"  ],   \
         [parser.unique(), "green"   ], \
         [parser.unique(), "egreen"  ], \
         [parser.unique(), "bggreen"   ], \
         [parser.unique(), "ebggreen"  ], \
         [parser.unique(), "blue"   ],  \
         [parser.unique(), "eblue"  ],  \
         [parser.unique(), "bgblue"   ],  \
         [parser.unique(), "ebgblue"  ],  \
         [parser.unique(), "large"   ],  \
         [parser.unique(), "elarge"  ],  \
         [parser.unique(), "xlarge"   ],  \
         [parser.unique(), "exlarge"  ],  \
         [parser.unique(), "xxlarge"   ],  \
         [parser.unique(), "exxlarge"  ],  \
         [parser.unique(), "small"   ],  \
         [parser.unique(), "esmall"  ],  \
         [parser.unique(), "xsmall"   ],  \
         [parser.unique(), "exsmall"  ],  \
         [parser.unique(), "strike"   ],\
         [parser.unique(), "estrike"  ],\
         [parser.unique(), "escquo" ],  \
         [parser.unique(), "dblbs"  ],  \
         [parser.unique(), "ident"  ],  \
         [parser.unique(), "str"    ],  \
         [parser.unique(), "str2"   ],  \
         [parser.unique(), "str3"   ],  \
         [parser.unique(), "eq"     ],  \
         [parser.unique(), "comm"   ],  \
         [parser.unique(), "bsnl"   ],  \
         [parser.unique(), "lt"     ],  \
         [parser.unique(), "gt"     ],  \
         [parser.unique(), "sp"     ],  \
         [parser.unique(), "tab"    ],  \
         [parser.unique(), "nl"     ],  \
         [parser.unique(), "any"    ],  \
         
# ------------------------------------------------------------------------
# Lexer tokens. The lexer will search for the next token. 
# When editing, update tokdef and tokens together. 
#
# The order of the definitions matter. First token match is returned.
#
# Please note for simplicity we defined a stateless lexer. For example,
# the str is delimited by "" and str2 is delimited by '' to allow
# quotes in the str. For more complex string with quotes in it, escape 
# the quotes. (\48)
#
#      --- enum tokdef -- token regex -- placeholder (compiled regex) --

parser.tokens =    \
            [parse_lookup("span"),      "<span "        ,  None  ],  \
            [parse_lookup("espan"),     "</span>"       ,  None, ],  \
            [parse_lookup("it"),        "<i>"           ,  None, ],  \
            [parse_lookup("eit"),       "</i>"          ,  None, ],  \
            [parse_lookup("hid"),       "<hid>"         ,  None, ],  \
            [parse_lookup("ehid"),      "</hid>"        ,  None, ],  \
            [parse_lookup("bold"),      "<b>"           ,  None, ],  \
            [parse_lookup("ebold"),     "</b>"          ,  None, ],  \
            [parse_lookup("itbold"),    "<ib>"          ,  None, ],  \
            [parse_lookup("eitbold"),   "</ib>"         ,  None, ],  \
            [parse_lookup("red"),       "<r>"           ,  None, ],  \
            [parse_lookup("ered"),      "</r>"          ,  None, ],  \
            [parse_lookup("bgred"),      "<rb>"           ,  None, ],  \
            [parse_lookup("ebgred"),      "</rb>"          ,  None, ],  \
            [parse_lookup("indent"),    "<in>"          ,  None, ],  \
            [parse_lookup("eindent"),   "</in>"         ,  None, ],  \
            [parse_lookup("margin"),    "<m>"          ,  None, ],  \
            [parse_lookup("emargin"),   "</m>"         ,  None, ],  \
            [parse_lookup("blue"),      "<e>"           ,  None, ],  \
            [parse_lookup("eblue"),     "</e>"          ,  None, ],  \
            [parse_lookup("bgblue"),    "<eb>"           ,  None, ],  \
            [parse_lookup("ebgblue"),   "</eb>"          ,  None, ],  \
            [parse_lookup("green"),     "<g>"           ,  None, ],  \
            [parse_lookup("egreen"),    "</g>"          ,  None, ],  \
            [parse_lookup("bggreen"),   "<gb>"           ,  None, ],  \
            [parse_lookup("ebggreen"),  "</gb>"          ,  None, ],  \
            [parse_lookup("large"),     "<l>"           ,  None, ],  \
            [parse_lookup("elarge"),    "</l>"          ,  None, ],  \
            [parse_lookup("xlarge"),    "<xl>"          ,  None, ],  \
            [parse_lookup("exlarge"),   "</xl>"         ,  None, ],  \
            [parse_lookup("xxlarge"),   "<xxl>"         ,  None, ],  \
            [parse_lookup("exxlarge"),  "</xxl>"        ,  None, ],  \
            [parse_lookup("small"),     "<m>"           ,  None, ],  \
            [parse_lookup("esmall"),    "</m>"          ,  None, ],  \
            [parse_lookup("xsmall"),    "<xs>"           ,  None, ],  \
            [parse_lookup("exsmall"),   "</xs>"          ,  None, ],  \
            [parse_lookup("cent"),      "<c>"           ,  None, ],  \
            [parse_lookup("ecent"),     "</c>"          ,  None, ],  \
            [parse_lookup("right"),     "<t>"           ,  None, ],  \
            [parse_lookup("eright"),    "</t>"          ,  None, ],  \
            [parse_lookup("strike"),    "<s>"           ,  None, ],  \
            [parse_lookup("estrike"),   "</s>"          ,  None, ],  \
            [parse_lookup("ul"),        "<u>"           ,  None, ],  \
            [parse_lookup("eul"),       "</u>"          ,  None, ],  \
            [parse_lookup("dul"),       "<uu>"          ,  None, ],  \
            [parse_lookup("edul"),      "</uu>"         ,  None, ],  \
            [parse_lookup("wrap"),      "<w>"           ,  None, ],  \
            [parse_lookup("ewrap"),     "</w>"          ,  None, ],  \
            [parse_lookup("link"),      "<link "           ,  None, ],  \
            [parse_lookup("elink"),     "</link>"          ,  None, ],  \
            [parse_lookup("image"),      "<image "           ,  None, ],  \
            [parse_lookup("eimage"),     "</image>"          ,  None, ],  \
            [parse_lookup("sub"),       "<sub>"          ,  None, ],  \
            [parse_lookup("esub"),      "</sub>"         ,  None, ],  \
            [parse_lookup("sup"),       "<sup>"          ,  None, ],  \
            [parse_lookup("esup"),      "</sup>"         ,  None, ],  \
            [parse_lookup("fill"),      "<j>"           ,  None, ],  \
            [parse_lookup("efill"),      "</j>"          ,  None, ],  \
            [parse_lookup("fixed"),      "<f>"          ,  None, ],  \
            [parse_lookup("efixed"),     "</f>"         ,  None, ],  \
            [parse_lookup("nbgcol"),    "<bg#[0-9a-fA-F]+ *>"  ,  None, ],  \
            [parse_lookup("enbgcol"),   "</bg#>"          ,  None, ],  \
            [parse_lookup("ncol2"),      "<fg#[0-9a-fA-F]+ *>"  ,  None, ],  \
            [parse_lookup("ncol"),      "<#[0-9a-fA-F]+ *>"  ,  None, ],  \
            [parse_lookup("encol"),     "</#>"          ,  None, ],  \
            [parse_lookup("escquo"),    r"\\\""         ,  None, ],  \
            [parse_lookup("dblbs"),     r"\\\\"         ,  None, ],  \
            [parse_lookup("ident"),     "[A-Za-z0-9_\./]+" ,  None, ],  \
            [parse_lookup("str3"),      "(\\\\[0-7]+)+"    ,  None, ],  \
            [parse_lookup("str"),       "\".*?\""       ,  None, ],  \
            [parse_lookup("str2"),      "\'.*?\'"       ,  None, ],  \
            [parse_lookup("bsnl"),      "\\\\\n"        ,  None, ],  \
            [parse_lookup("comm"),     "\n##.*"          ,  None, ],  \
            [parse_lookup("eq"),        "="             ,  None, ],  \
            [parse_lookup("lt"),        "<"             ,  None, ],  \
            [parse_lookup("gt"),        ">"             ,  None, ],  \
            [parse_lookup("sp"),        " "             ,  None, ],  \
            [parse_lookup("tab"),       "\t"            ,  None, ],  \
            [parse_lookup("nl"),        "\n"            ,  None, ],  \
            [parse_lookup("any"),       "."             ,  None, ],  \

if len(parser.tokens) != len(parser.tokdef):
    print "Number of token definitions and tokens do not match."
    sys.exit(1)    

# ------------------------------------------------------------------------
# Parser state machine states. The state machine runs through the whole 
# file stepping the rules. The functions may do anything, including reduce.
# Blank reduce may be executed with the state transition to 'REDUCE'
#
# The number is the state, the string is for debugging / analyzing
# Once ready, operate on the numbers for speed.
# The E-states are not used, kept it for extensibility.

parser.IGNORE  = [parser.unique(),  "ignore"],
parser.INIT    = [parser.unique(),  "init"],
parser.SPAN    = [parser.unique(),  "span"],
parser.SPANTXT = [parser.unique(),  "spantxt"],
parser.IDENT   = [parser.unique(),  "ident"],
parser.KEY     = [parser.unique(),  "key"],
parser.VAL     = [parser.unique(),  "val"],
parser.EQ      = [parser.unique(),  "eq"],
parser.KEYVAL  = [parser.unique(),  "keyval"],
parser.ITALIC  = [parser.unique(),  "italic"],
parser.EITALIC = [parser.unique(),  "eitalic"],
parser.BOLD    = [parser.unique(),  "bold"],
parser.EBOLD   = [parser.unique(),  "ebold"],
parser.ITBOLD  = [parser.unique(),  "itbold"],
parser.EITBOLD = [parser.unique(),  "eitbold"],
parser.UL      = [parser.unique(),  "ul"],
parser.EUL     = [parser.unique(),  "eul"],
parser.DUL     = [parser.unique(),  "dul"],
parser.EDUL    = [parser.unique(),  "edul"],
parser.RED     = [parser.unique(),  "red"],
parser.ERED    = [parser.unique(),  "ered"],
parser.BGRED     = [parser.unique(), "bgred"],
parser.EBGRED    = [parser.unique(),  "ebgred"],
parser.GREEN   = [parser.unique(),  "green"],
parser.EGREEN  = [parser.unique(),  "egreen"],
parser.BGGREEN   = [parser.unique(),  "bggreen"],
parser.EBGGREEN  = [parser.unique(),  "ebggreen"],
parser.BLUE    = [parser.unique(),  "blue"],
parser.EBLUE   = [parser.unique(),  "eblue"],
parser.BGBLUE    = [parser.unique(),  "bgblue"],
parser.EBGBLUE   = [parser.unique(),  "ebgblue"],
parser.STRIKE  = [parser.unique(),  "strike"],
parser.ESTRIKE = [parser.unique(),  "estrike"],
parser.LARGE  = [parser.unique(),   "large"],
parser.ELARGE = [parser.unique(),   "elarge"],
parser.XLARGE  = [parser.unique(),  "xlarge"],
parser.EXLARGE = [parser.unique(),  "exlarge"],
parser.XXLARGE  = [parser.unique(), "xlarge"],
parser.EXXLARGE = [parser.unique(), "exlarge"],
parser.SMALL  = [parser.unique(),   "small"],
parser.ESMALL = [parser.unique(),   "esmall"],
parser.XSMALL  = [parser.unique(),   "xsmall"],
parser.EXSMALL = [parser.unique(),   "exsmall"],
parser.CENT  = [parser.unique(),    "cent"],
parser.ECENT = [parser.unique(),    "ecent"],
parser.RIGHT  = [parser.unique(),   "right"],
parser.ERIGHT = [parser.unique(),   "eright"],
parser.WRAP  = [parser.unique(),    "wrap"],
parser.EWRAP = [parser.unique(),    "ewrap"],
parser.LINK  = [parser.unique(),    "link"],
parser.ELINK = [parser.unique(),    "elink"],
parser.IMAGE  = [parser.unique(),    "image"],
parser.EIMAGE = [parser.unique(),    "eimage"],
parser.SUB  = [parser.unique(),     "sup"],
parser.ESUB = [parser.unique(),     "esup"],
parser.SUP  = [parser.unique(),     "sub"],
parser.ESUP = [parser.unique(),     "esub"],
parser.FILL  = [parser.unique(),    "fill"],
parser.EFILL = [parser.unique(),    "efill"],
parser.FIXED  = [parser.unique(),    "fixed"],
parser.EFIXED = [parser.unique(),    "efixed"],
parser.INDENT  = [parser.unique(),  "indent"],
parser.EINDENT = [parser.unique(),  "eindent"],
parser.MARGIN  = [parser.unique(),  "margin"],
parser.EMARGIN = [parser.unique(),  "emargin"],
parser.HID  = [parser.unique(),     "hid"],
parser.EIHID = [parser.unique(),    "ehid"],
parser.NCOL  = [parser.unique(),    "ncol"],
parser.ENCOL = [parser.unique(),    "encol"],
parser.NBGCOL  = [parser.unique(),  "nbgcol"],
parser.ENBNCOL = [parser.unique(),  "enbgcol"],

# ------------------------------------------------------------------------
# State groups for recursion:

# Color instructions: (not used)

STATECOL = [parser.RED, parser.GREEN, parser.BLUE]

# These are states that have recursive actions: 
# (like bold in italic or size in color etc ...) Note specifically, that
# the SPAN state is not in this list, as inside span definitions formatting
# does not make sence. This parser ignores such occurances.

STATEFMT = [parser.INIT,  parser.BOLD, parser.ITALIC, \
            parser.RED, parser.GREEN, parser.BLUE, \
            parser.BGRED, parser.BGGREEN, parser.BGBLUE, \
            parser.UL, parser.DUL, parser.STRIKE, parser.SMALL, \
            parser.NCOL, parser.NBGCOL, \
            parser.XSMALL, parser.LARGE, parser.XLARGE, parser.XXLARGE,\
            parser.SUB, parser.SUP, parser.LINK, \
            parser.CENT, parser.RIGHT, parser.WRAP, parser.FILL, parser.INDENT, \
            parser.SPANTXT, parser.FIXED, parser.MARGIN ]

# ------------------------------------------------------------------------
# Class of tokens for simple alternates:

# This token class is for generic text.
TXTCLASS = "ident", "eq", "lt", "str", "str2", "str3", "gt", "nl", "sp", "tab", "any",

# Accumulate output: (mostly for testing)
_cummulate = ""
def emit(strx):
    global _cummulate;
    _cummulate += " '" + strx + "' "

# Our display object
mainview = None

# Some globals
buf = None; xstack = None; 
pgdebug = False; show_lexer = False; 
          
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
    print "margin", TextState.margin

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
            fname = docroot + "/" + vv
            if not isfile(fname):
                fname = vv
                if not isfile(fname):
                    fname = "~/" + vv
        
            TextState.link = fname                        
        
    emit( "<link2>")
    
def eLink(vparser, token, tentry):
    TextState.link = ""
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<elink>")

def Image(vparser, token, tentry):
    emit( "<image>")

from stat import *

def isfile(fname):

    try:    
        ss = os.stat(fname)
    except:
        return False

    if S_ISREG(ss[ST_MODE]):
        return True
    return False

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
            fname = docroot + "/" + vv
            if not isfile(fname):
                fname = vv
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
    TextState.bold = True
    emit( "<bold>")
    
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
    
def isTrue(strx):
    if strx == "1": return True
    if strx == "0": return False
    if strx.upper() == "TRUE": return True
    if strx.upper() == "FALSE": return False
    return False

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
    sub = False; sup = False; image = ""; link = ""
    fill = False
        
old_stresc = ""

def Text(vparser, token, tentry):
    global mainview
    emit(vparser.strx)        

    xtag = gtk.TextTag()
    xtag2 = gtk.TextTag()

    if TextState.font != "":
        xtag.set_property("font", TextState.font)

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
    
# ------------------------------------------------------------------------
# Parse table.
#
# Specify state machine state, token to see for action or class to see for
# action, function to execute when match encountered, the new parser 
# state when match encountered, continuation flag for reduce. (will 
# reduce until cont flag == 0) See reduce example for key->val.
#
# Alternatives can be specified with multiple lines for the same state.
# New parser state field overrides state set by function. (set to IGNORE)
#
# Parser ignores unmatched entries. 
#    (Bad for languages, good for error free parsing like text parsing)
#
# Parser starts in INIT. Parser skips IGNORE. (in those cases, usually 
# the function sets the new state)
#
# Use textual context for development, numeric for production
#
# This table specifies a grammar for text processing, similar to Pango
#
#     -- State -- StateClass -- Token -- TokenClass -- Function -- newState -- cont. flag
 
parser.parsetable = \
         [ None,    STATEFMT,     "span",     None,   Span,       parser.SPAN, 0 ],       \
         [ None,    STATEFMT,     "bold",     None,   Bold,       parser.BOLD, 0 ],       \
         [ None,    STATEFMT,     "it",       None,   Italic,     parser.ITALIC, 0 ],     \
         [ None,    STATEFMT,     "itbold",   None,   ItBold,     parser.ITBOLD, 0 ],     \
         [ None,    STATEFMT,     "ul",       None,   Underline,  parser.UL, 0 ],         \
         [ None,    STATEFMT,     "dul",      None,   Dunderline, parser.DUL, 0 ],        \
         [ None,    STATEFMT,     "red",      None,   Red,        parser.RED, 0 ],        \
         [ None,    STATEFMT,     "bgred",    None,   Bgred,      parser.BGRED, 0 ],      \
         [ None,    STATEFMT,     "blue",     None,   Blue,       parser.BLUE, 0 ],       \
         [ None,    STATEFMT,     "bgblue",   None,   Bgblue,     parser.BGBLUE, 0 ],     \
         [ None,    STATEFMT,     "green",    None,   Green,      parser.GREEN, 0 ],      \
         [ None,    STATEFMT,     "bggreen",  None,   Bggreen,    parser.BGGREEN, 0 ],      \
         [ None,    STATEFMT,     "strike",   None,   Strike,     parser.STRIKE, 0 ],     \
         [ None,    STATEFMT,     "large",    None,   Large,      parser.LARGE, 0 ],      \
         [ None,    STATEFMT,     "xlarge",   None,   Xlarge,     parser.XLARGE, 0 ],     \
         [ None,    STATEFMT,     "xxlarge",  None,   Xxlarge,    parser.XXLARGE, 0 ],    \
         [ None,    STATEFMT,     "small",    None,   Small,      parser.SMALL, 0 ],      \
         [ None,    STATEFMT,     "xsmall",    None,  Xsmall,     parser.XSMALL, 0 ],     \
         [ None,    STATEFMT,     "cent",     None,   Center,     parser.CENT, 0 ],       \
         [ None,    STATEFMT,     "right",    None,   Right,      parser.RIGHT, 0 ],      \
         [ None,    STATEFMT,     "wrap",     None,   Wrap,       parser.WRAP, 0 ],       \
         [ None,    STATEFMT,     "link",     None,   Link,       parser.LINK, 0 ],       \
         [ None,    STATEFMT,     "image",     None,  Image,      parser.IMAGE, 0 ],       \
         [ None,    STATEFMT,     "sub",     None,    Sub,        parser.SUB, 0 ],        \
         [ None,    STATEFMT,     "sup",     None,    Sup,        parser.SUP, 0 ],        \
         [ None,    STATEFMT,     "fill",     None,   Fill,       parser.FILL, 0 ],       \
         [ None,    STATEFMT,     "fixed",    None,   Fixed,      parser.FIXED, 0 ],       \
         [ None,    STATEFMT,     "indent",   None,   Indent,     parser.INDENT, 0 ],     \
         [ None,    STATEFMT,     "margin",   None,   Margin,     parser.MARGIN, 0 ],     \
         [ None,    STATEFMT,     "hid",      None,   Hid,        parser.HID, 0 ],        \
         [ None,    STATEFMT,     "ncol",     None,   Ncol,       parser.NCOL, 0 ],       \
         [ None,    STATEFMT,     "nbgcol",   None,   Nbgcol,     parser.NBGCOL, 0 ],       \
                                                                                          \
         [ parser.INIT,   None,   None,       TXTCLASS, Text,     parser.IGNORE, 0 ],     \
                                                                                          \
         [ parser.SPAN,   None,   "ident",    None,     None,     parser.KEY, 1 ],        \
         [ parser.KEYVAL, None,   "ident",    None,     Keyval,   parser.KEY, 1 ],        \
         [ parser.KEY,    None,   "eq",       None,     None,     parser.VAL, 1 ],        \
         [ parser.VAL,    None,   "ident",    None,     Keyval,   parser.IGNORE, 0 ],     \
         [ parser.VAL,    None,   "str",      None,     Keyval,   parser.IGNORE, 0 ],     \
         [ parser.VAL,    None,   "str2",     None,     Keyval,   parser.IGNORE, 0 ],     \
         [ parser.SPAN,   None,   "gt",       None,     Span2,    parser.SPANTXT, 0 ],    \
         [ parser.SPAN,   None,   "sp",       None,     None,     parser.IGNORE, 0 ],     \
                                                                                          \
         [ parser.IMAGE,   None,   "ident",    None,     None,     parser.KEY, 1 ],       \
         [ parser.IMAGE,   None,   "gt",       None,     Image2,   parser.IGNORE, 0 ],    \
         [ parser.IMAGE,   None,   "sp",       None,     None,     parser.IGNORE, 0 ],    \
                                                                                          \
         [ parser.LINK,   None,   "ident",    None,     None,     parser.KEY, 1 ],        \
         [ parser.LINK,   None,   "gt",       None,     Link2,    parser.SPANTXT, 0 ],    \
         [ parser.LINK,   None,   "sp",       None,     None,     parser.IGNORE, 0 ],     \
                                                                                          \
         [ parser.SPANTXT, None,  "espan",    None,     eSpan,      parser.INIT, 0 ],     \
         [ parser.SPANTXT, None,  "elink",    None,     eLink,      parser.INIT, 0 ],     \
                                                                                          \
         [ parser.SPANTXT,  None,  "bold",     None,        Bold,   parser.BOLD, 0 ],     \
         [ parser.SPANTXT,  None,  "it",       None,        Italic, parser.ITALIC, 0 ],         \
         [ parser.SPANTXT,  None,  None,       TXTCLASS,    Text,   parser.IGNORE, 0 ],         \
                                                                                                \
         [ parser.ITALIC,   None,  None,       TXTCLASS,    Text,       parser.IGNORE, 0 ],     \
         [ parser.ITALIC,   None,  "eit",      None,        eItalic,    parser.IGNORE, 0 ],     \
                                                                                                \
         [ parser.BOLD,     None,  None,       TXTCLASS,    Text,       parser.IGNORE, 0 ],     \
         [ parser.BOLD,     None,  "ebold",    None,        eBold,      parser.IGNORE, 0 ],     \
                                                                                                \
         [ parser.ITBOLD,   None,   None,       TXTCLASS,   Text,       parser.IGNORE, 0 ],     \
         [ parser.ITBOLD,   None,   "eitbold",  None,       eItBold,    parser.IGNORE, 0 ],     \
                                                                                                \
         [ parser.UL,       None,   None,       TXTCLASS,   Text,         parser.IGNORE, 0 ],   \
         [ parser.UL,       None,  "eul",       None,       eUnderline,   parser.IGNORE, 0 ],   \
                                                                                                \
         [ parser.DUL,       None,   None,       TXTCLASS,   Text,         parser.IGNORE, 0 ],   \
         [ parser.DUL,       None,  "edul",       None,       eDunderline,   parser.IGNORE, 0 ],   \
                                                                                                \
         [ parser.RED,      None,   None,       TXTCLASS,   Text,        parser.IGNORE, 0 ],    \
         [ parser.RED,      None,   "ered",     None,       eRed,        parser.IGNORE, 0 ],    \
                                                                                                \
         [ parser.BGRED,    None,   None,       TXTCLASS,   Text,        parser.IGNORE, 0 ],    \
         [ parser.BGRED,    None,   "ebgred",     None,     eBgred,      parser.IGNORE, 0 ],    \
                                                                                                \
         [ parser.BLUE,     None,    None,       TXTCLASS,  Text,       parser.IGNORE, 0 ],     \
         [ parser.BLUE,     None,   "eblue",     None,      eBlue,       parser.IGNORE, 0 ],    \
                                                                                                \
         [ parser.BGBLUE,     None,    None,       TXTCLASS,  Text,       parser.IGNORE, 0 ],     \
         [ parser.BGBLUE,     None,   "ebgblue",     None,      eBgblue,       parser.IGNORE, 0 ],    \
                                                                                                \
         [ parser.GREEN,    None,    None,       TXTCLASS,  Text,      parser.IGNORE, 0 ],      \
         [ parser.GREEN,    None,   "egreen",     None,     eGreen,    parser.IGNORE, 0 ],      \
                                                                                                \
         [ parser.BGGREEN,    None,    None,       TXTCLASS,  Text,      parser.IGNORE, 0 ],      \
         [ parser.BGGREEN,    None,   "ebggreen",     None,    eBggreen,    parser.IGNORE, 0 ],      \
                                                                                                \
         [ parser.STRIKE,   None,   None,       TXTCLASS,   Text,      parser.IGNORE, 0 ],      \
         [ parser.STRIKE,   None,   "estrike",  None,       eStrike,   parser.IGNORE, 0 ],      \
                                                                                                \
         [ parser.LARGE,    None,   None,       TXTCLASS,   Text,      parser.IGNORE, 0 ],      \
         [ parser.LARGE,    None,   "elarge",    None,      eLarge,    parser.IGNORE, 0 ],      \
                                                                                                \
         [ parser.XLARGE,    None,   None,       TXTCLASS,  Text,      parser.IGNORE, 0 ],      \
         [ parser.XLARGE,    None,   "exlarge",    None,    eXlarge,    parser.IGNORE, 0 ],     \
                                                                                                \
         [ parser.XXLARGE,    None,   None,       TXTCLASS, Text,      parser.IGNORE, 0 ],      \
         [ parser.XXLARGE,    None,   "exxlarge",    None,  eXxlarge,    parser.IGNORE, 0 ],    \
                                                                                                \
         [ parser.SMALL,     None,   None,       TXTCLASS,  Text,      parser.IGNORE, 0 ],      \
         [ parser.SMALL,     None,  "esmall",    None,      eSmall,    parser.IGNORE, 0 ],      \
                                                                                                \
         [ parser.XSMALL,     None,   None,       TXTCLASS,  Text,      parser.IGNORE, 0 ],      \
         [ parser.XSMALL,     None,  "exsmall",    None,     eXsmall,    parser.IGNORE, 0 ],      \
                                                                                                \
         [ parser.CENT,     None,   None,       TXTCLASS,   Text,       parser.IGNORE, 0 ],     \
         [ parser.CENT,     None,  "ecent",    None,        eCenter,     parser.IGNORE, 0 ],    \
                                                                                                \
         [ parser.RIGHT,     None,   None,      TXTCLASS,   Text,       parser.IGNORE, 0 ],     \
         [ parser.RIGHT,     None,  "eright",    None,      eRight,     parser.IGNORE, 0 ],    \
                                                                                                \
         [ parser.WRAP,     None,   None,       TXTCLASS,   Text,       parser.IGNORE, 0 ],     \
         [ parser.WRAP,     None,  "ewrap",    None,        eWrap,      parser.IGNORE, 0 ],     \
                                                                                                \
         [ parser.SUB,     None,   None,       TXTCLASS,   Text,       parser.IGNORE, 0 ],     \
         [ parser.SUB,     None,  "esub",      None,        eSub,      parser.IGNORE, 0 ],     \
                                                                                                \
         [ parser.SUP,     None,   None,       TXTCLASS,   Text,       parser.IGNORE, 0 ],     \
         [ parser.SUP,     None,  "esup",      None,        eSup,      parser.IGNORE, 0 ],     \
                                                                                                \
         [ parser.FILL,     None,   None,       TXTCLASS,   Text,       parser.IGNORE, 0 ],     \
         [ parser.FILL,     None,  "efill",    None,        eFill,      parser.IGNORE, 0 ],     \
                                                                                                \
         [ parser.FIXED,     None,   None,       TXTCLASS,   Text,       parser.IGNORE, 0 ],     \
         [ parser.FIXED,     None,  "efixed",    None,      eFixed,      parser.IGNORE, 0 ],     \
                                                                                                \
         [ parser.INDENT,     None,   None,       TXTCLASS, Text,       parser.IGNORE, 0 ],     \
         [ parser.INDENT,     None,  "eindent",    None,    eIndent,  parser.IGNORE, 0 ],       \
                                                                                                \
         [ parser.MARGIN,     None,   None,       TXTCLASS, Text,       parser.IGNORE, 0 ],     \
         [ parser.MARGIN,     None,  "emargin",    None,    eMargin,  parser.IGNORE, 0 ],       \
                                                                                                \
         [ parser.HID,     None,   None,       TXTCLASS,    None,     parser.IGNORE, 0 ],       \
         [ parser.HID,     None,  "ehid",    None,          eHid,     parser.IGNORE, 0 ],       \
                                                                                                \
         [ parser.NCOL,     None,   None,     TXTCLASS,     Text,      parser.IGNORE, 0 ],      \
         [ parser.NCOL,     None,  "encol",    None,        eNcol,    parser.IGNORE, 0 ],       \
                                                                                                \
         [ parser.NBGCOL,     None,   None,     TXTCLASS,     Text,      parser.IGNORE, 0 ],    \
         [ parser.NBGCOL,     None,  "enbgcol",    None,      eNbgcol,    parser.IGNORE, 0 ],   \
         
# Check parse table:
for aa in parser.parsetable:
    if aa[2]:
        found = 0
        for bb in parser.tokdef:
            if aa[2] == bb[1]:
                found = True
        if not found :
            print "Parse table contains unkown definition '" + aa[2] + "'"
            sys.exit(1)

def main():
    gtk.main()
    return 0

# ------------------------------------------------------------------------
# Convert unicode sequence to unicode char
     
def uni(xtab):

    #print str.format("{0:b}",  xtab[0])

    cc = 0
    try:                        
        if xtab[0] & 0xe0 == 0xc0:  # two numbers
            cc = (xtab[0] & 0x1f) << 6 
            cc += (xtab[1] & 0x3f)                       
        elif xtab[0] & 0xf0 == 0xe0: # three numbers
            cc = (xtab[0] & 0x0f) << 12 
            cc += (xtab[1] & 0x3f) << 6
            cc += (xtab[2] & 0x3f)                                              
        elif xtab[0] & 0xf8 == 0xf0: # four numbers
            cc = (xtab[0] & 0x0e)  << 18 
            cc += (xtab[1] & 0x3f) << 12
            cc += (xtab[2] & 0x3f) << 6                                             
            cc += (xtab[3] & 0x3f)                                              
        elif xtab[0] & 0xfc == 0xf8: # five numbers
            cc = (xtab[0] & 0x03)  << 24
            cc += (xtab[1] & 0x3f) << 18
            cc += (xtab[2] & 0x3f) << 12                                            
            cc += (xtab[3] & 0x3f) << 6                                             
            cc += (xtab[4] & 0x3f)                                              
        elif xtab[0] & 0xfe == 0xf8: # six numbers
            cc = (xtab[0] & 0x01)  << 30
            cc += (xtab[1] & 0x3f) << 24
            cc += (xtab[2] & 0x3f) << 18
            cc += (xtab[3] & 0x3f) << 12                                            
            cc += (xtab[4] & 0x3f) << 6                                             
            cc += (xtab[5] & 0x3f)                                              

        ccc = unichr(cc)
    except:
        pass

    return ccc

# ------------------------------------------------------------------------

xtab = []; xtablen = 0

def unescape(strx):
   
    #print " x[" + strx + "]x "

    global xtab, xtablen
    retx = u""; pos = 0; lenx = len(strx)
        
    while True:
        if pos >= lenx:
            break

        chh = strx[pos]

        if(chh == '\\'):
            #print "backslash", strx[pos:]
            pos2 = pos + 1; strx2 = ""
            while True:
                if pos2 >= lenx:                   
                    # See if we accumulated anything
                    if strx2 != "":
                        xtab.append(oct2int(strx2))                        
                    if len(xtab) > 0:
                        #print "final:", xtab
                        if xtablen == len(xtab):                       
                            retx += uni(xtab)                                
                            xtab = []; xtablen = 0         
                    pos = pos2 - 1
                    break
                chh2 = strx[pos2]
                if chh2  >= "0" and chh2 <= "7":
                    strx2 += chh2
                else:
                    #print "strx2: '"  + strx2 + "'"
                    if strx2 != "":
                        octx = oct2int(strx2)
                        if xtablen == 0:                       
                            if octx & 0xe0 == 0xc0:
                                #print "two ",str.format("{0:b}", octx)
                                xtablen = 2
                                xtab.append(octx)
                            elif octx & 0xf0 == 0xe0: # three numbers
                                #print "three ",str.format("{0:b}", octx)
                                xtablen = 3
                                xtab.append(octx)
                            elif octx & 0xf8 == 0xf0: # four numbers
                                print "four ",str.format("{0:b}", octx)
                                xtablen = 4
                                xtab.append(octx)
                            elif octx & 0xfc == 0xf8: # five numbers
                                print "five ",str.format("{0:b}", octx)
                                xtablen = 5
                                xtab.append(octx)
                            elif octx & 0xfe == 0xfc: # six numbers
                                print "six ",str.format("{0:b}", octx)
                                xtablen = 6
                                xtab.append(octx)
                            else:
                                #print "other ",str.format("{0:b}", octx)
                                retx += unichr(octx)
                        else:
                            xtab.append(octx)
                            #print "data ",str.format("{0:b}", octx)
                            if xtablen == len(xtab):                       
                                retx += uni(xtab)                                
                                xtab = []; xtablen = 0                        

                    pos = pos2 - 1
                    break
                pos2 += 1
        else:

            if xtablen == len(xtab) and xtablen != 0:                       
                retx += uni(xtab)                                
            xtab=[]; xtablen = 0

            retx += chh        
        pos += 1

    #print "y[" + retx + "]y"
    return retx

fullpath = None
docroot = None

def link(strx):

    print "linking to:", strx
    showfile(strx)

# ------------------------------------------------------------------------
  
def showfile(strx):

    global buf, xstack, mainview

    try:
        f = open(strx)
    except:
        strerr = "File:  '" + strx + "'  must be an existing and readble file.\n";  
        print strerr
        mainview.add_text(strerr)
        return
    
    try:
        buf = f.read();
    except:
        strerr2 =  "Cannot read file '" + strx + "'"
        print strerr2
        mainview.add_text(strerr2)        
        return

    f.close()

    if pgdebug > 5: print buf
    mainview.clear()

    xstack = stack.Stack()       
    lexer.Lexer(buf, xstack, parser.tokens)
    
    if show_lexer: xstack.dump() # To show what the lexer did
  
    parser.Parse(buf, xstack)
  
    # Output results (to show workings)
    if pgdebug > 6: print _cummulate
    
# ------------------------------------------------------------------------

pgdebug = False

# ------------------------------------------------------------------------
# Convert octal string to integer

def oct2int(strx):
    retx = 0
    for aa in strx:
        num = ord(aa) - ord("0")
        if num > 7 or num < 0: 
            break    
        retx <<= 3; retx += num       
    #print "oct:", strx, "int:", retx
    return retx

# ------------------------------------------------------------------------

if __name__ == "__main__":

    import getopt
    
    opts = []; args = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:vhx")
    except getopt.GetoptError, err:
        print "Invalid option(s) on command line:", err
        sys.exit(1)

    #print "opts", opts, "args", args
    
    for aa in opts:
        if aa[0] == "-d":
            try:
                pgdebug = int(aa[1])
            except:
                pgdebug = 0

        if aa[0] == "-v":
            print "Verbose"

        if aa[0] == "-h":
            print "Help"

        if aa[0] == "-x":
            print "Show Lexer"
            show_lexer = True

    try:
        strx = args[0]
    except:
        print "Usage: " + sys.argv[0] + " [options] filename"
        print "Options are:"
        print "            -d level  - Debug level (1-10)"
        print "            -v        - Verbose"
        print "            -x        - show lexer output"
        print "            -h        - Help"
        print

        exit(1);

    fullpath = os.path.abspath(strx);
    docroot = os.path.dirname(fullpath)    
    #print "docroot:", docroot

    mainview = pangodisp.PangoView()
    mainview.callback = link

    showfile(strx)
 
    main()
  
