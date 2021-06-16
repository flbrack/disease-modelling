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
init_I = 0

homes = [np.array([100,100]), np.array([400,100]), np.array([100,400]), np.array([400,400])]
home_size = 50.0

screen = pygame.display.set_mode((width,height))
screen.fill(WHITE)
clock = pygame.time.Clock()


# population = agent_sim.setup_simulation(init_S, init_I, radius, beta, gamma, width, height)


population = []

for i in range(5):

	for home in homes:

		x = home[0] + (random()-0.5)*home_size
		y = home[1] + (random()-0.5)*home_size


		xspeed = (random() - 0.5)*2
		yspeed = (random() - 0.5)*2

		population.append( agent_sim.HomePerson(position=np.array([x,y]),dx=xspeed, dy=yspeed, home=home, home_size=home_size, SIR='S', radius=radius , gamma=gamma, beta=beta, width=600, height=600) )




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

