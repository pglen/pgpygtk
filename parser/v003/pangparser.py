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
         [parser.unique(), "indent"   ],    \
         [parser.unique(), "eindent"  ],    \
         [parser.unique(), "wrap"   ],    \
         [parser.unique(), "ewrap"  ],    \
         [parser.unique(), "cent"   ],    \
         [parser.unique(), "ecent"  ],    \
         [parser.unique(), "red"   ],   \
         [parser.unique(), "ered"  ],   \
         [parser.unique(), "green"   ], \
         [parser.unique(), "blue"   ],  \
         [parser.unique(), "eblue"  ],  \
         [parser.unique(), "large"   ],  \
         [parser.unique(), "elarge"  ],  \
         [parser.unique(), "xlarge"   ],  \
         [parser.unique(), "exlarge"  ],  \
         [parser.unique(), "xxlarge"   ],  \
         [parser.unique(), "exxlarge"  ],  \
         [parser.unique(), "small"   ],  \
         [parser.unique(), "esmall"  ],  \
         [parser.unique(), "egreen"  ], \
         [parser.unique(), "strike"   ],\
         [parser.unique(), "estrike"  ],\
         [parser.unique(), "escquo" ],  \
         [parser.unique(), "dblbs"  ],  \
         [parser.unique(), "ident"  ],  \
         [parser.unique(), "str"    ],  \
         [parser.unique(), "str2"   ],  \
         [parser.unique(), "eq"     ],  \
         [parser.unique(), "bsnl"   ],  \
         [parser.unique(), "lt"     ],  \
         [parser.unique(), "gt"     ],  \
         [parser.unique(), "sp"     ],  \
         [parser.unique(), "tab"    ],  \
         [parser.unique(), "nl"     ],  \
         [parser.unique(), "any"    ],  \
         
# ------------------------------------------------------------------------
# Lexer tokens. The lexer will search for the next token. Update tokdef 
# and tokens together. The order of the definitions matter. First token
# match is returned.
#
#         --- enum tokdef -- token regex -- placeholder (compiled regex) --

parser.tokens =    \
            [parse_lookup("span"),      "<span "        ,  None  ], \
            [parse_lookup("espan"),     "</span>"       ,  None, ],  \
            [parse_lookup("it"),        "<i>"           ,  None, ],  \
            [parse_lookup("eit"),       "</i>"          ,  None, ],  \
            [parse_lookup("bold"),      "<b>"           ,  None, ],  \
            [parse_lookup("ebold"),     "</b>"          ,  None, ],  \
            [parse_lookup("itbold"),    "<ib>"          ,  None, ],  \
            [parse_lookup("eitbold"),   "</ib>"         ,  None, ],  \
            [parse_lookup("red"),       "<r>"           ,  None, ],  \
            [parse_lookup("ered"),      "</r>"          ,  None, ],  \
            [parse_lookup("indent"),    "<in>"           ,  None, ],  \
            [parse_lookup("eindent"),   "</in>"          ,  None, ],  \
            [parse_lookup("blue"),      "<e>"           ,  None, ],  \
            [parse_lookup("eblue"),     "</e>"          ,  None, ],  \
            [parse_lookup("green"),     "<g>"           ,  None, ],  \
            [parse_lookup("egreen"),    "</g>"          ,  None, ],  \
            [parse_lookup("large"),     "<l>"           ,  None, ],  \
            [parse_lookup("elarge"),    "</l>"          ,  None, ],  \
            [parse_lookup("xlarge"),    "<xl>"           ,  None, ],  \
            [parse_lookup("exlarge"),   "</xl>"          ,  None, ],  \
            [parse_lookup("xxlarge"),    "<xxl>"           ,  None, ],  \
            [parse_lookup("exxlarge"),   "</xxl>"          ,  None, ],  \
            [parse_lookup("small"),     "<m>"           ,  None, ],  \
            [parse_lookup("esmall"),    "</m>"          ,  None, ],  \
            [parse_lookup("cent"),     "<c>"           ,  None, ],  \
            [parse_lookup("ecent"),    "</c>"          ,  None, ],  \
            [parse_lookup("strike"),    "<s>"           ,  None, ],  \
            [parse_lookup("estrike"),   "</s>"          ,  None, ],  \
            [parse_lookup("ul"),        "<u>"           ,  None, ],  \
            [parse_lookup("eul"),       "</u>"          ,  None, ],  \
            [parse_lookup("wrap"),      "<w>"           ,  None, ],  \
            [parse_lookup("ewrap"),     "</w>"          ,  None, ],  \
            [parse_lookup("escquo"),    r"\\\""         ,  None, ],  \
            [parse_lookup("dblbs"),     r"\\\\"         ,  None, ],  \
            [parse_lookup("ident"),     "[A-Za-z0-0_]+" ,  None, ],  \
            [parse_lookup("str"),       "\".*?\""       ,  None, ],  \
            [parse_lookup("str2"),      "\'.*?\'"       ,  None, ],  \
            [parse_lookup("bsnl"),      "\\\\\n"        ,  None, ],  \
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
# Once ready, operate on the numbers for speed

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
parser.RED     = [parser.unique(),  "red"],
parser.ERED    = [parser.unique(),  "ered"],
parser.GREEN   = [parser.unique(),  "green"],
parser.EGREEN  = [parser.unique(),  "egreen"],
parser.BLUE    = [parser.unique(),  "blue"],
parser.EBLUE   = [parser.unique(),  "eblue"],
parser.STRIKE  = [parser.unique(),  "strike"],
parser.ESTRIKE = [parser.unique(),  "estrike"],
parser.LARGE  = [parser.unique(),   "large"],
parser.ELARGE = [parser.unique(),   "elarge"],
parser.XLARGE  = [parser.unique(),   "xlarge"],
parser.EXLARGE = [parser.unique(),   "exlarge"],
parser.XXLARGE  = [parser.unique(),   "xlarge"],
parser.EXXLARGE = [parser.unique(),   "exlarge"],
parser.SMALL  = [parser.unique(),   "small"],
parser.ESMALL = [parser.unique(),   "esmall"],
parser.CENT  = [parser.unique(),   "cent"],
parser.ECENT = [parser.unique(),   "ecent"],
parser.WRAP  = [parser.unique(),   "wrap"],
parser.EWRAP = [parser.unique(),   "ewrap"],
parser.INDENT  = [parser.unique(),   "indent"],
parser.EINDENT = [parser.unique(),   "eindent"],

