'''
This is the backend of the simulations, where the agent classes are defined, 
along with other functions for the setup of the simulations.
The Person class is the base class, with most of the others being extensions of this.
'''
from random import random, shuffle
import numpy as np
import pygame

# ------------- Some functions and set up for Pygame animations -------------------------------

RED = (255,0,0,180)
BLUE = (0,0,255,180)
GREEN = (0,255,0,180)
GREY = (84,84,84,180)
PURPLE = (128,0,128,180)

def draw_circle_alpha(surface, color, center, radius):

	# Special function so that the circles representing the agents can have transparency.

    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)


# ------------- Agent classes used in simulations --------------------------------------------

class Person:

	'''
	This is the base class for the agents. It has a init, draw, infect and update method.
	Generally, only the init and update methods change in the extended classes.
	It has three status options; Susceptible, Infectious or Recovered.
	The infection rate is controlled by parameter beta.
	The recovery rate is controlled by parameter gamma.
	'''
	
	def __init__(self, position, velocity, radius, gamma, beta, width, height, status='S'):
		self.position = position # The postition of the agent
		self.status = status # The health status of the agent
		self.velocity = velocity # The velocity of the agent
		self.radius = radius # The radius of the agent
		self.gamma = gamma # The recovery rate of the disease
		self.beta = beta # The infection rate of the disease
		self.width = width # This is the width of the environment it is contained in.
		self.height = height # This is the height of the environment it is contained in.

		if self.status == 'S':    # We only ever initialise an agent with status = 'S' or 'I'
			self.color = BLUE
		elif self.status == 'I':
			self.color = GREEN

	def draw(self, screen):

	# Draws agent on screen.
		draw_circle_alpha(screen, self.color, self.position, self.radius)

		
	def infect(self, other):

	# Method for an agent to infect another agent.
		if self.status =='S' and other.status =='I':
			distance = np.linalg.norm(self.position - other.position)
			
			if distance <1.5*self.radius and  random() < self.beta:
				self.status = 'I'
				self.color = GREEN

	def position_update(self):

	# Keeps agent moving and inside given area.
		if self.position[0] + self.radius > self.width or self.position[0] - self.radius < 0:
			self.velocity[0] = -self.velocity[0]	
			
		if self.position[1] + self.radius > self.height or self.position[1] - self.radius < 0:
			self.velocity[1] = -self.velocity[1]

		self.position += self.velocity
		
	def status_update(self):

	# Controls when agent turns from Infectious to Recovered.
		if self.status == 'I' and random() < self.gamma:
			self.status = 'R'
			self.color = RED


class HomePerson(Person):

	'''
	This is an extension of the base Person class such that each HomePerson has an area within the environment, which it stays within.
	This is to simulate more closely real world, heterogeneous population mixing.
	'''
	
	def __init__(self, home, home_size, position, velocity, radius, gamma, beta, width, height, status):
		
		self.home = home
		self.home_size = home_size
		Person.__init__(self, position, velocity, radius, gamma, beta, width, height, status)

	def position_update(self):

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
		


class DeathPerson(Person):

	'''
	This is an extension of the Person class. It extends it by adding the status option of Dead.
	The death rate is controlled by the parameter mu.
	In animation, when an agent has status Dead, it will be coloured grey and it will stop moving.
	'''

	def __init__(self, position, velocity, radius, gamma, beta, mu, width, height, status):
		self.mu = mu # The death rate of the disease
		Person.__init__(self, position, velocity, radius, gamma, beta, width, height, status)


	def status_update(self):

		if self.status == 'I' and random() < self.gamma:
			self.status = 'R'
			self.color = RED

		if self.status == 'I' and random() < self.mu:
			self.status = 'D'
			self.color = GREY
			self.velocity = np.array([0, 0])


