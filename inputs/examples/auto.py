import paho.mqtt.client as mqtt
import serial 
from time import sleep
import sys
import threading
from inputs import get_gamepad
import math


i = 0
on_mqtt = True
client = mqtt.Client()
client.connect("192.168.1.49", 1883, 60)
oldauto = False
auto = False   
def timers():
	while 1:
	    global i
	    sleep(1)
	    i = i + 1
	    print (i)
def worker():
	while 1:
	    sleep(1)
	    global i
	    print(i)
	    global auto
	    if auto:
	        if i == 1:
	            print("1")
	            client.publish("admin/BTN_TR", 0)
	            client.publish("admin/ABS_BRAKE", 0)
	            client.publish("admin/ABS_GAS", 2)
	            client.publish("admin/BTN_TL", 1)
	        elif i == 3:
	            print("2")
	            client.publish("admin/BTN_TL", 0)
	            client.publish("admin/ABS_GAS", 0)
	            client.publish("admin/ABS_BRAKE", 2)
	            client.publish("admin/BTN_TR", 1)
	        elif i == 4:
	            print("3")
	            i=0
	            
	    if oldauto and not auto:
	            client.publish("admin/BTN_TR", 0)
	            client.publish("admin/ABS_GAS", 0)
	            client.publish("admin/BTN_TL", 0)
	            client.publish("admin/ABS_BRAKE", 0)
		
def serials():
	while 1:
		test = ser.read();

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("enable")
	
def on_message(client, userdata, msg):
	global auto
	global oldauto
	global i
	sleep(1)
	print(msg.topic+" "+str(msg.payload.decode("utf-8")))
	if msg.topic == "enable":
		if str(msg.payload.decode("utf-8")) == 'false':
			if not auto:
				print("true")
				if i > 30:
					auto = True
					oldauto = False
					i = 0
				else:
					auto = False
					oldauto = True
		elif str(msg.payload.decode("utf-8")) == "true":
			print("true")
			auto = False
			if not oldauto:
				oldauto = True
				i = 0
			
			
			
			
			
		
t = threading.Thread(target=timers)
t.start()
t = threading.Thread(target=worker)
t.start()
client.on_connect = on_connect
client.on_message = on_message


client.loop_forever()