import numpy as np
import matplotlib.pyplot as plt
import agents

width, height = 600, 600

T = 5000

gamma = 0.0015
beta = 0.05
radius = 10.0
init_S = 198
init_I = 2

population = agents.setup_simulation(init_S, init_I, radius, beta, gamma, width, height)

Sarray = np.zeros(T)
Iarray = np.zeros(T)
Rarray = np.zeros(T)


for i in range(T):

	for person in population:
		for otherperson in population:
			if person==otherperson:
				continue
			person.infect(otherperson)
		person.update()

		if person.SIR == 'S':
			Sarray[i] += 1
		elif person.SIR == 'I':
			Iarray[i] += 1
		elif person.SIR == 'R':
			Rarray[i] += 1



plt.plot(Sarray, label='Susceptible', color=(0,0,1))
plt.plot(Iarray, label='Infected', color=(0,1,0))
plt.plot(Rarray, label='Recoverd', color=(1,0,0))

plt.xlabel("Time")
plt.ylabel("Number of people")
plt.title("Agent Based SIR Model")
plt.legend(loc=0)

plt.savefig("./Plots/SimpleModel.png")