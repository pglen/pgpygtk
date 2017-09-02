#!/usr/bin/env python

# ------------------------------------------------------------------------
# Voice recognition input

import ossaudiodev, random, sys, os, wave, audioop, gobject
import threading

from vrutil import  *

class soundthread(threading.Thread):
  
    def __init__(self):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.event = threading.Event()
        self.done = False
        print "init thread"
        
    def run(self):
        print "run thread"
        #usleep(1000)
        #self.lock.acquire()
        while 1:
            self.event.wait()
            self.event.clear()
            if self.done:
                self.event.clear()
                break
            app_tick()
        print "end thread"

def app_tick():

    print "app_tick"
    
    fd =  ossaudiodev.open("/dev/dsp", "rw")
    fmt = fd.getfmts()
    '''if (fmt & ossaudiodev.AFMT_U16_LE) == ossaudiodev.AFMT_U16_LE:
        print  "AFMT_U16_LE"
    if (fmt & ossaudiodev.AFMT_U16_BE) == ossaudiodev.AFMT_U16_BE:
        print  "AFMT_U16_BE"
    
    if (fmt & ossaudiodev.AFMT_IMA_ADPCM) == ossaudiodev.AFMT_IMA_ADPCM:
        print  "AFMT_IMA_ADPCM"
         
    if (fmt & ossaudiodev.AFMT_A_LAW) == ossaudiodev.AFMT_A_LAW:
        print  "AFMT_A_LAW"
    if (fmt & ossaudiodev.AFMT_MU_LAW) == ossaudiodev.AFMT_MU_LAW:
        print  "AFMT_MU_LAW"
                              
    if fmt & ossaudiodev.AFMT_S16_LE:
        print  "AFMT_S16_LE"
    if fmt & ossaudiodev.AFMT_S16_BE:
        print  "AFMT_S16_BE"
    
    if fmt & ossaudiodev.AFMT_U8:
        print "AFMT_U8"
    if fmt & ossaudiodev.AFMT_S8:
        print "AFMT_S8"'''
                
    # --------------------------------------------------------------------
    wh = wave.open("test.wav")
    # (nchannels, sampwidth, framerate, nframes, comptype, compname),
    params = wh.getparams()
    
    print params
    fd.setfmt(ossaudiodev.AFMT_S16_LE)
    #fd.speed(44100)
    fd.speed(params[2])
    fd.channels(2)
    
    #print fd.bufsize()
    #print fd.obuffree()
    
    data = ""
    for aa in range(params[3] / 100):
        data = wh.readframes(100)
        
        if params[0] == 1:
            data = audioop.tostereo(data, 2, 1, 1)
        fd.write(data)
    
    fd.close()
    print "done play"
    

if __name__ == '__main__':

    #gobject.timeout_add(100, app_tick)
    #print "after gobj"
    
    th = soundthread()
    th.start()
    print "created thread, waiting"
    usleep(1000)
    th.event.set()
    
    #usleep(1000)
    th.event.set()
    
    usleep(1000)
    th.done = True
    th.event.set()


