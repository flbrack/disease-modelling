'''
This runs one instance of the basic simulation, which is composed solely of agents of the base Person class defined in agents.py.
This is analagous to the SIR equation based model.
It can be run with or without animation by setting the ANIMATION_FLAG to true or false.
The data from the simulation is not stored but is immediately plotted and the plot saved to the Plots folder.
'''
import numpy as np
import pygame
import sys
from pygame.locals import *
import matplotlib.pyplot as plt
import agents

ANIMATION_FLAG = True  # Change this depending on if you want an animation or not.

WHITE = (255, 255, 255)
width, height = 800, 600 # This determines the size of the environment for the agents
radius = 10.0 # This determines the size of the agents

T = 500 # The length of time the simulation will run for. 5000 works well for SIR model.

# The disease parameters
gamma = 0.0015 # The rate of recovery
beta = 0.05 # The infection rate
mu = 0.0015 # The death rate

init_S = 200 # The number of Susceptible agents at beginning of simulation
init_I = 5 # The number of Infectious agents at beginning of simulation

if ANIMATION_FLAG: # Some set up for animation
	screen = pygame.display.set_mode((width,height))
	screen.fill(WHITE)
	clock = pygame.time.Clock()

# This set ups the simulation using a function defined in agents.py
population = agents.setup_death_simulation(init_S, init_I, radius, beta, gamma, mu, width, height)



# Arrays to store the number of agents in each category at each time step
Sarray = np.zeros(T)
Iarray = np.zeros(T)
Rarray = np.zeros(T)
Darray = np.zeros(T)

# The simulation loop
for i in range(T):

	# The actual running of the simulation.
	# This relies on the agent's methods defined in agents.py
	for person in population:
		for otherperson in population:
			if person==otherperson:
				continue
			person.infect(otherperson)
		person.update()

		if ANIMATION_FLAG:
			person.draw(screen)

		if person.SIR == 'S':
			Sarray[i] += 1
		elif person.SIR == 'I':
			Iarray[i] += 1
		elif person.SIR == 'R':
			Rarray[i] += 1
		else:
			Darray[i] += 1
	

	# Things to take care of for animation
	if ANIMATION_FLAG:
		clock.tick(60)
		pygame.display.update()
		screen.fill(WHITE)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

# We plot the results of the simulation
plt.plot(Sarray, label='Susceptible', color=(0,0,1))
plt.plot(Iarray, label='Infected', color=(0,1,0))
plt.plot(Rarray, label='Recovered', color=(1,0,0))
plt.plot(Darray, label='Dead', color=(0.3,0.3,0.3))

plt.xlabel("Time")
plt.ylabel("Number of people")
plt.title("Agent Based SIRD Model")
plt.legend(loc=0)

plt.savefig("./Plots/SimpleDeathModel.png")