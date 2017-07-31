import pygame
from pygame.locals import *

import time
import threading

import os
import sys
from termios import tcflush, TCIOFLUSH
import serial
import time

from gpiozero import LED
from time import sleep

class Slimgate(object):

	count = 0

	motorPin = LED(18)
	dirPin = LED(23)

	#front sensor self.sensors
	ser1 = serial.Serial('/dev/ttyACM0', 115200)
	#back sensor self.sensors
	ser2 = serial.Serial('/dev/ttyACM1', 115200)
	ser4 = serial.Serial('/dev/ttyUSB0', 115200)
  	
	#initialize serial for tera rangers	
	ser4.write("T")
	ser4.write("P")

	#motor arduino
	ser3 = serial.Serial('/dev/ttyACM2', 115200)

	#flush all self.sensors before beginning
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
	state = 1
	
	#Loop variable
	Running = True


	def __init__(self):
		print('Zones are as follows:')
		print('-----------------')
		print('| 1 | 2 | 3 | 4 |')
		print('-----------------')

		self._lock = threading.Lock()
		self._count_callback = None
		self._state_callback = None
		self._state_thread = threading.Thread(target=self._update_state)
		self._state_thread.daemon = True
		self._state_thread.start()
	
	def _update_state(self):
		#pygame.init()
		#pygame.display.set_mode((100,100))
		while self.Running:
			self.state += 1
		#       time.sleep(0.1)
			with self._lock:
