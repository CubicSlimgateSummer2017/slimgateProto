from curses import wrapper
import RPi.GPIO as GPIO
import sys
import time


#setup
Running = True

def main(stdscr):

	while Running:
		stdscr.clear()

		c = stdscr.getkey()

		if c == 'KEY_DOWN':
			stdscr.addstr(10, 2, 'keydown detected')
		elif c == 'KEY_Q':
			stdscr.addstr(10, 2, 'pressed q')
		#else:
		#	stdscr.addstr(10, 2, 'You pressed {}'.format(c))
		stdscr.refresh()
		stdscr.getkey()

wrapper(main)
