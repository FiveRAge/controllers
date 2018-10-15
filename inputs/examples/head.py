"""Simple example showing how to get gamepad events."""

from __future__ import print_function


from inputs import get_gamepad
import serial
import threading
import time 
import math
import paho.mqtt.client as mqtt
time.sleep(2) 
ser = serial.Serial("/dev/ttyS2",115200)
time.sleep(2)

client = mqtt.Client()
client.connect("192.168.1.49", 1883, 60)

auto = False;
def worker():
	while 1: 
		global speedY
		global speedZ
		events = get_gamepad()
		for event in events:
			global auto
			if auto:
				if event.code == 'ABS_HAT0Y':
					speedZ = event.state;
				if event.code == 'ABS_HAT0X': 
					speedY = event.state;
			
		if event.code == 'BTN_START':
			if event.state == 1:
				auto = not auto
				print("diactive")

	return 

speedY = 0
speedZ = 0
def seriall():
	global speedY
	while 1:
		if speedY > 0:
			time.sleep(0.05)
			ser.write(b"<turn1:0>")
			time.sleep(0.05)
			ser.write(b"<speed1:5>")
			print("left")
	
		elif speedY < 0:
			time.sleep(0.05)
			ser.write(b"<turn1:1>")
			time.sleep(0.05)
			ser.write(b"<speed1:5>")
			print("right")
			
		if speedY == 0:
			time.sleep(0.05)
			ser.write(b"<stop1:0>")
			#print("stop")
			
			
		if speedZ > 0:
			time.sleep(0.05)
			ser.write(b"<turn2:0>")
			time.sleep(0.05)
			ser.write(b"<speed2:5>")
			print("left1")
	
		elif speedZ < 0:
			time.sleep(0.05)
			ser.write(b"<turn2:1>")
			time.sleep(0.05)
			ser.write(b"<speed2:5>")
			print("right1")
			
		elif speedZ == 0:
			time.sleep(0.05)
			ser.write(b"<stop2:0>") 
			#print("stop")
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("admin/ABS_RZ")
    client.subscribe("admin/ABS_Z")
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	global speedY
	
	if not auto:
		print(msg.topic+" "+str(msg.payload.decode("utf-8")))
		if msg.topic == "admin/ABS_RZ":
			speedZ = (int(msg.payload.decode("utf-8")));
			
		if msg.topic == "admin/ABS_Z":
			speedY = -(int(msg.payload.decode("utf-8")));
#	while 1:
#		print(ser.read())
t = threading.Thread(target=worker)
t.start()

t1 = threading.Thread(target=seriall)
t1.start()
    
    
client.on_connect = on_connect
client.on_message = on_message


client.loop_forever()