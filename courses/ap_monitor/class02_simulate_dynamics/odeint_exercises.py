from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

# Function (dy/dt)
def model(y, t, k):
    dydt = -k * y
    return dydt

# Initial condition
y0 = 5

# Time points
t = np.linspace(0, 20)

# solve ODE
y1 = odeint(model, y0, t, args=(0.1,))
y2 = odeint(model, y0, t, args=(0.2,))
y3 = odeint(model, y0, t, args=(0.5,))

# Plot results
plt.plot(t, y1)
plt.plot(t, y2)
plt.plot(t, y3)
plt.xlabel('Time')
plt.ylabel('y(t)')
plt.show()


# Exercises

t = np.linspace(0, 20)

## Problem 1
# dy(t)/dt = -y(t) + 1
# y(0) = 0

def model1(y, t):
    return -y + 1

y0 = 0

y1 = odeint(model1, y0, t)
plt.plot(t, y1)
plt.xlabel('Time')
plt.ylabel('y(t)')
plt.show()


## Problem 2
# 5*dy(t)/dt = -y(t) + u(t)
# => dy(t)/dt = -y(t)/5 + u(t)/5
# y(0) = 1

def u(t):
    if t < 10:
        u = 0
    else:
        u = 2
    return u

def model2(y, t):
    return -y/5 + u(t)/5

y0 = 1

y2 = odeint(model2, y0, t)
plt.plot(t, y2)
plt.plot(t, [u(t) for t in t], 'r--', label='u(t)')
plt.xlabel('Time')
plt.ylabel('y(t)')
plt.show()

## Problem 3
# dx(t)/dt = 3 * exp(-t)
# dy(t)/dt = 3 - y(t)
# x0 = 0
# y0 = 0

def model3_1(x, t):
    return 3 * np.exp(-t)

def model3_2(y, t):
    return 3 - y

x0 = 0
y0 = 0

y3_1 = odeint(model3_1, x0, t)
y3_2 = odeint(model3_2, y0, t)

plt.plot(t, y3_1, 'r--', label='x(t)')
plt.plot(t, y3_2, 'b.', label='y(t)')
plt.xlabel('Time')
plt.show()

## Problem 4
# 2 * dx(t)/dt = -x(t) + u(t)
# => dx(t)/dt = -x(t)/2 + u(t)/2
# 5 * dy(t)/dt = -y(t) + x(t)
# => dy(t)/dt = -y(t)/5 + x(t)/5
# u=2*S(t - 5)
# x0 = 0
# y0 = 0

def model4(z, t, u):
    x, y = z
    dxdt = -x/2 + u/2
    dydt = -y/5. + x/5
    dzdt = [dxdt, dydt]
    return dzdt

x0 = 0
y0 = 0
z0 = [x0, y0]

n = 401
t = np.linspace(0, 40, n)

# step input
u = np.zeros(n)
u[50:] = 2.0  # u(t) = 2 for t >= 5

x = np.empty_like(t)
y = np.empty_like(t)

# initial conditions
x[0] = x0
y[0] = y0

for i in range(1, n):
    tspan = [t[i-1], t[i]]
    z = odeint(model4, z0 , tspan, args=(u[i],))
    # store solution
    x[i] = z[1][0]
    y[i] = z[1][1]
    # update initial conditions for next step
    z0 = z[1]

plt.plot(t, u, 'g:', label='u(t)')
plt.plot(t, x, 'b-', label='x(t)')
plt.plot(t, y, 'r--', label='y(t)')
plt.xlabel('time')
plt.ylabel('values')
plt.legend(loc='best')
plt.show()