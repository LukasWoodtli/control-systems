# min x_1 * x_4 * (x_1 + X_2 + x_3) + x_3
# s.t.
# x_1 * x_2 * x_3 * x_4 >= 25
# x_1^2 + x_2^2 + x_3^2 + x_4^2 = 40
# 1 <= x_i <= 5
# Starting point (1,5,5,1)

import numpy as np
from scipy.optimize import minimize

def objective(x):
    # Python arrays are zero-indexed
    x_1 = x[0]
    x_2 = x[1]
    x_3 = x[2]
    x_4 = x[3]
    return x_1 * x_4 * (x_1 + x_2 + x_3) + x_3

def constraint0(x):
    # Python arrays are zero-indexed
    x_1 = x[0]
    x_2 = x[1]
    x_3 = x[2]
    x_4 = x[3]
    return x_1 * x_2 * x_3 * x_4 - 25

def constraint1(x):
    sum_sq = 40
    # Python arrays are zero-indexed
    x_1 = x[0]
    x_2 = x[1]
    x_3 = x[2]
    x_4 = x[3]
    return sum_sq - (x_1**2 + x_2**2 + x_3**2 + x_4**2)

# initial guess
x0 = [1, 5, 5, 1]
print("Objective with initial guess: ", objective(x0))

# bounds
b = (1.0, 5.0)
bounds = (b, b, b, b)

# constraint definitions
con1 = {'type': 'ineq', 'fun': constraint0}
con2 = {'type': 'eq', 'fun': constraint1}
cons = (con1, con2)

# Minimize
sol = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=cons)

print('Solution: ', sol.fun)
print('x (for solution): ', sol.x)
