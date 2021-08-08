import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

plt.rcParams['figure.figsize'] = 10, 8

plt.rcParams.update({
    "text.usetex": True,
    'font.size': 22
})


N = 1000 # Population
beta = 0.5 # Transmission rate
gamma = 0.04 # Recovery rate
mu = 0.03 # Death rate
kappa = 0.04 # Quarantine rate

# solve the system dy/dt = f(y, t)
def f(y, t):
    Si = y[0]
    Ii = y[1]
    Ri = y[2]
    Di = y[3]
    Qi = y[4]

    f0 = - ( beta * Si * Ii )/N
    f1 = ( beta * Si * Ii )/N - (gamma * Ii) - (mu * Ii) - (kappa * Ii)
    f2 = gamma * Ii + gamma * Qi
    f3 = mu * Ii + mu * Qi
    f4 = (kappa * Ii) - (mu * Qi) - (gamma * Qi)
    return [f0, f1, f2, f3, f4]

# initial conditions
I0 = 3           # initial susceptible
S0 = N-I0               # initial infected
R0 = 0
D0 = 0                 # initial recovered
X0 = 0
y0 = [S0, I0, R0, D0, Q0]     # initial condition vector
t  = np.linspace(0, 150., 1000)         # time grid

# solve the DEs
soln = odeint(f, y0, t)
S = soln[:, 0]
I = soln[:, 1]
R = soln[:, 2]
D = soln[:, 3]
Q = soln[:, 4]

# plot results
plt.figure()
plt.plot(t, S, label='Susceptible')
plt.plot(t, I, label='Infected')
plt.plot(t, R, label='Recovered')
plt.plot(t, D, label='Deceased')
plt.plot(t, Q, label='Quarantined')
plt.xticks([])
plt.yticks([])
plt.xlabel('Time')
plt.ylabel('Population')
plt.title(f'SIRQD Model: $\gamma$={gamma}, $\\beta$={beta}, $\mu$={mu}, $\kappa$={kappa}')
plt.legend(loc=0)
plt.savefig(f'./Plots/SIRQD_g={gamma}_b={beta}_m={mu}_k={kappa}.png')
