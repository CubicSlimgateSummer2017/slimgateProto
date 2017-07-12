import serial, time
#from subprocess import Popen
#from threading import Thread
import multiprocessing

from gpiozero import LED
from time import sleep

motorPin = LED(18)
dirPin = LED(23)

ser1 = serial.Serial('/dev/ttyACM0', 9600, timeout = None)
#ser2 = serial.Serial('/dev/ttyUSB0', 115200)
#ser2.write("T")
#ser2.write("P")

ser1.flush()
array = [0,0]

def motorOpen():
	print("open")
	dirPin.off()
	for i in range(0,200):
		motorPin.on()
		sleep(0.01)
		motorPin.off()
		sleep(0.01)

def portReader():
	while 1:	
		test = ser1.readline()
#		zone1 = ser1[8]
#		zone2 = ser1[18]
#		time.sleep(0.5)
		sensor1 = str(test)
#		print(sensor1)
#		print(zone1)
#		print(zone2)
		if (len(sensor1)>18):
			if (int(sensor1[18]) == 1):
				array[0] = 1
			else:
				array[0] = 0
	
			if (int(sensor1[8]) == 1):
				array[1] = 1
			else:
				array[1] = 0
	
#		print(str(sensor1[18]) + str(sensor1[8]))
		print(str(array[0]) + str(array[1]))
		if (array[0] == 1 and array[1] == 1):
#			print("open")
#			q.put(1)
			motorHandler = multiprocessing.Process(target=motorOpen)
			motorHandler.start()
#		print(string[8])
#		print(ser1.readline())
		ser1.flush()

if __name__ == '__main__':
#	queue = multiprocessing.Queue()

	portReader = multiprocessing.Process(target=portReader)
	motorHandler = multiprocessing.Process(target=motorOpen)

	portReader.start()
#	motorHandler.start()
#	print(array[0])

