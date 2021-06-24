import numpy as np
import pygame
import sys
from pygame.locals import *
import matplotlib.pyplot as plt
import agents

WHITE = (255,255,255)

width, height = 600, 600

T = 50

gamma = 0.0015
beta = 0.05

radius = 10.0
init_S = 200
init_I = 5

screen = pygame.display.set_mode((width,height))
screen.fill(WHITE)
clock = pygame.time.Clock()

population = agents.setup_simulation(init_S, init_I, radius, beta, gamma, width, height)

Sarray = np.zeros(T)
Iarray = np.zeros(T)
Rarray = np.zeros(T)


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

		if person.SIR == 'S':
			Sarray[i] += 1
		elif person.SIR == 'I':
			Iarray[i] += 1
		elif person.SIR == 'R':
			Rarray[i] += 1

	pygame.display.update()
	screen.fill(WHITE)


plt.plot(Sarray, label='Susceptible', color=(0,0,1))
plt.plot(Iarray, label='Infected', color=(0,1,0))
plt.plot(Rarray, label='Recoverd', color=(1,0,0))

plt.xlabel("Time")
plt.ylabel("Number of people")
plt.title("Agent Based SIR Model")
plt.legend(loc=0)

plt.savefig("./Plots/agent.png")

