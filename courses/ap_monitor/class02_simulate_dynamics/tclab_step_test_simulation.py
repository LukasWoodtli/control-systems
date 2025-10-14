import numpy as np
import matplotlib.pyplot as plt
import tclab
import time
from gekko import GEKKO
from scipy.integrate import odeint

n = 300  # Number of second time points (5 min)
tm = np.linspace(0,n,n+1) # Time values

# data
lab = tclab.TCLab()
T1 = [lab.T1]
lab.Q1(50)
for i in range(n):
    time.sleep(1)
    print(lab.T1)
    T1.append(lab.T1)
lab.close()

# Model:
# tau_p * dT/dt = (T_a - T) + K_p * Q
# with:
Q = 50    # % of heater power
tau_p = 120 # sec
K_p = 0.8   # degC / %
T_a = 23    # degC

# Simulation GEKKO
m = GEKKO(remote=False)
m.time = tm
TC = m.Var(23)
m.Equation(tau_p * TC.dt() == (T_a-TC)+ K_p * Q)
m.options.IMODE = 4
m.solve(disp=False)

# Simulation scipy.odeint
def model(TC,t):
    dTCdt = ((T_a - TC) + K_p * Q)/tau_p
    return dTCdt
T_sim = odeint(model,T_a,tm)



# Plot results
plt.figure(1)
plt.plot(tm,TC,'b.',label='Simulated (GEKKO)')
plt.plot(tm,T_sim,'y:',label='Simulated (odeint)')
plt.plot(tm,T1,'r.',label='Measured')
plt.ylabel('Temperature (degC)')
plt.xlabel('Time (sec)')
plt.legend()
plt.show()
