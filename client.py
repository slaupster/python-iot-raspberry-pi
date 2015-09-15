import RPi.GPIO as GPIO
import time
import os, json
import ibmiotf.device
import uuid

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.OUT)

def myCommandCallback(cmd):
    print "Received command %s %s" % (cmd.command, cmd.data)
    if cmd.command == "light":
        if cmd.data["command"] == "on":
            GPIO.output(17, True)
        elif cmd.data["command"] == "off":
            GPIO.output(17, False)

try:
    options = ibmiotf.device.ParseConfigFile("/home/me/device.cfg")
    client = ibmiotf.device.Client(options)
    client.connect()
    client.commandCallback = myCommandCallback
    
    while True:
        GPIO.wait_for_edge(18, GPIO.FALLING)
        print "Button Pushed"
        myData = {'buttonPushed' : True}
        client.publishEvent("raspberrypievt", "json", myData)
        time.sleep(0.2)

except ibmiotf.ConnectionException  as e:
    print e
