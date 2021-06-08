from random import random
import numpy as np

width, height = 600, 600

T = 5000

gamma = 0.0015
beta = 0.05
radius = 10.0
init_S = 95
init_I = 5


class Person:
	
	def __init__(self, position, dx, dy, SIR='S'):
		self.position = position
		self.SIR = SIR
		self.dx = dx
		self.dy = dy
	
		
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

		self.position += np.array([self.dx, self.dy]) #* dt * 0.15
		

		if self.SIR == 'I' and random() < gamma:
			self.SIR = 'R'

		for i in range(len(population)):
			if self == population[i]:
				continue
			else:
				self.infect(population[i])


repeats = 10

data = np.zeros([repeats*T,3])

for k in range(repeats):

	population = []

	for i in range(init_S):
		x = radius + random()*(width - 2*radius)
		y = radius + random()*(height - 2*radius)

		xspeed = (random() - 0.5)*2
		yspeed = (random() - 0.5)*2

		
		population.append( Person(position=np.array([x,y]),dx=xspeed, dy=yspeed, SIR='S' ) )

	for i in range(init_I):
		x = radius + random()*(width - 2*radius)
		y = radius + random()*(height - 2*radius)
		
		xspeed = (random() - 0.5)*2
		yspeed = (random() - 0.5)*2
		
		population.append( Person(position=np.array([x, y]),dx=xspeed, dy=yspeed, SIR='I' ) )




	for i in range(T):

		for person in population:
			person.update()

			if person.SIR == 'S':
				data[i + k*T, 0] += 1
			elif person.SIR == 'I':
				data[i + k*T, 1] += 1
			elif person.SIR == 'R':
				data[i + k*T, 2] += 1


np.savetxt('AgentData.csv', data, fmt = '%.1f', delimiter=",", header="S,I,R")


