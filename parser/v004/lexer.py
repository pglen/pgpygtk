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
        for bb, cc, dd in tokens:
            #print bb, cc
            mmm = dd.match(strx, pos)
            if mmm:
                #print mmm.end() - mmm.start(), strx[mmm.start():mmm.end()]
                tt = bb, mmm, strx[mmm.start():mmm.end()]
                return tt
        
        return None;

class Lexer():

    def __init__(self, data, stack, tokens):
        
        # Pre-compile tokens
        cnt = 0;  
        while True: 
            try: 
                tokens[cnt][2] = re.compile(tokens[cnt][1])
            except: break
            cnt += 1

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

if __name__ == "__main__":
    print "This module was not meant to operate as main."

# EOF
