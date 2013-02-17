#!/usr/bin/python

import pjsua as pj
import threading
import datetime
from keypad import RaspiBoard
import time

LOG_LEVEL_PJSIP = 3
SIP_SERVER="192.168.1.10"
SIP_USER="raspi"
SIP_PASS="1111"
SIP_REALM="asterisk"
SIP_LOCAL_PORT=5072

def log(msg):
    print "[",datetime.datetime.now(), "] ", msg

def pj_log(level, msg, length):
    msg = msg.replace("\n","\n\t")
    print "[PJ] " + msg, 

class DBCallCallback(pj.CallCallback):

    def __init__(self, call=None):
        pj.CallCallback.__init__(self, call)
        
    def on_media_state(self):
        print "***** ON MEDIA STATE " , self.call.info()
        if self.call.info().media_state == pj.MediaState.ACTIVE:
            # Connect the call to sound device
            call_slot = self.call.info().conf_slot
            pj.Lib.instance().conf_connect(call_slot, 0)
            pj.Lib.instance().conf_connect(0, call_slot)
            print "Media is now active"
        else:
            print "Media is inactive"
            
    def on_state(self):
        print "**** ON STATE ", self.call
        print self.call.dump_status()
        #pj.CallCallback.on_state(self)
        
class DBAccountCallback(pj.AccountCallback):
    sem = None

    def __init__(self, account = None):
        pj.AccountCallback.__init__(self, account)

    def wait(self):
        self.sem = threading.Semaphore(0,verbose=True)
        self.sem.acquire()

    def on_reg_state(self):
        if self.sem:
            if self.account.info().reg_status >= 200:
                self.sem.release()
    def on_incoming_call(self, call):
        cb = DBCallCallback(call)
        call.set_callback(cb)
        call.answer(200,'')

class DoorStation:
    lib = None
    acc = None
    acc_cb = None
    _call = None
    
    def __init__(self):
        lib = pj.Lib()

        try:
            ua= pj.UAConfig()
            ua.user_agent = "DoorBerry UA"
            #ua.max_calls = 1
       
            mc = pj.MediaConfig()
#            mc.no_vad = False
#            mc.ec_tail_len = 800 
            mc.clock_rate = 8000

            lib.init(ua_cfg = ua, log_cfg = pj.LogConfig(level=LOG_LEVEL_PJSIP, callback=pj_log), media_cfg=mc)
            lib.create_transport(pj.TransportType.UDP, pj.TransportConfig(SIP_LOCAL_PORT))
            lib.start()
        
            # temporary workaround on RPi
            #pj.Lib.instance().set_snd_dev(1, 0) 
            acc_cfg = pj.AccountConfig()
            acc_cfg.id = "sip:" + SIP_USER + "@" + SIP_SERVER
            acc_cfg.reg_uri = "sip:" + SIP_SERVER
            acc_cfg.auth_cred = [ pj.AuthCred(SIP_REALM, SIP_USER, SIP_PASS) ]
            acc_cfg.allow_contact_rewrite = False
            self.acc = lib.create_account(acc_cfg)
            log("Account created")

        except pj.Error, e:
            log("Exception: " + str(e))

    def print_media_cfg(self,mc):
            print "no vad",mc.no_vad
            print "audio frame type ", mc.audio_frame_ptime
            print "channel count ",mc.channel_count
            print "clock rate ",mc.clock_rate
            print "ec options ",mc.ec_options
            print "ec tail len ",mc.ec_tail_len
            print "ilbc mode ",mc.ilbc_mode
            print "jb max ",mc.jb_max
            print "jb min ",mc.jb_min
            print "max media ports ",mc.max_media_ports
            print "no vad ",mc.no_vad
            print "ptime ",mc.ptime
            print "quality ",mc.quality
            print "snd clock rate ",mc.snd_clock_rate

    def start(self):
        self.acc_cb = DBAccountCallback(self.acc)
        self.acc.set_callback(self.acc_cb)
        #self.acc_cb.wait()

    def call(self):
        if (self._call != None and self._call.is_valid()):
            print "call in progress -> SKIP"
            return

        self._call = self.acc.make_call("sip:100@"+SIP_SERVER, DBCallCallback())
    
    def stop(self):
        try:
            self.acc.delete()
            self.acc = None
            #self.lib = None
        except pj.Error, e:
            log("Exception: " + str(e))
    
class DoorBerry:
    
    station = None
    keyboard = None    
    
    def __init__(self):
        self.station = DoorStation()
        self.keyboard = RaspiBoard()

    def run(self):
        try:
            #station = DoorStation()
            self.station.start()
            #keyboard = RaspiBoard()
   
            log("entering main loop") 
            while True:
                key = self.keyboard.keyPressed()
                if(key == 0): 
                    time.sleep(0.2)
                    continue
       
                log("Selected extension =" + str(key))
        
                if(key ==  1):
                    try:
                        log("calling extension 1")
                        self.station.call()
                    except pj.Error, ee:
                        print ee
                    time.sleep(2)
                
        except Exception, e:
            print e
