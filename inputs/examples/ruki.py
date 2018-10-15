import paho.mqtt.client as mqtt
import serial 
from time import sleep
import sys
import threading
from inputs import get_gamepad
import math
from rcpy.led import red, green


debug = True
on_serial = True
on_mqtt = False

ser = serial.Serial("/dev/ttyS1",38400)

client = mqtt.Client()
if on_mqtt: 
	client.connect("192.168.1.49", 1883, 60)
ser.close()
ser.open()
Vmax = 600
left = True;
right = True;
getData = False   
def worker():
	global left
	global right
	while 1:
		events = get_gamepad()
		for event in events:
			print("event")
			if event.code == "BTN_TR":
				if event.state == 1:
					if right:
						direction(1,2)
						right = False
						sleep(0.005)
					speed(Vmax, 1)
				elif event.state == 0:
					speed(0, 1)
			if event.code == "BTN_TL":
				if event.state == 1:
					if left:
						direction(2,2)
						left = False
						sleep(0.005)
					speed(Vmax, 2)
				elif event.state == 0:
					speed(0, 2)
			
			if event.code == "ABS_GAS":
				if event.state > 1:
					if not right:
						direction(1,1)
						right = True
						sleep(0.005)
					speed(Vmax, 1)
				elif event.state == 0:
					speed(0, 1)
			
			if event.code == "ABS_BRAKE":
				if event.state > 1:
					if not left:
						direction(2,1)
						left = True
						sleep(0.005)
					speed(Vmax, 2)
				elif event.state == 0:
					speed(0, 2)
			
			
		
		
def serials():
	while 1:
		global getData
		test = ser.read();
		print (test)
		if test:
			print("stop")
			getData = True
def ControlSumm(mas):
	Summ = 0
	i = 2
	n = mas[2] + 3
	while i <= n:
		Summ = Summ + mas[i]
		i+=1

	Summ = ~Summ
	return abs(Summ%256)

def send(mass):
	if debug:
		print(mass)
	ser.write(mass)
	
	

def direction(n,i):
	if n == 1:
		if i == 1:
			mass = bytearray(5)
			mass[0] = 0xff
			mass[1] = 0xff
			mass[2] = 1
			mass[3] = 191
			mass[4] = ControlSumm(mass)
			send(mass)
		if i == 2:
			mass = bytearray(5)
			mass[0] = 0xff
			mass[1] = 0xff
			mass[2] = 1
			mass[3] = 192
			mass[4] = ControlSumm(mass)
			send(mass)
	if n == 2:
		if i == 1:
			mass = bytearray(5)
			mass[0] = 0xff
			mass[1] = 0xff
			mass[2] = 1
			mass[3] = 193
			mass[4] = ControlSumm(mass)
			send(mass)
		if i == 2:
			mass = bytearray(5)
			mass[0] = 0xff
			mass[1] = 0xff
			mass[2] = 1
			mass[3] = 194
			mass[4] = ControlSumm(mass)
			send(mass)
def speed(n, i):
	Trmm = int(n)
	if i == 1 or i == 3:
		mass = bytearray(7)
		mass[0] = 0xff
		mass[1] = 0xff
		mass[2] = 3
		mass[3] = 22
		mass[4] = Trmm%256
		mass[5] = (Trmm >> 8)%256 
		mass[6] = ControlSumm(mass)
		send(mass)
		sleep(0.002)
	if i == 2 or i == 3:
		mass = bytearray(7)
		mass[0] = 0xff
		mass[1] = 0xff
		mass[2] = 3
		mass[3] = 226
		mass[4] = Trmm%256
		mass[5] = (Trmm >> 8)%256 
		mass[6] = ControlSumm(mass)
		send(mass)


def init():
	while 1:
		
		mass = bytearray(5)
		mass[0] = 255
		mass[1] = 255
		mass[2] = 1
		mass[3] = 113
		mass[4] = ControlSumm(mass)
		ser.write(mass)
		sleep(0.005)
	
		mass = bytearray(17)
		mass[0] = 0xff
		mass[1] = 0xff
		mass[2] = 13
		mass[3] = 20
		mass[4] = 73
		mass[16] = ControlSumm(mass)
		ser.write(mass)
		sleep(0.005)
	
	
		mass = bytearray(17)
		mass[0] = 0xff
		mass[1] = 0xff
		mass[2] = 13
		mass[3] = 232
		mass[4] = 185
		mass[5] = 211
		mass[6] = 11
		mass[7] = 193
		mass[8] = 72
		mass[9] = 95
		mass[10] = 123
		mass[11] = 19
		mass[12] = 228
		mass[13] = 117
		mass[14] = 3
		mass[15] = 55
		mass[16] = ControlSumm(mass)
		ser.write(mass)
		sleep(0.005)
	
		mass = bytearray(5)
		mass[0] = 255
		mass[1] = 255
		mass[2] = 1
		mass[3] = 36
		mass[4] = ControlSumm(mass)
		ser.write(mass)
		sleep(0.005)
		
		global getData
		sleep(1)
		if getData:
			#blink.stop()
			m = 0;
			break
	client.publish("admin/status","Руки запущены");
	
	
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("admin/BTN_TR")
    client.subscribe("admin/BTN_TL")
    client.subscribe("admin/ABS_BRAKE")
    client.subscribe("admin/ABS_GAS")
	
def on_message(client, userdata, msg):
	global left
	global right
	print(msg.topic+" "+str(msg.payload))
	if msg.topic == "admin/BTN_TR":
		if int(str(msg.payload.decode("utf-8"))) == 1:
			if right:
				direction(1,2)
				right = False
				sleep(0.005)
			speed(Vmax, 1)
		elif int(str(msg.payload.decode("utf-8"))) == 0:
			speed(0, 1)
	if msg.topic == "admin/BTN_TL":
		if int(str(msg.payload.decode("utf-8"))) == 1:
			if left:
				direction(2,2)
				left = False
				sleep(0.005)
			speed(Vmax, 2)
		elif int(str(msg.payload.decode("utf-8"))) == 0:
			speed(0, 2)
	
	if msg.topic == "admin/ABS_GAS":
		if int(str(msg.payload.decode("utf-8"))) > 1:
			if not right:
				direction(1,1)
				right = True
				sleep(0.005)
			speed(Vmax, 1)
		elif int(str(msg.payload.decode("utf-8"))) == 0:
			speed(0, 1)
	
	if msg.topic == "admin/ABS_BRAKE":
		if int(str(msg.payload.decode("utf-8"))) > 1:
			if not left:
				direction(2,1)
				left = True
				sleep(0.005)
			speed(Vmax, 2)
		elif int(str(msg.payload.decode("utf-8"))) == 0:
			speed(0, 2)												
		
t = threading.Thread(target=serials)
t.start()
init()
t = threading.Thread(target=worker)
t.start()
client.on_connect = on_connect
client.on_message = on_message


client.loop_forever()