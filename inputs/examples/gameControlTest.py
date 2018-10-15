import paho.mqtt.client as mqtt
import serial 
from time import sleep
import sys
import threading
from inputs import get_gamepad
import math
import rcpy.led as led
from rcpy.led import red, green
blink = led.Blink(red, .5)

debug = False
on_serial = True
on_mqtt = False

client = mqtt.Client()
if on_mqtt:
	client.connect("192.168.1.49", 1883, 60)
ser = serial.Serial("/dev/ttyS5",38400)
ser.close()
ser.open()
Vmax = 800
direct = "forward"
direct1 = "forward"
X = 0
Y = 0
Y1 = 0
getData = False
def seral():
	while 1:
		global getData
		test = ser.read();
		print (test)
		if test:
			print("stop")
			getData = True
def worker():
	global X
	global Y
	global Y1
	while 1:
		events = get_gamepad()
		for event in events:
			if (event.code == 'ABS_Y'):
				Y = -(event.state-128)
			if (event.code == 'ABS_RZ'):
				Y1 = -(event.state-128)
def run():
	v0 = 0
	while 1:
		global X
		global Y
		global Y1
		global direct
		global direct1
	#	print("X = ", X, " Y = ",Y)
		v0 = math.ceil(abs((Y/128)*Vmax))
		if (Y > 0 and direct != "forward"):
			sleep(0.009)
			dir1(191)
			direct = "forward"
			sleep(0.009)
		else:
			speed(math.ceil(v0),1)
			
		if (Y < 0 and direct != "back"):
			sleep(0.009)
			dir1(192)
			direct = "back"
			sleep(0.009)
		else:
			speed(math.ceil(v0),1)
		v1 = math.ceil(abs((Y1/128)*Vmax))
		if (Y1 > 0 and direct1 != "forward"):
			sleep(0.009)
			dir2(193)
			direct1 = "forward"
			sleep(0.009)
		else:
			speed(math.ceil(v1),2)
		if (Y1 < 0 and direct1 != "back"):
			sleep(0.009)
			dir2(194)
			direct1 = "back"
			sleep(0.009)
		else:
			speed(math.ceil(v1),2)
			
def serials():
    while 1:
        print()
        print(ser.read())
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
	
	
def dir1(a):
	speed(0, 3)
	mass = bytearray(5)
	mass[0] = 0xff
	mass[1] = 0xff
	mass[2] = 1
	mass[3] = a
	mass[4] = ControlSumm(mass)
	send(mass)
	sleep(0.009)
	
def dir2(a):
	speed(0, 3)
	mass = bytearray(5)
	mass[0] = 0xff
	mass[1] = 0xff
	mass[2] = 1
	mass[3] = a
	mass[4] = ControlSumm(mass)
	send(mass)
	sleep(0.009)
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
		sleep(0.005)
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
	blink.start()
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
		print("send")
		sleep(0.005)
		#changedir(1)
		global getData
		sleep(1)
		if getData:
			blink.stop()
			
			break
	client.publish("admin/status","Ноги запущены");
	
	
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("admin/ABS_Y")
    client.subscribe("admin/ABS_X")
    
v0 = 0
Y = 0
X= 0
	
def on_message(client, userdata, msg):
	global v0 
	global Y 
	global X
	print(msg.topic+" "+str(msg.payload))
	global direct
	if (msg.topic == "admin/ABS_Y"):
		Y = int(str(msg.payload.decode("utf-8")))-128
			
	if (msg.topic == "admin/ABS_X"):
		Y1 = int(str(msg.payload.decode("utf-8"))) - 128
		

t = threading.Thread(target=seral)
t.start()
init()
t = threading.Thread(target=worker)
t.start()
t = threading.Thread(target=run)
t.start()
client.on_connect = on_connect
client.on_message = on_message


client.loop_forever()