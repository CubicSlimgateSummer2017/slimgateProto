from time import sleep

while True:
	f = open('/home/pi/slimgateProto/gate/data.txt')
	print(f.readline())
	f.close()
	sleep(0.1)
