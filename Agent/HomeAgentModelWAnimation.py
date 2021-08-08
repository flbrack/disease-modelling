import numpy as np
import pygame
import sys
from pygame.locals import *
import matplotlib.pyplot as plt
import agents
from random import random

ANIMATION_FLAG = True

WHITE = (255,255,255)
width, height = 800, 600

T = 5000

gamma = 0.0015
beta = 0.05

init_S = 200
init_I = 10

super_spreaders = 10
home_people = init_S + init_I - super_spreaders

people_per_home = 10
home_number = home_people // people_per_home

radius = 10.0
home_radius = 60.0

columns = 8

overlap = 50
w_offset = (overlap)/2
h_offset = (overlap)/2

homes = []
for i in range(columns):
	for j in range(home_number//columns):
		homes.append(np.array([w_offset + home_radius + i*(width-overlap)//columns, h_offset + home_radius+j*(height-overlap)//(home_number//columns)]))


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

		population.append( agents.HomePerson(position=np.array([x,y]), velocity=np.array([xspeed, yspeed]), home=home, home_size=home_radius, status='S', \
			radius=radius , gamma=gamma, beta=beta, width=width, height=height) )



for person in agents.setup_simulation(super_spreaders,0, radius=radius, beta=beta,gamma=gamma,height=height,width=width):
	population.append(person)


agents.initial_infection(init_I, population)

Sarray = np.zeros(T)
Iarray = np.zeros(T)
Rarray = np.zeros(T)

super_spreader_array = np.zeros(T)


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

		if person.status == 'S':
			Sarray[i] += 1
		elif person.status == 'I':
			Iarray[i] += 1
			if type(person) == agents.Person:
				super_spreader_array[i] += 1
		elif person.status == 'R':
			Rarray[i] += 1

	pygame.display.update()
	screen.fill(WHITE)
	for home in homes:
		pygame.draw.circle(screen, color=(0,0,0) ,center= home, radius = 2)
		pygame.draw.circle(screen, color=(0,0,0) ,center= home, radius = home_radius, width=1)	


plt.plot(Sarray, label='Susceptible', color=(0,0,1))
plt.plot(Iarray, label='Infected', color=(0,1,0))
plt.plot(Rarray, label='Recoverd', color=(1,0,0))
plt.plot(super_spreader_array, label="Super Spreader", color="black")

plt.xlabel("Time")
plt.ylabel("Number of people")
plt.title("Agent Based status Model")
plt.legend(loc=0)

plt.savefig("./Plots/HomeAgentWOverlapAnimated.png")