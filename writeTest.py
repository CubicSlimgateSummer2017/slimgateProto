import serial, time

ser1 = serial.Serial('/dev/ttyACM1', 9600)
#ser2 = serial.Serial('/dev/ttyUSB0', 115200)
#ser2.write("T")
#ser2.write("P")

ser1.flush()

ser1.write("o")

while 1:	
	test = ser1.readline()
#	zone1 = ser1[8]
#	zone2 = ser1[18]
#	time.sleep(0.5)
	string = str(test)

#	print(zone1)
#	print(zone2)
	print(string[18] + string[8])
#	print(ser1.readline())
