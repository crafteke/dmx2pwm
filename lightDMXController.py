import time
import RPi.GPIO as GPIO
from signal import signal, SIGINT
from sys import exit
from ola.ClientWrapper import ClientWrapper

GPIO.setmode(GPIO.BCM)

NUMBER_OUTPUT=28
PWM_FREQ=100
REFRESH_DELAY=int(1000/30)

pwm_pins= [None]*NUMBER_OUTPUT
pwm_values =[0]*NUMBER_OUTPUT

def initPWM():
    for x in range(0,NUMBER_OUTPUT):
        GPIO.setup(x, GPIO.OUT)
        pwm_pins[x]=GPIO.PWM(x,PWM_FREQ)
        pwm_pins[x].start(0)

def stopPWM():
    for x in range(0,NUMBER_OUTPUT):
        pwm_pins[x].stop()

def updatePWM():
    wrapper.AddEvent(REFRESH_DELAY, updatePWM)
    for x in range(0,NUMBER_OUTPUT):
        pwm_pins[x].ChangeDutyCycle(int(pwm_values[x]*100/255))

def NewData(data):
    for x in range(0,NUMBER_OUTPUT):
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
    # Clear all the pixels to turn them off.
    wrapper = ClientWrapper()
    initPWM()
    client = wrapper.Client()
    client.RegisterUniverse(3, client.REGISTER, NewData)
    wrapper.AddEvent(REFRESH_DELAY, updatePWM)
    wrapper.Run()