# State groups for recursion:

STATECOL = [parser.RED, parser.GREEN, parser.BLUE]

# These are states that have recursive actions: (like bold in italic)
# or size in color etc...

STATEFMT = [parser.INIT, parser.RED, parser.GREEN, parser.BLUE, parser.BOLD,\
            parser.ITALIC, parser.UL, parser.STRIKE, parser.SMALL, \
            parser.LARGE, parser.XLARGE, parser.XXLARGE, parser.CENT, \
            parser.WRAP, parser.INDENT]

# ------------------------------------------------------------------------
# Class of tokens for simple alternates:

# This class is for generic text.
TXTCLASS = "ident", "eq", "lt", "str", "str2", "gt", "nl", "sp", "any",

# Accumulate output:
_cummulate = ""
def emit(strx):
    global _cummulate;
    _cummulate += " '" + strx + "' "

# Our display object
mainview = None
                  
# ------------------------------------------------------------------------
# Parser functions that are called on parser events. Note the 'e' prefix
# for the 'end' function -> bold -> endbold

def Indent(vparser, token, tentry):
    Textstate.indent += 1
    emit( "<indent>")
    
def eIndent(vparser, token, tentry):
    if Textstate.indent > 0:
        Textstate.indent -= 1
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<eindent>")

def Wrap(vparser, token, tentry):
    Textstate.wrap = True
    emit( "<wrap>")
    
def eWrap(vparser, token, tentry):
    Textstate.wrap = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<ewrap>")

def Center(vparser, token, tentry):
    Textstate.center = True
    emit( "<center>")
    
def eCenter(vparser, token, tentry):
    Textstate.center = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<ecenter>")

def Small(vparser, token, tentry):
    Textstate.small = True
    emit( "<small>")
    
def eSmall(vparser, token, tentry):
    Textstate.small = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<esmall>")

def Xxlarge(vparser, token, tentry):
    Textstate.xxlarge = True
    emit( "<xxlarge>")
    
def eXxlarge(vparser, token, tentry):
    Textstate.xxlarge = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<exxlarge>")

def Xlarge(vparser, token, tentry):
    Textstate.xlarge = True
    emit( "<xlarge>")
    
def eXlarge(vparser, token, tentry):
    Textstate.xlarge = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<exlarge>")

