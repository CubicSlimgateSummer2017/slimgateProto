#Tests if button is working

from gpiozero import Button

button = Button(18)

while (True):
	if button.is_pressed:
		print("asdfasdfdfasdfasdf")
