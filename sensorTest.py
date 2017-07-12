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
startIdleTimer2 = False
cardTimer = 0
idleTimer = 0
idleTimer2 = 0

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

	#turn on timer is safe flag 1
 	if shortFlag == 1:
		startIdleTimer2 = True
	else:
		idleTimer2 = 0
		startIdleTimer2 = False

#Alarm check
	if alarm == 1:
		if sensors[0] == 0 and sensors[1] == 0 and sensors[2] == 0 and sensors[3] == 0 and sensors[4] == 0 and shortFlag == 0:
			alarm = 0
			if startIdleTimer == True:
				idleTimer = 0
				startIdleTimer = False
			if startIdleTimer2 == True:
				idleTimer2 = 0
				startIdleTimer2 = False
		else:
			print("ALARM")

#Timer rules
	if startCardTimer == True:
		cardTimer += 1
		# while loop runs every 0.1 seconds, 10 = roughly 1 sec(not accounting for program runtime)
		if cardTimer >= 50:
			startCardTimer = False
			smartCard = 0
			cardTimer = 0
	#idleTimer
	if startIdleTimer == True:
		idleTimer += 1
		if idleTimer >= 50:
#			startIdleTimer = False
#			sensors = [0,0,0,0,0,0]
#			smartCard = 0
			alarm = 1
			currState = 1

	#second timer for if gate is open too long
	if startIdleTimer2 == True:
		idleTimer2 += 1
		if idleTimer2 >= 100:
			alarm = 1

#Set state rules

	if currState == 1:
		if sensors[0] == 1:
			currState = 2
		elif sensors[1] == 1:
			startIdleTimer = True
	elif currState == 2:
		startIdleTimer = True
		if sensors[1] == 1:
			currState = 3
	elif currState == 3:
		if smartCard == 1:
			currState = 4
	elif currState == 4:
		idleTimer = 0
		startIdleTimer = False
		gate = 1
		if sensors[2] == 1:
			currState = 5
	elif currState == 5:
		if sensors[2] == 0 and shortFlag == 0:
			currState = 6
			idleTimer2 = 0
			startIdleTimer2 = False
		else:
			startIdleTimer2 = True
	elif currState == 6:
		smartCard = 0
		gate = 0
		idleTimer = 0
		if sensors[3] == 1:
			currState = 7
	elif currState == 7:
		if sensors [3] == 0:
			currState = 1

	print('gate:' + str(gate) + ' sensors:' + str(sensors[0]) + str(sensors[1]) + str(sensors[2]) + str(sensors[3]) + ' card:' + str(smartCard) + ' state:' + str(currState) + " flag:" + str(shortFlag))
