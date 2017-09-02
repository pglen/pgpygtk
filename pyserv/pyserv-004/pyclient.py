#!/usr/bin/env python

import os, sys, getopt, signal, select, socket, time, struct
import random, stat

# Test for sequencial send
def send2(sock, message):
    for aa in range(len(message)):
        #print "send '" + message[aa] + "'"
        sock.send(message[aa])

def send3(sock, message):
    strx = struct.pack("!h", len(message))
    #print "Sent: %s" % strx
    sock.send(strx)
    #print "Sent: '%s'" % message[:8]
    sock.send(message)

# ------------------------------------------------------------------------

def client(sock, message):

    send3(sock, message)
    print "Sent: '%s'" % message
    response = sock.recv(1024)
    print "Received: '%s'" % response

data =  "Hello data1" \
        "Hello data2 " \
        "Hello data3 " \
        "Hello data4 " \
        "Hello data5 " \
        "Hello data6 "
        
if __name__ == '__main__':

    port = 9999;
    #ip = '127.0.0.1' 
    ip = '192.168.1.13'

    fh = open("aa")
    flen = os.stat("aa")[stat.ST_SIZE]
    
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect((ip, port))

    client(s1, "user peter")
    client(s1, "pass 1234")
    client(s1, "file bb")
    client(s1, "data " + str(flen))
    
    while 1:
        buff = fh.read(1024)
        if len(buff) == 0:
            break
        send3(s1, buff)
        
    response = s1.recv(1024)
    print "Received: '%s'" % response
     
    client(s1, "quit")

    s1.close();










