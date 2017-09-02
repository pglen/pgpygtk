#!/usr/bin/env python

import os, sys, string, time

buffsize = 4096

# ------------------------------------------------------------------------
# A more informative exception print 
 
def put_debug(xstr):
    try:
        if os.isatty(sys.stdout.fileno()):
            print xstr
        else:
            syslog.syslog(xstr)
    except:
        print "Failed on debug output."
        print sys.exc_info()

def put_exception(xstr):

    cumm = xstr + " "
    a,b,c = sys.exc_info()
    if a != None:
        cumm += str(a) + " " + str(b) + "\n"
        try:
            #cumm += str(traceback.format_tb(c, 10))
            ttt = traceback.extract_tb(c)
            for aa in ttt: 
                cumm += "File: " + os.path.basename(aa[0]) + \
                        " Line: " + str(aa[1]) + "\n" +  \
                    "   Context: " + aa[2] + " -> " + aa[3] + "\n"
        except:
            print "Could not print trace stack. ", sys.exc_info()
            
    put_debug(cumm)    
    #syslog.syslog("%s %s %s" % (xstr, a, b))

# ------------------------------------------------------------------------
# Helper functions.
# Escape spaces to %20 and misc chars

def escape(strx):

    aaa = ""; 
    for aa in strx:
        if aa == "%":
            aaa += aa + aa
        elif aa == " ":
            aaa += "%%%x" % ord(aa)
        elif aa == "\"":
            aaa += "%%%x" % ord(aa)
        elif aa == "\'":
            aaa += "%%%x" % ord(aa)
        else:
            aaa += aa
    return aaa
    
# Run through a state machine to descramble

def unescape(strx):

    aaa = ""; back = ""; state = 0; chh = ""
    
    for aa in strx:
        if state == 3:
            aaa += back; back = ""; state = 0; chh = ""
            
        if state == 2:
            if aa >= "0" and aa <= "9":
                back = ""; state = 3; chh += aa
                aaa += chr(int(chh, 16))
            else: 
                back += aa; state = 3
        
        if state == 1:
            if aa >= "0" and aa <= "9":
               state = 2; chh += aa
            elif aa == "%":
                aaa += "%"; back = ""; state = 3
            else: 
                back += aa; state = 3
            
        if state == 0:
            if aa == "%":
                state = 1; back += aa
            else:
                aaa += aa
    
    return aaa
    
# ------------------------------------------------------------------------
# Remove dup //

def dirclean(strx):
    rrr = ""; aaa = strx.split("/")
    for aa in aaa:
        if aa != "": rrr += "/" + aa
    return rrr    

# ------------------------------------------------------------------------
# Change directory to up (..)

def chup(strx):
    # Stage 1: clean
    rrr2 = ""; rrr = dirclean(strx)
    # Stage 2: cut end
    for aa in rrr.split("/")[:-1]: 
        rrr2 += "/" + aa
    return rrr2

if __name__ == '__main__':

    strx = "test str he%re \" aa%12aa %20"
    strx2 = escape(strx);  strx3 = unescape(strx2)
    
    print strx
    print strx2
    print strx3
    
    print "String equality test:", strx == strx3

    # Print characters 
    '''for aa in range(0x80):
        if aa >= 0 and aa < 17:
            print "%3x  " % (aa),
        else:
            print "%3x %c" % (aa, aa),
        if aa % 8 == 0 and aa > 0:
            print '''



