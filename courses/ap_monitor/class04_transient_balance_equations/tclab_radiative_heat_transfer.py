import datetime

import numpy as np
import matplotlib.pyplot as plt
import tclab
import time

from fontTools.misc.bezierTools import epsilon
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
epsilon = 0.9
sigma = 5.67e-8  # W/m2-K4
U = 5  # W/m2-K
A = 0.0012  # m2
c_p = 500  # J / kg - K
T_a = 23  # deg C
T_inf = 273.15 + T_a  # deg C
alpha = 0.01  # W/%

model = GEKKO(remote=False)
model.time = tm
T = model.Var(T_a)
TK = model.Intermediate(T+273.15)
conv = model.Intermediate(U*A*(T_a-T))
rad  = model.Intermediate(sigma*epsilon*A*(T_inf**4-TK**4))
loss = model.Intermediate(conv + rad)
gain = model.Intermediate(alpha*50)
model.Equation(m*c_p*T.dt()==conv+rad+gain)
model.options.NODES = 3
model.options.IMODE = 4
model.solve(disp=False)


# Plot results
plt.figure()
plt.subplot(2,1,1)
plt.plot(tm,T,'b-',label='Simulated')
plt.plot(tm,T1,'r.',label='Measured')
plt.ylabel(r'Temperature ($^oC$)')
plt.legend()
plt.subplot(2,1,2)
plt.plot(tm,conv,'g:',label='Convection')
plt.plot(tm,rad,'r--',label='Radiation')
plt.plot(tm,loss,'k-',label='Total Lost')
plt.text(150,-0.1,'Heater input = '+str(gain)+' W')
plt.ylabel(r'Heat Loss (W)')
plt.legend(loc=3)
plt.xlabel('Time (sec)')
plt.show()