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
m.options.IMODE = 4
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

m.options.IMODE = 4
m.solve()
plt.plot(m.time, y, 'g:')

plt.xlabel('time')
plt.ylabel('y(t)')
plt.show()

# calculate the steady state
m.options.imode = 3
m.solve(disp=False)
print('Steady state:', y.value)


## Problem 2
# 5*dy(t)/dt = -y(t) + u(t)
m = GEKKO(remote=False)
m.time = np.linspace(0, 40, 401)

u_step = np.zeros(len(m.time))
u_step[100:] = 2.
u = m.Param(u_step)  # Step input at t=10

y = m.Var(1.)
m.Equation(5 * y.dt() == -y + u)

m.options.IMODE = 4
m.solve(disp=False)

plt.plot(y, 'r-', label='Output y(t)')
plt.plot(u, 'b-', label='Input u(t)')
plt.xlabel('time')
plt.ylabel('values')
plt.legend()
plt.show()


## Problem 3
# dx(t)/dt = 3 * exp(-t)
# dy(t)/dt = 3 - y(t)
# x(0) = 0
# y(0) = 0
m = GEKKO(remote=False)
m.time = np.linspace(0, 5)

t = m.Var(0.) # t is a variable in the first ODE
x = m.Var(0.)
y = m.Var(0.)
m.Equation(t.dt() == 1)
m.Equation(x.dt() == 3 * m.exp(-t))
m.Equation(y.dt() == 3 - y)

m.options.IMODE = 4
m.options.NODES = 3
m.solve(disp=False)

plt.plot(t, x, 'b.', label='dx(t)/dt = 3 * exp(-t)')
plt.plot(t, y, 'r--', label='dy(t)/dt = -y + 3')
plt.xlabel('time')
plt.ylabel('response')
plt.legend()
plt.show()


## Problem 4
# 2 * dx(t)/dt = -x(t) + u(t)
# 5 * dy(t)/dt = -y(t) + x(t)
# u=2*S(t - 5)
# x0 = 0
# y0 = 0
m = GEKKO(remote=False)
m.time = np.linspace(0, 40, 401)

t = m.Var(0.)
x = m.Var(0.)
y = m.Var(0.)

u_step = np.zeros(len(m.time))
u_step[50:] = 2.
u = m.Param(u_step)

m.Equation(t.dt() == 1)
m.Equation(2 * x.dt() == -x + u)
m.Equation(5 * y.dt() == - y + x)

m.options.IMODE = 4
m.solve(disp=False)

plt.plot(m.time, u, 'g:', label='u(t)')
plt.plot(m.time, x, 'b-', label='x(t)')
plt.plot(m.time, y, 'r--', label='y(t)')
plt.xlabel('time')
plt.ylabel('values')
plt.legend()
plt.show()
