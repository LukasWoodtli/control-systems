import numpy as np
from gekko import GEKKO
import matplotlib.pyplot as plt

# ODE: dy(t)/dt = -k * y(t)
m = GEKKO(remote=False)
k = m.Param() # constant
# Initial condition for y
y = m.Var(5.0)

m.Equation(y.dt() == -k * y)
m.time = np.linspace(0, 20)

# Solve the ODE
m.options.imode = 4
m.options.TIME_SHIFT = 0

k.value = 0.1
m.solve(disp=False)
plt.plot(m.time, y, 'r-', linewidth=2, label='k=0.1')

k.value = 0.2
m.solve(disp=False)
plt.plot(m.time, y, 'b--', linewidth=2, label='k=0.2')

k.value = 0.5
m.solve(disp=False)
plt.plot(m.time, y, 'g:', linewidth=2, label='k=0.5')

plt.xlabel('time')
plt.ylabel('y(t)')
plt.legend()
plt.show()


# Exercises

## Problem 1
# dy(t)/dt = -y(t) + 1
# y(0) = 0

m = GEKKO(remote=False)
# Initial condition for y
y = m.Var(0.)

m.Equation(y.dt() == -y + 1)
m.time = np.linspace(0, 5)

m.options.imode = 4
m.solve()
plt.plot(m.time, y, 'g:')

plt.xlabel('time')
plt.ylabel('y(t)')
plt.show()

# calculate the steady state
m.options.imode = 3
m.solve(disp=False)
print('Steady state:', y.value)