# Import necessary packages for calculations
import numpy as np                                                              # For extracting the actual value of pi
from scipy.integrate import quad                                                # For extracting the quadrature integration function

# Definite integrator to evaluate a definite integral with a function from a lower bound to an upper bound
def definite_integrator(function, lower_bound, upper_bound):
    result, error = quad(function, lower_bound, upper_bound)                    # Integrate the function with respect to given variable; change bounds here                                            
    print(f"Pi is {format(np.pi, '.8f')}")                                      # Print the value of pi as a floating point to 8 decimal places
    print(f"Difference from numpy.pi is: {format(np.pi - result, '.15f')}")     # Print the value of the difference between the actual and theoretical values of pi as a floating point to 15 decimal places

##########################################################################################################################################################
# NORMAL: Result from normal infinite integral integration

# definite_integrator(lambda x: 1 / ((1 + x) * np.sqrt(x)), 0, np.inf)
##########################################################################################################################################################

##########################################################################################################################################################
# REQUIRED: Result from using only the special substitution to convert infinite limit integral to definite integral

# Preliminary mathematical work: Integral from 0 to Infinity of dx/((1 + x)sqrt(x)) = pi
# Step 1: Changing the bounds of integration to turn the infinite limit integral into a definite integral
#         Let u = x/(1 + x), x = u/(1 - u), dx = 1/(1 - u)^2 du
#         Integral from 0 to Infinity of dx/((1 + x) sqrt(x)) = Integral from 0 to 1 of (du/(1 - u)^2)/((1 + u/(1 - u))sqrt(u/(1 - u)))
#                                                             = Integral from 0 to 1 of du/((1 + u/(1 - u))sqrt(u/(1 - u))(1 - u)^2)
#                                                             = Integral from 0 to 1 of du/sqrt(u(1 - u))
# Step 2: The implementation of the integral found by using the method in Step 1 is shown below.

definite_integrator(lambda x: 1 / np.sqrt(x * (1 - x)), 0, 1)
##########################################################################################################################################################

##########################################################################################################################################################
# IMPROVED (Version 1): Result from using an intermediate u-substitution before doing the special substitution to convert infinite limit integral to definite integral

# Preliminary mathematical work: Integral from 0 to Infinity of dx/((1 + x)sqrt(x)) = pi
# Step 1: U-substitution
#         Let u = sqrt(x), u^2 = x, du = 1/(2sqrt(x)) dx, dx = 2u du
#         Integral from 0 to Infinity of dx/((1 + x) sqrt(x)) = Integral from 0 to Infinity of 2u/((1 + u^2)u) du
#                                                             = Integral from 0 to Infinity of 2/(1 + u^2) du
# Step 2: The implementation of the integral found by using the method in Step 1 is shown below.

# definite_integrator(lambda x: 2 / (1 + x**2), 0, np.inf)
##########################################################################################################################################################

##########################################################################################################################################################
# IMPROVED (Version 2): Result from using an intermediate u-substitution before doing the special substitution to convert infinite limit integral to definite integral

# Preliminary mathematical work: Integral from 0 to Infinity of dx/((1 + x)sqrt(x)) = pi
# Step 1: U-substitution
#         Let u = sqrt(x), u^2 = x, du = 1/(2sqrt(x)) dx, dx = 2u du
#         Integral from 0 to Infinity of dx/((1 + x) sqrt(x)) = Integral from 0 to Infinity of 2u/((1 + u^2)u) du
#                                                             = Integral from 0 to Infinity of 2/(1 + u^2) du
# Step 2: Changing the bounds of integration to turn the infinite limit integral into a definite integral
#         Let v = u/(1 + u), u = v/(1 - v), du = 1/(1 - v)^2 dv
#         Integral from 0 to Infinity of 2/(1 + u^2) du = Integral from 0 to 1 of 2/(1 + (v/(1 - v))^2) 1/(1 - v)^2 dv
#                                                       = Integral from 0 to 1 of 2/((1 - v)^2 + v^2) dv
# Step 3: The implementation of the integral found by using the method in Steps 1 and 2 is shown below.

# definite_integrator(lambda x: 2 / (x**2 + (x - 1)**2), 0, 1)
##########################################################################################################################################################