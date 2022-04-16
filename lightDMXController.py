import time
import RPi.GPIO as GPIO
from signal import signal, SIGINT
from sys import exit
from ola.ClientWrapper import ClientWrapper

GPIO.setmode(GPIO.BCM)

PWM_FREQ=100
REFRESH_DELAY=int(1000/30)
#default: all pins active as PWM output
enabled_outputs = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]
pwm_pins= [None]*len(enabled_outputs)
pwm_values =[0]*len(enabled_outputs)

def initPWM():
    #for x in range(0,NUMBER_OUTPUT):
    for x in range(0,len(enabled_outputs)):
        GPIO.setup(enabled_outputs[x], GPIO.OUT)
        pwm_pins[x]=GPIO.PWM(enabled_outputs[x],PWM_FREQ)
        pwm_pins[x].start(0)

def stopPWM():
    for x in range(0,len(enabled_outputs)):
        pwm_pins[x].stop()

def updatePWM():
    wrapper.AddEvent(REFRESH_DELAY, updatePWM)
    for x in range(0,len(enabled_outputs)):
        pwm_pins[x].ChangeDutyCycle(int(pwm_values[x]*100/255))

def NewData(data):
    #take the minimum of both array to avoid exception
    for x in range(0,min(len(data),len(enabled_outputs)):
        pwm_values[x]=data[x]

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    stopPWM()
    GPIO.cleanup()
    wrapper.Stop()
    exit(0)


if __name__ == "__main__":
    signal(SIGINT, handler)
    config_file=open("/boot/dmx.config",'r')
    s=config_file.read()
    params = list(map(lambda e : e.split('\t') ,s.split('\n')))
    pins=list(filter(lambda e: e[0]=='pins',params))[0][1].split(',')
    universe=int(list(filter(lambda e: e[0]=='universe',params))[0][1])
    enabled_outputs = list(map(int,pins))
    pwm_pins= [None]*len(enabled_outputs)
    pwm_values =[0]*len(enabled_outputs)
    enabled_outputs=list(map(int,pins))
    print("Starting DMX2PWM. ",len(enabled_outputs)," outputs activated.\nListening on universe ",universe,".")
    # Clear all the pixels to turn them off.
    wrapper = ClientWrapper()
    initPWM()
    client = wrapper.Client()
    client.PatchPort(2, 0, False, OlaClient.PATCH, universe, PatchPortCallback)
    client.RegisterUniverse(universe, client.REGISTER, NewData)
    wrapper.AddEvent(REFRESH_DELAY, updatePWM)
    wrapper.Run()
