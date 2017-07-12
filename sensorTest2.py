import pygame
from pygame.locals import *
import sys
import time

pygame.init()

pygame.display.set_mode((100, 100))

Running = True

sensors=[0,0,0,0,0,0]
gate = 0
gateclock = 0

print('Zones are as follows:')
print('-----------------')
print('| 1 | 2 | 3 | 4 |')
print('-----------------')
print('Press s to start')

while Running:
    time.sleep(0.1)
    gateclock += 1	
    
    #main loop
    
    for event in pygame.event.get():
	if event.type == QUIT:
	    Running = False
	if event.type == KEYDOWN:
	    if event.key == K_ESCAPE:
		Running = False
	    elif event.key == K_SPACE:
		sensors = [0,0,0,0,0,0]
 
    print('sensors: ' + str(sensors[0]) + ' ' + str(sensors[1]) + ' ' + str(sensors[2]) + ' ' + str(sensors[3]) + ' smartCard: ' + str(sensors[4]) + ' gate: ' + str(gate))
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        if sensors[0] == 1: 
	    sensors[0] = 0
        elif sensors[0] == 0:
    	    sensors[0] = 1

    if keys[pygame.K_w]:
        if sensors[1] == 1: 
	    sensors[1] = 0
        elif sensors[1] == 0:
    	    sensors[1] = 1

    if keys[pygame.K_e]:
        if sensors[2] == 1: 
	    sensors[2] = 0
        elif sensors[2] == 0:
    	    sensors[2] = 1

    if keys[pygame.K_r]:
        if sensors[3] == 1: 
	    sensors[3] = 0
        elif sensors[3] == 0:
    	    sensors[3] = 1

    if keys[pygame.K_c]:
        if sensors[4] == 1: 
	    sensors[4] = 0
        elif sensors[4] == 0:
    	    sensors[4] = 1

    if keys[pygame.K_t]:
        if sensors[5] == 1: 
	    sensors[5] = 0
        elif sensors[5] == 0:
    	    sensors[5] = 1

    
    
    #Set rules
   
    #normal routine s1 => s2 => open => s3 =>close
#    if sensors[0] == 1:
#       if sensors[1] == 1 & smartCard == 1:
#	    gate = 1
#	    if sensors[2] == 1:
#	        gate = 0
	

