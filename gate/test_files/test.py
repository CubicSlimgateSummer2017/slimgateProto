#testing curses keypress module

import curses
import time
#import pygame
#from pygame.locals import *

def main(win):
	win.nodelay(True)
	key=""
	i = 0
	win.clear()
	win.addstr("Detected key:")
	while 1:
		win.clear()
		win.addstr(str(i))
		time.sleep(0.5)
		i+=1
		if key == os.linesep:
			break	
curses.wrapper(main)
