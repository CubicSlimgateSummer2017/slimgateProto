import pygame
from pygame.locals import *

from threading import Thread

import os
import sys
from termios import tcflush, TCIOFLUSH
import serial, time

from gpiozero import LED
from time import sleep

motorPin = LED(18)
dirPin = LED(23)
gateState = 0

#front sensor sensors
ser1 = serial.Serial('/dev/ttyACM0', 115200)
#back sensor sensors
ser2 = serial.Serial('/dev/ttyACM1', 115200)
ser4 = serial.Serial('/dev/ttyUSB0', 115200)
ser4.write("T")
ser4.write("P")

#motor arduino
ser3 = serial.Serial('/dev/ttyACM2', 115200)

#flush all sensors before beginning
ser1.flushInput()
ser2.flushInput()
ser4.flushInput()

sensors = [0,0,0,0]
smartCard = 0
gate = 0
shortFlag = 0
alarm = 0

#Timing variables
startCardTimer = False
startIdleTimer = False
startGateTimer = False
cardTimer = 0
idleTimer = 0
gateTimer = 0

#Current state of the machine
currState = 1

#Helper functions
def int_check(s):
	s = s.strip()
	return int(s) if s else 0

pygame.init()

pygame.display.set_mode((100,100))

Running = True

print('Zones are as follows:')
print('-----------------')
print('| 1 | 2 | 3 | 4 |')
print('-----------------')

while Running:
#	time.sleep(0.1)
	for event in pygame.event.get():
		if event.type == QUIT:
			Running = False
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				Running = False
			elif event.key == K_SPACE:
				print("all sensors reset and current state set to 1")
				ser3.write("s")
				alarm = 0
				startCardTimer = False
				startIdleTimer = False
				cardTimer = 0
				idleTimer = 0
				sensors = [0,0,0,0]
				smartCard = 0
				currState = 1
				ser3.write("o")
				time.sleep(0.1)
				ser3.write("c")
			elif event.key == K_c:
				if smartCard == 1:
					cardTimer = 0
				elif smartCard == 0:
					smartCard = 1
					currState = 4
					startCardTimer = True
	#turn on timer if safe flag 1
	if gate == 1 or shortFlag == 1:
		startGateTimer = True
	else:
		gateTimer = 0
		startGateTimer = False

#Alarm check
        if alarm == 1:
                if sensors[0] == 0 and sensors[1] == 0 and sensors[2] == 0 and sensors[3] == 0 and shortFlag == 0:
			ser3.write("s")
			print(gate)
			alarm = 0
                        if startIdleTimer == True:
                                idleTimer = 0
                                startIdleTimer = False
                        if startGateTimer == True:
                                gateTimer = 0
                                startGateTimer = False
			if gate == 1:
				ser3.write("c")
				gate = 0
                else:
			ser3.write("a")
			alarm = 0
                        print("ALARM")
	elif alarm == 0:
		ser3.write("s")

#Timer rules
        if startCardTimer == True:
                cardTimer += 1
                # while loop runs every 0.1 seconds, 10 = roughly 1 sec(not accounting for program runtime)
                if cardTimer >= 300:
                        startCardTimer = False
                        smartCard = 0
                        cardTimer = 0
        #idleTimer
        if startIdleTimer == True:
                idleTimer += 1
                if idleTimer >= 300:
                        alarm = 1
                        currState = 1

        #second timer for if gate is open too long
        if startGateTimer == True:
                gateTimer += 1
                if gateTimer >= 300:
                        alarm = 1
	
	sensorArray1 = ser1.readline()
	sensorArray2 = ser2.readline()
	teraranger1 = ser4.readline()

	sensor1 = str(sensorArray1)
	sensor2 =str(sensorArray2)
	
	tera1 = int_check(str(teraranger1).strip())
	
	print tera1
		
	print(sensor1)
	print(sensor2)	
	print(len(sensor1))
	print(len(sensor2))

	if ((len(sensor1) < 51) or (len(sensor2) < 51)):
		ser1.flushInput()
		print("flushed ser1")
		ser2.flushInput()
		print("flushed ser2")
		continue
	
	try:
		if((int(sensor2[8]) + int(sensor1[8])) == 0):
			shortFlag = 0
		else:
			shortFlag = 1

		if (int(sensor1[18]) == 1 or (tera1 > 220 and tera1 < 2000)):
			sensors[0] = 1
		else:
			sensors[0] = 0

		if (int(sensor1[8]) == 1):
			sensors[1] = 1
		else:
			sensors[1] = 0

		if (int(sensor2[18]) == 1):
			sensors[3] = 1
		else:
			sensors[3] = 0

		if (int(sensor2[8]) == 1):
			sensors[2] = 1
		else:
			sensors[2] = 0

	except (ValueError, IndexError):
#		print("parse error, passing")
		continue

#Set state rules

	if currState == 1:
#		startIdleTimer = True
		if (sensors[1] or sensors[2] or sensors[3] == 1):
		       startIdleTimer = True
		
		elif (sensors[0] == 1):
			startIdleTimer = False
			idleTimer = 0
			currState = 2
#               elif (sensors[1] or sensors[2] or sensors[3] == 1):
#                       startIdleTimer = True
	elif currState == 2:
		startIdleTimer = True
		if sensors[1] == 1:
			startIdleTimer = False
			idleTimer = 0
			currState = 3
	elif currState == 3:
		startIdleTimer = True
		if smartCard == 1:
			startIdleTimer = False
			idleTimer = 0
			currState = 4
	elif currState == 4:
		startIdleTimer = True
		startGateTimer = True
		gate = 1
		ser3.write("o")
		if sensors[2] == 1:
			startIdleTimer = False
			idleTimer = 0
			currState = 5
	elif currState == 5:
		startGateTimer = True
		if sensors[2] == 0 and shortFlag == 0:
			startGateTimer = False
			gateTimer = 0
			currState = 6
	elif currState == 6:
                smartCard = 0
#		if gate == 1:
#                	gate = 0
#			ser3.write("c")
		if sensors[3] == 1 or shortFlag == 0:
			currState = 7
	elif currState == 7:
		smartCard = 0
		gate = 0
		ser3.write("c")
		startIdleTimer = True
		if sensors [3] == 0:
			currState = 1

	print('gate:' + str(gate) + ' sensors:' + str(sensors[0]) + str(sensors[1]) + str(sensors[2]) + str(sensors[3]) + ' card:' + str(smartCard) + ' state:' + str(currState) + " flag:" + str(shortFlag))

	ser1.flushInput()
	ser2.flushInput()
	ser4.flushInput()
