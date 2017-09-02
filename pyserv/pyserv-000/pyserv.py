#!/usr/bin/env python

import os, sys, getopt, signal, select, string
import tarfile, subprocess, commands, struct
import socket, threading, SocketServer

#import gobject, pango, gst
#import warnings
#warnings.simplefilter("ignore")
#import gtk
#warnings.simplefilter("default")
    
create_proj = False             
install_proj = False            
list_proj = False             
verbose = False  
force = False 
version = "1.0"
pgdebug = 0
    
mydata = {}
mystate = {}
myhandler = {}

class DataHandler():
    
    def __init__(self, par):
        #print  "DataHandler"
        pass
        
    def handle(self, par):    
        cur_thread = threading.currentThread()
        name = cur_thread.getName()
        
        state = 0; xlen = 0; data = ""; ldata = ""
        print "handling connection from", name
        while 1:
            if state == 0:
                xdata = par.request.recv(2)
                if len(xdata) == 0:
                    break
                ldata += xdata    
                if len(ldata) == 2:
                    state = 1; 
                    xlen = struct.unpack("!h", ldata)[0]
                    print "got len", xlen
                
            elif state == 1:
                data2 = par.request.recv(xlen)
                if len(data2) == 0:
                    break
                data += data2
                if len(data) == xlen:
                    state = 3
            
            elif state == 3:
                print "got data '" + data + "'"
                #response = "%s: %s" % (name, str.upper(data))
                response = "%s" % str.upper(data)
                print "Reply with", response
                par.request.send(response)
                state = 0
            else:
                print "Unkown state"
    
class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def __init__(self, a1, a2, a3):
        SocketServer.BaseRequestHandler.__init__(self, a1, a2, a3)
        
    def finish(self):
        del mydata[self.name]
        del mystate[self.name]
        del myhandler[self.name]
        print "Closed socket on", self.name
    
    def setup(self):
        cur_thread = threading.currentThread()
        self.name = cur_thread.getName()
        mydata[self.name] = 0
        mystate[self.name] = 0
        myhandler[self.name] = DataHandler(self)
        
        #self.server.RequestHandlerClass.state = 23
        #self.server.RequestHandlerClass.len = 48
        #print "Opened connection on", self.name
        
    def handle(self):
        myhandler[self.name].handle(self)
    
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def help():

    print 
    print "Usage: " + os.path.basename(sys.argv[0]) + " [options]"
    print "Options:"
    print "            -d level  - Debug level 1-10. (Limited implementation)"
    print "            -v        - Verbose"
    print "            -f        - Force"
    print "            -V        - Print version"
    print "            -h        - Help"
    print 
    sys.exit(0)

# ------------------------------------------------------------------------

def print_except(xstr):
    print xstr; a,b,c = sys.exc_info();  print a, b, c.print_tb()

def terminate(arg1, arg2):
    global mydata, mystate
    print "Terminating pyserv.py"
    print mydata, mystate

# ------------------------------------------------------------------------

if __name__ == '__main__':

    opts = []; args = []
    
    signal.signal(signal.SIGTERM, terminate)
    signal.signal(signal.SIGINT, terminate)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvVf")
    except getopt.GetoptError, err:
        print "Invalid option(s) on command line:", err
        sys.exit(1)

    #print "opts", opts, "args", args
    
    for aa in opts:
        if aa[0] == "-d":
            try:
                pgdebug = int(aa[1])
            except:
                pgdebug = 0

        if aa[0] == "-h": help();  exit(1)
        if aa[0] == "-v": verbose = True            
        if aa[0] == "-f": force = True            
        if aa[0] == "-V": 
            print os.path.basename(sys.argv[0]), "Version", version
            sys.exit(0)
                
    # Port 0 would mean to select an arbitrary unused port
    HOST, PORT = "localhost", 9999

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more threads for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.setDaemon(True)
    server_thread.start()
    print "Server running:", server.server_address
    #print "Server loop running in thread:", server_thread.getName()
    server.serve_forever()
    #server.shutdown()
    #sys.exit(0)    
    print "terminating"





