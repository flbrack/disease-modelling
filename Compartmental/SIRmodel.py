import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

plt.rcParams['figure.figsize'] = 10, 8

N = 1000 # Population
beta = 0.5 # Infection rate
gamma = 0.04 # Recovery rate
init_outbreak = 0.003

# solve the system dy/dt = f(y, t)
def f(y, t):
    Si = y[0]
    Ii = y[1]
    Ri = y[2]

    f0 = - ( beta * Si * Ii )/N
    f1 = ( beta * Si * Ii )/N - gamma * Ii
    f2 = gamma * Ii
    return [f0, f1, f2]

# initial conditions
I0 = np.floor(N * init_outbreak)           # initial susceptible
S0 = N-I0               # initial infected
R0 = 0                 # initial recovered
y0 = [S0, I0, R0]     # initial condition vector
t  = np.linspace(0, 150., 1000)         # time grid

# solve the DEs
soln = odeint(f, y0, t)
S = soln[:, 0]
I = soln[:, 1]
R = soln[:, 2]

# plot results
plt.figure()
plt.plot(t, S, label='Susceptible')
plt.plot(t, I, label='Infected')
plt.plot(t, R, label='Recovered')
plt.xlabel('Days from outbreak')
plt.ylabel('Population')
plt.title('Disease Model - SIR')
plt.legend(loc=0)
plt.savefig('SIR.png')
