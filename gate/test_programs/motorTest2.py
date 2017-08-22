#test motor movement with PWM

from gpiozero import PWMOutputDevice
from time import sleep

motor = PWMOutputDevice(18, True, 0, 100)

while True:
        motor.pulse(0.0001, 0.0001, 400, False)
	sleep(1)
