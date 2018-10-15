"""Simple example showing how to get gamepad events."""
import serial
import threading
import time
import math

ser = serial.Serial("/dev/ttyS2",115200)

time.sleep(5)
def serials():
	while 1:
		print(ser.read())	
t = threading.Thread(target=serials)
t.start()	
unlock()







