import numpy as np
import agent_sim

width, height = 600, 600

T = 5000

gamma = 0.0015
beta = 0.05
radius = 10.0
init_S = 95
init_I = 5


repeats = 10

data = np.zeros([repeats*T,3])

for k in range(repeats):

	population = agent_sim.setup_simulation(init_S, init_I, radius, beta, gamma, width, height)

	for i in range(T):

		for person in population:
			for otherperson in population:
				if person==otherperson:
					continue
				person.infect(otherperson)
			person.update()

			if person.SIR == 'S':
				data[i + k*T, 0] += 1
			elif person.SIR == 'I':
				data[i + k*T, 1] += 1
			elif person.SIR == 'R':
				data[i + k*T, 2] += 1


np.savetxt('AgentData.csv', data, fmt = '%.1f', delimiter=",", header="S,I,R")


