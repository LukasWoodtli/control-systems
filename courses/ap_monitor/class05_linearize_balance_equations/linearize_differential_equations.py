# analytic solution with Python
import sympy as sp
sp.init_printing()
# define symbols
x,u = sp.symbols(['x','u'])
# define equation
dxdt = -x**2 + sp.sqrt(u)

print(sp.diff(dxdt,x))
print(sp.diff(dxdt,u))

# numeric solution with Python
import numpy as np
from scipy.differentiate import derivative
u = 16.0
x = 2.0
def pd_x(x):
    dxdt = -x**2 + np.sqrt(u)
    return dxdt
def pd_u(u):
    dxdt = -x**2 + np.sqrt(u)
    return dxdt

print('Approximate Partial Derivatives')
dx_approx = derivative(pd_x,x,initial_step=1e-4)
print(dx_approx.df)
du_approx = derivative(pd_u,u,initial_step=1e-4)
print(du_approx.df)

print('Exact Partial Derivatives')
print(-2.0*x) # exact d(f(x,u))/dx
print(0.5 / np.sqrt(u)) # exact d(f(x,u))/du
