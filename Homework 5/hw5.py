import numpy as np                                                                                # For extracting methods for arrays
import matplotlib.pyplot as plt                                                                   # For extracting plotting functions
from scipy.integrate import odeint                                                                # For extracting the ordinary differential equation solver

T_POINTS = np.linspace(0, 10, 100)                                                                # Constant time interval spacing for each plot of each differential equation problem

# Problem 1: Solving y' = cos(x), y(0) = 1
def Problem1(y, t):
    return np.cos(t)

y_points = odeint(Problem1, 1, T_POINTS)                                                          # Invoke the ordinary differential equation solver (first-order)
plt.plot(T_POINTS, y_points)                                                                      # Plot the solution to the differential equation (y)
plt.xlabel('Time (t)')
plt.xlim(-1, 11)
plt.ylabel('y')
plt.ylim(-1, 3)
plt.title('Problem 1: Solving y\' = cos(x), y(0) = 1')
plt.show()

# Problem 2: Solving y' = -y + t^2e^(-2t) + 10, y(0) = 0
def Problem2(y, t):
    return -y + t**2 * np.exp(-2 * t) + 10

y_points = odeint(Problem2, 0, T_POINTS)                                                          # Invoke the ordinary differential equation solver (first-order)
plt.plot(T_POINTS, y_points)                                                                      # Plot the solution to the differential equation (y)
plt.xlabel('Time (t)')
plt.xlim(-1, 11)
plt.ylabel('y')
plt.ylim(-1, 11)
plt.title('Problem 2: Solving y\' + y = t^2e^(-2t) + 10, y(0) = 0')
plt.show()

# Problem 3: Solving y'' + 4y' + 4y = 25cos(t) + 25sin(t), y(0) = 1, y'(0) = 1
# System of Differential Equations
# Let z = y'; then z' = y'' = -4z - 4y + 25cos(t) + 25sin(t)
# Resulting System of Differential Equations
# y' = z
# z' = y'' = -4z - 4y + 25cos(t) + 25sin(t)
# r = [r[0], r[1]] = [y, z] = [y, y']
def Problem3(r, t):
    return [r[1], -4 * r[0] - 4 * r[1] + 25 * np.cos(t) + 25 * np.sin(t)]

y_points, y_prime_points = odeint(Problem3, [1, 1], T_POINTS).T                                   # Invoke the ordinary differential equation solver (second-order)
plt.plot(T_POINTS, y_points, label = 'y')                                                         # Plot the solution to the differential equation (y)
plt.plot(T_POINTS, y_prime_points, label = 'y\'')                                                 # Plot the derivative of the solution to the differential equation (y')
plt.xlabel('Time (t)')
plt.xlim(-1, 11)
plt.ylabel('y')
plt.ylim(-11, 11)
plt.title('Problem 3: Solving y\'\' + 4y\' + 4y = 25cos(t) + 25sin(t), y(0) = 1, y\'(0) = 1')
plt.legend()
plt.show()