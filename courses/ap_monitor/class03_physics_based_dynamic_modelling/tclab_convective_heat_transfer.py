import datetime

import numpy as np
import matplotlib.pyplot as plt
import tclab
import time

from gekko import GEKKO

n = 300  # Number of second time points (5 min)
tm = np.linspace(0,n,n+1) # Time values

# data
lab = tclab.TCLab()
T1 = [lab.T1]
lab.Q1(50)
start_time = datetime.datetime.now()
for i in range(n):
    time.sleep(1)
    elapsed_time = datetime.datetime.now() - start_time
    t1 = lab.T1
    print(f"{elapsed_time}: {t1}")
    T1.append(t1)
lab.close()

# Simulate with GEKKO
Q = 50    # % of heater power
m = 0.004  # kg
U = 10  # W/m2-K
A = 0.0012  # m2
c_p = 500  # J / kg - K
T_a = 23  # deg C
alpha = 0.01  # W/%

model = GEKKO(remote=False)
model.time = tm
T = model.Var(T_a)
model.Equation(m * c_p * T.dt() == U * A * (T_a - T) + alpha * Q)
model.options.IMODE = 4
model.solve(disp=False)


# Plot results
plt.figure(1)
plt.plot(tm, T,'b.',label='Simulated (GEKKO)')
plt.plot(tm, T1,'r.',label='Measured')
plt.ylabel('Temperature (degC)')
plt.xlabel('Time (sec)')
plt.legend()
plt.show()