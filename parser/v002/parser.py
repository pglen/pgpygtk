#!/usr/bin/env python

import sys, os, re

# Our modules
import stack, lexer

# State machine states

gl_cnt = 0
def _unique():
    global gl_cnt; gl_cnt+= 10
    return gl_cnt
    
# The number is the state, the string for debugging / analizing
# Once ready, operate on the numbers for speed
REDUCE  = [-1, "reduce"],

states = \
    "state_1", "state2"

states2 = []

#for aa in states:
#    states2.append([aa, _unique()])    

#print states
#print states2

IGNORE  = [_unique(), "ignore"],
INIT    = [_unique(), "init"],
SPAN    = [_unique(), "span"],
IDENT   = [_unique(), "ident"],
KEY     = [_unique(), "key"],
VAL     = [_unique(), "val"],
EQ      = [_unique(), "EQ"],
KEYVAL  = [_unique(), "KEYVAL"],

# Token definitions:
tokdef = [_unique(), "span"],      \
         [_unique(), "endspan"],   \
         [_unique(), "it"      ],  \
         [_unique(), "eit"     ],  \
         [_unique(), "bold"    ],  \
         [_unique(), "ebold"   ],  \
         [_unique(), "escquo"  ],  \
         [_unique(), "dblbs"   ],  \
         [_unique(), "ident"    ], \
         [_unique(), "str"    ],   \
         [_unique(), "str2"   ],   \
         [_unique(), "eq"     ],   \
         [_unique(), "lt"     ],   \
         [_unique(), "gt"     ],   \
         [_unique(), "sp"     ],   \
         [_unique(), "tab"    ],   \
         [_unique(), "nl"     ],   \
         [_unique(), "any"    ],   \

#print tokdef

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

# ------------------------------------------------------------------------
# Parser functions that are called on parser events

def emit(strx):
    print strx,
    pass    

def Ident():
    #print "called ident"
    pass

def Span(parser, token, tentry):
    print "called span", parser.strx
    #parser.fstack.show()
    xstack = stack.Stack()
    # Walk optionals:
    while True:             
        fsm, contflag, ttt, stry = parser.fstack.pop()
        if fsm == KEYVAL:          
            print " Reducing keyval", fsm, \
                "'"+ttt+"'", "\"" + stry + "\""            
            xstack.push([ttt, "+", stry])
        if contflag == 0:
            break
    
    #parser.fstack.show()
    # Emit final
    emit("<span ");
    while True:
        strx = xstack.pop()
        if not strx:
            break
        emit(strx)
    emit (">\n" )
    
def Keyval(parser, token, tentry):

    print "called keyval", parser.fsm, token, parser.strx
    
    # Pop two items, create keyval
    fsm, contflag, ttt, stry = parser.fstack.pop()      # EQ
    fsm2, contflag2, ttt2, stry2 = parser.fstack.pop()  # Key

    # Push back summed item
    parser.fstack.push([KEYVAL, 1, stry2, parser.strx])
    parser.fsm = fsm2
    
    #parser.fstack.push([ ])
    
# ------------------------------------------------------------------------
# Parse table.
#
#  Specify parse state, token to see for action, function to execute,
# new parse state, and continuation flag for reduce.
# Alternatives can be specified with multiple lines for the same state
#
# Parser ignores unmatched entries. 
#    (bad for lanuages, good for error free parsing like text parsing)
#
# This table specifies a grammar for <span> tag in text processing
#
#     --- state ---- token ---- function ----- new state --- cont flag
 
parsetable = \
         [ INIT,     "span",     None,      SPAN, 0 ],    \
         [ SPAN,     "ident",    None,      KEY, 1 ],    \
         [ KEY,      "eq",       None,      VAL, 1 ],    \
         [ VAL,      "ident",    Keyval,    IGNORE, 0 ],  \
         [ VAL,      "str",      Keyval,    IGNORE, 0 ],  \
         [ SPAN,     "gt",       Span,      IGNORE, 0 ],  \

# ------------------------------------------------------------------------
# Reduce table.
#
# When reducing, if the pattern is recognized, the result function is called.
# 

        # Resultfunc ---  state 1 ... state2 ...

reducetable = \
        [Keyval, VAL, EQ, KEY], \
        [Span,   KEYVAL,0,0],       \

class ParseEvent():
    
    def run(self, ttt):
        #print typex, mmm.start(), mmm.end(), mmm.string
        mmm = ttt[1]
        print mmm.string[:mmm.start()]

class Parse():

    def __init__(self, data, xstack, event):

        self.fstack = stack.Stack()
        self.fsm = INIT; self.contflag = 0

        #print "Showing list:"
        while True:
            tt = xstack.get2()  # Gen Next token
            if not tt: 
                break

            #print data, tt[0], tt[1].start(), tt[1].end()
            mmm = tt[1];
            self.strx = data[mmm.start():mmm.end()]
           
            #print "Scanning in state:", self.fsm,
            #print  "for", tt[0][1] + "=\"" + self.strx + "\""
            match = False

            # Scan parse table:            
            for pt in parsetable:
                if pt[0] != self.fsm:
                    #print "Not in state ", pt[0]
                    continue
    
                if tt[0][1] == pt[1]:
                    #print " matching table entry ", pt[0], pt[1]
                    match = True
                    if pt[2] != None:
                        pt[2](self, tt, pt) 
                    
                    if pt[3] == REDUCE:     
                        self.reduce(tt)

                    elif pt[3] == IGNORE:
                        pass   
                    else: 
                        #print " Setting new state", pt[3], self.strx
                        self.fstack.push([self.fsm, self.contflag, tt, self.strx])                    
                        self.fsm = pt[3]
                        self.contflag = pt[4]            
                    # Done working, next token
                    break;

            if not match:
                #print " default action executed"
                pass

    def reduce(self, tt):
        return # disabled
        # Current state:                              
            
        rstack = stack.Stack()     
        print " Reducing curr", self.fsm, self.contflag, \
                    "with",  "\"" + self.strx + "\""                    
        rstack.push([self.fsm, self.contflag, tt, self.strx])                                                   
        while True:             
            self.fsm, self.contflag, ttt, stry = self.fstack.pop()
            print " Reducing to", self.fsm, self.contflag, \
                    "with", "\"" + stry + "\""            
            rstack.push([self.fsm, self.contflag, ttt, self.strx])                    
            if self.contflag == 0: break # until bound

        cnt2 = 0
        while True:
            try:
                rrr = reducetable[cnt2]
            except:
                break;
            cnt2 += 1
            print "reduceitem",rrr
            
            cnt = 1
            while True:
                sss = rstack.get2()
                if not sss: break
                print sss[0]
                #if rrr[1] == sss[1]: pass
                print "redsttack:", rrr[cnt], sss[cnt]
                cnt += 1

    #        rstack.dump()
                   
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
    lexer.Lexer(buf, xstack, tokens)
    Parse(buf, xstack, ParseEvent())
    
    main()

