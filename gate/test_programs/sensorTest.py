#final version of gate state machine simulation

import pygame
from pygame.locals import *
import sys
import time

#define sensor variables

#current mapping:
#sensors[0] = sensor 1
#sensors[1] = sensor 2
#sensors[2] = sensor 3
#sensors[3] = sensor 4

sensors=[0,0,0,0,0,0]
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

#stateStack = []
#prevState = 0
currState = 1


#define helper functions
#def reset(bool):
#	if bool == True:
#		print(sensors[0])
#		sensors[0] = 1
#		smartCard = 0
#		currState = 1
#	return


#start program
pygame.init()

pygame.display.set_mode((100, 100))

Running = True

print('Zones are as follows:')
print('-----------------')
print('| 1 | 2 | 3 | 4 |')
print('-----------------')


while Running:
	time.sleep(0.1)

#main loop

	for event in pygame.event.get():
		if event.type == QUIT:
			Running = False
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				Running = False

			elif event.key == K_SPACE:
				print("All sensors reset and current state set to 1")
				startCardTimer = False
				startIdleTimer = False
				cardTimer = 0
				idleTimer = 0
				sensors = [0,0,0,0,0,0]
				smartCard = 0
				currState = 1
				alarm = 0

			elif event.key == K_q:
				if sensors[0] == 1:
					sensors[0] = 0
				elif sensors[0] == 0:
					sensors[0] = 1

			elif event.key == K_w:
				if sensors[1] == 1:
					sensors[1] = 0
				elif sensors[1] == 0:
					sensors[1] = 1

			elif event.key == K_e:
				if sensors[2] == 1:
					sensors[2] = 0
				elif sensors[2] == 0:
					sensors[2] = 1

			elif event.key == K_r:
				if sensors[3] == 1:
					sensors[3] = 0
				elif sensors[3] == 0:
					sensors[3] = 1

			elif event.key == K_c:
				if smartCard == 1:
					cardTimer = 0
				elif smartCard == 0:
					smartCard = 1
					startCardTimer = True
			elif event.key == K_t:
				if shortFlag == 1:
					shortFlag = 0
				elif shortFlag == 0:
					shortFlag = 1

	#turn on timer if safe flag 1
 	if shortFlag == 1:
		startGateTimer = True
	else:
		gateTimer = 0
		startGateTimer = False

#Alarm check
	if alarm == 1:
		if sensors[0] == 0 and sensors[1] == 0 and sensors[2] == 0 and sensors[3] == 0 and sensors[4] == 0 and shortFlag == 0:
			alarm = 0
			if startIdleTimer == True:
				idleTimer = 0
				startIdleTimer = False
			if startGateTimer == True:
				gateTimer = 0
				startGateTimer = False
		else:
			print("ALARM")

#Timer rules
	if startCardTimer == True:
		cardTimer += 1
		# while loop runs every 0.1 seconds, 10 = roughly 1 sec(not accounting for program runtime)
		if cardTimer >= 100:
			startCardTimer = False
			smartCard = 0
			cardTimer = 0
	#idleTimer
	if startIdleTimer == True:
		idleTimer += 1
		if idleTimer >= 100:
#			startIdleTimer = False
#			sensors = [0,0,0,0,0,0]
#			smartCard = 0
			alarm = 1
			currState = 1

	#second timer for if gate is open too long
	if startGateTimer == True:
		gateTimer += 1
		if gateTimer >= 100:
			alarm = 1

#Set state rules

	if currState == 1:
		if sensors[0] == 1:
			startIdleTimer = False
			idleTimer = 0
			currState = 2
		elif (sensors[1] or sensors[2] or sensors[3] == 1):
			startIdleTimer = True
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
		gate = 1
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
		gate = 0
		if sensors[3] == 1 or shortFlag == 0:
			currState = 7
	elif currState == 7:
		startIdleTimer = True
		if sensors [3] == 0:
			currState = 1

	print('gate:' + str(gate) + ' sensors:' + str(sensors[0]) + str(sensors[1]) + str(sensors[2]) + str(sensors[3]) + ' card:' + str(smartCard) + ' state:' + str(currState) + " flag:" + str(shortFlag))
