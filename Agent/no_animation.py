from random import random
import numpy as np
import matplotlib.pyplot as plt

width, height = 600, 600


T = 5000

gamma = 0.0015
beta = 0.05
radius = 10.0
init_S = 198
init_I = 2



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



Sarray = np.zeros(T)
Iarray = np.zeros(T)
Rarray = np.zeros(T)


for i in range(T):

	for person in population:
		person.update()

		if person.SIR == 'S':
			Sarray[i] += 1
		elif person.SIR == 'I':
			Iarray[i] += 1
		elif person.SIR == 'R':
			Rarray[i] += 1



plt.plot(Sarray, label='Susceptible', color=(0,0,1))
plt.plot(Iarray, label='Infected', color=(0,1,0))
plt.plot(Rarray, label='Recoverd', color=(1,0,0))

plt.xlabel("Time")
plt.ylabel("Number of people")
plt.title("Agent Based SIR Model")
plt.legend(loc=0)

plt.savefig("no_animation.png")


