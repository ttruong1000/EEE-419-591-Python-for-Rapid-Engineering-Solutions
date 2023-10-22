# Import necessary packages for calculations
import numpy as np                                                                                        # For real roots

# Exercise 2.13 - Factorial function
# def factorial(n):
#     if n == 1:
#         return 1
#     else:
#         return n * factorial(n - 1)

# Finding the square root of a number via Babylonian recursion
def my_sqrt(n, N, epsilon):
    n_next = (n + N / n) / 2                                                                              # Store next term in a variable
    if np.abs(n_next - n) < epsilon:                                                                      # If the positive difference in two consecutive terms is less than the desired tolerance
        return n_next                                                                                     # Return this approximation
    else:                                                                                                 # Otherwise
        return my_sqrt(n_next, N, epsilon)                                                                # Evaluate the next term recursively

# Input processing
N = int(input("Enter a number whose square root is desired: "))
n_0 = int(input("Enter an initial guess: "))

# Tolerance
EPSILON = 0.01                                                                                            # Choose epsilon here (input 10^(-n), where n is the amount of decimal digits for precision)

print(f"The square root of {N} is {round(my_sqrt(n_0, N, EPSILON), np.abs(int(np.log10(EPSILON))))}")     # Print Babylonian square root approximation 