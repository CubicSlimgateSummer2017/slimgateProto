import serial, time

ser1 = serial.Serial('/dev/ttyACM0', 9600)
ser3 = serial.Serial('/dev/ttyACM2', 9600)
ser2 = serial.Serial('/dev/ttyUSB0', 115200)
ser2.write("T")
ser2.write("P")

ser1.flush()

while 1:	
	test = ser1.readline()
	test2 = ser2.readline()
	test3 = ser3.readline()
#	zone1 = ser1[8]
#	zone2 = ser1[18]
#	time.sleep(0.5)
	string = str(test)
	string2 = str(test2)
	string3 = str(test3)
	
#	print(zone1)
#	print(zone2)
	print(string[18] + string[8])
#	print(ser1.readline())
	print(string2)
	print(string3)
	ser2.flushInput()
