#!/usr/bin/env python

import sys, os, re

# Our modules
import stack, lexer

''' 
The parser needs several variables to operate. 
  Quick summary of variables:
     Token definitions, Lexer tokens, Parser functions,
      Parser states, Parse state table.
See pangparser.py for documentation and examples.
'''

# Quick into: The lexer creates a stack of tokens. The parser scans
# the tokens, and walks the state machine for matches. If match 
# is encountered, the parser calls the function in the state table, 
# and / or changes state. Reduce is called after the state has been 
# successfully digested. For more info see lex / yacc literature.

_gl_cnt = 0
def unique():             # create a unique temporary number
    global _gl_cnt; _gl_cnt+= 10
    return _gl_cnt

# This variable controls the display of the default action.
# The default action is executed when there is no rule for the 
# expression. Mostly useful for debugging the grammar.

_show_default_action = False

# May be redefined, included here for required initial states:

ANYSTATE    = [-2, "anystate"]
REDUCE      = [-1, "reduce"]
IGNORE      = [unique(), "ignore"]
INIT        = [unique(), "init"]

# define one for printable zero for faster

PARIDX = 1

# ------------------------------------------------------------------------
# Parser:
#
# Note: This parser creates no error conditions. Bad for languages, good
# for text parsing. Warnings can be generated by enabling show_default
# action. The parser is not recursive, so states need to be nested by 
# hand. The flat parser is an advantage for text processing.

class Parse():

    def __init__(self, data, xstack):

        self.fstack = stack.Stack()
        self.fsm = INIT; self.contflag = 0

        #print "Showing list:"
        while True:
            tt = xstack.get2()  # Gen Next token
            if not tt: 
                #print "Ended parsing"
                break

            #print data, tt[0], tt[1].start(), tt[1].end()
            mmm = tt[1];
            self.strx = data[mmm.start():mmm.end()]
           
            #print "Scanning in state:", self.fsm,
            #print  "for", tt[0][1] + "=\"" + self.strx + "\""
            match = False

            # Scan parse table:            
            for pt in parsetable:
                statematch = 0
                if pt[0] == None:
                  for aaa in pt[1]:             # Scan for state match
                        if aaa == self.fsm:
                            statematch = 1
                elif pt[0] == self.fsm:
                       statematch = 1

                if not statematch:
                    #print "Not in state ", pt[0]
                    continue
    
                classmatch = False
                # See if we have a class match
                if pt[3] != None:                
                    for ptt in pt[3]:
                        if tt[0][1] == ptt:
                            #print "classmatch", ptt
                            classmatch = True  
                
                if tt[0][1] == pt[2] or classmatch:
                    #print " matching table entry ", pt[0], pt[1]
                    match = True
                    if pt[4] != None:
                        pt[4](self, tt, pt) 
                    
                    if pt[5] == REDUCE:     
                        # This is an actionless reduce ... rare
                        self.reduce(tt)

                    elif pt[5] == IGNORE:
                        pass   
                    else: 
                        #print " Setting new state", pt[3], self.strx
                        self.fstack.push([self.fsm, self.contflag, tt, self.strx])                    
                        self.fsm = pt[5]
                        self.contflag = pt[6]            
                    # Done working, next token
                    break;

            if not match:
                if _show_default_action:
                    print " default action on",  tt[0], "'" + self.strx + "'", \
                    "Pos:", mmm.start()

    def popstate(self):
        self.fsm, self.contflag, self.ttt, self.stry = self.fstack.pop()

if __name__ == "__main__":
    print "This module was not meant to operate as main."

# EOF
