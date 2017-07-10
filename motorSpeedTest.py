from curses import wrapper
from gpiozero import LED
from time import sleep

def main(stdscr):
	
	motorPin = LED(18)
	dirPin = LED(23)
	direction = 0
	count = 0
	factor = 1.0
	while True:
		if count == 0:
			stdscr.addstr("Guide: q = slow down")
			stdscr.addstr("       w = speed up")
			stdscr.addstr("       p = display current delay time")
			stdscr.addstr("       d = change direction")
		stdscr.nodelay(True)
		c = stdscr.getch()
		
		#w
		if c == 113:
			factor = factor*2
			stdscr.addstr("\n" + "slow down")
		#q
		elif c == 119:
			factor = factor/2
			stdscr.addstr("\n" + "speed up")
		#p
		elif c == 112:
			stdscr.addstr("\n" + str(0.001*factor))
		#d
		elif c == 100:
			if direction == 0:
				direction = 1
				dirPin.on()
				stdscr.addstr("\n" + "direction: 1")
			elif direction == 1:
				direction = 0
				dirPin.off()
				stdscr.addstr("\n" + "direction: 0")
		motorPin.on()
       		sleep(0.01*factor)
      		motorPin.off()
      		sleep(0.01*factor)
        	count+=1
       		if count%200 == 0:
               		sleep(1)

if __name__ == '__main__':
	wrapper(main)
