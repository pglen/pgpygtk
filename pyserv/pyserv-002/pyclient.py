#!/usr/bin/env python

import os, sys, getopt, signal, select, socket, time, struct
import random

def send2(sock, message):

    for aa in range(len(message)):
        #print "send '" + message[aa] + "'"
        sock.send(message[aa])
    
# ------------------------------------------------------------------------

def client(ip, port, message):

    #print ip, port
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    
    str2 = "%04d" % len(message)
    str2 = struct.pack("!h", len(message))
    #print "Sent: %s" % str2
    #sock.send(str2)
    send2(sock, str2)
    
    #print "Sent: '%s'" % message[:8]
    #sock.send(message[:8])
    send2(sock, message[:8])
    
    #print "Sent: '%s'" % message[8:]
    #sock.send(message[8:])
    send2(sock, message[8:])
    
    response = sock.recv(1024)
    print "Received: '%s'" % response
    
    return sock
    
if __name__ == '__main__':

    port = 9999; 
    ip = '127.0.0.1'
    #ip = '192.168.1.13'
    
    s1 = client(ip, port, "Hello World 1 ")
    s2 = client(ip, port, "Hello World 2  ")
    s3 = client(ip, port, "Hello World 3   ")

    time.sleep(5)
    
    s1.setblocking(False)
    s2.setblocking(False)
    s3.setblocking(False)
    
    print s1.recv(1024)
    print s2.recv(1024)
    print s3.recv(1024)
    
    s1.close(); s2.close(); s3.close()






