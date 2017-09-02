#!/usr/bin/env python

# ------------------------------------------------------------------------
# Test client for the pyserv project

import os, sys, getopt, signal, select, socket, time, struct
import random, stat

import pyserv.pydata, pyserv.pyservsup

# ------------------------------------------------------------------------
# Globals 

myhandler = None
mydathand = None

pgdebug = 0
verbose = 0
port    = 9999
version = 1.0

# Send out our special buffer (short)len + (str)message

def sendx(sock, message):
    strx = struct.pack("!h", len(message)) + message
    sock.send(strx)
    
def sendfile(s1, fname, toname):

    try:    
        flen = os.stat(fname)[stat.ST_SIZE]
        fh = open(fname)
    except:
        print "Cannot open file", sys.exc_info()[1]
        return
    
    client(s1, "file " + toname)
    client(s1, "data " + str(flen))
    while 1:
        buff = fh.read(4096)
        if len(buff) == 0:
            break
        sendx(s1, buff)
    response = myhandler.handle_one(mydathand)
    print "Received: '%s'" % response
    
# ------------------------------------------------------------------------

def client(sock, message, quiet = False):

    sendx(sock, message)
    if verbose and not quiet:
        print "Sent: '%s'" % message,
        
    response = myhandler.handle_one(mydathand)
    if verbose and not quiet:
        print "Recd: '%s'" % response
        
    return response

# ------------------------------------------------------------------------

def help():

    print
    print "Usage: " + os.path.basename(sys.argv[0]) + " [options]"
    print
    print "Options:    -d level  - Debug level 0-10"
    print "            -p        - Port to use (default: 9999)"
    print "            -v        - Verbose"
    print "            -q        - Quiet"
    print "            -h        - Help"
    print
    sys.exit(0)

# ------------------------------------------------------------------------

if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:p:qhvVfp")
    except getopt.GetoptError, err:
        print "Invalid option(s) on command line:", err
        sys.exit(1)

    #print "opts", opts, "args", args
    
    for aa in opts:
        if aa[0] == "-d":
            try:
                pgdebug = int(aa[1])
                if verbose:
                    print "Debug level:", pgdebug
                if pgdebug > 10 or pgdebug < 0:
                    raise(ValueError, \
                        "Debug range needs to be between 0-10")
            except:
                pyservsup.put_exception("Command line:")
                sys.exit(3)

        if aa[0] == "-p": 
            try:
                port = int(aa[1])            
                if verbose:
                    print "Port:", port
            except:
                pyservsup.put_exception("Command line:")
                sys.exit(3)
        
        if aa[0] == "-h": help();  exit(1)
        if aa[0] == "-v": verbose = True            
        if aa[0] == "-q": quiet = True            
        if aa[0] == "-f": force = True            
        if aa[0] == "-V": 
            print os.path.basename(sys.argv[0]), "Version", version
            sys.exit(0)

    if len(args) == 0:
        ip = '127.0.0.1' 
    else:
        ip = args[0]
    
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mydathand  = pyserv.pydata.xHandler(s1)
    myhandler  = pyserv.pydata.DataHandler()
    
    try:
        s1.connect((ip, port))
    except:
        print "Cannot connect to:", ip + ":" + str(port), sys.exc_info()[1]
        sys.exit(1)

    client(s1, "ver")
    client(s1, "user peter")
    resp = client(s1, "pass 1234")
    if resp.split(" ")[0] == "ERR":
        print "Cannot authenticate: ", resp
        sys.exit(2)

    #client(s1, "timeout 10")
        
    resp = client(s1, "lsd")
    got = resp.split(" ")
    if got[0] == "OK":
        # Discard ends (OK and trailing space)
        got = got[1:-1]
        for aa in got:
            client(s1, "cd " + aa, True)
            client(s1, "ls")
            client(s1, "cd ..", True)
        #client(s1, "ls")
    
    client(s1, "quit")
    s1.close();
    
    sys.exit(0)







