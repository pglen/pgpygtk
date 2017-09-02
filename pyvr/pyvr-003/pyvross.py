#!/usr/bin/env python

# ------------------------------------------------------------------------
# Voice recognition input

import ossaudiodev, random, sys, os, wave, audioop, gobject
import threading, sndhdr

from vrutil import  *

class soundthread(threading.Thread):
  
    def __init__(self):
        threading.Thread.__init__(self)
        self.fd =  ossaudiodev.open("/dev/dsp", "rw")
        self.lock = threading.Lock()
        self.event = threading.Event()
        self.finish = threading.Event()
        self.low    = threading.Event()
        self.done = False
        self.params = None
        self.data = []
        print "init thread"

    def addbuff(self, data):
        self.lock.acquire()
        self.data.append(data)
        self.lock.release()
        self.event.set()
                
    def run(self):
        print "run thread"
        if self.params:
            self.fd.setfmt(ossaudiodev.AFMT_S16_LE)
            self.fd.speed(self.params[2])
            self.fd.channels(2)
        else:
            #raise ValueError, "Must set 'params' to wave params"
            # Safety defaults instead
            self.fd.setfmt(ossaudiodev.AFMT_S16_LE)
            self.fd.speed(44100)
            self.fd.channels(2)
        
        while 1:
            print "new event"
            self.event.wait()
            self.event.clear()
            if self.done:
                break
            while 1:
                print "new loop", len(self.data)
                if len(self.data) == 0:
                    break
                             
                data = self.data[0]
                self.fd.write(data)
                
                self.lock.acquire()
                self.data = self.data[1:]
                self.lock.release()
                
                if len(self.data) < 10:
                    self.low.set()
                    
            th.finish.set()    
        print "end thread"
        

def app_tick(th):

    print "app_tick"
    
    #fd =  ossaudiodev.open("/dev/dsp", "rw")
    #fmt = fd.getfmts()
    
    # --------------------------------------------------------------------
    wh = wave.open("test.wav")
    # (nchannels, sampwidth, framerate, nframes, comptype, compname),
    params = wh.getparams()
    
    print params
    th.fd.setfmt(ossaudiodev.AFMT_S16_LE)
    #fd.speed(44100)
    th.fd.speed(params[2])
    th.fd.channels(2)
    
    #print fd.bufsize()
    #print fd.obuffree()
    
    data = ""
    for aa in range(params[3] / 100):
        data = wh.readframes(100)
        
        if params[0] == 1:
            data = audioop.tostereo(data, 2, 1, 1)
        th.fd.write(data)
    
    th.fd.close()
    print "done play"

if __name__ == '__main__':

    #gobject.timeout_add(100, app_tick)
    #print "after gobj"

    snd = sndhdr.what(sys.argv[1])
    #type, sampling_rate, channels, frames, bits_per_sample
    print snd
    #sys.exit()
         
    th = soundthread(); 
    wh = wave.open(sys.argv[1])
    # (nchannels, sampwidth, framerate, nframes, comptype, compname),
    th.params = wh.getparams(); th.start()

    while 1:        
        wh.rewind()
        for aa in range(th.params[3] / 100):
            th.low.clear()               
            data = wh.readframes(100)
            if th.params[0] == 1:
                data = audioop.tostereo(data, 2, 1, 1)
            th.addbuff(data)    
            th.low.wait()               
        
    th.done = True
    th.event.set()
    wh.close()


