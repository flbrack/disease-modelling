'''
This runs repeated simulations of the model with just the base Person agent that's defined in agents.py.
The same simulation as is run in SimpleAgentModel.py.
As these are repeated simulations, and can take a bit of time, there is no option to animate.
If an animation is required, us the SimpleAgentModel.py script.
The data from the simulations is written to a file and saved in the data folder.
'''
import numpy as np
import agents

width, height = 600, 600

T = 5000

gamma = 0.015
beta = 0.05
radius = 10.0
init_S = 95
init_I = 5


repeats = 10

data = np.zeros([repeats*T,3])

for k in range(repeats):

	population = agents.create_SIR_population(init_S, init_I, radius, beta, gamma, width, height)

	for i in range(T):

		for person in population:
			for otherperson in population:
				if person==otherperson:
					continue
				person.infect(otherperson)
			if i % 10 == 0:
				person.status_update()
			
			person.position_update()

			if person.status == 'S':
				data[i + k*T, 0] += 1
			elif person.status == 'I':
				data[i + k*T, 1] += 1
			else:
				data[i + k*T, 2] += 1


np.savetxt('Data/RepeatedSIRModel.csv', data, fmt = '%.1f', delimiter=",", header="S,I,R")