def Large(vparser, token, tentry):
    Textstate.large = True
    emit( "<large>")
    
def eLarge(vparser, token, tentry):
    Textstate.large = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<elarge>")

def Underline(vparser, token, tentry):
    Textstate.ul = True
    emit( "<underline>")
    
def eUnderline(vparser, token, tentry):
    Textstate.ul = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<eunderline>")
   
def ItBold(vparser, token, tentry):
    Textstate.itbold = True
    emit( "<itbold>")
    
def eItBold(vparser, token, tentry):
    Textstate.itbold = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<eitbold>")

def Green(vparser, token, tentry):
    Textstate.green = True
    emit( "<green>")
    
def eGreen(vparser, token, tentry):
    Textstate.green = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<egreen>")
    
def Blue(vparser, token, tentry):
    Textstate.blue = True
    emit( "<blue>")
    
def eBlue(vparser, token, tentry):
    Textstate.blue = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<eblue>")
    
def Strike(vparser, token, tentry):
    Textstate.strike = True
    emit( "<strike>")
    
def eStrike(vparser, token, tentry):
    Textstate.strike = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<estrike>")    
    
def Red(vparser, token, tentry):
    Textstate.red = True
    emit( "<red>")
    
def eRed(vparser, token, tentry):
    Textstate.red = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<ered>")
    
def Bold(vparser, token, tentry):
    Textstate.bold = True
    emit( "<bold>")
    
def eBold(vparser, token, tentry):
    Textstate.bold = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit( "<ebold>")
    
def Italic(vparser, token, tentry):
    Textstate.italic = True
    emit("<italic>")
    
def eItalic(vparser, token, tentry):
    Textstate.italic = False
    vparser.fsm, vparser.contflag, ttt, vparser.stry = vparser.fstack.pop()
    emit ( "<eitalic>")
    
def Ident(vparser, token, tentry):
    #print "called ident"
    pass

def Span(vparser, token, tentry):

    #print "called span", parser.strx
    xstack = stack.Stack()

    if vparser.fsm == parser.KEYVAL:
        print " Reducing keyval", fsm, "'"+ttt+"'", "\"" + stry + "\""            
        xstack.push(["aa", "=", vparser.strx])
     
    # Walk optionals:
    while True:             
        fsm, contflag, ttt, stry = vparser.fstack.pop()
        if fsm == parser.KEYVAL:          
            print " Reducing keyval", fsm, "'"+ttt+"'", "\"" + stry + "\""            
            xstack.push([ttt, "=", stry])
        if contflag == 0:
            break
    
    # Emit final
    emit("<span ");
    while True:
        strx = xstack.pop()     
        if not strx:
            break
        stry = "" 
        for aa in strx: stry += " '" + aa + "' " # collapse to str
        emit(stry)

    vparser.fsm = parser.SPANTXT
    #emit (" ")  
    emit (">\n" )

def eSpan(parser, token, tentry):
    emit ("<espan>" )
        
def Keyval(vparser, token, tentry):

    #print "called keyval", parser.fsm, token, parser.strx
    
    # Pop two items, create keyval
    fsm, contflag, ttt, stry = vparser.fstack.pop()      # EQ
    fsm2, contflag2, ttt2, stry2 = vparser.fstack.pop()  # Key

    # Push back summed item (reduce)
    vparser.fstack.push([parser.KEYVAL, 1, stry2, vparser.strx])
    vparser.fsm = fsm2

# ------------------------------------------------------------------------
# Text display state:
   
class Textstate():
    bold = False;  itbold = False;  italic = False
    ul = False
    red = False;  blue = False; green = False
    strike = False; large = False; small = False
    xlarge = False; xxlarge = False; center = False
    wrap = False; 
    indent = 0

# Stack for text states, make initial
#textstates = stack.Stack()
#textstates.push(Textstate())
        
