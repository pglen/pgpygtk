#!/usr/bin/env python

import os, sys, string, time #, crypt

# Globals and configurables

buffsize = 4096
passfile =  ".pyserv/passwd.secret"
keyfile = ".pyserv/keys.secret"

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

# ------------------------------------------------------------------------
# Save key to local file. Return err code and cause.
#   kadd = 0 -> Authenticate
#   kadd = 1 -> add
#   kadd = 2 -> delete
#
# Return negative for error
#        0 for key added
#        1 for key match
#        2 for duplicate
#        4 for key deleted


def kauth(namex, keyx, kadd = False):

    fields = ""; dup = False; ret = 0, ""
    try:
        fh = open(keyfile, "r")
    except:
        try:
            fh = open(keyfile, "w+")
        except:
            return -1, "Cannot open / create key file " + keyfile + " for reading"
    keydb = fh.readlines()
    for line in keydb:
        fields = line.split(",")
        if namex == fields[0]:
            dup = True
            break                      
    if not dup:
        if kadd == 1:
            # Add
            fh.close()
            try:
                fh2 = open(keyfile, "r+")
            except:
                try:
                    fh2 = open(keyfile, "w+")
                except:
                    return -1, "Cannot open / create " + keyfile + " for writing"
            try:
                fh2.seek(0, os.SEEK_END)
                fh2.write(namex + "," + keyx + "\n")                
            except:
                fh2.close()
                return -1, "Cannot write to " + keyfile 
            fh2.close()
            ret = 0, "Key saved"
    else:
        if kadd == 0:
            ret = 1, fields[1].rstrip()
        elif kadd == 1:
            ret = 2, "Duplicate key"
        elif kadd == 2:
            # Delete key
            delok = 0
            pname3 = keyfile + ".tmp"
            try:
                fh3 = open(pname3, "r+")
            except:
                try:
                    fh3 = open(pname3, "w+")
                except:
                    ret = 0, "Cannot open " + pname3 + " for writing"
                    return ret
            # Do not touch line 1
            fh3.write(keydb[0])
            for line in keydb[1:]:
                fields = line.split(",")
                if fields[0] == namex:
                    delok = 1
                    pass
                else:
                    fh3.write(line)
            # Rename       
            try:
                os.remove(keyfile)
                os.rename(pname3, passfile)
            except:
                ret = -1, "Cannot rename from " + pname3 
                return ret  
            if delok:
                ret = 4, "Key deleted"
            else:
                ret = -1, "Key NOT deleted (possibly kini key)"
        else:
            ret = -1, "Invalid opcode"
    return ret

# ------------------------------------------------------------------------
# Authenticate from local file. Return err code and cause.
#
#   uadd = 0 -> Authenticate
#   uadd = 1 -> add
#   uadd = 2 -> delete
#
# Return negative for error
#        0 for user added
#        0 for bad user or bad pass
#        1 for user match
#        2 for duplicate
#        3 for no user
#        4 for user deleted

def auth(userx, upass, uadd = False):

    fields = ""; dup = False
    upass2 = crypt.crypt(upass)
    try:
        fh = open(passfile, "r")
    except:
        try:
            fh = open(passfile, "w+")
        except:
            return -1, "Cannot open pass file " + passfile
            
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
                fh2 = open(passfile, "r+")
            except:
                try:
                    fh2 = open(passfile, "w+")
                except:
                    ret = 0, "Cannot open " + passfile + " for writing"
                    return ret
            fh2.seek(0, os.SEEK_END)
            fh2.write(userx + "," + upass2 + "\n")                
            fh2.close()
            ret = 2, "Saved pass"
        else:
            ret = 3, "No such user"
    else:
        if uadd == 2:
            delok = 0
            # Delete userx
            pname3 = passfile + ".tmp"
            try:
                fh3 = open(pname3, "r+")
            except:
                try:
                    fh3 = open(pname3, "w+")
                except:
                    ret = 0, "Cannot open " + pname3 + " for writing"
                    return ret
            # Do not touch line 1
            fh3.write(passdb[0])
            for line in passdb[1:]:
                fields = line.split(",")
                if fields[0] == userx:
                    delok = 1
                    pass
                else:
                    fh3.write(line)
            # Rename       
            try:
                os.remove(passfile)
                os.rename(pname3, passfile)
            except:
                ret = 0, "Cannot rename from " + pname3 
                return ret  
            if delok:
                ret = 4, "User deleted"
            else:
                ret = 0, "User NOT deleted (possibly uini user)"
        else:
            c2 = crypt.crypt(upass, fields[1])
            if c2 == fields[1].rstrip():
                ret = 1, "Authenicated"
            else:
                ret = 0, "Bad User or Bad Pass"
    fh.close()
    return ret

if __name__ == '__main__':
    print "test"
    


