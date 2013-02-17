import RPi.GPIO as GPIO
import time
import os

class RaspiBoard():

    OUT1=24
    OUT2=23
    OUT3=18
    
    IN1=22
    IN2=17
    IN3=4

    def __init__(self):
        '''
        Constructor        '''
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.OUT1, GPIO.OUT)
        GPIO.setup(self.OUT2, GPIO.OUT)
        GPIO.setup(self.OUT3, GPIO.OUT)
    
        GPIO.setup(self.IN1, GPIO.IN)
        GPIO.setup(self.IN2, GPIO.IN)
        GPIO.setup(self.IN3, GPIO.IN)

    def destroy(self):
        GPIO.cleanup()
        
    def on(self,out):
        GPIO.output(out, True)
    
    def off(self,out):
        GPIO.output(out, False)
    
    def wait(self,sec):
        time.sleep(sec)
    
    def flash(self,out, sec):
        self.on(out)
        self.wait(sec)
        self.off(out)