def Text(vparser, token, tentry):
    global mainview
    emit(vparser.strx)        

    xtag = gtk.TextTag()

    # Decorate textag according to machine state
    if Textstate.bold:     xtag.set_property("weight", pango.WEIGHT_BOLD)
    if Textstate.italic:   xtag.set_property("style", pango.STYLE_ITALIC)
    if Textstate.itbold:   xtag.set_property("foreground", "red")
    if Textstate.large:    xtag.set_property("scale", pango.SCALE_LARGE) 
    if Textstate.xlarge:   xtag.set_property("scale", pango.SCALE_X_LARGE) 
    if Textstate.xxlarge:  xtag.set_property("scale", pango.SCALE_XX_LARGE) 
    if Textstate.small:    xtag.set_property("scale", pango.SCALE_SMALL) 
    if Textstate.ul:       xtag.set_property("underline", pango.UNDERLINE_SINGLE)
    if Textstate.red:      xtag.set_property("foreground", "red")
    if Textstate.green:    xtag.set_property("foreground", "green")
    if Textstate.blue:     xtag.set_property("foreground", "blue")
    if Textstate.strike:   xtag.set_property("strikethrough", True)
    if Textstate.center:   xtag.set_property("justification", gtk.JUSTIFY_CENTER)
    if Textstate.wrap:     xtag.set_property("wrap_mode", gtk.WRAP_WORD)
 
    cnt = 0; ind = 48
    while True:   
        if Textstate.indent > cnt:   
            xtag.set_property("indent", ind)
            ind += 32; cnt += 1
        else:
            break

    mainview.add_text_xtag(vparser.strx, xtag)
    
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
#     --- state --- token --- class --- function --- new state --- cont flag
 
