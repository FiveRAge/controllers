import paho.mqtt.client as mqtt
import serial 
from time import sleep
import sys
import threading

debug = True
on_serial = True
on_mqtt = True

ser = serial.Serial(sys.argv[1],38400)
ser.close()
ser.open()
def serials():
    while 1:
        print(ser.read())
def ControlSumm(mas):
	Summ = 0
	i = 2
	n = mas[2] + 3
	while i <= n:
		Summ = Summ + mas[i]
		i+=1

	Summ = ~Summ
	print( abs(Summ%256))
	return abs(Summ%256)

def send(mass):
	if debug:
		print(mass)
	ser.write(mass)
def changedir(dir):
	speed(0)
	if dir == 1:
		direction(191, 193)
	if dir == 2:
		direction(192, 194)
	if dir == 3:
		direction(191, 194)
	if dir == 4:
		direction(192, 193)
	
def direction(a, b):
	mass = bytearray(5)
	mass[0] = 0xff
	mass[1] = 0xff
	mass[2] = 1
	mass[3] = a
	mass[4] = ControlSumm(mass)
	send(mass)
	sleep(0.5)
	mass = bytearray(5)
	mass[0] = 0xff
	mass[1] = 0xff
	mass[2] = 1
	mass[3] = b
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
		sleep(0.5)
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
	
	mass = bytearray(5)
	mass[0] = 255
	mass[1] = 255
	mass[2] = 1
	mass[3] = 113
	mass[4] = ControlSumm(mass)
	ser.write(mass)
	sleep(0.05)

	mass = bytearray(17)
	mass[0] = 0xff
	mass[1] = 0xff
	mass[2] = 13
	mass[3] = 20
	mass[4] = 73
	mass[16] = ControlSumm(mass)
	ser.write(mass)
	sleep(0.05)


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
	sleep(0.05)

	mass = bytearray(5)
	mass[0] = 255
	mass[1] = 255
	mass[2] = 1
	mass[3] = 36
	mass[4] = ControlSumm(mass)
	ser.write(mass)
	print("send")
	
	
	
	
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe(sys.argv[2])

	
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	mess = msg.payload.decode('utf-8')
	mes = mess.split(';')
	print(mes)
	if mes[0] == 'rotate':
		if mes[1] == "forward":
			changedir(1)
		elif mes[1] == "back":
			changedir(2)
		elif mes[1] == "left":
			changedir(3)
		elif mes[1] == "right":
			changedir(4)
	elif mes[0] == 'stop':
		speed(0, 3)
	elif mes[0] ==  'run':
		print(mes[1])
		speed(mes[1], mes[2])
		
t = threading.Thread(target=serials)
t.start()
init()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

if on_mqtt:
	client.connect("192.168.7.2", 1883, 60)
client.loop_forever()