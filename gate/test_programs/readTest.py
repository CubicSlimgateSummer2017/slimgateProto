#gathering all sensor readings test

import serial, time

#ser1 = serial.Serial('/dev/ttyACM2', 115200)
#ser3 = serial.Serial('/dev/ttyACM1', 115200)
ser2 = serial.Serial('/dev/ttyUSB1', 115200)
ser2.write("T")
ser2.write("P")

#ser1.flush()

while 1:	
#	print(ser1.readline())
#	print(ser3.readline())
	print(ser2.readline())
#	test = ser1.readline()
	test2 = ser2.readline()
#	test3 = ser3.readline()
#	zone1 = ser1[8]
#	zone2 = ser1[18]
#	time.sleep(0.5)
#	string = str(test)
	string2 = str(test2)
#	string3 = str(test3)
	
#	print(zone1)
#	print(zone2)
#	print(string[18] + string[8])
#	print(ser1.readline())
#	print(string2)
#	print(string3)
#	ser2.flushInput()
