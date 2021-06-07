from random import random
import numpy as np
import pygame
import sys
from pygame.locals import *
import matplotlib.pyplot as plt

width, height = 600, 600

T = 500

gamma = 0.0015
beta = 0.05
radius = 30
init_S = 15
init_I = 2

WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)


class Person:
	
	def __init__(self, position, dx, dy, SIR='S'):
		self.position = position
		self.SIR = SIR
		self.dx = dx
		self.dy = dy
	
	def draw(self):
		pygame.draw.circle(screen, self.color, self.position, radius)
	
		
	def infect(self, other):
		if self.SIR =='S' and other.SIR =='I':
			distance = np.linalg.norm(self.position - other.position)
			
			if distance <1.5*radius and  random() < beta:
				self.SIR = 'I'

	def update(self):
		if self.position[0] + radius > width or self.position[0] - radius < 0:
			self.dx = -self.dx	
			
		if self.position[1] + radius > height or self.position[1] - radius < 0:
			self.dy = -self.dy

		self.position += np.array([self.dx, self.dy]) * dt * 0.15
		
		if self.SIR == 'S':
			self.color = BLUE 
		elif self.SIR =='I':
			self.color = GREEN
		elif self.SIR == 'R':
			self.color = RED

		if self.SIR == 'I' and random() < gamma:
			self.SIR = 'R'

		for i in range(len(population)):
			if self == population[i]:
				continue
			else:
				self.infect(population[i])

		self.draw()

population = []

for i in range(init_S):
	x = random() * (width - radius*2) + 1.5*radius
	y = random() * (height - radius*2) + 1.5*radius
	
	xspeed = (random() - 0.5)*2
	yspeed = (random() - 0.5)*2
	
	population.append( Person(position=np.array([x,y]),dx=xspeed, dy=yspeed, SIR='S' ) )

for i in range(init_I):
	x = random() * (width - radius*2) + 1.5*radius
	y = random() * (height - radius*2) + 1.5*radius
	
	xspeed = (random() - 0.5)*2
	yspeed = (random() - 0.5)*2
	
	population.append( Person(position=np.array([x, y]),dx=xspeed, dy=yspeed, SIR='I' ) )

screen = pygame.display.set_mode((width,height))
screen.fill(WHITE)
clock = pygame.time.Clock()


Sarray = np.zeros(T)
Iarray = np.zeros(T)
Rarray = np.zeros(T)

for i in range(T):

	dt = clock.tick(30)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	
	for person in population:
		person.update()

		if person.SIR == 'S':
			Sarray[i] += 1
		elif person.SIR == 'I':
			Iarray[i] += 1
		elif person.SIR == 'R':
			Rarray[i] += 1

	pygame.display.update()
	screen.fill(WHITE)

plt.plot(Sarray, label='Susceptible')
plt.plot(Iarray, label='Infected')
plt.plot(Rarray, label='Recoverd')

plt.xlabel("Time")
plt.ylabel("Number of people")
plt.title("Agent Based SIR Model")
plt.legend(loc=0)

plt.savefig("agent.png")

