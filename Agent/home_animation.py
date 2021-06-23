import numpy as np
import pygame
import sys
from pygame.locals import *
import matplotlib.pyplot as plt
import agent_sim
from random import random

WHITE = (255,255,255)

width, height = 600, 600

T = 2000

gamma = 0.0015
beta = 0.05

radius = 10.0
init_S = 20
init_I = 5


home_number = 12
home_radius = 50.0
people_per_home = 5

offset = 30

homes = []
for i in range(3):
	for j in range(home_number//3):
		homes.append(np.array([offset + home_radius + i*width//3, offset + home_radius+j*height//(home_number//3)]))


screen = pygame.display.set_mode((width,height))
screen.fill(WHITE)
clock = pygame.time.Clock()


population = []

for i in range(people_per_home):

	for home in homes:

		x = home[0] + (random()-0.5)*home_radius
		y = home[1] + (random()-0.5)*home_radius


		xspeed = (random() - 0.5)*2
		yspeed = (random() - 0.5)*2

		population.append( agent_sim.HomePerson(position=np.array([x,y]),dx=xspeed, dy=yspeed, home=home, home_size=home_radius, SIR='S', \
			radius=radius , gamma=gamma, beta=beta, width=600, height=600) )


super_spreaders = 4
for person in agent_sim.setup_simulation(10,0, radius=radius, beta=beta,gamma=gamma,height=height,width=width):
	population.append(person)


agent_sim.initial_infection(init_I, population)


for i in range(T):

	clock.tick(60)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	
	for person in population:
		for otherperson in population:
			if person==otherperson:
				continue
			person.infect(otherperson)
		person.update()
		person.draw(screen)


	pygame.display.update()
	screen.fill(WHITE)
	for home in homes:
		pygame.draw.circle(screen, color=(0,0,0) ,center= home, radius = 2)

