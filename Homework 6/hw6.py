import random                                                                                          # Extract the random number generator
import numpy as np                                                                                     # Extract the number pi

for precision_exponent in range(-1, -7 - 1, -1):                                                       # For the precision exponents between -1 to -7, inclusive
    pi_estimates, sum_pi_estimate = [], 0.0                                                            # Set up an array for the pi estimates within each of the 100 iterations of 10000 points of a quarter circle inscribed in a square
    for iterations in range(100):                                                                      # For each iteration, up to 100 iterations
        points_in_circle, points_in_square = 0, 0                                                      # Set up the number of points in the circle and square
        for points in range(10000):                                                                    # For each point, up to 10000 points
            if random.random()**2 + random.random()**2 <= 1: points_in_circle += 1                     # If the distance between the origin and a random point is at most 1, this point lies in the circle
            points_in_square += 1                                                                      # The point always lies inside of the square
            if abs(np.pi - 4 * points_in_circle / points_in_square) < 10**precision_exponent:          # If the absolute difference between pi and the estimated value of pi is at most the desired decimal precision for the first time
                pi_estimates.append(4 * points_in_circle / points_in_square)                           # Add this estimate for pi into the pi estimates array
                break                                                                                  # Break out of this iteration
    if len(pi_estimates) == 0: print(f"{10**precision_exponent} no success")                           # If the length of the array for the pi estimates is 0, then there were no values of pi that were captured with the desired precision
    else:                                                                                              # Otherwise,
        for estimate in pi_estimates: sum_pi_estimate += estimate                                      # Take the sum of all estimates
        average_pi_estimate = sum_pi_estimate / len(pi_estimates)                                      # Take the average of all estimates
        print(f"{10**precision_exponent} success {len(pi_estimates)} times {average_pi_estimate}")     # Print the average estimated value of pi at the desired precision with the number of iterations that first reaches the desired precision