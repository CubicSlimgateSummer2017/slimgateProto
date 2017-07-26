from gpiozero import LED
from time import sleep

motorPin = LED(18)
dirPin = LED(23)
#direction = 0
dirPin.off()

for i in range(0, 200):
	motorPin.on()
	sleep(0.01)
	motorPin.off()
	sleep(0.01)
