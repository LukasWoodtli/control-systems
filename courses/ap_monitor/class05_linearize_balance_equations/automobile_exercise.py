
print("analytic solution")
import sympy as sp
sp.init_printing()
# define symbols
v,u = sp.symbols(['v','u'])
Fp,rho,Cd,A,m = sp.symbols(['Fp','rho','Cd','A','m'])
# define equation
eqn = Fp*u/m - rho*A*Cd*v**2/(2*m)

print(sp.diff(eqn,v))
print(sp.diff(eqn,u))


print(20*"=")
print("numeric solution")
from scipy.differentiate import derivative
m = 700.0   # kg
Cd = 0.24
rho = 1.225 # kg/m^3
A = 5.0     # m^2
Fp = 30.0   # N/%pedal
u = 40.0    # % pedal
v = 50.0    # km/hr (change this for SS condition)
def fv(v):
    return Fp*u/m - rho*A*Cd*v**2/(2*m)
def fu(u):
    return Fp*u/m - rho*A*Cd*v**2/(2*m)

print('Approximate Partial Derivatives')
print(derivative(fv,v,initial_step=1e-4).df)
print(derivative(fu,u,initial_step=1e-4).df)

print('Exact Partial Derivatives')
print(-A*Cd*rho*v/m) # exact d(f(u,v))/dv
print(Fp/m) # exact d(f(u,v))/du


# simulate step response of vehicle model

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# define model
def vehicle(v,t,u,load):
    # inputs
    #  v    = vehicle velocity (m/s)
    #  t    = time (sec)
    #  u    = gas pedal position (0% to 100%)
    #  load = passenger load + cargo (kg)
    Cd = 0.24    # drag coefficient
    rho = 1.225  # air density (kg/m^3)
    A = 5.0      # cross-sectional area (m^2)
    Fp = 30      # thrust parameter (N/%pedal)
    m = 500      # vehicle mass (kg)
    # calculate derivative of the velocity
    dv_dt = (1.0/(m+load)) * (Fp*u - 0.5*rho*Cd*A*v**2)
    return dv_dt

tf = 60.0                 # final time for simulation
nsteps = 61               # number of time steps
delta_t = tf/(nsteps-1)   # how long is each time step?
ts = np.linspace(0,tf,nsteps) # linearly spaced time vector

# simulate step test operation
step = np.zeros(nsteps) # u = valve % open
step[11:] = 50.0       # step up pedal position
# passenger(s) + cargo load
load = 200.0 # kg
# velocity initial condition
v0 = 0.0
# for storing the results
vs = np.zeros(nsteps)

# simulate with ODEINT
for i in range(nsteps-1):
    u = step[i]
    v = odeint(vehicle,v0,[0,delta_t],args=(u,load))
    v0 = v[-1]   # take the last value as initial condition
    vs[i+1] = v0 # store the velocity for plotting

# plot results
plt.figure()
plt.subplot(2,1,1)
plt.plot(ts,vs,'b-',linewidth=3)
plt.ylabel('Velocity (m/s)')
plt.legend(['Velocity'],loc=2)
plt.subplot(2,1,2)
plt.plot(ts,step,'r--',linewidth=3)
plt.ylabel('Gas Pedal')
plt.legend(['Gas Pedal (%)'])
plt.xlabel('Time (sec)')
plt.show()