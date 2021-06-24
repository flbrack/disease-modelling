import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd

agentData = pd.read_csv("/Users/fionnbracken/Desktop/project-flbrack/Agent/Data/AgentData.csv", delimiter=",")

for k in range(10):
    agentData['S'][5000*k:5000+5000*k].plot(color='blue', use_index=False, alpha=0.5)
    agentData['I'][5000*k:5000+5000*k].plot(color='green', use_index=False, alpha=0.5)
    agentData['R'][5000*k:5000+5000*k].plot(color='red', use_index=False, alpha=0.5)
plt.legend(labels=['Susceptible', 'Infected', 'Recoverd'], loc=0)
plt.xlabel('Time')
plt.ylabel('People')
plt.title('Multiple Agent Based Simulations')
plt.savefig("./Plots/MultipleSIRSimuls.png")