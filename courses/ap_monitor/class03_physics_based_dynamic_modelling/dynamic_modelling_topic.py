import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import odeint


def tank(Level, time, c, valve):
    rho = 1000.  # kg/m^3
    A = 1.0  # m^2, cross-sectional area of the tank
    dLevel_dt = c * valve / (A * rho)
    return dLevel_dt

t = np.linspace(0, 10, 101)


c = 50.
u = np.zeros(len(t))
u[21:70] = 100.0  # valve open between 2 and 7 seconds

Level0 = 0.0  # initially tank is empty

# init results
z = np.zeros(len(t))

for i in range(len(t)-1):
    v = u[i + 1]
    y = odeint(tank, Level0, [0, 0.1], args=(c, v))
    Level0 = y[-1]
    z[i + 1] = Level0

# plot results
plt.figure()
plt.subplot(2,1,1)
plt.plot(t,z,'b-',linewidth=3)
plt.ylabel('Tank Level')
plt.subplot(2,1,2)
plt.plot(t,u,'r--',linewidth=3)
plt.ylabel('Valve')
plt.xlabel('Time (sec)')
plt.show()
