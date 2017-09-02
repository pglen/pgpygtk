#!/usr/bin/env python

import os, sys, getopt, signal, select, string, time
import tarfile, subprocess, commands, struct, gobject
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
version = 1.0
pgdebug = 0

# Globals
mydata = {}
mystate = {}
myhandler = {}
server = None

# Walk thru a state machine 
# 1. Get length
# 2. Get data
# 3. Reply

class DataHandler():
    
    def __init__(self, par):
        #print  "DataHandler"
        self.src = None
        self.tout = None
        pass
        
    def handler_timeout(self):
        self.tout.cancel()
        print "handler_timeout", self.name 
        # Force closing connection
        print self.par.client_address, self.par.server.socket
        self.par.request.send("Timeout occured.\n")
        self.par.request.shutdown(socket.SHUT_RD)
    
    def putdata(self, response):
        if self.tout: self.tout.cancel()
        self.par.request.send(response)
          
    def getdata(self, amount):
        # We use gobj instead of SIGALRM, so it is more multi platform
        #if self.src: gobject.source_remove(self.src)        
        #self.src = gobject.timeout_add(100, self.handler_timeout)
        if self.tout: self.tout.cancel()
        self.tout = threading.Timer(2, self.handler_timeout)
        self.tout.start()
        return self.par.request.recv(amount)
    
    def handle(self, par):    
        self.par = par
        cur_thread = threading.currentThread()
        self.name = cur_thread.getName()
        
        state = 0; xlen = 0; data = ""; ldata = ""
        print "*** Handling connection on", self.name, "From", self.par.client_address
        while 1:
            if state == 0:
                xdata = self.getdata(2-len(ldata))
                if len(xdata) == 0:
                    break
                ldata += xdata    
                if len(ldata) == 2:
                    state = 1; 
                    xlen = struct.unpack("!h", ldata)[0]
                    #print "got len =", xlen
                
            elif state == 1:
                data2 = self.getdata(xlen-len(data))
                if len(data2) == 0:
                    break
                data += data2
                if len(data) == xlen:
                    state = 3
            
            elif state == 3:
                print "got data '" + data + "'"
                #response = "%s: %s" % (name, str.upper(data))
                response = "%s" % str.upper(data)
                print "Replied with", "'" + response + "'"
                self.putdata(response)
                if self.tout: self.tout.cancel()
                state = 0
            else:
                print "Unkown state"
    
        if self.tout: self.tout.cancel()
        #if self.src: gobject.source_remove(self.src)        
        
# ------------------------------------------------------------------------

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def __init__(self, a1, a2, a3):
        self.a2 = a2
        #print a1 #print a2 #print a3
        SocketServer.BaseRequestHandler.__init__(self, a1, a2, a3)
        #print  SocketServer
        
    def finish(self):
        del mydata[self.name]
        del mystate[self.name]
        del myhandler[self.name]
        print "Closed socket on", self.name
    
    def setup(self):
        cur_thread = threading.currentThread()
        self.name = cur_thread.getName()
        if verbose:
            print "Connection from ", self.a2
            
        mydata[self.name] = 0
        mystate[self.name] = 0
        myhandler[self.name] = DataHandler(self)
        
        #self.server.RequestHandlerClass.state = 23
        #self.server.RequestHandlerClass.len = 48
        
        if verbose:
            print "Opened connection on", self.name
        
    def handle(self):
        myhandler[self.name].handle(self)
    
# ------------------------------------------------------------------------
# Override stock methods

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    
    def stop(self):
        self._BaseServer__shutdown_request = True
        print "stop called"
        
    '''def serve_forever(self):
        print self.__dict__
        while 1:
            self.handle_request()
            print "Handled"
            if self._BaseServer__shutdown_request:
                break 
                
        print "closing"        
        #self.server_close()
        self._BaseServer__is_shut_down.set()
        #sys.exit(2)'''

# ------------------------------------------------------------------------

def help():

    print
    print "Usage: " + os.path.basename(sys.argv[0]) + " [options]"
    print
    print "Options:    -d level  - Debug level 1-10"
    print "            -v        - Verbose"
    print "            -f        - Force"
    print "            -h        - Help"
    print
    sys.exit(0)

# ------------------------------------------------------------------------

def print_except(xstr):

    a,b,c = sys.exc_info();  
    print xstr; 
    if a != None:
        print a, b, c.print_tb()
        
def terminate(arg1, arg2):
    global mydata, mystate
    
    print "Dumping connection info:"
    print mydata, mystate
    server.shutdown()
    server.stop()
    print_except("Terminated pyserv.py.")
    sys.exit(2)

def hello():
    print "timeout"
    
def handler_tick(signum, frame):
    print "handle_tick", signum, frame
    
    
# ------------------------------------------------------------------------

if __name__ == '__main__':

    opts = []; args = []

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
                
    # Set termination handlers
    signal.signal(signal.SIGTERM, terminate)
    signal.signal(signal.SIGINT, terminate)
    
    # Set the signal handler for 1s tick, restrtable sys calls
    #signal.signal(signal.SIGALRM, handler_tick)
    #signal.siginterrupt(signal.SIGALRM, False)
    #signal.alarm(1)
    
    # Port 0 would mean to select an arbitrary unused port
    HOST, PORT = "localhost", 9999
    #HOST, PORT = "192.168.1.13", 9999

    #gobject.timeout_add(1000, handle_timeout)
            
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server.allow_reuse_address = True
    
    #server.timeout = 5
    #server.handle_timeout = handle_timeout

    # Start a thread with the server -- that thread will then start one
    # more threads for each request
    server_thread = threading.Thread(target=server.serve_forever)
    
    # Exit the server thread when the main thread terminates
    server_thread.setDaemon(True)
    server_thread.start()

    
    #gobject.timeout_add(1000, handle_timeout)
    
    print "Server running:", server.server_address
    #print "Server loop running in thread:", server_thread.getName()
    server.serve_forever()
    
    #gobject.MainLoop().run()
    
    #server.shutdown()
    #sys.exit(0)    
    #print "terminating"






