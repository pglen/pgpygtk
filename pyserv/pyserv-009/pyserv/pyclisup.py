#!/usr/bin/env python

import os, sys, getopt, signal, select, string, time, struct, stat, base64

import pydata, pyserv, pycrypt

# ------------------------------------------------------------------------
# Globals 

myhandler = None; mydathand = None

# ------------------------------------------------------------------------
# Handle command line. Interpret optarray and decorate the passed in 
# class      

class Config:

    def __init__(self, optarr):
        self.optarr = optarr

    def comline(self, argv):
        optletters = ""
        for aa in self.optarr:
            optletters += aa[0]
        #print optletters    
        # Create defaults:
        for bb in range(len(self.optarr)):
            if self.optarr[bb][1]:
                # Coerse type
                if type(self.optarr[bb][2]) == type(0):
                    self.__dict__[self.optarr[bb][1]] = int(self.optarr[bb][2])
                if type(self.optarr[bb][2]) == type(""):
                    self.__dict__[self.optarr[bb][1]] = str(self.optarr[bb][2])
        try:
            opts, args = getopt.getopt(argv, optletters)
        except getopt.GetoptError, err:
            print "Invalid option(s) on command line:", err
            return -1
        #print "opts", opts, "args", args
        for aa in opts:
            for bb in range(len(self.optarr)):
                if aa[0][1] == self.optarr[bb][0][0]:
                    #print "match", aa, self.optarr[bb]
                    if len(self.optarr[bb][0]) > 1:
                        #print "arg", self.optarr[bb][1], aa[1]
                        if self.optarr[bb][2] != None: 
                            if type(self.optarr[bb][2]) == type(0):
                                self.__dict__[self.optarr[bb][1]] = int(aa[1])
                            if type(self.optarr[bb][2]) == type(""):
                                self.__dict__[self.optarr[bb][1]] = str(aa[1])
                    else:
                        #print "set", self.optarr[bb][1], self.optarr[bb][2]
                        if self.optarr[bb][2] != None: 
                            self.__dict__[self.optarr[bb][1]] = 1
                        #print "call", self.optarr[bb][3]
                        if self.optarr[bb][3] != None: 
                            self.optarr[bb][3]()
        return args
    
# ------------------------------------------------------------------------
# Send out our special buffer (short)len + (str)message
def sendx(sock, message):
    strx = struct.pack("!h", len(message)) + message
    sock.send(strx)

# ------------------------------------------------------------------------
# Send file.

def sendfile(s1, fname, toname, verbose = False, key = ""):
    response = ""
    try:    
        flen = os.stat(fname)[stat.ST_SIZE]
        fh = open(fname)
    except:
        print "Cannot open file", sys.exc_info()[1]
        return
    resp = client(s1, "file " + toname, verbose, key)
    if resp.split()[0] != "OK":
        print "Cannot send command", resp
        return 
    resp = client(s1, "data " + str(flen), verbose, key)
    if resp.split()[0] != "OK":
        print "Cannot send command", resp
        return 
    while 1:
        buff = fh.read(pyserv.pyservsup.buffsize)
        if len(buff) == 0:
            break
        if key != "":
            buff = pycrypt.xencrypt(buff, key)
        sendx(s1, buff)
        
    response = myhandler.handle_one(mydathand)
    if key != "":
        response = pycrypt.xdecrypt(response, key)
 
    if verbose:
        print "Received: '%s'" % response
    return True
    
# ------------------------------------------------------------------------
def getfile(s1, fname, toname, verbose = False, key = ""):

    try:  
        fh = open(toname, "w")         
    except:
        print "Cannot create local file: '" + toname + "'"
        return
    response = client(s1, "fget " + fname, verbose, key)
    aaa = response.split(" ")
    if aaa[0] == "ERR":
        fh.close()
        if verbose:
            print "Server said: ", response
        return 
    mylen = 0; flen = int(aaa[1])
    #print "getting", flen,
    while mylen < flen:
        need = min(pyserv.pyservsup.buffsize,  flen - mylen)
        need = max(need, 0)
        data = myhandler.handle_one(mydathand)
        if key != "":
            data = pycrypt.xdecrypt(data, key)
        try:
            fh.write(data)
        except:
            if verbose:
                print "Cannot write to local file: '" + toname + "'"
            fh.close()
            return
        mylen += len(data)
        # Faulty transport, abort
        if len(data) == 0:
            break
    fh.close()
    if verbose:
        print "Got data, len =", mylen
    if  mylen != flen:
        if verbose:
            print "Faulty amount of data arrived"
        return
    return True

# ------------------------------------------------------------------------

def client(sock, message, verbose = False, key = ""):
    global mydathand, myhandler
    
    if verbose:
        print "Sending: '%s'" % message
        
    if key != "":
        message = pycrypt.xencrypt(message, key)
    
    sendx(sock, message)
    
    if verbose and key != "":
        print "   put: '%s'" % base64.b64encode(message),
    
    response = myhandler.handle_one(mydathand)
    
    if verbose and key != "":
        print "get: '%s'" % base64.b64encode(response)
        
    if key != "":
        response = pycrypt.xdecrypt(response, key)
        
    if verbose:
        print "Rec: '%s'" % response
        
    return response

def init_handler(sock):
    global mydathand, myhandler
    mydathand  = pydata.xHandler(sock)
    myhandler  = pydata.DataHandler()
    