#				for event in pygame.event.get():
#					if event.type == QUIT:
#						Running = False
#					if event.type == KEYDOWN:
#						if event.key == K_ESCAPE:
#							self.ser3.write("s")
#							Running = False
#						elif event.key == K_SPACE:
#							print("all self.sensors reset and current state set to 1")
#							self.ser3.write("s")
#							self.alarm = 0
#							self.startCardTimer = False
#							self.startIdleTimer = False
#							self.cardTimer = 0
#							self.idleTimer = 0
#							self.sensors = [0,0,0,0]
#							self.smartCard = 0
#							self.state = 1
#							self.ser3.write("o")
#							time.sleep(0.1)
#							self.ser3.write("c")
#						elif event.key == K_c:
#							if self.smartCard == 1:
#								self.cardTimer = 0
#							elif self.smartCard == 0:
#								self.smartCard = 1
#								self.state = 4
#								self.startCardTimer = True
				#turn on timer if safe flag 1
				if self.gate == 1 or self.shortFlag == 1:
					self.startGateTimer = True
				else:
					self.gateTimer = 0
					self.startGateTimer = False

			#Alarm check
				if self.alarm == 1:
					if self.sensors[0] == 0 and self.sensors[1] == 0 and self.sensors[2] == 0 and self.sensors[3] == 0 and self.shortFlag == 0:
						self.ser3.write("s")
						#print(self.gate)
						self.alarm = 0
						if self.startIdleTimer == True:
							self.idleTimer = 0
							self.startIdleTimer = False
						if self.startGateTimer == True:
							self.gateTimer = 0
							self.startGateTimer = False
						if self.gate == 1:
							self.ser3.write("c")
							self.gate = 0
					else:
						self.ser3.write("a")
						self.alarm = 0
						#print("ALARM")
				elif self.alarm == 0:
					self.ser3.write("s")
	 
			#Timer rules
				if self.startCardTimer == True:
					self.cardTimer += 1
					# while loop runs every 0.1 seconds, 10 = roughly 1 sec(not accounting for program runtime)
					if self.cardTimer >= 300:
						self.startCardTimer = False
						self.smartCard = 0
						self.cardTimer = 0
				#self.idleTimer
				if self.startIdleTimer == True:
					self.idleTimer += 1
					if self.idleTimer >= 300:
						self.alarm = 1
						self.state = 1

				#second timer for if self.gate is open too long
				if self.startGateTimer == True:
					self.gateTimer += 1
					if self.gateTimer >= 300:
						self.alarm = 1
				sensorArray1 = self.ser1.readline()
				sensorArray2 = self.ser2.readline()
				teraranger1 = self.ser4.readline()

				sensor1 = str(sensorArray1)
				sensor2 =str(sensorArray2)

				tera1 = self.int_check(str(teraranger1).strip())

				print tera1

				#print(sensor1)
				#print(sensor2)
				#print(len(sensor1))
				#print(len(sensor2))

				if ((len(sensor1) < 51) or (len(sensor2) < 51)):
					self.ser1.flushInput()
					#print("flushed self.ser1")
					self.ser2.flushInput()
					#print("flushed self.ser2")
					continue

				try:
					if((int(sensor2[8]) + int(sensor1[8])) == 0):
						self.shortFlag = 0
					else:
						self.shortFlag = 1

					if (int(sensor1[18]) == 1 or (tera1 > 220 and tera1 < 2000)):
						self.sensors[0] = 1
					else:
						self.sensors[0] = 0

					if (int(sensor1[8]) == 1):
						self.sensors[1] = 1
					else:
						self.sensors[1] = 0

					if (int(sensor2[18]) == 1):
						self.sensors[3] = 1
					else:
						self.sensors[3] = 0

					if (int(sensor2[8]) == 1):
						self.sensors[2] = 1
					else:
						self.sensors[2] = 0

				except (ValueError, IndexError):
			#               print("parse error, passing")
					continue

			#Set state rules

				if self.state == 1:
			#               self.startIdleTimer = True
					if (self.sensors[1] or self.sensors[2] or self.sensors[3] == 1):
					       self.startIdleTimer = True

					elif (self.sensors[0] == 1):
						if self._state_callback is not None:
							self._state_callback(self.state)
						self.startIdleTimer = False
						self.idleTimer = 0
						self.state = 2
			#               elif (self.sensors[1] or self.sensors[2] or self.sensors[3] == 1):
			#                       self.startIdleTimer = True
				elif self.state == 2:
					self.startIdleTimer = True
					if self.sensors[1] == 1:
						if self._state_callback is not None:
							self._state_callback(self.state)
						self.startIdleTimer = False
						self.idleTimer = 0
						self.state = 3
				elif self.state == 3:
					self.startIdleTimer = True
					if self.smartCard == 1:
						if self._state_callback is not None:
							self._state_callback(self.state)
						self.startIdleTimer = False
						self.idleTimer = 0
						self.state = 4
				elif self.state == 4:
					self.startIdleTimer = True
					self.startGateTimer = True
					self.gate = 1
					self.ser3.write("o")
					if self.sensors[2] == 1:
						if self._state_callback is not None:
							self._state_callback(self.state)
						self.startIdleTimer = False
						self.idleTimer = 0
						self.state = 5
				elif self.state == 5:
					self.startGateTimer = True
					if self.sensors[2] == 0 and self.shortFlag == 0:
						if self._state_callback is not None:
							self._state_callback(self.state)
						self.startGateTimer = False
						self.gateTimer = 0
						self.state = 6
				elif self.state == 6:
					self.smartCard = 0
			#               if self.gate == 1:
			#                       self.gate = 0
			#                       self.ser3.write("c")
					if self.sensors[3] == 1 or self.shortFlag == 0:
						if self._state_callback is not None:
							self._state_callback(self.state)
						self.state = 7
				elif self.state == 7:
					self.smartCard = 0
					self.gate = 0
					self.ser3.write("c")
					self.startIdleTimer = True
					if self.sensors [3] == 0:
						if self._state_callback is not None:
							self._state_callback(self.state)
						self.state = 1

#				print('self.gate:' + str(self.gate) + ' self.sensors:' + str(self.sensors[0]) + str(self.sensors[1]) + str(self.sensors[2]) + str(self.sensors[3]) + ' card:' + str(self.smartCard) + ' state:' + str(self.state) + " flag:" + str(self.shortFlag))
								
				self.ser1.flushInput()
				self.ser2.flushInput()
				self.ser4.flushInput()
				if self._state_callback is not None:
					self._state_callback(self.state)
				time.sleep(0.5)

	def _update_count(self):
		for i in range(0,1000):
			with self._lock:
#				print("testing repeated outputs, count = " + str(count))
				self.count += 1
				if self._count_callback is not None:
					self._count_callback(self.count)
			time.sleep(1)
	
	def on_state_change(self, callback):
		self._state_callback = callback
	
	def on_count_change(self, callback):
		self._count_callback = callback
	
	def int_check(self, s):
		try:
			s = s.strip()
			return int(s) if s else 0
		except(ValueError):
			pass

