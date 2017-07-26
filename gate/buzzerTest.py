from gpiozero import Buzzer
from time import sleep


bz = Buzzer(23)
count = 0

while True:
#	bz.beep(1, 1, 10, False)
	bz.on()
	sleep(0.01)
	bz.off()
	sleep(0.01)
	count += 1

	if count == 50:
		break

