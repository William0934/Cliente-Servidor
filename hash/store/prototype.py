import pygame
import math
from pygame.locals import *

class animation():	
	def __init__(self,x,y,type):
		self.x=x
		self.y=y
		self.type=type



pygame.init()
pantalla = pygame.display.set_mode((500,700))
while True:		
	pygame.display.flip()
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			raise SystemExit
	pygame.time.delay(50)
