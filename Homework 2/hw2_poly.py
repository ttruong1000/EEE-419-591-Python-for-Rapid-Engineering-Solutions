# Import necessary packages for calculations
import numpy as np                                                                                    # For extracting the actual value of pi
from scipy.integrate import quad                                                                      # For extracting the quadrature integration function
import matplotlib.pyplot as plt                                                                       # For extracting plotting functions

# Initialize constants for numerical integration
START = 0                                                                                             # Starting value of r
END = 5                                                                                               # Ending value of r
STEP_SIZE = 0.01                                                                                      # Step size of r

# Plot the integral of a general quadratic function with real coefficients a, b, c
# Integral from 0 to r of ax^2 + bx + c dx for r in the interval [0, 5] = ar^3/3 + br^2/2 + rc
# Values of this integral are in the interval [0, 125a/3 + 25b/2 + 5c]
def plot_general_quadratic_integral(a, b, c):
    r_values = np.arange(START, END, STEP_SIZE)                                                       # Generate r values from the start, end, and step size values
    length =  len(r_values)                                                                           # Compute the number of r values to process for numerical integration
    quadratic_values = np.zeros(length, float)                                                        # Initialize values for storing quadratic output values
    for index in range(length):                                                                       # For each r value
        quadratic_values[index], error = quad(lambda x: a * x**2 + b * x + c, 0, r_values[index])     # Store the result of the integral evaluated at r into the quadratic output array; store the error in a dummy variable 
    return plt.plot(r_values, quadratic_values, label = f"Integral of {a}x^2 + {b}x + {c}")           # Return the plot of the integral of the general quadratic function with its corresponding label

# Plot the integral of a general quadratic function with specific real coefficients a, b, c
plot_general_quadratic_integral(2, 3, 4)                                                              # a = 2, b = 3, c = 4
plot_general_quadratic_integral(2, 1, 1)                                                              # a = 2, b = 1, c = 1
plt.xlabel("X-Value")
plt.ylabel("Y-Value")
plt.title("Integral of a General Quadratic Equation From 0 to r (for r in the Interval [0, 5])")
plt.legend()
plt.show()