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
client.connect("192.168.8.102", 1883, 60)

auto = False;
def worker():
	while 1:
		global speedY
		global speedZ
		events = get_gamepad()
		for event in events:
			if event.code == 'BTN_EAST':
			    if event.state == 1:
    				print("say")
    				client.publish("admin/say", "Play;Добро пожаловать в зоопарк")
			if event.code == 'BTN_WEST':
			    if event.state == 1:
    				print("say")
    				client.publish("admin/say", "Play;Вы можете приобрести билеты у меня")
			if event.code == 'BTN_SOUTH':
			    if event.state == 1:
    				print("say")
    				client.publish("admin/say", "Play;Привет я ВэйБот.")
			if event.code == 'BTN_NORTH':
			    if event.state == 1:
    				print("say")
    				client.publish("admin/say", "Play;Я не кусаюсь. Разработчики не вложили в меня такой функции")
			

	return 

#	while 1:
#		print(ser.read())
t = threading.Thread(target=worker)
t.start()


client.loop_forever()