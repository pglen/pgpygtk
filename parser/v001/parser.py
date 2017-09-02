#!/usr/bin/env python

import sys, os, re

# Our modules
import stack, lexer

# State machine states
IGNORE  = 0
INIT    = 1
SPAN    = 2
EQ      = 3

# Token definitions:
tokdef = [10, "span"],     \
         [20, "endspan"],  \
         [30, "it"      ], \
         [40, "eit"     ], \
         [50, "bold"    ], \
         [60, "ebold"   ], \
         [70, "escquo"  ], \
         [80, "dblbs"   ], \
         [90, "iden"    ], \
         [100, "str"    ], \
         [110, "str2"   ], \
         [120, "eq"     ], \
         [130, "lt"     ], \
         [140, "gt"     ], \
         [150, "sp"     ], \
         [160, "tab"    ], \
         [170, "nl"     ], \
         [180, "any"    ], \

# ------------------------------------------------------------------------
# Lexer tokens
#     --- enum ---- token ---- function ----- new state ---

tokens =    [tokdef[0],    re.compile("<span ")     ], \
            [tokdef[1],    re.compile("</span>")    ], \
            [tokdef[2],    re.compile("<i>")         ], \
            [tokdef[3],    re.compile("</i>")        ], \
            [tokdef[4],    re.compile("<b>")         ], \
            [tokdef[5],    re.compile("</b>")        ], \
            [tokdef[6],    re.compile(r"\\\"")       ], \
            [tokdef[7],    re.compile(r"\\\\")      ], \
            [tokdef[8],    re.compile("[A-Za-z0-0_]+")  ], \
            [tokdef[9],    re.compile("\".*?\"")    ], \
            [tokdef[10],   re.compile("\'.*?\'")    ], \
            [tokdef[11],   re.compile("=")           ], \
            [tokdef[12],   re.compile("<")           ], \
            [tokdef[13],   re.compile(">")           ], \
            [tokdef[14],   re.compile(" ")           ], \
            [tokdef[15],   re.compile("\t")          ], \
            [tokdef[16],   re.compile("\n")          ], \
            [tokdef[17],   re.compile(".")           ], \

def Ident():
    pass

# ------------------------------------------------------------------------
# Parse table
#     --- state ---- token ---- function ----- new state ---
 
parsetable = \
         [INIT,     "span",     None,       SPAN ],     \
         [ SPAN,     "ident",   Ident(),    IGNORE ],  \
         [ SPAN,     "eq",      None,       EQ ],      \

class ParseEvent():
    
    def run(self, ttt):
        #print typex, mmm.start(), mmm.end(), mmm.string
        mmm = ttt[1]
        print mmm.string[:mmm.start()]

class Parse():

    def __init__(self, data, xstack, event):

        self.fsm = stack.Stack()

        print "\nShowing list:"
        while True:
            tt = xstack.get2()
            if not tt: 
                break
            mmm = tt[1];
            print  tt[0][1] + "=\"" + data[mmm.start():mmm.end()] + "\"  ",

            # Scan Parse table:            
            for pt in parsetable:
                print tt[0], pt[1]           
                #if tt[1] == pt[1]:
                #    self.fsm = SPAN                
            break;
        
def main():
    #gtk.main()
    return 0

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

    #print tokens;
    #exit();
  
    xstack = stack.Stack()   
    #xstack.data = buf            # carry the original buffer

    lexer.Lexer(buf, xstack, tokens)
    Parse(buf, xstack, ParseEvent())
    
    main()

