#!/usr/bin/env python

import re

# ------------------------------------------------------------------------
#

class _LexIter():
      
    def __init__(self):
        cnt = 0; 
        
    def ptokens():
        for xx in self.tokens: # print tokens
            print xx
        
    def lexiter(self, pos, tokens, strx):
        #print strx[pos:]
        for bb, cc in tokens:
            #print bb, cc
            mmm = cc.match(strx, pos)
            if mmm:
                #print mmm.end() - mmm.start(), strx[mmm.start():mmm.end()]
                tt = bb, mmm
                return tt
        
        return None;

class Lexer():

    def __init__(self, data, stack, tokens):
        
        print data  
        lexiter = _LexIter()
        lastpos = 0;  pos = 0; lenx = len(data)
        while True:
            if pos >= lenx:
                break; 
            tt = lexiter.lexiter(pos, tokens, data)
            if tt == None: break
            mmm = tt[1]
            if mmm: 
                # skip token                
                pos = mmm.end()
                #print  tt[1], "'" + data[mmm.start():mmm.end()] + "' - ",
                stack.push(tt)
            else:
                pos += 1  # step to next

# EOF
