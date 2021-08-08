'''
This is for repeated simulations using the models with home agents and superspreaders.
There are no animations, as the script can take a while to run.
The data from the is written to a file in the data folder.
'''
import numpy as np
import agents
from random import random
from tqdm import tqdm

# Set up

width, height = 600, 600

T = 5000

gamma = 0.0015
beta = 0.05

init_S = 200
init_I = 10

super_spreaders = 10
home_people = init_S + init_I - super_spreaders

people_per_home = 5
home_number = home_people // people_per_home

radius = 10.0
home_radius = 70.0

columns = 5
offset = 10


homes = []
for i in range(columns):
	for j in range(home_number//columns):
		homes.append(np.array([offset + home_radius + i*width//columns, offset + home_radius+j*height//(home_number//columns)]))


# Running the Repeated Simulations

repeats = 10

data = np.zeros([repeats*T,4])

for k in tqdm( range(repeats) , desc="Loading…", ascii=False, ncols=75 ):

	population = []

	for i in  range(people_per_home):

		for home in homes:

			x = home[0] + (random()-0.5)*home_radius
			y = home[1] + (random()-0.5)*home_radius


			xspeed = (random() - 0.5)*2
			yspeed = (random() - 0.5)*2

			population.append( agents.HomePerson(position=np.array([x,y]), velocity=np.array([xspeed, yspeed]), home=home, home_size=home_radius, status='S', \
				radius=radius , gamma=gamma, beta=beta, width=600, height=600) )


	for person in agents.setup_simulation(super_spreaders,0, radius=radius, beta=beta,gamma=gamma,height=height,width=width):
		population.append(person)


	agents.initial_infection(init_I, population)

	for i in range(T):

		for person in population:
			for otherperson in population:
				if person==otherperson:
					continue
				person.infect(otherperson)
			person.update()

			if person.status == 'S':
				data[i + k*T, 0] += 1
			elif person.status == 'I':
				data[i + k*T, 1] += 1
				if type(person) == agents.Person:
					data[i + k*T, 3] += 1
			elif person.status == 'R':
				data[i + k*T, 2] += 1


np.savetxt('Data/HomeAgentWOverlap_70_Data.csv', data, fmt = '%.1f', delimiter=",", header="S,I,R,SuperSpreader")