parser.parsetable = \
         [ parser.INIT, None,   "span",     None,   None,       parser.SPAN, 0 ],       \
         [ None,  STATEFMT,     "bold",     None,   Bold,       parser.BOLD, 0 ],       \
         [ None,  STATEFMT,     "it",       None,   Italic,     parser.ITALIC, 0 ],     \
         [ None,  STATEFMT,     "itbold",   None,   ItBold,     parser.ITBOLD, 0 ],     \
         [ None,  STATEFMT,     "ul",       None,   Underline,  parser.UL, 0 ],         \
         [ None,  STATEFMT,     "red",      None,   Red,        parser.RED, 0 ],        \
         [ None,  STATEFMT,     "blue",     None,   Blue,       parser.BLUE, 0 ],       \
         [ None,  STATEFMT,     "green",    None,   Green,      parser.GREEN, 0 ],      \
         [ None,  STATEFMT,     "strike",   None,   Strike,     parser.STRIKE, 0 ],      \
         [ None,  STATEFMT,     "large",    None,   Large,      parser.LARGE, 0 ],      \
         [ None,  STATEFMT,     "xlarge",   None,   Xlarge,     parser.XLARGE, 0 ],      \
         [ None,  STATEFMT,     "xxlarge",  None,   Xxlarge,    parser.XXLARGE, 0 ],      \
         [ None,  STATEFMT,     "small",    None,   Small,      parser.SMALL, 0 ],      \
         [ None,  STATEFMT,     "cent",     None,   Center,     parser.CENT, 0 ],      \
         [ None,  STATEFMT,     "wrap",     None,   Wrap,       parser.WRAP, 0 ],      \
         [ None,  STATEFMT,     "indent",   None,   Indent,     parser.INDENT, 0 ],      \
                                                                                            \
         [ parser.INIT,   None,   None,      TXTCLASS,   Text,       parser.IGNORE, 0 ],     \
                                                                                            \
         [ parser.SPAN,   None,   "ident",    None,     None,       parser.KEY, 1 ],        \
         [ parser.KEY,    None,   "eq",       None,     None,       parser.VAL, 1 ],        \
         [ parser.VAL,    None,   "ident",    None,           Keyval,     parser.IGNORE, 0 ],     \
         [ parser.VAL,    None,   "str",      None,           Keyval,     parser.IGNORE, 0 ],     \
         [ parser.SPAN,   None,   "gt",       None,           Span,       parser.IGNORE, 0 ],     \
         [ parser.SPAN,   None,   "sp",       None,           Span,       parser.IGNORE, 0 ],     \
                                                                                            \
         [ parser.SPANTXT,  None,  "bold",     None,           Bold,       parser.BOLD, 0 ],       \
         [ parser.SPANTXT,  None,  "it",       None,           Italic,     parser.ITALIC, 0 ],     \
         [ parser.SPANTXT,  None,  None,       TXTCLASS,       Text,       parser.IGNORE, 0 ],     \
         [ parser.SPANTXT,  None,  "espan",    None,           eSpan,      parser.IGNORE, 0 ],     \
                                                                                            \
         [ parser.ITALIC,   None,  None,       TXTCLASS,       Text,       parser.IGNORE, 0 ],     \
         [ parser.ITALIC,   None,  "eit",      None,           eItalic,    parser.IGNORE, 0 ],     \
                                                                                            \
         [ parser.BOLD,     None,  None,       TXTCLASS,       Text,       parser.IGNORE, 0 ],     \
         [ parser.BOLD,     None,  "ebold",    None,           eBold,      parser.IGNORE, 0 ],     \
                                                                                            \
         [ parser.ITBOLD,   None,   None,       TXTCLASS,     Text,       parser.IGNORE, 0 ],     \
         [ parser.ITBOLD,   None,   "eitbold",  None,         eItBold,   parser.IGNORE, 0 ],     \
                                                                                            \
         [ parser.UL,       None,   None,       TXTCLASS,       Text,         parser.IGNORE, 0 ],    \
         [ parser.UL,       None,  "eul",       None,           eUnderline,   parser.IGNORE, 0 ],    \
                                                                                            \
         [ parser.RED,      None,   None,       TXTCLASS,       Text,        parser.IGNORE, 0 ],    \
         [ parser.RED,      None,   "ered",     None,          eRed,        parser.IGNORE, 0 ],    \
                                                                                            \
         [ parser.BLUE,     None,    None,       TXTCLASS,       Text,       parser.IGNORE, 0 ],    \
         [ parser.BLUE,     None,   "eblue",     None,         eBlue,       parser.IGNORE, 0 ],    \
                                                                                            \
         [ parser.GREEN,    None,    None,       TXTCLASS,       Text,      parser.IGNORE, 0 ],    \
         [ parser.GREEN,    None,   "egreen",     None,         eGreen,    parser.IGNORE, 0 ],    \
                                                                                            \
         [ parser.STRIKE,   None,   None,       TXTCLASS,      Text,      parser.IGNORE, 0 ],    \
         [ parser.STRIKE,   None,   "estrike",  None,       eStrike,   parser.IGNORE, 0 ],    \
                                                                                            \
         [ parser.LARGE,    None,   None,       TXTCLASS,       Text,      parser.IGNORE, 0 ],    \
         [ parser.LARGE,    None,   "elarge",    None,           eLarge,    parser.IGNORE, 0 ],    \
                                                                                            \
         [ parser.XLARGE,    None,   None,       TXTCLASS,       Text,      parser.IGNORE, 0 ],    \
         [ parser.XLARGE,    None,   "exlarge",    None,         eXlarge,    parser.IGNORE, 0 ],    \
                                                                                            \
         [ parser.XXLARGE,    None,   None,       TXTCLASS,       Text,      parser.IGNORE, 0 ],    \
         [ parser.XXLARGE,    None,   "exxlarge",    None,         eXxlarge,    parser.IGNORE, 0 ],    \
                                                                                            \
         [ parser.SMALL,     None,   None,       TXTCLASS,       Text,      parser.IGNORE, 0 ],    \
         [ parser.SMALL,     None,  "esmall",    None,           eSmall,    parser.IGNORE, 0 ],     \
                                                                                                \
         [ parser.CENT,     None,   None,       TXTCLASS,       Text,       parser.IGNORE, 0 ],    \
         [ parser.CENT,     None,  "ecent",    None,           eCenter,     parser.IGNORE, 0 ],     \
                                                                                                \
         [ parser.WRAP,     None,   None,       TXTCLASS,       Text,       parser.IGNORE, 0 ],    \
         [ parser.WRAP,     None,  "ewrap",    None,            eWrap,      parser.IGNORE, 0 ],     \
                                                                                                \
         [ parser.INDENT,     None,   None,       TXTCLASS,       Text,       parser.IGNORE, 0 ],    \
         [ parser.INDENT,     None,  "eindent",    None,            eIndent,      parser.IGNORE, 0 ],     \
         
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

if __name__ == "__main__":

    try:
        strx = sys.argv[1]    
    except:
        print "Usage: parser.py filename"; exit(1);

    try:
        f = open(strx)
    except:
        print "file '" + strx + "' must be an existing and readble file.";  
        exit(2);
    
    try:
        buf = f.read();
    except:
        print "Cannot read'" + strx + "'"

    f.close()

    mainview = pangodisp.PangoView()
    #mainview.add_text("hello")

    xstack = stack.Stack()       
    lexer.Lexer(buf, xstack, parser.tokens)
    #xstack.dump() # To show what the lexer did
    parser.Parse(buf, xstack)
  
  # Output results (to show workings)
    print _cummulate
  
    main()
  