class QuarantineDeathPerson(DeathPerson):

	'''
	This extends the DeathPerson class by adding the status option of Quarantined.
	The quarantine rate is controlled by kappa.
	The length of quarantine is controlled by mu and gamma.
	Thus someone leaves quarantine if they have either recovered or died.
	'''

	def __init__(self, position, velocity, radius, gamma, beta, mu, kappa, width, height, status):

		self.kappa = kappa # The chance of being quarantined after infection
		DeathPerson.__init__(self, position, velocity, radius, gamma, beta, mu, width, height, status)


	def infect(self, other):

	# Method for an agent to infect another agent.

		if self.status =='S' and other.status =='I':
			distance = np.linalg.norm(self.position - other.position)
			
			if distance <1.5*self.radius and  random() < self.beta:
			
				if random() < self.kappa:
					self.status = 'Q'
					self.color = PURPLE
					self.velocity = np.array([0,0])
				else:
					self.status = 'I'
					self.color = GREEN


	def status_update(self):

	# Keeps agent moving and inside given area. Also controls when it recovers or dies from disease.

		if self.status == 'I' and random() < self.gamma:
			self.status = 'R'
			self.color = RED

		if self.status == 'I' and random() < self.mu:
			self.status = 'D'
			self.color = GREY
			self.velocity = np.array([0, 0])

		if self.status == 'Q' and random() < self.gamma:
			self.status = 'R'
			self.color = RED
			self.velocity = np.array([(random() - 0.5)*2,(random() - 0.5)*2]) 

		if self.status == 'Q' and random() < self.mu:
			self.status = 'D'
			self.color = GREY
			self.velocity = np.array([0,0])
				




class Hospitalisations(QuarantineDeathPerson):

	def __init__(self, max_hospital):

		self.max_hospital = max_hospital

	def status_update(self):
		pass

	def hospital_status_update(self):
		pass



# ----------------- Functions for initialising simulations --------------------------------------------------------

def initial_infection(init_I, population):

	# Given a population, possibly of different agent classes; infects a random subset of given size

	shuffle(population)
	for i in range(init_I):
		person = population[int((random() * len(population)))]
		person.status = "I"
		person.color = GREEN


def create_SIR_population(N, init_I, radius, beta, gamma, width, height):

	# Creates an array of agents.
	population = []

	for i in range(N):
		x = radius + random()*(width - 2*radius)
		y = radius + random()*(height - 2*radius)

		xspeed = (random() - 0.5)*2
		yspeed = (random() - 0.5)*2

		population.append( Person(position=np.array([x,y]), velocity=np.array([xspeed, yspeed]), status='S', radius=radius, \
									gamma=gamma, beta=beta, width=width, height=height) )

	initial_infection(init_I, population)

	return population


def create_SIRD_population(N, init_I, radius, beta, gamma, mu, width, height):

	# Creates an array of agents.
	population = []

	for i in range(N):
		x = radius + random()*(width - 2*radius)
		y = radius + random()*(height - 2*radius)

		xspeed = (random() - 0.5)*2
		yspeed = (random() - 0.5)*2

		population.append( DeathPerson(position=np.array([x,y]), velocity=np.array([xspeed, yspeed]), status='S', radius=radius, \
										gamma=gamma, beta=beta, mu=mu, width=width, height=height) )

	initial_infection(init_I, population)
	
	return population


def create_SIRQD_population(N, init_I, radius, beta, gamma, mu, kappa, width, height):

	# Creates an array of agents.
	population = []

	for i in range(N):
		x = radius + random()*(width - 2*radius)
		y = radius + random()*(height - 2*radius)

		xspeed = (random() - 0.5)*2
		yspeed = (random() - 0.5)*2

		population.append( QuarantineDeathPerson(position=np.array([x,y]), velocity=np.array([xspeed, yspeed]), status='S', radius=radius, \
												gamma=gamma, beta=beta, mu=mu, kappa=kappa, width=width, height=height) )

	initial_infection(init_I, population)

	return population


def create_SIRQD_population_with_age_profile(N_old, N_young, init_I, radius, beta, gamma, old_mu, young_mu, kappa, width, height):

	# Creates an array of agents.
	population = []

	for _ in range(N_old):
		x = radius + random()*(width - 2*radius)
		y = radius + random()*(height - 2*radius)

		xspeed = (random() - 0.5)*2
		yspeed = (random() - 0.5)*2

		population.append( QuarantineDeathPerson(position=np.array([x,y]), velocity=np.array([xspeed, yspeed]), status='S', radius=radius, \
												gamma=gamma, beta=beta, mu=old_mu, kappa=kappa, width=width, height=height) )

	for _ in range(N_young):
		x = radius + random()*(width - 2*radius)
		y = radius + random()*(height - 2*radius)

		xspeed = (random() - 0.5)*2
		yspeed = (random() - 0.5)*2

		population.append( QuarantineDeathPerson(position=np.array([x,y]), velocity=np.array([xspeed, yspeed]), status='S', radius=radius, \
												gamma=gamma, beta=beta, mu=young_mu, kappa=kappa, width=width, height=height) )

	initial_infection(init_I, population)

	return population
