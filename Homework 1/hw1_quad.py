# Import necessary packages for calculations
import numpy as np                                                  # For real roots
import cmath                                                        # For complex roots

# Tolerance
EPSILON = 0.000001                                                  # Choose epsilon here (input 10^(-n), where n is the amount of decimal digits for precision)

# Discriminant analysis
def quadratic_roots(a, b, c):
    if np.abs(b**2 - 4*a*c) < EPSILON:                              # If the discriminant is zero (or close to 0 in magnitude to a tolerance), roots are real and nondistinct (double root)
        print("Double root:", -b/(2*a))
    elif b**2 - 4*a*c > 0:                                          # If the discriminant is positive, roots are real and distinct
        print("Root 1:", (-b + np.sqrt(b**2 - 4*a*c))/(2*a))
        print("Root 2:", (-b - np.sqrt(b**2 - 4*a*c))/(2*a))
    else:                                                           # If the discriminant is negative, roots are complex conjugates
        print("Root 1:", (-b + cmath.sqrt(b**2 - 4*a*c))/(2*a))
        print("Root 2:", (-b - cmath.sqrt(b**2 - 4*a*c))/(2*a))

# Input processing
a = int(input("Input coefficient a: "))
b = int(input("Input coefficient b: "))
c = int(input("Input coefficient c: "))

quadratic_roots(a, b, c)                                            # Print roots to quadratic equation given coefficients