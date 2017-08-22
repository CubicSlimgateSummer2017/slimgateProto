from gpiozero import LED
from time import sleep

led = LED(23)

while True:
	led.on()
