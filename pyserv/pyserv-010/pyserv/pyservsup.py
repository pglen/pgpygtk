#!/usr/bin/env python

import os, sys, string, time, crypt

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

# ------------------------------------------------------------------------
# Authenticate from local file. Return err code and cause.
#
#   uadd = 0 -> Authenticate
#   uadd = 1 -> add
#   uadd = 2 -> delete


def auth(userx, upass, uadd = False):

    pname = "passwd"; fields = ""; dup = False
    upass2 = crypt.crypt(upass)
    try:
        fh = open(pname, "r")
    except:
        try:
            fh = open(pname, "w+")
        except:
            return -1, "Cannot open pass file " + pname
            
    passdb = fh.readlines()
    for line in passdb:
        fields = line.split(",")
        if fields[0] == userx:
            dup = True
            break
    if not dup:
        fh.close()
        if uadd == 1:
            try:
                fh2 = open(pname, "r+")
            except:
                try:
                    fh2 = open(pname, "w+")
                except:
                    ret = 0, "Cannot open " + pname + " for writing"
                    return ret
            fh2.seek(0, os.SEEK_END)
            fh2.write(userx + "," + upass2 + "\n")                
            fh2.close()
            ret = 2, "Saved pass"
        else:
            ret = 3, "No such user"
    else:
        if uadd == 2:
            # Delete userx
            pname3 = pname + ".tmp"
            try:
                fh3 = open(pname3, "r+")
            except:
                try:
                    fh3 = open(pname3, "w+")
                except:
                    ret = 0, "Cannot open " + pname3 + " for writing"
                    return ret
            for line in passdb:
                fields = line.split(",")
                if fields[0] == userx:
                    pass
                else:
                    fh3.write(line)
            # Rename       
            try:
                os.remove(pname)
                os.rename(pname3, pname)
            except:
                ret = 0, "Cannot rename from " + pname3 
                return ret  
            ret = 4, "User deleted"
        else:
            c2 = crypt.crypt(upass, fields[1])
            if c2 == fields[1].rstrip():
                ret = 1, "Authenicated"
            else:
                ret = 0, "Bad User or Bad Pass"
    fh.close()
    return ret






