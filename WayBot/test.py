"""Simple example showing how to get gamepad events."""
import serial
import threading
import time
import math

ser = serial.Serial("/dev/ttyS0",38400)

time.sleep(5)
def unlock():
	mass = bytearray(5)
	mass[0] = 255
	mass[1] = 255
	mass[2] = 1
	mass[3] = 113
	mass[4] = ControlMass(mass)
	ser.write(mass)
	time.sleep(0.05)

	mass = bytearray(17)
	mass[0] = 0xff
	mass[1] = 0xff
	mass[2] = 13
	mass[3] = 20
	mass[4] = 73
	mass[16] = ControlMass(mass)
	ser.write(mass)
	time.sleep(0.05)


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
	mass[16] = ControlMass(mass)
	ser.write(mass)
	time.sleep(0.05)

	mass = bytearray(5)
	mass[0] = 255
	mass[1] = 255
	mass[2] = 1
	mass[3] = 36
	mass[4] = ControlMass(mass)
	ser.write(mass)
	print("active")
def ControlMass(mas):
	Summ = 0 
	j=2
	n = mas[2] + 3
	while j <= n:
		Summ = Summ + mas[j]
		j+=1
	Summ = ~Summ
	return abs(Summ%256)

def serials():
	while 1:
		print(ser.read())	
t = threading.Thread(target=serials)
t.start()	
unlock()







