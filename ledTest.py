from gpiozero import LED
from time import sleep

led = LED(18)
count = 0

while True:
	led.on()
	sleep(0.001)
	led.off()
	sleep(0.001)
	count+=1
	if count%400 == 0:
		sleep(1)



