'''
The death rate from a disease is not always constant.
If the number of people in hospital saturates the availability of hospital beds,
then it is expected that the death rate would increase.
This simulation implements this scenario, inside of a SIRQD simulation.
The parameter hospital_limit controls when the hospital system is saturated.
The parameter hospital_factor controls by what factor the death rate increase when the hospital system is saturated.
It can be run with or without animation by changing the ANIMATION_FLAG constant to True or False.
When the hospital limit is reached the animation will display the text "Hospital Limit Reached".
The results are immediatly plotted and the plot saved in the Plots folder.
'''
import numpy as np
import pygame
import sys
from pygame.locals import *
import matplotlib.pyplot as plt
import agents

ANIMATION_FLAG = True  # Change this depending on if you want an animation or not.

#------------------- Tunable Parameters ----------------------------------------------------

width, height = 800, 600 # This determines the size of the environment for the agents, as well as the animation window
radius = 15.0 # This determines the size of the agents

T = 500 # The length of time the simulation will run for. 2000 works well for status model.

# The disease parameters
gamma = 0.015 # The rate of recovery
beta = 0.55 # The infection rate
mu = 0.015 # The death rate
kappa = 0.2 # The quarantine rate

N = 100 # The total number of agents
init_I = 5 # The number of Infectious agents at beginning of simulation

hospital_limit = 15 # The number of infectious people there can be before hospital is overwhelmed
hospital_factor = 2 # The factor that the death rate is increased by when hospital limit is reached
#-------------------------------------------------------------------------------------------

WHITE = (255, 255, 255)
if ANIMATION_FLAG: # Some set up for animation
	screen = pygame.display.set_mode((width,height))
	screen.fill(WHITE)
	clock = pygame.time.Clock()
	pygame.font.init()
	myfont = pygame.font.Font(None, 20)
	text = myfont.render('Hospital Limit Reached', False, (0,0,0))	


# This set ups the simulation using a function defined in agents.py
population = agents.create_SIRQD_population_with_hospital_limit(N, init_I, radius, beta, gamma, mu, kappa, width, height, hospital_factor)


# Arrays to store the number of agents in each category at each time step
Sarray = np.zeros(T)
Iarray = np.zeros(T)
Rarray = np.zeros(T)
Darray = np.zeros(T)
Qarray = np.zeros(T)

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
			if i == 0:
				person.status_update()
			if i>0 and Iarray[i-1] > hospital_limit:
				person.hospital_status_update()
			else:
				person.status_update()
		
		person.position_update()

		if ANIMATION_FLAG:
			person.draw(screen)	
			if i> 0 and Iarray[i-1] > hospital_limit:
				screen.blit(text, (10,10))

		if person.status == 'S':
			Sarray[i] += 1
		elif person.status == 'I':
			Iarray[i] += 1
		elif person.status == 'R':
			Rarray[i] += 1
		elif person.status == 'D':
			Darray[i] += 1
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

for i in range(T-1):
	if Iarray[i] > hospital_limit:
		plt.fill_betweenx(y=[0,N], x1=[i,i], x2=[i+0.9,i+0.9], color=(0.3,0.3,0.3), alpha=0.05)
plt.plot([], label='Hospital Limit Exceeded', color=(0.3,0.3,0.3), alpha=0.2)

plt.xlabel("Time")
plt.ylabel("Number of people")
plt.title("Agent Based SIRQD Model with Hospital Limit")
leg = plt.legend(loc=0)
leg.get_lines()[-1].set_linewidth(7)
plt.savefig("./Plots/AgentHospitalLimitSIRQDModel.png")