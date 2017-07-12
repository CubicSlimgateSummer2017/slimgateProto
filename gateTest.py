import serial, time
import multiprocessing

from gpiozero import LED
from time import sleep

motorPin = LED(18)
dirPin = LED(23)
gateState = 0

#front sensor array
ser1 = serial.Serial('/dev/ttyACM0', 9600)
#back sensor array
ser2 = serial.Serial('/dev/ttyACM1', 9600)
#ser2 = serial.Serial('/dev/ttyUSB0', 115200)
#ser2.write("T")
#ser2.write("P")

#motor arduino
ser3 = serial.Serial('/dev/ttyACM2', 9600)

ser1.flush()
array = [0,0,0,0]

def motorOpen(q):
#	tmp = q.get()
	if (q.empty() == False):
		print("open")
		dirPin.off()
#		for i in range(0,200):
#			motorPin.on()
#			sleep(0.1)
#			motorPin.off()
#			sleep(0.1)


#queue = multiprocessing.Queue()
#motorHandler = multiprocessing.Process(target=motorOpen, args=(queue,))
#motorHandler.start()

while 1:
	sensorArray1 = ser1.readline()
	sensorArray2 = ser2.readline()

	sensor1 = str(sensorArray1)
	sensor2 =str(sensorArray2)

	print(sensor1)
	print(sensor2)	
	print(len(sensor1))
	print(len(sensor2))
	if (len(sensor1) >= 40):
		if (int(sensor1[18]) == 1):
			array[0] = 1
		else:
			array[0] = 0

		if (int(sensor1[8]) == 1):
			array[1] = 1
		else:
			array[1] = 0
	
		if (int(sensor2[18]) == 1):
			array[2] = 1
		else:
			array[2] = 0
	
		if (int(sensor2[8]) == 1):
			array[3] = 1
		else:
			array[3] = 0

#	print(str(sensor1[18]) + str(sensor1[8]))
	print(str(array[0]) + str(array[1]) + str(array[2]) + str(array[3]))
	if (array[0] == 1 and array[1] == 1):
		if gateState == 0:
			ser3.write("o")
			gateState = 1
	elif (array[2] == 1 and array[3] == 1):
		if gateState == 1:
			ser3.write("c")
			gateState = 0

	ser1.flush()
