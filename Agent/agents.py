from random import random, shuffle
import numpy as np
import pygame

RED = (255,0,0,180)
BLUE = (0,0,255,180)
GREEN = (0,255,0,180)

def draw_circle_alpha(surface, color, center, radius):

	# Special function so that the circles representing the agents can be transparent.

    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)

class Person:

	# Base class for agents.
	
	def __init__(self, position, velocity, radius, gamma, beta, width, height, SIR='S'):
		self.position = position
		self.SIR = SIR
		self.velocity = velocity
		self.radius = radius
		self.gamma = gamma
		self.beta = beta
		self.width = width
		self.height = height

	def draw(self, screen):

	# Draws agent on screen, method is ignored when no animation is required.

		if self.SIR == 'S':
			self.color = BLUE 
		elif self.SIR =='I':
			self.color = GREEN
		elif self.SIR == 'R':
			self.color = RED

		draw_circle_alpha(screen, self.color, self.position, self.radius)

	
		
	def infect(self, other):

	# Method for an agent to infect another agent.

		if self.SIR =='S' and other.SIR =='I':
			distance = np.linalg.norm(self.position - other.position)
			
			if distance <1.5*self.radius and  random() < self.beta:
				self.SIR = 'I'

	def update(self):

	# Keeps agent moving and inside given area. Also controls when it recovers from disease.

		if self.position[0] + self.radius > self.width or self.position[0] - self.radius < 0:
			self.velocity[0] = -self.velocity[0]	
			
		if self.position[1] + self.radius > self.height or self.position[1] - self.radius < 0:
			self.velocity[1] = -self.velocity[1]

		self.position += self.velocity
		

		if self.SIR == 'I' and random() < self.gamma:
			self.SIR = 'R'



def setup_simulation(init_S, init_I, radius, beta, gamma, width, height):

	# Creates an array of agents.

	population = []

	for i in range(init_S):
		x = radius + random()*(width - 2*radius)
		y = radius + random()*(height - 2*radius)

		xspeed = (random() - 0.5)*2
		yspeed = (random() - 0.5)*2


		population.append( Person(position=np.array([x,y]), velocity=np.array([xspeed, yspeed]), SIR='S', radius=radius , gamma=gamma, beta=beta, height=height, width=width) )

	for i in range(init_I):
		x = radius + random()*(width - 2*radius)
		y = radius + random()*(height - 2*radius)

		xspeed = (random() - 0.5)*2
		yspeed = (random() - 0.5)*2

		population.append( Person(position=np.array([x,y]),velocity=np.array([xspeed, yspeed]), SIR='I', radius=radius , gamma=gamma, beta=beta) )
	
	return population


class HomePerson(Person):

	# Extended agent class, will not leave a specified area, its "home"

	def __init__(self, home, home_size, position, velocity, radius, gamma, beta, width, height, SIR):
		
		self.home = home
		self.home_size = home_size
		Person.__init__(self, position, velocity, radius, gamma, beta, width, height, SIR)

	def update(self):

		if self.position[0] + self.radius > self.width or self.position[0] - self.radius < 0:
			self.velocity[0] = -self.velocity[0]
			
		if self.position[1] + self.radius > self.height or self.position[1] - self.radius < 0:
			self.velocity[1] = -self.velocity[1]


		if np.linalg.norm(self.position - self.home) > (self.home_size - self.radius):
			normal = self.position - self.home
			u = ( np.dot(self.velocity, normal)/np.dot(normal, normal) ) * normal
			w = self.velocity - u
			self.velocity = w - u


		self.position += self.velocity
		

		if self.SIR == 'I' and random() < self.gamma:
			self.SIR = 'R'


def initial_infection(init_I, population):

	# Given a population, infect a random subset of given size

	shuffle(population)

	for i in range(init_I):
		person = population[int((random() * len(population)))]
		person.SIR = "I"