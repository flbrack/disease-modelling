'''
Many diseases affect people in older age groups more than younger age groups.
This simulation implements this possibility inside a regular agent based SIRQD model.
A population is created with two age profiles. Agents can be either old or young.
The agents in the old population have a higher death rate.
The results are immediately plotted and save to the Plots folder.
'''
import numpy as np
import pygame
import sys
from pygame.locals import *
import matplotlib.pyplot as plt
import agents

ANIMATION_FLAG = True  # Change this depending on if you want an animation or not.

#--------------- Tunable Parameters ---------------------------------------------

width, height = 800, 600 # This determines the size of the environment for the agents, as well as the animation window
radius = 15.0 # This determines the size of the agents

T = 2000 # The length of time the simulation will run for. 2000 works well.

# The disease parameters
beta = 0.05 # The infection rate
gamma = 0.015 # The rate of recovery
old_mu = 0.04 # The death rate for old people
young_mu = 0.015 # The death rate for young people
kappa = 0.5 # The quarantine rate

N_old = 30 # The number of old people
N_young = 70 # The number of young people
init_I = 5 # The number of Infectious agents at beginning of simulation

# --------------------------------------------------------------------------------

WHITE = (255, 255, 255)
if ANIMATION_FLAG: # Some set up for animation
	screen = pygame.display.set_mode((width,height))
	screen.fill(WHITE)
	clock = pygame.time.Clock()

# This set ups the simulation using a function defined in agents.py
population = agents.create_SIRQD_population_with_age_profile(N_old, N_young, init_I, radius, beta, gamma, old_mu, young_mu, kappa, width, height)

# Arrays to store the number of agents in each category at each time step
Sarray = np.zeros(T)
Iarray = np.zeros(T)
Rarray = np.zeros(T)
Darray = np.zeros(T)
Qarray = np.zeros(T)
old_Darray = np.zeros(T)

# The simulation loop
for i in range(T):

	# The actual running of the simulation.
	# This relies on the agent's methods defined in agents.py
	for person in population:
		for otherperson in population:
			if person==otherperson:
				continue
			person.infect(otherperson)
		
		# Each agent's status is only updated every 10th timestep.
		# This stops them from turning from I to D or I to R etc. too quickly.
		# And it keeps gamma and mu values on more realistic scale.
		if i % 10 == 0:
			person.status_update()
		
		person.position_update()

		if ANIMATION_FLAG:
			person.draw(screen)

		if person.status == 'S':
			Sarray[i] += 1
		elif person.status == 'I':
			Iarray[i] += 1
		elif person.status == 'R':
			Rarray[i] += 1
		elif person.status == 'D':
			Darray[i] += 1
			if person.mu == old_mu:
				old_Darray[i] += 1
		else:
			Qarray[i] += 1
	

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
plt.plot(Qarray, label='Quarantined', color=(0.5,0,0.5))

old_deaths_percent = round(100*old_Darray[-1]/Darray[-1],2)
plt.plot([], label=f'Old % deaths: {old_deaths_percent}', color=(1,1,1))
plt.plot([], label=f'Old % of population: {round((100*N_old)/(N_old+N_young),2)}', color=(1,1,1))

plt.xlabel("Time")
plt.ylabel("Number of people")
plt.title("Agent Based SIRQD Model with Age Profiles")
plt.legend(loc=0)

plt.savefig("./Plots/AgentAgeProfileSIRQDModel.png")