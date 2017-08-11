import pygame
from pygame.locals import *

from threading import Thread

import os
import sys
from termios import tcflush, TCIOFLUSH
import serial, time

from gpiozero import Button
from gpiozero import LED
from time import sleep

#initialize indicators and buttons
button = Button(18)
led1g = LED(23)
led1r = LED(24)
led2g = LED(17)
led2r = LED(27)
ledgate = LED(26)

#initialize status variables
gateState = 0
piggyback = 0

#User Config Variables
#Orienation var for direction that gate is allowing patrons through
#0 for gate on left hand side, 1 for gate on right hand side
orientation = 0

#front sensor sensors
ser1 = serial.Serial('/dev/ttyACM0', 115200)
time.sleep(0.1)
#back sensor sensors
ser2 = serial.Serial('/dev/ttyACM1', 115200)
time.sleep(0.1)

ser4 = serial.Serial('/dev/ttyUSB0', 115200)
time.sleep(0.1)
ser5 = serial.Serial('/dev/ttyUSB1', 115200)
time.sleep(0.1)

#write "T" and "P" in order to initialize terarangers
ser4.write("T")
ser4.write("P")
ser5.write("T")
ser5.write("P")

#motor arduino
ser3 = serial.Serial('/dev/ttyACM2', 115200)
time.sleep(0.1)

#flush all sensors before beginning
ser1.flushInput()
ser2.flushInput()
ser4.flushInput()
ser5.flushInput()

sensors = [0,0,0,0]
smartCard = 0
gate = 0
piggybackThreshold = 0
shortFlag = 0
alarm = 0
incrementLock = 0
led1r.off()
led1g.off()
led2r.off()
led2g.off()

#Timing variables
startCardTimer = False
startIdleTimer = False
startGateTimer = False
piggybackDebounce = False

cardTimer = 0
idleTimer = 0
gateTimer = 0
piggybackDebounceTimer = 0 

#Current state of the machine
currState = 1

#Number of visitors
visitors = 0

#Helper functions
def int_check(s):
	try:
		s = s.strip()
		return int(s) if s else 0
	except(ValueError):
		pass

Running = True

print('Gate Running')
#print('Zones are as follows:')
#print('-----------------')
#print('| 1 | 2 | 3 | 4 |')
#print('-----------------')

while Running:
	time.sleep(0.01)

	if button.is_pressed:
		if (sensors[2] == 0 and sensors[3] == 0):
			ledgate.on()
			if smartCard == 1:
				cardTimer = 0
			elif smartCard == 0:
				smartCard = 1
				currState = 4
				startCardTimer = True
	
#turn on timer if short flag 1
	if gate == 1 or shortFlag == 1:
		startGateTimer = True
	else:
		gateTimer = 0
		startGateTimer = False

#Alarm check
        if alarm == 1:
                if sensors[0] == 0 and sensors[1] == 0 and sensors[2] == 0 and sensors[3] == 0 and shortFlag == 0:
			ser3.write("s")
			#print(gate)
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
				ledgate.off()
	#idleTimer
		if startIdleTimer == True:
			idleTimer += 1
			if idleTimer >= 200:
				alarm = 1
				currState = 1

	#second timer for if gate is open too long
		if startGateTimer == True:
			gateTimer += 1
			if gateTimer >= 200:
				alarm = 1
	
	#Read and process data from sensors serial
	sensorArray1 = ser1.readline()
	sensorArray2 = ser2.readline()
	teraranger1 = ser4.readline()
	teraranger2 = ser5.readline()

	sensor1 = str(sensorArray1)
	sensor2 =str(sensorArray2)
	
	tera1 = int_check(str(teraranger1).strip())
	tera2 = int_check(str(teraranger2).strip())
	
	#print("tera1")
	#print tera1
	#print("\n")
	#print("tera2")
	#print tera2
	#print("\n")
		
	#print(sensor1)
	#print(sensor2)	
	#print(len(sensor1))
	#print(len(sensor2))

	if ((len(sensor1) < 51) or (len(sensor2) < 51)):
		ser1.flushInput()
		#print("flushed ser1")
		ser2.flushInput()
		#print("flushed ser2")
		continue

#Piggyback Detection
	if (currState == 5 or currState == 6):
		if (piggybackThreshold > 220 and piggybackThreshold < 500):
			piggyback = 1
        if sensors[0] == 0 and sensors[1] == 0 and sensors[2] == 0 and sensors[3] == 0 and shortFlag == 0:
		piggyback = 0

	try:
		if((int(sensor2[8]) + int(sensor1[8])) == 0):
			shortFlag = 0
		else:
			shortFlag = 1

		if (int(sensor1[18]) == 1 or (tera1 > 220 and tera1 < 1400)):
			sensors[0] = 1
		else:
			sensors[0] = 0

		if (int(sensor1[8]) == 1):
			sensors[1] = 1
		else:
			sensors[1] = 0

		if (int(sensor2[18]) == 1 or (tera2 > 220 and tera2 < 1400)):
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

#Set orientation
	if orientation == 0:
		sensors = sensors[::-1]
		piggybackThreshold = tera2
		led2r.on()
		ledgate = led1g
		#ledgate.on()
	else:
		piggybackThreshold = tera1
		led1r.on()
		ledgate = led2g
		#ledgate.on()



#piggyback debounce timer			
#	if piggybackDebounce == True:
#		piggybackDebounceTimer += 1
#		if piggybackDebounceTimer >= 10:
#			alarm = 1
#			print("piggyback")

#State Machine
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
		if incrementLock == 0:
			visitors += 1
			incrementLock = 1
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
		ledgate.off()
		ser3.write("c")
		if incrementLock == 1:
			incrementLock = 0
		startIdleTimer = True
		if sensors [3] == 0:
			currState = 1

	f = open('data.txt', 'w')
	printstr = str(sensors[0]) + str(sensors[1]) + str(sensors[2]) + str(sensors[3]) + str(gate) + str(smartCard) + str(currState) + str(shortFlag) + str(orientation) + str(piggyback)
	f.write(printstr)
	f.write("\n")
	f.write(str(visitors))
	f.close()
	
	#print('gate:' + str(gate) + ' sensors:' + str(sensors[0]) + str(sensors[1]) + str(sensors[2]) + str(sensors[3]) + ' card:' + str(smartCard) + ' state:' + str(currState) + " flag:" + str(shortFlag))

	ser1.flushInput()
	ser2.flushInput()
	ser4.flushInput()
	ser5.flushInput()
